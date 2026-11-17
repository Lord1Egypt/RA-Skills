#!/usr/bin/env python3
"""investor-search memory store: the only way this skill writes its files.

Append-only. Existing rows are never removed or renumbered; ids continue from the
highest one on disk; a firm already held (same domain, or same key with no domain) is
skipped and reported. Standard library only.

  python3 store.py init    --root ROOT --market M --scope "..." [--budget N]
  python3 store.py status  --root ROOT --market M
  python3 store.py finish  --root ROOT --market M [--early user | --early "blocker: ..."]  (exit 4 = keep searching)
  python3 store.py deliver --root ROOT --market M --out DIR     (ONE file for the user)
  python3 store.py add     --root ROOT --market M  < batch.json
  python3 store.py export  --root ROOT --market M --out DIR     (tier B hand-over)
  python3 store.py import  --root ROOT --market M --from DIR|FILE.xlsx  (what the user uploaded)

ROOT is investor-search, or investor-search/@<space> in a shared workspace. Relative
paths resolve against the current directory (the agent's working directory).

batch.json (every key optional):
  {"investors": [{"ref": "a", "name": ..., "website": ..., <investors.csv columns>}],
   "sources":   [{"ref": "a", "field": "website", "rung": 1, "url": ...}],
   "pending":   [{"name": ..., "reason": ..., "note": ..., "source_url": ...}],
   "rejected":  [{"name": ..., "reason": ..., "evidence": ..., "source_url": ..., "website": ...}],
   "round":     {"query": ..., "surface": ..., "offered": 3, "survived": 1, "fetch_failed": false}}

A run ends only when `finish` allows it: six consecutive rounds with no new firm (the
dry streak) across at least three surfaces, none resting on a failed fetch, and an empty
pending queue - or the user's budget, if they named one - or the 60-round backstop.
A source's "ref" names an investor in the same batch, or an existing id ("f-004").
"""
import argparse
import contextlib
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

INVESTOR_COLS = ["id", "name", "type", "investor_evidence", "matches_request", "website",
                 "headquarters", "headquarters_partial", "person", "role", "people_known",
                 "linkedin", "sectors", "fold_conflict", "formerly", "type_blanked_reason",
                 "part_of", "sovereign_parent", "key_quote", "key_quote_url", "checked",
                 "provenance"]
FILES = {
    "investors.csv": INVESTOR_COLS,
    "sources.csv": ["id", "field", "rung", "url"],
    "investors-pending.csv": ["name", "reason", "note", "first_seen", "source_url"],
    "investors-rejected.csv": ["name", "reason", "evidence", "checked", "source_url"],
    "rounds.csv": ["round", "query", "surface", "offered", "survived", "dry_streak", "fetch_failed",
                   "at", "proof", "seen", "seen_notes"],
}
BOM_FILES = {"investors.csv"}
LEGAL = {"gmbh", "ag", "kg", "og", "mbh", "co", "ltd", "llc", "inc", "sa", "sarl", "bv", "nv",
         "as", "oy", "ab", "ou", "sia", "uab", "spa", "srl", "sro", "plc", "lp", "llp", "se",
         "privatstiftung", "stiftung", "holding", "group", "the"}
TODAY = dt.date.today().isoformat()
DRY_ROUNDS = 6
MIN_SEEN_NEW = 3          # a dry round must list this many new result URLs, each with a note
MIN_SURFACES = 3
BACKSTOP = 60


TERMINAL_PENDING = {"outOfCountry", "outOfScopeSovereign", "namedFamilyNotFirm", "individualNotFirm",
                    "hqNotPublished"}
ACTIVE_MINUTES = 15
ADVISER_HINTS = ("advisory", "advisor", "adviser", "consulting", "consultancy", "multi family office",
                 "multi-family office", "wealth management", "our clients", "for clients",
                 "catering to", "serves families", "services for families")
PLACEHOLDERS = {"—", "–", "-", "n/a", "na", "none", "null", "not found", "not available"}


def unproven(r):
    """No evidencing quote, or the firm's page was never read: Job 0 has not run on this row."""
    return not str(r.get("key_quote") or "").strip() or "not fetched" in str(r.get("provenance") or "").lower()


FO_WORDS = ("family office", "family-office", "familyoffice", "familienbüro", "familienbuero",
            "single family", "single-family", "familien-office", "family investment office")
OWN_CAPITAL = ("private investment office", "own capital", "own money", "family capital", "family wealth",
               "eigene kapital", "eigenes kapital", "eigene vermögen", "eigenes vermögen", "privates kapital",
               "private capital of the family", "familienvermögen")


def fo_proof(r):
    """'' unless type is family_office; 'proven' when the quote (minus the firm's own name) says
    family office; 'likely' when only the name or a register entry says so."""
    if r.get("type") != "family_office":
        return ""
    full = str(r.get("key_quote") or "").lower()
    own_site = bool(r.get("website")) and domain(r.get("key_quote_url")) == domain(r.get("website"))
    if own_site and any(w in full for w in FO_WORDS + OWN_CAPITAL):
        return "proven"          # the firm describes itself on its own website
    quote = full
    for part in (str(r.get("name") or "").lower(), str(r.get("formerly") or "").lower()):
        if part:
            quote = quote.replace(part, " ")
    return "proven" if any(w in quote for w in FO_WORDS + OWN_CAPITAL) else "likely"


