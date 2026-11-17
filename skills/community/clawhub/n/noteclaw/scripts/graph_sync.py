#!/usr/bin/env python3
"""noteclaw graph_sync.py — page-level read-only incremental sync over the Microsoft Graph OneNote API

Mirror OneNote notebooks read-only into a local HTML cache + manifest (page ETags).

Why change detection uses ETags: the page-level lastModifiedDateTime in Graph has a
known reliability problem (the timestamp may not move even when the content is
edited), so an incremental sync driven by page timestamps misses pure content edits.
Two reliable signals:
  1. section-level lastModifiedDateTime — any addition/change/removal inside a
     section updates it
  2. the ETag of page /content — a content fingerprint; a conditional GET
     (If-None-Match) answers precisely "did this page change since last time":
     304 = unchanged (empty body) / 200 = changed (new full text returned)

Detection strategy (--mode etag, the default):
  1. section gate: enumerate sections (with the section timestamp) → compare against
     the manifest record
     - section untouched → skip the whole section, zero requests
     - section touched/new/encryption state changed → go to step 2
  2. ETag probe (only for touched sections):
     - fetch that section's page list → compare against the manifest: added pages,
       deleted pages, existing pages
     - existing pages: $batch conditional GET (20 per batch, If-None-Match=last ETag)
       304 → unchanged, nothing to do / 200 → store the new content + new ETag /
       404 → the page was deleted
     - pages without an ETag record (migration/cold start): plain GET
  3. true-signal statistics for timestamps: among the pages whose conditional GET
     reported a change (200), count how many moved lastModifiedDateTime as well —
     if all of them moved, the timestamp field is trustworthy and switching back to
     --mode timestamp (fewer requests) can be suggested; otherwise stay in etag mode.

Fallback mode (--mode timestamp): compare by page lastModifiedDateTime; switch back
  to it when timestamps are reliable (each round only pulls the list + changed pages,
  which is cheaper).

First use (authorization): run auth_code.py (authorization code flow) in the same
directory first to obtain a token.
Credentials: client_id + client_secret as a pair — environment variables
CLIENT_ID/CLIENT_SECRET, or a section in rclone.conf holding
client_id+client_secret (the authorization code flow needs the secret).
Permissions: Notes.Read offline_access (token: .auth/notes_token.json, 0600)
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Single source of shared credentials (env vars → rclone.conf → built-in rclone
# public application fallback); when refreshing credentials the client_id recorded
# in the token file is preferred
from noteclaw_creds import refresh_client_creds

# Working directory = the cwd the command was run from (NOTECLAW_HOME overrides).
# Every artifact (manifest/store/cache/.auth) lands in the working directory; the
# script itself may live anywhere.
NOTECLAW = os.environ.get("NOTECLAW_HOME") or os.getcwd()
TOKEN_FILE = os.path.join(NOTECLAW, ".auth", "notes_token.json")
MANIFEST = os.path.join(NOTECLAW, "manifest.json")
CACHE_BASE = os.path.join(NOTECLAW, "cache", "pages")
STORE_BASE = os.path.join(NOTECLAW, "store")
# After a notebook is chosen, narrow down to the <notebook> subdirectory (switching
# notebooks in one data directory never overwrites the other)
CACHE_DIR = CACHE_BASE
STORE_DIR = STORE_BASE

API = "https://graph.microsoft.com/v1.0"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
REFRESH_SCOPE = "Notes.Read offline_access"
SLEEP = 0.25          # base rate limit (interval between Graph requests)
BATCH_MAX = 20        # $batch cap per batch
ILLEGAL = re.compile(r'[/\\:*?"<>|\x00-\x1f]')


# ---------- utilities ----------
def log(msg):
    print(msg, flush=True)


def sanitize(name):
    """section/page name → safe directory/file name (same cleanup rules as
    html2md.py / notequery.py)"""
    s = ILLEGAL.sub("_", name).strip()
    return s or "untitled"


# ---------- token ----------
def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        raise RuntimeError(
            f"token file not found: {TOKEN_FILE}\n"
            f"→ authorize first: python3 <noteclaw-skill>/scripts/auth_code.py")
    with open(TOKEN_FILE) as f:
        return json.load(f)


def refresh_access_token():
    """Refresh the token and write it back to the token file (kept at 0600).
    Credentials prefer the client_id recorded in the token file (the one actually
    used at authorization time) and fall back to env vars → rclone.conf → the
    built-in rclone public application only when it is missing."""
    tok = load_tokens()
    if not tok.get("refresh_token"):
        raise RuntimeError(
            f"{TOKEN_FILE} has no refresh_token (old token / incomplete authorization)\n"
            f"→ rerun python3 <noteclaw-skill>/scripts/auth_code.py to finish authorizing")
    cid, csec = refresh_client_creds(TOKEN_FILE)
    if not cid:
        raise RuntimeError(
            f"no client_id + client_secret found: set the environment variables CLIENT_ID/CLIENT_SECRET, "
            f"or make sure {os.path.expanduser('~/.config/rclone/rclone.conf')} has a "
            f"section with client_id+client_secret (this tool only reads it, your rclone config stays untouched)")
    body = {
        "client_id": cid,
        "client_secret": csec,
        "grant_type": "refresh_token",
        "refresh_token": tok["refresh_token"],
        "scope": REFRESH_SCOPE,
    }
    data = urllib.parse.urlencode(body).encode()
    req = urllib.request.Request(TOKEN_ENDPOINT, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            nt = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="replace")
        raise RuntimeError(
            f"token refresh failed HTTP {e.code} (expired/revoked/network hiccup)\n"
            f"→ just authorize again: python3 <noteclaw-skill>/scripts/auth_code.py\n"
            f"  (server returned: {body_txt[:200]})")
    except urllib.error.URLError as e:
        raise RuntimeError(f"token refresh failed: cannot reach Microsoft services ({e.reason}) — check your network and retry")
    tok["access_token"] = nt["access_token"]
    tok["refresh_token"] = nt.get("refresh_token", tok["refresh_token"])
    tok["expires_in"] = nt.get("expires_in", 3600)
    with open(TOKEN_FILE, "w") as f:
        json.dump(tok, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)
    log("  ↻ token refreshed")
    return tok["access_token"]


class Graph:
    """Minimal Graph client: JSON + text + automatic refresh/retry on 401 + backoff
    on 429"""
    def __init__(self):
        tok = load_tokens()
        if not tok.get("access_token"):
            # only a refresh_token (right after authorization, before the first
            # start) → refresh first to get an access_token
            if not tok.get("refresh_token"):
                raise RuntimeError(
                    f"{TOKEN_FILE} has no usable credentials\n"
                    f"→ run python3 <noteclaw-skill>/scripts/auth_code.py to authorize")
            self.token = refresh_access_token()
        else:
            self.token = tok["access_token"]

    def _headers(self, extra=None):
        h = {"Authorization": f"Bearer {self.token}"}
        if extra:
            h.update(extra)
        return h

    def _open_full(self, url, retry=True):
        """GET → (status, headers_dict, body_bytes)"""
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            if e.code == 401 and retry:
                self.token = refresh_access_token()
                return self._open_full(url, retry=False)
            if e.code == 429 and retry:
                wait = 5
                try:
                    wait = max(1, int(e.headers.get("Retry-After", "5")))
                except (TypeError, ValueError):
                    pass
                log(f"  ⏳ 429 rate limited, backing off {wait}s …")
                time.sleep(wait)
                return self._open_full(url, retry=False)
            return e.code, dict(e.headers), e.read()
        except urllib.error.URLError as e:
            raise RuntimeError(f"cannot reach Microsoft services ({e.reason}) — check your network and retry")

    def _post_full(self, url, payload, retry=True):
        """POST JSON → (status, headers_dict, body_bytes)"""
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data,
                                     headers=self._headers({"Content-Type": "application/json"}))
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            if e.code == 401 and retry:
                self.token = refresh_access_token()
                return self._post_full(url, payload, retry=False)
            if e.code == 429 and retry:
                wait = 5
                try:
                    wait = max(1, int(e.headers.get("Retry-After", "5")))
                except (TypeError, ValueError):
                    pass
                log(f"  ⏳ 429 rate limited, backing off {wait}s …")
                time.sleep(wait)
                return self._post_full(url, payload, retry=False)
            return e.code, dict(e.headers), e.read()
        except urllib.error.URLError as e:
            raise RuntimeError(f"cannot reach Microsoft services ({e.reason}) — check your network and retry")

    def json(self, url):
        s, _, body = self._open_full(url)
        if s != 200:
            return None, s, body
        return json.loads(body), 200, None

    def text(self, url):
        s, _, body = self._open_full(url)
        return body.decode("utf-8", "replace") if s == 200 else None, s

    def page_content(self, page_id):
        """plain GET of one page's content → (html, etag, status)"""
        s, h, body = self._open_full(f"{API}/me/onenote/pages/{page_id}/content")
        if s != 200:
            return None, None, s
        return body.decode("utf-8", "replace"), h.get("ETag"), 200

    def batch_content(self, conds):
        """$batch conditional GET of content. conds: [(page_id, etag), ...]
        → {page_id: {"status": 304|200|404|other, "html": str|None, "etag": str|None}}"""
        out = {}
        for i in range(0, len(conds), BATCH_MAX):
            chunk = conds[i:i + BATCH_MAX]
            requests = [
                {"id": str(j), "method": "GET",
                 "url": f"/me/onenote/pages/{pid}/content",
                 "headers": {"If-None-Match": etag}}
                for j, (pid, etag) in enumerate(chunk)]
            s, _h, body = self._post_full(f"{API}/$batch", {"requests": requests})
            if s != 200:
                err = body.decode("utf-8", "replace")[:200] if body else ""
                log(f"  ✗ $batch HTTP {s}: {err}")
                for pid, _etag in chunk:
                    out[pid] = {"status": s, "html": None, "etag": None}
                continue
            try:
                resp = json.loads(body)
            except Exception:
                log("  ✗ failed to parse the $batch response")
                for pid, _etag in chunk:
                    out[pid] = {"status": -1, "html": None, "etag": None}
                continue
            for r in resp.get("responses", []):
                pid = chunk[int(r["id"])][0]
                st = r.get("status")
                hd = r.get("headers") or {}
                b = r.get("body")
                if st == 200:
                    html = b if isinstance(b, str) else (
                        b.decode("utf-8", "replace") if isinstance(b, bytes) else "")
                    out[pid] = {"status": 200, "html": html, "etag": hd.get("ETag")}
                else:
                    out[pid] = {"status": st, "html": None, "etag": None}
            time.sleep(SLEEP)
        return out

    def pages(self, section_id):
        """paged fetch of the full page list of a section (id,title,created,lastModified)"""
        out, seen, url = [], set(), f"{API}/me/onenote/sections/{section_id}/pages?$select=id,title,createdDateTime,lastModifiedDateTime"
        while url:
            d, s, body = self.json(url)
            if s != 200:
                err = body.decode("utf-8", "replace")[:300] if body else ""
                return None, s, err
            for p in d.get("value", []):
                if p["id"] not in seen:
                    seen.add(p["id"])
                    out.append(p)
            url = d.get("@odata.nextLink")
            if url:
                time.sleep(SLEEP)
        return out, 200, None


