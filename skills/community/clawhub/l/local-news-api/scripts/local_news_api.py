#!/usr/bin/env python3
"""
local_news_api.py, a READ-ONLY client for a Communities News newsroom's public API.
Example: Alaska News at alaskanews.com, whose API is https://alaskanews.com/api/v1.

For external creators (community journalists, bloggers, civic writers) to pull
published articles, meeting transcripts, public events, and prior-coverage RAG
into their OWN work. It never writes back to the platform: submitting content
back to the newsroom is a separate, editor-authenticated workflow, not this tool.

DEFAULTS to alaskanews.com, which is the only newsroom live on this platform
today. It is not limited to it: set NEWS_SITE and NEWS_COMMUNITY to point it at
another one. Nothing about a market is compiled in.

Terms of use are READ FROM THE NEWSROOM, per request, never assumed: robots.txt
`Content-Signal` first (contentsignals.org), then llms.txt. Every mode's output
carries them, because the person running this is republishing someone else's
reporting, and the attribution is the consideration for using it. If the terms
cannot be read, the output says so instead of inventing them.

## HATEOAS: every output points onward

The API and this client both follow a HATEOAS discipline: every response tells you
where to go next, so no external map is needed.

- CONSUMING the server's: API responses carry a `next_steps` array
  (`{rel, method, href, description}`). Non-JSON output surfaces them; `--json`
  passes them through in the payload for machine consumers.
- EMITTING our own: every mode ends with prioritized Next steps (with the WHY),
  the related modes, and a See also. No dead ends. Errors carry recovery paths.

## Auth: your own key, and only what it reaches

Each user supplies their OWN `cn_` key (env `COMMUNITIES_NEWS_API_KEY`, or the legacy
`NEWS_DESK_API_KEY` / `ALASKA_DESK_API_KEY`, or a `.env.local`
next to this script). `digest`, `topics` and `tags` need none; `search`/`angles`/`article`/`transcript`
/`events`/`rag`/`communities` need a valid key. `check` reports what YOUR key can
reach by ASKING the server: `GET /api/v1/me` returns a `reachability` block
derived from the platform's own router, so this client no longer carries a
hand-written copy that could go stale. It separates `session_auth_only` (no key
of any role reaches it, so there is nothing to request) from `requires_role` (a
membership you could be granted), which is the distinction a bare 401 destroys.

## Discovery: the five Ws (angles mode)

`angles` scaffolds the five-Ws investigative method for a READ-ONLY consumer. That
method has two modes: MATCHING (rank related coverage) is the server's job and stays
there; DISCOVERY (fix two Ws, expand the rest) is a human workflow of chained
searches, which a thin client CAN scaffold. `angles` fixes two Ws (an intent) and
runs the one framed search that intent implies, then hands back the nested-expansion
plan as next-steps, so the journalist drives depth, not the key's rate limit. See
SKILL.md's "Working the story" section.

Auth + HTTP + env plumbing is inlined below; stdlib only, no dependencies.

    COMMUNITIES_NEWS_API_KEY=cn_...  python3 local_news_api.py search "port of alaska settlement"
    python3 local_news_api.py digest       # no key needed
    python3 local_news_api.py check        # what can my key reach?
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# --- which newsroom this is pointed at ------------------------------------------
#
# The platform behind alaskanews.com is multi-community by design (it maps a host
# to a community), and this client already took `--community` and a base-URL
# override. What kept it Alaska-only was four hard-coded constants, not its
# structure. They are defaults now, so pointing it at another newsroom on the
# same platform is configuration rather than a fork.
#
#     NEWS_SITE=https://<host>          the newsroom (API base is derived from it)
#     NEWS_COMMUNITY=<slug>             default for --community
#     COMMUNITIES_NEWS_API_KEY=cn_...   your key (cn_ is the Communities News prefix)
#     PLATFORM_API_BASE=...             override only if the API is not at /api/v1

DEFAULT_SITE = "https://alaskanews.com"
DEFAULT_COMMUNITY = "alaska-news"
# Kept equal to SKILL.md's metadata.version by a test; it was "1.1" while the
# skill shipped 1.2.0, which is the drift that test exists to stop.
UA = "local-news-api/1.6.2"


def site():
    """The newsroom's origin. One knob: the API base is derived from it."""
    return os.environ.get("NEWS_SITE", DEFAULT_SITE).rstrip("/")


def default_community():
    return os.environ.get("NEWS_COMMUNITY", DEFAULT_COMMUNITY)


def site_host():
    """The configured newsroom's host, for the messages a reader acts on."""
    return urllib.parse.urlparse(site()).netloc or site()


def key_settings_url():
    """Where a reader creates a key: the same account page at every newsroom on
    the platform. These messages named alaskanews.com until 1.6.2, which sent a
    reader of any other newsroom to the wrong site."""
    return f"{site_host()}/profile/settings"


# The key is a Communities News platform key (cn_ is its prefix), so that is its
# name. It was ALASKA_DESK_API_KEY until 1.1 and NEWS_DESK_API_KEY until 1.4, when
# the skill was named for a desk. Renaming without honouring the old names would
# break every existing setup silently, reported as "no key set", so both still work,
# in that order of precedence, and are the only reason this is three names.
# Deliberately not NEWS_API_KEY: newsapi.org users commonly have that set, and this
# client would then send a stranger's key to the newsroom.
KEY_ENV = "COMMUNITIES_NEWS_API_KEY"
LEGACY_KEY_ENV = "NEWS_DESK_API_KEY"
OLDEST_KEY_ENV = "ALASKA_DESK_API_KEY"


def read_key():
    return (os.environ.get(KEY_ENV) or os.environ.get(LEGACY_KEY_ENV)
            or os.environ.get(OLDEST_KEY_ENV) or "")


RELATED_MODES = ("digest · browse · search · angles · brief · article · transcript · events · people · "
                 "person · topics · tags · rag · clip · communities · check")
def see_also():
    host = urllib.parse.urlparse(site()).netloc or site()
    return f"SKILL.md  ·  full API: {host}/docs/api  ·  machine spec: {host}/api/v1/openapi.json"


# --- auth + HTTP + env plumbing (inlined; stdlib only, no dependencies) -------

SCRIPT_DIR = Path(__file__).resolve().parent


def api_base():
    """Derived from NEWS_SITE unless PLATFORM_API_BASE overrides it outright."""
    return os.environ.get("PLATFORM_API_BASE") or f"{site()}/api/v1"


# --- usage terms: read from the newsroom, never assumed ------------------------
#
# This used to be a constant reciting alaskanews.com's stance. That was the same
# defect as the rest of this audit: a claim about the world, baked into source,
# with nothing to notice when it changed. It is worse than the others, because
# every mode prints it under someone else's reporting, and the attribution is the
# consideration for using it. Pointed at a second newsroom, a constant would have
# published Alaska's terms over their work.
#
# Read from robots.txt's `Content-Signal` (contentsignals.org, the canonical
# machine-readable location), falling back to the `key=value` pairs in llms.txt.
# If NEITHER can be read, the client says so rather than inventing terms: a tool
# that cannot read the terms has no business asserting them.
_TERMS_CACHE = {}
_SIGNAL_RE = re.compile(r"([a-z][a-z-]*)\s*=\s*([a-z]+)")


def content_signal(site_url, timeout=10):
    """The newsroom's usage signals as `(signal, source)`, or `(None, None)`.

    `robots.txt`'s `Content-Signal` is the canonical machine-readable location
    and is authoritative here. `llms.txt` is a fallback and is PROSE, so what it
    yields is labelled in the output rather than presented as equivalent.

    Comments are stripped before anything is parsed. Without that, a newsroom
    that had commented a directive OUT still had it read as active policy, which
    on 2026-09-10 turned `# Content-Signal: ai-train=yes` into a printed
    permission to train. The dangerous direction is the permissive one: reading
    `no` as `yes` invites a reader to break terms they were never granted."""
    if site_url in _TERMS_CACHE:
        return _TERMS_CACHE[site_url]
    found = (None, None)
    for path, source in (("/robots.txt", "robots.txt"), ("/llms.txt", "llms.txt")):
        try:
            req = urllib.request.Request(site_url + path, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                text = r.read(65536).decode("utf-8", "replace")
        except Exception:
            continue
        pairs = []
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].strip()  # a commented directive is not policy
            if not line:
                continue
            low = line.lower()
            if source == "robots.txt":
                if not low.startswith("content-signal:"):
                    continue
                scan = low.split(":", 1)[1]
            else:
                # Only a declaration-shaped list item, never free prose.
                m = re.match(r"[-*]\s+`([a-z][a-z-]*=[a-z]+)`", low)
                if not m:
                    continue
                scan = m.group(1)
            for k, v in _SIGNAL_RE.findall(scan):
                if k in ("ai-train", "search", "ai-input") and (k, v) not in pairs:
                    pairs.append((k, v))
        if pairs:
            found = (", ".join(f"{k}={v}" for k, v in pairs), source)
            break
    _TERMS_CACHE[site_url] = found
    return found


def terms_note(origin=None):
    """The line printed under every rendered output.

    Takes the origin the CONTENT came from, which is not always the configured
    newsroom: `article <url>` fetches whatever URL it is handed. Printing the
    configured newsroom's terms over another newsroom's story was the same
    defect as hardcoding them, one level further in."""
    s = (origin or site()).rstrip("/")
    host = urllib.parse.urlparse(s).netloc or s
    signal, source = content_signal(s)
    if not signal:
        return (f"Source: {host}. Its usage terms could NOT be read "
                f"({host}/robots.txt and /llms.txt). Check them yourself before you "
                "publish anything from this, and attribute with a backlink regardless.")
    via = "" if source == "robots.txt" else f" (read from {source}, which is prose; confirm it)"
    note = f"Source: {host}. Per its Content-Signal: {signal}.{via}"
    if "ai-train=no" in signal:
        note += " Do not train on it."
    if "ai-input=yes" in signal:
        note += " Quote with attribution and a backlink."
    return note


# Pseudo-statuses for failures that are not HTTP statuses. Negative so they can
# never collide with a real code.
NON_JSON = -1      # transport worked, payload was not JSON
TIMED_OUT = -2     # API is up, it just did not answer in time
CROSS_ORIGIN = -3  # a 3xx tried to take the credential to another origin
# /rag/query synthesizes an answer over retrieved passages and is far slower than
# every other mode: measured 84s on 2026-09-09, against the 60s default that used
# to cut it off and report "unreachable".
RAG_TIMEOUT = 180


class ApiError(Exception):
    def __init__(self, code, body=""):
        self.code = code
        self.body = body
        super().__init__(f"HTTP {code}: {body[:300]}")


