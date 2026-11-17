"""Transactions: build + locally sign + submit, with spending safeguards.

Safety model (config-driven, defaults conservative):
  automatic_send_limit_uj — sends at/below this may go out without an
    interactive confirmation (the CLI still prints what it did)
  daily_limit_uj          — total sent per UTC day (tracked in a small
    state file; the node enforces consensus, this enforces policy)
  require_confirmation    — when True, `send` with `--yes` absent and
    amount above the automatic limit prints a summary and exits with
    code 3 instead of submitting (the agent must ask the user and re-run
    with --yes)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import nacl.signing

from jerith_client import Client, NodeError
from jerith_config import uj_to_jer
from jerith_wallet import load_wallet, secret_key


def _state_file() -> Path:
    """Daily-send state file. Overridable via JERITH_SKILL_STATE_DIR so
    tests (and multi-instance setups) never share state with the host."""
    base = os.environ.get("JERITH_SKILL_STATE_DIR", "")
    d = Path(base).expanduser() if base else Path.home() / ".config" / "jerith"
    return d / "send-state.json"


class SpendError(Exception):
    pass


def _daily_sent_uj() -> int:
    sf = _state_file()
    try:
        st = json.loads(sf.read_text())
        if st.get("date") == time.strftime("%Y-%m-%d", time.gmtime()):
            return int(st.get("sent_uj", 0))
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    return 0


def _record_sent(amount_uj: int) -> None:
    sf = _state_file()
    today = time.strftime("%Y-%m-%d", time.gmtime())
    sent = _daily_sent_uj() if sf.exists() else 0
    try:
        st = json.loads(sf.read_text())
        if st.get("date") == today:
            sent = int(st.get("sent_uj", 0))
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    sf.parent.mkdir(parents=True, exist_ok=True)
    fd = sf.open("w")
    json.dump({"date": today, "sent_uj": sent + amount_uj}, fd)
    fd.close()


def validate_address(address: str) -> str:
    a = (address or "").strip()
    if not (a.startswith("JER") and len(a) == 35
            and all(c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in a[3:])):
        raise SpendError(
            f"invalid JER address: {a[:12]}… — must be 'JER' + 32 chars "
            f"(alphanumeric, 35 total)")
    return a


def enforce_limits(cfg: dict, amount_uj: int, confirmed: bool) -> None:
    sp = cfg["spending"]
    auto = round(sp["automatic_send_limit_jer"] * 1_000_000)
    daily = round(sp["daily_limit_jer"] * 1_000_000)
    sent = _daily_sent_uj()
    if sent + amount_uj > daily:
        raise SpendError(
            f"daily send limit exceeded: already sent {uj_to_jer(sent):g} JER "
            f"today, limit {uj_to_jer(daily):g} JER "
            f"(this send: {uj_to_jer(amount_uj):g} JER)")
    if sp["require_confirmation"] and not confirmed and amount_uj > auto:
        raise _ConfirmNeeded(amount_uj)


class _ConfirmNeeded(SpendError):
    """Internal signal: needs explicit user confirmation (--yes)."""
    def __init__(self, amount_uj: int):
        super().__init__(f"confirmation required for {uj_to_jer(amount_uj):g} JER")
        self.amount_uj = amount_uj


FEE_UJ = 100_000  # 0.1 JER — the node's documented flat spend fee


def _canonical_payload(sender: str, to: str, amount_uj: int, fee: int,
                       nonce: int, timestamp: int, memo: str,
                       vk_hex: str) -> bytes:
    """Byte-exact reconstruction of the tx payload the node SHOULD be asking
    us to sign (see jerith_core.Tx.payload — canonical JSON, sorted keys)."""
    body = {
        "kind": "spend", "sender": sender, "recipient": to,
        "amount": int(amount_uj), "fee": int(fee), "nonce": int(nonce),
        "timestamp": int(timestamp), "memo": memo, "vk": vk_hex,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode()


def build_and_sign(cfg: dict, to: str, amount_uj: int, memo: str = "") -> dict:
    """Build via node /x/tx/buildraw (nonce/fee from ledger), verify the
    returned payload EXACTLY matches the transfer the user approved, sign
    LOCALLY, return signed tx dict + txid.

    The node fully controls payload_hex — so it is never trusted: we
    rebuild the expected payload ourselves (canonical JSON, same rule as
    the chain's validator) and refuse to sign on ANY divergence. Only the
    ledger-owned nonce and the node clock's timestamp are taken from the
    response; recipient, amount, fee, sender, memo, and vk must equal what
    this function was called with. A hostile or impersonated node cannot
    obtain a signature over a different transfer.
    The secret key never leaves this function's process."""
    client = Client(cfg)
    wallet = load_wallet(cfg)
    sk = nacl.signing.SigningKey(secret_key(cfg))
    vk_hex = bytes(sk.verify_key).hex()
    build = client.tx_buildraw(wallet["address"], to, amount_uj, memo,
                               vk_hex=vk_hex)
    unsigned = dict(build["unsigned_tx"])
    payload = bytes.fromhex(build["payload_hex"])

    # ---- bind the signature to the approved transfer (never trust node) ----
    if unsigned.get("signature") not in ("", None):
        raise SpendError("node returned a pre-filled signature — refusing")
    try:
        nonce = int(unsigned["nonce"])
        ts = int(unsigned["timestamp"])
    except (KeyError, TypeError, ValueError):
        raise SpendError("build response missing valid nonce/timestamp")
    fee = unsigned.get("fee")
    if fee != FEE_UJ:
        raise SpendError(
            f"node returned unexpected fee {fee} (expected {FEE_UJ}) — "
            f"refusing to sign")
    expected = _canonical_payload(
        wallet["address"], to, amount_uj, FEE_UJ, nonce, ts,
        (memo or "")[:120], vk_hex)
    if payload != expected:
        raise SpendError(
            "node payload does not match the approved transfer "
            "(recipient/amount/memo/sender altered?) — refusing to sign. "
            "No funds were spent; check your rpc_url configuration.")

    unsigned["signature"] = sk.sign(payload).signature.hex()
    # verify the signature we just made actually matches the payload
    if not sk.verify_key.verify(payload, bytes.fromhex(unsigned["signature"])):
        raise SpendError("internal error: self-verification failed (aborting)")
    txid = hashlib.sha256(payload + bytes.fromhex(unsigned["signature"])).hexdigest()
    return {"signed_tx": unsigned, "txid": txid}


def send(cfg: dict, to: str, amount_jer: float, memo: str = "",
         confirmed: bool = False) -> dict:
    """Full send flow with all safeguards. Returns structured result dict
    suitable for LLM consumption. Raises SpendError/NodeError on failure."""
    from jerith_config import jer_to_uj
    to = validate_address(to)
    amount_uj = jer_to_uj(amount_jer)          # exact integer conversion
    enforce_limits(cfg, amount_uj, confirmed)

    client = Client(cfg)
    wallet = load_wallet(cfg)
    bal = client.balance(wallet["address"])
    fee_uj = FEE_UJ                             # 0.1 JER — node also enforces
    total = amount_uj + fee_uj
    if int(bal.get("balance_uj", 0)) < total:
        raise SpendError(
            f"insufficient balance: have {uj_to_jer(bal.get('balance_uj', 0)):g} JER, "
            f"need {uj_to_jer(total):g} JER (amount {uj_to_jer(amount_uj):g} + "
            f"fee {uj_to_jer(fee_uj):g}). No funds were spent.")

    signed = build_and_sign(cfg, to, amount_uj, memo)
    res = client.tx_sendraw(signed["signed_tx"])
    _record_sent(amount_uj)
    return {
        "success": True,
        "txid": res.get("txid") or signed["txid"],
        "amount_uj": amount_uj, "amount_jer": uj_to_jer(amount_uj),
        "fee_uj": fee_uj, "fee_jer": uj_to_jer(fee_uj),
        "total_uj": total, "total_jer": uj_to_jer(total),
        "to": to, "block_height": res.get("block_height"),
        "block_hash": res.get("block_hash"),
        "confirmations": res.get("confirmations"),
        "standard_confirmations": res.get("standard_confirmations"),
    }