# ---------- tree enumeration (OneNote API: section groups may be nested) ----------
def list_notebooks(g):
    d, s, body = g.json(f"{API}/me/onenote/notebooks?$select=id,displayName")
    if s != 200:
        raise RuntimeError(f"listing notebooks failed HTTP {s}: {body.decode('utf-8','replace')[:200]}")
    return d.get("value", [])


def walk_group(g, group_id, prefix):
    """recursively enumerate section groups → [(relpath, section_id, name, lastModifiedDateTime)]"""
    log(f"  ↳ group {prefix}")
    out = []
    d, s, _ = g.json(f"{API}/me/onenote/sectionGroups/{group_id}/sections?$select=id,displayName,lastModifiedDateTime")
    if s == 200:
        for sec in d.get("value", []):
            out.append((os.path.join(prefix, sec["displayName"]), sec["id"],
                        sec["displayName"], sec.get("lastModifiedDateTime", "")))
    d, s, _ = g.json(f"{API}/me/onenote/sectionGroups/{group_id}/sectionGroups?$select=id,displayName")
    if s == 200:
        for grp in d.get("value", []):
            out.extend(walk_group(g, grp["id"], os.path.join(prefix, grp["displayName"])))
    return out


def list_sections(g, notebook_id):
    """enumerate every section of a notebook (including those inside section
    groups), keeping the group hierarchy in relpath
    returns [(relpath, section_id, name, lastModifiedDateTime)]"""
    out = []
    d, s, _ = g.json(f"{API}/me/onenote/notebooks/{notebook_id}/sections?$select=id,displayName,lastModifiedDateTime")
    if s == 200:
        for sec in d.get("value", []):
            out.append((sec["displayName"], sec["id"], sec["displayName"],
                        sec.get("lastModifiedDateTime", "")))
    d, s, _ = g.json(f"{API}/me/onenote/notebooks/{notebook_id}/sectionGroups?$select=id,displayName")
    if s == 200:
        for grp in d.get("value", []):
            out.extend(walk_group(g, grp["id"], grp["displayName"]))
    return out