# What a .env in the CURRENT DIRECTORY may set. That directory is whatever project
# the skill happens to run in, so its .env is workspace-controlled: if it could set
# NEWS_SITE or PLATFORM_API_BASE it could choose where your key is sent, and an agent
# working inside an untrusted repository would carry your exported key there. It may
# supply the key and the community, never a destination. Destinations come from your
# real environment or from a .env next to this script, both of which you control.
# Flagged by ClawHub's security scan of 1.3.0 on 2026-09-29, and correctly.
CWD_ENV_ALLOWED = frozenset({KEY_ENV, LEGACY_KEY_ENV, OLDEST_KEY_ENV, "NEWS_COMMUNITY"})
_IGNORED_NOTICES = set()  # _load_env runs more than once per command; say it once


def _load_env():
    """Read KEY=VALUE lines from .env / .env.local next to this script OR in the
    current directory, without overriding anything already set in the environment.
    Checking both means the key file is found whether you run from the script's
    folder or from your project root. A current-directory file is restricted to
    CWD_ENV_ALLOWED, and anything else it tries to set is named on stderr."""
    seen = set()
    script_dir = SCRIPT_DIR.resolve()
    for d in (SCRIPT_DIR, Path.cwd()):
        workspace = d.resolve() != script_dir
        for name in (".env", ".env.local"):
            p = (d / name).resolve()
            if p in seen or not p.exists():
                continue
            seen.add(p)
            # utf-8 explicitly: read_text() otherwise uses the platform's preferred
            # encoding, which on Windows is a code page rather than utf-8, so a key
            # file with any non-ascii byte in it decodes differently per machine.
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip()
                # Quoted values keep their content verbatim, including a #.
                # Unquoted ones lose an inline comment, which otherwise ends up
                # INSIDE the key: `KEY=cn_x  # mine` was parsed as the literal
                # value "cn_x  # mine" and every request failed on a credential
                # that looked right in the file.
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                else:
                    v = v.split(" #", 1)[0].split("\t#", 1)[0].strip()
                k = k.strip()
                if workspace and k not in CWD_ENV_ALLOWED:
                    if k in ("NEWS_SITE", "PLATFORM_API_BASE") and (p, k) not in _IGNORED_NOTICES:
                        _IGNORED_NOTICES.add((p, k))
                        print(f"Ignored {k} from {p}: a project's .env can supply your key but "
                              "not choose where it is sent. Export it, or put it in a .env "
                              "next to local_news_api.py.", file=sys.stderr)
                    continue
                os.environ.setdefault(k, v)


def get_api_key():
    _load_env()
    key = read_key()
    if not key:
        print(f"Error: {KEY_ENV} not set.", file=sys.stderr)
        print(f"Create a key at {key_settings_url()}, then set it:", file=sys.stderr)
        print(f"  export {KEY_ENV}=cn_...", file=sys.stderr)
        print(f"  # or: echo '{KEY_ENV}=cn_...' >> .env.local  (next to this script)", file=sys.stderr)
        sys.exit(2)
    return key


def _origin(url):
    u = urllib.parse.urlsplit(url)
    return (u.scheme, u.hostname, u.port or (443 if u.scheme == "https" else 80))


class _SameOriginOnly(urllib.request.HTTPRedirectHandler):
    """Refuse to carry the API key across origins on a redirect.

    urllib follows 3xx by default and rebuilds the request with the headers it
    was given, `Authorization` included. It does not care that the new URL is a
    different host, or that it is plain http when the first hop was https. So
    anything able to answer for the configured newsroom, or to sit in front of
    it, can collect a reader's key with one redirect. Reproduced 2026-09-10: a
    302 to a second local origin received `Bearer cn_...` intact.

    Refusing rather than quietly stripping the header, because a newsroom API
    that redirects a JSON GET to another origin is not a thing this client
    should paper over: the 401 that stripping would produce reads as a key
    problem, which is exactly the wrong place to send the reader."""

    def __init__(self, origin):
        self.origin = origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if _origin(newurl) != self.origin:
            raise ApiError(
                CROSS_ORIGIN,
                f"{req.full_url} redirected to a different origin ({newurl}); "
                "refused rather than send your API key there")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _auth_header(public):
    """The Authorization header a request should carry, or none.

    A public endpoint gets NO credential, even when a key is set. It buys nothing
    there, and a key sent where it is not needed is a key sent to one more place
    than necessary; a wrong-prefix key would also turn a public read into a 401.
    Only endpoints verified to answer without a key are marked public: /tags was,
    on 2026-09-29, and the platform's OpenAPI spec lists it with no security."""
    if public:
        return {}
    return {"Authorization": f"Bearer {get_api_key()}"}


