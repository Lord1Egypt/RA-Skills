#!/usr/bin/env python3
"""noteclaw notequery.py — analysis-layer query CLI (read-only, zero LLM cost)

Data source: manifest.json (authoritative metadata/timestamps) + store/ (md
snapshot, versioned by git).
Iron rule: never guess directories/file names; a page is located by manifest rel +
in-section order NNN (the store file name prefix).

Usage:
    notequery.py list [--section X]
    notequery.py since --since <YYYY-MM-DD> [--until <YYYY-MM-DD>] [--section X] [--kind all|new|edited]
    notequery.py grep --kw <keyword> [--section X] [--since D] [--until D] [--format json]
    notequery.py fetch --page <NNN> | "<title substring>" | "<section>/<NNN>"  [--section X]
    notequery.py week [--weeks-ago 0] [--full] [--max-pages N] [--max-bytes B]
    notequery.py diff --from REV [--to REV] [--section X] [--max-bytes B]  # content-level diff (side track)

Common options: by default only the metadata list is produced (zero tokens);
         --full appends the body text;
         --max-pages/--max-bytes = body budget gate (only the body is truncated,
         the list stays complete);
         --format json|md (md by default).

Window semantics: a page is in the window ⟺ createdDateTime∈W or
lastModifiedDateTime∈W; kind=new looks at creation only, kind=edited at
modification only. Graph times are UTC; the window is judged in the timezone from
NOTECLAW_TZ (default UTC), a date is a calendar day including both ends.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

# Working directory = the cwd the command was run from (NOTECLAW_HOME overrides).
NOTECLAW = os.environ.get("NOTECLAW_HOME") or os.getcwd()
MANIFEST = os.path.join(NOTECLAW, "manifest.json")
STORE_BASE = os.path.join(NOTECLAW, "store")
# After loading the manifest, narrow down to the <notebook> subdirectory
# (must match the naming used by graph_sync.py)
STORE = STORE_BASE
NB_SEG = ""          # store segment name of the current notebook (load_manifest fills it from the manifest notebook name)
try:
    from zoneinfo import ZoneInfo as _ZI
    TZ = _ZI(os.environ.get("NOTECLAW_TZ", "UTC"))
except ImportError:            # Python < 3.9: no zoneinfo module
    TZ = dt.timezone.utc
except Exception as e:         # unusable zone name, or tzdata missing
    print(f"⚠ NOTECLAW_TZ={os.environ.get('NOTECLAW_TZ', 'UTC')!r} is not a "
          f"usable timezone ({e}); query windows fall back to UTC",
          file=sys.stderr)
    TZ = dt.timezone.utc
DISPLAY_TITLE_MAX = 90


def _safe(name):
    """section/page/notebook name → safe directory name (same as sanitize in
    graph_sync.py)"""
    s = re.sub(r'[/\\:*?"<>|\x00-\x1f]', "_", name).strip()
    return s or "untitled"


def _git_store_path():
    """git paths are limited to this notebook's store segment"""
    return os.path.join("store", NB_SEG)


# ---------- basics ----------
def manifest_unusable_msg(why):
    """Single wording used when manifest.json exists but is unusable (the literal
    is kept identical across the three scripts)"""
    return (f"manifest.json is unusable ({why})\n"
            f"  → back it up, delete manifest.json and cold start again: graph_sync.py --all && html2md.py")


def load_manifest():
    if not os.path.exists(MANIFEST):
        raise RuntimeError("no manifest.json: run graph_sync.py cold start (--all) before querying")
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    if m.get("schema") != 3:
        raise RuntimeError(manifest_unusable_msg(f"schema={m.get('schema')}, needs 3"))
    if not isinstance(m.get("sections"), dict):
        raise RuntimeError(manifest_unusable_msg("sections missing, file is corrupt"))
    # store layout: <notebook>/<section>/NNN_<title>.md (same as graph_sync.py)
    global STORE, NB_SEG
    nb = m.get("notebook") or {}
    NB_SEG = _safe(nb.get("displayName") or "")
    STORE = os.path.join(STORE_BASE, NB_SEG)
    return m


def utc_to_local(iso):
    """'2024-02-26T13:49:11.231Z' → naive datetime in the NOTECLAW_TZ zone"""
    if not iso:
        return None
    try:
        aware = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    return aware.astimezone(TZ).replace(tzinfo=None)


