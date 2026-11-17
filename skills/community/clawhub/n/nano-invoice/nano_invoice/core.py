"""Invoices that bind a Nano payment to the order it pays for.

Nano blocks carry no memo, so the binding is a UNIQUE TAGGED AMOUNT:

    pay_raw = amount_raw + tag

amount_raw must be a multiple of TAG_MODULUS (10**6 raw), so the lowest six raw
digits of pay_raw are exactly the tag. A tag is unique among the merchant's open
invoices and is not reused for TAG_QUARANTINE_S after its invoice closes, so a
late payment for an old invoice cannot settle a new one. A tag is below 10**6
raw, i.e. under 1e-24 XNO: economically nothing.

Non-custodial: this module reads the public ledger, never holds a key and never
sends. Refunds come out as instructions for the merchant's own wallet.
"""
import contextlib
import dataclasses
import hashlib
import secrets
import sqlite3
import time

from . import account as acct
from .rpc import as_rpc

RAW_PER_XNO = 10 ** 30
TAG_MODULUS = 10 ** 6
TAG_QUARANTINE_S = 7 * 86400
CLOCK_SKEW_S = 120
MAX_RAW = 2 ** 128 - 1
ID_PREFIX = "nano-invoice/v1"
RECEIPT_SCHEMA = "nano-invoice/receipt/v1"

STATES = ("open", "paid", "underpaid", "overpaid", "expired")
TRANSITIONS = {"open": frozenset({"paid", "underpaid", "overpaid", "expired"})}
SETTLING_KINDS = ("payment", "underpaid", "overpaid")
KIND_TO_STATE = {"payment": "paid", "underpaid": "underpaid", "overpaid": "overpaid"}


class InvoiceError(Exception):
    pass


class AmountError(InvoiceError, TypeError):
    pass


class OrderConflict(InvoiceError):
    pass


class IllegalTransition(InvoiceError):
    pass


class BlockAlreadyBound(InvoiceError):
    pass


class TagsExhausted(InvoiceError):
    pass


class NotFound(InvoiceError, KeyError):
    pass


def require_raw(value, name="amount_raw", minimum=1):
    """Amounts are ints in raw (1 XNO = 10**30 raw). Floats and bools are refused."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise AmountError(
            f"{name} must be an int in raw (1 XNO = 10**30 raw), got {type(value).__name__}"
            + ("; a float cannot represent raw amounts exactly" if isinstance(value, float) else ""))
    if value < minimum:
        raise AmountError(f"{name} must be >= {minimum}, got {value}")
    if value > MAX_RAW:
        raise AmountError(f"{name} exceeds the 128-bit Nano supply limit")
    return value


def xno_to_raw(text):
    """Exact decimal XNO string -> raw int ('0.5' -> 5 * 10**29). Never via float."""
    from decimal import Decimal, InvalidOperation, localcontext
    if not isinstance(text, str):
        raise AmountError("pass XNO as a decimal string, e.g. '0.5'")
    try:
        with localcontext() as ctx:  # the default 28 digits would silently round raw away
            ctx.prec = 100
            d = Decimal(text.strip()) * RAW_PER_XNO
        if not d.is_finite():
            raise InvalidOperation
    except InvalidOperation as e:
        raise AmountError(f"not a decimal number: {text!r}") from e
    if d != d.to_integral_value():
        raise AmountError(f"{text} XNO is finer than 1 raw")
    return int(d)


def order_key_hash(order_key):
    if not isinstance(order_key, str) or not order_key:
        raise InvoiceError("order_key must be a non-empty string")
    return hashlib.sha256(order_key.encode("utf-8")).hexdigest()


def invoice_id_for(merchant, order_key_sha256):
    """Re-derivable by anyone who knows the merchant and the order key."""
    return "inv_" + hashlib.sha256(f"{ID_PREFIX}|{merchant}|{order_key_sha256}".encode()).hexdigest()[:32]


@dataclasses.dataclass(frozen=True)
class Invoice:
    id: str
    merchant: str
    order_key_sha256: str
    amount_raw: int
    tag: int
    pay_raw: int
    created_at: int
    expires_at: int
    state: str
    closed_at: int = None
    send_block: str = None
    receive_block: str = None
    sender: str = None
    received_raw: int = None

    def to_dict(self):
        d = dataclasses.asdict(self)
        for k in ("amount_raw", "pay_raw", "received_raw"):
            if d[k] is not None:
                d[k] = str(d[k])
        return d


SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices(
  id TEXT PRIMARY KEY,
  merchant TEXT NOT NULL,
  order_key_sha256 TEXT NOT NULL,
  amount_raw TEXT NOT NULL,
  tag INTEGER NOT NULL CHECK (tag > 0 AND tag < 1000000),
  pay_raw TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  state TEXT NOT NULL DEFAULT 'open'
    CHECK (state IN ('open','paid','underpaid','overpaid','expired')),
  closed_at INTEGER,
  send_block TEXT,
  receive_block TEXT,
  sender TEXT,
  received_raw TEXT,
  UNIQUE (merchant, order_key_sha256)
);
CREATE UNIQUE INDEX IF NOT EXISTS invoices_open_tag ON invoices(merchant, tag) WHERE state = 'open';
CREATE TRIGGER IF NOT EXISTS invoices_terminal BEFORE UPDATE OF state ON invoices
  WHEN OLD.state != 'open'
  BEGIN SELECT RAISE(ABORT, 'illegal transition: invoice already closed'); END;
CREATE TABLE IF NOT EXISTS payments(
  send_block TEXT PRIMARY KEY,
  receive_block TEXT UNIQUE,
  merchant TEXT NOT NULL,
  invoice_id TEXT REFERENCES invoices(id),
  kind TEXT NOT NULL
    CHECK (kind IN ('payment','underpaid','overpaid','duplicate','late','not_income')),
  sender TEXT NOT NULL,
  amount_raw TEXT NOT NULL,
  block_ts INTEGER,
  reason TEXT,
  recorded_at INTEGER NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS payments_one_settlement ON payments(invoice_id)
  WHERE kind IN ('payment','underpaid','overpaid');
"""


