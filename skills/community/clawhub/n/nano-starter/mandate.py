"""Operator mandate: a spend cap the human operator signs once, enforced before every send.

Why this exists. Outside agents told us the #1 reason they cannot pay in Nano
(XNO) is not the currency: the human operator owns the wallet and the
authority to spend ("standing latitude to operate, but not to spend"; "no
funds, no signature"; "I at least want a pizza" - i.e. tell me what the spend
buys). A mandate is the answer an operator can sign once and then stop
worrying about:

    agent            the account allowed to spend           nano_...
    operator         the human's account, whose key signs   nano_...
    total_cap_raw    the most the agent may ever spend       "500000000000000000000000000000"
    per_payment_max_raw   the most in any single payment     "10000000000000000000000000000"
    allowed_payees   optional allow-list of destinations    ["nano_..."] or null (anyone)
    purpose          what the spend buys, in words          "web-search API calls for ..."
    issued_at / expires_at   UTC, "YYYY-MM-DDTHH:MM:SSZ"
    nonce            random hex, so two identical mandates are still two mandates
    version / type   1 / "nano-operator-mandate"

Money is an integer count of raw end to end (1 XNO = 10**30 raw). Amounts are
decimal integer STRINGS in the document (JSON numbers lose precision above
2**53), and a float is refused everywhere a caller can hand one in.

Signing is Nano's own scheme: Ed25519 with every SHA-512 replaced by
BLAKE2b-512, so an operator signs with the same key that holds their XNO and
anyone can check the signature against the operator's public address. The
signed message is a domain tag plus the mandate hash, never a bare 32-byte
value, so a mandate signature can never double as a Nano block signature.

Enforcement fails closed. Before any send, `MandateGuard.spend` checks, in
order: the signature, the agent, the expiry, the amount's type, the
per-payment max, the payee allow-list and the remaining cap (from a small
local ledger file). Any doubt - an unreadable ledger, a ledger for another
mandate, an unknown field, a clock before issue time - is a refusal with a
machine-readable reason. A send whose outcome is unknown (it raised) stays
counted as spent: under-counting is how a cap gets overrun.

What the local ledger cannot do: it stops an honest runtime from
overspending; it cannot stop someone with shell access from deleting the
file. For a hard ceiling, also fund the agent's account with no more than the
cap. Both together are the whole story; neither alone is.

Standard library only. This file is self-contained on purpose so the same
bytes can be vendored into nano-wallet-xno and openai-agents-nano-x402; the
golden vectors in each repo's tests pin that the copies agree.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import secrets
import sys
import tempfile

try:  # POSIX advisory lock for the ledger; Windows falls back to no lock.
    import fcntl as _fcntl
except ImportError:  # pragma: no cover
    _fcntl = None

MANDATE_TYPE = "nano-operator-mandate"
MANDATE_VERSION = 1
RAW_PER_XNO = 10 ** 30
SIGN_DOMAIN = b"nano-operator-mandate/v1:"
HASH_DOMAIN = b"nano-operator-mandate/v1\n"
PURPOSE_MAX_CHARS = 500
MAX_RAW = 2 ** 128 - 1  # a Nano balance is a 128-bit unsigned integer

REQUIRED_FIELDS = (
    "type", "version", "agent", "operator", "total_cap_raw", "per_payment_max_raw",
    "purpose", "issued_at", "expires_at", "nonce",
)
OPTIONAL_FIELDS = ("allowed_payees",)


class MandateRefused(Exception):
    """A refusal with a stable machine-readable `reason` and a human `message`."""

    def __init__(self, reason: str, message: str):
        super().__init__("%s: %s" % (reason, message))
        self.reason = reason
        self.message = message

    def as_dict(self) -> dict:
        return {"ok": False, "reason": self.reason, "message": self.message}


# ------------------------------------------------------------ ed25519-blake2b
# Nano uses RFC 8032 Ed25519 with BLAKE2b-512 in place of SHA-512. The curve
# code takes the hash as a parameter so the RFC's own SHA-512 vectors can pin
# the arithmetic (see tests). Adapted from nano-wallet-xno/ed25519_blake2b.py,
# plus the verification half, which that module did not need.

_Q = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _Q - 2, _Q) % _Q
_I = pow(2, (_Q - 1) // 4, _Q)


def _inv(x):
    return pow(x, _Q - 2, _Q)


def _ext_add(p, q):
    # RFC 8032 section 5.1.4, extended homogeneous coordinates: no inversion per add.
    x1, y1, z1, t1 = p
    x2, y2, z2, t2 = q
    a = (y1 - x1) * (y2 - x2) % _Q
    b = (y1 + x1) * (y2 + x2) % _Q
    c = 2 * t1 * t2 * _D % _Q
    d = 2 * z1 * z2 % _Q
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % _Q, g * h % _Q, f * g % _Q, e * h % _Q)


def _to_ext(p):
    x, y = p
    return (x, y, 1, x * y % _Q)


def _from_ext(p):
    x, y, z, _ = p
    zi = _inv(z)
    return (x * zi % _Q, y * zi % _Q)


def _add(p, q):
    return _from_ext(_ext_add(_to_ext(p), _to_ext(q)))


def _mul(p, e):
    result = (0, 1, 1, 0)
    addend = _to_ext(p)
    while e > 0:
        if e & 1:
            result = _ext_add(result, addend)
        addend = _ext_add(addend, addend)
        e >>= 1
    return _from_ext(result)


def _x_recover(y):
    xx = (y * y - 1) * _inv(_D * y * y + 1)
    x = pow(xx, (_Q + 3) // 8, _Q)
    if (x * x - xx) % _Q != 0:
        x = x * _I % _Q
    if x % 2 != 0:
        x = _Q - x
    return x


_BY = 4 * _inv(5) % _Q
_B = (_x_recover(_BY), _BY)


def _encode_point(p):
    x, y = p
    return ((y & ~(1 << 255)) | ((x & 1) << 255)).to_bytes(32, "little")


def _decode_point(b: bytes):
    """Decode a 32-byte point, or None if it is not a valid curve point."""
    if len(b) != 32:
        return None
    n = int.from_bytes(b, "little")
    y = n & ((1 << 255) - 1)
    sign = n >> 255
    if y >= _Q:
        return None
    xx = (y * y - 1) * _inv(_D * y * y + 1) % _Q
    x = pow(xx, (_Q + 3) // 8, _Q)
    if (x * x - xx) % _Q != 0:
        x = x * _I % _Q
    if (x * x - xx) % _Q != 0:
        return None
    if x == 0 and sign:
        return None
    if (x & 1) != sign:
        x = _Q - x
    return (x, y)


def _clamp(h32: bytes) -> int:
    a = int.from_bytes(h32, "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a


def _blake2b512(data: bytes) -> bytes:
    return hashlib.blake2b(data, digest_size=64).digest()


def _sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()


def public_key_from_private(private_key: bytes, hashfn=_blake2b512) -> bytes:
    if len(private_key) != 32:
        raise ValueError("private key must be 32 bytes")
    return _encode_point(_mul(_B, _clamp(hashfn(private_key)[:32])))


def sign(message: bytes, private_key: bytes, hashfn=_blake2b512) -> bytes:
    """64-byte Ed25519(-blake2b) signature over `message`."""
    public_key = public_key_from_private(private_key, hashfn)
    h = hashfn(private_key)
    a = _clamp(h[:32])
    r = int.from_bytes(hashfn(h[32:64] + message), "little") % _L
    r_enc = _encode_point(_mul(_B, r))
    k = int.from_bytes(hashfn(r_enc + public_key + message), "little") % _L
    return r_enc + ((r + k * a) % _L).to_bytes(32, "little")


def verify(signature: bytes, message: bytes, public_key: bytes, hashfn=_blake2b512) -> bool:
    """True only for a valid signature. Never raises on malformed input."""
    try:
        if len(signature) != 64 or len(public_key) != 32:
            return False
        r_point = _decode_point(signature[:32])
        a_point = _decode_point(public_key)
        s = int.from_bytes(signature[32:], "little")
        if r_point is None or a_point is None or s >= _L:
            return False
        k = int.from_bytes(hashfn(signature[:32] + public_key + message), "little") % _L
        left = _mul(_B, s)
        right = _add(r_point, _mul(a_point, k))
        return left == right
    except Exception:
        return False


def private_key_from_seed(seed: bytes, index: int = 0) -> bytes:
    """Nano account derivation: blake2b-256(seed || index as 4 big-endian bytes)."""
    if len(seed) != 32:
        raise ValueError("seed must be 32 bytes")
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index <= 0xFFFFFFFF:
        raise ValueError("index must be an integer in [0, 2**32)")
    return hashlib.blake2b(seed + index.to_bytes(4, "big"), digest_size=32).digest()


# ------------------------------------------------------------ addresses

_ALPHABET = "13456789abcdefghijkmnopqrstuwxyz"
_DECODE = {c: i for i, c in enumerate(_ALPHABET)}


def _b32(value: int, length: int) -> str:
    return "".join(_ALPHABET[(value >> s) & 0x1F] for s in range((length - 1) * 5, -1, -5))


def _checksum(public_key: bytes) -> str:
    digest = hashlib.blake2b(public_key, digest_size=5).digest()
    return _b32(int.from_bytes(digest[::-1], "big"), 8)


def address_from_public_key(public_key: bytes) -> str:
    if len(public_key) != 32:
        raise ValueError("public key must be 32 bytes")
    return "nano_" + _b32(int.from_bytes(public_key, "big"), 52) + _checksum(public_key)


def public_key_from_address(address) -> bytes:
    """Decode and checksum-verify a nano_/xrb_ address, or raise MandateRefused."""
    if not isinstance(address, str):
        raise MandateRefused("invalid_address", "address must be a string")
    text = address.strip()
    for prefix in ("nano_", "xrb_"):
        if text.startswith(prefix):
            rest = text[len(prefix):]
            break
    else:
        raise MandateRefused("invalid_address", "%r does not start with nano_ or xrb_" % address)
    if len(rest) != 60 or rest[0] not in "13" or any(c not in _DECODE for c in rest):
        raise MandateRefused("invalid_address", "%r is not a well-formed Nano address" % address)
    value = 0
    for c in rest[:52]:
        value = (value << 5) | _DECODE[c]
    public_key = value.to_bytes(33, "big")[1:]
    if _checksum(public_key) != rest[52:]:
        raise MandateRefused("invalid_address", "%r fails its checksum" % address)
    return public_key


def normalise_address(address) -> str:
    return address_from_public_key(public_key_from_address(address))


# ------------------------------------------------------------ amounts


def parse_raw(value, field: str = "amount") -> int:
    """An exact raw amount from an int or a decimal-integer string. Floats refused."""
    if isinstance(value, bool) or isinstance(value, float):
        raise MandateRefused("invalid_amount", "%s must be an integer count of raw, never a %s"
                             % (field, type(value).__name__))
    if isinstance(value, int):
        n = value
    elif isinstance(value, str):
        text = value.strip()
        if not text.isdigit() or not text.isascii() or (len(text) > 1 and text[0] == "0"):
            raise MandateRefused("invalid_amount", "%s must be a decimal integer string of raw, got %r"
                                 % (field, value))
        n = int(text)
    else:
        raise MandateRefused("invalid_amount", "%s must be an integer count of raw" % field)
    if n <= 0 or n > MAX_RAW:
        raise MandateRefused("invalid_amount", "%s must be between 1 and 2**128-1 raw, got %d" % (field, n))
    return n


def xno_to_raw(text) -> int:
    """Exact decimal XNO string -> raw integer. No float is ever involved."""
    if not isinstance(text, str):
        raise MandateRefused("invalid_amount", "XNO amounts must be given as a decimal string")
    t = text.strip()
    whole, dot, frac = t.partition(".")
    if not whole:
        whole = "0"
    if not (whole.isdigit() and whole.isascii()) or (dot and not (frac.isdigit() and frac.isascii())) \
            or len(frac) > 30:
        raise MandateRefused("invalid_amount", "%r is not a decimal XNO amount (max 30 decimals)" % text)
    return int(whole) * RAW_PER_XNO + int(frac.ljust(30, "0") or "0")


def raw_to_xno(raw: int) -> str:
    whole, frac = divmod(int(raw), RAW_PER_XNO)
    frac_s = str(frac).rjust(30, "0").rstrip("0")
    return "%d.%s" % (whole, frac_s) if frac_s else "%d" % whole


# ------------------------------------------------------------ time


def _parse_time(value, field: str) -> _dt.datetime:
    if not isinstance(value, str):
        raise MandateRefused("invalid_mandate", "%s must be a UTC time string YYYY-MM-DDTHH:MM:SSZ" % field)
    try:
        return _dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except ValueError:
        raise MandateRefused("invalid_mandate", "%s must be YYYY-MM-DDTHH:MM:SSZ (UTC), got %r"
                             % (field, value)) from None


def format_time(moment: _dt.datetime) -> str:
    return moment.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _now(now=None) -> _dt.datetime:
    if now is None:
        return _dt.datetime.now(_dt.timezone.utc)
    if isinstance(now, (int,)) and not isinstance(now, bool):
        return _dt.datetime.fromtimestamp(now, _dt.timezone.utc)
    if isinstance(now, _dt.datetime):
        return now if now.tzinfo else now.replace(tzinfo=_dt.timezone.utc)
    return _parse_time(now, "now")


# ------------------------------------------------------------ the document


def canonical_bytes(mandate: dict) -> bytes:
    """The one serialisation that is hashed and signed: sorted keys, no spaces, ASCII."""
    return json.dumps(mandate, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def mandate_hash(mandate: dict) -> str:
    """64 upper-case hex: blake2b-256 over a domain tag and the canonical bytes."""
    return hashlib.blake2b(HASH_DOMAIN + canonical_bytes(mandate), digest_size=32).hexdigest().upper()


def signing_message(mandate: dict) -> bytes:
    return SIGN_DOMAIN + bytes.fromhex(mandate_hash(mandate))


def validate_fields(mandate) -> dict:
    """Check the mandate's shape. Returns a normalised view; raises MandateRefused."""
    if not isinstance(mandate, dict):
        raise MandateRefused("invalid_mandate", "the mandate must be a JSON object")
    unknown = sorted(set(mandate) - set(REQUIRED_FIELDS) - set(OPTIONAL_FIELDS))
    if unknown:
        raise MandateRefused("invalid_mandate", "unknown field(s) %s - refusing rather than ignoring"
                             % ", ".join(unknown))
    missing = [f for f in REQUIRED_FIELDS if f not in mandate]
    if missing:
        raise MandateRefused("invalid_mandate", "missing field(s) %s" % ", ".join(missing))
    if mandate["type"] != MANDATE_TYPE:
        raise MandateRefused("invalid_mandate", "type must be %r" % MANDATE_TYPE)
    if mandate["version"] != MANDATE_VERSION or isinstance(mandate["version"], bool):
        raise MandateRefused("unsupported_version", "only version %d is understood" % MANDATE_VERSION)
    agent_pk = public_key_from_address(mandate["agent"])
    operator_pk = public_key_from_address(mandate["operator"])
    if agent_pk == operator_pk:
        raise MandateRefused("invalid_mandate", "the operator and the agent must be different accounts")
    for f in ("total_cap_raw", "per_payment_max_raw"):
        if not isinstance(mandate[f], str):
            raise MandateRefused("invalid_amount", "%s must be a decimal integer STRING of raw" % f)
    total = parse_raw(mandate["total_cap_raw"], "total_cap_raw")
    per = parse_raw(mandate["per_payment_max_raw"], "per_payment_max_raw")
    if per > total:
        raise MandateRefused("invalid_mandate", "per_payment_max_raw exceeds total_cap_raw")
    purpose = mandate["purpose"]
    if not isinstance(purpose, str) or not purpose.strip():
        raise MandateRefused("missing_purpose", "purpose must say, in words, what the spend buys")
    if len(purpose) > PURPOSE_MAX_CHARS:
        raise MandateRefused("invalid_mandate", "purpose is longer than %d characters" % PURPOSE_MAX_CHARS)
    issued = _parse_time(mandate["issued_at"], "issued_at")
    expires = _parse_time(mandate["expires_at"], "expires_at")
    if expires <= issued:
        raise MandateRefused("invalid_mandate", "expires_at must be after issued_at")
    nonce = mandate["nonce"]
    if not isinstance(nonce, str) or not 8 <= len(nonce) <= 64 or any(c not in "0123456789abcdef" for c in nonce):
        raise MandateRefused("invalid_mandate", "nonce must be 8-64 lower-case hex characters")
    payees = mandate.get("allowed_payees")
    payee_keys = None
    if payees is not None:
        if not isinstance(payees, list) or not payees:
            raise MandateRefused("invalid_mandate", "allowed_payees must be a non-empty list or null")
        payee_keys = frozenset(public_key_from_address(p) for p in payees)
    return {
        "agent_pk": agent_pk, "operator_pk": operator_pk, "total_cap_raw": total,
        "per_payment_max_raw": per, "issued_at": issued, "expires_at": expires,
        "payee_keys": payee_keys,
    }


