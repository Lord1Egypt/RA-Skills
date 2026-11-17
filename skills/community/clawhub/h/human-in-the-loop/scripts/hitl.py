#!/usr/bin/env python3
"""Approval lifecycle + crash-safe apply for agent actions that need a human.

Stdlib only, Python 3.9+, POSIX (fcntl). Every guard fails CLOSED: absent,
empty, null or wrongly typed input raises `Refused`; it never passes.

    python3 hitl.py --selftest          # hostile fixtures, exit 1 on any failure
    python3 hitl.py status <state.json> # read-only: counts, waiting_human gates, uncertain items

States (one item = one plan = ONE mutating action):
    proposed -> waiting_human -> approved -> applying -> applied
                     |  \\-> rejected | expired         \\-> uncertain -> (reconcile)
A `draft_only` item may go proposed -> applying without an approval: the draft
filter is then the only barrier, so it runs in code before any creation.
"""
from __future__ import annotations

import base64
import contextlib
import fcntl
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

CLOCK_SKEW_S = 60
MIN_SECRET_BYTES = 32
MAX_ATTEMPTS = 2                      # first try + one bounded retry, then a human
DRAFT_VERBS = frozenset({"create_draft", "update_draft"})
STATES = ("proposed", "waiting_human", "approved", "applying", "applied",
          "uncertain", "rejected", "expired")
ALLOWED = {                           # from -> to; anything else raises
    None: {"proposed"},
    "proposed": {"waiting_human", "applying"},
    "waiting_human": {"waiting_human", "approved", "rejected", "expired"},
    "expired": {"waiting_human"},
    "rejected": {"waiting_human"},
    "approved": {"applying", "waiting_human"},
    "applying": {"applied", "uncertain", "approved", "proposed", "waiting_human"},
    "uncertain": {"applied", "approved", "proposed", "waiting_human"},
    "applied": set(),
}
_GATE = re.compile(r"^[a-z][a-z0-9_]{2,48}$")
_ITEM = re.compile(r"^[A-Za-z0-9_.:-]{1,80}$")
_APPROVER = re.compile(r"^[A-Za-z0-9_.@-]{2,64}$")
_MARKER = "[TO COMPLETE: %s]"
_PLACEHOLDER = re.compile(r"\{\{\s*[A-Za-z_][A-Za-z0-9_.]*\s*\}\}")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


class Refused(Exception):
    """A check that did not positively pass."""


class SkipLocked(Exception):
    """Another run holds a live lock: do nothing this tick."""


def _now(now: Optional[int]) -> int:
    if now is None:
        return int(time.time())
    if type(now) is not int:
        raise Refused("now must be an int epoch")
    return now


# ------------------------------------------------------------------ plan

def fingerprint(plan: Any) -> str:
    """sha256 of canonical JSON. Plan = {"action": {"verb", "target", ...},
    "business_key": {...}, optional "unknowns": [...] and any other field}."""
    if not isinstance(plan, dict) or not plan:
        raise Refused("plan must be a non-empty dict")
    act, key = plan.get("action"), plan.get("business_key")
    if not isinstance(act, dict) or not isinstance(act.get("verb"), str) or not act["verb"] \
            or not isinstance(act.get("target"), str) or not act["target"]:
        raise Refused("plan.action needs non-empty verb and target")
    if not isinstance(key, dict) or not key or not all(
            isinstance(k, str) and isinstance(v, (str, int)) and not isinstance(v, bool)
            and str(v).strip() for k, v in key.items()):
        raise Refused("plan.business_key must map names to non-empty str/int values")
    unk = plan.get("unknowns", [])
    if not isinstance(unk, list) or not all(isinstance(u, str) and u.strip() for u in unk):
        raise Refused("plan.unknowns must be a list of non-empty strings")
    try:
        blob = json.dumps(plan, sort_keys=True, separators=(",", ":"), allow_nan=False,
                          ensure_ascii=False)
    except (TypeError, ValueError):
        raise Refused("plan is not canonical JSON") from None
    return hashlib.sha256(blob.encode()).hexdigest()


def _same(a: Any, b: Any) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# ------------------------------------------------------------------ store

