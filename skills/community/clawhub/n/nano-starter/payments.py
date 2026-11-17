"""The five tools, as plain functions. The MCP server is a thin shell over this.

Money is an integer count of raw everywhere below (1 XNO = 10**30 raw).
Decimal XNO strings are parsed by `wallet.xno_to_raw` and rendered by
`wallet.raw_to_xno`, both exact. No float touches a balance, an amount or
a comparison in this file. A double holds 53 bits of mantissa and a raw
balance needs up to 128, so a single float round-trip would silently
round away real money.
"""

import os

import blocks
import keystore as _keystore
import mandate as _mandate
import nanoaddr as _addr
import nanonode
import profiles
import wallet

#: The spec's error table uses `invalid_*`; nanoaddr's parser has always used
#: `bad_*`. Map at the boundary rather than renaming the parser's codes, which
#: are pinned by known-answer tests, and expose BOTH so neither contract breaks.
CANONICAL_REASON = {
    "bad_prefix": "invalid_prefix",
    "bad_length": "invalid_length",
    "bad_character": "invalid_charset",
    "bad_padding": "invalid_padding",
    "bad_checksum": "invalid_checksum",
    "not_a_string": "invalid_prefix",
    "empty": "invalid_prefix",
}

CUSTODY_SENTENCE = (
    "This key was generated in your process. It was not transmitted. "
    "No third party can spend from this address."
)

UNPAYABLE_SENTENCE = (
    "This address would be rejected by every Nano node - a payment sent to it can "
    "never arrive, and nothing is lost in transit because nothing is ever sent. "
    "Regenerate with create_address."
)

DEFAULT_MAX_SEND_XNO = "1.0"
MAX_RECEIVE_BLOCKS = 64


class ToolError(Exception):
    """A tool refusal with the spec's code and HTTP-ish status."""

    def __init__(self, reason: str, message: str, status: int = 400, **extra):
        super().__init__(message)
        self.reason = reason
        self.message = message
        self.status = status
        self.extra = extra

    def payload(self) -> dict:
        out = {"error": self.reason, "status": self.status, "message": self.message}
        out.update(self.extra)
        return out


# ---------------------------------------------------------------- offline

def validate_address(address: str) -> dict:
    """Offline. Never raises; a rejection says what a payment to it would do."""
    verdict = _addr.validate(address)
    if verdict["valid"]:
        candidate = str(address).strip()
        out = {
            "valid": True,
            "canonical": verdict["normalised"],
            "public_key": verdict["public_key"],
        }
        if candidate.startswith("xrb_"):
            out["prefix_normalised_from"] = "xrb_"
        return out
    return {
        "valid": False,
        "reason": CANONICAL_REASON.get(verdict["reason"], verdict["reason"]),
        "parser_reason": verdict["reason"],
        "message": "%s %s" % (verdict["message"].rstrip("."), UNPAYABLE_SENTENCE),
        "position": None,
    }


def require_valid(address: str) -> bytes:
    """Validate before anything else, and before any network call."""
    verdict = validate_address(address)
    if not verdict["valid"]:
        raise ToolError("invalid_address", verdict["message"], 400,
                        reason_detail=verdict["reason"])
    return bytes.fromhex(verdict["public_key"])


def create_address(label: str = None, store: str = "memory", path: str = None,
                   keys: _keystore.KeyStore = None) -> dict:
    """Offline. The seed and the private key are NEVER in the return value."""
    if store not in ("memory", "file"):
        raise ToolError("invalid_store", "store must be \"memory\" or \"file\", got %r" % store)
    if label is not None and len(str(label)) > 64:
        raise ToolError("invalid_label", "label must be at most 64 characters")
    if store == "file" and not path:
        raise ToolError("invalid_path", "store=\"file\" requires a path")

    account = wallet.create_wallet()
    private_key = bytes.fromhex(account["private_key"])
    keys = keys if keys is not None else _keystore.KeyStore()
    keys.put(private_key)

    if store == "file":
        try:
            written = keys.save(private_key, path)
        except _keystore.KeyStoreError as exc:
            raise ToolError(exc.reason, exc.message) from None
        stored = "file:%s" % written
    else:
        stored = "memory (lost on restart)"

    return {
        "address": account["address"],
        "public_key": account["public_key"],
        "label": label,
        "stored": stored,
        "custody": CUSTODY_SENTENCE,
        "validated": True,
    }


# ---------------------------------------------------------------- network

def balance(address: str, node: nanonode.NanoNode) -> dict:
    """Validate first. A bad address makes NO network call - assert that in tests."""
    require_valid(address)
    try:
        info = node.account_info(address)
        pending = node.receivable(address, MAX_RECEIVE_BLOCKS)
    except nanonode.NodeError as exc:
        raise ToolError(exc.reason, exc.message, 503) from None
    pending_raw = sum(int(block["amount_raw"]) for block in pending)
    return {
        "address": address,
        "balance_xno": _six(info.get("balance_raw", 0)),
        "pending_xno": _six(pending_raw),
        "block_count": int(info.get("block_count", 0)),
        "confirmed": bool(info.get("confirmed", True)),
    }