def fmt_dt(dt_naive):
    return dt_naive.strftime("%Y-%m-%d %H:%M") if dt_naive else "—"


def display_title(t):
    t = t.replace("\xa0", " ").strip()
    return t if len(t) <= DISPLAY_TITLE_MAX else t[:DISPLAY_TITLE_MAX] + "…"


def page_path(rel, order):
    """real path of store/<notebook>/<rel>/NNN_*.md (the file name is sanitized and
    truncated, so look it back up with glob)"""
    hits = glob.glob(os.path.join(STORE, rel, f"{order:03d}_*.md"))
    return hits[0] if hits else None


def page_relpath(rel, order):
    """page → path relative to the data directory (for output; same path
    convention as diff / fetch)"""
    p = page_path(rel, order)
    return os.path.relpath(p, NOTECLAW) if p else None


def match_section(rel, sec_filter):
    return sec_filter is None or rel == sec_filter \
        or rel.startswith(sec_filter + os.sep)


def pick_sections(manifest, sec_filter):
    secs = [(rel, sec) for rel, sec in manifest["sections"].items()
            if match_section(rel, sec_filter)]
    if sec_filter is not None and not secs:
        avail = ", ".join(manifest["sections"].keys())
        sys.exit(f"section {sec_filter!r} matched nothing. available: {avail}")
    return secs


def iter_pages(manifest, sec_filter=None):
    """yield (rel, order, pageid, pmeta), in API order inside a section (manifest
    insertion order)"""
    for rel, sec in pick_sections(manifest, sec_filter):
        for order, (pid, pmeta) in enumerate(sec["pages"].items(), 1):
            yield rel, order, pid, pmeta


# ---------- window ----------
def parse_day(s):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        sys.exit(f"date format should be YYYY-MM-DD: {s!r}")


def window_bounds(since_s, until_s):
    """returns [start, end) local naive; dates include both ends"""
    since_d = parse_day(since_s) if since_s else dt.date(1970, 1, 1)
    until_d = parse_day(until_s) if until_s else dt.date.max
    if until_d < since_d:
        sys.exit(f"--until {until_d} is earlier than --since {since_d}")
    start = dt.datetime.combine(since_d, dt.time.min)
    if until_d == dt.date.max:
        end = dt.datetime.max
    else:
        end = dt.datetime.combine(until_d + dt.timedelta(days=1), dt.time.min)
    return start, end


def page_in_window(pmeta, start, end, kind):
    cr, lm = utc_to_local(pmeta.get("createdDateTime")), utc_to_local(pmeta.get("lastModifiedDateTime"))
    if kind == "new":
        return cr is not None and start <= cr < end
    if kind == "edited":
        return lm is not None and start <= lm < end
    return (cr is not None and start <= cr < end) or (lm is not None and start <= lm < end)


def this_week(weeks_ago):
    """from Monday 00:00 of this week; weeks_ago=0 → up to today, >0 → up to that
    week's Sunday"""
    today = dt.datetime.now(TZ).date()
    monday = today - dt.timedelta(days=today.weekday()) - dt.timedelta(weeks=weeks_ago)
    since_s = monday.isoformat()
    until_s = today.isoformat() if weeks_ago == 0 else (monday + dt.timedelta(days=6)).isoformat()
    return since_s, until_s


# ---------- output ----------
def hit_json(pages):
    clean = []
    for pg in pages:
        c = dict(pg)
        for k in ("created", "lastModified"):
            v = c.get(k)
            if isinstance(v, dt.datetime):
                c[k] = v.isoformat(sep=" ", timespec="seconds")
        clean.append(c)
    return json.dumps(clean, ensure_ascii=False, indent=1)


def read_md(rel, order):
    p = page_path(rel, order)
    if not p:
        return None, None
    with open(p, encoding="utf-8") as f:
        return f.read(), os.path.relpath(p, NOTECLAW)


def missing_bodies(pages):
    """number of pages present in the manifest but without an md file in store —
    the signal of an incomplete snapshot"""
    return sum(1 for pg in pages if page_path(pg["rel"], pg["order"]) is None)