def api_request(method, path, params=None, body=None, timeout=60, public=False):
    base = api_base()
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    headers = {
        **_auth_header(public),
        "Accept": "application/json",
        "User-Agent": UA,
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(_SameOriginOnly(_origin(url)))
    try:
        with opener.open(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        raise ApiError(e.code, e.read().decode("utf-8", "replace"))
    except (TimeoutError, socket.timeout):
        # NOT the same as unreachable, and saying "unreachable" sends the reader
        # to check their network when the API is up and merely slow. /rag/query
        # synthesizes an answer and measured 84s on 2026-09-09.
        raise ApiError(TIMED_OUT, f"{path} did not answer within {timeout}s")
    except urllib.error.URLError as e:
        if isinstance(e.reason, (TimeoutError, socket.timeout)):
            raise ApiError(TIMED_OUT, f"{path} did not answer within {timeout}s")
        raise ApiError(0, f"unreachable: {e.reason}")
    # Not every 200 on this API is JSON: /clips/<id>/stream 302s to an MP4 in
    # storage, and a proxy or captive portal can return HTML. Decoding those as
    # JSON used to raise UnicodeDecodeError/JSONDecodeError straight through
    # ApiError's net and print a traceback. Fail like every other error here:
    # a status, a why, and a recovery.
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ApiError(NON_JSON, f"{path} returned {len(raw)} bytes that are not JSON")


def api_redirect(path, timeout=30):
    """Resolve a redirecting endpoint to its target WITHOUT following it.

    `/clips/<id>/stream` 302s to a public MP4. Following that gets you video
    bytes, which is not something a research client can render; the useful
    answer is the URL itself, which the caller can hand to a player or curl."""
    base = api_base()
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **kw):
            return None

    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {get_api_key()}", "User-Agent": UA})
    try:
        with opener.open(req, timeout=timeout) as r:
            # No redirect: the endpoint answered directly (an error body, say).
            return {"status": r.status, "location": None,
                    "body": r.read(4096).decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308):
            loc = e.headers.get("Location")
            # Location may legally be relative; a caller needs something it can
            # actually fetch, so resolve it against the request URL.
            return {"status": e.code,
                    "location": urllib.parse.urljoin(url, loc) if loc else None,
                    "body": ""}
        raise ApiError(e.code, e.read().decode("utf-8", "replace"))
    except urllib.error.URLError as e:
        raise ApiError(0, f"unreachable: {e.reason}")


# The eight corpora /search queries. Verified against the live API 2026-09-09;
# `search --corpus <name>` with a name outside this set returns nothing.
# external_documents and social_post are editor/admin only: naming one explicitly
# is a 403, omitting --corpus drops them silently and returns the rest.
CORPORA = ("articles", "users", "tags", "transcripts", "speakers", "events",
           "external_documents", "social_post")
RESTRICTED_CORPORA = frozenset({"external_documents", "social_post"})


def _check_corpora(spec):
    """Reject a corpus name the API does not have, and warn before asking for one
    it gates.

    A typo used to travel all the way to the server and come back as an empty
    result set, which reads exactly like "no coverage exists" and is the single
    most misleading answer a research tool can give a reporter."""
    asked = [c.strip() for c in spec.split(",") if c.strip()]
    unknown = [c for c in asked if c not in CORPORA]
    if unknown:
        sys.exit(
            f"Unknown corpus: {', '.join(unknown)}.\n"
            f"  Valid: {', '.join(CORPORA)}\n"
            "  Why this matters: an unknown name returns an empty result set, which looks\n"
            "  identical to 'nothing has been published about this'."
        )
    gated = [c for c in asked if c in RESTRICTED_CORPORA]
    if gated:
        print(f"Note: {', '.join(gated)} is editor/admin only and will 403 for a consumer key. "
              "Omit --corpus to have it dropped silently instead.", file=sys.stderr)


def _add_paging(p, default_limit):
    """Every list endpoint answers {data, count, offset, limit, has_more}. Without
    --offset a caller can only ever see the first page, and has_more becomes a
    fact the tool states but cannot act on."""
    p.add_argument("--limit", type=int, default=default_limit)
    p.add_argument("--offset", type=int, default=0, help="skip this many (paging)")


def _add_date_range(p):
    """The When axis. /search grew date_from/date_to on 2026-08-14, which is the
    only one of the five Ws the server can filter on, and the axis `angles`
    intents talk about holding or expanding. Shared so search and angles cannot
    drift apart on it."""
    p.add_argument("--since", metavar="YYYY-MM-DD", help="only results on/after this date (When axis)")
    p.add_argument("--until", metavar="YYYY-MM-DD", help="only results on/before this date (When axis)")


def _date_params(args):
    """Map --since/--until onto the API's date_from/date_to, omitting unset ones."""
    out = {}
    if getattr(args, "since", None):
        out["date_from"] = args.since
    if getattr(args, "until", None):
        out["date_to"] = args.until
    return out


# The two-axis grid from the five-Ws investigative method, as a sourcing scaffold.
# Each intent FIXES two Ws and names (fixed axes prose, expand prose, corpora to
# pull). One framed /search call, not a fan-out: the nesting is handed back as
# next-steps so the journalist drives depth.
INTENTS = {
    #            fixed axes                    expand (context)   corpora
    "similar":   ("What + Why",               "When + Where",     "articles"),
    "precedent": ("What + Why (ignore When)",  "When",            "articles,transcripts"),
    "track":     ("Who + What",               "When",            "articles,transcripts"),
    "local":     ("Where + What",             "Who",             "articles,events,transcripts"),
    "angle":     ("Why + What",               "Who",             "articles"),
}


# --- HATEOAS -----------------------------------------------------------------

def _server_next_steps(resp) -> list:
    """The API's OWN next_steps, wherever it put them (top level or under data).
    The API uses `next_steps: [{rel, method, href, description}]`."""
    if not isinstance(resp, dict):
        return []
    ns = resp.get("next_steps")
    if not ns and isinstance(resp.get("data"), dict):
        ns = resp["data"].get("next_steps")
    out = []
    for s in (ns or []):
        if isinstance(s, dict):
            rel = s.get("rel") or s.get("action") or ""
            method = s.get("method") or "GET"
            href = s.get("href") or ""
            desc = s.get("description") or ""
            out.append(f"{method} {href}  ({rel}){(' - ' + desc) if desc else ''}".strip())
        else:
            out.append(str(s))
    return out


def _skill_next_steps(mode, args, has_key, state=None) -> list:
    """State-driven next actions for THIS skill: (action, why). Priority order,
    capped at 5 by the caller. State shows up as `has_key` and per-mode context."""
    if mode == "digest":
        steps = []
        if not has_key:
            steps.append((f"echo '{KEY_ENV}=cn_...' >> .env.local ; then `check`",
                          "digest, topics and tags need no key; a key unlocks search, brief, "
                          "transcripts and the rest"))
        if getattr(args, "date", None):
            steps += [
                ("article <slug from a story above>", "read one in full, and cite the article, not this summary"),
                ('brief "<topic from a story above>"',
                 "turn a story into a research brief: prior coverage, the record, who is on it"),
                ("digest --date <the day before>", "step back a day"),
            ]
        else:
            steps.append(("digest --date today", "today's stories with a one-line summary each"))
        steps += [
            ('search "<topic from a headline above>"',
             "internal before external: confirm what the newsroom already has before you write"),
        ]
        return steps
    if mode == "check":
        if not has_key:
            return [(f"set {KEY_ENV}, then re-run `check`",
                     "digest, topics and tags work without a key; the rest report their reach once one is set")]
        # Read the probe results rather than assuming they passed. This block
        # used to congratulate the reader on reaching search immediately after
        # every request had been refused.
        surfaces = (state or {}).get("surfaces", {})
        reached = {k for k, v in surfaces.items() if v == "OK"}
        rejected = [v for v in surfaces.values() if str(v).startswith("rejected")]
        if rejected and not (reached - {"digest (public)"}):
            return [("replace the key, then re-run `check`",
                     "every keyed request was refused, so there is nothing to try until it works"),
                    ("digest", "digest needs no key and still works")]
        steps = []
        if "search" in reached:
            steps.append(('search "<topic>"', "your key reached search; start there"))
            steps.append(('angles "<topic>" --intent similar', "or work a story across the five Ws"))
        if "calendar (events)" in reached:
            steps.append(("events --days 14", "your key reached the calendar; see what is coming up"))
        if not steps:
            steps.append(("digest", "the keyed surfaces did not answer; digest needs no key"))
        return steps[:5]
    if mode == "search":
        return [
            ("article <id from a result above>", "open a match's full body to quote (hold What: this is your story)"),
            ('rag "<same topic>"', "expand What+Why across time, ignore When: prior coverage + precedent"),
            ('angles "<topic>" --intent similar', "widen into discovery: fix two Ws, expand the rest"),
            ('search "<topic>" --corpus transcripts', "shift to the public record (the When/Where axis)"),
        ]
    if mode == "article":
        return [
            ('rag "<this article\'s topic>"', "gather supporting quotes and prior coverage (What+Why, varying When)"),
            ('angles "<topic>" --intent track', "work the actor as a beat: fix Who+What, expand When"),
            ('search "<a related angle>"', "find sibling stories to cite as 'previously reported'"),
        ]
    if mode == "transcript":
        return [('search "<meeting topic>" --corpus articles', "find the article(s) that covered this meeting"),
                ("events", "the When axis: what other public meetings are upcoming"),
                ('angles "<meeting topic>" --intent local', "fix Where+What: the local landscape around it")]
    if mode == "events":
        return [('search "<an event\'s topic>" --corpus articles,transcripts',
                 "get the coverage and the record for a specific event"),
                ('angles "<topic>" --intent track', "fix Who+What on the convening body; expand When")]
    if mode == "rag":
        return [("article <id from a quote's source>", "open the article a quote came from"),
                ('angles "<topic>" --intent angle', "fix Why+What: who else deploys this framing"),
                ('search "<topic>"', "widen beyond the RAG hits")]
    if mode == "brief":
        return [
            ("article <url or id from Prior coverage>", "read what you will cite in full before you cite it"),
            ("transcript <source id from the record>", "the whole meeting, not just the matching excerpt"),
            ('person <id from On the record>', "everything a person appears in, marked where they are quoted"),
            ("events --days 30", "what is still coming up that you could attend or file comment on"),
        ]
    if mode == "angles":
        # Discovery is nested: one intent fixes two Ws; the next steps expand a
        # free axis or pivot the fixed pair. Placeholders (not the live seed) match
        # the house style of the other modes and keep this args-free.
        return [
            ("article <id from a hit above>",
             "open a match: a SECOND axis agreeing makes it relevant; an independent source makes it confirmed"),
            ('rag "<seed>"',
             "expand What+Why across time (ignore When): prior coverage and precedent"),
            ('angles "<seed>" --intent track   (or: local, precedent, angle)',
             "pivot the fixed pair: each intent fixes a different two Ws and expands the rest"),
        ]
    if mode == "people":
        return [("person <id from a row above>",
                 "open the actor: their record plus every article that quotes them"),
                ('angles "<their name>" --intent track',
                 "work them as a beat: fix Who+What, expand When"),
                ('search "<their name>" --corpus transcripts',
                 "hear them in the public record rather than in coverage")]
    if mode == "person":
        return [("article <id from the coverage above>",
                 "open a story the quote came from, to cite it rather than the excerpt"),
                ('angles "<their name>" --intent track',
                 "fix Who+What and expand When: the actor as a running beat"),
                ("browse --tag <a tag from their coverage>",
                 "widen from the person to the subject they keep appearing in")]
    if mode == "topics":
        return [("browse --tag <slug from above>", "read what has actually been published on one beat"),
                ('tags "<word>" --category organization',
                 "or find the agencies and bodies that coverage is filed under"),
                ('search "<topic name>"', "or go straight to a query inside the beat")]
    if mode == "tags":
        return [("browse --tag <slug from above>", "that tag's coverage, newest first"),
                ("topics", "or step back to the beats, ranked by how much each holds"),
                ('angles "<tag name>" --intent local', "fix Where+What around it")]
    if mode == "browse":
        return [("article <id from a row above>", "open one in full"),
                ('search "<something you noticed>"',
                 "switch from what EXISTS to what MATCHES, once you have a lead"),
                ("browse --sort top --window week",
                 "or re-cut the same list by what readers actually read")]
    if mode == "communities":
        return [('search "<topic>" --community <slug from above>',
                 "point the read surface at a specific community"),
                ("digest", "or stay on the default community's recent stories")]
    if mode == "clip":
        return [("transcript <source-id>", "read the full transcript the clip was cut from"),
                ("curl -o clip.mp4 '<the url above>'", "the id resolves to a public MP4; nothing here downloads it")]
    return []


def _print_hateoas(mode, args, resp=None, state=None):
    """The CLI HATEOAS footer: surface the server's next_steps, then this skill's,
    then related modes + see-also. Never called in --json mode (machine consumers
    read next_steps from the payload)."""
    has_key = bool(read_key())
    server = _server_next_steps(resp)
    if server:
        print("\nThe API points onward to:")
        for s in server[:5]:
            print(f"  {s}")
    steps = _skill_next_steps(mode, args, has_key, state)
    if steps:
        print("\nNext steps:")
        for action, why in steps[:5]:
            print(f"  {action}")
            print(f"      {why}")
    print(f"\nRelated modes: {RELATED_MODES}")
    print(f"See also: {see_also()}")


# --- helpers ----------------------------------------------------------------

def fetch_markdown(url: str, timeout: int = 30) -> str:
    """Public markdown surface (no key): the homepage digest and per-article body."""
    req = urllib.request.Request(url, headers={"Accept": "text/markdown", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raise ApiError(e.code, e.read().decode("utf-8", "replace"))
    except urllib.error.URLError as e:
        raise ApiError(0, f"unreachable: {e.reason}")


def _guided(fn):
    """Run an api_request-using command and translate auth failures into recovery
    a consumer can act on (HATEOAS error discipline), not a raw HTTP body."""
    try:
        return fn()
    except ApiError as e:
        if e.code == 401:
            key = read_key()
            if key and not key.startswith("cn_"):
                sys.exit(
                    f"Not authorized (401). Your key starts with {key[:4]!r}, but Communities News API "
                    "keys start with 'cn_' (cn_ + 40 hex).\n"
                    "  That looks like a key for a different service. Recovery: create a key at "
                    f"{key_settings_url()} and put it in a .env.local next to this script."
                )
            sys.exit(
                f"Not authorized (401). This mode needs your API key for {site_host()} (starts with 'cn_').\n"
                f"  Recovery: echo '{KEY_ENV}=cn_...' >> .env.local\n"
                "  Then: python3 local_news_api.py check\n"
                f"  Get a key at {key_settings_url()}."
            )
        if e.code == 403:
            sys.exit(
                "Forbidden (403). Your key is valid but its role does not permit this.\n"
                "  Why: the external_documents and social_post search corpora are editor/admin "
                "only. Asking for them by name is a 403; leaving --corpus off drops them silently "
                "and returns the rest.\n"
                "  Recovery: run `check` to see your reach, and stay on "
                "articles/transcripts/events/tags/speakers/users, which any valid key reaches."
            )
        if e.code == TIMED_OUT:
            sys.exit(
                f"Timed out ({e.body}).\n"
                "  Why: the API is reachable but slow for this query; `rag` synthesizes an\n"
                "  answer over retrieved passages and routinely takes over a minute.\n"
                "  Recovery: narrow the query, or re-run: nothing was written, so a retry is safe."
            )
        if e.code == CROSS_ORIGIN:
            sys.exit(
                f"Refused a cross-origin redirect ({e.body}).\n"
                "  Why: your API key would have been sent to a host that is not the newsroom\n"
                "  you configured. Nothing was sent.\n"
                "  Recovery: check NEWS_SITE and PLATFORM_API_BASE for a value you did not set."
            )
        if e.code == NON_JSON:
            sys.exit(
                f"Unexpected non-JSON response ({e.body}).\n"
                "  Why: usually a proxy or captive portal answering instead of the API.\n"
                f"  Recovery: confirm you can reach {site_host()}, then re-run `check`."
            )
        if e.code == 429:
            sys.exit("Rate limited (429). Recovery: back off ~a minute; the API allows 300 reads/min per user.")
        raise


def _emit(obj, args, render=None, mode=""):
    """Single output point for keyed modes. JSON: valid JSON only (its own
    next_steps are the HATEOAS for machines). Markdown: rendered data + the CLI
    HATEOAS footer + the license reminder."""
    if args.json:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
        return
    print(render(obj) if render else json.dumps(obj, indent=2, ensure_ascii=False))
    if mode:
        _print_hateoas(mode, args, obj)
    print(f"\n---\n{terms_note()}")


# --- modes ------------------------------------------------------------------

# --- digest --date: one day's stories, read from the public feed ----------------
#
# GET /api/v1/feed answers without a key (/articles does not), so a keyless daily
# briefing comes from it. Since the platform fix of 2026-09-30 it filters by
# `community` (a slug; an unknown one is a 404), takes `published_after`
# (inclusive) and `published_before` (exclusive) as ISO 8601, reports the
# newsroom's own time zone as `community.timezone` when one newsroom is in scope,
# and pages exactly: `has_more` is true only when another page exists, and the
# `next_page` link in `next_steps` carries `as_of` so every story lands on exactly
# one page. So a day is one window query, paged by following that link.
#
# The feed's ORDER is still ranked, deliberately, so the day comes from the date
# parameters, never from the order. And the client still checks that the rows it
# got are the ones it asked for, because a server that ignores a filter answers
# with a list that looks like a filtered one.
FEED_PAGE = 100
FEED_PAGE_CAP = 20      # 2,000 stories: far past any real day, a guard against a runaway link

_TS_RE = re.compile(r"(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)(?::(\d\d)(?:\.(\d+))?)?"
                    r"\s*(Z|[+-]\d\d:?\d\d)?$")


def _parse_ts(value):
    """An API timestamp as an aware UTC datetime, or None. Written by hand because
    Python 3.9's fromisoformat, this client's floor, rejects fractional seconds
    with trailing zeros trimmed ("19:12:56.45725+00:00"), which the API emits.
    No offset is read as UTC."""
    if isinstance(value, (int, float)):
        secs = value / 1000 if value > 1e11 else value
        return _dt.datetime.fromtimestamp(secs, _dt.timezone.utc)
    m = _TS_RE.match(str(value or "").strip())
    if not m:
        return None
    y, mo, d, h, mi, s, frac, off = m.groups()
    ts = _dt.datetime(int(y), int(mo), int(d), int(h), int(mi), int(s or 0),
                      int((frac or "0")[:6].ljust(6, "0")), tzinfo=_dt.timezone.utc)
    if off and off != "Z":
        sign = 1 if off[0] == "+" else -1
        ts -= sign * _dt.timedelta(hours=int(off[1:3]), minutes=int(off[-2:]))
    return ts


def _utc_iso(ts):
    return ts.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _feed_zone(community):
    """The newsroom's time zone as the public feed reports it, or None."""
    resp = api_request("GET", "/feed", {"community": community, "limit": 1}, public=True)
    return ((resp.get("community") or {}).get("timezone")) if isinstance(resp, dict) else None


def _day_zone(explicit, reported):
    """(tzinfo, name, note) for counting days. An explicit --tz that does not exist
    is an error. The newsroom's reported zone missing from this machine's tz
    database, or no zone reported at all, falls back to UTC, and the note says so."""
    name = explicit or reported
    if not name:
        return (_dt.timezone.utc, "UTC", "Days are counted in UTC: the newsroom did not report "
                "its time zone. Pass --tz <Area/City> for local days.")
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name), name, ""
    except Exception:
        if explicit:
            sys.exit(f"Unknown time zone {explicit!r}. Use an IANA name such as America/Anchorage.")
        return (_dt.timezone.utc, "UTC", f"Days are counted in UTC: the time zone {name} is not "
                "available on this machine (no tz database; `pip install tzdata` adds one).")


def _parse_day(text, tz):
    """--date as a calendar date. `today` and `yesterday` are in the day's zone."""
    today = _dt.datetime.now(tz).date()
    if text in ("today", "yesterday"):
        return today - _dt.timedelta(days=text == "yesterday")
    try:
        return _dt.date.fromisoformat(text)
    except ValueError:
        sys.exit(f"--date takes YYYY-MM-DD, today or yesterday, not {text!r}.")


def _next_page_params(resp):
    """The query of the feed's own next_page link, which carries as_of."""
    for step in (resp.get("next_steps") or []):
        if isinstance(step, dict) and step.get("rel") == "next_page" and step.get("href"):
            return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(step["href"]).query))
    return None