# ---------- manifest ----------
def manifest_unusable_msg(why):
    """Single wording used when manifest.json exists but is unusable (the literal
    is kept identical across the three scripts)"""
    return (f"manifest.json is unusable ({why})\n"
            f"  → back it up, delete manifest.json and cold start again: graph_sync.py --all && html2md.py")


def load_manifest():
    """Read the manifest. File missing → create an empty one (cold start); file
    present but unusable (schema is not 3 / corrupt structure) → fail with an error
    instead of silently clearing it."""
    if not os.path.exists(MANIFEST):
        m = {"schema": 3, "notebook": None, "last_sync": None,
             "detect_mode": None, "sections": {}, "skipped": []}
    else:
        with open(MANIFEST) as f:
            m = json.load(f)
        if m.get("schema") != 3:
            raise RuntimeError(manifest_unusable_msg(f"schema={m.get('schema')}, needs 3"))
        if not isinstance(m.get("sections"), dict):
            raise RuntimeError(manifest_unusable_msg("sections missing, file is corrupt"))
    if m.get("detect_mode") is None:
        m["detect_mode"] = "etag"
    m.setdefault("skipped", [])
    return m


def save_manifest(m):
    with open(MANIFEST, "w") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)
    os.chmod(MANIFEST, 0o600)