def budget_bodies(pages, max_pages, max_bytes):
    """pre-read the body of every candidate page → truncate by
    --max-pages/--max-bytes (only the body is truncated)
    returns (note, [(pg, body, relp), ...]); body=None when the md file is
    missing."""
    bodies = []
    for pg in pages:
        body, relp = read_md(pg["rel"], pg["order"])
        bodies.append((pg, body, relp))
    kept, note, total = [], "", 0
    for i, (pg, body, relp) in enumerate(bodies, 1):
        size = len((body or "").encode("utf-8"))
        if max_pages and i > max_pages:
            note = (f"⚠ body budget: {len(bodies)} pages matched, --max-pages {max_pages} "
                    f"→ only the first {max_pages} page bodies included (the list stays complete)")
            break
        if max_bytes and total + size > max_bytes:
            note = (f"⚠ body budget: total exceeds --max-bytes {max_bytes} "
                    f"→ first {len(kept)} pages included ({total} bytes)")
            break
        kept.append((pg, body, relp))
        total += size
    return note, kept


def render(pages, full=False, max_pages=None, max_bytes=None, json_out=False,
           grep=False):
    """pages: list of dict {rel,order,id,title,created,lastModified,path}"""
    if json_out:
        for pg in pages:
            pg.pop("content", None)
        if full:
            note, kept = budget_bodies(pages, max_pages, max_bytes)
            by_id = {id(pg): (body, relp) for pg, body, relp in kept}
            for pg in pages:
                if id(pg) in by_id and by_id[id(pg)][0] is not None:
                    pg["content"] = by_id[id(pg)][0]
            if note:
                pages.append({"_note": note})
        return hit_json(pages)

    # ---- md / human-readable mode ----
    lines, cur = [], None
    for pg in pages:
        if pg["rel"] != cur:
            cur = pg["rel"]
            lines.append(f"\n## {cur}")
        lines.append(
            f"- {pg['order']:03d} | {display_title(pg['title'])}"
            f"  [created {fmt_dt(pg['created'])} · modified {fmt_dt(pg['lastModified'])}]"
            f"{'  (matched)' if grep else ''}")
    head = "\n".join(lines)
    if not full:
        return head + "\n"

    note, kept = budget_bodies(pages, max_pages, max_bytes)
    chunks = [head]
    for pg, body, relp in kept:
        if body is None:
            chunks.append(f"\n\n<!-- missing md file: {pg['rel']} {pg['order']:03d} -->")
            continue
        chunks.append(f"\n\n<!-- ═══ {pg['order']:03d} {display_title(pg['title'])} · {relp} ═══ -->\n{body}")
    if note:
        chunks.append("\n\n" + note)
    return "".join(chunks)


# ---------- subcommands ----------
def cmd_list(manifest, args):
    n = 0
    out = []
    for rel, order, pid, pm in iter_pages(manifest, args.section):
        out.append({"rel": rel, "order": order, "id": pid,
                    "title": pm.get("title", ""),
                    "created": utc_to_local(pm.get("createdDateTime")),
                    "lastModified": utc_to_local(pm.get("lastModifiedDateTime")),
                    "path": page_relpath(rel, order)})
        n += 1
    sys.stderr.write(f"# {n} page(s)\n")
    print(render(out, json_out=args.format == "json"))


def cmd_since(manifest, args):
    start, end = window_bounds(args.since, args.until)
    out = []
    for rel, order, pid, pm in iter_pages(manifest, args.section):
        if page_in_window(pm, start, end, args.kind):
            out.append({"rel": rel, "order": order, "id": pid,
                        "title": pm.get("title", ""),
                        "created": utc_to_local(pm.get("createdDateTime")),
                        "lastModified": utc_to_local(pm.get("lastModifiedDateTime")),
                        "path": page_relpath(rel, order)})
    if not out:
        if args.format == "json":
            return print("[]")
        print(f"window [{args.since or 'earliest'} → {args.until or 'today'}] kind={args.kind}: no page matched")
        return
    print(render(out, full=args.full, max_pages=args.max_pages,
                 max_bytes=args.max_bytes, json_out=args.format == "json"))
    if args.full:
        miss = missing_bodies(out)
        if miss:
            print(f"⚠ {miss} page(s) missing their md file — the body text in this batch is "
                  f"incomplete (store snapshot incomplete), run html2md.py to fill it in and read again", file=sys.stderr)
            sys.exit(1)