def fo_counts(inv):
    likely = [r["name"] for r in inv if fo_proof(r) == "likely"]
    proven = sum(1 for r in inv if fo_proof(r) == "proven")
    return {"proven": proven, "likely_name_or_register_only": len(likely), "likely_names": likely,
            "report_rule": "Report these as two numbers. Never add likely family offices to the proven count."}


def fold(name):
    s = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    words = [w for w in re.split(r"[^a-z0-9]+", s) if w]
    while words and words[-1] in LEGAL:
        words.pop()
    while words and words[0] in LEGAL:
        words.pop(0)
    return " ".join(words)


def domain(url):
    d = (url or "").strip().lower()
    d = re.sub(r"^[a-z]+://", "", d).split("/")[0].split("?")[0]
    return d[4:] if d.startswith("www.") else d


@contextlib.contextmanager
def locked(folder, wait=60.0):
    """Portable exclusive lock: a lock file created with O_EXCL; a stale one (>10 min) is taken over."""
    import time
    folder.mkdir(parents=True, exist_ok=True)
    lock = folder / ".lock"
    deadline = time.time() + wait
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            with contextlib.suppress(OSError):
                if time.time() - lock.stat().st_mtime > 600:
                    lock.unlink()
                    continue
            if time.time() > deadline:
                sys.exit("another run is writing this market; try again")
            time.sleep(0.2)
    try:
        yield
    finally:
        with contextlib.suppress(OSError):
            lock.unlink()


def read_rows(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_rows(path, cols, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in cols})
    data = buf.getvalue()
    enc = "utf-8-sig" if path.name in BOM_FILES else "utf-8"
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
    with os.fdopen(fd, "w", encoding=enc, newline="") as fh:
        fh.write(data)
    os.replace(tmp, path)


def market_dir(root, market):
    m = re.sub(r"[^a-z0-9-]+", "-", market.strip().lower()).strip("-")
    if not m:
        sys.exit("market name is empty")
    return Path(root) / m, m


def scope_of(folder):
    led = folder / "ledger.txt"
    if led.exists():
        for line in led.read_text(encoding="utf-8").splitlines():
            if line.startswith("#SCOPE "):
                return line[7:]
    return ""


def uploaded_ledger(folder):
    """(key, domain) pairs from ledgers the user brought back; they stop duplicates only."""
    out = set()
    for p in sorted(folder.glob("ledger-uploaded*.txt")):
        for line in p.read_text(encoding="utf-8-sig").splitlines():
            parts = line.split("|")
            if line.startswith(("#", "key|")) or not line.strip():
                continue
            if len(parts) == 4:
                out.add((parts[0].strip(), parts[2].strip()))
            else:  # a malformed row must not be dropped in silence: it means a duplicate later
                msg = f"ledger line skipped ({len(parts)} fields, expected 4): {line[:90]}"
                LEDGER_WARNINGS.append(msg)
                sys.stderr.write(msg + "\n")
    return out


# --- ledger: a "|" inside a name broke the row into 5 fields, so a later run read the
# --- wrong domain and the firm came back as a duplicate. Found in a real Austria run:
# --- "fresh minds|FRESH|MINDS Holding GmbH|freshminds-holding.at|ok"
LEDGER_WARNINGS = []


def led_cell(v):
    """One ledger field: never contains the separator, never a newline."""
    return str(v or "").replace("|", "/").replace("\n", " ").replace("\r", " ").strip()


def uploaded_ledger_rows(folder):
    """(key, name, domain, status) from ledgers the user brought back.
    Without these, a rejected firm is forgotten on the run after next: run 2 skips it from the
    uploaded file, but the ledger run 2 writes does not carry it, so run 3 adds it as a new firm."""
    out = {}
    for p in sorted(folder.glob("ledger-uploaded*.txt")):
        try:
            text = p.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        for line in text.splitlines():
            if line.startswith(("#", "key|")) or not line.strip():
                continue
            parts = line.split("|")
            if len(parts) == 4:
                k = parts[0].strip()
                if k:
                    out[k] = (k, parts[1].strip(), parts[2].strip(), parts[3].strip())
    return out