def _read_day_from_feed(day, tz, community):
    """Every story published on `day` in `tz`: one window query on the public feed,
    paged by its next_page link. Returns the list envelope, or the first non-list
    response untouched so the renderer can fall back to it."""
    start = _dt.datetime.combine(day, _dt.time(), tz)
    end = _dt.datetime.combine(day + _dt.timedelta(days=1), _dt.time(), tz)
    params = {"community": community, "published_after": _utc_iso(start),
              "published_before": _utc_iso(end), "limit": FEED_PAGE}
    rows, seen, pages = [], set(), 0
    while True:
        resp = api_request("GET", "/feed", params, public=True)
        data = resp.get("data") if isinstance(resp, dict) else None
        if not isinstance(data, list):
            return resp
        if "as_of" not in resp:
            sys.exit("This newsroom's feed predates date filtering (its response carries no "
                     "`as_of`), so `digest --date` cannot ask it for one day. Use `digest`.")
        pages += 1
        for r in data:
            if not isinstance(r, dict):
                continue
            pub = _parse_ts(r.get("published_at"))
            slug = (r.get("communities") or {}).get("slug")
            if (pub and not (start <= pub < end)) or (slug and slug != community) or r.get("id") in seen:
                sys.exit("The feed answered with stories outside what was asked for (another day, "
                         "another newsroom, or a repeat), so its filters or paging were not applied. "
                         "Nothing is printed rather than a wrong day.")
            seen.add(r.get("id"))
            if r.get("status") in (None, "published"):
                rows.append(r)
        if not resp.get("has_more"):
            return {"data": rows, "pages": pages, "complete": True}
        nxt = _next_page_params(resp)
        if nxt is None or pages >= FEED_PAGE_CAP:
            return {"data": rows, "pages": pages, "complete": False}
        params = nxt


def _day_story(r, tz, community):
    pub = _parse_ts(r.get("published_at"))
    slug = r.get("slug")
    comm = (r.get("communities") or {}).get("slug") or community
    return {"id": r.get("id"), "title": r.get("title"), "tldr": r.get("tldr") or r.get("excerpt"),
            "location": r.get("location"), "story_type": r.get("story_type"),
            "published_at": r.get("published_at"),
            "local_time": pub.astimezone(tz).strftime("%H:%M") if pub else None,
            "url": f"{site()}/c/{comm}/{slug}" if slug else None}


def cmd_digest_day(args):
    """One day's stories with a one-line summary each: the daily briefing. Public."""
    reported = None if args.tz else _guided(lambda: _feed_zone(args.community))
    tz, tz_name, tz_note = _day_zone(args.tz, reported)
    day = _parse_day(args.date, tz)
    resp = _guided(lambda: _read_day_from_feed(day, tz, args.community))
    rows = resp.get("data") if isinstance(resp, dict) else None
    if not isinstance(rows, list):
        _emit(resp, args, None, mode="digest")
        return
    stories = sorted((_day_story(r, tz, args.community) for r in rows),
                     key=lambda s: s["published_at"] or "", reverse=True)
    note = "Read from the public feed, no key."
    if not resp.get("complete"):
        note += (f" Stopped after {resp.get('pages')} pages without reaching the end of the day, "
                 "so stories may be missing.")
    if args.json:
        print(json.dumps({"date": day.isoformat(), "time_zone": tz_name, "stories": stories,
                          "pages": resp.get("pages"), "complete": resp.get("complete"),
                          "note": " ".join(x for x in (tz_note, note) if x)}, ensure_ascii=False))
        return
    name = urllib.parse.urlsplit(site()).netloc or site()
    for r in rows:
        name = (r.get("communities") or {}).get("name") or name
        break
    out = [f"# {name}, {day.strftime('%A')} {day.isoformat()}: {len(stories)} "
           f"{'story' if len(stories) == 1 else 'stories'}  (times in {tz_name})"]
    if not stories:
        out.append(f"\nNo stories published on {day.isoformat()}.")
    for s in stories:
        where = f"  ({s['location']})" if s.get("location") else ""
        out.append(f"\n- {s.get('local_time') or '--:--'}  **{str(s.get('title') or '(untitled)').strip()}**{where}")
        if s.get("tldr"):
            out.append(f"  {str(s['tldr']).strip()[:320]}")
        if s.get("url"):
            out.append(f"  {s['url']}")
    out.append("\n" + " ".join(x for x in (tz_note, note) if x))
    print("\n".join(out))
    _print_hateoas("digest", args, None)
    print(f"\n---\n{terms_note()}")


# --- brief: a research brief before writing -------------------------------------

# Sections in the order a writer needs them. Each corpus is one /search corpus
# any valid key reaches; the editor-only ones (external_documents, social_post)
# are never requested by name, so the server leaves them out rather than refusing.
BRIEF_SECTIONS = (
    ("articles", "Prior coverage", "Cite the article itself, by its URL."),
    ("transcripts", "The public record: meeting and hearing transcripts",
     "Quote verbatim, and name the meeting; open it with `transcript <source id>`."),
    ("speakers", "On the record: people", "Check names and spellings against these before you use one."),
    ("events", "Meetings, hearings and deadlines", "What is coming up, or just happened, on this story."),
    ("tags", "Beats and subjects", "A slug here works with `browse --tag` for the rest of the coverage."),
)

BRIEF_BLANKS = (
    ("Why it matters", "One sentence: this matters because [the larger local story, pattern or "
     "decision]. If you cannot write it from what is above, the piece will read as a press release."),
    ("Whose voice is missing", "Name one person or group this does not hear from, and where you "
     "looked for them (the transcripts and people above first)."),
    ("What you will cite", "The articles and transcripts above you will actually cite, by URL or id. "
     "Cite a specific piece, never \"previously reported\"."),
    ("Premise check", "Is the premise of the story true on the record? Check dates (published is not "
     "when it happened), names, and the primary document, not a summary of it."),
)


def _brief_item(corpus, it, community):
    """One brief entry: a headline line plus up to two detail lines."""
    lines = []
    if corpus == "articles":
        when = (it.get("published_at") or "")[:10]
        lines.append(f"- **{str(it.get('title') or '(untitled)').strip()}**" + (f" ({when})" if when else ""))
        comm = (it.get("communities") or {}).get("slug") or community
        if it.get("slug"):
            lines.append(f"  {site()}/c/{comm}/{it['slug']}")
        excerpt = it.get("excerpt") or it.get("description") or it.get("tldr")
        if excerpt:
            lines.append(f"  {str(excerpt).strip()[:200]}")
    elif corpus == "transcripts":
        lines.append(f"- **{it.get('speaker') or 'unidentified speaker'}** in "
                     f"*{it.get('source_title') or 'a meeting'}*  [transcript {it.get('source_id') or '?'}]")
        if it.get("content"):
            lines.append(f"  \"{str(it['content']).strip()[:260]}\"")
    elif corpus == "speakers":
        name = it.get("display_name") or it.get("name") or it.get("slug") or "?"
        tail = ", ".join(x for x in (it.get("role"), it.get("organization")) if x)
        lines.append(f"- **{name}**" + (f": {tail}" if tail else "") + (f"  [{it.get('id')}]" if it.get("id") else ""))
    elif corpus == "events":
        when = (it.get("event_date") or "")[:10]
        tail = ", ".join(x for x in (it.get("event_location"), it.get("event_type")) if x)
        lines.append(f"- **{it.get('event_title') or '(untitled event)'}**" + (f" ({when})" if when else "")
                     + (f": {tail}" if tail else ""))
    elif corpus == "tags":
        lines.append(f"- **{it.get('name') or it.get('slug') or '?'}** [{it.get('category') or '?'}]"
                     + (f"  `{it.get('slug')}`" if it.get("slug") else ""))
    else:
        lines.append(_result_line(corpus, it))
    return lines