def build_mandate(agent: str, operator: str, total_cap_raw, per_payment_max_raw, purpose: str,
                  expires_at: str, allowed_payees=None, issued_at: str = None, nonce: str = None) -> dict:
    """Assemble an UNSIGNED mandate and validate it. Amounts: raw ints or integer strings."""
    mandate = {
        "type": MANDATE_TYPE,
        "version": MANDATE_VERSION,
        "agent": normalise_address(agent),
        "operator": normalise_address(operator),
        "total_cap_raw": str(parse_raw(total_cap_raw, "total_cap_raw")),
        "per_payment_max_raw": str(parse_raw(per_payment_max_raw, "per_payment_max_raw")),
        "purpose": purpose,
        "issued_at": issued_at or format_time(_now()),
        "expires_at": expires_at,
        "nonce": nonce or secrets.token_hex(16),
    }
    if allowed_payees:
        mandate["allowed_payees"] = [normalise_address(p) for p in allowed_payees]
    validate_fields(mandate)
    return mandate


def sign_mandate(mandate: dict, operator_private_key: bytes) -> dict:
    """Sign as the operator. Refuses a key that is not the mandate's operator."""
    view = validate_fields(mandate)
    if public_key_from_private(operator_private_key) != view["operator_pk"]:
        raise MandateRefused("wrong_key", "this key is not the key of the mandate's operator %s"
                             % mandate["operator"])
    return {
        "mandate": mandate,
        "hash": mandate_hash(mandate),
        "signature": sign(signing_message(mandate), operator_private_key).hex().upper(),
    }