class Store:
    """A single SQLite file. Every write runs inside BEGIN IMMEDIATE, so two
    processes cannot both settle one invoice or bind one block twice."""

    def __init__(self, path, timeout=30.0):
        self.path = str(path)
        self.conn = sqlite3.connect(self.path, timeout=timeout, isolation_level=None,
                                    check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(f"PRAGMA busy_timeout = {int(timeout * 1000)}")
        if self.path != ":memory:":
            self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    @contextlib.contextmanager
    def tx(self):
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield self.conn
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")

    @staticmethod
    def _invoice(row):
        d = dict(row)
        for k in ("amount_raw", "pay_raw", "received_raw"):
            if d[k] is not None:
                d[k] = int(d[k])
        return Invoice(**d)

    def get(self, invoice):
        inv_id = invoice.id if isinstance(invoice, Invoice) else invoice
        row = self.conn.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone()
        if row is None:
            raise NotFound(f"no invoice {inv_id}")
        return self._invoice(row)

    def payment(self, send_block):
        row = self.conn.execute("SELECT * FROM payments WHERE send_block = ?", (send_block,)).fetchone()
        return _payment(row) if row else None

    def payments_for(self, invoice_id):
        rows = self.conn.execute(
            "SELECT * FROM payments WHERE invoice_id = ? ORDER BY block_ts, send_block", (invoice_id,)).fetchall()
        return [_payment(r) for r in rows]

    def record(self, observed, kind, invoice_id=None, reason=None, now=None):
        """Bind a block to an invoice (or to nothing, for not_income). A block can
        be recorded once; settling kinds also move the invoice out of 'open' in
        the same transaction."""
        now = int(time.time()) if now is None else now
        with self.tx() as c:
            prior = c.execute("SELECT invoice_id, kind FROM payments WHERE send_block = ?",
                              (observed["send_block"],)).fetchone()
            if prior is not None:
                raise BlockAlreadyBound(
                    f"block {observed['send_block']} already recorded as {prior['kind']} "
                    f"for {prior['invoice_id']}")
            if kind in SETTLING_KINDS:
                _transition(c, invoice_id, KIND_TO_STATE[kind], now, observed)
            try:
                c.execute(
                    "INSERT INTO payments(send_block, receive_block, merchant, invoice_id, kind, sender,"
                    " amount_raw, block_ts, reason, recorded_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (observed["send_block"], observed.get("receive_block"), observed["merchant"], invoice_id,
                     kind, observed["sender"], str(observed["amount_raw"]), observed.get("block_ts"),
                     reason, now))
            except sqlite3.IntegrityError as e:
                raise BlockAlreadyBound(str(e)) from e
        return self.payment(observed["send_block"])

    def expire(self, invoice_id, now=None):
        now = int(time.time()) if now is None else now
        with self.tx() as c:
            _transition(c, invoice_id, "expired", now, None)
        return self.get(invoice_id)