def _render_brief(resp, args):
    data = resp.get("data") if isinstance(resp, dict) else None
    if not isinstance(data, dict):
        return json.dumps(resp, indent=2, ensure_ascii=False)
    window = " ".join(x for x in (f"since {args.since}" if args.since else "",
                                  f"until {args.until}" if args.until else "") if x)
    out = [f"# Research brief: {args.topic}",
           f"> {urllib.parse.urlsplit(site()).netloc or site()}, community `{args.community}`"
           + (f", {window}" if window else "")
           + f". Generated {_dt.datetime.now(_dt.timezone.utc).date().isoformat()} (UTC)."]
    for corpus, heading, how in BRIEF_SECTIONS:
        block = data.get(corpus) or {}
        results = block.get("results") or []
        out += ["", f"## {heading} ({block.get('total', len(results))})", f"_{how}_"]
        if not results:
            out.append("- nothing found")
        for it in results[:args.limit]:
            out += _brief_item(corpus, it, args.community)
    others = [c for c in data if c not in {s[0] for s in BRIEF_SECTIONS}]
    for corpus in others:
        results = (data.get(corpus) or {}).get("results") or []
        if results:
            out += ["", f"## Also found: {corpus} ({len(results)})"]
            out += [_result_line(corpus, it) for it in results[:args.limit]]
    missing = [c for c in CORPORA if c not in data]
    if missing:
        out += ["", f"_Not searched for your key: {', '.join(missing)} (external documents and social "
                    "posts need an editor role)._"]
    out += ["", "## Fill these in before you write"]
    for i, (label, prompt) in enumerate(BRIEF_BLANKS, 1):
        out += ["", f"{i}. **{label}.** {prompt}", "   > "]
    return "\n".join(out)


def cmd_brief(args):
    """A research brief before writing: one /search across every corpus the key
    reaches, arranged for a writer, then four blanks the writer fills. Mechanical
    assembly, no model call; the judgment is the reader's. Read-only against the
    API; --out writes the brief to a LOCAL file and nothing else."""
    params = {"q": args.topic, "community": args.community, "limit": args.limit}
    params.update(_date_params(args))
    resp = _guided(lambda: api_request("GET", "/search", params))
    if args.json:
        _emit(resp, args, None, mode="brief")
        return
    text = _render_brief(resp, args)
    if args.out:
        Path(args.out).write_text(f"{text}\n\n---\n{terms_note()}\n", encoding="utf-8")
        text += f"\n\n(Written to {args.out}.)"
    _emit(resp, args, lambda r: text, mode="brief")


def cmd_digest(args):
    """Recent-stories markdown homepage. Public, no key. The on-ramp. With --date,
    one day's stories with a summary each instead (see cmd_digest_day)."""
    if getattr(args, "date", None):
        cmd_digest_day(args)
        return
    md = fetch_markdown(site() + "/")
    if args.json:
        print(json.dumps({"markdown": md}, ensure_ascii=False))
        return
    print(md.rstrip())
    _print_hateoas("digest", args, None)
    print(f"\n---\n{terms_note()}")