def verify_signed(signed, now=None, agent: str = None) -> dict:
    """Verify a signed mandate document. Returns the normalised view; raises MandateRefused.

    Checks shape, hash, operator signature, the agent (if given), issue time and expiry.
    """
    if not isinstance(signed, dict) or set(signed) != {"mandate", "hash", "signature"}:
        raise MandateRefused("invalid_mandate", "a signed mandate is exactly {mandate, hash, signature}")
    mandate = signed["mandate"]
    view = validate_fields(mandate)
    computed = mandate_hash(mandate)
    if not isinstance(signed["hash"], str) or signed["hash"].upper() != computed:
        raise MandateRefused("hash_mismatch", "the mandate's content does not match its hash "
                             "(it was changed after signing)")
    try:
        signature = bytes.fromhex(signed["signature"])
    except (TypeError, ValueError):
        raise MandateRefused("bad_signature", "signature is not hex") from None
    if not verify(signature, signing_message(mandate), view["operator_pk"]):
        raise MandateRefused("bad_signature", "the signature is not the operator's over this mandate")
    if agent is not None and public_key_from_address(agent) != view["agent_pk"]:
        raise MandateRefused("wrong_agent", "this mandate authorises %s, not %s" % (mandate["agent"], agent))
    moment = _now(now)
    if moment < view["issued_at"]:
        raise MandateRefused("not_yet_valid", "the mandate is not valid before %s" % mandate["issued_at"])
    if moment >= view["expires_at"]:
        raise MandateRefused("expired", "the mandate expired at %s" % mandate["expires_at"])
    view["hash"] = computed
    view["mandate"] = mandate
    return view