def cmd_week(manifest, args):
    since_s, until_s = this_week(args.weeks_ago)
    args.since, args.until = since_s, until_s
    args.kind = "all"
    sys.stderr.write(f"# this week window: {since_s} → {until_s}\n")
    cmd_since(manifest, args)


def cmd_grep(manifest, args):
    kw = args.kw
    start, end = window_bounds(args.since, args.until)
    out, unreadable = [], 0
    for rel, order, pid, pm in iter_pages(manifest, args.section):
        if not page_in_window(pm, start, end, "all"):
            continue
        title_hit = kw in pm.get("title", "")
        body, _ = read_md(rel, order)
        if body is None:
            # an unreadable body ≠ the keyword is absent: whether this page
            # matches is unknown
            unreadable += 1
        body_hit = body is not None and kw in body
        if title_hit or body_hit:
            out.append({"rel": rel, "order": order, "id": pid,
                        "title": pm.get("title", ""),
                        "created": utc_to_local(pm.get("createdDateTime")),
                        "lastModified": utc_to_local(pm.get("lastModifiedDateTime")),
                        "path": page_relpath(rel, order),
                        "match": ("title" if title_hit else "") +
                                 ("body" if body_hit else "")})
    def bail_if_blind():
        """the body of some page could not be read at all → results may be missing
        hits, rc=1 tells the caller/scheduler about it"""
        if unreadable:
            print(f"⚠ the body text of {unreadable} page(s) is unreadable (store is missing the md "
                  f"file) — this search result is incomplete, \"no match\" cannot be trusted; "
                  f"run html2md.py to fill it in and search again", file=sys.stderr)
            sys.exit(1)

    if not out:
        if args.format == "json":
            print("[]")
        else:
            print(f"grep {kw!r}: no match")
        bail_if_blind()
        return
    sys.stderr.write(f"# grep {kw!r}: {len(out)} page(s) matched\n")
    if args.format == "json":
        print(hit_json(out))
    else:
        for pg in out:
            print(f"- [{pg['rel']} {pg['order']:03d}] {display_title(pg['title'])}"
                  f"  (match {pg['match']})")
    bail_if_blind()


def cmd_fetch(manifest, args):
    """locate by: NNN | title substring | rel/NNN | rel/title substring; output
    metadata + full text"""
    q = args.page.strip()
    rel_q, rest = (q.rsplit("/", 1) + [None])[:2] if "/" in q else (None, q)
    # locate candidates
    cands = []
    for rel, order, pid, pm in iter_pages(manifest, args.section):
        if rel_q and not match_section(rel, rel_q):
            continue
        if rest.isdigit() and order == int(rest):
            cands.append((rel, order, pid, pm))
        elif not rest.isdigit() and rest.lower() in pm.get("title", "").lower():
            cands.append((rel, order, pid, pm))
    if not cands:
        sys.exit(f"fetch {args.page!r}: no match. use NNN, a title substring or section/NNN")
    if len(cands) > 1:
        for rel, order, pid, pm in cands:
            print(f"- [{rel} {order:03d}] {display_title(pm.get('title',''))}")
        sys.exit(f"fetch {args.page!r}: several pages matched — qualify it, e.g. "
                 f"--section {cands[0][0]} --page {cands[0][1]:03d}, "
                 f"or use a more precise title")
    rel, order, pid, pm = cands[0]
    body, relp = read_md(rel, order)
    meta = (f"# {pm.get('title','')}\n"
            f"- section: {rel}\n- order: {order:03d}\n"
            + (f"- path: {relp}\n" if relp else "")
            + f"- created: {fmt_dt(utc_to_local(pm.get('createdDateTime')))}\n"
            f"- modified: {fmt_dt(utc_to_local(pm.get('lastModifiedDateTime')))}\n")
    print(meta)
    if body is None:
        # the manifest has this page but store does not → snapshot incomplete, it
        # is not "cannot be found"
        print(f"✗ the md file of {rel} {order:03d} is not in store — the snapshot is "
              f"incomplete, run html2md.py to fill it in", file=sys.stderr)
        sys.exit(1)
    print(body)