def cmd_article(args):
    """Full article. A URL or slug uses the public markdown surface (no key); a
    bare id uses GET /articles/<id> (keyed, richer: sources, persons)."""
    ref = args.ref
    # A UUID is an id and takes the keyed endpoint. EVERYTHING else is a slug or a
    # URL and takes the public markdown surface. The old test was `"/" in ref`,
    # which sent a bare slug down the keyed branch and demanded a key for
    # something this client documents as public.
    is_id = bool(re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                              r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", ref))
    if not is_id:
        url = ref if ref.startswith("http") else f"{site()}/c/{args.community}/{ref.lstrip('/')}"
        # The terms belong to wherever the CONTENT came from, which for an explicit
        # URL need not be the configured newsroom.
        parts = urllib.parse.urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if args.json:
            print(json.dumps({"markdown": fetch_markdown(url)}, ensure_ascii=False))
            return
        print(fetch_markdown(url).rstrip())
        _print_hateoas("article", args, None)
        print(f"\n---\n{terms_note(origin)}")
    else:
        resp = _guided(lambda: api_request("GET", f"/articles/{ref}"))

        def render(r):
            a = r.get("data") if isinstance(r, dict) else None
            if not isinstance(a, dict) or "title" not in a:
                return json.dumps(r, indent=2, ensure_ascii=False)
            head = [f"# {a.get('title')}"]
            meta = "  ".join(x for x in (
                (a.get("published_at") or "")[:10],
                a.get("location") or "",
                f"{a.get('word_count')} words" if a.get("word_count") else "",
                f"~{a.get('estimated_read_minutes')} min" if a.get("estimated_read_minutes") else "",
            ) if x)
            if meta:
                head.append(meta)
            if a.get("slug"):
                head.append(f"{site()}/c/{args.community}/{a['slug']}")
            for label in ("tldr", "excerpt"):
                if a.get(label):
                    head += ["", f"## {label}", str(a[label]).strip()]
            body = a.get("content") or a.get("body") or ""
            if body:
                head += ["", "## body", str(body).strip()]
            else:
                head += ["", "(no body in this payload: fetch by slug or URL for the full markdown, "
                             "or use --json to see every field)"]
            return "\n".join(head)

        _emit(resp, args, render, mode="article")


def _result_line(corpus, it):
    """One rendered search-result line, shared by `search` and `angles` so the
    display-field logic (tuned against live shapes) can't drift between them.

    Display field varies by corpus (verified live 2026-07-23): articles=title,
    tags/speakers=name/display_name, events=event_title, transcripts=source_title,
    social=body_text, docs=title/summary. Actionable id: a transcript's is its
    source_id (feed `transcript`); everything else uses id, falling back to slug."""
    title = (it.get("title") or it.get("name") or it.get("display_name")
             or it.get("event_title") or it.get("source_title")
             or it.get("summary") or it.get("body_text") or it.get("content")
             or "(untitled)")
    rid = it.get("source_id") if corpus == "transcripts" else (it.get("id") or it.get("slug") or "")
    when = (it.get("published_at") or it.get("event_date") or "")[:10]
    return (f"- {str(title).strip()[:140]}"
            + (f"  ({when})" if when else "")
            + (f"  [{rid}]" if rid else ""))


def _render_corpora(data, limit):
    """Render a /search `data` dict (corpus -> {results,total}) as grouped lines,
    or a shape-mismatch note. Shared by `search` and `angles`."""
    if not isinstance(data, dict):
        return ["(unexpected response shape; use --json to inspect)"]
    out = []
    for corpus, block in data.items():
        results = (block or {}).get("results") or []
        out.append(f"\n## {corpus} ({(block or {}).get('total', len(results))})")
        for it in results[:limit]:
            out.append(_result_line(corpus, it))
    return out


def cmd_search(args):
    """Unified multi-corpus search. `community` is required by the API."""
    params = {"q": args.query, "community": args.community, "limit": args.limit}
    params.update(_date_params(args))
    if args.corpus:
        _check_corpora(args.corpus)
        params["corpus"] = args.corpus
    resp = _guided(lambda: api_request("GET", "/search", params))

    def render(r):
        out = [f"# search: {args.query!r}  (corpus: {args.corpus or 'all'})"]
        out += _render_corpora(r.get("data") if isinstance(r, dict) else None, args.limit)
        return "\n".join(out)

    _emit(resp, args, render, mode="search")


def cmd_angles(args):
    """Discovery mode (the five-Ws investigative method): fix two Ws (an intent),
    pull the corpora that intent implies in ONE framed /search, and frame the hits
    as fixed-vs-expanding axes. Read-only: it only GETs /search. It does one level;
    the nesting is handed back as Next steps, so the journalist drives depth, not
    the key's rate limit."""
    fixed, expand, corpora = INTENTS[args.intent]
    params = {"q": args.seed, "community": args.community, "corpus": corpora, "limit": args.limit}
    params.update(_date_params(args))
    resp = _guided(lambda: api_request("GET", "/search", params))

    def render(r):
        out = [
            f"# angles: {args.seed!r}",
            f"Intent: {args.intent}  (fix {fixed}; expand {expand})",
            "Held on the fixed axes; the hits below vary the rest. One level only: nest via Next steps.",
        ]
        out += _render_corpora(r.get("data") if isinstance(r, dict) else None, args.limit)
        out.append("\nRelevance, not corroboration: a hit is relevant when a SECOND axis agrees, not "
                   "just the topic. That still does not confirm a claim, since several pieces can repeat "
                   "one source: verify against an independent source, ideally the primary record.")
        return "\n".join(out)

    _emit(resp, args, render, mode="angles")


def _mmss(t):
    try:
        s = int(float(t))
        return f"{s // 60:02d}:{s % 60:02d}"
    except (TypeError, ValueError):
        return "--:--"


def cmd_transcript(args):
    """A meeting transcript's text chunks (speaker + timestamps). Keyed.

    Live-verified shape (2026-07-23): a top-level dict with `chunks`
    (chunk_index, content, speaker, start_time, end_time), `speakerMap`, `total`,
    `status`. Falls back to raw JSON if the shape ever changes."""
    resp = _guided(lambda: api_request("GET", f"/transcript/{args.source_id}/chunks", {"limit": args.limit}))

    def render(r):
        chunks = r.get("chunks") if isinstance(r, dict) else None
        if not isinstance(chunks, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        out = [f"# transcript {args.source_id}  ({r.get('status', '?')}, {r.get('total', len(chunks))} chunks)"]
        for c in chunks[: args.limit]:
            out.append(f"[{_mmss(c.get('start_time'))}] {c.get('speaker') or '?'}: "
                       f"{str(c.get('content', '')).strip()}")
        return "\n".join(out)

    _emit(resp, args, render, mode="transcript")


def cmd_events(args):
    """Genuinely UPCOMING public events, from GET /calendar.

    This used to run `/search?corpus=events`, which ranks by relevance and not by
    date. On 2026-09-09 that returned 15 of 15 events already in the past under a
    heading that said "upcoming", which is the one thing a hearing listing must
    never do: the whole use is deciding what you can still attend or still file
    comment on. `/calendar` is the date-ranged endpoint (start defaults to now,
    end to now+30d) and is what "upcoming" actually means.

    `/calendar` has no full-text parameter, so a query filters the window
    client-side on title and location. To search events by relevance across all
    time (including past ones), use `search <q> --corpus events`."""
    now = _dt.datetime.now(_dt.timezone.utc)
    base = {
        "community": args.community,
        "start": now.isoformat(),
        "end": (now + _dt.timedelta(days=args.days)).isoformat(),
    }
    if args.type:
        base["types"] = args.type

    if not args.query:
        resp = _guided(lambda: api_request("GET", "/calendar", dict(base, limit=args.limit)))
        truncated = False
    else:
        # /calendar has no full-text parameter, so a query filters client-side. It
        # used to filter ONE page of 50 and report "nothing in the window" when the
        # match sat at position 55, which on a tool people use to find hearings and
        # comment deadlines is the worst possible way to be wrong: it does not look
        # like a limitation, it looks like an answer. Page the whole window instead,
        # and say so when the cap stops us rather than implying completeness.
        events, offset, truncated = [], 0, False
        while True:
            page = _guided(lambda: api_request(
                "GET", "/calendar", dict(base, limit=EVENTS_PAGE, offset=offset)))
            rows = ((page.get("data") or {}).get("events")) if isinstance(page, dict) else None
            if not isinstance(rows, list):
                resp = page
                break
            events.extend(rows)
            offset += len(rows)
            if len(rows) < EVENTS_PAGE:
                break
            if offset >= EVENTS_SCAN_CAP:
                truncated = True
                break
        else:
            pass
        resp = {"data": {"events": events}} if isinstance(rows, list) else resp

    def render(r):
        events = ((r.get("data") or {}).get("events")) if isinstance(r, dict) else None
        if not isinstance(events, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        if args.query:
            q = args.query.lower()
            events = [e for e in events
                      if q in f"{e.get('event_title') or ''} {e.get('event_location') or ''}".lower()]
        head = f"# events: next {args.days} days"
        if args.query:
            head += f", matching {args.query!r}"
        out = [head]
        if truncated:
            out.append(f"(scanned the first {EVENTS_SCAN_CAP} events in the window and stopped; "
                       "there may be later matches. Narrow with --type or --days.)")
        if not events:
            out.append(f"(nothing in the window{' matching that' if args.query else ''}"
                       f"{', in the part scanned' if truncated else ''}. "
                       f"Widen with --days, or use `search` to reach past events.)")
        for e in events[: args.limit]:
            when = (e.get("event_date") or "")[:16].replace("T", " ")
            where = e.get("event_location") or ""
            kind = e.get("event_type") or ""
            out.append(f"- {e.get('event_title') or '(untitled)'}")
            meta = "  ".join(x for x in (when, where, f"({kind})" if kind else "") if x)
            out[-1] += (f"\n    {meta}" if meta else "") + (f"  [{e.get('id')}]" if e.get("id") else "")
        return "\n".join(out)

    _emit(resp, args, render, mode="events")


def cmd_rag(args):
    """Prior-coverage RAG: a synthesized answer plus the citations behind it.

    Live-verified shape (2026-09-09): `data` carries `answer` (markdown, with
    [F4]/[H2]-style refs), `citations` ({ref, kind, verbatim_excerpt, speaker,
    url, source_id}), `pools`, `retrieval` and `token_usage`. The citations are
    the point: an answer you cannot trace is not usable in reporting, and the
    excerpt + url are what let you quote a source rather than a summary of it."""
    resp = _guided(lambda: api_request(
        "POST", "/rag/query",
        body={"query": args.query, "community": args.community}, timeout=RAG_TIMEOUT))

    def render(r):
        d = r.get("data") if isinstance(r, dict) else None
        if not isinstance(d, dict) or "answer" not in d:
            return json.dumps(r, indent=2, ensure_ascii=False)
        out = [f"# rag: {args.query!r}  ({d.get('mode', '?')})", "", str(d.get("answer", "")).strip()]
        cites = d.get("citations") or []
        if cites:
            out += ["", f"## citations ({len(cites)})"]
            for c in cites[: args.limit]:
                who = f", {c['speaker']}" if c.get("speaker") else ""
                out.append(f"- [{c.get('ref', '?')}] {c.get('kind', '')}{who}")
                if c.get("verbatim_excerpt"):
                    out.append(f'    "{str(c["verbatim_excerpt"]).strip()[:220]}"')
                if c.get("url"):
                    out.append(f"    {c['url']}")
            if len(cites) > args.limit:
                out.append(f"  (+{len(cites) - args.limit} more; --limit to widen, --json for all)")
        out.append("\nQuote the CITATION, not the answer: the synthesized text is a summary of "
                   "someone else's reporting, and the excerpt + url are what you can attribute.")
        return "\n".join(out)

    _emit(resp, args, render, mode="rag")


def cmd_clip(args):
    """Resolve a KNOWN clip id to its MP4 URL.

    `/clips/<id>/stream` 302s to a public storage object, so there is no JSON to
    render: the answer IS the URL. It is returned unfollowed, so nothing here
    downloads video. Browsing the clip library (`GET /clips`) is a separate
    endpoint that takes cookie-session auth ONLY and rejects every API key, so
    ids come from `search` or an article, not from this tool."""
    r = _guided(lambda: api_redirect(f"/clips/{args.clip_id}/stream"))
    url = r.get("location")
    if args.json:
        print(json.dumps({"clip_id": args.clip_id, "stream_url": url,
                          "status": r.get("status")}, indent=2))
        return
    if url:
        print(f"# clip {args.clip_id}\n{url}")
    else:
        print(f"# clip {args.clip_id}\nNo redirect (HTTP {r.get('status')}). "
              f"{r.get('body', '')[:300]}")
    _print_hateoas("clip", args, None)
    print(f"\n---\n{terms_note()}")


def cmd_communities(args):
    """List the community slugs `--community` accepts.

    Every keyed mode requires a community and the API rejects an unknown slug,
    but nothing in this client used to tell you what the valid ones ARE, so the
    only discoverable value was the default baked into the source."""
    resp = _guided(lambda: api_request("GET", "/communities", {"limit": 100}))

    def render(r):
        rows = r.get("data") if isinstance(r, dict) else None
        if not isinstance(rows, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        out = [f"# communities ({len(rows)})"]
        for c in rows:
            if not isinstance(c, dict):
                continue
            mark = "  <- default" if c.get("slug") == default_community() else ""
            out.append(f"- {c.get('slug', '?'):24} {c.get('name', '')}{mark}")
        out.append("\nPass one as --community <slug>.")
        return "\n".join(out)

    _emit(resp, args, render, mode="communities")


def _paged(resp):
    """The list envelope's pagination line, or "" when it isn't a list response.

    List endpoints answer {data, count, offset, limit, has_more, total?}. A page
    that silently drops the rest is how a reporter concludes "there are only
    three" when there are ninety, so has_more is rendered, not swallowed."""
    if not isinstance(resp, dict) or "has_more" not in resp:
        return ""
    shown = resp.get("count", 0)
    start = resp.get("offset", 0)
    total = resp.get("total")
    line = f"showing {start + 1}-{start + shown}" + (f" of {total}" if total is not None else "")
    if resp.get("has_more"):
        line += f"  (more: --offset {start + (resp.get('limit') or shown)})"
    return line


def _article_lines(rows, limit):
    """One rendered line per article, shared by every mode that lists articles so
    the date and id cannot go missing from one of them."""
    out = []
    for a in (rows or [])[:limit]:
        if not isinstance(a, dict):
            continue
        when = (a.get("published_at") or "")[:10]
        out.append(f"- {str(a.get('title') or '(untitled)').strip()[:130]}"
                   + (f"  ({when})" if when else "")
                   + (f"  [{a.get('id') or a.get('slug') or ''}]"
                      if (a.get("id") or a.get("slug")) else ""))
        # persons/<id>/articles carries the actual quote that tied the person to
        # the story. That excerpt IS the Who axis; a bare title is just a link.
        if a.get("verbatim_excerpt"):
            n = a.get("attribution_count") or 0
            out.append(f'    quoted{f" ({n}x)" if n else ""}: '
                       f'"{str(a["verbatim_excerpt"]).strip()[:200]}"')
    return out


def cmd_people(args):
    """The Who axis as a directory: named speakers, filterable by substring and
    role. `angles --intent track` fixes Who+What but had no way to LOOK UP a
    who, so the actor had to be spelled exactly right from memory."""
    params = {"community": args.community, "limit": args.limit, "offset": args.offset}
    if args.query:
        params["q"] = args.query
    if args.role:
        params["role"] = args.role
    resp = _guided(lambda: api_request("GET", "/persons", params))

    def render(r):
        rows = r.get("data") if isinstance(r, dict) else None
        if not isinstance(rows, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        out = [f"# people{': ' + repr(args.query) if args.query else ''}"]
        if not rows:
            out.append("(no match. Names are as published: try a surname alone.)")
        for p in rows:
            desc = "  ".join(x for x in (p.get("title") or "", p.get("organization") or "",
                                         p.get("district") or "") if x)
            out.append(f"- {p.get('display_name') or '(unnamed)'}"
                       + (f"  ({p.get('role')})" if p.get("role") else "")
                       + f"  [{p.get('id', '')}]")
            if desc:
                out.append(f"    {desc}")
        page = _paged(r)
        if page:
            out.append(f"\n{page}")
        return "\n".join(out)

    _emit(resp, args, render, mode="people")


def cmd_person(args):
    """One person, plus the published articles they appear in.

    Two calls, both GET: the record and their coverage. It is the one place this
    client makes more than one request per run, because a person without their
    coverage is a contact card, and the coverage without the person is a list of
    links whose relevance you have to take on trust.

    "Appears in", not "quoted in", and the difference is load-bearing. The
    endpoint returns a UNION of two things: articles where an attribution matched
    this person's NAME, and articles structurally linked to them. Only the first
    kind carries a verbatim excerpt, so a row without one is an association the
    platform asserts rather than a quote you can attribute. Rows are marked
    accordingly, because "Dunleavy appears in this piece" and "Dunleavy said this
    in this piece" are different claims and only one of them is quotable."""
    who = _guided(lambda: api_request("GET", f"/persons/{args.person_id}"))
    cov = _guided(lambda: api_request(
        "GET", f"/persons/{args.person_id}/articles",
        {"limit": args.limit, "offset": args.offset}))
    if args.json:
        print(json.dumps({"person": who, "articles": cov}, indent=2, ensure_ascii=False))
        return
    # GET /persons/<id> nests the record under data.speaker (alongside data.aliases),
    # unlike the list endpoint which returns person objects directly.
    d = (who.get("data") if isinstance(who, dict) else None) or {}
    p = d.get("speaker") if isinstance(d.get("speaker"), dict) else d
    out = [f"# {p.get('display_name') or args.person_id}"]
    meta = "  ".join(x for x in (p.get("role") or "", p.get("title") or "",
                                 p.get("organization") or "", p.get("district") or "",
                                 p.get("location") or "") if x)
    if meta:
        out.append(meta)
    aliases = [a.get("alias") or a.get("name") for a in (d.get("aliases") or [])
               if isinstance(a, dict)]
    if aliases:
        out.append("also known as: " + ", ".join(str(a) for a in aliases if a))
    for field in ("bio", "website"):
        if p.get(field):
            out.append(f"{field}: {str(p[field]).strip()[:400]}")
    rows = cov.get("data") if isinstance(cov, dict) else None
    out.append(f"\n## appears in ({(cov or {}).get('total', len(rows or []))})")
    out += _article_lines(rows, args.limit) or ["(no linked coverage)"]
    if rows and not any((r or {}).get("verbatim_excerpt") for r in rows if isinstance(r, dict)):
        out.append("\n(No row here carries a verbatim excerpt, so these are structural links "
                   "rather than matched quotes. Open one and confirm before writing that this "
                   "person said anything in it.)")
    page = _paged(cov)
    if page:
        out.append(f"\n{page}")
    print("\n".join(out))
    _print_hateoas("person", args, cov)
    print(f"\n---\n{terms_note()}")


# The tag categories /tags can FILTER on. Verified against the live API 2026-09-29:
# organization 230, location 199, topic 104. A fourth category, election (67 tags),
# exists on the rows but the server does not filter by it: `category=election`
# answered all 600 tags, exactly like a misspelling. Offering it would print the
# whole vocabulary under a heading saying "category: election", so it stays out
# until the server honours it.
TAG_CATEGORIES = ("organization", "topic", "location")

# Topic tags are read whole so they can be ranked; the category held 104 on
# 2026-09-29. The cap bounds a runaway vocabulary rather than a real one.
TOPIC_PAGE = 100
TOPIC_SCAN_CAP = 1000


def _read_topic_tags():
    """Every topic-category tag, in pages. Returns the combined list envelope, or
    the first non-list response untouched so the renderer can fall back to it."""
    rows, off, total = [], 0, None
    while off < TOPIC_SCAN_CAP:
        page = api_request("GET", "/tags", {"category": "topic", "limit": TOPIC_PAGE,
                                            "offset": off}, public=True)
        data = page.get("data") if isinstance(page, dict) else None
        if not isinstance(data, list):
            return page
        rows += data
        off += len(data)
        total = page.get("total", total)
        if not page.get("has_more") or not data:
            return {"data": rows, "total": total if total is not None else len(rows),
                    "complete": True}
    return {"data": rows, "total": total if total is not None else len(rows), "complete": False}


def cmd_topics(args):
    """The beats, ranked by how much has been published under each.

    This read GET /topics until 2026-09-29. That is the retired topics taxonomy:
    the platform's own OpenAPI spec marks it deprecated ("Use GET /api/v1/tags
    instead"), topics were replaced by tags in April 2026, and on 2026-09-09 every
    one of its 15 rows reported 0 articles. The topic-category TAGS carry real
    counts, answer without a key, and are exactly what `browse --tag` takes, so
    every beat listed here is one you can open.

    The server lists tags alphabetically and takes no sort, so ranking by coverage
    means reading the whole category first; --limit and --offset then page the
    RANKED list, not the server's alphabet. Counts are per tag and do not roll up
    (on 2026-09-29 "Politics & Government" held 28 articles directly while
    "Government" beneath it held 556), so each row names its parent rather than
    this client summing a hierarchy it does not own."""
    resp = _guided(_read_topic_tags)

    def render(r):
        rows = r.get("data") if isinstance(r, dict) else None
        if not isinstance(rows, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        rows = [t for t in rows if isinstance(t, dict)]
        names = {t.get("slug"): t.get("name") for t in rows}
        # Printing "0 articles" against a beat that HAS coverage reads as "nothing
        # published here". The retired /topics did exactly that for every row, so
        # if a vocabulary ever arrives with no counts at all, say so once rather
        # than rendering a column of zeros.
        any_counts = any(t.get("article_count") for t in rows)
        ranked = sorted(rows, key=lambda t: (-(t.get("article_count") or 0), str(t.get("name", ""))))
        start = max(args.offset, 0)
        page = ranked[start:start + args.limit]
        out = [f"# topics: {len(ranked)} beats, ranked by published articles"]
        for t in page:
            n = t.get("article_count")
            counts = f"{n} articles" if any_counts and n is not None else ""
            parts = str(t.get("path") or "").split("/")
            parent = names.get(parts[-2]) if len(parts) > 1 else None
            under = f"  (under {parent})" if parent else ""
            out.append(f"- {str(t.get('name', '?'))[:32]:32} {counts:>13}{under}  [{t.get('slug', '')}]")
        if not any_counts:
            out.append("\n(The API reports no article counts for these beats, so read them as "
                       "UNKNOWN, not as empty. These stats are not being populated; use "
                       "`browse --tag <slug>` for what a beat actually has.)")
        if not r.get("complete", True):
            out.append(f"\n(Read the first {len(ranked)} of {r.get('total')} topic tags and ranked "
                       "only those: the scan cap stopped it.)")
        out.append("\nCounts are per beat and do not roll up into the parent named beside them.")
        line = _paged({"count": len(page), "offset": start, "limit": args.limit,
                       "has_more": start + len(page) < len(ranked), "total": len(ranked)})
        if line:
            out.append(line)
        return "\n".join(out)

    _emit(resp, args, render, mode="topics")


def cmd_tags(args):
    """The subject vocabulary: organizations, topics and locations that coverage
    is filed under. `--category` narrows; the slug is what `browse --tag`
    takes. Public: /tags answers without a key.

    The category list is closed on purpose. The server IGNORES a category it does
    not know and returns the whole vocabulary (checked 2026-09-29: an unknown
    category answered all 600 tags), which would read as a filtered result."""
    params = {"limit": args.limit, "offset": args.offset}
    if args.query:
        params["q"] = args.query
    if args.category:
        params["category"] = args.category
    resp = _guided(lambda: api_request("GET", "/tags", params, public=True))

    def render(r):
        rows = r.get("data") if isinstance(r, dict) else None
        if not isinstance(rows, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        out = [f"# tags{': ' + repr(args.query) if args.query else ''}"
               + (f"  (category: {args.category})" if args.category else "")]
        stray = sorted({str(t.get("category")) for t in rows
                        if isinstance(t, dict) and args.category and t.get("category") != args.category})
        if stray:
            # The server answers an unfiltered list for a category it does not
            # filter on. Say so, rather than let the heading above claim a filter.
            out.append(f"(The server did NOT apply category={args.category}: rows include "
                       f"{', '.join(stray)}. Treat this as the unfiltered vocabulary.)")
        if not rows:
            out.append("(no match)")
        for t in rows:
            out.append(f"- {str(t.get('name', '?'))[:44]:44} {t.get('category', ''):13} "
                       f"[{t.get('slug', '')}]")
            if t.get("description"):
                out.append(f"    {str(t['description']).strip()[:110]}")
        page = _paged(r)
        if page:
            out.append(f"\n{page}")
        out.append("\nOpen a tag's coverage with: browse --tag <slug>")
        return "\n".join(out)

    _emit(resp, args, render, mode="tags")


# Sort modes the article list accepts. Verified against the live API 2026-09-09.
# Paging for the client-side event filter. 200 is the API's own max page size.
EVENTS_PAGE = 200
EVENTS_SCAN_CAP = 1000

SORTS = ("hot", "new", "timeline", "top", "popular", "alphabetical")
TIME_WINDOWS = ("today", "week", "month", "all")


def cmd_browse(args):
    """The published article list, without a search query.

    `search` answers "what do you have about X". This answers "what has been
    published", which is a different question and the one you ask before you know
    what X is. With `--tag <slug>` it lists a single beat's coverage instead.

    GET /feed is deliberately NOT wrapped: it returns byte-identical results to
    `/articles?sort=new` (checked 2026-09-09) and accepts no community parameter,
    so for a consumer targeting a community it is the same mode with less reach."""
    if args.tag:
        path, params = f"/tags/{args.tag}/articles", {"limit": args.limit, "offset": args.offset}
    else:
        path = "/articles"
        params = {"community": args.community, "limit": args.limit,
                  "offset": args.offset, "sort": args.sort}
        if args.sort == "top" and args.window:
            params["t"] = args.window
    resp = _guided(lambda: api_request("GET", path, params))

    def render(r):
        rows = r.get("data") if isinstance(r, dict) else None
        if not isinstance(rows, list):
            return json.dumps(r, indent=2, ensure_ascii=False)
        head = f"# browse: tag {args.tag}" if args.tag else f"# browse: {args.sort}"
        out = [head] + (_article_lines(rows, args.limit) or ["(nothing published here)"])
        page = _paged(r)
        if page:
            out.append(f"\n{page}")
        return "\n".join(out)

    _emit(resp, args, render, mode="browse")


# (label, method, path, params, body) for the keyed probes. digest is separate.
# `clips` and `transcripts/search` are deliberately absent: both authenticate via
# cookie session only (platform reads `supabase.auth.getUser()` rather than going
# through runApiHandler), so they 401 for EVERY API key including an admin's.
# Probing them taught the reader a role they could acquire, which was false.
# These stay even though GET /me now reports reachability, because the two answer
# different questions and have been observed to DISAGREE. /me is derived from the
# router: it says what the code permits. A probe says what actually happened to
# this key just now, against this deploy, including the RLS and validation layers
# the router cannot see. Keeping a small empirical check is what would catch the
# server's self-description going wrong, and on 2026-09-09 it was wrong: /me
# listed `/api/v1/clips/{id}` as session_auth_only while its GET answers 404
# unauthenticated, and listed three POST-only paths that have no GET at all.
#
# `rag` was REMOVED from this list on 2026-09-09. /me reports it, and probing it
# meant a synthesis call measured at 84s on every `check`.
def keyed_probes(community):
    """Built per call, because these used to hard-code `alaska-news`, which made
    `check --community X` report on Alaska while saying it had checked X."""
    return [
        ("articles", "GET", "/articles", {"limit": 1, "community": community}, None),
        ("search", "GET", "/search", {"q": "news", "community": community, "limit": 1}, None),
        ("transcripts", "GET", "/transcripts", {"limit": 1}, None),
        ("calendar (events)", "GET", "/calendar", {"community": community, "limit": 1}, None),
        ("communities", "GET", "/communities", {"limit": 1}, None),
    ]
# KEY_BLIND_ENDPOINTS was deleted on 2026-09-09.
#
# It listed, by hand, the endpoints no API key reaches. It was correct when it
# was written and nothing compared it to the platform's router, so it would have
# kept answering confidently after the server changed. That is the whole failure
# mode this client was compensating for.
#
# The platform now answers the question itself: GET /api/v1/me returns a
# `reachability` block derived from its own route tree, which the platform checks
# against its live router. It distinguishes `session_auth_only` (no key of any
# role reaches it, so there is nothing to request) from `requires_role` (a
# membership you could be granted), which is the distinction this list existed
# to preserve and the one a bare 401 destroys. The public spec for /me is at
# <newsroom>/api/v1/openapi.json (for Alaska News, alaskanews.com/api/v1/openapi.json).
_STATUS = {401: "needs a key", 403: "forbidden (role/scope)", 429: "rate-limited",
           0: "unreachable", TIMED_OUT: "timed out (slow, not blocked)",
           NON_JSON: "non-JSON reply"}


def render_reachability(reach):
    """Render GET /me's `reachability` block as lines. Pure, so the render is
    testable without a credential.

    That matters more than it sounds. The only test covering this path needs a
    real key and therefore skips in CI, which is how the previous version of this
    code shipped a claim its own suite never executed."""
    if not isinstance(reach, dict) or not reach:
        # A 200 with no block is an older platform, not an empty answer. Printing
        # "auth method: ?" would present a missing feature as a missing value.
        return ["\n  reachability: not reported by this platform build "
                "(GET /api/v1/me returned no `reachability`)"]
    out = [f"\n  auth method: {reach.get('auth_method', '?')}"
           f"   reachable: {reach.get('reachable_count', '?')}"
           f"   role-gated: {reach.get('conditional_count', '?')}"]

    # read_only is the field this skill cares about most: SKILL.md tells the
    # reader to tick "Read-only" when creating a key, and until now nothing could
    # tell them whether they actually did.
    ro = reach.get("read_only")
    if ro is True:
        out.append("  key is READ-ONLY: the server rejects writes before a handler runs. "
                   "Note /rag/query is an HTTP POST and is refused too.")
    elif ro is False:
        out.append("  key is NOT read-only: it can write. Nothing here writes, but a "
                   "read-only key would make that a server guarantee instead of a promise. "
                   f"Create one at {key_settings_url()} (rag would then be refused).")

    for c in reach.get("communities") or []:
        if isinstance(c, dict):
            out.append(f"  community {c.get('slug', '?')}: role {c.get('role', '?')}")

    groups = {}
    for e in reach.get("unreachable") or []:
        if isinstance(e, dict):
            groups.setdefault(e.get("reason", "unknown"), []).append(e)

    blind = groups.get("session_auth_only") or []
    if blind:
        out.append(f"\n  Not reachable by ANY api key ({len(blind)}), "
                   "and not a role you can be granted:")
        for e in blind:
            out.append(f"    {e.get('path', '?')}")
        # The server ships a remedy per entry. Reciting it once per group keeps
        # the list readable without discarding the actionable half.
        remedy = next((e.get("remedy") for e in blind if e.get("remedy")), None)
        if remedy:
            out.append(f"    -> {remedy}")

    for reason, label in (("requires_role", "Needs an editor/admin membership"),
                          ("requires_platform_admin", "Needs platform admin")):
        rows = groups.get(reason) or []
        if rows:
            out.append(f"\n  {label} ({len(rows)}), e.g.:")
            for e in rows[:3]:
                out.append(f"    {e.get('path', '?')}")

    for reason, rows in groups.items():
        if reason not in ("session_auth_only", "requires_role", "requires_platform_admin"):
            out.append(f"\n  {reason} ({len(rows)}), e.g.: "
                       + ", ".join(str(e.get('path', '?')) for e in rows[:3]))
    return out


def cmd_check(args):
    """Report what THIS key can actually reach, so a user learns their access
    before building on it.

    Three things this used to get wrong, all of them the instrument answering a
    question next to the one asked:
      - `--json` printed prose, so the one mode a script would parse was the one
        mode that could not be parsed.
      - A key rejected by EVERY endpoint was labelled "no access (role)" on each
        of them, sending the reader after a role upgrade when the key was simply
        bad. A role gate is something some endpoints apply; a rejection
        everywhere is a credential.
      - The footer said "your key reached the search surface; start there" after
        every single request had failed."""
    _load_env()
    host = urllib.parse.urlparse(site()).netloc or site()
    key = read_key()
    result = {"newsroom": host, "community": args.community, "surfaces": {},
              "key": {"present": bool(key), "format_ok": key.startswith("cn_") if key else None},
              "reachability": None, "notes": []}

    try:
        fetch_markdown(site() + "/", timeout=15)
        result["surfaces"]["digest (public)"] = "OK"
    except ApiError as e:
        result["surfaces"]["digest (public)"] = _STATUS.get(e.code, f"HTTP {e.code}")

    codes = []
    if key:
        for label, method, path, params, body in keyed_probes(args.community):
            try:
                api_request(method, path, params=params, body=body, timeout=30)
                result["surfaces"][label] = "OK"
                codes.append(200)
            except ApiError as e:
                codes.append(e.code)
                result["surfaces"][label] = _STATUS.get(e.code, f"HTTP {e.code}") if e.code != 401 else "401"

        # Now interpret, with every probe in hand rather than one at a time.
        all_401 = bool(codes) and all(c == 401 for c in codes)
        for label, status in list(result["surfaces"].items()):
            if status != "401":
                continue
            if not result["key"]["format_ok"]:
                result["surfaces"][label] = "rejected (bad key format)"
            elif all_401:
                result["surfaces"][label] = "rejected (key not accepted)"
            else:
                result["surfaces"][label] = "no access (role)"
        if all_401:
            result["notes"].append(
                "Every keyed request was rejected. That is the key itself, not a role: a role "
                "gate stops some endpoints, never all of them. Check it is current and not revoked.")
        if key and not result["key"]["format_ok"]:
            result["notes"].append(
                f"Key starts {key[:4]!r}; keys for this API start 'cn_'.")

        try:
            me = api_request("GET", "/me", timeout=30)
        except ApiError as e:
            result["notes"].append(
                f"Reachability unavailable (HTTP {e.code})."
                + (" Expected, given the key was rejected everywhere." if all_401
                   else " This platform may predate GET /api/v1/me reachability."))
        else:
            result["reachability"] = (me or {}).get("reachability")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"reachability: {host}, community {args.community}\n")
    for label, status in result["surfaces"].items():
        print(f"  {label:26} {status}")
    if not key:
        print(f"  {'(keyed modes)':26} no key set")
    for note in result["notes"]:
        print(f"\n  {note}")
    if result["reachability"] is not None:
        for line in render_reachability(result["reachability"]):
            print(line)

    _print_hateoas("check", args, None, state=result)
    print(f"\n---\n{terms_note()}")


def main():
    _load_env()  # so has_key is knowable in every footer, digest/check included

    # Shared flags live on a parent parser added to every subcommand, so they work
    # AFTER the mode (`digest --json`), which is the order a CLI user reaches for.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true",
                        help="Raw JSON (its next_steps are the machine HATEOAS)")
    common.add_argument("--community", default=default_community(),
                        help=f"Community slug (default {default_community()})")

    ap = argparse.ArgumentParser(
        description=f"Read-only research client for the {site_host()} public API "
                    "(external consumers; NEWS_SITE picks the newsroom).",
        epilog=f"Every mode ends with Next steps (HATEOAS). Related modes: {RELATED_MODES}.")
    sub = ap.add_subparsers(dest="mode", required=True)

    p = sub.add_parser("digest", parents=[common],
                       help="Recent stories; --date for one day's stories with a summary each (public, no key)")
    p.add_argument("--date", metavar="YYYY-MM-DD",
                   help="one day's stories, each with its summary: a date, today or yesterday")
    p.add_argument("--tz", metavar="AREA/CITY",
                   help="the time zone a day is counted in (default: the one the newsroom reports)")
    sub.add_parser("check", parents=[common], help="What can my key reach?")
    sub.add_parser("communities", parents=[common],
                   help="List community slugs valid for --community")

    p = sub.add_parser("search", parents=[common], help="Multi-corpus semantic + keyword search")
    p.add_argument("query")
    p.add_argument("--corpus", help=f"comma-sep, default all: {','.join(CORPORA)} "
                                    "(external_documents and social_post are editor/admin only)")
    _add_date_range(p)
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("angles", parents=[common],
                       help="Discovery: fix two Ws (an intent), expand the rest (the five Ws)")
    p.add_argument("seed", help="the story seed (a topic, or an entity for --intent track)")
    p.add_argument("--intent", choices=list(INTENTS), default="similar",
                   help="which two Ws to fix (default: similar = What+Why)")
    _add_date_range(p)
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("brief", parents=[common],
                       help="Research brief before writing: prior coverage, the record, people, events, then blanks")
    p.add_argument("topic", help="what the piece is about, in the words you would search")
    _add_date_range(p)
    p.add_argument("--limit", type=int, default=5, help="entries per section (default 5)")
    p.add_argument("--out", metavar="FILE",
                   help="also write the brief to this local Markdown file (replaces one already there)")

    p = sub.add_parser("people", parents=[common], help="Who-axis directory: named speakers")
    p.add_argument("query", nargs="?", default="", help="substring match on the name")
    p.add_argument("--role", help="filter by role, e.g. official, candidate")
    _add_paging(p, 20)

    p = sub.add_parser("person", parents=[common],
                       help="One person, plus every article quoting them (with the quote)")
    p.add_argument("person_id", help="person id (from `people`)")
    _add_paging(p, 10)

    p = sub.add_parser("topics", parents=[common],
                       help="The beats, ranked by published articles (public, no key)")
    _add_paging(p, 30)

    p = sub.add_parser("tags", parents=[common],
                       help="Subject vocabulary: orgs, topics, locations (public, no key)")
    p.add_argument("query", nargs="?", default="", help="substring match on name/slug/aliases")
    p.add_argument("--category", choices=TAG_CATEGORIES)
    _add_paging(p, 20)

    p = sub.add_parser("browse", parents=[common],
                       help="Published articles without a query (what IS there, not what matches)")
    p.add_argument("--sort", choices=SORTS, default="new")
    p.add_argument("--window", choices=TIME_WINDOWS, help="only with --sort top")
    p.add_argument("--tag", help="list one tag's coverage instead (slug from `tags`)")
    _add_paging(p, 10)

    p = sub.add_parser("article", parents=[common], help="Full article by URL/slug (public) or id (keyed)")
    p.add_argument("ref", help="article id, slug, or full URL")

    p = sub.add_parser("transcript", parents=[common], help="Meeting transcript chunks by source id")
    p.add_argument("source_id")
    p.add_argument("--limit", type=int, default=50)

    p = sub.add_parser("events", parents=[common],
                       help="Upcoming public meetings/hearings (date-ranged, via /calendar)")
    p.add_argument("query", nargs="?", default="", help="optional substring filter on title/location")
    p.add_argument("--days", type=int, default=30, help="size of the forward window (default 30)")
    p.add_argument("--type", help="event type, e.g. meeting, public_notice, community_event, class")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("rag", parents=[common],
                       help="Prior-coverage RAG: synthesized answer + citations (slow: ~1-2 min)")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=8, help="citations to render (default 8)")

    p = sub.add_parser("clip", parents=[common], help="Stream a KNOWN clip id (browse needs editor role)")
    p.add_argument("clip_id")

    args = ap.parse_args()
    {
        "digest": cmd_digest, "check": cmd_check, "search": cmd_search, "angles": cmd_angles, "brief": cmd_brief,
        "article": cmd_article, "transcript": cmd_transcript, "events": cmd_events,
        "rag": cmd_rag, "clip": cmd_clip, "communities": cmd_communities,
        "people": cmd_people, "person": cmd_person, "topics": cmd_topics,
        "tags": cmd_tags, "browse": cmd_browse,
    }[args.mode](args)


if __name__ == "__main__":
    try:
        main()
    except ApiError as e:
        print(f"API error: {e}\n  Recovery: run `check` to confirm your key's reach, or --json to inspect.",
              file=sys.stderr)
        sys.exit(1)