# ---------- fetch helpers ----------
def save_html(rel, pid, html):
    dest_dir = os.path.join(CACHE_DIR, sanitize(rel))
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, sanitize(pid) + ".html")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    return dest


def page_entry(p, etag=None):
    """list entry → manifest page entry (etag None = no fingerprint yet)"""
    return {"title": p.get("title", ""),
            "lastModifiedDateTime": p.get("lastModifiedDateTime", ""),
            "createdDateTime": p.get("createdDateTime", ""),
            "etag": etag}


def http_err(err):
    try:
        return json.loads(err or "{}").get("error", {}).get("code", "")
    except Exception:
        return ""


# ---------- section comparison (two modes) ----------
def plan_timestamp(pages, old_pages, force_all):
    """compare by page lastModifiedDateTime → (todo_pages, removed_pids)"""
    todo, seen = [], set()
    for p in pages:
        pid = p["id"]
        seen.add(pid)
        op = old_pages.get(pid)
        lm = p.get("lastModifiedDateTime", "")
        if op is None or op.get("lastModifiedDateTime") != lm or force_all:
            todo.append(p)
    removed = [pid for pid in old_pages if pid not in seen]
    return todo, removed


def plan_etag(pages, old_pages, force_all):
    """etag: → (plain_pages[no fingerprint/new], cond[(pid,etag)], removed_pids)"""
    plain, cond, seen = [], [], set()
    for p in pages:
        pid = p["id"]
        seen.add(pid)
        op = old_pages.get(pid)
        if op is None or not op.get("etag") or force_all:
            plain.append(p)
        else:
            cond.append((pid, op["etag"]))
    removed = [pid for pid in old_pages if pid not in seen]
    return plain, cond, removed