def rebuild(root, folder, market, scope):
    inv = read_rows(folder / "investors.csv")
    pen = read_rows(folder / "investors-pending.csv")
    rej = read_rows(folder / "investors-rejected.csv")
    lines = [f"#LEDGER v2 market={market} date={TODAY}", f"#SCOPE {scope}", "key|name|domain|status"]
    for r in inv:
        lines.append(f"{led_cell(fold(r['name']))}|{led_cell(r['name'])}|{led_cell(domain(r.get('website')))}|ok")
    for r in pen:
        lines.append(f"{led_cell(fold(r['name']))}|{led_cell(r['name'])}||pending")
    for r in rej:  # names of rejected firms never travel
        lines.append(f"{led_cell(fold(r['name']))}|—|{led_cell(domain(r.get('source_url')))}|rejected")
    # carry forward what an uploaded ledger already decided, so tier B does not forget it
    have = {l.split("|")[0] for l in lines[3:]}
    for k, (key, nm, dom, st) in sorted(uploaded_ledger_rows(folder).items()):
        if k not in have and st in ("rejected", "pending", "ok"):
            lines.append(f"{led_cell(key)}|{led_cell(nm)}|{led_cell(dom)}|{st}")
    lines.append(f"#END rows={len(lines) - 3}")
    (folder / "ledger.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # index.md: one row per market of THIS root only
    idx = Path(root) / "index.md"
    rows = {}
    if idx.exists():
        for line in idx.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 5 and cells[0] not in ("market", "") and not set(cells[0]) <= {"-"}:
                if (Path(root) / cells[0]).is_dir():
                    rows[cells[0]] = cells
    rows[market] = [market, scope, str(len(inv)), str(len(pen)), TODAY]
    out = ["# Investor search — markets held", "", "| market | scope | firms | pending | last run |",
           "|---|---|---|---|---|"] + ["| " + " | ".join(c) + " |" for c in rows.values()]
    idx.write_text("\n".join(out) + "\n", encoding="utf-8")


def run_state(folder):
    p = folder / ".run.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def gates(folder, pending, rounds, state):
    started = int(state.get("started_at_round", 0))
    this_run = len(rounds) - started
    # the streak must be earned in THIS run: a new run never inherits "finished"
    streak = rounds[-DRY_ROUNDS:] if this_run >= DRY_ROUNDS else []
    g = {
        "gate0_record_on_disk": bool(rounds),
        "gate1_pending_empty": pending == 0,
        "gate2_dry_streak": bool(streak) and (int(rounds[-1]["dry_streak"]) if rounds else 0) >= DRY_ROUNDS,
        "gate2_surfaces_in_streak": len({r.get("surface", "") for r in streak}) >= MIN_SURFACES,
        "gate2_streak_proven": bool(streak) and not any(
            str(r.get("proof", "")) == "missing" for r in streak),
        "gate3_no_failed_fetch_in_streak": bool(streak) and not any(
            str(r.get("fetch_failed", "")).lower() in ("true", "1", "yes") for r in streak),
    }
    budget = state.get("budget")
    limit = min(int(budget), BACKSTOP) if budget else BACKSTOP
    if budget and int(budget) > BACKSTOP and state.get("user_raised_backstop"):
        limit = int(budget)
    if all(g.values()):
        reason, allowed = "EXHAUSTED on the surfaces named", True
    elif this_run >= limit:
        reason = "STOPPED ON BUDGET" if budget else "STOPPED ON THE 60-ROUND BACKSTOP"
        allowed = True
    else:
        missing = [k for k, v in g.items() if not v]
        reason, allowed = "keep searching: " + ", ".join(missing), False
    return {"gates": g, "rounds_this_run": this_run, "round_limit": limit,
            "budget_set_by_user": bool(budget), "stop_allowed": allowed, "stop_reason": reason}


def pace(rounds):
    """Median minutes between consecutive logged rounds (gaps over 2 hours are breaks)."""
    t = []
    for r in rounds:
        try:
            t.append(dt.datetime.strptime(r.get("at", ""), "%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            t.append(None)
    gaps = sorted((b - a).total_seconds() / 60 for a, b in zip(t, t[1:])
                  if a and b and 0 < (b - a).total_seconds() < 7200)
    return round(gaps[len(gaps) // 2], 1) if gaps else None


def status(folder, market):
    inv = read_rows(folder / "investors.csv")
    rounds = read_rows(folder / "rounds.csv")
    ids = [int(m.group(1)) for r in inv if (m := re.match(r"f-(\d+)$", r.get("id", "")))]
    checked = sorted(r["checked"] for r in inv if r.get("checked"))
    newest = checked[-1] if checked else ""
    age = (dt.date.today() - dt.date.fromisoformat(newest)).days if newest else None
    return {
        "market": market, "scope": scope_of(folder), "folder": str(folder.resolve()),
        "exists": (folder / "investors.csv").exists(),
        "firms": len(inv), "pending": len(read_rows(folder / "investors-pending.csv")),
        "rejected_count": len(read_rows(folder / "investors-rejected.csv")),
        "rounds": len(rounds), "dry_streak": int(rounds[-1]["dry_streak"]) if rounds else 0,
        # Gate 1 counts only pending rows that a search can still resolve; terminal reasons stay listed
        "pending_open": sum(1 for p in read_rows(folder / "investors-pending.csv")
                            if p.get("reason") not in TERMINAL_PENDING),
        **gates(folder, sum(1 for p in read_rows(folder / "investors-pending.csv")
                            if p.get("reason") not in TERMINAL_PENDING), rounds, run_state(folder)),
        "next_id": f"f-{(max(ids) + 1 if ids else 1):03d}",
        "minutes_per_round": pace(rounds),
        "empty_rounds_still_needed": max(0, DRY_ROUNDS - (int(rounds[-1]["dry_streak"]) if rounds else 0)),
        "newest_check": newest, "newest_check_age_days": age,
        "held_domains": sorted({domain(r.get("website")) for r in inv if r.get("website")}),
        "held_names": [r["name"] for r in inv],
        "pending_names": [r["name"] for r in read_rows(folder / "investors-pending.csv")],
        "excluded_domains": sorted(
            {domain(r.get("website")) for r in inv if r.get("website")}
            | {domain(r.get("source_url")) for r in read_rows(folder / "investors-rejected.csv") if r.get("source_url")}
            | {d for _, d in uploaded_ledger(folder) if d}),
    }


def cmd_init(a):
    folder, market = market_dir(a.root, a.market)
    if not scope_of(folder) and not a.scope:
        sys.exit("first run for this market: pass --scope")
    with locked(folder):
        created = []
        for name, cols in FILES.items():
            p = folder / name
            if not p.exists():
                write_rows(p, cols, [])
                created.append(name)
        scope = scope_of(folder) or (a.scope or "")
        if not scope:
            sys.exit("first run for this market: pass --scope")
        if a.scope and scope_of(folder) and a.scope.strip() != scope:
            print(json.dumps({"scope_mismatch": True, "on_file": scope, "asked": a.scope}))
            sys.exit(3)
        rebuild(a.root, folder, market, scope)
        prev = run_state(folder)
        resumed = bool(prev) and not prev.get("finished") and "started_at_round" in prev
        idle = None
        if resumed and prev.get("last_write"):
            try:
                idle = (dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(
                    prev["last_write"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)).total_seconds() / 60
            except ValueError:
                idle = None
        state = {"started_at_round": int(prev["started_at_round"]) if resumed
                 else len(read_rows(folder / "rounds.csv")),
                 "started": prev.get("started", TODAY) if resumed else TODAY,
                 "budget": a.budget or (prev.get("budget") if resumed else None),
                 "user_raised_backstop": bool(a.budget and a.budget > BACKSTOP)
                 or bool(resumed and prev.get("user_raised_backstop")),
                 "finished": False, "last_write": prev.get("last_write", "") if resumed else ""}
        (folder / ".run.json").write_text(json.dumps(state), encoding="utf-8")
        st = status(folder, market)
        if idle is not None and idle < ACTIVE_MINUTES:
            st["active_run_warning"] = (
                f"this market was written {idle:.0f} min ago by a run that has not finished. If THIS "
                "conversation started it, carry on. Otherwise another conversation is running it: "
                "do not search in parallel - tell the user and stop.")
        st["created"] = created
        st["first_run"] = len(created) == len(FILES)
        # read-back proof
        st["write_test"] = "ok" if (Path(a.root) / "index.md").read_text(encoding="utf-8").count(f"| {market} |") == 1 else "failed"
        print(json.dumps(st, ensure_ascii=False, indent=1))


def cmd_status(a):
    folder, market = market_dir(a.root, a.market)
    print(json.dumps(status(folder, market), ensure_ascii=False, indent=1))


def cmd_add(a):
    folder, market = market_dir(a.root, a.market)
    batch = json.load(sys.stdin)
    if not (folder / "investors.csv").exists():
        sys.exit("run init first")
    if ";" in str((batch.get("round") or {}).get("query", "")):
        print(json.dumps({"refused": "one round is ONE query on ONE surface - nothing was written; "
                                     "send each query as its own add"}))
        sys.exit(5)
    report = {"added": [], "already_held": [], "fold_conflicts": [], "pending_added": [],
              "pending_resolved": [], "rejected_added": 0, "sources_added": 0, "errors": []}
    with locked(folder):
        inv = read_rows(folder / "investors.csv")
        src = read_rows(folder / "sources.csv")
        pen = read_rows(folder / "investors-pending.csv")
        rej = read_rows(folder / "investors-rejected.csv")
        rnd = read_rows(folder / "rounds.csv")
        before = {k: len(v) for k, v in (("inv", inv), ("src", src), ("rej", rej), ("rnd", rnd))}
        for r in inv:  # a placeholder on file counts as blank; unclear evidence is never a match
            for c in INVESTOR_COLS[2:]:
                if str(r.get(c, "")).strip().lower() in PLACEHOLDERS:
                    r[c] = ""
            if r.get("matches_request") == "yes" and (r.get("investor_evidence") in ("", "unclear") or unproven(r)):
                r["matches_request"] = ""
        by_domain = {domain(r.get("website")): r["id"] for r in inv if r.get("website")}
        by_key = {fold(r["name"]): r for r in inv}
        rej_keys = {fold(r["name"]) for r in rej} | {domain(r.get("source_url")) for r in rej}
        upl = uploaded_ledger(folder)
        upl_keys, upl_domains = {k for k, _ in upl}, {d for _, d in upl if d}
        report["skipped_rejected_or_uploaded"] = []
        ids = [int(m.group(1)) for r in inv if (m := re.match(r"f-(\d+)$", r.get("id", "")))]
        nxt = max(ids) + 1 if ids else 1
        refmap = {r["id"]: r["id"] for r in inv}
        alias_keys = set()
        survived = 0
        for x in batch.get("rejected", []):
            k = fold(x.get("name"))
            if not k or k in {fold(r["name"]) for r in rej}:
                continue
            rej.append({"name": x["name"], "reason": x.get("reason", ""), "evidence": x.get("evidence", ""),
                        "checked": x.get("checked") or TODAY, "source_url": x.get("source_url") or x.get("website", "")})
            pen = [p for p in pen if fold(p["name"]) != k]
            report["rejected_added"] += 1
            rej_keys |= {k, domain(x.get("source_url") or x.get("website"))}
        for r in batch.get("investors", []):
            r = {c: ("" if c != "name" and isinstance(v, str) and v.strip().lower() in PLACEHOLDERS else v)
                 for c, v in r.items()}
            name = (r.get("name") or "").strip()
            if not name:
                report["errors"].append("investor without a name skipped")
                continue
            d, k = domain(r.get("website")), fold(name)
            held = by_domain.get(d) if d else None
            if held is None and not d and k in by_key:
                held = by_key[k]["id"]
            if not held and ((d and (d in rej_keys or d in upl_domains)) or (not d and (k in rej_keys or k in upl_keys))):
                report["skipped_rejected_or_uploaded"].append(
                    "(a rejected firm)" if (k in rej_keys or d in rej_keys) else name)
                continue
            if held:
                report["already_held"].append(f"{name} = {held}")
                alias_keys.add(k)  # an alias of a held firm clears its pending row
                existing = next(x for x in inv if x["id"] == held)
                for c in INVESTOR_COLS[1:]:  # enrich blanks only, never overwrite
                    if not existing.get(c) and r.get(c) not in (None, ""):
                        existing[c] = r[c]
                refmap[r.get("ref") or name] = held
                continue
            row = {c: r.get(c, "") for c in INVESTOR_COLS}
            text = " ".join(str(row.get(c, "")) for c in ("name", "key_quote", "sectors")).lower()
            if row.get("matches_request") == "yes" and any(h in text for h in ADVISER_HINTS):
                row["matches_request"] = ""
                report.setdefault("warnings", []).append(
                    f"{name}: reads like an adviser - matches_request left blank; run the Job 0 test")
            if row.get("investor_evidence") in ("", "unclear") and row.get("matches_request") == "yes":
                row["matches_request"] = ""
                report.setdefault("warnings", []).append(
                    f"{name}: matches_request left blank - investor evidence is unclear")
            if not str(row.get("matches_request") or "").strip():
                report.setdefault("warnings", []).append(
                    f"{name}: matches_request is blank - every row must be yes or no against the "
                    "population the user named")
            _nm = str(row.get("name") or "").lower()
            if (("stiftung" in _nm or "stichting" in _nm)
                    and str(row.get("investor_evidence") or "").strip() == "invests"
                    and str(row.get("type") or "").strip() in ("", "unknown")):
                report.setdefault("warnings", []).append(
                    f"{name}: a family foundation whose evidence says it invests is a family_office "
                    "(likely at least), not 'unknown'")
            if fo_proof(row) == "likely":
                report.setdefault("warnings", []).append(
                    f"{name}: family_office rests on the name or a register entry only - counted as 'likely', "
                    "not as a proven family office; look for a page that says it")
            if row.get("matches_request") == "yes" and unproven(row):
                row["matches_request"] = ""
                report.setdefault("warnings", []).append(
                    f"{name}: matches_request left blank - no key_quote, or the source was not fetched")
            if k in by_key and d:
                row["fold_conflict"] = row.get("fold_conflict") or by_key[k]["name"]
                report["fold_conflicts"].append(f"{name} vs {by_key[k]['name']}")
            if d:
                row["website"] = d
            keep = batch.get("_keep_ids") and re.match(r"f-\d+$", r.get("id") or "") \
                and r["id"] not in {x["id"] for x in inv}
            if keep:
                row["id"] = r["id"]
                nxt = max(nxt, int(r["id"][2:]) + 1)
            else:
                row["id"] = f"f-{nxt:03d}"
                nxt += 1
            row["checked"] = row.get("checked") or TODAY
            inv.append(row)
            survived += 1
            refmap[r.get("ref") or name] = row["id"]
            if d:
                by_domain[d] = row["id"]
            by_key[k] = row
            report["added"].append(f"{row['id']} {name}")
        for s in batch.get("sources", []):
            rid = refmap.get(s.get("ref")) or refmap.get(s.get("id"))
            if not rid or not s.get("url"):
                report["errors"].append(f"source without a known ref or url: {s}")
                continue
            key = (rid, s.get("field", ""), s.get("url"))
            if any((x["id"], x["field"], x["url"]) == key for x in src):
                continue
            src.append({"id": rid, "field": s.get("field", ""), "rung": s.get("rung", ""), "url": s["url"]})
            report["sources_added"] += 1
        held_keys = set(by_key) | alias_keys
        report["pending_resolved"] = [p["name"] for p in pen if fold(p["name"]) in held_keys]
        pen = [p for p in pen if fold(p["name"]) not in held_keys]
        for p in batch.get("pending", []):
            k = fold(p.get("name"))
            if not k or k in held_keys or k in rej_keys:
                continue
            same = next((x for x in pen if fold(x["name"]) == k), None)
            if same is not None:  # a re-check may move a row to a new reason, with a note saying what was searched
                new_reason = p.get("reason", "")
                if new_reason and new_reason != same["reason"]:
                    if new_reason == "hqNotPublished" and not (p.get("note") or "").strip():
                        report["errors"].append(f"{p['name']}: hqNotPublished needs a note naming what was searched")
                        continue
                    same.update({"reason": new_reason, "note": p.get("note") or same["note"],
                                 "source_url": p.get("source_url") or same["source_url"]})
                    report.setdefault("pending_updated", []).append(f"{p['name']} -> {new_reason}")
                continue
            pen.append({"name": p["name"], "reason": p.get("reason", ""), "note": p.get("note", ""),
                        "first_seen": p.get("first_seen") or TODAY, "source_url": p.get("source_url", "")})
            report["pending_added"].append(p["name"])
        if batch.get("round"):
            r = batch["round"]
            n = len(rnd) + 1
            prev = int(rnd[-1]["dry_streak"]) if rnd else 0
            surv = survived if r.get("survived") in (None, "") else int(r["survived"])
            raw = r.get("seen") or []
            if isinstance(raw, str):
                raw = [x for x in raw.split("\n")] if "\n" in raw else raw.split()
            seen, notes = [], {}
            for x in raw:
                if isinstance(x, dict):
                    u, note = str(x.get("url", "")).strip(), str(x.get("note", "")).strip()
                else:
                    u, _, note = str(x).partition("|")
                    u, note = u.strip(), note.strip()
                    if " " in u:
                        u, _, more = u.partition(" ")
                        note = (more.strip() + " " + note).strip()
                if u.startswith("http"):
                    seen.append(u)
                    notes.setdefault(u, note)
            earlier = {u for row in rnd for u in str(row.get("seen") or "").split()}
            fresh = [u for u in dict.fromkeys(seen) if u not in earlier]
            noted = [u for u in fresh if len(notes.get(u, "")) >= 3]
            surface = r.get("surface", "")
            site = re.search(r"site:([A-Za-z0-9.-]+)", str(r.get("query", "")))
            if site and not surv and fresh:
                dom = site.group(1).lower().lstrip(".")
                domain_of = lambda u: re.sub(r"^https?://", "", u).split("/")[0].split(":")[0].lower()
                if not any(domain_of(u) == dom or domain_of(u).endswith("." + dom) for u in fresh):
                    report.setdefault("warnings", []).append(
                        f"round {n}: the query says site:{dom} but no URL in 'seen' is on {dom} - "
                        f"that surface was not searched, so this round counts as 'open web'. "
                        f"Search {dom} another way (fetch its search or list page) to count it.")
                    surface = "open web"
            proof = "ok" if surv or r.get("fetch_failed") or len(noted) >= MIN_SEEN_NEW else "missing"
            if proof == "missing":
                report.setdefault("warnings", []).append(
                    f"round {n} does not count as dry: a dry round needs 'seen' with at least "
                    f"{MIN_SEEN_NEW} result URLs the search returned that no earlier round listed, "
                    f"each with a note saying what it is and why it is not a new investor "
                    f"(got {len(noted)}). A URL that may name a new investor goes to 'add' or "
                    f"'pending', and then the round is not dry.")
            rnd.append({"round": n, "query": r.get("query", ""), "surface": surface,
                        "offered": r.get("offered", ""), "survived": surv,
                        "fetch_failed": "true" if r.get("fetch_failed") else "",
                        "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "proof": proof, "seen": " ".join(seen),
                        "seen_notes": " || ".join(f"{u} | {notes.get(u, '')}" for u in dict.fromkeys(seen)),
                        "dry_streak": 0 if surv else (prev + 1 if proof == "ok" else prev)})
            report["round"] = n
            report["dry_streak"] = rnd[-1]["dry_streak"]
        # guard: nothing on disk may shrink
        after = {"inv": len(inv), "src": len(src), "rej": len(rej), "rnd": len(rnd)}
        if any(after[k] < before[k] for k in before):
            sys.exit(f"refused: a write would remove rows {before} -> {after}")
        write_rows(folder / "investors.csv", INVESTOR_COLS, inv)
        write_rows(folder / "sources.csv", FILES["sources.csv"], src)
        write_rows(folder / "investors-pending.csv", FILES["investors-pending.csv"], pen)
        write_rows(folder / "investors-rejected.csv", FILES["investors-rejected.csv"], rej)
        write_rows(folder / "rounds.csv", FILES["rounds.csv"], rnd)
        state = run_state(folder)
        if state:
            state["last_write"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            (folder / ".run.json").write_text(json.dumps(state), encoding="utf-8")
        rebuild(a.root, folder, market, scope_of(folder))
        st = status(folder, market)
        if LEDGER_WARNINGS:
            report.setdefault("warnings", []).extend(LEDGER_WARNINGS)
        report["family_offices"] = fo_counts(inv)
        report.update({k: st[k] for k in ("firms", "pending", "rejected_count", "rounds", "next_id",
                                          "rounds_this_run", "round_limit", "stop_allowed", "stop_reason")})
        print(json.dumps(report, ensure_ascii=False, indent=1))


def cmd_finish(a):
    folder, market = market_dir(a.root, a.market)
    st = status(folder, market)
    inv = read_rows(folder / "investors.csv")
    rounds = read_rows(folder / "rounds.csv")[int(run_state(folder).get("started_at_round", 0)):]
    if a.early and not (a.early == "user" or a.early.startswith("blocker:")):
        print(json.dumps({"refused": "--early takes 'user' (the user ended the run) or "
                                     "'blocker: <what failed>' (tools or model limit). A gate that "
                                     "is still closed is not a blocker - keep searching."}))
        sys.exit(2)
    if not st["stop_allowed"] and not a.early:
        print(json.dumps({"stop_allowed": False, "stop_reason": st["stop_reason"],
                          "dry_streak": st["dry_streak"], "rounds_this_run": st["rounds_this_run"],
                          "instruction": "Do not end the run. Search a surface not yet in rounds.csv, "
                                         "work the pending queue, and call add after each round."}, indent=1))
        sys.exit(4)
    reason = st["stop_reason"] if st["stop_allowed"] else f"STOPPED EARLY - {a.early}"
    def count(col):
        out = {}
        for r in inv:
            key = r.get(col) or "blank"
            out[key] = out.get(key, 0) + 1
        return dict(sorted(out.items()))
    report = {
        "headline": f"{market} - {st['firms']} firms over {len(rounds)} rounds this run ({st['rounds']} in total)",
        "why_stopped": reason,
        "complete": reason.startswith("EXHAUSTED"),
        "surfaces_tried": sorted({r["surface"] for r in rounds if r.get("surface")}),
        "offered_this_run": sum(int(r["offered"] or 0) for r in rounds),
        "kept_this_run": sum(int(r["survived"] or 0) for r in rounds),
        "pending": st["pending"], "rejected_count": st["rejected_count"],
        "type": count("type"), "evidence": count("investor_evidence"),
        "family_offices": fo_counts(inv),
        "matches_request": count("matches_request"),
        "flags": {
            "operating_group": [r["name"] for r in inv if r.get("investor_evidence") == "operating_group"],
            "fold_conflict": [r["name"] for r in inv if r.get("fold_conflict")],
            "no_website": [r["name"] for r in inv if not r.get("website")],
            "headquarters_partial": [r["name"] for r in inv if r.get("headquarters_partial") == "yes"],
            "no_person": [r["name"] for r in inv if not r.get("person")],
            "evidence_unclear": [r["name"] for r in inv if r.get("investor_evidence") in ("", "unclear")],
            "no_quote_or_not_fetched": [r["name"] for r in inv if unproven(r)],
            "stray_files_in_working_dir": sorted(f.name for f in Path.cwd().glob("*round*.json")),
        },
        "citations": len(read_rows(folder / "sources.csv")),
        "folder": st["folder"],
    }
    state = run_state(folder)
    state["finished"] = True
    (folder / ".run.json").write_text(json.dumps(state), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))


def _xlsx(path, sheets):
    """Minimal .xlsx writer (stdlib only): sheets = [(name, [header, *rows])]."""
    import zipfile
    from xml.sax.saxutils import escape

    def col(i):
        s = ""
        i += 1
        while i:
            i, r = divmod(i - 1, 26)
            s = chr(65 + r) + s
        return s

    def sheet_xml(rows):
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
               '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" state="frozen"/></sheetView></sheetViews>'
               '<sheetData>']
        for ri, row in enumerate(rows, 1):
            cells = []
            for ci, v in enumerate(row):
                v = "" if v is None else str(v)
                style = ' s="1"' if ri == 1 else ""
                cells.append(f'<c r="{col(ci)}{ri}" t="inlineStr"{style}><is><t xml:space="preserve">{escape(v)}</t></is></c>')
            out.append(f'<row r="{ri}">{"".join(cells)}</row>')
        out.append('</sheetData></worksheet>')
        return "".join(out)

    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                             for i in range(1, len(sheets) + 1)) + '</Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", f'<?xml version="1.0" encoding="UTF-8"?><workbook {ns}><sheets>'
                   + "".join(f'<sheet name="{escape(n[:31])}" sheetId="{i}" r:id="rId{i}"/>' for i, (n, _) in enumerate(sheets, 1))
                   + '</sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
                             for i in range(1, len(sheets) + 1))
                   + f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        z.writestr("xl/styles.xml", '<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                   '<fonts count="2"><font/><font><b/></font></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
                   '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
                   '<cellXfs count="2"><xf/><xf fontId="1" applyFont="1"/></cellXfs></styleSheet>')
        for i, (_, rows) in enumerate(sheets, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows))


def cmd_deliver(a):
    """ONE file for the user: <market>-investors.xlsx (Investors with their source links, and Sources)."""
    folder, market = market_dir(a.root, a.market)
    inv = read_rows(folder / "investors.csv")
    src = read_rows(folder / "sources.csv")
    links = {}
    for s in src:
        links.setdefault(s["id"], []).append(f"{s['field']}: {s['url']}")
    head = INVESTOR_COLS + ["family_office_proof", "source_links"]
    rows = [head] + [[r.get(c, "") for c in INVESTOR_COLS]
                     + [{"proven": "proven", "likely": "likely: name or register only"}.get(fo_proof(r), ""),
                        "\n".join(links.get(r["id"], []))] for r in inv]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{market}-investors.xlsx"
    def sheet(name):
        cols = FILES[name]
        return [cols] + [[r.get(c, "") for c in cols] for r in read_rows(folder / name)]
    # One file: what the user reads, and everything a later run needs to continue.
    # The rejected list is never in it.
    _xlsx(path, [("Investors", rows), ("Sources", sheet("sources.csv")),
                 ("Pending", sheet("investors-pending.csv")), ("Rounds", sheet("rounds.csv")),
                 ("Ledger", [["ledger"]] + [[line] for line in (folder / "ledger.txt").read_text(encoding="utf-8").splitlines()])])
    print(json.dumps({"file": str(path.resolve()), "firms": len(inv), "citations": len(src),
                      "family_offices": fo_counts(inv),
                      "send_with": {"tool": "send_file", "path": str(path.resolve())}}, indent=1))


def cmd_export(a):
    folder, market = market_dir(a.root, a.market)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    sent = []
    for name in ("investors.csv", "sources.csv", "investors-pending.csv", "rounds.csv", "ledger.txt"):
        p = folder / name
        if p.exists():
            (out / name).write_bytes(p.read_bytes())
            sent.append(str((out / name).resolve()))
    print(json.dumps({"files": sent, "never_exported": "investors-rejected.csv"}, indent=1))


def _read_xlsx(path):
    """Read the sheets written by _xlsx (inline strings) -> {sheet name: [dict rows]}."""
    import zipfile
    import xml.etree.ElementTree as ET
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    out = {}
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        for i, sh in enumerate(wb.find("m:sheets", ns), 1):
            root = ET.fromstring(z.read(f"xl/worksheets/sheet{i}.xml"))
            rows = []
            for row in root.iter(f"{{{ns['m']}}}row"):
                vals = {}
                for c in row:
                    ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                    idx = 0
                    for ch in ref:
                        idx = idx * 26 + ord(ch) - 64
                    vals[idx - 1] = "".join(x.text or "" for x in c.iter(f"{{{ns['m']}}}t"))
                rows.append([vals.get(k, "") for k in range(max(vals) + 1)] if vals else [])
            if rows:
                head = rows[0]
                out[sh.get("name")] = [dict(zip(head, r + [""] * (len(head) - len(r)))) for r in rows[1:]]
    return out


def cmd_import(a):
    folder, market = market_dir(a.root, a.market)
    src_dir = Path(getattr(a, "from"))
    if src_dir.is_file() and src_dir.suffix == ".txt":  # a ledger handed over on its own
        _t = Path(tempfile.mkdtemp())
        (_t / "ledger.txt").write_text(src_dir.read_text(encoding="utf-8-sig"), encoding="utf-8")
        src_dir = _t
    books = sorted(src_dir.glob("*.xlsx")) if src_dir.is_dir() else ([src_dir] if src_dir.suffix == ".xlsx" else [])
    if books:  # the single file this skill hands over: unpack it to CSVs, then import as usual
        tmp = Path(tempfile.mkdtemp())
        data = _read_xlsx(books[0])
        for sheet, name in (("Investors", "investors.csv"), ("Sources", "sources.csv"),
                            ("Pending", "investors-pending.csv"), ("Rounds", "rounds.csv")):
            if sheet in data:
                write_rows(tmp / name, FILES[name], data[sheet])
        if "Ledger" in data:  # carries rejected firms as key + domain, without names
            (tmp / "ledger.txt").write_text("\n".join(r["ledger"] for r in data["Ledger"]) + "\n", encoding="utf-8")
        src_dir = tmp
    if not (folder / "investors.csv").exists():
        sys.exit("run init first")
    done = []
    led = src_dir / "ledger.txt"
    if led.exists():
        n = len(list(folder.glob("ledger-uploaded*.txt")))
        (folder / f"ledger-uploaded-{n + 1}.txt").write_text(led.read_text(encoding="utf-8-sig"), encoding="utf-8")
        done.append("ledger.txt")
    inv = read_rows(src_dir / "investors.csv")
    if inv:
        srcs = read_rows(src_dir / "sources.csv")
        batch = {"investors": [dict(r, ref=r.get("id")) for r in inv],
                 "sources": [dict(s, ref=s.get("id")) for s in srcs],
                 "pending": read_rows(src_dir / "investors-pending.csv"),
                 "_keep_ids": not read_rows(folder / "investors.csv")}
        # uploaded ledger must not block the very rows it describes
        for p in folder.glob("ledger-uploaded*.txt"):
            p.rename(p.with_suffix(".hold"))
        sys.stdin = io.StringIO(json.dumps(batch))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_add(a)
        finally:
            for p in folder.glob("ledger-uploaded*.hold"):
                p.rename(p.with_suffix(".txt"))
        done += ["investors.csv", "sources.csv", "investors-pending.csv"]
    rnd = read_rows(src_dir / "rounds.csv")
    if rnd and not read_rows(folder / "rounds.csv"):
        write_rows(folder / "rounds.csv", FILES["rounds.csv"], rnd)
        done.append("rounds.csv")
        # imported rounds are history, not this run
        state = dict(run_state(folder), started_at_round=len(rnd), finished=False)
        (folder / ".run.json").write_text(json.dumps(state), encoding="utf-8")
    rebuild(a.root, folder, market, scope_of(folder))
    print(json.dumps({"imported": done, **status(folder, market)}, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "status", "add", "export", "import", "finish", "deliver"):
        p = sub.add_parser(name)
        p.add_argument("--root", required=True)
        p.add_argument("--market", required=True)
        if name == "init":
            p.add_argument("--scope", default="")
            p.add_argument("--budget", type=int, default=0,
                           help="only when the user named a number of rounds")
        if name == "finish":
            p.add_argument("--early", default="",
                           help="'user' (the user ended the run) or 'blocker: <what failed>'")
        if name == "deliver":
            p.add_argument("--out", required=True)
        if name == "export":
            p.add_argument("--out", required=True)
        if name == "import":
            p.add_argument("--from", required=True, help="a folder of files, or the .xlsx this skill delivered")
    a = ap.parse_args()
    {"init": cmd_init, "status": cmd_status, "add": cmd_add, "export": cmd_export,
     "import": cmd_import, "finish": cmd_finish, "deliver": cmd_deliver}[a.cmd](a)


if __name__ == "__main__":
    main()