def load_signed(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh, parse_float=_refuse_float, parse_constant=_refuse_float)
    except MandateRefused:
        raise
    except (OSError, ValueError) as exc:
        raise MandateRefused("unreadable_mandate", "cannot read mandate %s: %s" % (path, exc)) from None


def _refuse_float(text):
    raise MandateRefused("invalid_amount", "a non-integer number (%s) appears in the file" % text)


# ------------------------------------------------------------ ledger + guard


class _Locked:
    def __init__(self, path):
        self.path = path + ".lock"
        self.fh = None

    def __enter__(self):
        self.fh = open(self.path, "a+")
        if _fcntl is not None:
            _fcntl.flock(self.fh, _fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if _fcntl is not None:
            _fcntl.flock(self.fh, _fcntl.LOCK_UN)
        self.fh.close()


def default_ledger_path(mandate_path: str) -> str:
    return mandate_path + ".ledger.json"


class MandateGuard:
    """Checks every payment against a signed mandate and records it in a local ledger.

        guard = MandateGuard.from_file("mandate.json")          # ledger: mandate.json.ledger.json
        guard.spend(payee, amount_raw, lambda: my_send(payee, amount_raw))

    `spend` refuses with MandateRefused before calling `send` if anything is off.
    """

    def __init__(self, signed: dict, ledger_path: str, agent: str = None, clock=None):
        self.signed = signed
        self.ledger_path = ledger_path
        self.agent = agent
        self.clock = clock  # callable returning a datetime / epoch int; None = real time
        verify_signed(signed, now=self._time(), agent=agent)  # refuse a bad mandate at construction

    @classmethod
    def from_file(cls, mandate_path: str, ledger_path: str = None, agent: str = None, clock=None):
        return cls(load_signed(mandate_path), ledger_path or default_ledger_path(mandate_path),
                   agent=agent, clock=clock)

    def _time(self):
        return self.clock() if self.clock else None

    # -- ledger file -------------------------------------------------------
    def _read(self, mandate_hash_hex: str) -> dict:
        if not os.path.exists(self.ledger_path):
            return {"mandate_hash": mandate_hash_hex, "spent_raw": "0", "payments": []}
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if data.get("mandate_hash") != mandate_hash_hex:
                raise MandateRefused("ledger_mismatch", "ledger %s belongs to another mandate (%s)"
                                     % (self.ledger_path, data.get("mandate_hash")))
            spent = int(data["spent_raw"]) if str(data["spent_raw"]).isdigit() else None
            if spent is None or sum(int(p["amount_raw"]) for p in data["payments"]) != spent:
                raise MandateRefused("ledger_corrupt", "ledger totals do not add up")
            return data
        except MandateRefused:
            raise
        except Exception as exc:
            raise MandateRefused("ledger_unreadable", "cannot read ledger %s (%s); refusing to spend"
                                 % (self.ledger_path, exc)) from None

    def _write(self, data: dict) -> None:
        directory = os.path.dirname(os.path.abspath(self.ledger_path))
        fd, tmp = tempfile.mkstemp(prefix=".mandate-ledger-", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, sort_keys=True)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, self.ledger_path)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    # -- the checks ----------------------------------------------------------
    def _check(self, view: dict, data: dict, payee: str, amount) -> int:
        amount_raw = parse_raw(amount, "amount")
        payee_pk = public_key_from_address(payee)
        if amount_raw > view["per_payment_max_raw"]:
            raise MandateRefused("over_per_payment_max", "%s raw is above the per-payment max of %s raw"
                                 % (amount_raw, view["per_payment_max_raw"]))
        if view["payee_keys"] is not None and payee_pk not in view["payee_keys"]:
            raise MandateRefused("payee_not_allowed", "%s is not on the operator's allow-list"
                                 % normalise_address(payee))
        remaining = view["total_cap_raw"] - int(data["spent_raw"])
        if amount_raw > remaining:
            raise MandateRefused("cap_exhausted", "%s raw requested, %s raw left of the %s raw cap"
                                 % (amount_raw, max(remaining, 0), view["total_cap_raw"]))
        return amount_raw

    def check(self, payee: str, amount) -> dict:
        """Dry run: would this payment be allowed right now? Records nothing."""
        view = verify_signed(self.signed, now=self._time(), agent=self.agent)
        with _Locked(self.ledger_path):
            data = self._read(view["hash"])
            amount_raw = self._check(view, data, payee, amount)
        return {"ok": True, "amount_raw": str(amount_raw),
                "remaining_after_raw": str(view["total_cap_raw"] - int(data["spent_raw"]) - amount_raw)}

    def spend(self, payee: str, amount, send, ref: str = None):
        """Check, reserve in the ledger, then call `send()` and return its result.

        If `send` raises, the reservation stays (status "unknown"): the money
        may have moved, and a cap that forgets an unknown payment can be overrun.
        """
        view = verify_signed(self.signed, now=self._time(), agent=self.agent)
        with _Locked(self.ledger_path):
            data = self._read(view["hash"])
            amount_raw = self._check(view, data, payee, amount)
            entry = {"payee": normalise_address(payee), "amount_raw": str(amount_raw),
                     "at": format_time(_now(self._time())), "status": "pending", "ref": ref or ""}
            data["payments"].append(entry)
            data["spent_raw"] = str(int(data["spent_raw"]) + amount_raw)
            self._write(data)
            index = len(data["payments"]) - 1
            try:
                result = send()
            except BaseException:
                data["payments"][index]["status"] = "unknown"
                self._write(data)
                raise
            data["payments"][index]["status"] = "returned"
            self._write(data)
        return result

    def status(self) -> dict:
        """Remaining cap and validity, for `mandate status`. Never raises on an expired mandate."""
        mandate = self.signed["mandate"]
        view = validate_fields(mandate)
        valid, reason = True, None
        try:
            verify_signed(self.signed, now=self._time(), agent=self.agent)
        except MandateRefused as exc:
            valid, reason = False, exc.reason
        with _Locked(self.ledger_path):
            data = self._read(mandate_hash(mandate))
        spent = int(data["spent_raw"])
        remaining = max(view["total_cap_raw"] - spent, 0)
        return {
            "valid": valid, "refusal": reason, "hash": mandate_hash(mandate),
            "agent": mandate["agent"], "operator": mandate["operator"], "purpose": mandate["purpose"],
            "expires_at": mandate["expires_at"],
            "total_cap_raw": str(view["total_cap_raw"]), "spent_raw": str(spent),
            "remaining_raw": str(remaining), "remaining_xno": raw_to_xno(remaining),
            "per_payment_max_raw": str(view["per_payment_max_raw"]),
            "allowed_payees": mandate.get("allowed_payees"), "payments": len(data["payments"]),
            "ledger": self.ledger_path,
        }