def receive(address: str, node: nanonode.NanoNode, keys: _keystore.KeyStore,
            max_blocks: int = 8, representative: str = None) -> dict:
    """Pocket receivable blocks. Receiving is not spending: no spend gate here.

    Each block is built, hashed and signed in this process; the node is
    handed an already-signed block and never the key.
    """
    public_key = require_valid(address)
    try:
        max_blocks = int(max_blocks)
    except (TypeError, ValueError):
        raise ToolError("invalid_max_blocks", "max_blocks must be an integer 1..64") from None
    if not 1 <= max_blocks <= MAX_RECEIVE_BLOCKS:
        raise ToolError("invalid_max_blocks",
                        "max_blocks must be between 1 and %d, got %d"
                        % (MAX_RECEIVE_BLOCKS, max_blocks))
    try:
        private_key = keys.get(address)
    except _keystore.KeyStoreError as exc:
        raise ToolError(exc.reason, exc.message) from None

    try:
        pending = node.receivable(address, max_blocks)
        info = node.account_info(address)
        balance_raw = int(info.get("balance_raw", 0))
        previous = bytes.fromhex(info["frontier"]) if info.get("frontier") else blocks.ZERO32
        rep_pk = _representative_pk(representative, info.get("representative"), public_key)

        received = []
        for block in pending:
            amount_raw = int(block["amount_raw"])
            balance_raw += amount_raw
            signed = blocks.build_signed(
                private_key, public_key, previous, rep_pk, balance_raw,
                bytes.fromhex(block["hash"]),
                "receive" if previous != blocks.ZERO32 else "open",
            )
            signed["work"] = node.work_generate(signed.pop("_work_root"))
            block_hash = signed.pop("_hash")
            node.process(dict(signed))
            previous = bytes.fromhex(block_hash)
            received.append({
                "block_hash": block_hash,
                "amount_xno": _six(amount_raw),
                "from": block.get("source"),
            })
        remaining = node.receivable(address, MAX_RECEIVE_BLOCKS)
    except nanonode.NodeError as exc:
        raise ToolError(exc.reason, exc.message, 503) from None

    return {
        "address": address,
        "received": received,
        "balance_xno": _six(balance_raw),
        "remaining_pending": len(remaining),
    }


def send(source: str, destination: str, amount_xno: str, idempotency_key: str,
         node: nanonode.NanoNode, keys: _keystore.KeyStore, sent: dict,
         env=None, representative: str = None) -> dict:
    """Gated. Refused outright unless NANO_WALLET_ALLOW_SEND is exactly "1".

    Never registered at all in the receive-only profile - see profiles.py.
    """
    env = os.environ if env is None else env
    if str(env.get("NANO_WALLET_ALLOW_SEND", "")).strip() != "1":
        raise ToolError(
            "spend_not_enabled",
            "this install cannot send. Set NANO_WALLET_ALLOW_SEND=1 to enable it. "
            "create_address, validate_address, balance and receive all work without it.",
            403,
        )

    source_pk = require_valid(source)
    require_valid(destination)
    destination_pk = bytes.fromhex(validate_address(destination)["public_key"])

    if not idempotency_key or len(str(idempotency_key)) > 64:
        raise ToolError("invalid_idempotency_key",
                        "idempotency_key is required and must be at most 64 characters")
    try:
        amount_raw = wallet.xno_to_raw(amount_xno)
    except ValueError as exc:
        raise ToolError("invalid_amount", str(exc)) from None
    if amount_raw <= 0:
        raise ToolError("invalid_amount", "amount must be greater than zero")

    limit_raw = wallet.xno_to_raw(env.get("NANO_WALLET_MAX_SEND_XNO") or DEFAULT_MAX_SEND_XNO)
    if amount_raw > limit_raw:
        raise ToolError(
            "send_limit_exceeded",
            "this install refuses to send more than %s XNO in one call "
            "(NANO_WALLET_MAX_SEND_XNO); asked for %s"
            % (wallet.raw_to_xno(limit_raw), wallet.raw_to_xno(amount_raw)),
            403,
        )

    previous_call = sent.get(str(idempotency_key))
    if previous_call is not None:
        if (previous_call["to"], previous_call["amount_raw"]) != (destination, amount_raw):
            raise ToolError(
                "idempotency_conflict",
                "idempotency_key %r was already used to send %s XNO to %s; a repeat with "
                "different parameters is refused"
                % (idempotency_key, _six(previous_call["amount_raw"]), previous_call["to"]),
                409,
            )
        return dict(previous_call["result"], replayed=True)

    guard = _mandate_guard(env, source)  # after the replay: a replay sends nothing
    if guard is not None:
        try:  # refuse before anything is signed; spend() re-checks at broadcast
            guard.check(destination, amount_raw)
        except _mandate.MandateRefused as exc:
            raise _mandate_refusal(exc) from None

    try:
        private_key = keys.get(source)
    except _keystore.KeyStoreError as exc:
        raise ToolError(exc.reason, exc.message) from None

    try:
        info = node.account_info(source)
        balance_raw = int(info.get("balance_raw", 0))
        if balance_raw < amount_raw:
            raise ToolError("insufficient_balance",
                            "balance is %s XNO, asked to send %s XNO"
                            % (_six(balance_raw), _six(amount_raw)),
                            409, available_xno=_six(balance_raw))
        if not info.get("frontier"):
            raise ToolError("insufficient_balance",
                            "this account has never received anything, so it has nothing "
                            "to send", 409, available_xno=_six(0))
        previous = bytes.fromhex(info["frontier"])
        rep_pk = _representative_pk(representative, info.get("representative"), source_pk)
        signed = blocks.build_signed(private_key, source_pk, previous, rep_pk,
                                     balance_raw - amount_raw, destination_pk, "send")
        signed["work"] = node.work_generate(signed.pop("_work_root"))
        block_hash = signed.pop("_hash")
        if guard is None:
            node.process(dict(signed))
        else:
            # Reserved in the mandate ledger BEFORE the block is broadcast; a
            # broadcast that raises stays counted, because it may have landed.
            guard.spend(destination, amount_raw, lambda: node.process(dict(signed)),
                        ref=str(idempotency_key))
    except _mandate.MandateRefused as exc:
        raise _mandate_refusal(exc) from None
    except nanonode.NodeError as exc:
        raise ToolError(exc.reason, exc.message, 503) from None

    result = {
        "block_hash": block_hash,
        "amount_xno": _six(amount_raw),
        "to": destination,
        "confirmed": False,
        "receipt": "https://nanolooker.com/block/%s" % block_hash,
    }
    sent[str(idempotency_key)] = {"to": destination, "amount_raw": amount_raw,
                                  "result": result}
    return dict(result)