# ---------- content-level diff (side track: a git wrapper, on demand) ----------
def store_commits(n=1):
    """the last n commits that changed this notebook's store (newest → oldest)"""
    out = subprocess.run(["git", "-C", NOTECLAW, "log", f"-{n}", "--format=%H", "--",
                          _git_store_path()],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [h for h in (out.stdout or "").split() if h]


def last_store_commit():
    """hash of the most recent commit that changed this notebook's store (the
    default --from base)"""
    cs = store_commits(1)
    return cs[0] if cs else None


def store_entry(sp):
    """git path → (rel, nnn, stem). store/<notebook>/<section>/NNN_<title>.md."""
    parts = sp.split("/")
    if parts and parts[0] == "store":
        parts = parts[1:]
    if NB_SEG and parts and parts[0] == NB_SEG:
        parts = parts[1:]
    relp = "/".join(parts)
    d, fn = os.path.split(relp)
    m = re.match(r"^(\d+)_(.*)\.md$", fn)
    if m:
        return d, int(m.group(1)), m.group(2)
    return d, None, fn


def diff_entries(manifest, frm, to):
    """git diff --name-status -z -M → list of page-level change entries.
    returns [{kind, sim?, rel, nnn, stem, title?, old_nnn?, old_stem?, old_title?, path}]
    the title is looked up in the current manifest first (rel+NNN), falling back
    to the file name stem when not found."""
    raw = subprocess.run(["git", "-C", NOTECLAW, "diff", "--name-status", "-z", "-M",
                          frm, to, "--", _git_store_path()], capture_output=True)
    if raw.returncode != 0:
        sys.exit(f"git diff {frm} {to} failed: "
                 + raw.stderr.decode("utf-8", "replace").strip())
    toks = raw.stdout.split(b"\0")
    idx = {}
    for rel, sec in manifest.get("sections", {}).items():
        for order, (pid, pm) in enumerate(sec["pages"].items(), 1):
            idx[(rel, order)] = pm.get("title", "")

    def resolve_title(rel, nnn, stem):
        """prefer the full title from the manifest, but only when the file name
        stem for this rel/NNN in the current store matches the given stem (so an
        NNN drift across snapshots never attributes the wrong title); otherwise
        fall back to the title carried by the file name."""
        if rel is not None and nnn is not None and (rel, nnn) in idx:
            p = page_path(rel, nnn)
            if p:
                base = os.path.basename(p)[:-3]
                fstem = base.split("_", 1)[1] if "_" in base else base
                if fstem == stem:
                    return idx[(rel, nnn)], False
        return stem, True

    entries, i = [], 0
    while i < len(toks):
        t = toks[i].decode("utf-8", "replace")
        if not t:
            i += 1
            continue
        if t[0] in ("R", "C"):
            sim = int(t[1:]) if t[1:].isdigit() else None
            old = toks[i + 1].decode("utf-8", "replace")
            new = toks[i + 2].decode("utf-8", "replace")
            i += 3
            rel, nnn, stem = store_entry(new)
            orel, onnn, ostem = store_entry(old)
            t_new, f_new = resolve_title(rel, nnn, stem)
            t_old, f_old = resolve_title(orel, onnn, ostem)
            entries.append({"kind": "R", "sim": sim, "rel": rel, "nnn": nnn,
                            "stem": stem, "title": t_new, "title_is_fn": f_new,
                            "old_nnn": onnn, "old_stem": ostem, "old_title": t_old,
                            "old_title_is_fn": f_old, "path": new, "old_path": old})
        else:
            kind = t
            sp = toks[i + 1].decode("utf-8", "replace")
            i += 2
            rel, nnn, stem = store_entry(sp)
            t_new, f_new = resolve_title(rel, nnn, stem)
            entries.append({"kind": kind, "rel": rel, "nnn": nnn, "stem": stem,
                            "title": t_new, "title_is_fn": f_new, "path": sp})
    return entries


def diff_label(k):
    return {"A": "added", "D": "deleted", "M": "modified", "R": "renamed", "C": "copied"}.get(k, k)


def cmd_diff(manifest, args):
    defaulted = args.from_rev is None
    frm = args.from_rev or last_store_commit()
    if frm is None:
        sys.exit("diff: store/ has no commit yet, run a sync snapshot first")
    to = args.to_rev or "HEAD"
    sha = {}
    for r in (frm, to):
        chk = subprocess.run(["git", "-C", NOTECLAW, "rev-parse", "--verify", "--quiet", r],
                             capture_output=True, text=True)
        if chk.returncode != 0:
            sys.exit(f"diff: rev {r!r} does not exist")
        sha[r] = chk.stdout.strip()
    # default base = "the most recent commit that changed store", while html2md.py
    # commits on every sync round and later commits (e.g. the weekly report) do not
    # touch store — so there is necessarily no store change between the default base
    # and HEAD, and this "0 entries" was chosen by the base, it is not "nothing
    # changed". When --from is given explicitly the user's choice rules, and the hint
    # is only shown when both sides are the same commit.
    degenerate = (defaulted or sha[frm] == sha[to])

    entries = diff_entries(manifest, frm, to)
    if args.section:
        entries = [e for e in entries if e["rel"]
                   and (e["rel"] == args.section
                        or e["rel"].startswith(args.section + os.sep))]
    if args.page:
        q = args.page.strip()
        def hit(e):
            return (q.isdigit() and (e.get("nnn") == int(q)
                                     or e.get("old_nnn") == int(q))) or \
                   q in e.get("title", "") or q in e.get("stem", "") or \
                   (e.get("old_title") and q in e["old_title"]) or \
                   (e.get("old_stem") and q in e["old_stem"])
        entries = [e for e in entries if hit(e)]

    # summary
    stats = {}
    for e in entries:
        k = "R(same content)" if e["kind"] == "R" and e.get("sim") == 100 else e["kind"]
        stats[k] = stats.get(k, 0) + 1
    total = sum(stats.values())
    stat_s = " · ".join(f"{diff_label(k)} {v}" if k != "R(same content)" else f"renamed, same content {v}"
                         for k, v in sorted(stats.items(), key=lambda x: x[0]))

    # group per section (keeping first-appearance order)
    groups = {}
    order = []
    for e in entries:
        rel = e["rel"] or "(store root)"
        if rel not in groups:
            groups[rel] = []
            order.append(rel)
        groups[rel].append(e)

    if args.format == "json":
        clean = []
        for e in entries:
            d = {k: e[k] for k in ("kind", "rel", "nnn", "title", "path")}
            d["title_is_fn"] = e["title_is_fn"]
            if e["kind"] == "R":
                d["sim"] = e.get("sim")
                d["old_nnn"] = e.get("old_nnn")
                d["old_title"] = e.get("old_title")
            clean.append(d)
        return print(json.dumps({"from": frm, "to": to,
                                 "from_sha": sha[frm], "to_sha": sha[to],
                                 # true = this empty result does not mean "nothing
                                 # changed": there is no store commit to compare
                                 # between the base and the target (run a sync first,
                                 # then query again with --from)
                                 "degenerate_base": degenerate,
                                 "summary": stats, "changes": clean},
                                ensure_ascii=False, indent=1))

    head = (f"# store diff: {frm} → {to}\n"
            f"{total} {'entry' if total == 1 else 'entries'}: {stat_s or '(no differences)'}\n")
    if degenerate and not total:
        why = (f"the base and the target resolve to the same commit ({sha[frm][:7]})"
               if sha[frm] == sha[to] else
               f"the default base (the most recent commit that changed store, {sha[frm][:7]}) has no store snapshot after it")
        cs = store_commits(2)                      # newest → oldest
        prev = cs[1] if len(cs) > 1 else None
        go = (f"  · to see what changed since the previous snapshot: --from {prev[:7]}\n" if prev else
              "  · there is only one snapshot so far, no earlier base to compare (diff again after the next sync)\n")
        print(head + f"\n⚠ {why} — this \"0 entries\" was chosen by the base, it does not mean \"nothing changed\".\n"
              + go +
              "  · to see a whole period: use $BASE from the weekly report flow (references/weekly-report.md)")
        return
    if not total:
        print(head + "\nstore content is identical between the two snapshots (determinism check: no change means no output, no noise).")
        return

    # list
    lines = [head]
    for rel in order:
        lines.append(f"\n## {rel}")
        for e in groups[rel]:
            old = f""
            if e["kind"] == "R":
                old = f"  {e.get('old_nnn') or '—'}→{e.get('nnn') or '—'} old name {e.get('old_title') or '?'}"
            lines.append(f"- {diff_label(e['kind'])} [{e.get('nnn') or '—':>3}] {e['title'] or '(no title)'}"
                         + (f" (file name)" if e["title_is_fn"] else "")
                         + (f" · sim {e['sim']}%" if e["kind"] == "R" else "") + old)
    print("\n".join(lines))

    # content-level diff (only M and R<100; budget gate: truncate per file, the list
    # is always complete)
    if args.full:
        budget = args.max_bytes if args.max_bytes else 60000
        used = 0
        for e in entries:
            if e["kind"] not in ("M", "R") or (e["kind"] == "R" and e.get("sim") == 100):
                continue
            if used >= budget:
                print(f"\n⚠ the content diff budget of {budget} bytes is used up ({used} bytes "
                      f"printed), raise --max-bytes for the rest. The list is unaffected.")
                break
            diff = subprocess.run(["git", "-C", NOTECLAW, "diff", "--unified=3", "-M",
                                   frm, to, "--", e["path"], e["old_path"]], capture_output=True) \
                if e["kind"] == "R" else \
                subprocess.run(["git", "-C", NOTECLAW, "diff", "--unified=3", "-M",
                                frm, to, "--", e["path"]], capture_output=True)
            body = diff.stdout.decode("utf-8", "replace")
            nxt = len(body.encode("utf-8"))
            hdr = (f"\n=== {diff_label(e['kind'])} "
                   f"[{e.get('nnn') or '—'}] {e['title']} · {e['rel']} ===")
            avail = budget - used
            print(hdr)
            if nxt <= avail:
                print(body.rstrip("\n"))
                used += nxt
            else:
                cut = body.encode("utf-8")[:avail].decode("utf-8", "ignore")
                print(cut.rstrip("\n"))
                print(f"… ⚠ this page's diff of {nxt} bytes exceeds the remaining budget of {avail}, truncated (raise --max-bytes)")
                used = budget


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="noteclaw query layer (read-only)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="page list per section")
    p.add_argument("--section")
    p.add_argument("--format", choices=["md", "json"], default="md")

    p = sub.add_parser("since", help="page filtering by time window")
    p.add_argument("--since", required=True)
    p.add_argument("--until")
    p.add_argument("--section")
    p.add_argument("--kind", choices=["all", "new", "edited"], default="all")
    p.add_argument("--full", action="store_true")
    p.add_argument("--max-pages", type=int)
    p.add_argument("--max-bytes", type=int)
    p.add_argument("--format", choices=["md", "json"], default="md")

    p = sub.add_parser("week", help="this-week shortcut window")
    p.add_argument("--weeks-ago", type=int, default=0)
    p.add_argument("--section")
    p.add_argument("--full", action="store_true")
    p.add_argument("--max-pages", type=int)
    p.add_argument("--max-bytes", type=int)
    p.add_argument("--format", choices=["md", "json"], default="md")

    p = sub.add_parser("grep", help="keyword in title/body")
    p.add_argument("--kw", required=True)
    p.add_argument("--section")
    p.add_argument("--since")
    p.add_argument("--until")
    p.add_argument("--format", choices=["md", "json"], default="md")

    p = sub.add_parser("fetch", help="full text of one page (NNN/title substring/section+NNN)")
    p.add_argument("--page", required=True)
    p.add_argument("--section")

    p = sub.add_parser("diff", help="content-level diff (git side track, changes between snapshots)")
    p.add_argument("--from", dest="from_rev", default=None,
                   help="base rev (default: the most recent commit that changed store/)")
    p.add_argument("--to", dest="to_rev", default="HEAD", help="target rev (HEAD by default)")
    p.add_argument("--section")
    p.add_argument("--page", help="look at one page only (NNN/title substring)")
    p.add_argument("--name-only", action="store_true", help="print the list only, expand no diff")
    p.add_argument("--full", action="store_true",
                   help="expand the line-level diff of M/R (content changed) (budget 60KB by default)")
    p.add_argument("--max-bytes", type=int, help="content diff budget gate")
    p.add_argument("--format", choices=["md", "json"], default="md")

    args = ap.parse_args()
    m = load_manifest()
    {"list": cmd_list, "since": cmd_since, "week": cmd_week,
     "grep": cmd_grep, "fetch": cmd_fetch, "diff": cmd_diff}[args.cmd](m, args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(2)