def main():
    ap = argparse.ArgumentParser(description="noteclaw Graph OneNote page-level incremental sync")
    ap.add_argument("--list-notebooks", action="store_true")
    ap.add_argument("--list", action="store_true", help="list the tree + page counts, fetch no content")
    ap.add_argument("--dry-run", action="store_true", help="show what would be fetched, fetch nothing")
    ap.add_argument("--all", action="store_true", help="ignore the checks and fetch everything (cold start, builds the baseline)")
    ap.add_argument("--no-gate", action="store_true",
                    help="bypass the section time gate but keep the ETag conditional GET (safety net: a missed section lm never means a missed sync)")
    ap.add_argument("--mode", choices=["etag", "timestamp"], default="etag",
                    help="detection mode: etag=section gate + ETag probe (default) / timestamp=compare by page timestamp")
    ap.add_argument("--notebook", default=None, help="notebook name (default: the NOTECLAW_NOTEBOOK env var; a manifest record is reused)")
    ap.add_argument("--section", default=None, help="sync only matching sections (relpath prefix)")
    args = ap.parse_args()

    if args.list_notebooks:
        # purely diagnostic command, reads no manifest (must run even with a broken
        # manifest, for troubleshooting)
        for nb in list_notebooks(Graph()):
            print(f"  {nb['displayName']}  id={nb['id']}")
        return

    # validate the local manifest first (fail immediately instead of wasting a round
    # of network calls)
    m = load_manifest()

    # pick the notebook: a manifest record wins; with no record and several
    # notebooks it fails so the user names one explicitly
    g = Graph()
    nbs = list_notebooks(g)
    rec = m.get("notebook") or {}
    want = args.notebook or os.environ.get("NOTECLAW_NOTEBOOK")
    if want:
        nb = next((x for x in nbs if x["displayName"] == want), None)
        if nb is None:
            print(f"notebook {want!r} not found, available: {[x['displayName'] for x in nbs]}")
            sys.exit(1)
    elif rec.get("id"):
        nb = next((x for x in nbs if x["id"] == rec["id"]), None)
        if nb is None:
            log(f"⚠ the notebook recorded in the manifest ({rec.get('displayName','?')}) no longer exists, choosing again")
    else:
        nb = None
    if nb is None:
        if len(nbs) == 1:
            nb = nbs[0]
            log(f"single notebook: {nb['displayName']!r}")
        else:
            print(f"{len(nbs)} notebooks detected. To avoid mirroring the wrong one, name the notebook to mirror explicitly:")
            print("  --notebook <name>   or   the environment variable NOTECLAW_NOTEBOOK=<name>")
            print("available: python3 graph_sync.py --list-notebooks lists them all")
            for x in nbs:
                print(f"  · {x['displayName']}  id={x['id']}")
            sys.exit(1)
    log(f"📓 notebook: {nb['displayName']}  ({nb['id']})")
    # data is grouped per notebook: switching notebooks in one data directory never
    # overwrites the previous notebook's files
    global CACHE_DIR, STORE_DIR
    nb_key = sanitize(nb["displayName"])
    CACHE_DIR = os.path.join(CACHE_BASE, nb_key)
    STORE_DIR = os.path.join(STORE_BASE, nb_key)
    log(f"🔎 detection mode: {args.mode}{' (--all, everything)' if args.all else ''}")

    # enumerate sections (with the section-level timestamp, lightweight)
    log("enumerating sections …")
    secs = list_sections(g, nb["id"])
    if args.section:
        hit = [t for t in secs if t[0] == args.section
               or t[0].startswith(args.section + os.sep)]
        if not hit:
            log(f"⚠ section {args.section!r} matched nothing, available: {[t[0] for t in secs]}")
            sys.exit(1)
        secs = hit
        log(f"  ↳ filtered: only {args.section!r} ({len(hit)} section(s))")
    for rel, _sid, _name, lm in secs:
        log(f"    · {rel}  (section time {lm or '—'})")

    if args.list:
        # list the page count of every section in full (needs the per-section page
        # list)
        log(f"probing page counts for {len(secs)} section(s) — one request each, "
            "a line per section as it returns")
        for rel, sid, _name, _lm in secs:
            pages, s, err = g.pages(sid)
            if s == 200:
                log(f"    ✓ {rel}  ({len(pages)} page(s))")
            else:
                log(f"    🔒 {rel}  (HTTP {s} {http_err(err)})")
            time.sleep(SLEEP)
        return

    # manifest (reuse the m already loaded when the notebook was chosen; switching
    # notebooks → clear and rebuild, to prevent leftovers and same-name mixups)
    if m.get("notebook") and m["notebook"]["id"] != nb["id"]:
        log(f"⚠ the notebook recorded in the manifest ({m['notebook']['displayName']}) differs from the current one"
            f" → clearing sections/skipped and rebuilding (prevents old-notebook leftovers and same-name section mixups)")
        m["sections"] = {}
        m["skipped"] = []
        m["notebook"] = {"id": nb["id"], "displayName": nb["displayName"]}
    elif not m.get("notebook"):
        m["notebook"] = {"id": nb["id"], "displayName": nb["displayName"]}
    prev = m["sections"]
    skipped_map = {x.get("rel"): x for x in m.get("skipped", []) if isinstance(x, dict)}

    stats = {"plain": 0, "cond": 0, "not304": 0, "changed": 0, "removed": 0,
             "skip_sections": 0, "sync_sections": 0, "cond_changed": 0,
             "lm_moved": 0, "renamed_sections": 0, "gone_sections": 0,
             "fetch_err": 0}
    log("")

    # section identity map: rel currently in the manifest → id (for rename migration
    # and disappearance convergence)
    prev_by_id = {sec.get("id"): rel for rel, sec in prev.items()
                  if isinstance(sec, dict) and sec.get("id")}
    seen_ids = set()

    for rel, sid, _name, lm in secs:
        # ---- section rename migration (same id, new rel): move manifest/cache/store
        # together, no refetch ----
        if sid in prev_by_id and prev_by_id[sid] != rel:
            old_rel = prev_by_id[sid]
            log(f"↳ section renamed: {old_rel!r} → {rel!r} (id unchanged, data migrated without refetching)")
            prev[rel] = prev.pop(old_rel)
            if not args.dry_run:
                # cache directory name = sanitize(rel); store directory name = the
                # original rel (html2md's write rule)
                old_c = os.path.join(CACHE_DIR, sanitize(old_rel))
                new_c = os.path.join(CACHE_DIR, sanitize(rel))
                if os.path.isdir(old_c) and not os.path.isdir(new_c):
                    os.rename(old_c, new_c)
                old_s = os.path.join(STORE_DIR, old_rel)
                new_s = os.path.join(STORE_DIR, rel)
                if os.path.isdir(old_s) and not os.path.isdir(new_s):
                    os.rename(old_s, new_s)
            if old_rel in skipped_map:
                skipped_map[rel] = skipped_map.pop(old_rel)
                skipped_map[rel]["rel"] = rel
            prev_by_id[sid] = rel
            stats["renamed_sections"] += 1
        seen_ids.add(sid)
        old_sec = prev.get(rel)
        old_pages = old_sec.get("pages", {}) if isinstance(old_sec, dict) else {}

        # ---- encrypted/denied section (skipped memory + section timestamp gate) ----
        if rel in skipped_map and not args.all and not args.no_gate:
            if skipped_map[rel].get("lastModifiedDateTime") == lm:
                log(f"  🔒 {rel}: encrypted/denied and the section time did not move, skipping")
                stats["skip_sections"] += 1
                continue
            # the time moved → try the page list again to see whether it became
            # readable
            pages, s, err = g.pages(sid)
            time.sleep(SLEEP)
            if s != 200:
                if s in (401, 403):
                    skipped_map[rel] = {"rel": rel, "reason": f"HTTP {s} {http_err(err)}".strip(),
                                        "lastModifiedDateTime": lm}
                    log(f"  🔒 {rel}: still encrypted/denied (HTTP {s}), updating skipped")
                else:
                    # 5xx/other: suspected transient failure, do not lock it into
                    # skipped, retry automatically next round
                    log(f"  ⚠ {rel}: HTTP {s} (suspected transient failure) skipped this round; retried next round")
                continue
            del skipped_map[rel]
            m["skipped"] = [x for x in m.get("skipped", []) if x.get("rel") != rel]
            log(f"  🔓 {rel}: readable again, continuing the sync")
        else:
            # ---- section gate (the core): section time unchanged → skip the whole
            # section, zero requests ----
            # --no-gate (safety net) bypasses this gate but keeps the ETag conditional
            # GET (304 = unchanged, zero transfer)
            gate_open = args.all or args.no_gate or old_sec is None \
                or old_sec.get("lastModifiedDateTime") != lm
            if not gate_open:
                log(f"  ➖ {rel}: section time unchanged, skipping (manifest {len(old_pages)} page(s) untouched)")
                stats["skip_sections"] += 1
                continue
            pages, s, err = g.pages(sid)
            time.sleep(SLEEP)
            if s != 200:
                if s in (401, 403):
                    skipped_map[rel] = {"rel": rel, "reason": f"HTTP {s} {http_err(err)}".strip(),
                                        "lastModifiedDateTime": lm}
                    log(f"  🔒 {rel}: encrypted/denied (HTTP {s}), recorded in skipped")
                else:
                    # 5xx/other: suspected transient failure, do not lock it into
                    # skipped, retry automatically next round
                    log(f"  ⚠ {rel}: HTTP {s} (suspected transient failure) skipped this round; retried next round")
                continue

        stats["sync_sections"] += 1
        if args.mode == "timestamp":
            todo, removed = plan_timestamp(pages, old_pages, args.all)
            plain, cond = todo, []
        else:
            plain, cond, removed = plan_etag(pages, old_pages, args.all)

        stats["plain"] += len(plain)
        stats["cond"] += len(cond)
        stats["removed"] += len(removed)
        log(f"  ▶ {rel}: section moved, probing {len(pages)} page(s)"
            f" (plain {len(plain)} / conditional GET {len(cond)} / removed {len(removed)})")

        if args.dry_run:
            continue

        # ---- fetch phase ----
        # seed: pages still on the list keep their old entry (including the old etag)
        # and are overwritten after a successful fetch
        new_pages = {}
        for p in pages:
            pid = p["id"]
            new_pages[pid] = old_pages.get(pid) or page_entry(p)
        fetch_err = 0

        # 1) plain GET (new pages / pages without etag / --all)
        t0 = time.time()
        for i, p in enumerate(plain, 1):
            pid = p["id"]
            html, etag, s = g.page_content(pid)
            if i % 10 == 0 or i == len(plain):
                log(f"    … {rel}: plain {i}/{len(plain)} (elapsed {time.time()-t0:.0f}s)")
            if s == 200:
                save_html(rel, pid, html)
                new_pages[pid] = page_entry(p, etag)
                stats["changed"] += 1
            elif s == 404:
                removed.append(pid)
                stats["removed"] += 1
                log(f"    🗑 404: {rel} / {p.get('title','')[:30]} page deleted")
            else:
                fetch_err += 1
                log(f"    ✗ {rel} / {p.get('title','')[:30]}: HTTP {s} (old entry kept)")
            time.sleep(SLEEP)
        # 2) conditional GET (existing pages, $batch 20 per batch)
        if cond:
            res = g.batch_content(cond)
            for pid, etag0 in cond:
                r = res.get(pid, {})
                st = r.get("status")
                p = next(x for x in pages if x["id"] == pid)
                if st == 200:
                    save_html(rel, pid, r.get("html") or "")
                    new_pages[pid] = page_entry(p, r.get("etag"))
                    stats["changed"] += 1
                    stats["cond_changed"] += 1
                    # true signal: among the pages the ETag reported as changed, does
                    # lm move along — used to judge whether the timestamp field can be
                    # trusted (only if all of them move can timestamp mode be suggested)
                    old_lm = (old_pages.get(pid) or {}).get("lastModifiedDateTime")
                    new_lm = p.get("lastModifiedDateTime")
                    if old_lm and new_lm and old_lm != new_lm:
                        stats["lm_moved"] += 1
                    log(f"    ✎ changed: {rel} / {p.get('title','')[:30]}")
                elif st == 304:
                    stats["not304"] += 1
                    new_pages[pid] = page_entry(p, etag0)   # unchanged, keep the old etag
                elif st == 404:
                    removed.append(pid)
                    stats["removed"] += 1
                    log(f"    🗑 404: {rel} / {p.get('title','')[:30]} page deleted")
                else:
                    fetch_err += 1
                    log(f"    ✗ conditional GET {rel} / {p.get('title','')[:30]}: HTTP {st} (old entry kept)")
        # 3) removed-page cleanup (manifest + cache)
        for pid in removed:
            if pid in old_pages:
                log(f"    🧹 removing deleted page: {rel} / {old_pages[pid].get('title','')[:30]}")
            new_pages.pop(pid, None)
            fp = os.path.join(CACHE_DIR, sanitize(rel), sanitize(pid) + ".html")
            if os.path.exists(fp):
                os.remove(fp)

        # 4) update the manifest section (list order kept = insertion order)
        prev[rel] = {"id": sid, "lastModifiedDateTime": lm, "pages": new_pages}
        if fetch_err:
            log(f"  ⚠ {rel}: {fetch_err} page(s) failed to fetch (old entries kept, retried next round)")
            stats["fetch_err"] += fetch_err

    # skipped convergence: drop the ones gone or readable again (already removed in
    # the sync loop, this only writes the survivors back)
    m["skipped"] = list(skipped_map.values())

    # ---- disappeared-section convergence (full sync only; a partial --section sync
    # leaves other sections alone) ----
    if not args.section:
        enum_rels = {t[0] for t in secs}   # every rel enumerated this round (including new names after a rename)
        gone = []
        for rel, sec in prev.items():
            if isinstance(sec, dict) and sec.get("id"):
                # has an id: compare against the id set enumerated this round (an id
                # never changes across a rename migration, so nothing is hit by mistake)
                if sec["id"] not in seen_ids:
                    gone.append(rel)
            else:
                # old/odd entries without an id: absent from this round's rel set
                # means gone
                if rel not in enum_rels:
                    gone.append(rel)
        for rel in gone:
            sec = prev.get(rel)
            sec_id = sec.get("id") if isinstance(sec, dict) else None
            log(f"🕳 section disappeared: {rel!r}" + (f" (id={sec_id})" if sec_id else "")
                + " → removed from the manifest (cache/store directories cleaned up as well)")
            prev.pop(rel, None)
            m["skipped"] = [x for x in m.get("skipped", []) if x.get("rel") != rel]
            if not args.dry_run:
                import shutil
                cache_p = os.path.join(CACHE_DIR, sanitize(rel))
                if os.path.isdir(cache_p):
                    shutil.rmtree(cache_p)
                store_p = os.path.join(STORE_DIR, rel)
                if os.path.isdir(store_p):
                    shutil.rmtree(store_p)
            stats["gone_sections"] += 1

    if args.dry_run:
        # a dry run only previews, it rewrites no state
        log("(--dry-run, manifest not written)")
        return

    m["last_sync"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    m["detect_mode"] = args.mode
    save_manifest(m)

    # summary
    log("")
    log(f"sections: synced {stats['sync_sections']} / skipped {stats['skip_sections']}"
        + (f" / renamed {stats['renamed_sections']}" if stats["renamed_sections"] else "")
        + (f" / gone {stats['gone_sections']}" if stats["gone_sections"] else ""))
    log(f"pages: conditional GET {stats['cond']} (304 unchanged {stats['not304']}), plain {stats['plain']}, "
        f"content changed {stats['changed']}, removed {stats['removed']}")
    if stats["cond_changed"] and stats["lm_moved"] == stats["cond_changed"]:
        log(f"💡 all {stats['cond_changed']} pages the ETag reported as changed moved lm too — the timestamp "
            f"field is trustworthy, --mode timestamp can be used again (fewer requests)")
    elif stats["cond_changed"]:
        log(f"ℹ of the {stats['cond_changed']} pages the ETag reported as changed only {stats['lm_moved']} moved lm"
            f" — the timestamp field still cannot be fully trusted, staying in etag mode")
    if stats["fetch_err"]:
        log(f"✗ {stats['fetch_err']} page(s) failed to fetch (old entries kept, retried next round) — this sync is incomplete")
        sys.exit(1)
    log(f"done → {CACHE_DIR}/ , manifest updated (detect_mode={m['detect_mode']})")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        sys.exit(130)