# ------------------------------------------------------------ key files


def load_private_key(path: str) -> bytes:
    """A key file is JSON: {"seed": hex64, "index": n} or {"private_key": hex64}."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if "private_key" in data:
            key = bytes.fromhex(data["private_key"])
        else:
            key = private_key_from_seed(bytes.fromhex(data["seed"]), int(data.get("index", 0)))
        if len(key) != 32:
            raise ValueError("key must be 32 bytes")
        return key
    except Exception as exc:
        raise MandateRefused("unreadable_key", "cannot read key file %s: %s" % (path, exc)) from None


def _write_private(path: str, data: dict) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


# ------------------------------------------------------------ CLI


def _amount_arg(raw, xno, name):
    if (raw is None) == (xno is None):
        raise MandateRefused("invalid_amount", "give exactly one of --%s-raw or --%s-xno" % (name, name))
    return parse_raw(raw, name) if raw is not None else parse_raw(xno_to_raw(xno), name)


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="mandate", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    kg = sub.add_parser("keygen", help="write a new operator key file (mode 600) and print its address")
    kg.add_argument("--out", required=True)

    cr = sub.add_parser("create", help="build a mandate; sign it if --operator-key is given")
    cr.add_argument("--agent", required=True, help="the agent's nano_ address")
    who = cr.add_mutually_exclusive_group(required=True)
    who.add_argument("--operator-key", help="operator key file: signs the mandate")
    who.add_argument("--operator", help="operator address: prints the UNSIGNED mandate + hash to sign")
    cr.add_argument("--total-cap-raw")
    cr.add_argument("--total-cap-xno")
    cr.add_argument("--per-payment-max-raw")
    cr.add_argument("--per-payment-max-xno")
    cr.add_argument("--purpose", required=True, help="what the spend buys, in words")
    exp = cr.add_mutually_exclusive_group(required=True)
    exp.add_argument("--expires", help="UTC YYYY-MM-DDTHH:MM:SSZ")
    exp.add_argument("--days", type=int, help="expire this many days from now")
    cr.add_argument("--payee", action="append", help="allowed payee (repeatable); omit for any payee")
    cr.add_argument("--out", help="write here instead of stdout")

    sg = sub.add_parser("sign", help="sign an unsigned mandate file with the operator key")
    sg.add_argument("file")
    sg.add_argument("--operator-key", required=True)
    sg.add_argument("--out")

    vf = sub.add_parser("verify", help="verify signature, hash and expiry; exit 0 only if valid")
    vf.add_argument("file")
    vf.add_argument("--agent", help="also require this agent address")

    st = sub.add_parser("status", help="remaining cap and validity")
    st.add_argument("file")
    st.add_argument("--ledger", help="default: <file>.ledger.json")

    ck = sub.add_parser("check", help="dry run: would this payment be allowed? records nothing")
    ck.add_argument("file")
    ck.add_argument("--payee", required=True)
    ck.add_argument("--amount-raw", required=True)
    ck.add_argument("--ledger")

    args = parser.parse_args(argv)
    try:
        if args.command == "keygen":
            seed = secrets.token_bytes(32)
            address = address_from_public_key(public_key_from_private(private_key_from_seed(seed, 0)))
            _write_private(args.out, {"seed": seed.hex().upper(), "index": 0, "address": address})
            _print({"ok": True, "key_file": args.out, "address": address})
            return 0
        if args.command == "create":
            key = load_private_key(args.operator_key) if args.operator_key else None
            operator = address_from_public_key(public_key_from_private(key)) if key else args.operator
            if args.days is not None:
                if args.days <= 0:
                    raise MandateRefused("invalid_mandate", "--days must be positive")
                expires = format_time(_now() + _dt.timedelta(days=args.days))
            else:
                expires = args.expires
            mandate = build_mandate(
                agent=args.agent, operator=operator,
                total_cap_raw=_amount_arg(args.total_cap_raw, args.total_cap_xno, "total-cap"),
                per_payment_max_raw=_amount_arg(args.per_payment_max_raw, args.per_payment_max_xno,
                                                "per-payment-max"),
                purpose=args.purpose, expires_at=expires, allowed_payees=args.payee)
            doc = sign_mandate(mandate, key) if key else {
                "mandate": mandate, "hash": mandate_hash(mandate),
                "sign_this_hex": signing_message(mandate).hex().upper(),
                "note": "sign with `mandate sign FILE --operator-key KEY`, or sign sign_this_hex "
                        "with the operator's Nano key (ed25519-blake2b) and add it as `signature`, "
                        "dropping sign_this_hex and note",
            }
            text = json.dumps(doc, indent=2, sort_keys=True) + "\n"
            if args.out:
                with open(args.out, "x", encoding="utf-8") as fh:
                    fh.write(text)
                _print({"ok": True, "written": args.out, "hash": doc["hash"], "signed": bool(key)})
            else:
                sys.stdout.write(text)
            return 0
        if args.command == "sign":
            with open(args.file, "r", encoding="utf-8") as fh:
                doc = json.load(fh, parse_float=_refuse_float)
            signed = sign_mandate(doc["mandate"], load_private_key(args.operator_key))
            text = json.dumps(signed, indent=2, sort_keys=True) + "\n"
            if args.out:
                with open(args.out, "x", encoding="utf-8") as fh:
                    fh.write(text)
                _print({"ok": True, "written": args.out, "hash": signed["hash"]})
            else:
                sys.stdout.write(text)
            return 0
        if args.command == "verify":
            view = verify_signed(load_signed(args.file), agent=args.agent)
            m = view["mandate"]
            _print({"ok": True, "hash": view["hash"], "agent": m["agent"], "operator": m["operator"],
                    "purpose": m["purpose"], "total_cap_raw": m["total_cap_raw"],
                    "per_payment_max_raw": m["per_payment_max_raw"], "expires_at": m["expires_at"],
                    "allowed_payees": m.get("allowed_payees")})
            return 0
        if args.command == "status":
            guard = MandateGuard.__new__(MandateGuard)
            guard.signed, guard.agent, guard.clock = load_signed(args.file), None, None
            guard.ledger_path = args.ledger or default_ledger_path(args.file)
            report = guard.status()
            _print(report)
            return 0 if report["valid"] else 1
        if args.command == "check":
            guard = MandateGuard.from_file(args.file, args.ledger)
            _print(guard.check(args.payee, args.amount_raw))
            return 0
    except MandateRefused as exc:
        _print(exc.as_dict())
        return 1
    except FileExistsError as exc:
        _print({"ok": False, "reason": "file_exists", "message": "refusing to overwrite %s" % exc.filename})
        return 1
    return 2  # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