def _payment(row):
    d = dict(row)
    d["amount_raw"] = int(d["amount_raw"])
    return d


def _transition(c, invoice_id, new_state, now, observed):
    row = c.execute("SELECT state FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    if row is None:
        raise NotFound(f"no invoice {invoice_id}")
    if new_state not in TRANSITIONS.get(row["state"], ()):
        raise IllegalTransition(f"{invoice_id}: {row['state']} -> {new_state} is not allowed")
    if observed is None:
        cur = c.execute("UPDATE invoices SET state = ?, closed_at = ? WHERE id = ? AND state = 'open'",
                        (new_state, now, invoice_id))
    else:
        cur = c.execute(
            "UPDATE invoices SET state = ?, closed_at = ?, send_block = ?, receive_block = ?, sender = ?,"
            " received_raw = ? WHERE id = ? AND state = 'open'",
            (new_state, now, observed["send_block"], observed.get("receive_block"), observed["sender"],
             str(observed["amount_raw"]), invoice_id))
    if cur.rowcount != 1:
        raise IllegalTransition(f"{invoice_id}: lost the race to {new_state}")


def _require_store(store):
    if not isinstance(store, Store):
        raise InvoiceError("store=Store(path) is required")
    return store


def create_invoice(merchant_account, amount_raw, order_key, expires_s=3600, store=None, now=None,
                   _rand=secrets.randbelow):
    """Idempotent: the same (merchant, order_key) always returns the same invoice.
    The same order key with a different amount raises OrderConflict."""
    store = _require_store(store)
    merchant = acct.normalise(merchant_account)
    require_raw(amount_raw, "amount_raw", minimum=TAG_MODULUS)
    if amount_raw % TAG_MODULUS:
        raise AmountError(
            f"amount_raw must be a multiple of {TAG_MODULUS} raw (1e-24 XNO): its lowest six digits carry "
            f"the invoice tag; round the price, e.g. to {amount_raw - amount_raw % TAG_MODULUS}")
    if isinstance(expires_s, bool) or not isinstance(expires_s, int) or expires_s <= 0:
        raise InvoiceError("expires_s must be a positive int (seconds)")
    now = int(time.time()) if now is None else now
    okh = order_key_hash(order_key)
    inv_id = invoice_id_for(merchant, okh)
    with store.tx() as c:
        row = c.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone()
        if row is not None:
            existing = Store._invoice(row)
            if existing.amount_raw != amount_raw:
                raise OrderConflict(
                    f"order already invoiced as {existing.id} for {existing.amount_raw} raw; "
                    f"refusing a second invoice for {amount_raw} raw")
            return existing
        busy = {r[0] for r in c.execute(
            "SELECT tag FROM invoices WHERE merchant = ? AND (state = 'open' OR closed_at > ?)",
            (merchant, now - TAG_QUARANTINE_S))}
        tag = _allocate_tag(busy, _rand)
        pay_raw = amount_raw + tag
        require_raw(pay_raw, "pay_raw")
        c.execute(
            "INSERT INTO invoices(id, merchant, order_key_sha256, amount_raw, tag, pay_raw, created_at,"
            " expires_at, state) VALUES (?,?,?,?,?,?,?,?, 'open')",
            (inv_id, merchant, okh, str(amount_raw), tag, str(pay_raw), now, now + expires_s))
    return store.get(inv_id)


def _allocate_tag(busy, rand):
    if len(busy) >= TAG_MODULUS - 1:
        raise TagsExhausted("every tag is open or in quarantine for this merchant")
    for _ in range(64):
        tag = 1 + rand(TAG_MODULUS - 1)
        if tag not in busy:
            return tag
    for tag in range(1, TAG_MODULUS):
        if tag not in busy:
            return tag
    raise TagsExhausted("no free tag")


# ---------------------------------------------------------------- ledger reads

def _blocks_field(data):
    blocks = data.get("blocks") if isinstance(data, dict) else None
    if not blocks:
        return {}
    if isinstance(blocks, list):
        return {h: None for h in blocks}
    return blocks


def _subtype(info):
    t = info.get("subtype") or info.get("type")
    if t == "state":
        t = info.get("subtype")
    if not t and isinstance(info.get("contents"), dict):
        t = info["contents"].get("type")
    return t


def _resolve_send(rpc, merchant, send_hash, receive_hash=None, receive_ts=0):
    info = rpc.call("block_info", json_block="true", hash=send_hash)
    contents = info.get("contents") or {}
    dest = contents.get("link_as_account") or contents.get("destination")
    sender = acct.normalise(info["block_account"])
    problems = []
    if _subtype(info) != "send":
        problems.append(f"block is a {_subtype(info)}, not a send")
    if not dest or acct.normalise(dest) != merchant:
        problems.append("send is not addressed to the merchant")
    ts = int(info.get("local_timestamp") or 0) or int(receive_ts or 0)
    return {
        "send_block": send_hash.upper(),
        "receive_block": receive_hash.upper() if receive_hash else None,
        "merchant": merchant,
        "sender": sender,
        "amount_raw": int(info["amount"]),
        "confirmed": str(info.get("confirmed")).lower() == "true",
        "block_ts": ts,
        "problems": problems,
    }


def scan(rpc, merchant, tag, since, max_blocks=1000):
    """Every incoming send to merchant whose amount ends in this tag, with its
    sender, amount, confirmation and timestamp read from the ledger."""
    rpc = as_rpc(rpc)
    found = {}
    pending = _blocks_field(rpc.call("receivable", account=merchant, count=str(max_blocks), source="true"))
    for h, info in pending.items():
        amount = int(info["amount"]) if isinstance(info, dict) else (int(info) if info is not None else None)
        if amount is not None and amount % TAG_MODULUS != tag:
            continue
        ob = _resolve_send(rpc, merchant, h)
        if ob["amount_raw"] % TAG_MODULUS == tag:
            found[ob["send_block"]] = ob
    head, seen = None, 0
    while seen < max_blocks:
        data = rpc.call("account_history", account=merchant, count=str(min(200, max_blocks - seen)), head=head)
        history = data.get("history") or []
        if not history:
            break
        older = False
        for e in history:
            seen += 1
            ts = int(e.get("local_timestamp") or 0)
            if ts and ts < since:
                older = True
                break
            if _subtype(e) != "receive" or int(e["amount"]) % TAG_MODULUS != tag:
                continue
            rinfo = rpc.call("block_info", json_block="true", hash=e["hash"])
            link = (rinfo.get("contents") or {}).get("link") or (rinfo.get("contents") or {}).get("source")
            if not link or acct.normalise(rinfo["block_account"]) != merchant:
                continue
            ob = _resolve_send(rpc, merchant, link, receive_hash=e["hash"], receive_ts=ts)
            ob["confirmed"] = ob["confirmed"] and str(rinfo.get("confirmed")).lower() == "true"
            found.setdefault(ob["send_block"], ob)
        nxt = data.get("previous")
        if older or not nxt:
            break
        head = nxt
    return sorted(found.values(), key=lambda o: (o["block_ts"], o["send_block"]))


# ---------------------------------------------------------------- checking

def _accounts(values):
    return {acct.normalise(v) for v in (values or ())}


def check_invoice(invoice, rpc=None, store=None, own_accounts=(), not_income=None, now=None,
                  max_blocks=1000, skew_s=CLOCK_SKEW_S):
    """Read the merchant's account from the public ledger and settle the invoice.

    A block pays only if: it is a confirmed send to the merchant, it was sent
    after the invoice was created, before it expired, its amount ends in this
    invoice's tag, it is not from the merchant's own or a not-income account,
    and it is not already bound to any invoice. Exactly pay_raw -> paid.
    """
    store = _require_store(store)
    inv = store.get(invoice)
    now = int(time.time()) if now is None else now
    own = _accounts(own_accounts) | {inv.merchant}
    excluded = {acct.normalise(k): v for k, v in (not_income or {}).items()}
    observations = []
    for ob in scan(rpc, inv.merchant, inv.tag, inv.created_at - skew_s, max_blocks):
        view = {k: (str(v) if k == "amount_raw" else v) for k, v in ob.items() if k != "problems"}
        if ob["problems"]:
            observations.append(dict(view, outcome="ignored", reason="; ".join(ob["problems"])))
            continue
        if not ob["block_ts"]:
            observations.append(dict(view, outcome="ignored",
                                     reason="no timestamp: cannot prove it was sent after the invoice"))
            continue
        if ob["block_ts"] < inv.created_at - skew_s:
            observations.append(dict(view, outcome="ignored", reason="sent before the invoice existed"))
            continue
        if not ob["confirmed"]:
            observations.append(dict(view, outcome="unconfirmed", reason="not confirmed yet; re-check later"))
            continue
        prior = store.payment(ob["send_block"])
        if prior is not None:
            observations.append(dict(view, outcome="already_recorded", kind=prior["kind"],
                                     invoice_id=prior["invoice_id"]))
            continue
        if ob["sender"] in own or ob["sender"] in excluded:
            reason = ("from the merchant's own account" if ob["sender"] in own
                      else f"listed as not income: {excluded[ob['sender']]}")
            observations.append(_record(store, ob, "not_income", inv.id, reason, now, view))
            continue
        current = store.get(inv.id)
        if ob["block_ts"] > inv.expires_at:
            observations.append(_record(store, ob, "late", inv.id, "sent after the invoice expired", now, view))
            continue
        if current.state == "open":
            kind = ("payment" if ob["amount_raw"] == inv.pay_raw
                    else "underpaid" if ob["amount_raw"] < inv.pay_raw else "overpaid")
            try:
                observations.append(_record(store, ob, kind, inv.id, None, now, view))
                continue
            except IllegalTransition:
                current = store.get(inv.id)  # another process settled it first
        kind = "late" if current.state == "expired" else "duplicate"
        observations.append(_record(store, ob, kind, inv.id, f"invoice already {current.state}", now, view))
    current = store.get(inv.id)
    if current.state == "open" and now > current.expires_at + skew_s:
        try:
            current = store.expire(inv.id, now)
        except IllegalTransition:
            current = store.get(inv.id)
    return {
        "invoice": current.to_dict(),
        "observations": observations,
        "refunds": refund_hints(store, inv.id),
    }


def _record(store, ob, kind, inv_id, reason, now, view):
    try:
        store.record(ob, kind, inv_id, reason, now)
    except BlockAlreadyBound as e:
        return dict(view, outcome="already_recorded", reason=str(e))
    return dict(view, outcome=kind, reason=reason)


# ---------------------------------------------------------------- refunds

REFUND_KINDS = ("overpaid", "underpaid", "duplicate", "late")


def refund_instruction(item, store=None, claimed_payer=None):
    """An instruction, never a transfer. `item` is a payment record, a send block
    hash (needs store) or an Invoice/id (needs store; returns its settling
    payment's refund). The destination is always the sender read from the
    ledger; a claimed payer is ignored and reported."""
    if isinstance(item, dict):
        pay = item
    elif isinstance(item, (Invoice, str)) and store is not None:
        pay = None
        if isinstance(item, str) and not item.startswith("inv_"):
            pay = store.payment(item.upper())
            if pay is None:
                raise NotFound(f"no recorded block {item}")
        else:
            inv = store.get(item)
            settled = [p for p in store.payments_for(inv.id) if p["kind"] in SETTLING_KINDS]
            if not settled:
                return None
            pay = settled[0]
    else:
        raise InvoiceError("pass a payment record, or a block hash / invoice with store=")
    if pay["kind"] not in REFUND_KINDS:
        return None
    amount = pay["amount_raw"]
    if pay["kind"] == "overpaid":
        inv = store.get(pay["invoice_id"]) if store is not None else None
        if inv is None:
            raise InvoiceError("an overpayment refund needs store= to read the invoice's pay_raw")
        amount = pay["amount_raw"] - inv.pay_raw
    out = {
        "to": pay["sender"],
        "amount_raw": amount,
        "reason": pay["kind"],
        "source_block": pay["send_block"],
        "invoice_id": pay["invoice_id"],
        "note": "instruction only: nano-invoice never sends; pay it from the merchant wallet",
    }
    if claimed_payer is not None:
        claimed = claimed_payer if not acct.is_valid(claimed_payer) else acct.normalise(claimed_payer)
        if claimed != pay["sender"]:
            out["ignored_claimed_payer"] = claimed_payer
            out["note"] += "; the claimed payer differs from the ledger's sender and was ignored"
    return out


def refund_hints(store, invoice_id):
    hints = []
    for p in store.payments_for(invoice_id):
        r = refund_instruction(p, store=store)
        if r:
            r = dict(r, amount_raw=str(r["amount_raw"]))
            hints.append(r)
    return hints


# ---------------------------------------------------------------- receipts

def receipt(invoice, store=None):
    store = _require_store(store)
    inv = store.get(invoice)
    if inv.state not in ("paid", "overpaid", "underpaid"):
        raise InvoiceError(f"{inv.id} is {inv.state}: no settling block to put on a receipt")
    pay = store.payment(inv.send_block)
    reproduce = [{"action": "block_info", "json_block": "true", "hash": inv.send_block}]
    claims = [
        "block_info(send_block).block_account == sender",
        "block_info(send_block).subtype == 'send'",
        "block_info(send_block).contents.link_as_account == merchant",
        "block_info(send_block).amount == received_raw",
        "block_info(send_block).confirmed == 'true'",
    ]
    if inv.receive_block:
        reproduce.append({"action": "block_info", "json_block": "true", "hash": inv.receive_block})
        claims += [
            "block_info(receive_block).block_account == merchant",
            "block_info(receive_block).contents.link == send_block",
            "block_info(receive_block).confirmed == 'true'",
        ]
    return {
        "schema": RECEIPT_SCHEMA,
        "invoice_id": inv.id,
        "id_rule": f"'inv_' + sha256('{ID_PREFIX}|' + merchant + '|' + order_key_sha256).hexdigest()[:32]",
        "order_key_sha256": inv.order_key_sha256,
        "merchant": inv.merchant,
        "amount_raw": str(inv.amount_raw),
        "tag": inv.tag,
        "pay_raw": str(inv.pay_raw),
        "state": inv.state,
        "send_block": inv.send_block,
        "receive_block": inv.receive_block,
        "sender": inv.sender,
        "received_raw": str(inv.received_raw),
        "confirmed": True,
        "created_at": inv.created_at,
        "expires_at": inv.expires_at,
        "sent_at": pay["block_ts"] if pay else None,
        "reproduce": reproduce,
        "claims": claims,
    }


def verify_receipt(rcpt, rpc=None):
    """Re-check a receipt from its own fields and the public ledger alone."""
    rpc = as_rpc(rpc)
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        return bool(ok)

    try:
        merchant = acct.normalise(rcpt["merchant"])
        sender = acct.normalise(rcpt["sender"])
        amount, tag, pay = int(rcpt["amount_raw"]), int(rcpt["tag"]), int(rcpt["pay_raw"])
        received = int(rcpt["received_raw"])
        send_block = rcpt["send_block"].upper()
    except (KeyError, ValueError, TypeError, acct.InvalidAccount) as e:
        check("receipt_well_formed", False, str(e))
        return {"ok": False, "checks": checks}
    check("schema", rcpt.get("schema") == RECEIPT_SCHEMA, rcpt.get("schema", ""))
    check("invoice_id_rederives", invoice_id_for(merchant, rcpt["order_key_sha256"]) == rcpt["invoice_id"])
    check("tag_in_range", 0 <= tag < TAG_MODULUS, f"tag={tag}" + (" (0 = untagged, binds no order)" if tag == 0 else ""))
    check("amount_leaves_room_for_tag", amount % TAG_MODULUS == 0)
    check("pay_raw_is_amount_plus_tag", pay == amount + tag)
    check("received_ends_in_tag", received % TAG_MODULUS == tag)
    expected_state = "paid" if received == pay else "overpaid" if received > pay else "underpaid"
    check("state_matches_amount", rcpt.get("state") == expected_state, f"expected {expected_state}")
    try:
        s = rpc.call("block_info", json_block="true", hash=send_block)
        contents = s.get("contents") or {}
        dest = contents.get("link_as_account") or contents.get("destination")
        check("send.block_account == sender", acct.normalise(s["block_account"]) == sender, s["block_account"])
        check("send.subtype == send", _subtype(s) == "send", str(_subtype(s)))
        check("send.destination == merchant", bool(dest) and acct.normalise(dest) == merchant, str(dest))
        check("send.amount == received_raw", int(s["amount"]) == received, s["amount"])
        check("send.confirmed", str(s.get("confirmed")).lower() == "true", str(s.get("confirmed")))
        if rcpt.get("receive_block"):
            r = rpc.call("block_info", json_block="true", hash=rcpt["receive_block"])
            rc = r.get("contents") or {}
            link = (rc.get("link") or rc.get("source") or "").upper()
            check("receive.block_account == merchant", acct.normalise(r["block_account"]) == merchant,
                  r["block_account"])
            check("receive.link == send_block", link == send_block, link)
            check("receive.confirmed", str(r.get("confirmed")).lower() == "true", str(r.get("confirmed")))
    except Exception as e:  # an unreachable or lying node must never read as verified
        check("ledger_reachable", False, f"{type(e).__name__}: {e}")
    return {"ok": all(c["ok"] for c in checks), "checks": checks}