# ---------------------------------------------------------------- operator mandate

def _mandate_guard(env, source: str):
    """The operator's signed spend cap for `source`, or None when none is configured.

    NANO_WALLET_MANDATE           path to a signed mandate (see mandate.py)
    NANO_WALLET_MANDATE_LEDGER    its spend ledger (default: <mandate>.ledger.json)
    NANO_WALLET_REQUIRE_MANDATE=1 refuse every send that has no mandate

    A configured mandate that does not verify - bad signature, another agent,
    expired, unreadable - refuses the send. It never falls back to no mandate.
    """
    path = str(env.get("NANO_WALLET_MANDATE", "") or "").strip()
    if not path:
        if str(env.get("NANO_WALLET_REQUIRE_MANDATE", "")).strip() == "1":
            raise ToolError("mandate_required",
                            "NANO_WALLET_REQUIRE_MANDATE=1 and no NANO_WALLET_MANDATE is set: "
                            "this install sends only under an operator-signed mandate", 403)
        return None
    try:
        return _mandate.MandateGuard.from_file(
            path, str(env.get("NANO_WALLET_MANDATE_LEDGER", "") or "").strip() or None, agent=source)
    except _mandate.MandateRefused as exc:
        raise _mandate_refusal(exc) from None


def _mandate_refusal(exc) -> ToolError:
    return ToolError("mandate_refused", "operator mandate refused this send: %s" % exc.message,
                     403, mandate_reason=exc.reason)


# ---------------------------------------------------------------- helpers

def _six(raw: int) -> str:
    """Exact raw -> XNO, rendered at no fewer than 6 decimal places.

    Six is what the spec's worked examples show. Nothing is rounded: a
    balance with more than six significant decimals keeps every one of
    them, because the string is built from the integer, not from a float.
    """
    text = wallet.raw_to_xno(int(raw))
    whole, _, frac = text.partition(".")
    return "%s.%s" % (whole, frac.ljust(6, "0"))


def _representative_pk(explicit: str, current: str, own_public_key: bytes) -> bytes:
    """Who this account votes for. Defaults to itself.

    Self-representation is the choice that involves no third party, which
    is the same reason the rest of this package makes no network call it
    does not need. NANO_WALLET_REPRESENTATIVE overrides it; an account
    that already has a representative keeps it, because changing it is
    not something a receive should ever do silently.
    """
    chosen = explicit or os.environ.get("NANO_WALLET_REPRESENTATIVE") or current
    if not chosen:
        return own_public_key
    verdict = validate_address(chosen)
    if not verdict["valid"]:
        raise ToolError("invalid_representative",
                        "representative %r fails its checksum: %s" % (chosen, verdict["message"]))
    return bytes.fromhex(verdict["public_key"])