class Store:
    """JSON state file, one flock'ed transaction per call, atomic replace.
    Holds statuses, fingerprints, nonce digests and remote ids, never plan content."""

    def __init__(self, path: Any):
        if not isinstance(path, (str, Path)) or not str(path):
            raise Refused("no state path")
        self.path = Path(path)
        self.lock = Path(str(path) + ".lock")

    @contextlib.contextmanager
    def txn(self):
        try:
            fd = os.open(str(self.lock), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        except OSError as e:
            raise Refused("state lock unusable: %s" % type(e).__name__) from None
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            data = self._load()
            yield data                # an exception inside the block discards changes
            self._save(data)
        finally:
            os.close(fd)

    def read(self) -> Dict[str, Any]:
        """Locked read, never writes (for status/reporting)."""
        try:
            fd = os.open(str(self.lock), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        except OSError as e:
            raise Refused("state lock unusable: %s" % type(e).__name__) from None
        try:
            fcntl.flock(fd, fcntl.LOCK_SH)
            return self._load()
        finally:
            os.close(fd)

    def _load(self) -> Dict[str, Any]:
        if os.path.islink(self.path):
            raise Refused("state file is a symlink")
        if not self.path.exists():
            return {"v": 1, "items": {}}
        try:
            data = json.loads(self.path.read_text("utf-8"))
        except (OSError, ValueError):
            raise Refused("state corrupt; refusing rather than guessing") from None
        if not isinstance(data, dict) or data.get("v") != 1 or not isinstance(data.get("items"), dict) \
                or not all(isinstance(r, dict) and r.get("status") in STATES
                           for r in data["items"].values()):
            raise Refused("state corrupt; refusing rather than guessing")
        return data

    def _save(self, data: Dict[str, Any]) -> None:
        tmp = self.path.with_name(".%s.%s.tmp" % (self.path.name, secrets.token_hex(6)))
        fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            os.write(fd, json.dumps(data, sort_keys=True, indent=1).encode())
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(str(tmp), str(self.path))


def _move(rec: Dict[str, Any], to: str, now: int, **fields: Any) -> None:
    frm = rec.get("status")
    if to not in ALLOWED.get(frm, set()):
        raise Refused("illegal transition %s -> %s" % (frm, to))
    rec.update(fields, status=to, updated_at=now)
    rec.setdefault("history", []).append([now, frm, to])


def _item(data: Dict[str, Any], item_id: Any) -> Dict[str, Any]:
    if not isinstance(item_id, str) or not _ITEM.match(item_id):
        raise Refused("bad item id")
    rec = data["items"].get(item_id)
    if rec is None:
        raise Refused("unknown item")
    return rec


# ------------------------------------------------------------------ lifecycle

def propose(store: Store, item_id: str, plan: Any, regime: str, now: Optional[int] = None) -> None:
    t, fp = _now(now), fingerprint(plan)
    if regime not in ("approval", "draft_only"):
        raise Refused("regime must be 'approval' or 'draft_only'")
    if regime == "draft_only" and plan["action"]["verb"] not in DRAFT_VERBS:
        raise Refused("draft_only regime cannot carry a %r action" % plan["action"]["verb"])
    if not isinstance(item_id, str) or not _ITEM.match(item_id):
        raise Refused("bad item id")
    with store.txn() as d:
        if item_id in d["items"]:
            raise Refused("item exists; never re-propose a known item (reconcile or reopen)")
        rec: Dict[str, Any] = {"status": None}
        _move(rec, "proposed", t, fp=fp, regime=regime, attempts=0, gates=[])
        d["items"][item_id] = rec


def open_request(store: Store, item_id: str, plan: Any, gates: Any, ttl_s: int = 3600,
                 now: Optional[int] = None) -> str:
    """-> waiting_human with named gates and a fresh single-use nonce. Returns the
    nonce to show next to the plan; only its sha256 is stored. Supersedes any older
    request (its token dies)."""
    t, fp = _now(now), fingerprint(plan)
    if not isinstance(gates, list) or not gates or not all(isinstance(g, str) and _GATE.match(g) for g in gates):
        raise Refused("gates must be a non-empty list of snake_case names")
    if type(ttl_s) is not int or not 60 <= ttl_s <= 7 * 86400:
        raise Refused("ttl_s must be an int in [60, 604800]")
    nonce = secrets.token_urlsafe(24)
    with store.txn() as d:
        rec = _item(d, item_id)
        if rec["status"] in ("applying", "uncertain", "applied"):
            raise Refused("item is %s: reconcile first, a new OK cannot restart a creation" % rec["status"])
        _move(rec, "waiting_human", t, fp=fp, gates=list(gates), request_exp=t + ttl_s,
              nonce_sha256=hashlib.sha256(nonce.encode()).hexdigest())
    return nonce


def sign_decision(secret: Any, item_id: str, nonce: str, fp: str, approver: str, decision: str,
                  ttl_s: int = 900, now: Optional[int] = None) -> str:
    """Approval side (bot on the private channel, after checking the sender id)."""
    key, t = _key(secret), _now(now)
    if decision not in ("approve", "reject") or not isinstance(approver, str) \
            or not _APPROVER.match(approver) or not isinstance(nonce, str) or len(nonce) < 16:
        raise Refused("bad decision, approver or nonce")
    body = {"v": 1, "rid": item_id, "fp": fp, "nonce": nonce, "approver": approver,
            "decision": decision, "iat": t, "exp": t + int(ttl_s)}
    raw = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=") + "." + \
        hmac.new(key, raw, hashlib.sha256).hexdigest()


def _key(secret: Any) -> bytes:
    if isinstance(secret, str):
        secret = secret.encode()
    if not isinstance(secret, bytes) or len(secret) < MIN_SECRET_BYTES:
        raise Refused("approval secret absent or shorter than %d bytes" % MIN_SECRET_BYTES)
    return secret


def _claims(token: Any, key: bytes) -> Dict[str, Any]:
    if not isinstance(token, str) or token.count(".") != 1:
        raise Refused("not a signed decision (free text is never an approval)")
    b64, sig = token.split(".")
    try:
        raw = base64.urlsafe_b64decode(b64 + "=" * (-len(b64) % 4))
        body = json.loads(raw)
    except (ValueError, TypeError):
        raise Refused("token undecodable") from None
    if not hmac.compare_digest(hmac.new(key, raw, hashlib.sha256).hexdigest(), sig):
        raise Refused("bad signature")
    if not isinstance(body, dict) or set(body) != {"v", "rid", "fp", "nonce", "approver",
                                                   "decision", "iat", "exp"}:
        raise Refused("unexpected claims")
    if body["v"] != 1 or type(body["iat"]) is not int or type(body["exp"]) is not int \
            or not all(isinstance(body[k], str) for k in ("rid", "fp", "nonce", "approver", "decision")):
        raise Refused("bad claim types")
    return body


def decide(store: Store, item_id: str, token: Any, secret: Any, plan: Any, approvers: Iterable[str],
           now: Optional[int] = None) -> str:
    """Redeem a signed decision: -> approved | rejected. Single use: the stored
    nonce digest is cleared in the same locked step. An expired request is marked
    `expired` and refused, whatever the token says."""
    key, t, fp = _key(secret), _now(now), fingerprint(plan)
    allowed = set(approvers or ())
    if not allowed:
        raise Refused("no approver allowlist")
    c = _claims(token, key)
    err, result = None, None
    with store.txn() as d:
        rec = _item(d, item_id)
        if rec["status"] != "waiting_human" or not rec.get("nonce_sha256"):
            raise Refused("no open request for this item (replay or never asked)")
        if t >= rec["request_exp"]:
            _move(rec, "expired", t, nonce_sha256=None)
            err = "request expired; open a new one"
        elif c["rid"] != item_id or not hmac.compare_digest(
                hashlib.sha256(c["nonce"].encode()).hexdigest(), rec["nonce_sha256"]):
            raise Refused("token belongs to another item or an older request")
        elif not (hmac.compare_digest(c["fp"], rec["fp"]) and hmac.compare_digest(fp, rec["fp"])):
            raise Refused("plan changed since the request; the OK covered another plan")
        elif c["approver"] not in allowed:
            raise Refused("approver not allowed")
        elif c["exp"] <= c["iat"] or c["iat"] > t + CLOCK_SKEW_S or c["exp"] <= t:
            raise Refused("decision expired or not yet valid")
        elif c["decision"] not in ("approve", "reject"):
            raise Refused("unknown decision")
        else:
            result = "approved" if c["decision"] == "approve" else "rejected"
            _move(rec, result, t, nonce_sha256=None, approver=c["approver"],
                  approval_exp=min(c["exp"], rec["request_exp"]) if result == "approved" else None)
    if err:
        raise Refused(err)
    return result


def sweep_expired(store: Store, now: Optional[int] = None) -> List[str]:
    t, out = _now(now), []
    with store.txn() as d:
        for iid, rec in d["items"].items():
            if rec["status"] == "waiting_human" and rec.get("nonce_sha256") and t >= rec["request_exp"]:
                _move(rec, "expired", t, nonce_sha256=None)
                out.append(iid)
    return out


# ------------------------------------------------------------------ draft filter

def draft_gate(action: Any, draft: Any, plan: Dict[str, Any], forbidden: Any) -> List[str]:
    """Blocking reasons for a draft ([] = may be created). Runs BEFORE creation.
    Never blocks on ordinary words: only on structure the plan makes checkable."""
    if not isinstance(draft, dict) or not isinstance(draft.get("body"), str):
        raise Refused("draft must be a dict with a str body")
    if not isinstance(forbidden, list) or not all(isinstance(p, str) and p for p in forbidden):
        raise Refused("forbidden must be a list of regex strings (may be empty)")
    reasons = []
    if action.get("verb") not in DRAFT_VERBS:
        reasons.append("not_a_draft_action")
    if draft.get("target") != plan["action"]["target"]:
        reasons.append("target_mismatch")
    visible = _HTML_COMMENT.sub(" ", draft["body"])
    if not visible.strip():
        reasons.append("empty_body")
    for field in plan.get("unknowns", []):
        if (_MARKER % field) not in visible:
            reasons.append("marker_missing:%s" % field)
    if _PLACEHOLDER.search(visible):
        reasons.append("unresolved_placeholder")
    for i, pat in enumerate(forbidden):
        if re.search(pat, visible):
            reasons.append("forbidden_pattern:%d" % i)
    return reasons


# ------------------------------------------------------------------ apply

def begin_apply(store: Store, item_id: str, plan: Any, action: Any, draft: Any = None,
                forbidden: Any = None, now: Optional[int] = None) -> Dict[str, Any]:
    """Persist `applying` BEFORE the API call. Refuses anything but the exact
    approved action, a stale approval, and any item that must reconcile first."""
    t, fp = _now(now), fingerprint(plan)
    with store.txn() as d:
        rec = _item(d, item_id)
        st = rec["status"]
        if st in ("applying", "uncertain"):
            raise Refused("previous attempt unresolved: reconcile first, never re-create")
        if not (st == "approved" or (st == "proposed" and rec["regime"] == "draft_only")):
            raise Refused("item is %s, not approved" % st)
        if not hmac.compare_digest(fp, rec["fp"]):
            raise Refused("plan changed after approval")
        try:
            same = isinstance(action, dict) and _same(action, plan["action"])
        except (TypeError, ValueError):
            same = False
        if not same:
            raise Refused("action differs from the approved one; an OK is not a permit for the adjacent")
        if st == "approved" and t >= rec.get("approval_exp", 0):
            _move(rec, "waiting_human", t, gates=["approval_stale"], nonce_sha256=None)
            return {"status": "waiting_human", "gates": ["approval_stale"]}
        if rec["regime"] == "draft_only" or action["verb"] in DRAFT_VERBS:
            reasons = draft_gate(action, draft, plan, forbidden)
            if reasons:
                _move(rec, "waiting_human", t, gates=["draft_filter"], reasons=reasons,
                      nonce_sha256=None)
                return {"status": "waiting_human", "gates": ["draft_filter"], "reasons": reasons}
        _move(rec, "applying", t, attempts=rec["attempts"] + 1)
    return {"status": "applying"}


def record_result(store: Store, item_id: str, response: Any, id_key: str = "id",
                  now: Optional[int] = None) -> str:
    """Success = the id the API returned. Exit 0, {}, None, "", True: `uncertain`."""
    t = _now(now)
    rid = response.get(id_key) if isinstance(response, dict) else None
    ok = (isinstance(rid, str) and rid.strip()) or (type(rid) is int and rid > 0)
    with store.txn() as d:
        rec = _item(d, item_id)
        if rec["status"] != "applying":
            raise Refused("no attempt in flight")
        if ok:
            _move(rec, "applied", t, remote_id=str(rid))
        else:
            _move(rec, "uncertain", t)
    return "applied" if ok else "uncertain"


def reconcile(store: Store, item_id: str, plan: Any, matches: Any, now: Optional[int] = None) -> str:
    """After crash/timeout/uncertain. `matches` = what YOUR lookup by business key
    returned; a lookup that failed must raise, never return []. Candidates are
    re-checked here: a candidate missing a key field counts as a possible duplicate."""
    t, fp = _now(now), fingerprint(plan)
    if not isinstance(matches, list) or not all(isinstance(m, dict) for m in matches):
        raise Refused("matches must be a list of dicts; unknown is not absent")
    key = {k: str(v).strip().casefold() for k, v in plan["business_key"].items()}
    exact, doubtful = [], 0
    for m in matches:
        vals = {k: m.get(k) for k in key}
        if any(v is None for v in vals.values()) or not m.get("id"):
            doubtful += 1
        elif all(str(vals[k]).strip().casefold() == key[k] for k in key):
            exact.append(m)
    with store.txn() as d:
        rec = _item(d, item_id)
        if rec["status"] not in ("applying", "uncertain"):
            raise Refused("nothing to reconcile")
        if not hmac.compare_digest(fp, rec["fp"]):
            raise Refused("plan changed; reconcile against the plan that was applied")
        if len(exact) == 1 and not doubtful:
            _move(rec, "applied", t, remote_id=str(exact[0]["id"]))
        elif exact or doubtful:
            _move(rec, "waiting_human", t, gates=["possible_duplicate"], nonce_sha256=None)
        elif rec["attempts"] >= MAX_ATTEMPTS:
            _move(rec, "waiting_human", t, gates=["retry_exhausted"], nonce_sha256=None)
        else:                                      # proven absent: one bounded retry
            _move(rec, "approved" if rec["regime"] == "approval" else "proposed", t)
        return rec["status"]


def guarded_apply(store: Store, item_id: str, plan: Any, action: Any,
                  create: Callable[[Dict[str, Any], Any], Any], draft: Any = None,
                  forbidden: Any = None, now: Optional[int] = None) -> Dict[str, Any]:
    """gate -> persist applying -> call -> record. An exception from `create`
    (timeout, 5xx, crash of the client) is `uncertain`, never `failed`."""
    r = begin_apply(store, item_id, plan, action, draft, forbidden, now)
    if r["status"] != "applying":
        return r
    try:
        response = create(action, draft)
    except Exception:
        record_result(store, item_id, None, now=now)
        return {"status": "uncertain"}
    return {"status": record_result(store, item_id, response, now=now)}


# ------------------------------------------------------------------ run lock

def acquire_lock(path: Any, job_id: str, ttl_s: int, app_running: Any,
                 now: Optional[int] = None) -> None:
    """One runner per external application. Live lock -> SkipLocked. Expired lock
    is taken over ONLY if app_running is exactly False; True/None/unknown -> Refused."""
    t = _now(now)
    if not isinstance(path, (str, Path)) or not str(path) or not isinstance(job_id, str) or not job_id:
        raise Refused("lock path and job id required")
    if type(ttl_s) is not int or ttl_s <= 0:
        raise Refused("ttl_s must be a positive int")
    try:
        fd = os.open(str(path), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    except OSError as e:
        raise Refused("lock unusable: %s" % type(e).__name__) from None
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        raw = os.read(fd, 65536).decode("utf-8", "replace").strip()
        if raw:
            try:
                cur = json.loads(raw)
                exp, holder = cur["expires_at"], cur["job_id"]
                if type(exp) is not int or not isinstance(holder, str):
                    raise TypeError
            except (ValueError, KeyError, TypeError):
                raise Refused("lock file corrupt: technical alert, do not overwrite") from None
            if t < exp:
                raise SkipLocked("SKIP_LOCKED held by %s" % holder)
            if app_running is not False:
                raise Refused("stale lock and the application may still be running: alert, do not overwrite")
        body = json.dumps({"job_id": job_id, "locked_at": t, "expires_at": t + int(ttl_s)})
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, body.encode())
        os.fsync(fd)
    finally:
        os.close(fd)


def release_lock(path: Any, job_id: str) -> None:
    try:
        fd = os.open(str(path), os.O_RDWR | os.O_NOFOLLOW)
    except OSError as e:
        raise Refused("lock unusable: %s" % type(e).__name__) from None
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            cur = json.loads(os.read(fd, 65536).decode())
        except ValueError:
            raise Refused("lock file corrupt") from None
        if not isinstance(cur, dict) or cur.get("job_id") != job_id:
            raise Refused("lock held by another job")
        os.ftruncate(fd, 0)
    finally:
        os.close(fd)


# ------------------------------------------------------------------ status

def status(path: str) -> int:
    items = Store(path).read()["items"]
    counts: Dict[str, int] = {}
    for rec in items.values():
        counts[rec["status"]] = counts.get(rec["status"], 0) + 1
    print("HITL STATUS " + " ".join("%s=%d" % kv for kv in sorted(counts.items())))
    for iid, rec in sorted(items.items()):
        if rec["status"] in ("waiting_human", "uncertain", "applying"):
            print("  %-14s %s gates=%s" % (rec["status"], iid, ",".join(rec.get("gates") or [])))
    return 0


# ------------------------------------------------------------------ selftest

def _selftest() -> int:
    fails: List[str] = []

    def refuses(name, fn, exc=Refused):
        try:
            fn()
        except exc:
            print("PASS refuse  %s" % name)
            return
        except Exception as e:  # a crash is not a refusal
            fails.append(name)
            print("FAIL crash   %s (%s: %s)" % (name, type(e).__name__, e))
            return
        fails.append(name)
        print("FAIL allowed %s" % name)

    def accepts(name, fn, check=lambda r: True):
        try:
            ok = bool(check(fn()))
        except Exception as e:
            ok = False
            print("     (%s: %s)" % (type(e).__name__, e))
        print(("PASS accept  %s" if ok else "FAIL         %s") % name)
        if not ok:
            fails.append(name)

    work = Path(tempfile.mkdtemp(prefix="hitl-selftest-"))
    try:
        _cases(work, refuses, accepts)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print("\n%d failure(s)" % len(fails))
    return 1 if fails else 0


def _cases(work: Path, refuses, accepts) -> None:
    T, S, A = 1_900_000_000, secrets.token_bytes(32), ("owner",)
    act = {"verb": "create_record", "target": "folder/REF-1", "fields": {"amount": 120}}
    plan = {"action": act, "business_key": {"client_ref": "REF-1", "party": "Party A"}}
    st = Store(work / "state.json")
    state = lambda i: st.read()["items"][i]["status"]  # noqa: E731
    calls = {"n": 0}

    def create_ok(a, d):
        calls["n"] += 1
        return {"id": "R-%d" % calls["n"]}

    # --- plan / propose
    for n, p in [("plan None", None), ("plan {}", {}), ("plan without action", {"business_key": {"k": "v"}}),
                 ("action verb empty", {"action": {"verb": "", "target": "x"}, "business_key": {"k": "v"}}),
                 ("business_key empty", {"action": act, "business_key": {}}),
                 ("business_key value null", {"action": act, "business_key": {"k": None}}),
                 ("business_key value bool", {"action": act, "business_key": {"k": True}}),
                 ("unknowns not a list", dict(plan, unknowns="date"))]:
        refuses("propose: " + n, lambda p=p: propose(st, "x1", p, "approval", now=T))
    refuses("propose: unknown regime", lambda: propose(st, "x1", plan, "auto", now=T))
    refuses("propose: draft_only carrying a non-draft verb", lambda: propose(st, "x1", plan, "draft_only", now=T))
    refuses("propose: now as str", lambda: propose(st, "x1", plan, "approval", now="1"))
    accepts("propose i1", lambda: propose(st, "i1", plan, "approval", now=T) or state("i1"),
            lambda s: s == "proposed")
    refuses("propose: same item twice", lambda: propose(st, "i1", plan, "approval", now=T))

    # --- request / decision
    refuses("request: gates empty", lambda: open_request(st, "i1", plan, [], now=T))
    refuses("request: gates None", lambda: open_request(st, "i1", plan, None, now=T))
    refuses("request: gate not snake_case", lambda: open_request(st, "i1", plan, ["Need OK!"], now=T))
    refuses("request: ttl as str", lambda: open_request(st, "i1", plan, ["new_record_review"], ttl_s="60", now=T))
    refuses("apply before any approval", lambda: guarded_apply(st, "i1", plan, act, create_ok, now=T))
    old = open_request(st, "i1", plan, ["new_record_review"], ttl_s=3600, now=T)
    nonce = open_request(st, "i1", plan, ["new_record_review"], ttl_s=3600, now=T)  # supersedes
    fp = fingerprint(plan)
    tok = lambda n=nonce, f=fp, a="owner", dec="approve", t=T, i="i1": sign_decision(S, i, n, f, a, dec, now=t)  # noqa: E731
    dec = lambda k, p=plan, s=S, ap=A, t=T + 5: decide(st, "i1", k, s, p, ap, now=t)  # noqa: E731
    for n, k in [("None", None), ("empty", ""), ("free text 'OK'", "OK"), ("free text 'NO GO 42'", "NO GO 42"),
                 ("int", 42)]:
        refuses("decide: token " + n, lambda k=k: dec(k))
    good = tok()
    refuses("decide: tampered token", lambda: dec(good[:-1] + ("0" if good[-1] != "0" else "1")))
    refuses("decide: wrong secret", lambda: dec(good, s=secrets.token_bytes(32)))
    refuses("decide: secret None", lambda: dec(good, s=None))
    refuses("decide: secret too short", lambda: dec(good, s=b"short"))
    refuses("decide: empty approver allowlist", lambda: dec(good, ap=()))
    refuses("decide: approver not allowed", lambda: dec(tok(a="intern")))
    refuses("decide: token of the superseded request", lambda: dec(tok(n=old)))
    refuses("decide: token for another item", lambda: dec(tok(i="i2")))
    refuses("decide: plan edited after the OK was signed", lambda: dec(good, p=dict(plan, note="x")))
    refuses("decide: token signed over another fingerprint", lambda: dec(tok(f="0" * 64)))
    refuses("decide: token issued 61s in the future", lambda: dec(tok(t=T + 5 + 61)))
    refuses("decide: token already expired", lambda: dec(tok(t=T - 2000)))
    raw = {"v": 1, "rid": "i1", "fp": fp, "nonce": nonce, "approver": "owner", "decision": "approve",
           "iat": str(T), "exp": T + 900}

    def forge(body):
        r = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(r).decode().rstrip("=") + "." + hmac.new(S, r, hashlib.sha256).hexdigest()
    refuses("decide: iat as string", lambda: dec(forge(raw)))
    refuses("decide: extra claim", lambda: dec(forge(dict(raw, iat=T, scope="all"))))
    refuses("decide: decision 'maybe'", lambda: dec(forge(dict(raw, iat=T, decision="maybe"))))
    accepts("decide: iat 50s ahead is within clock tolerance", lambda: dec(tok(t=T + 55)),
            lambda r: r == "approved")
    refuses("decide: replay of the same token", lambda: dec(tok(t=T + 55)))

    # --- exact action, never the adjacent
    refuses("apply: other verb", lambda: begin_apply(st, "i1", plan, dict(act, verb="delete_record"), now=T + 10))
    refuses("apply: other target", lambda: begin_apply(st, "i1", plan, dict(act, target="folder/REF-2"), now=T + 10))
    refuses("apply: extra field 'while I'm here'", lambda: begin_apply(
        st, "i1", plan, dict(act, fields={"amount": 120, "status": "closed"}), now=T + 10))
    refuses("apply: action None", lambda: begin_apply(st, "i1", plan, None, now=T + 10))
    refuses("apply: plan edited after approval", lambda: begin_apply(
        st, "i1", dict(plan, action=dict(act, fields={"amount": 999})), dict(act, fields={"amount": 999}), now=T + 10))
    accepts("apply: exact action -> applied with API id",
            lambda: guarded_apply(st, "i1", plan, act, create_ok, now=T + 10), lambda r: r["status"] == "applied")
    refuses("apply: applied item cannot run twice", lambda: guarded_apply(st, "i1", plan, act, create_ok, now=T + 11))
    refuses("request: reopen an applied item", lambda: open_request(st, "i1", plan, ["again"], now=T + 11))

    # --- expiry
    propose(st, "i2", dict(plan, business_key={"client_ref": "REF-2"}), "approval", now=T)
    p2 = dict(plan, business_key={"client_ref": "REF-2"})
    n2 = open_request(st, "i2", p2, ["new_record_review"], ttl_s=600, now=T)
    accepts("sweep: request past its ttl -> expired", lambda: sweep_expired(st, now=T + 601),
            lambda r: r == ["i2"] and state("i2") == "expired")
    refuses("decide: late valid token on an expired request", lambda: decide(
        st, "i2", sign_decision(S, "i2", n2, fingerprint(p2), "owner", "approve", now=T + 602), S, p2, A, now=T + 602))
    n2 = open_request(st, "i2", p2, ["new_record_review"], ttl_s=600, now=T + 700)
    refuses("decide: request expired at decision time (no sweep)", lambda: decide(
        st, "i2", sign_decision(S, "i2", n2, fingerprint(p2), "owner", "approve", now=T + 1300), S, p2, A, now=T + 1300))
    accepts("...and the item is now marked expired", lambda: state("i2"), lambda s: s == "expired")
    n2 = open_request(st, "i2", p2, ["new_record_review"], ttl_s=600, now=T + 2000)
    decide(st, "i2", sign_decision(S, "i2", n2, fingerprint(p2), "owner", "approve", ttl_s=300, now=T + 2000),
           S, p2, A, now=T + 2001)
    accepts("apply: approval gone stale -> waiting_human approval_stale, no call",
            lambda: guarded_apply(st, "i2", p2, act, create_ok, now=T + 2400),
            lambda r: r["gates"] == ["approval_stale"] and calls["n"] == 1)
    n2 = open_request(st, "i2", p2, ["new_record_review"], now=T + 2500)
    decide(st, "i2", sign_decision(S, "i2", n2, fingerprint(p2), "owner", "reject", now=T + 2500), S, p2, A, now=T + 2501)
    accepts("decide: explicit reject -> rejected", lambda: state("i2"), lambda s: s == "rejected")
    refuses("apply: rejected item", lambda: guarded_apply(st, "i2", p2, act, create_ok, now=T + 2502))

    # --- exit 0 is not proof; crash between create and record
    def approved(iid, p):
        propose(st, iid, p, "approval", now=T)
        n = open_request(st, iid, p, ["new_record_review"], now=T)
        decide(st, iid, sign_decision(S, iid, n, fingerprint(p), "owner", "approve", now=T), S, p, A, now=T + 1)
    for i, (n, resp) in enumerate([("None", None), ("{}", {}), ("exit_code 0, no id", {"exit_code": 0, "ok": True}),
                                   ("id empty", {"id": ""}), ("id null", {"id": None}), ("id True", {"id": True}),
                                   ("id 0", {"id": 0}), ("string 'ok'", "ok")]):
        iid, p = "u%d" % i, dict(plan, business_key={"client_ref": "U-%d" % i})
        approved(iid, p)
        accepts("result %s -> uncertain, never applied" % n,
                lambda iid=iid, p=p, resp=resp: guarded_apply(st, iid, p, act, lambda a, d: resp, now=T + 2),
                lambda r: r["status"] == "uncertain")
    pc = dict(plan, business_key={"client_ref": "C-1", "party": "Party C"})
    approved("c1", pc)
    begin_apply(st, "c1", pc, act, now=T + 2)          # crash here: created remotely, never recorded
    before = calls["n"]
    refuses("crash: rerun refuses to create again", lambda: guarded_apply(st, "c1", pc, act, create_ok, now=T + 3))
    accepts("crash: create() was not called on the rerun", lambda: calls["n"], lambda n: n == before)
    refuses("request: a new OK cannot restart an in-flight creation",
            lambda: open_request(st, "c1", pc, ["new_record_review"], now=T + 3))
    refuses("reconcile: lookup result None (lookup failed) is not 'absent'", lambda: reconcile(st, "c1", pc, None, now=T + 3))
    refuses("reconcile: lookup result a string", lambda: reconcile(st, "c1", pc, "[]", now=T + 3))
    refuses("reconcile: list of non-dicts", lambda: reconcile(st, "c1", pc, ["R-9"], now=T + 3))
    accepts("reconcile: one exact business-key match -> applied, id attached",
            lambda: reconcile(st, "c1", pc, [{"id": "R-77", "client_ref": " c-1 ", "party": "PARTY C"},
                                             {"id": "R-78", "client_ref": "C-2", "party": "Party C"}], now=T + 4),
            lambda s: s == "applied" and st.read()["items"]["c1"]["remote_id"] == "R-77")
    timeout = lambda a, d: (_ for _ in ()).throw(TimeoutError())  # noqa: E731
    pd = dict(plan, business_key={"client_ref": "D-1"})
    approved("d1", pd)
    accepts("timeout from the API -> uncertain", lambda: guarded_apply(st, "d1", pd, act, timeout, now=T + 2),
            lambda r: r["status"] == "uncertain")
    accepts("reconcile: two matches -> waiting_human possible_duplicate",
            lambda: (reconcile(st, "d1", pd, [{"id": "a", "client_ref": "D-1"}, {"id": "b", "client_ref": "d-1"}],
                               now=T + 3), st.read()["items"]["d1"]["gates"]),
            lambda r: r == ("waiting_human", ["possible_duplicate"]))
    pe = dict(plan, business_key={"client_ref": "E-1", "party": "Party E"})
    approved("e1", pe)
    guarded_apply(st, "e1", pe, act, timeout, now=T + 2)
    accepts("reconcile: candidate missing a key field counts as possible duplicate",
            lambda: reconcile(st, "e1", pe, [{"id": "x", "client_ref": "E-1"}], now=T + 3), lambda s: s == "waiting_human")
    pf = dict(plan, business_key={"client_ref": "F-1"})
    approved("f1", pf)
    guarded_apply(st, "f1", pf, act, timeout, now=T + 2)
    accepts("reconcile: proven absent -> approved for ONE bounded retry",
            lambda: reconcile(st, "f1", pf, [{"id": "z", "client_ref": "F-9"}], now=T + 3), lambda s: s == "approved")
    guarded_apply(st, "f1", pf, act, timeout, now=T + 4)
    accepts("reconcile: absent again after the retry -> waiting_human retry_exhausted",
            lambda: (reconcile(st, "f1", pf, [], now=T + 5), st.read()["items"]["f1"]["gates"]),
            lambda r: r == ("waiting_human", ["retry_exhausted"]))
    refuses("reconcile: nothing in flight", lambda: reconcile(st, "i1", plan, [], now=T + 5))

    # --- draft_only: the filter is the only barrier. Half the cases prove it does NOT over-block.
    dact = {"verb": "create_draft", "target": "thread-7"}
    dp = {"action": dact, "business_key": {"thread": "thread-7"}, "unknowns": ["hearing date"]}
    mk = "[TO COMPLETE: hearing date]"
    body = "Dear colleague,\nThe hearing is on %s.\nKind regards" % mk
    sig = [r"(?m)^--\s*$"]                       # caller rule: no pre-applied signature block
    dn = [0]

    def gate(b, target="thread-7", p=dp, a=dact, forbidden=sig):
        dn[0] += 1
        iid = "dr%d" % dn[0]
        propose(st, iid, p, "draft_only", now=T)
        return guarded_apply(st, iid, p, a, create_ok, draft={"target": target, "body": b},
                             forbidden=forbidden, now=T + 1)
    blocked = lambda r: r["status"] == "waiting_human" and r["gates"] == ["draft_filter"]  # noqa: E731
    created = lambda r: r["status"] == "applied"  # noqa: E731
    n0 = calls["n"]
    accepts("draft BLOCK: marker removed", lambda: gate(body.replace(mk, "12 May")), blocked)
    accepts("draft BLOCK: marker softened to prose", lambda: gate(body.replace(mk, "(date to be confirmed)")), blocked)
    accepts("draft BLOCK: marker only inside an HTML comment",
            lambda: gate("<p>The hearing is on TBC.</p><!-- %s -->" % mk), blocked)
    accepts("draft BLOCK: marker case changed", lambda: gate(body.replace(mk, mk.lower())), blocked)
    accepts("draft BLOCK: target mismatch", lambda: gate(body, target="thread-8"), blocked)
    accepts("draft BLOCK: unresolved {{placeholder}}", lambda: gate(body + "\n{{ client_name }}"), blocked)
    accepts("draft BLOCK: pre-applied signature block", lambda: gate(body + "\n--\nThe Partner"), blocked)
    accepts("draft BLOCK: empty body", lambda: gate("   \n"), blocked)
    accepts("draft BLOCK: nothing was created by the blocked drafts", lambda: calls["n"], lambda n: n == n0)
    refuses("draft REFUSE: draft body None", lambda: gate(None))
    refuses("draft REFUSE: forbidden rules None", lambda: gate(body, forbidden=None))
    refuses("draft REFUSE: a send action in draft_only", lambda: propose(
        st, "drs", dict(dp, action={"verb": "send_mail", "target": "thread-7"}), "draft_only", now=T))
    accepts("draft PASS: plain draft with its marker", lambda: gate(body), created)
    accepts("draft PASS: body says 'send', 'sent', 'signature'",
            lambda: gate(body + "\nPlease send the signed copy; we sent the signature page."), created)
    accepts("draft PASS: single braces and JSON in the body", lambda: gate(body + '\nRef {A-12} {"k": 1}'), created)
    accepts("draft PASS: marker inside HTML tags", lambda: gate("<p>Hearing: <b>%s</b></p>" % mk), created)
    accepts("draft PASS: accents and non-Latin text", lambda: gate(body + "\nÉchéance reçue, 期日"), created)
    accepts("draft PASS: dashes that are not a signature line", lambda: gate(body + "\n-- see below --\n---"), created)
    accepts("draft PASS: extra markers beyond the plan's unknowns",
            lambda: gate(body + "\n[TO COMPLETE: room number]"), created)
    accepts("draft PASS: an unrelated HTML comment next to a visible marker",
            lambda: gate("<!-- tracking -->\n<p>%s</p>" % mk), created)
    accepts("draft PASS: long body (20k chars)", lambda: gate(body + "\n" + "x" * 20000), created)
    accepts("draft PASS: empty forbidden list", lambda: gate(body, forbidden=[]), created)
    accepts("draft PASS: no unknowns, no marker needed",
            lambda: gate("All facts known.", p=dict(dp, unknowns=[])), created)
    accepts("draft PASS: update_draft verb", lambda: gate(body, p=dict(dp, action=dict(dact, verb="update_draft")),
                                                          a=dict(dact, verb="update_draft")), created)

    ap = dict(dp, business_key={"thread": "thread-9"}, action={"verb": "create_draft", "target": "thread-9"})
    approved("ha", ap)
    accepts("draft BLOCK: a human OK does not bypass the filter (approval regime, draft verb)",
            lambda: guarded_apply(st, "ha", ap, ap["action"], create_ok,
                                  draft={"target": "thread-9", "body": "No marker here."}, forbidden=[], now=T + 2),
            blocked)

    # --- run lock
    lk = work / "app.lock"
    accepts("lock: free -> acquired", lambda: acquire_lock(lk, "job-a", 900, None, now=T) or True)
    refuses("lock: live lock -> SKIP_LOCKED", lambda: acquire_lock(lk, "job-b", 900, False, now=T + 10), SkipLocked)
    for n, running in [("True", True), ("None (unknown)", None), ("'false' string", "false"), ("0", 0)]:
        refuses("lock: expired + app_running %s -> alert, not overwritten" % n,
                lambda r=running: acquire_lock(lk, "job-b", 900, r, now=T + 1000))
    accepts("lock: expired + app proven stopped -> taken over",
            lambda: acquire_lock(lk, "job-b", 900, False, now=T + 1000) or json.loads(lk.read_text())["job_id"],
            lambda j: j == "job-b")
    refuses("lock: release by another job", lambda: release_lock(lk, "job-a"))
    accepts("lock: release by owner", lambda: release_lock(lk, "job-b") or lk.read_text(), lambda s: s == "")
    refuses("lock: ttl 0", lambda: acquire_lock(lk, "job-c", 0, None, now=T))
    bad = work / "bad.lock"
    bad.write_text("{not json")
    refuses("lock: corrupt lock file", lambda: acquire_lock(bad, "job-c", 900, False, now=T))
    link = work / "link.lock"
    link.symlink_to(work / "elsewhere.lock")
    refuses("lock: lock path is a symlink", lambda: acquire_lock(link, "job-c", 900, False, now=T))

    # --- state store
    cs = work / "corrupt.json"
    cs.write_text('{"v": 1, "items": {"k": {"status": "done"}}}')
    refuses("store: unknown status in state", lambda: Store(cs).read())
    cs.write_text("")
    refuses("store: empty state file", lambda: Store(cs).read())
    sl = work / "sl.json"
    sl.symlink_to(work / "state.json")
    refuses("store: state file is a symlink", lambda: Store(sl).read())
    refuses("store: path None", lambda: Store(None))
    accepts("store: holds no plan content", lambda: (work / "state.json").read_text(),
            lambda s: "Party A" not in s and "folder/REF-1" not in s and nonce not in s)


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(_selftest())
    if len(sys.argv) == 3 and sys.argv[1] == "status":
        sys.exit(status(sys.argv[2]))
    print(__doc__)
