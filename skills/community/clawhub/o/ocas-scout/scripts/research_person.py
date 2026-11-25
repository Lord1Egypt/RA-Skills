#!/usr/bin/env python3
"""Scout person-research entrypoint (Tier 1 person OSINT).

The runnable implementation of the `scout.research.start` step described in
references/plans/contact-enrichment.plan.md. Given a name and whatever context
the address book already holds (email, org, occupation, city, and any profile
URLs the user hand-entered), it:

  1. USES known profile URLs as context. A URL already on the contact record
     is something the user typed, so it is recorded with provenance
     'contact_record', GitHub URLs are expanded via the structured users API,
     personal sites are cheaply title-fetched, and LinkedIn is recorded WITHOUT
     scraping (auth-walled). It does NOT by itself resolve identity — see (5).
     Getting that URL into weave is google_sync.py's job (it imports Google
     Contacts urls directly at 0.95); scout does not need to launder it
     through a corroboration gate it cannot honestly pass.
  2. Derives distinctive handle candidates from (a) explicit handles, (b) the
     slug of any known profile URL (linkedin.com/in/rheaott -> 'rheaott'),
     (c) the email local-part, and (d) name combinations — (d) only when the
     email handle is generic or absent.
  3. Runs Maigret (username -> 3000+ sites, with profile metadata) and Holehe
     (email -> which sites the address is registered on) from the isolated
     OSINT venv. Holehe needs only the email and runs even when no handle
     candidate survives.
  4. Enriches GitHub hits via the structured users API.
  5. CORROBORATES identity across sources: a profile only counts if its
     reported full name agrees with the contact's name (scout's normalizer).
     This is the discriminator that accepts 'wrenkeeley' -> Wren Keeley and
     rejects a common handle like 'geekgirl' whose profiles name other people.
     Seeding a handle from a known URL does NOT weaken this gate — a maigret
     hit on a URL-derived handle still has to pass the name test.

     Corroboration requires an INDEPENDENT anchor, and two cases are therefore
     explicitly NOT corroboration:
       * a handle MANUFACTURED from the contact's name (name_handle_variants).
         The pivot and the check would be the same signal, so any namesake
         passes trivially. Those hits are returned with circular_anchor=True
         and zero corroboration weight; the raw measurement is kept under
         name_shared_tokens_raw / family_present_raw.
       * a hand-entered URL on its own. It is an assertion about which account
         belongs to the contact, not verification of what some third-party
         profile says. Alone it yields identity 'low' (below the write gate);
         combined with one name-corroborated site it yields 'high'.
     A curated URL whose FETCHED name names someone else is marked
     name_conflict and is excluded from anchors and enrichment entirely.
  6. FALLS BACK to a capped SearXNG name+org / name+occupation search when the
     handle pivot corroborates nothing. A candidate that is never opened cannot
     corroborate anything, so raw snippets are returned as UNVERIFIED CANDIDATES
     and neither raise the identity level nor produce enrichment. A candidate
     whose page IS fetched and whose text names the contact — given and family
     name adjacent, not merely both present somewhere on the page — meets the
     same corroboration standard as any other profile and does count. Those
     pages appear in identity.corroborating_sites.
  7. Probes the sources that reach a contact with NO handle and NO profile
     anywhere — the population this pipeline fails on. Each is fail-soft and
     each produces CANDIDATES that face the same name gate as everything else:
       * WHOIS/RDAP on a VANITY domain (one the contact owns, which is exactly
         where employer_from_email returns ""). Most registrations are
         privacy-proxied, and a proxied record is discarded whole rather than
         reported: the phone and city in it are the registrar's, and writing
         them would put a wrong number and a wrong city on every contact whose
         registrar happens to be the same. A record only becomes an anchor when
         the registrant NAME passes _name_confirms, and only then are its second
         email address and phone number reported at all.
       * The WAYBACK MACHINE, when a personal domain no longer resolves. The
         archived page still names them, which is what corroboration needs; a
         dead domain is never published as a live website.
       * EMAIL PERMUTATION at an employer domain (first.last@, flast@,
         firstl@, first@, f.last@), tested for existence with holehe. Corporate
         domains only. holehe proves a mailbox exists, never whose it is, so
         these never raise the identity level and never source a field.
       * PHONE INTELLIGENCE from libphonenumber: region, carrier, line type and
         timezone. Numbers are portable, so the region corroborates a city
         already on file and never establishes one.
  8. Reaches the contacts holding an EMPLOYER NAME and nothing else — no
     address, no profile URL — which is most of the population this pipeline
     fails on. The employer name is resolved to a company DOMAIN (a colleague's
     observed address, a search hit named after the company, or the obvious
     guess — always fetched and required to name the company, because a wrong
     domain is consumed by everything below it). That domain then unlocks the
     employer's own team/about page, a site: filter on the employer, and the
     address permutation that previously could only run for contacts who
     already had a corporate address. A GitHub account that passed the identity
     gate also yields the address its commits are authored from.
  9. Emits scout Findings (finding_id / claim / confidence / source_refs) plus
     structured enrichment fields, each with provenance.

Enrichment fields are drawn ONLY from structured sources (GitHub API company /
location, profile blog_url, pronouns parsed from bios, hand-entered URLs).
Free-text bios and search snippets are surfaced as evidence with quotes —
never regex-scraped into employer fields (that was the old failure mode).
Confidence gates whether the caller writes.

Website selection is ranked, not first-wins: personal domain > github blog >
professional profile (LinkedIn/Crunchbase) > portfolio (Behance/Dribbble/
Medium) > consumer social (Snapchat/TikTok/Duolingo/Chess) last.

Stdlib + subprocess only. Network egress happens inside maigret/holehe, the
GitHub API call, the optional page-title fetch, and the local SearXNG query.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _normalize import fold_accents, normalize_name, token_overlap_ratio

def _resolve_osint_venv():
    """The isolated holehe/maigret venv, FOUND rather than assumed.

    AGENT_ROOT names a PROFILE directory (<hermes>/profiles/<name>) in the
    scheduled wrapper, while the OSINT venv lives under the hermes home shared
    by every profile. Deriving the path from AGENT_ROOT alone therefore made
    both tools report status 'not_installed' on every scheduled run, while the
    same code found them when run by hand with no AGENT_ROOT set — so the
    handle sweep and the email-existence probe were silently no-ops in
    production and looked healthy in testing. The tools were never missing; the
    path was. Candidates are tried in order and the first one that actually
    holds the binaries wins; an explicit SCOUT_OSINT_VENV always overrides.
    """
    explicit = os.environ.get("SCOUT_OSINT_VENV")
    if explicit:
        return explicit
    seen, cands = set(), []
    for base in (os.environ.get("AGENT_ROOT"), os.environ.get("HERMES_HOME"),
                 os.path.join(os.path.expanduser("~"), ".hermes")):
        if not base:
            continue
        base = str(base).rstrip("/")
        # the directory itself, then its grandparent (<hermes>/profiles/<name>)
        for root in (base, os.path.dirname(os.path.dirname(base))):
            if not root:
                continue
            p = os.path.join(root, "tools", "osint-venv")
            if p not in seen:
                seen.add(p)
                cands.append(p)
    for p in cands:
        if os.path.exists(os.path.join(p, "bin", "maigret")):
            return p
    return cands[0] if cands else os.path.join(
        os.path.expanduser("~"), ".hermes", "tools", "osint-venv")


OSINT_VENV = _resolve_osint_venv()
MAIGRET_BIN = f"{OSINT_VENV}/bin/maigret"
HOLEHE_BIN = f"{OSINT_VENV}/bin/holehe"

# Pinned to 127.0.0.1 on purpose: 'localhost' can resolve to ::1 on this box
# and the SearXNG container only listens on IPv4 (cf. the Wikipedia IPv6 case).
SEARXNG_URL = os.environ.get("SCOUT_SEARXNG_URL", "http://127.0.0.1:8888/search")

# Hard caps so a fallback search cannot multiply into ~990 outbound sweeps.
MAX_SEARCH_QUERIES = 3
MAX_SEARCH_CANDIDATES = 12
MAX_SEARCH_VERIFY = 6   # candidates actually fetched and name-checked
MAX_MAIGRET_HANDLES = 3
# Each permutation costs a full holehe run, so the cheap shapes only.
MAX_EMAIL_PERMUTATIONS = 3

GENERIC_EMAIL_LOCALS = {
    "info", "support", "webmaster", "admin", "hello", "contact", "noreply",
    "no-reply", "privacy", "sales", "press", "office", "mail", "team", "help",
    "jobs", "careers", "abuse", "postmaster", "security", "billing", "service",
    "feedback", "newsletter",
}
# NOTE: a common-but-personal handle (e.g. 'geekgirl') is NOT blocklisted —
# cross-source name corroboration is what rejects it: maigret will find many
# 'geekgirl' profiles, but none reporting the contact's name, so identity
# resolves to 'none' and nothing is written. That is the real discriminator,
# not a hardcoded denylist.

# Enrichment fields we are willing to write from structured sources.
_PRONOUN_RE = re.compile(
    r"\b(she/her|he/him|they/them|she/they|he/they|ze/zir|xe/xem)\b", re.IGNORECASE
)

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

# --------------------------------------------------------------------------
# Profile-URL parsing
# --------------------------------------------------------------------------
# host suffix -> (platform label, path regex capturing a username, maigret_ok)
_URL_HANDLE_RULES = (
    ("linkedin.com", "LinkedIn", r"^/in/([^/?#]+)", True),
    ("github.com", "GitHub", r"^/([A-Za-z0-9][A-Za-z0-9\-]*)/?$", True),
    ("gitlab.com", "GitLab", r"^/([A-Za-z0-9][A-Za-z0-9._\-]*)/?$", True),
    ("twitter.com", "Twitter", r"^/([A-Za-z0-9_]+)/?$", True),
    ("x.com", "Twitter", r"^/([A-Za-z0-9_]+)/?$", True),
    ("instagram.com", "Instagram", r"^/([A-Za-z0-9_.]+)/?$", True),
    ("medium.com", "Medium", r"^/@([A-Za-z0-9_.\-]+)/?$", True),
    ("tiktok.com", "TikTok", r"^/@([A-Za-z0-9_.]+)/?$", True),
    ("dribbble.com", "Dribbble", r"^/([A-Za-z0-9_\-]+)/?$", True),
    ("behance.net", "Behance", r"^/([A-Za-z0-9_\-]+)/?$", True),
    ("keybase.io", "Keybase", r"^/([A-Za-z0-9_]+)/?$", True),
    ("reddit.com", "Reddit", r"^/u(?:ser)?/([A-Za-z0-9_\-]+)", True),
    ("about.me", "AboutMe", r"^/([A-Za-z0-9_.\-]+)/?$", True),
    # Handle exists but is not a maigret username (domain-shaped / numeric).
    ("bsky.app", "Bluesky", r"^/profile/([^/?#]+)", False),
    ("facebook.com", "Facebook", r"^/([A-Za-z0-9_.]+)/?$", False),
    ("crunchbase.com", "Crunchbase", r"^/person/([^/?#]+)", False),
    ("scholar.google.com", "GoogleScholar", r"", False),
    ("orcid.org", "ORCID", r"", False),
)

# Website-ranking host classes. Unknown host => treated as a personal domain.
_PROFESSIONAL_HOSTS = {
    "linkedin.com", "crunchbase.com", "angel.co", "wellfound.com", "xing.com",
    "researchgate.net", "orcid.org", "scholar.google.com", "stackoverflow.com",
    "github.com", "gitlab.com", "keybase.io",
}
_PORTFOLIO_HOSTS = {
    "behance.net", "dribbble.com", "medium.com", "substack.com",
    "artstation.com", "deviantart.com", "vimeo.com", "about.me", "carrd.co",
    "read.cv", "contra.com", "wordpress.com", "blogspot.com", "ghost.io",
    "hashnode.dev", "dev.to", "notion.site", "cargo.site", "squarespace.com",
}
_CONSUMER_SOCIAL_HOSTS = {
    "snapchat.com", "tiktok.com", "picsart.com", "duolingo.com", "chess.com",
    "instagram.com", "facebook.com", "pinterest.com", "twitter.com", "x.com",
    "reddit.com", "tumblr.com", "spotify.com", "last.fm", "twitch.tv",
    "steamcommunity.com", "vk.com", "myspace.com", "roblox.com", "discord.com",
    "t.me", "telegram.me", "youtube.com", "soundcloud.com", "flickr.com",
    "goodreads.com", "quora.com", "9gag.com", "imgur.com", "letterboxd.com",
    "strava.com", "untappd.com", "venmo.com", "cash.app", "bsky.app",
}

# Ordering knobs for website selection (lower is better).
_HOST_RANK_PERSONAL = 0
_HOST_RANK_PROFESSIONAL = 2
_HOST_RANK_PORTFOLIO = 3
_HOST_RANK_CONSUMER = 4
_KIND_RANK = {"curated": 0, "github_blog": 1, "profile_blog": 2, "profile_url": 3}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _host_of(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
    except Exception:  # noqa: BLE001
        return ""
    host = host.split("@")[-1].split(":")[0]
    host = host.removeprefix("www.")
    return host


def _host_matches(host, suffix):
    return host == suffix or host.endswith("." + suffix)


def _host_class(host):
    """0 personal / 2 professional / 3 portfolio / 4 consumer-social."""
    if not host:
        return _HOST_RANK_PERSONAL
    for s in _CONSUMER_SOCIAL_HOSTS:
        if _host_matches(host, s):
            return _HOST_RANK_CONSUMER
    for s in _PORTFOLIO_HOSTS:
        if _host_matches(host, s):
            return _HOST_RANK_PORTFOLIO
    for s in _PROFESSIONAL_HOSTS:
        if _host_matches(host, s):
            return _HOST_RANK_PROFESSIONAL
    return _HOST_RANK_PERSONAL


def rank_website_candidate(url, kind="profile_url"):
    """Sort key for a website candidate — LOWER is better.

    Ranking (requirement): personal domain > github blog > professional
    profile > portfolio > consumer social. Consumer-social URLs (Snapchat,
    Duolingo, Chess.com, Picsart) must never beat a real site.
    """
    return (_host_class(_host_of(url)), _KIND_RANK.get(kind, 3))


def pick_website(candidates):
    """candidates: iterable of (url, kind, source_url). Returns best or None."""
    best = None
    best_key = None
    for idx, cand in enumerate(candidates):
        url = (cand[0] or "").strip()
        if not url:
            continue
        kind = cand[1] if len(cand) > 1 else "profile_url"
        key = rank_website_candidate(url, kind) + (idx,)
        if best_key is None or key < best_key:
            best_key = key
            best = cand
    return best


def parse_profile_url(url):
    """Classify a URL from the contact record.

    Returns {url, platform, handle, maigret_ok, kind} or None for junk.
    kind is 'profile' for a recognised platform, 'website' otherwise.
    """
    url = (url or "").strip()
    if not url:
        return None
    if not re.match(r"^https?://", url, re.IGNORECASE):
        if re.match(r"^[\w.-]+\.[A-Za-z]{2,}(/|$)", url):
            url = "https://" + url
        else:
            return None
    host = _host_of(url)
    if not host or "." not in host:
        return None
    try:
        path = urllib.parse.urlparse(url).path or "/"
    except Exception:  # noqa: BLE001
        return None

    for suffix, platform, pattern, maigret_ok in _URL_HANDLE_RULES:
        if not _host_matches(host, suffix):
            continue
        handle = ""
        if pattern:
            m = re.match(pattern, path)
            if m:
                handle = urllib.parse.unquote(m.group(1)).strip().strip("/")
        return {"url": url, "platform": platform, "handle": handle,
                "maigret_ok": bool(maigret_ok and handle), "kind": "profile"}

    return {"url": url, "platform": "Website", "handle": "",
            "maigret_ok": False, "kind": "website"}


def _handle_ok(handle, min_len=5):
    if not handle:
        return False
    if not re.fullmatch(r"[A-Za-z0-9._\-]+", handle):
        return False
    if handle.isdigit():
        return False
    return len(re.sub(r"[._\-]", "", handle)) >= min_len


def _slug_variants(handle):
    """Handle plus useful rewrites: squashed, and LinkedIn's -<id> stripped."""
    out = []
    h = (handle or "").strip().lower()
    if not h:
        return out

    def _add(v):
        if v and v not in out:
            out.append(v)

    _add(h)
    # LinkedIn slugs often carry a disambiguating id: 'john-smith-1a2b3c4'.
    trimmed = re.sub(r"-[0-9a-f]{6,}$", "", h)
    if trimmed != h:
        _add(trimmed)
    for v in out:
        _add(re.sub(r"[._\-]", "", v))
    return out


def handles_from_urls(urls):
    """maigret-usable handle candidates derived from known profile URLs."""
    out = []
    for u in urls or []:
        parsed = parse_profile_url(u)
        if not parsed or not parsed["maigret_ok"]:
            continue
        for v in _slug_variants(parsed["handle"]):
            if _handle_ok(v) and v not in out:
                out.append(v)
    return out


def _email_local(email):
    email = (email or "").strip().lower()
    if "@" not in email:
        return ""
    return email.split("@", 1)[0].split("+", 1)[0]


def email_handle_variants(email):
    """Distinctive handle candidates from an email local part.

    Generic / short locals yield [] — probing 'info' manufactures wrong people.
    """
    local = _email_local(email)
    if not local or len(local) < 5 or local in GENERIC_EMAIL_LOCALS:
        return []
    variants = [local]
    squashed = re.sub(r"[._-]", "", local)
    if squashed != local and len(squashed) >= 5 and squashed not in variants:
        variants.append(squashed)
    return variants


def _split_name(name, name_given="", name_family=""):
    # Fold accents before any stripping. [^A-Za-z0-9] treats an accented letter as
    # punctuation and deletes it, so an accented given name lost the letter and
    # found in real text. Folding first keeps the base letter: oisin.
    name = fold_accents(name)
    name_given = fold_accents(name_given)
    name_family = fold_accents(name_family)
    given = (name_given or "").strip()
    family = (name_family or "").strip()
    if not (given and family):
        toks = [t for t in re.split(r"\s+", (name or "").strip()) if t]
        toks = [re.sub(r"[^A-Za-z0-9\-']", "", t) for t in toks]
        toks = [t for t in toks if t]
        if len(toks) >= 2:
            given = given or toks[0]
            family = family or toks[-1]
    given = re.sub(r"[^A-Za-z0-9]", "", given).lower()
    family = re.sub(r"[^A-Za-z0-9]", "", family).lower()
    return given, family


def name_handle_variants(name, name_given="", name_family=""):
    """Candidate handles built from the contact's name.

    These are only CANDIDATES — the same cross-source name-corroboration gate
    still decides whether any resulting profile counts. Used when the email
    handle is generic or absent (see research_person).
    """
    given, family = _split_name(name, name_given, name_family)
    if not given or not family:
        return []
    # Deliberately short: each surviving candidate costs a full maigret sweep
    # (~200s). first+last and first.last carry almost all the yield; last+first
    # and the underscore form are noise.
    raw = [
        f"{given}{family}",
        f"{given}.{family}",
        f"{given[0]}{family}",
    ]
    out = []
    for v in raw:
        if _handle_ok(v) and v not in out:
            out.append(v)
    return out


def _run(cmd, timeout):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except FileNotFoundError as e:
        return 127, "", str(e)


def run_maigret(handle, timeout=200, top_sites=300):
    """Return {site_name: {url, fullname, location, bio, blog_url}} for CLAIMED
    profiles of `handle`. Second value is a PersonToolRecord."""
    rec = {"tool_name": "maigret", "invoked_at": _now(), "input_type": "handle",
           "input_value": handle, "status": "error", "findings_count": 0,
           "error": None}
    if not Path(MAIGRET_BIN).exists():
        rec["status"] = "not_installed"
        rec["error"] = f"{MAIGRET_BIN} missing"
        return {}, rec

    outdir = tempfile.mkdtemp(prefix="maigret_")
    cmd = [MAIGRET_BIN, handle, "--no-recursion", "--no-progressbar",
           "--top-sites", str(top_sites), "--timeout", "8",
           "--json", "simple", "--folderoutput", outdir]
    code, _out, err = _run(cmd, timeout)
    report = Path(outdir) / f"report_{handle}_simple.json"
    if code == 124:
        rec["status"] = "timeout"
    if not report.exists():
        rec["error"] = (err or "no report")[:200]
        return {}, rec

    try:
        data = json.loads(report.read_text())
    except Exception as e:  # noqa: BLE001
        rec["error"] = f"parse: {e}"
        return {}, rec

    profiles = {}
    for site, info in data.items():
        st = info.get("status")
        if not isinstance(st, dict) or st.get("status") != "Claimed":
            continue
        ids = st.get("ids", {}) if isinstance(st.get("ids"), dict) else {}
        profiles[site] = {
            "url": info.get("url_user", ""),
            "fullname": (ids.get("fullname") or "").strip(),
            "location": (ids.get("location") or "").strip(),
            "bio": (ids.get("bio") or "").strip(),
            "blog_url": (ids.get("blog_url") or ids.get("url") or "").strip(),
        }
    rec["status"] = "success"
    rec["findings_count"] = len(profiles)
    return profiles, rec


def run_holehe(email, timeout=120):
    """Return (list of sites the email is registered on, PersonToolRecord)."""
    rec = {"tool_name": "holehe", "invoked_at": _now(), "input_type": "email",
           "input_value": email, "status": "error", "findings_count": 0,
           "error": None}
    if not Path(HOLEHE_BIN).exists():
        rec["status"] = "not_installed"
        rec["error"] = f"{HOLEHE_BIN} missing"
        return [], rec
    code, out, err = _run([HOLEHE_BIN, email, "--only-used", "--no-color"], timeout)
    if code == 124:
        rec["status"] = "timeout"
        return [], rec
    sites = []
    # A real hit line is "[+] <domain>". Guard against progress-bar / legend
    # text ("[x] Rate limit", "Email used") leaking into the site list: keep
    # only single tokens that look like domains.
    for line in out.splitlines():
        line = line.strip()
        if not line.startswith("[+]"):
            continue
        token = line[3:].strip()
        if " " in token or "." not in token:
            continue
        sites.append(token)
    rec["status"] = "success"
    rec["findings_count"] = len(sites)
    return sites, rec


def github_api_fields(handle, timeout=8):
    """Structured identity fields from api.github.com/users/<handle>, or {}."""
    url = f"https://api.github.com/users/{handle}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "hermes-scout/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return {}
            d = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return {}
    if not isinstance(d, dict) or "login" not in d or d.get("message"):
        return {}
    out = {}
    if d.get("name"):
        out["fullname"] = d["name"].strip()
    company = (d.get("company") or "").strip().lstrip("@")
    if company:
        out["org"] = company
    if d.get("location"):
        out["location"] = d["location"].strip()
    if d.get("blog"):
        out["blog_url"] = d["blog"].strip()
    if d.get("bio"):
        out["bio"] = d["bio"].strip()
    return out



_BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def fetch_page_html(url, timeout=10, max_bytes=400_000):
    """Raw markup of a page, or "". For the few callers that need the LINKS.

    Text extraction throws hrefs away, and finding where a company lists its
    people means reading its own navigation.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _BROWSER_UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read(max_bytes).decode("utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return ""


def extract_page_text(raw):
    """(title, body) from markup. Shared so an ARCHIVED copy of a page is read
    by exactly the same code as the live one."""
    m = _TITLE_RE.search(raw or "")
    title = ""
    if m:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()[:200]
    body = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw or "")
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    return title, body[:20000]


# Categories that must never be attributed to a contact. weave already refuses
# to write them; scout refuses to REPORT them, so a single missing filter
# downstream cannot put an adult or gambling account on a real person's record.
# This pipeline has made exactly that mistake before.
_SENSITIVE_ACCOUNT_SITES = (
    "porn", "xvideos", "xnxx", "xhamster", "redtube", "youporn", "onlyfans",
    "fansly", "chaturbate", "stripchat", "livejasmin", "cam4", "brazzers",
    "adultfriendfinder", "ashleymadison", "fetlife", "grindr", "scruff",
    "hornet", "tinder", "bumble", "hinge", "okcupid", "plentyoffish",
    "seekingarrangement", "casino", "poker", "bet365", "gambling", "bovada",
)

# An address's OWN mail provider is not an account somewhere else. Measured: a
# control address at outlook.com that cannot exist was reported as registered
# on Office 365, which is only a restatement of the domain.
_PROVIDER_ECHOES = {
    "office365": ("outlook.", "hotmail.", "live.", "msn.", "microsoft."),
    "microsoft": ("outlook.", "hotmail.", "live.", "msn.", "microsoft."),
    "gmail": ("gmail.", "googlemail."),
    "google": ("gmail.", "googlemail."),
    "yahoo": ("yahoo.", "ymail."),
    "apple": ("icloud.", "me.com", "mac.com"),
    "icloud": ("icloud.", "me.com", "mac.com"),
}


def _account_site_ok(site, email=""):
    """False for a category never attributed to a person, or a provider echo."""
    s = (site or "").strip().lower()
    if not s:
        return False
    if any(k in s for k in _SENSITIVE_ACCOUNT_SITES):
        return False
    host = (email or "").strip().lower().rsplit("@", 1)[-1]
    root = s.split(".")[0]
    for label, domains in _PROVIDER_ECHOES.items():
        if root == label and any(host.startswith(d) or host == d.rstrip(".")
                                 for d in domains):
            return False
    return True


USER_SCANNER_BIN = f"{OSINT_VENV}/bin/user-scanner"


def run_user_scanner(email, timeout=240, concurrency=25):
    """(sites the address is registered on, PersonToolRecord).

    A SECOND account-existence source alongside holehe, adopted on measurement
    rather than on its README. Benchmarked on 20 real addresses from this
    address book: holehe found 42 accounts in total, this found 293, of which
    261 were ones holehe missed and 10 were ones only holehe found; both took
    about eleven seconds per address. Four control addresses that cannot exist
    produced no hits from holehe and one from this tool — an Office 365 hit on
    an outlook.com address, which restates the address's own mail provider and
    is filtered by _account_site_ok. Neither tool replaces the other.

    --hudson is NEVER passed: that flag queries an infostealer/breach corpus,
    a different category from public-web OSINT and not authorised here.
    --allow-loud is never passed either, so the checks that would email the
    subject stay skipped, which is the package's own default.
    """
    rec = {"tool_name": "user_scanner", "invoked_at": _now(),
           "input_type": "email", "input_value": email, "status": "error",
           "findings_count": 0, "error": None}
    if not email or "@" not in email:
        rec["error"] = "not an email"
        return [], rec
    if not Path(USER_SCANNER_BIN).exists():
        rec["status"] = "not_installed"
        rec["error"] = f"{USER_SCANNER_BIN} missing"
        return [], rec
    import glob as _glob
    import shutil as _shutil
    workdir = tempfile.mkdtemp(prefix="scout-us-")
    base = os.path.join(workdir, "scan")
    try:
        code, _out, err = _run(
            [USER_SCANNER_BIN, "-e", email, "-f", "json", "-o", base,
             "-C", str(concurrency), "-t", "10"], timeout)
        if code == 124:
            rec["status"] = "timeout"
            return [], rec
        data = None
        for path in sorted(_glob.glob(base + "*")):
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
                break
            except Exception:  # noqa: BLE001
                continue
        if not isinstance(data, list):
            rec["error"] = (err or "no json output")[:200]
            return [], rec
        sites, seen = [], set()
        for row in data:
            if not isinstance(row, dict):
                continue
            if str(row.get("status", "")).strip().lower() != "registered":
                continue
            host = _host_of(row.get("url") or "")
            site = host or re.sub(r"\s+", "",
                                  str(row.get("site_name", "")).lower())
            if not site or site in seen:
                continue
            seen.add(site)
            sites.append(site)
        rec["status"] = "success"
        rec["findings_count"] = len(sites)
        return sites, rec
    except Exception as e:  # noqa: BLE001
        rec["error"] = str(e)[:200]
        return [], rec
    finally:
        try:
            _shutil.rmtree(workdir, ignore_errors=True)
        except Exception:  # noqa: BLE001
            pass


def fetch_page_text(url, timeout=10, max_bytes=300_000, with_raw=False):
    """Title + visible text of a page, for name corroboration.

    The default 2-tuple return is unchanged, so every existing caller keeps
    working. `with_raw=True` additionally hands back the HTML, because the page
    has already been paid for and the contact fields inside it (a tel: link, a
    mailto:, a schema.org address, an outbound profile link) are thrown away
    otherwise. Extraction itself stays in mine_contact_fields, which validates
    every value — this function still does no attribution of its own.
    """
    raw = fetch_page_html(url, timeout=timeout, max_bytes=max_bytes)
    if not raw:
        return ("", "", "") if with_raw else ("", "")
    title, body = extract_page_text(raw)
    return (title, body, raw) if with_raw else (title, body)




# Roles that make a <title> tail a plausible job title rather than a tagline.
_ROLE_WORDS = (
    "leader", "director", "manager", "engineer", "designer", "founder",
    "co-founder", "ceo", "cto", "coo", "cfo", "head", "principal", "lead",
    "architect", "developer", "analyst", "consultant", "writer", "editor",
    "producer", "researcher", "scientist", "professor", "advisor", "strategist",
    "president", "officer", "partner", "owner", "specialist", "coordinator",
    "photographer", "illustrator", "artist", "therapist", "attorney", "counsel",
)
_TITLE_SEP = re.compile("\\s+[|\u2013\u2014\u00b7:]+\\s+|\\s+-\\s+")
_HREF_RE = re.compile("href\\s*=\\s*[\"\']([^\"\']+)[\"\']", re.IGNORECASE)
_DESC_RE = re.compile("(?is)<meta[^>]+name=[\"\']description[\"\'][^>]+content=[\"\']([^\"\']+)")
_OGTITLE_RE = re.compile("(?is)<meta[^>]+property=[\"\']og:title[\"\'][^>]+content=[\"\']([^\"\']+)")
# Template placeholders, never real addresses.
_PLACEHOLDER_EMAILS = {"user@domain.com", "you@example.com", "name@email.com",
                       "email@example.com", "your@email.com", "info@domain.com"}


def mine_personal_site(url, name, timeout=12, max_bytes=400_000,
                       region_hint="US"):
    """Harvest a contact's OWN site, once it is confirmed to name them.

    A link the subject publishes on their own site is an assertion BY them, so
    profile links found here are accepted without a separate name match —
    unlike a link found on a third party's page. That is why this runs only
    after the site has corroborated the contact's name.

    The <title> tail is read as a job title only when it actually looks like
    one; prose is otherwise left alone, because mining arbitrary text for an
    employer is what previously produced nonsense values.
    """
    out = {"links": [], "occupation": None, "tagline": None, "emails": [],
           "phones": [], "cities": [], "linkedin": [], "websites": []}
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(max_bytes).decode("utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return out

    # The page is confirmed to be the contact's before this function is called,
    # so everything mined here is FIRST-PARTY: the contact published it about
    # themselves. That is the strongest tie available for a LinkedIn URL (see
    # linkedin_tie) and the only context in which a phone number found on a page
    # may be attributed to a person at all.
    try:
        _t, _b = extract_page_text(raw)
        _mined = mine_contact_fields(raw, _t + " " + _b, name,
                                     region_hint=region_hint, page_url=url)
        out["phones"] = _mined["phones"]
        out["cities"] = _mined["cities"]
        out["linkedin"] = _mined["linkedin"]
        out["websites"] = _mined["websites"]
    except Exception:  # noqa: BLE001
        pass

    seen = set()
    site_host = _host_of(url)
    for m in _HREF_RE.finditer(raw):
        u = m.group(1).split("#")[0].split("?")[0].strip()
        if not u.startswith("http") or _host_of(u) == site_host:
            continue
        parsed = parse_profile_url(u)
        if not parsed or not parsed.get("handle"):
            continue
        key = (parsed["platform"], (parsed["handle"] or "").lower())
        if key in seen:
            continue
        seen.add(key)
        out["links"].append(parsed)

    tm = _TITLE_RE.search(raw)
    title = ""
    if tm:
        title = re.sub("\\s+", " ", re.sub("<[^>]+>", " ", tm.group(1))).strip()
    if not title:
        om = _OGTITLE_RE.search(raw)
        if om:
            title = re.sub("\\s+", " ", om.group(1)).strip()
    if title:
        name_toks = set(normalize_name(name).split())
        for part in [x.strip() for x in _TITLE_SEP.split(title) if x.strip()]:
            if set(normalize_name(part).split()) & name_toks:
                continue                        # this fragment is the name
            low = part.lower()
            if any(w in low for w in _ROLE_WORDS) and 3 < len(part) <= 70:
                out["occupation"] = part
                break

    dm = _DESC_RE.search(raw)
    if dm:
        tag = re.sub("\\s+", " ", dm.group(1)).strip()
        if 3 < len(tag) <= 200:
            out["tagline"] = tag

    for em in set(re.findall("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}", raw)):
        low = em.lower()
        if low in _PLACEHOLDER_EMAILS:
            continue
        if low.endswith((".png", ".jpg", ".svg", ".css", ".js")):
            continue
        if low.split("@")[1] in ("example.com", "domain.com", "email.com"):
            continue
        out["emails"].append(low)
    return out


def gravatar_profile(email, timeout=10):
    """Gravatar profile for an email address, or None.

    Gravatar is keyed on the md5 of the address itself, so a hit is bound to
    THIS email rather than inferred from a name — stronger provenance than any
    name match. The displayName is often just a handle, so it is reported but
    never trusted as the person's real name.
    """
    if not email or "@" not in email:
        return None
    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        req = urllib.request.Request(
            "https://www.gravatar.com/%s.json" % h,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except Exception:  # noqa: BLE001
        return None
    entry = (d.get("entry") or [{}])[0]
    if not entry:
        return None
    name = (entry.get("displayName")
            or (entry.get("name") or {}).get("formatted") or "").strip()
    return {
        "display_name": name,
        "location": (entry.get("currentLocation") or "").strip(),
        "bio": (entry.get("aboutMe") or "").strip(),
        "accounts": [a.get("url") for a in (entry.get("accounts") or []) if a.get("url")],
        "urls": [u.get("value") for u in (entry.get("urls") or []) if u.get("value")],
        "profile_url": entry.get("profileUrl") or "",
    }


def email_domain_site(email):
    """A personal-domain email is a website hiding in plain sight.

    'ana@anaperez.example' -> https://anaperez.example. Returns None for
    consumer/webmail and obvious corporate shared domains, where the domain
    says nothing about which individual owns the mailbox.
    """
    if not email or "@" not in email:
        return None
    dom = email.split("@", 1)[1].strip().lower().rstrip(".")
    if not dom or "." not in dom:
        return None
    if dom in FREEMAIL_DOMAINS:
        return None
    return "https://" + dom


FREEMAIL_DOMAINS = {
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.co.uk", "hotmail.com",
    "outlook.com", "live.com", "msn.com", "aol.com", "icloud.com", "me.com",
    "mac.com", "proton.me", "protonmail.com", "gmx.com", "mail.com",
    "fastmail.com", "zoho.com", "yandex.com", "qq.com", "163.com", "126.com",
    "comcast.net", "sbcglobal.net", "verizon.net", "att.net", "cox.net",
    "aim.com", "earthlink.net", "juno.com", "mailinator.com", "example.com",
}


def fetch_page_title(url, timeout=10, max_bytes=200_000):
    """Cheapest possible read of a personal site: just the <title>. '' on any
    failure. Deliberately NOT a scraper — no body text is extracted, so there
    is nothing for a regex to mis-attribute into an employer field."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(max_bytes).decode("utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return ""
    m = _TITLE_RE.search(raw)
    if not m:
        return ""
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()
    return title[:200]


def searxng_search(query, limit=5, searxng_url=None, retries=1, timeout=15):
    """Query the local SearXNG. Returns [{url,title,content}] — [] on failure.

    Unlike weave's copy this does NOT raise: scout degrades to "no candidates"
    rather than failing a whole contact when the container is bouncing. 429 is
    treated as fail-fast (no retry) so a 990-contact run cannot hammer it.
    """
    base = (searxng_url or SEARXNG_URL).rstrip("/")
    if not base.endswith("/search"):
        base = base + "/search"
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": limit})
    url = f"{base}?{params}"
    for attempt in range(retries + 1):
        if attempt:
            time.sleep(1.5 * (2 ** (attempt - 1)))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HermesAgent/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
            return [
                {"url": i.get("url", ""), "title": i.get("title", ""),
                 "content": i.get("content", "")}
                for i in (data.get("results") or [])[:limit]
            ]
        except urllib.error.HTTPError as e:
            if getattr(e, "code", 0) == 429:
                return []
        except Exception:  # noqa: BLE001
            continue
    return []


_FREE_MAIL_HOSTS = (
    "gmail.", "googlemail.", "yahoo.", "ymail.", "hotmail.", "outlook.", "live.",
    "msn.", "aol.", "icloud.", "me.com", "mac.com", "proton", "pm.me", "fastmail",
    "hey.com", "zoho.", "gmx.", "web.de", "mail.ru", "comcast.", "verizon.",
    "att.net", "sbcglobal.", "cox.net", "earthlink.", "yandex.", "qq.com",
    "163.com", "126.com", "naver.", "duck.com", "tutanota.", "posteo.",
)


def phone_search_forms(phone):
    """The ways a phone number is written on a page, for exact-phrase search.

    A phone number is the most nearly unique field a contact record holds, and
    it was going unused: research_person accepted `phone` and only recorded it
    as a finding. Half the contacts this pipeline fails on have one.

    A national form that omits the country code can be too short to identify a
    line (+45 61 77 06 99 -> '61 77 06 99'), so it only leads when it carries
    10+ digits; otherwise the international form goes first.
    """
    raw = (phone or "").strip()
    if not raw:
        return []
    try:
        import phonenumbers as _pn
    except Exception:
        return []
    for region in (None, "US"):
        try:
            p = _pn.parse(raw, region)
        except Exception:
            continue
        if not _pn.is_valid_number(p):
            continue
        nat = _pn.format_number(p, _pn.PhoneNumberFormat.NATIONAL)
        intl = _pn.format_number(p, _pn.PhoneNumberFormat.INTERNATIONAL)
        e164 = _pn.format_number(p, _pn.PhoneNumberFormat.E164)
        dashed = re.sub(r"[()\s]+", "-", nat).strip("-")
        # The shapes a number is actually WRITTEN in, beyond the library's two
        # canonical forms. Compared against a published variant generator: the
        # separator-free forms, the dotted form, the spaced form and the
        # national form with its trunk prefix stripped were all missing, and
        # outside North America the trunk prefix is exactly what differs
        # between how a page prints a number and how the library formats it.
        nat_digits = re.sub(r"\D", "", nat)
        spaced = re.sub(r"[.\-]+", " ", re.sub(r"[()]", "", nat))
        spaced = re.sub(r"\s+", " ", spaced).strip()
        dotted = re.sub(r"[\s\-]+", ".", re.sub(r"[()]", "", nat)).strip(".")
        intl_nodashes = intl.replace("-", " ")
        intl_noplus = intl.lstrip("+").strip()
        e164_nodigitsep = e164.lstrip("+")
        # A leading trunk '0' is written by the local convention and omitted by
        # the international one; both spellings occur on real pages.
        nat_no_trunk = nat_digits[1:] if nat_digits.startswith("0") else ""
        extra = [f for f in (spaced, dotted, intl_nodashes, nat_digits,
                             intl_noplus, e164_nodigitsep, nat_no_trunk)
                 if f and len(re.sub(r"\D", "", f)) >= 7]
        order = ((nat, dashed, intl, e164)
                 if len(nat_digits) >= 10 else (intl, e164, nat, dashed))
        out, seen = [], set()
        for f in list(order) + extra:
            f = f.strip()
            if f and f not in seen:
                seen.add(f)
                out.append(f)
        return out[:10]
    return []


def employer_from_email(email, person_name=""):
    """The company a work email address names, or "".

    someone@examplecorp.com names Examplecorp. Free mail says nothing, and a vanity
    domain built from the contact's own name is their site, not their employer.
    """
    email = (email or "").strip().lower()
    if "@" not in email:
        return ""
    dom = email.split("@")[-1].strip()
    if not dom or "." not in dom or any(f in dom for f in _FREE_MAIL_HOSTS):
        return ""
    labels = [part for part in dom.split(".") if part]
    if labels and labels[0] in ("mail", "smtp", "mx", "email"):
        labels = labels[1:]
    if len(labels) < 2:
        return ""
    if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in (
            "co", "com", "org", "net", "ac", "gov", "edu"):
        root = labels[-3]
    else:
        root = labels[-2]
    flat = re.sub(r"[^a-z0-9]", "", root)
    if len(flat) < 3:
        return ""
    parts = [re.sub(r"[^a-z0-9]", "", w.lower())
             for w in re.findall(r"[^\W\d_]+", person_name or "", re.UNICODE)]
    parts = [p for p in parts if len(p) > 2]
    if parts:
        joined = "".join(parts)
        if flat == joined or joined in flat or flat in joined:
            return ""
        if sum(1 for p in parts if p in flat) >= 2:
            return ""
        for p in parts:
            if len(p) >= 4 and flat.startswith(p) and len(flat) > len(p):
                return ""
    return root


# --------------------------------------------------------------------------
# Domain registration (WHOIS / RDAP)
# --------------------------------------------------------------------------
# Measured over a real set of personal domains: a naive parse "yields" a
# registrant phone for 30 of 53 domains and a city for 29 of 53 — and almost
# every one of them belongs to the REGISTRAR, not the person. The large
# resellers each answer with one switchboard number and one head-office city
# for every domain they hold. Writing those would have put a wrong phone
# number and a wrong city on dozens of contacts, which is exactly the
# false-attribution failure this pipeline has already paid for once.
#
# So the record is treated as an ALL-OR-NOTHING block: unless a registrant
# NAME or ORGANISATION survives the privacy-proxy filter, every other field in
# it is discarded too, because there is no evidence the block describes the
# person rather than the reseller. Even then it only becomes an identity anchor
# when the surviving name passes the same name gate every other source faces.
WHOIS_TIMEOUT = 25

# Values a privacy proxy puts where a human's details belong.
_WHOIS_REDACTED_RE = re.compile(
    r"redact|privacy|priv\.?\s*person|proxy|not disclosed|non-public|"
    r"data protected|protection service|withheld|statutory masking|gdpr|"
    r"whoisguard|contact privacy|perfect privacy|domains by proxy|"
    r"registration private|private registration|anonymi[sz]|obscured|masked|"
    r"on behalf of|see (?:the )?registrar|query the|please ask|"
    r"identity shield|domain admin|hostmaster|not available|^n/?a$|^-+$",
    re.IGNORECASE)

# A registrar's own contact block, recognised by its address rather than its
# name: these are the answers the big resellers return for every domain.
_WHOIS_REGISTRAR_CONTACTS = {
    "+1.4806242599", "+1.4165385457", "+1.7147064182", "+1.5707088622",
    "+1.2086851750", "+1.9027492701", "+1.3478717726",
}

# Exact WHOIS keys. Substring matching previously pulled "Registrant Street:"
# into the organisation field; only whole keys are read now.
_WHOIS_KEYS = {
    "registrant name": "registrant_name",
    "registrant": "registrant_name",
    "registrant contact name": "registrant_name",
    "person": "registrant_name",
    "registrant organization": "registrant_org",
    "registrant organisation": "registrant_org",
    "registrant contact organisation": "registrant_org",
    "organization": "registrant_org",
    "registrant email": "registrant_email",
    "registrant contact email": "registrant_email",
    "registrant phone": "registrant_phone",
    "registrant contact phone": "registrant_phone",
    "registrant city": "registrant_city",
    "registrant state/province": "registrant_state",
    "registrant country": "registrant_country",
    "registrar": "registrar",
    "creation date": "created",
    "created": "created",
}
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


def _whois_clean(value):
    """A registrant value, or "" when it is a proxy placeholder / not a value."""
    v = re.sub(r"\s+", " ", (value or "")).strip().strip(".,")
    if not v or len(v) > 120:
        return ""
    if _WHOIS_REDACTED_RE.search(v):
        return ""
    if v.lower().startswith(("http://", "https://", "www.")):
        return ""      # a contact FORM, not an address
    return v


def parse_whois_text(text):
    """Registrant fields from raw WHOIS output, proxy placeholders removed.

    Returns {} when nothing identifies a human, and always reports whether the
    record was redacted so the caller can distinguish "no data" from "no lookup".
    """
    out, raw_seen = {}, False
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.startswith(("%", "#", ">>>")) or ":" not in line:
            continue
        key, _, val = line.partition(":")
        field = _WHOIS_KEYS.get(re.sub(r"\s+", " ", key).strip().lower())
        if not field:
            continue
        raw_seen = True
        clean = _whois_clean(val)
        if not clean:
            continue
        if field == "registrant_email" and not _EMAIL_RE.match(clean):
            continue
        if field == "registrant_phone":
            digits = "+" + re.sub(r"\D", "", clean)
            if digits in _WHOIS_REGISTRAR_CONTACTS or clean in _WHOIS_REGISTRAR_CONTACTS:
                continue
        out.setdefault(field, clean)
    out["_had_fields"] = raw_seen
    # All-or-nothing: with no surviving human name the rest of the block is the
    # registrar's, so it identifies nobody and is dropped rather than reported.
    if not (out.get("registrant_name") or out.get("registrant_org")):
        return {"_had_fields": raw_seen, "redacted": True}
    return out


def rdap_domain(domain, timeout=12):
    """RDAP registrant fields — the fallback for when no whois binary exists."""
    try:
        req = urllib.request.Request(
            "https://rdap.org/domain/" + urllib.parse.quote(domain),
            headers={"User-Agent": "hermes-scout/1.0", "Accept": "application/rdap+json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return {}
    out = {}
    for ent in (data.get("entities") or []):
        if "registrant" not in [str(x).lower() for x in (ent.get("roles") or [])]:
            continue
        for item in (ent.get("vcardArray") or [None, []])[1]:
            try:
                label, _params, _typ, value = item[0], item[1], item[2], item[3]
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(value, str):
                continue
            clean = _whois_clean(value)
            if not clean:
                continue
            if label == "fn":
                out.setdefault("registrant_name", clean)
            elif label == "org":
                out.setdefault("registrant_org", clean)
            elif label == "email" and _EMAIL_RE.match(clean):
                out.setdefault("registrant_email", clean)
            elif label == "tel":
                out.setdefault("registrant_phone", clean)
    if not (out.get("registrant_name") or out.get("registrant_org")):
        return {"redacted": True, "_had_fields": bool(data)}
    out["_had_fields"] = True
    return out


def whois_domain(domain, timeout=WHOIS_TIMEOUT):
    """(registrant fields, PersonToolRecord) for a domain.

    Fail-soft by construction: a missing binary, a timeout or an unparseable
    answer returns ({}, record) and never raises, so one uncooperative registry
    cannot abort a contact's enrichment.
    """
    domain = (domain or "").strip().lower().rstrip(".")
    rec = {"tool_name": "whois", "invoked_at": _now(), "input_type": "domain",
           "input_value": domain, "status": "error", "findings_count": 0,
           "error": None}
    if not domain or "." not in domain:
        rec["error"] = "not a domain"
        return {}, rec
    try:
        import shutil as _shutil
        binpath = _shutil.which("whois")
        text = ""
        if binpath:
            code, out, err = _run([binpath, "--", domain], timeout)
            if code == 124:
                rec["status"] = "timeout"
                rec["error"] = "whois timeout"
                return {}, rec
            text = out or ""
            if err and not text:
                rec["error"] = err[:200]
        fields = parse_whois_text(text) if text else {}
        if not binpath or not fields.get("_had_fields"):
            fields = rdap_domain(domain) or fields
            rec["input_type"] = "domain(rdap)" if not binpath else rec["input_type"]
        fields.pop("_had_fields", None)
        rec["status"] = "success"
        if fields.get("redacted") and len(fields) == 1:
            rec["status"] = "redacted"
            rec["error"] = "registration is privacy-protected"
            return {}, rec
        rec["findings_count"] = len([k for k in fields if not k.startswith("_")])
        return fields, rec
    except Exception as e:  # noqa: BLE001
        rec["error"] = str(e)[:200]
        return {}, rec


def _whois_names(fields):
    """Every spelling of the registrant worth testing against the contact.

    WHOIS commonly stores '<Family>, <Given>', which reads as a different
    person to a last-token comparison, so the flipped form is offered too.
    """
    out = []
    for key in ("registrant_name", "registrant_org"):
        v = (fields.get(key) or "").strip()
        if not v:
            continue
        out.append(v)
        if "," in v:
            a, _, b = v.partition(",")
            flipped = (b.strip() + " " + a.strip()).strip()
            if flipped:
                out.append(flipped)
    return out


def whois_confirms(name, fields):
    """True when the domain's registrant IS the contact (same gate as any URL).

    Deliberately _name_confirms and not _name_agreement: a shared surname is
    how a relative's or a stranger's domain gets attributed. Both cases were
    measured on real data — a domain at the contact's surname registered to a
    different member of that family, and a surname-matching domain belonging to
    an unrelated person — and requiring the given name too rejects both.
    """
    return any(_name_confirms(name, cand) for cand in _whois_names(fields))


# --------------------------------------------------------------------------
# Email permutation against a known EMPLOYER domain
# --------------------------------------------------------------------------
def email_permutations(name, domain, name_given="", name_family="", limit=5):
    """The standard corporate address shapes for a name at a domain.

    Corporate only. Running these at a free-mail host would be guessing at a
    namespace shared by a billion strangers, so callers must pass an employer
    domain (employer_from_email returns "" for personal/vanity domains and the
    caller checks that before getting here).
    """
    dom = (domain or "").strip().lower().lstrip("@").rstrip(".")
    if not dom or "." not in dom or any(f in dom for f in _FREE_MAIL_HOSTS):
        return []
    given, family = _split_name(name, name_given, name_family)
    if not given or not family:
        return []
    shapes = [f"{given}.{family}", f"{given[0]}{family}", f"{given}{family[0]}",
              given, f"{given[0]}.{family}"]
    out = []
    for local in shapes:
        if len(local) < 2:
            continue
        addr = f"{local}@{dom}"
        if addr not in out:
            out.append(addr)
    return out[:limit]


def probe_email_permutations(name, domain, known_email="", name_given="",
                             name_family="", limit=3, timeout=120):
    """Test candidate corporate addresses for existence with holehe.

    Yields CANDIDATES only. holehe reports that an address is registered
    somewhere, which is evidence the mailbox exists — never evidence that it
    belongs to this contact — so nothing here raises the identity level or
    writes a field.
    """
    known = (known_email or "").strip().lower()
    results, recs = [], []
    for addr in email_permutations(name, domain, name_given, name_family,
                                   limit=limit + 1):
        if addr == known:
            continue
        if len(results) >= limit:
            break
        try:
            sites, rec = run_holehe(addr, timeout=timeout)
        except Exception as e:  # noqa: BLE001
            recs.append({"tool_name": "holehe", "invoked_at": _now(),
                         "input_type": "email_permutation", "input_value": addr,
                         "status": "error", "findings_count": 0,
                         "error": str(e)[:200]})
            continue
        rec["input_type"] = "email_permutation"
        recs.append(rec)
        if sites:
            results.append({"email": addr, "sites": sites})
    return results, recs


# --------------------------------------------------------------------------
# Wayback Machine
# --------------------------------------------------------------------------
# The availability API (/wayback/available) was the only source here, and it
# was answering NOTHING. Two separate causes, both measured:
#   * the URL was percent-encoded whole, so the scheme arrived as https%3A%2F%2F
#     and the endpoint rejected it — even a URL it definitely holds;
#   * and once that is corrected the endpoint answers 429 after roughly one
#     request, so a run over an address book gets exactly one lookup and then
#     silently nothing. The failure is invisible because the exception handler
#     turns every error into "no snapshot", which reads identically to "never
#     archived" — which is how a technique reported as the best-performing one
#     could in fact be returning None for every contact.
# The CDX endpoint has neither problem: measured on five dead vanity domains
# that the availability API had just 429'd on, it answered for all five.
_WAYBACK_CDX = "http://web.archive.org/cdx/search/cdx"
_WAYBACK_AVAILABLE = "http://archive.org/wayback/available?url="


def _wayback_url_key(url):
    """The form both Wayback endpoints accept: no scheme, no over-encoding."""
    u = (url or "").strip()
    if not u:
        return ""
    return urllib.parse.quote(u.split("://", 1)[-1].strip("/"), safe="/")


def _wayback_cdx_snapshot(url, timeout=12):
    key = _wayback_url_key(url)
    if not key:
        return None
    api = ("%s?url=%s&output=json&limit=3&filter=statuscode:200"
           "&collapse=urlkey&fl=timestamp,original,statuscode&sort=reverse"
           % (_WAYBACK_CDX, key))
    try:
        req = urllib.request.Request(api, headers={"User-Agent": "hermes-scout/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            rows = json.loads(r.read(200_000).decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return None
    if not isinstance(rows, list) or len(rows) < 2:
        return None
    for row in rows[1:]:
        try:
            timestamp, original = str(row[0]), str(row[1])
        except Exception:  # noqa: BLE001
            continue
        if not timestamp or not original:
            continue
        return {"url": "https://web.archive.org/web/%s/%s" % (timestamp, original),
                "timestamp": timestamp, "status": "200", "source": "wayback"}
    return None


def _wayback_available_snapshot(url, timeout=12):
    key = _wayback_url_key(url)
    if not key:
        return None
    try:
        req = urllib.request.Request(_WAYBACK_AVAILABLE + key,
                                     headers={"User-Agent": "hermes-scout/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return None
    snap = (((data or {}).get("archived_snapshots") or {}).get("closest") or {})
    if not snap.get("available") or not snap.get("url"):
        return None
    return {"url": snap["url"].replace("http://web.archive.org",
                                       "https://web.archive.org"),
            "timestamp": snap.get("timestamp", ""),
            "status": snap.get("status", ""), "source": "wayback"}


def wayback_snapshot(url, timeout=12):
    """Closest archived snapshot of a URL, or None.

    A personal domain that no longer resolves is the commonest way a contact's
    only first-party page disappears. The archive still holds the page that
    named them, which is what identity corroboration actually needs.

    CDX first (see above), the availability API only as a fallback.
    """
    if not (url or "").strip():
        return None
    return (_wayback_cdx_snapshot(url, timeout=timeout)
            or _wayback_available_snapshot(url, timeout=timeout))


# --------------------------------------------------------------------------
# Common Crawl — a second archive, for the pages Wayback never captured
# --------------------------------------------------------------------------
# Wayback is the best-measured technique in this pipeline (of the vanity domains
# that no longer resolve, all were archived and several still named the
# contact), so a second free archive is worth having for the ones it missed.
# Common Crawl indexes a different sample of the web and needs no key. Its index
# returns a WARC file plus a byte range rather than a page, so the record is
# fetched with a Range request and gunzipped — three requests in the worst case.
_CC_INDEX = "https://index.commoncrawl.org"
_CC_DATA = "https://data.commoncrawl.org/"
_CC_CRAWLS_TTL = 7 * 86400
_CC_CRAWLS_CACHE = Path(
    os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
) / "commons" / "data" / "ocas-scout" / "commoncrawl-crawls.json"


def _commoncrawl_crawls(timeout=15, limit=3):
    """The newest crawl ids, cached for a week. [] on any failure."""
    try:
        cached = json.loads(_CC_CRAWLS_CACHE.read_text())
        if (time.time() - cached.get("fetched_at", 0)) < _CC_CRAWLS_TTL:
            return list(cached.get("ids") or [])[:limit]
    except Exception:  # noqa: BLE001
        pass
    try:
        req = urllib.request.Request(_CC_INDEX + "/collinfo.json",
                                     headers={"User-Agent": "hermes-scout/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", errors="ignore"))
        ids = [c["id"] for c in data if isinstance(c, dict) and c.get("id")]
    except Exception:  # noqa: BLE001
        return []
    try:
        _CC_CRAWLS_CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = _CC_CRAWLS_CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps({"fetched_at": time.time(), "ids": ids[:12]}))
        tmp.replace(_CC_CRAWLS_CACHE)
    except Exception:  # noqa: BLE001
        pass
    return ids[:limit]


def commoncrawl_snapshot(url, timeout=25, max_crawls=2):
    """{url, timestamp, source, html} for an archived copy, or None.

    Fail-soft at every step: a missing crawl list, a 404 from the index, a
    truncated Range response or an unreadable WARC all yield None.
    """
    u = (url or "").strip()
    if not u:
        return None
    for crawl in _commoncrawl_crawls(timeout=min(timeout, 15)) [:max_crawls]:
        try:
            api = "%s/%s-index?url=%s&output=json&limit=4" % (
                _CC_INDEX, crawl, urllib.parse.quote(u, safe=""))
            req = urllib.request.Request(
                api, headers={"User-Agent": "hermes-scout/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                lines = r.read(200_000).decode("utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        recs = []
        for line in lines.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if str(rec.get("status")) == "200" and rec.get("filename"):
                recs.append(rec)
        if not recs:
            continue
        recs.sort(key=lambda r: str(r.get("timestamp", "")), reverse=True)
        rec = recs[0]
        try:
            offset, length = int(rec["offset"]), int(rec["length"])
            data_req = urllib.request.Request(
                _CC_DATA + rec["filename"],
                headers={"User-Agent": "hermes-scout/1.0",
                         "Range": "bytes=%d-%d" % (offset, offset + length - 1)})
            with urllib.request.urlopen(data_req, timeout=timeout) as r:
                blob = r.read(4_000_000)
            import gzip as _gzip
            import io as _io
            warc = _gzip.GzipFile(fileobj=_io.BytesIO(blob)).read()
        except Exception:  # noqa: BLE001
            continue
        # WARC header, then HTTP header, then the body.
        parts = warc.split(b"\r\n\r\n", 2)
        if len(parts) < 3:
            continue
        html = parts[2].decode("utf-8", errors="ignore")
        if not html.strip():
            continue
        return {"url": rec.get("url") or u,
                "timestamp": str(rec.get("timestamp", "")),
                "source": "commoncrawl", "crawl": crawl, "html": html}
    return None


def archive_today_snapshot(url, timeout=15):
    """Always (None, record) — archive.today cannot be queried from a server.

    Checked rather than assumed: /newest/, /timemap/ and the archive.today,
    archive.ph hostnames all answer HTTP 429 to a plain request from this box,
    with an interstitial instead of content, and the service publishes no JSON
    API to ask differently. Solving that means running a browser and defeating
    bot detection, which is out of scope for a fail-soft OSINT step. Kept as an
    explicit negative so the next pass does not re-derive it.
    """
    return None, {"tool_name": "archive_today", "invoked_at": _now(),
                  "input_type": "url", "input_value": (url or "")[:200],
                  "status": "unavailable", "findings_count": 0,
                  "error": "archive.today answers 429 to server-side requests"}


def archived_page_text(url, timeout=20):
    """(title, body, snapshot) of the archived copy of a dead page.

    Wayback first because it is the larger archive and costs one cheap JSON
    call; Common Crawl second, for the pages Wayback never captured. The
    snapshot dict names which archive answered so the caller can record it.
    """
    snap = wayback_snapshot(url, timeout=max(timeout, 25))
    if snap:
        # Measured: the replay host returns an empty body on the first read for
        # roughly half of these and the real page on the second, so a single
        # attempt reported "not archived" for pages that WERE archived — one of
        # them an archived personal site whose title is the contact's own name.
        title, body = fetch_page_text(snap["url"], timeout=timeout)
        if not (title or body):
            title, body = fetch_page_text(snap["url"], timeout=max(timeout, 45))
        if title or body:
            snap.setdefault("source", "wayback")
            return title, body, snap
    try:
        cc = commoncrawl_snapshot(url, timeout=timeout)
    except Exception:  # noqa: BLE001
        cc = None
    if cc:
        title, body = extract_page_text(cc.pop("html", ""))
        if title or body:
            return title, body, cc
    return "", "", None


# --------------------------------------------------------------------------
# Phone intelligence
# --------------------------------------------------------------------------
# PhoneInfoga is NOT installed and is not installable cleanly here: it is a Go
# binary, this box has no Go toolchain, and its only offline scanner ("local")
# is a wrapper around libphonenumber — the same library `phonenumbers` already
# provides in the agent venv. Its remaining scanners (numverify, googlesearch)
# need third-party API keys. So the local scanner's output is produced directly
# instead of installing anything: region, carrier, line type and timezone.
def phone_intel(phone, region_hint=None):
    """Carrier / line-type / region for a phone number, or {}.

    Fails soft to {} when the library is missing or the number does not parse.
    The geographic description is a CANDIDATE only: US numbers are portable, so
    an area code corroborates a city rather than establishing one.
    """
    raw = (phone or "").strip()
    if not raw:
        return {}
    try:
        import phonenumbers as _pn
        from phonenumbers import carrier as _carrier, geocoder as _geo
        from phonenumbers import timezone as _tz
    except Exception:  # noqa: BLE001
        return {}
    _TYPES = {}
    try:
        from phonenumbers import PhoneNumberType as _T
        _TYPES = {_T.FIXED_LINE: "fixed_line", _T.MOBILE: "mobile",
                  _T.FIXED_LINE_OR_MOBILE: "fixed_line_or_mobile",
                  _T.TOLL_FREE: "toll_free", _T.PREMIUM_RATE: "premium_rate",
                  _T.SHARED_COST: "shared_cost", _T.VOIP: "voip",
                  _T.PERSONAL_NUMBER: "personal_number", _T.PAGER: "pager",
                  _T.UAN: "uan", _T.VOICEMAIL: "voicemail"}
    except Exception:  # noqa: BLE001
        pass
    for region in ([region_hint] if region_hint else []) + [None, "US"]:
        try:
            p = _pn.parse(raw, region)
        except Exception:  # noqa: BLE001
            continue
        if not _pn.is_valid_number(p):
            continue
        try:
            out = {
                "e164": _pn.format_number(p, _pn.PhoneNumberFormat.E164),
                "country_code": p.country_code,
                "region_code": _pn.region_code_for_number(p) or "",
                "geo": _geo.description_for_number(p, "en") or "",
                "carrier": _carrier.name_for_number(p, "en") or "",
                "line_type": _TYPES.get(_pn.number_type(p), "unknown"),
                "timezones": list(_tz.time_zones_for_number(p) or ()),
            }
        except Exception:  # noqa: BLE001
            return {}
        return out
    return {}


def _place_agrees(a, b):
    """Loose agreement between two place strings ('San Francisco, CA')."""
    def toks(s):
        return {t for t in re.split(r"[^a-z0-9]+", fold_accents(s or "").lower())
                if len(t) > 2}
    ta, tb = toks(a), toks(b)
    return bool(ta and tb and (ta & tb))


# Hosts that refuse a server-side fetch outright: LinkedIn answers HTTP 999 to
# any non-browser client, Instagram 302s to a login wall. A curated URL on one of
# these can NEVER be name-confirmed by this pipeline, however many times it runs.
_UNFETCHABLE_HOSTS = (
    "linkedin.com", "instagram.com", "facebook.com", "threads.net",
    "x.com", "twitter.com", "tiktok.com", "quora.com", "glassdoor.com",
)


def _host_is_unfetchable(url):
    h = _host_of(url or "")
    return any(h == d or h.endswith("." + d) for d in _UNFETCHABLE_HOSTS)


# The five fields this pipeline exists to fill. `missing_fields` names the
# subset a given contact still lacks, so the query budget is spent on what is
# actually missing instead of firing one battery at everybody.
TARGET_FIELDS = ("linkedin", "phone", "site", "email", "city")


def build_search_queries(name, name_given="", name_family="", org="",
                         occupation="", location_city="", email="", phone="",
                         missing_fields=None):
    """Queries shaped by WHICH of the five target fields are still missing.

    Passing missing_fields=None keeps the previous behaviour (every query), so
    existing callers and the CLI are unaffected.

    Query shapes were compared head-to-head on 18 real contacts missing a
    LinkedIn URL. Discovery differed a lot -- 'site:linkedin.com "<name>"'
    surfaced a LinkedIn URL for 9 of them against 6 for the others -- but the
    number that ended up with an accepted URL was 2 either way, because the
    extra hits were namesakes. '"<name>" <org> linkedin' produced 8 distinct
    LinkedIn URLs per sample against 20-25 for the site:-scoped shapes, so it
    goes first: fewer competing namesakes means the collision rule in
    resolve_linkedin_candidates refuses far less often.
    """
    name = (name or "").strip()
    if not name:
        return []
    want = set(missing_fields) if missing_fields is not None else set(TARGET_FIELDS)
    org = (org or "").strip()
    occupation = (occupation or "").strip()
    city_head = (location_city or "").split(",")[0].strip()

    # The bare quoted name goes FIRST, always. Qualifying a distinctive full
    # name with an employer measurably degraded results on the available
    # engines: the qualified query returned only unrelated popular pages while
    # the bare name returned the person's actual profiles. Qualified variants
    # still run afterwards to help common names.
    queries = []
    # The phone number goes ahead of even the bare name: two people do not share
    # a line, so an exact-phrase hit is near-proof of identity where a name match
    # is only a hint. This was never searched at all.
    for _f in phone_search_forms(phone)[:2]:
        queries.append('"%s"' % _f)
    queries.append(f'"{name}"')
    # The employer named by a work email domain. Where this disagrees with the
    # stored org it is likelier to be right -- the domain is on the contact's own
    # record, the org may be a value an earlier enrichment guessed.
    _dom_org = employer_from_email(email, name)
    if _dom_org and re.sub(r"[^a-z0-9]", "", _dom_org) not in re.sub(
            r"[^a-z0-9]", "", org.lower()):
        queries.append(f'site:linkedin.com/in "{name}" {_dom_org}')
        queries.append(f'"{name}" {_dom_org}')
    if org:
        if "linkedin" in want:
            queries.append(f'"{name}" {org} linkedin')
            queries.append(f'site:linkedin.com/in "{name}" {org}')
        queries.append(f'"{name}" {org}')
    if occupation:
        queries.append(f'"{name}" {occupation}' + (f" {org}" if org else ""))
    if "linkedin" in want and not org:
        queries.append(f'site:linkedin.com/in "{name}"'
                       + (f" {city_head}" if city_head else ""))
    # Field-shaped queries. Each one asks for the page type that actually
    # carries the missing value rather than for the person in general: a
    # contact/about page for a phone or an address, a portfolio or personal
    # site for a website. They run only for the fields a contact is missing, so
    # a contact who only lacks a LinkedIn URL never pays for them.
    if "phone" in want or "email" in want:
        queries.append(f'"{name}" {org} contact'.replace("  ", " ").strip()
                       if org else f'"{name}" contact email')
    if "site" in want:
        _q = f'"{name}" {occupation} portfolio' if occupation else f'"{name}" personal website'
        queries.append(_q)
    if "city" in want and org:
        queries.append(f'"{name}" {org} "based in"')
    # Always try the city. It was previously reachable only when the contact had
    # neither an org nor an occupation, yet 82% of the contacts this pipeline
    # fails on have one, and a city is what separates two people of one name.
    if city_head:
        queries.append(f'"{name}" {city_head}')
    out = []
    for q in queries:
        q = re.sub(r"\s+", " ", q).strip()
        if q and q not in out:
            out.append(q)
    return out


def _name_agreement(contact_name, profile_fullname):
    """(shared_token_count, family_present) between contact and a profile name."""
    if not profile_fullname:
        return 0, False
    # keep_initials so a contact whose given name is initials can match a profile
    # that displays exactly their name; the family-name requirement at the
    # corroboration site is what keeps that safe.
    ratio, shared = token_overlap_ratio(contact_name, profile_fullname,
                                        keep_initials=True)
    fam = (normalize_name(contact_name).split() or [""])[-1]
    fam_present = bool(fam) and fam in normalize_name(profile_fullname).split()
    return shared, fam_present


def _handle_is_bare_name_part(handle, name, name_given="", name_family=""):
    """True when the handle is nothing more than one part of the contact's name.

    A bare first or last name — or an initial plus one of them — is shared by
    every namesake on every site, so it is not a searchable anchor: a sweep on it
    returns strangers, and a profile agreeing on that one name part tells us
    nothing about which of them we found. Handles carrying anything further are
    left alone, because they are specific enough that name agreement is real
    evidence, which is the discriminator this pipeline relies on
    (a handle combining both name parts, or one sharing no name token at all).
    """
    h = re.sub(r"[^a-z0-9]", "", fold_accents(handle or "").lower())
    if not h:
        return False
    given, family = _split_name(name, name_given, name_family)
    f = re.sub(r"[^a-z0-9]", "", fold_accents(family or "").lower())
    g = re.sub(r"[^a-z0-9]", "", fold_accents(given or "").lower())

    # Exactly one name part and nothing else.
    if (g and h == g) or (f and h == f):
        return True

    # The given name spelled out makes the handle the whole name, however short
    # that name is — a two-letter given name plus a surname is both parts, not an
    # initial plus a surname.
    if len(g) >= 2 and g in h and h != g:
        return False

    for part in (f, g):
        if len(part) < 3 or part not in h:
            continue
        idx = h.find(part)
        prefix, suffix = h[:idx], h[idx + len(part):]
        # Trailing characters are entropy the owner chose — few namesakes pick
        # exactly <surname>+digits — so the handle is more than a name part.
        if suffix:
            continue
        # A single leading letter is an initial: it abbreviates the other name
        # into one of 26 values and identifies nobody (<initial><surname>).
        # One or two leading letters are initials: they abbreviate the other
        # name into a handful of values and identify nobody. Two letters matter as
        # much as one — the "<first two letters><surname>" address shape is common
        # and was measured colliding with a stranger sharing the surname.
        if 1 <= len(prefix) <= 2 and prefix.isalpha():
            return True
        # Anything longer in front is another name or word, which makes the
        # handle specific: <given><surname> carries the whole name.
    return False

def _name_phrase_in_text(name, text, name_given="", name_family="", max_gap=2):
    """True when the text names the contact, rather than merely containing both
    of their name tokens somewhere.

    Token overlap over a whole page cannot tell "<Given> <Family> is a ..." apart
    from a list of unrelated people that happens to include a <Given> and a
    <Family>. Requiring adjacency is the difference. A middle name or initial may
    sit between the two, and the "<Family>, <Given>" ordering is accepted.

    Delegates to _name_phrase_spans so the predicate and the position of the
    match can never disagree: role_near_name reads a job title out of the text
    immediately after a match, and it has to be the SAME match this returns.
    """
    return bool(_name_phrase_spans(name, text, name_given, name_family, max_gap))


# ── LinkedIn URL verification ────────────────────────────────────────────────
# A linkedin.com/in/<slug> URL is NOT evidence on its own, and this pipeline has
# already been burned by treating a name-shaped identifier as identity: a
# stranger's profiles were attributed to a real contact because a handle
# resembled their name. Three specific facts drive the rules below.
#
#   * Many slugs are opaque — a numeric id, or a name plus a random suffix —
#     and identify nobody by inspection.
#   * A slug like "<given><family>" for a common name is shared by thousands of
#     people. Matching it is the namesake failure, not corroboration.
#   * LinkedIn answers HTTP 999 to any server-side fetch (it is in
#     _UNFETCHABLE_HOSTS for exactly that reason), so the page can never be read
#     to check whose profile it is. There is no "just fetch it and confirm".
#
# Therefore a discovered LinkedIn URL is accepted ONLY when something
# INDEPENDENT of the slug ties it to this contact. See linkedin_tie().
_LINKEDIN_IN_RE = re.compile(r"linkedin\.com/in/([^/?#\s\"']+)", re.IGNORECASE)

# Public name-frequency data (census-style "most common names" lists). NOTHING
# here is drawn from any contact record — it exists so that a slug built from a
# common name is refused as an identifier. A name absent from these lists is
# treated as rare enough that a slug carrying BOTH of its parts is unlikely to
# belong to someone else.
_COMMON_SURNAMES = frozenset("""
smith johnson williams brown jones garcia miller davis rodriguez martinez
hernandez lopez gonzalez wilson anderson thomas taylor moore jackson martin
lee perez thompson white harris sanchez clark ramirez lewis robinson walker
young allen king wright scott torres nguyen hill flores green adams nelson
baker hall rivera campbell mitchell carter roberts gomez phillips evans turner
diaz parker cruz edwards collins reyes stewart morris morales murphy cook
rogers gutierrez ortiz morgan cooper peterson bailey reed kelly howard ramos
kim cox ward richardson watson brooks chavez wood james bennett gray mendoza
ruiz hughes price alvarez castillo sanders patel myers long ross foster
jimenez powell jenkins perry russell sullivan bell coleman butler henderson
barnes gonzales fisher vasquez simmons romero jordan patterson alexander
hamilton graham reynolds griffin wallace moreno west cole hayes bryant herrera
gibson ellis tran medina aguilar stevens murray ford castro marshall owens
harrison fernandez mcdonald woods washington kennedy wells vargas henry chen
freeman webb tucker guzman burns crawford olson simpson porter hunter gordon
mendez silva shaw snyder mason dixon munoz hunt hicks holmes palmer wagner
black robertson boyd rose stone salazar fox warren mills meyer rice schmidt
garza daniels ferguson nichols stephens soto weaver ryan gardner payne grant
dunn kelley spencer hawkins arnold pierce vazquez hansen peters santos hart
bradley knight elliott cunningham duncan armstrong hudson carroll lane riley
andrews ruiz harper fowler burke larson santiago maldonado morrison franklin
carlson austin dominguez carr lawrence walsh jensen barrett mullins fields
moran brennan wang li zhang liu yang huang zhao wu zhou xu sun ma zhu hu guo
lin he gao luo zheng liang song tang xie han cao deng singh kumar sharma verma
gupta reddy khan ali ahmed hussain rahman islam begum akhtar iqbal malik
sheikh syed shah ansari qureshi silva santos oliveira souza lima pereira
ferreira alves rodrigues costa gomes ribeiro carvalho almeida araujo mueller
muller schmidt schneider fischer weber meyer wagner becker schulz hoffmann
schaefer koch bauer richter klein wolf schroeder neumann zimmermann braun
krueger hofmann hartmann lange schmitt werner krause meier lehmann rossi
russo ferrari esposito bianchi romano colombo ricci marino greco bruno gallo
conti costa giordano mancini rizzo lombardi moretti barbieri fontana caruso
dubois bernard petit durand leroy moreau simon laurent lefebvre michel garcia
david bertrand roux vincent fournier morel girard andre mercier blanc guerin
boyer garnier chevalier francois legrand gauthier ivanov smirnov kuznetsov
popov sokolov lebedev kozlov novikov morozov petrov volkov solovyov vasilyev
zaytsev pavlov semyonov golubev vinogradov bogdanov park choi jung kang cho
yoon jang lim shin seo kwon hwang song ahn hong yamamoto tanaka suzuki sato
watanabe takahashi nakamura ito kobayashi yoshida yamada sasaki yamaguchi
matsumoto inoue kimura hayashi shimizu saito jong jansen vries bakker visser
smit meijer boer mulder bos vos peters hendriks dekker nielsen hansen andersen
pedersen christensen larsen sorensen rasmussen jorgensen petersen madsen
kristensen olsen thomsen johansson andersson karlsson nilsson eriksson larsson
olsson persson svensson gustafsson pettersson jonsson novak nowak kowalski
wojcik kaminski lewandowski zielinski szymanski wozniak dabrowski kozlowski
jankowski mazur horvath nagy kovacs toth szabo varga kiss molnar nemeth farkas
obrien byrne oconnor mccarthy oneill doyle gallagher doherty kavanagh mahoney
""".split())

_COMMON_GIVEN_NAMES = frozenset("""
james robert john michael david william richard joseph thomas charles
christopher daniel matthew anthony mark donald steven paul andrew joshua
kenneth kevin brian george timothy ronald jason edward jeffrey ryan jacob gary
nicholas eric jonathan stephen larry justin scott brandon benjamin samuel
gregory alexander patrick frank raymond jack dennis jerry tyler aaron jose
adam nathan henry zachary douglas peter kyle noah ethan jeremy walter
christian keith roger terry austin sean gerald carl harold dylan arthur
lawrence jordan jesse bryan billy bruce gabriel joe logan alan juan albert
willie elijah wayne randy vincent mason roy ralph bobby russell bradley philip
eugene mary patricia jennifer linda elizabeth barbara susan jessica sarah
karen lisa nancy betty margaret sandra ashley kimberly emily donna michelle
carol amanda dorothy melissa deborah stephanie rebecca sharon laura cynthia
kathleen amy angela shirley anna brenda pamela emma nicole helen samantha
katherine christine debra rachel carolyn janet catherine maria heather diane
ruth julie olivia joyce virginia victoria kelly lauren christina joan evelyn
judith megan andrea cheryl hannah jacqueline martha gloria teresa ann sara
madison frances kathryn janice jean abigail alice julia judy sophia grace
denise amber doris marilyn danielle beverly isabella theresa diana natalie
brittany charlotte marie kayla alexis lori tim tom dan dave mike chris steve
jeff greg jim bob rob rick nick matt joe sam ben alex ellen susan tina wendy
carlos luis pedro miguel antonio francisco manuel jorge rafael ricardo eduardo
fernando roberto sergio javier alberto ana isabel carmen rosa laura marta
lucia elena sofia paula claudia patricia mohamed mohammed muhammad ahmad ahmed
ali hassan hussein omar khalid youssef ibrahim mustafa fatima aisha maryam
zainab amina khadija noor layla raj rahul amit sunil anil vijay ajay sanjay
ravi arun deepak manoj suresh priya anita sunita neha pooja kavita meera divya
wei ming lei jun hui yan jing xin feng bin tao gang jian yong hao chao lan
mei ling ping xia hong yun juan yuki hiroshi takashi kenji akira satoshi
haruto yuto sota ren yui aoi hana sakura min soo hyun jae seung woo young jin
hee eun ji sun ivan sergey dmitry alexey andrey nikolai vladimir mikhail pavel
olga natalia elena irina tatiana svetlana anastasia ekaterina
""".split())


def linkedin_slug(url):
    """The <slug> of a linkedin.com/in/<slug> URL, lowercased, or ''.

    Fail-soft in its own right, not just at its call sites: it is called from
    inside the search-result loop and the gravatar loop, where an exception
    would abort the whole contact over one malformed URL.
    """
    try:
        m = _LINKEDIN_IN_RE.search(url or "")
    except Exception:  # noqa: BLE001
        return ""
    if not m:
        return ""
    try:
        slug = urllib.parse.unquote(m.group(1)).strip().strip("/").lower()
    except Exception:  # noqa: BLE001
        return ""
    # LinkedIn appends a disambiguating hash to non-unique vanity URLs
    # ("avery-placeholder-1a2b3c4"). The hash is entropy the OWNER did not
    # choose and carries no name signal, so it is stripped before the name
    # tests below rather than being mistaken for distinctiveness.
    slug = re.sub(r"-[0-9a-f]{6,9}$", "", slug)
    return slug


def _slug_tokens(slug):
    """The alphabetic runs of a slug, folded — 'avery-p-placeholder' -> [...]"""
    folded = fold_accents(slug or "").lower()
    return [t for t in re.split(r"[^a-z]+", folded) if t]


def slug_is_distinctive(slug, name, name_given="", name_family=""):
    """(ok, reason) — may this slug ALONE identify the contact?

    Only true for a slug that encodes a full name rare enough that a namesake
    collision is implausible. Everything else is refused, because a slug is an
    identifier the owner chose, not a statement about who they are:

      * a numeric or opaque slug names nobody;
      * '<given><family>' for a common name matches thousands of people — this
        is precisely the failure mode that attributed a stranger's accounts to
        a contact, so a common surname or a common given+family pair is refused
        even though the slug 'matches' perfectly;
      * a slug carrying only ONE name part is a bare name part, which
        _handle_is_bare_name_part already rejects everywhere else.

    A middle name or second family name in the slug counts as extra
    distinctiveness: it narrows the population far below the given+family pair.
    """
    slug = (slug or "").strip().lower()
    if not slug:
        return False, "no slug"
    given, family = _split_name(name, name_given, name_family)
    g = re.sub(r"[^a-z]", "", fold_accents(given or "").lower())
    f = re.sub(r"[^a-z]", "", fold_accents(family or "").lower())
    if not g or not f:
        return False, "contact has no full name to compare against"

    flat = re.sub(r"[^a-z0-9]", "", fold_accents(slug))
    if not re.search(r"[a-z]", flat):
        # "linkedin.com/in/884213705" — an opaque member id.
        return False, "slug is numeric/opaque and identifies nobody"
    if g not in flat or f not in flat:
        return False, "slug does not carry both name parts"

    g_common = g in _COMMON_GIVEN_NAMES
    f_common = f in _COMMON_SURNAMES
    # Anything in the slug beyond the two name parts: a middle name, a second
    # surname, a maternal name. Digits do NOT count — "-2" is a disambiguator
    # LinkedIn assigns, not something distinctive about the person.
    def _token_is_only_name_parts(tok):
        """Is this token just the name run together, with nothing added?

        Token equality alone gets the separator wrong: 'john-smith' splits into
        ['john','smith'] and correctly yields no extra, but 'johnsmith' is ONE
        token equal to neither part, so it counted as a distinguishing extra and
        the most common name in English was accepted on the slug alone -- while
        the hyphenated spelling of the same name was refused. Strip the name
        parts out and see whether anything of substance is left.
        """
        rest = tok
        for part in (g, f):
            if part:
                rest = rest.replace(part, "", 1)
        return len(rest) <= 1

    extra = [t for t in _slug_tokens(slug)
             if not _token_is_only_name_parts(t) and len(t) > 1
             and t not in ("dr", "mr", "ms", "mrs", "phd", "md")]
    if extra:
        return True, ("slug carries the full name plus %s, which is far more "
                      "specific than a given+family pair" % ", ".join(extra[:2]))
    if f_common:
        return False, ("surname is among the most common, so '<given><family>' "
                       "is shared by many people")
    if g_common and f_common:
        return False, "both name parts are common"
    if g_common:
        # A common given name with a rare surname is still rare as a pair, but
        # the margin is thin, so it is only accepted with nothing competing —
        # which resolve_linkedin_candidates() enforces separately.
        return True, "common given name but a rare surname"
    return True, "both name parts are uncommon"


def linkedin_tie(url, name, name_given="", name_family="", org="",
                 location_city="", context_text="", source=""):
    """(tie_kind, reason) if this URL is tied to the contact, else (None, why).

    The tie must come from something OTHER than the slug's resemblance to the
    name, except in the one narrow case slug_is_distinctive() allows. Ordered
    strongest first:

      first_party  the URL was found on a page already confirmed to be the
                   contact's — their own site, their GitHub profile's links,
                   a gravatar keyed on their address. The contact published it,
                   so it is their assertion, the same grade as a curated URL.
      context      the URL came back in a search result whose OWN text names
                   the contact (adjacency, via _name_phrase_in_text) AND names
                   their employer or city. Measured against a control of
                   fabricated names + real employers, which returned zero
                   results, so this text is the indexed page's, not an echo of
                   the query.
      slug         no independent tie, but the slug encodes a full name rare
                   enough that a collision is implausible (see
                   slug_is_distinctive).
    """
    slug = linkedin_slug(url)
    if not slug:
        return None, "not a linkedin.com/in URL"
    if source == "first_party":
        return "first_party", ("published on a page already confirmed to be "
                               "the contact's")

    ctx = context_text or ""
    if ctx:
        named = _name_phrase_in_text(name, ctx, name_given, name_family)
        org_ok = bool(org) and org_name_in_text(org, ctx)
        city_head = (location_city or "").split(",")[0].strip()
        city_ok = bool(city_head) and city_head.lower() in ctx.lower()
        if named and (org_ok or city_ok):
            return "context", ("result text names the contact and their %s"
                               % ("employer" if org_ok else "city"))

    ok, why = slug_is_distinctive(slug, name, name_given, name_family)
    if ok:
        return "slug", "no independent tie; " + why
    return None, why


_LINKEDIN_TIE_RANK = {"first_party": 0, "context": 1, "slug": 2}

# Whether a distinctive-slug tie may source a value on its own. It is the
# weakest of the three and the only one that is not INDEPENDENT of the slug: it
# argues that a namesake is improbable rather than pointing at a second source.
# It is enabled because three separate things have to hold before it fires --
# the slug must carry BOTH name parts, neither part may appear on public name-
# frequency data (or the slug must carry a middle name too), and nothing else
# may compete for this contact (resolve_linkedin_candidates refuses on any
# disagreement) -- and because weave then puts the URL through url_quality,
# which additionally rejects a slug naming a DIFFERENT person in the address
# book. Set to False to require a genuinely independent tie for every LinkedIn
# URL; the other two tie kinds are unaffected.
LINKEDIN_ACCEPT_SLUG_ONLY = True


def resolve_linkedin_candidates(candidates, name, name_given="", name_family="",
                                org="", location_city=""):
    """(accepted|None, [rejected]) from LinkedIn URLs seen for one contact.

    candidates: [{"url":..., "context":..., "source":...}]

    Two people of one name are the failure this whole module exists to prevent,
    and the cheapest detector for them is disagreement: if two DIFFERENT slugs
    both look tied to this contact, at least one of them is a stranger and we
    cannot tell which, so BOTH are refused. A single surviving candidate is
    accepted at the strength of its tie.
    """
    by_slug = {}
    rejected = []
    for c in candidates or []:
        url = (c.get("url") or "").strip()
        slug = linkedin_slug(url)
        if not slug:
            continue
        kind, why = linkedin_tie(
            url, name, name_given=name_given, name_family=name_family,
            org=org, location_city=location_city,
            context_text=c.get("context", ""), source=c.get("source", ""))
        if not kind:
            rejected.append({"url": url, "slug": slug, "reason": why})
            continue
        prev = by_slug.get(slug)
        if not prev or _LINKEDIN_TIE_RANK[kind] < _LINKEDIN_TIE_RANK[prev["tie"]]:
            by_slug[slug] = {"url": url, "slug": slug, "tie": kind,
                             "reason": why, "source": c.get("source", "")}

    if not by_slug:
        return None, rejected
    if len(by_slug) > 1:
        # A first-party link is the contact's own assertion and outranks any
        # number of search-derived namesakes, so it still wins outright.
        fp = [v for v in by_slug.values() if v["tie"] == "first_party"]
        if len(fp) == 1:
            for v in by_slug.values():
                if v is not fp[0]:
                    rejected.append({"url": v["url"], "slug": v["slug"],
                                     "reason": ("another URL for this contact is "
                                                "first-party, which outranks this")})
            return fp[0], rejected
        for v in by_slug.values():
            rejected.append({
                "url": v["url"], "slug": v["slug"],
                "reason": ("%d different LinkedIn profiles look tied to this "
                           "contact (%s) — at least one is a namesake and there "
                           "is no way to tell which, so none is accepted"
                           % (len(by_slug), ", ".join(sorted(by_slug)[:4])))})
        return None, rejected

    only = list(by_slug.values())[0]
    return only, rejected


# ── Mining the five target fields out of a page we already fetched ───────────
# Every page this pipeline opens costs a request and a timeout; reading only
# "does this name the contact?" out of it and discarding the rest is wasted
# work. These helpers pull phone / email / city / outbound-profile links from
# HTML that has ALREADY been fetched for corroboration.
#
# Measured before building it, on 40 contacts whose record carries a personal
# site: a naive phone regex "found" a number on 22 of 25 pages and nearly all
# of them were junk (an obituary listing, a comic strip, dates and ISBNs).
# Validating with libphonenumber AND requiring the number to sit in a telephone
# context cut that to 2. The strict version is the one worth having: the loose
# one would have written a wrong phone number onto 20 contacts.
# Imported at module level but never assumed present: the venv ships it today,
# and a future one that does not must degrade to "no phone mined", not crash a
# whole contact.
try:
    import phonenumbers as _phonenumbers
except Exception:  # noqa: BLE001
    _phonenumbers = None

_TEL_HREF_RE = re.compile(r"href\s*=\s*[\"']\s*tel:([^\"'>]{5,32})", re.IGNORECASE)
_MAILTO_RE = re.compile(r"href\s*=\s*[\"']\s*mailto:([^\"'?>]{3,120})", re.IGNORECASE)
_PHONE_CONTEXT_RE = re.compile(
    r"(?i)\b(phone|telephone|tel|mobile|cell|call|contact|reach me|whatsapp)\b")
# Numbers that are valid but belong to an organisation's switchboard rather than
# to a person. Attributing one to a contact is a wrong value, not a missing one.
_TOLLFREE_PREFIXES = ("800", "833", "844", "855", "866", "877", "888")
_JSONLD_RE = re.compile(r"(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>")
_GEO_PLACENAME_RE = re.compile(
    r"(?is)<meta[^>]+name=[\"']geo\.placename[\"'][^>]+content=[\"']([^\"']{2,80})")
# One inline-flag group, at the very start: Python refuses a global flag that
# appears part-way through a pattern, and both branches need the same flags.
_REL_ME_RE = re.compile(
    r"(?is)"
    r"<a[^>]+rel=[\"'][^\"']*\bme\b[^\"']*[\"'][^>]*href=[\"']([^\"']+)[\"']"
    r"|<a[^>]+href=[\"']([^\"']+)[\"'][^>]*rel=[\"'][^\"']*\bme\b[^\"']*[\"']")
# "Springfield, OR" / "Springfield, Oregon" / "Springfield, United Kingdom".
_CITY_STATE_RE = re.compile(
    r"\b([A-Z][A-Za-z.\-']{2,24}(?:\s+[A-Z][A-Za-z.\-']{1,24}){0,2}),\s*"
    r"([A-Z]{2}|[A-Z][a-z]{2,24}(?:\s+[A-Z][a-z]{2,24}){0,2})\b")
_ADDRESS_CONTEXT_RE = re.compile(
    r"(?i)\b(based in|located in|lives in|living in|address|office|studio|"
    r"headquarter|hq|from)\b")
_ASSET_EMAIL_RE = re.compile(r"\.(png|jpe?g|gif|svg|webp|css|js|ico|woff2?)$", re.I)
# Mail hosts that belong to infrastructure, not to a person.
_NON_CONTACT_MAIL_HOSTS = {
    "example.com", "example.org", "example.net", "example.test", "domain.com",
    "email.com", "sentry.io", "sentry-next.wixpress.com", "wixpress.com",
    "wix.com", "squarespace.com", "godaddy.com", "shopify.com", "localhost",
}


def _valid_phone(raw, region_hint="US"):
    """E.164 for a raw string that libphonenumber accepts as a REAL number.

    is_valid_number, not is_possible_number: 'possible' passes any string of the
    right length, which is what let dates and order numbers through.
    """
    if _phonenumbers is None:
        return ""
    try:
        num = _phonenumbers.parse(raw, region_hint or "US")
        if not _phonenumbers.is_valid_number(num):
            return ""
        e164 = _phonenumbers.format_number(
            num, _phonenumbers.PhoneNumberFormat.E164)
    except Exception:  # noqa: BLE001
        return ""
    if e164.startswith("+1") and e164[2:5] in _TOLLFREE_PREFIXES:
        return ""
    return e164


def mine_phones(raw_html, text, region_hint="US"):
    """[{phone, how}] — validated numbers, strongest evidence first.

    tel: links and schema.org 'telephone' are explicit assertions that the
    string IS a telephone number; a bare match in prose is not, so it must at
    least sit next to a telephone word.
    """
    out, seen = [], set()
    if _phonenumbers is None:
        return out

    def _take(raw, how):
        e164 = _valid_phone(raw, region_hint)
        if e164 and e164 not in seen:
            seen.add(e164)
            out.append({"phone": e164, "how": how})

    try:
        for m in _TEL_HREF_RE.finditer(raw_html or ""):
            _take(m.group(1), "tel_link")
        for m in _JSONLD_RE.finditer(raw_html or ""):
            for pm in re.finditer(r'"telephone"\s*:\s*"([^"]{5,32})"', m.group(1)):
                _take(pm.group(1), "schema_org")
        for m in _PHONE_CONTEXT_RE.finditer(text or ""):
            window = (text or "")[m.start():m.start() + 100]
            for match in _phonenumbers.PhoneNumberMatcher(
                    window, region_hint or "US"):
                _take(_phonenumbers.format_number(
                    match.number,
                    _phonenumbers.PhoneNumberFormat.E164), "labelled")
    except Exception:  # noqa: BLE001
        pass
    return out


def mine_emails(raw_html, name=""):
    """[{email, how}] — addresses published on the page, role addresses dropped.

    A mailto: link is the page saying "write here"; a bare address in the body
    is weaker but still first-party on the contact's own site.
    """
    out, seen = [], set()
    name_toks = {t for t in normalize_name(name or "").split() if len(t) > 2}

    def _take(addr, how):
        addr = (addr or "").strip().strip(".,;:<>()[]").lower()
        if not addr or "@" not in addr or not _EMAIL_RE.match(addr):
            return
        if addr in _PLACEHOLDER_EMAILS or _ASSET_EMAIL_RE.search(addr):
            return
        local, _, host = addr.partition("@")
        if host in _NON_CONTACT_MAIL_HOSTS or host.endswith(".wixpress.com"):
            return
        if local in GENERIC_EMAIL_LOCALS and not (name_toks & set(
                re.split(r"[^a-z]+", local))):
            return
        if addr in seen:
            return
        seen.add(addr)
        out.append({"email": addr, "how": how})

    try:
        for m in _MAILTO_RE.finditer(raw_html or ""):
            _take(urllib.parse.unquote(m.group(1)), "mailto")
        for addr in set(re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw_html or "")):
            _take(addr, "body")
    except Exception:  # noqa: BLE001
        pass
    return out


def mine_city(raw_html, text):
    """[{city, how}] — structured location first, prose only in context.

    schema.org addressLocality and the geo.placename meta tag are the page
    declaring a place. A "Word, XX" pattern in prose is a guess, so it is only
    taken when an address word sits next to it, and it is always a CANDIDATE.
    """
    out, seen = [], set()

    def _take(val, how):
        val = re.sub(r"\s+", " ", (val or "")).strip().strip(",;")
        if not val or len(val) > 60 or len(val) < 2:
            return
        if val.lower() in seen:
            return
        seen.add(val.lower())
        out.append({"city": val, "how": how})

    try:
        for m in _JSONLD_RE.finditer(raw_html or ""):
            blob = m.group(1)
            loc = re.search(r'"addressLocality"\s*:\s*"([^"]{2,60})"', blob)
            reg = re.search(r'"addressRegion"\s*:\s*"([^"]{2,40})"', blob)
            if loc:
                _take(loc.group(1) + (", " + reg.group(1) if reg else ""),
                      "schema_org")
        for m in _GEO_PLACENAME_RE.finditer(raw_html or ""):
            _take(m.group(1), "geo_meta")
        for m in _ADDRESS_CONTEXT_RE.finditer(text or ""):
            window = (text or "")[m.start():m.start() + 90]
            cm = _CITY_STATE_RE.search(window)
            if cm:
                _take(cm.group(1) + ", " + cm.group(2), "labelled_prose")
    except Exception:  # noqa: BLE001
        pass
    return out


def mine_outbound_links(raw_html, page_url="", name=""):
    """{"linkedin": [...], "websites": [...], "profiles": [parse_profile_url...]}

    Everything here comes off a page the caller has already confirmed belongs to
    the contact, so these are links the contact PUBLISHED about themselves —
    the first-party tie in linkedin_tie(). A website is only reported when the
    page marks it rel="me" (an explicit identity assertion) or its domain
    carries the contact's name, because a personal site links to plenty of
    pages that are not the author's.
    """
    out = {"linkedin": [], "websites": [], "profiles": []}
    seen_li, seen_w, seen_p = set(), set(), set()
    host_here = _host_of(page_url)
    name_flat = re.sub(r"[^a-z]", "", fold_accents(name or "").lower())
    try:
        rel_me = set()
        for m in _REL_ME_RE.finditer(raw_html or ""):
            u = (m.group(1) or m.group(2) or "").strip()
            if u.startswith("http"):
                rel_me.add(u.split("#")[0])
        for m in _HREF_RE.finditer(raw_html or ""):
            u = m.group(1).split("#")[0].strip()
            if not u.startswith("http"):
                continue
            slug = linkedin_slug(u)
            if slug:
                if slug not in seen_li:
                    seen_li.add(slug)
                    out["linkedin"].append(u.split("?")[0])
                continue
            h = _host_of(u)
            if not h or h == host_here:
                continue
            parsed = parse_profile_url(u)
            if parsed and parsed.get("handle"):
                key = (parsed["platform"], (parsed["handle"] or "").lower())
                if key not in seen_p:
                    seen_p.add(key)
                    out["profiles"].append(parsed)
                continue
            if _host_class(h) != _HOST_RANK_PERSONAL:
                continue
            label = re.sub(r"[^a-z]", "", _registrable_label(h) or "")
            owns = bool(name_flat) and bool(label) and (
                label in name_flat or name_flat in label)
            if u.split("?")[0] in rel_me or owns:
                if h not in seen_w:
                    seen_w.add(h)
                    out["websites"].append(u.split("?")[0])
    except Exception:  # noqa: BLE001
        pass
    return out


# How a mined value was found, best evidence first. This ranking is what decides
# which of several candidate values (if any) is written to a contact record.
MINED_HOW_RANK = {"tel_link": 0, "mailto": 0, "schema_org": 1, "geo_meta": 1,
                  "labelled": 2, "labelled_prose": 2, "body": 3, "near_name": 4}


def pick_mined_value(hits, key):
    """The single best-sourced value, or None when the best rank is TIED
    between two different values.

    Refusing on a tie is the point, not a limitation. Measured on real pages: a
    B2B supplier directory returned seven different tel: links, all rank 0, all
    belonging to companies rather than to the contact; a tribal directory
    returned three addresses next to three different names. Picking "the first
    one" on either page writes a stranger's number onto a contact. Where the
    page really is the contact's and really does carry one number, there is no
    tie and the value is taken.
    """
    best = {}
    for h in hits or []:
        v = (h.get(key) or "").strip()
        if not v:
            continue
        r = MINED_HOW_RANK.get(h.get("how"), 9)
        if v not in best or r < best[v][0]:
            best[v] = (r, h)
    if not best:
        return None
    top = min(r for r, _ in best.values())
    winners = [(v, h) for v, (r, h) in best.items() if r == top]
    if len(winners) != 1:
        return None
    v, h = winners[0]
    return {"value": v, "how": h.get("how"), "source_url": h.get("source_url", ""),
            "rank": top, "competing": len(best)}


def mine_contact_fields(raw_html, text="", name="", name_given="",
                        name_family="", region_hint="US", page_url=""):
    """All five target fields out of one already-fetched page.

    Returns {"phones", "emails", "cities", "linkedin", "websites", "profiles"}.
    Never raises: a page that defeats one extractor must still yield the others.
    """
    if not text:
        text = ""
    res = {"phones": [], "emails": [], "cities": [], "linkedin": [],
           "websites": [], "profiles": []}
    if not raw_html:
        return res
    try:
        res["phones"] = mine_phones(raw_html, text, region_hint)
    except Exception:  # noqa: BLE001
        pass
    try:
        res["emails"] = mine_emails(raw_html, name)
    except Exception:  # noqa: BLE001
        pass
    try:
        res["cities"] = mine_city(raw_html, text)
    except Exception:  # noqa: BLE001
        pass
    try:
        links = mine_outbound_links(raw_html, page_url, name)
        res["linkedin"] = links["linkedin"]
        res["websites"] = links["websites"]
        res["profiles"] = links["profiles"]
    except Exception:  # noqa: BLE001
        pass
    return res


# ── Reaching a GitHub account WITHOUT an email to pivot from ─────────────────
# github_commit_emails() is the most direct route to an address for a contact
# who has none, but it could never fire: it only reads accounts that already
# passed the identity gate, and a contact with no email has no email-derived
# handle, so the only handles available are manufactured from their name — which
# the gate correctly refuses as circular. The account was unreachable precisely
# for the population the technique was built for.
#
# GitHub's user search closes that loop with an INDEPENDENT signal. It matches
# on the profile's own `name` field, which the account owner typed, not on a
# handle we derived from the contact. A hit is then confirmed against two things
# the contact record already asserts — their name AND (employer or city) — so a
# namesake with a different company or city is refused rather than harvested.
def github_profile_is_harvestable(prof):
    """May this GitHub profile's commit history be read for an address?

    The SAME predicate decides two things that were previously written out
    separately and disagreed: whether we already have a usable account (so the
    user search can be skipped) and whether the harvest loop will actually read
    one. When those two drifted apart, a REJECTED GitHub profile -- one whose
    handle was manufactured from the contact's name, so its name agreement is
    circular -- was enough to suppress the search, while the harvest then
    skipped that same profile for being circular. Nothing ran, which is exactly
    the "unreachable by construction" trap this technique started in.
    """
    if not isinstance(prof, dict):
        return False
    if (prof.get("site") or "").lower() != "github":
        return False
    if prof.get("name_conflict") or prof.get("circular_anchor"):
        return False
    if not (prof.get("curated")
            or (prof.get("name_shared_tokens", 0) >= 2
                and prof.get("family_present"))):
        return False
    return bool((prof.get("handle") or "").strip())


def github_user_search(name, org="", location_city="", timeout=10, max_users=5):
    """([{handle, fullname, company, location, why}], PersonToolRecord).

    Only accounts whose PROFILE NAME confirms the contact and whose company or
    location agrees are returned. Fail-soft: rate limits, an outage or a
    malformed name cost one tool entry and nothing else.
    """
    rec = {"tool_name": "github_user_search", "invoked_at": _now(),
           "input_type": "name", "input_value": (name or "")[:120],
           "status": "error", "findings_count": 0, "error": None,
           "authenticated": bool(_github_token())}
    name = (name or "").strip()
    if len(name.split()) < 2:
        rec["status"] = "skipped"
        rec["error"] = "need a full name; one token matches too many accounts"
        return [], rec
    if not (org or "").strip() and not (location_city or "").strip():
        # Without a second axis this is a bare-name sweep, which is the exact
        # shape that produced false attributions before. Refuse it.
        rec["status"] = "skipped"
        rec["error"] = ("no employer or city to corroborate against; a name-only "
                        "match cannot be told apart from a namesake")
        return [], rec

    q = urllib.parse.quote('"%s" in:name type:user' % name)
    data = _github_json("/search/users?q=%s&per_page=%d" % (q, max_users), timeout)
    if not isinstance(data, dict):
        rec["error"] = "search API unavailable (rate limit or outage)"
        return [], rec
    rec["status"] = "success"

    city_head = (location_city or "").split(",")[0].strip().lower()
    out = []
    for item in (data.get("items") or [])[:max_users]:
        # Per-candidate try/except: one account whose profile defeats the name
        # comparison must not cost the other candidates or the contact.
        try:
            handle = ((item or {}).get("login") or "").strip()
            if not handle:
                continue
            fields = github_api_fields(handle, timeout=timeout) or {}
            full = (fields.get("fullname") or "").strip()
            if not full or not _name_confirms(name, full):
                continue
            company = (fields.get("org") or "").strip()
            loc = (fields.get("location") or "").strip()
            org_ok = bool(org) and bool(company) and org_name_in_text(org, company)
            city_ok = bool(city_head) and bool(loc) and city_head in loc.lower()
            if not (org_ok or city_ok):
                continue
        except Exception:  # noqa: BLE001
            continue
        out.append({
            "handle": handle, "fullname": full, "company": company,
            "location": loc, "blog_url": fields.get("blog_url", ""),
            "bio": fields.get("bio", ""),
            "why": ("profile name confirms the contact and the profile's %s agrees"
                    % ("company" if org_ok else "location")),
        })
    rec["findings_count"] = len(out)
    return out, rec



# ── Sites where a handle "existing" carries no information ───────────────────
# Some sites serve a profile-shaped page for any string. Measured: picsart and
# trello returned byte-identical pages for a real handle and for one that cannot
# exist, while github, calendly and snapchat answered 404 for the control. Without
# this check every swept contact collected "profiles" on the permissive sites.
_CONTROL_HANDLE = "qx7zzvnoexist4419"
_SOFT404_TTL = 30 * 86400
_SOFT404_CACHE = Path(
    os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
) / "commons" / "data" / "ocas-scout" / "soft404-sites.json"


def _soft404_cache_read():
    try:
        return json.loads(_SOFT404_CACHE.read_text())
    except Exception:  # noqa: BLE001
        return {}


def _soft404_cache_write(cache):
    try:
        _SOFT404_CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = _SOFT404_CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps(cache, indent=1, sort_keys=True))
        tmp.replace(_SOFT404_CACHE)
    except Exception:  # noqa: BLE001
        pass


def site_answers_for_any_handle(url, handle):
    """True when the site returns the same page for a handle that cannot exist.

    Finding a handle on such a site is not evidence that an account is there, let
    alone whose it is. Inconclusive probes return False on purpose: a site is
    never rejected because the measurement failed. Cached per host for 30 days.
    """
    if not url or not handle or handle.lower() not in url.lower():
        return False
    host = _host_of(url)
    if not host:
        return False
    cache = _soft404_cache_read()
    ent = cache.get(host)
    now = time.time()
    if ent and (now - ent.get("checked_at", 0)) < _SOFT404_TTL:
        return bool(ent.get("answers_for_any"))

    ctrl_url = re.sub(re.escape(handle), _CONTROL_HANDLE, url, flags=re.IGNORECASE)
    # Visible text, not raw bytes: fetch_page_text strips scripts and markup, so
    # the comparison works regardless of how much boilerplate the page carries,
    # and is not defeated by a page too large to read in full.
    r_title, r_body = fetch_page_text(url)
    c_title, c_body = fetch_page_text(ctrl_url)

    verdict, reason = False, "inconclusive"
    if not (r_title or r_body):
        reason = "the profile page itself could not be read"
    elif not (c_title or c_body):
        # A 404, or nothing at all, for a handle that cannot exist: the site
        # distinguishes real handles from invented ones.
        reason = "a handle that cannot exist returns nothing"
    else:
        _ph = "@@handle@@"
        rn = (re.sub(re.escape(handle), _ph, r_title + " " + r_body[:4000],
                     flags=re.IGNORECASE)).strip()
        cn = (re.sub(re.escape(_CONTROL_HANDLE), _ph, c_title + " " + c_body[:4000],
                     flags=re.IGNORECASE)).strip()
        if rn == cn:
            verdict = True
            reason = ("a handle that cannot exist returns the same page "
                      "(identical title and text)")
        else:
            reason = "a handle that cannot exist returns a different page"

    cache[host] = {"answers_for_any": verdict, "checked_at": now, "reason": reason}
    _soft404_cache_write(cache)
    return verdict


def _name_confirms(contact_name, profile_fullname):
    """Strict 'this profile's own name IS the contact's name'.

    Used ONLY to decide whether a FETCHED name confirms a hand-entered URL, and
    deliberately stricter than _name_agreement: the family names must be equal
    AND the given name has to appear too, so 'Peggy Smith' never confirms a URL
    filed under 'John Smith'. It is also free of token_overlap_ratio's >=4-char
    filter, which makes short family names ('Mun') invisible.
    """
    a = normalize_name(contact_name).split()
    b = normalize_name(profile_fullname).split()
    if not a or not b:
        return False
    if a[-1] != b[-1]:
        return False
    return len(set(a) & set(b)) >= min(2, len(a), len(b))


# --------------------------------------------------------------------------
# Employer NAME -> company domain
# --------------------------------------------------------------------------
# Measured on this address book: of the contacts with no address and no profile
# URL, the large majority still carry an EMPLOYER NAME, and a smaller number an
# occupation, a city or a phone. Only a handful hold nothing but a name. So the
# population this pipeline fails on is not "no signal" — it is "we know where
# they work and cannot use it". An employer NAME is unusable on its own: address
# permutation, first-party team pages and a site: filter all need a DOMAIN.
# Resolving one is therefore the step that unblocks the rest.
#
# A WRONG domain is worse than none, because everything downstream consumes it:
# it would manufacture address permutations at a stranger's company and mine a
# stranger's team page. So a candidate domain is never reported on the strength
# of its NAME alone — it is fetched, and the page has to name the company.
# Anything unverifiable is discarded rather than reported at low confidence.

_ORG_LEGAL_SUFFIXES = {
    "inc", "llc", "ltd", "limited", "corp", "corporation", "co", "company",
    "plc", "gmbh", "ag", "sa", "sas", "srl", "bv", "nv", "oy", "ab", "aps",
    "pty", "llp", "lp", "pc", "incorporated", "holdings", "holding", "sarl",
}

# Words that carry no identity: an employer named only by one of these is a
# placeholder, not a company, and 'bank.example' would verify against any page
# that says "bank". Refusing them outright is what keeps the guess tier honest.
_ORG_NON_IDENTIFYING = {
    "bank", "company", "school", "university", "college", "hospital", "clinic",
    "church", "restaurant", "cafe", "store", "shop", "office", "team", "group",
    "unknown", "none", "self", "freelance", "student", "retired", "home",
    "personal", "district", "city", "county", "state", "updated", "verification",
    "verified", "consultant", "consulting", "contractor", "various", "private",
    "misc", "other", "test", "temp", "family", "friend", "work", "job",
}

# Words that qualify a company name without identifying it. Dropping them gives
# a second slug to test, so 'Examplecorp Global Services' can still reach
# examplecorp.test.
_ORG_GENERIC_WORDS = {
    "the", "and", "of", "group", "international", "global", "worldwide",
    "company", "services", "service", "solutions", "systems", "partners",
    "associates", "enterprises", "ventures", "industries", "works",
}

# Hosts carrying a page for every company on earth. A directory entry is not a
# company's own site, and accepting one would aim every downstream technique at
# the directory. An EXACT slug match is exempt below, so an employer that really
# is one of these still resolves to itself.
_DIRECTORY_HOSTS = (
    "linkedin.com", "crunchbase.com", "wikipedia.org", "wikidata.org",
    "wikimedia.org", "bloomberg.com", "glassdoor.com", "indeed.com",
    "ziprecruiter.com", "zoominfo.com", "rocketreach.co", "apollo.io",
    "pitchbook.com", "owler.com", "dnb.com", "yelp.com", "tripadvisor.com",
    "mapquest.com", "yellowpages.com", "bbb.org", "g2.com", "capterra.com",
    "trustpilot.com", "producthunt.com", "wellfound.com", "angel.co",
    "medium.com", "substack.com", "github.com", "gitlab.com", "apps.apple.com",
    "play.google.com", "facebook.com", "twitter.com", "x.com", "instagram.com",
    "youtube.com", "tiktok.com", "reddit.com", "quora.com", "pinterest.com",
    "sec.gov", "opencorporates.com", "bizapedia.com", "manta.com",
    "chamberofcommerce.com", "sitejabber.com", "amazon.com", "ebay.com",
    "etsy.com", "muckrack.com", "f6s.com", "similarweb.com", "builtin.com",
    "levels.fyi", "yellowpages.ca", "doximity.com", "healthgrades.com",
    "webmd.com", "vitals.com", "zocdoc.com", "wikiwand.com", "dbpedia.org",
    "archive.org", "issuu.com", "scribd.com", "slideshare.net", "wordpress.com",
    "blogspot.com", "wixsite.com", "weebly.com", "godaddysites.com",
)

# A host answering with a for-sale placeholder names nobody.
_PARKED_MARKERS = (
    "domain is for sale", "buy this domain", "this domain is parked",
    "domain parking", "hugedomains", "afternic", "sedo.com",
    "is available for purchase", "domain name is for sale",
    "parked free, courtesy", "buy now for", "inquire about this domain",
)

# TLDs guessed from a flattened employer name, cheapest and commonest first.
_ORG_GUESS_TLDS = ("com", "org", "io", "co", "net", "ai")
_ORG_GUESS_TLDS_EDU = ("edu", "ac.uk", "org")

_ACADEMIC_WORDS = (
    "university", "universite", "universidad", "college", "institute",
    "school", "academy", "polytechnic", "faculty", "campus",
)


def _registrable_label(host):
    """The label a company's identity lives in: 'eightsleep' in eightsleep.test."""
    host = (host or "").strip().lower().rstrip(".")
    host = host.removeprefix("www.")
    labels = [part for part in host.split(".") if part]
    if len(labels) < 2:
        return ""
    if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in (
            "co", "com", "org", "net", "ac", "gov", "edu"):
        return labels[-3]
    return labels[-2]


def registrable_domain(host):
    """The domain a company is reachable at: 'accounts.example.test' -> example.test.

    Search returns whatever page ranked — a login host, a regional host — and
    every downstream use (address permutation, a site: filter) needs the
    registrable domain instead.
    """
    host = (host or "").strip().lower().rstrip(".")
    host = host.removeprefix("www.")
    labels = [part for part in host.split(".") if part]
    if len(labels) < 2:
        return ""
    if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in (
            "co", "com", "org", "net", "ac", "gov", "edu"):
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def org_slug_variants(org):
    """Every flattened spelling of an employer name worth testing against a host.

    A parenthetical is treated as an alternative name rather than part of the
    name, because it usually IS one ('Examplecorp Design (ExCoXD)'), and a
    legal suffix is dropped because no one registers it.
    """
    org = (org or "").strip()
    if not org:
        return []
    out = []

    def _add(s):
        if s and len(s) >= 3 and s not in out:
            out.append(s)

    inner = re.findall(r"\(([^)]{2,40})\)", org)
    outer = re.sub(r"\([^)]*\)", " ", org)
    for form in [outer, org] + inner:
        toks = [t for t in re.split(r"[^a-z0-9]+", fold_accents(form).lower()) if t]
        if not toks:
            continue
        core = list(toks)
        while core and core[-1] in _ORG_LEGAL_SUFFIXES:
            core.pop()
        _add("".join(core))
        _add("".join(toks))
        if core and core[0] == "the":
            _add("".join(core[1:]))
        sig = [t for t in core if t not in _ORG_GENERIC_WORDS]
        if sig != core:
            _add("".join(sig))
        # The head word ALONE is deliberately not a variant. Measured: it
        # resolved a three-word employer to an unrelated company sharing only
        # its first word, and did so at the highest confidence, because the head
        # word also satisfied the page check. Dropping it turned two false
        # domains into honest misses.
    return out


def org_is_resolvable(org):
    """(ok, reason) — whether an employer name can be resolved to a domain at all.

    A single non-identifying word is refused: 'bank' would verify against any
    page containing the word, and a domain accepted that way poisons every
    technique downstream of it. Very short names are refused for the same
    reason — a three-letter string appears everywhere — and are left to the peer
    tier, which needs no guessing at all.
    """
    org = (org or "").strip()
    if not org:
        return False, "no employer on file"
    toks = [t for t in re.split(r"[^a-z0-9]+", fold_accents(org).lower()) if t]
    core = [t for t in toks if t not in _ORG_LEGAL_SUFFIXES]
    if not core:
        return False, "employer name is only a legal suffix"
    if all(t in _ORG_NON_IDENTIFYING for t in core):
        return False, "employer name identifies no particular company"
    slugs = org_slug_variants(org)
    if not slugs:
        return False, "employer name has no usable form"
    if max(len(s) for s in slugs) < 4 and not org_is_acronym(org):
        return False, "employer name is too short to guess or search safely"
    return True, ""


def org_is_acronym(org):
    """True for an employer written as a short all-caps acronym.

    A three-letter name is far too generic to accept on a body-text match, which
    is why the length gate refuses one. An acronym is still a real employer
    though, so it is allowed back in under a stricter test: the domain has to be
    named exactly after it AND display it, in capitals, in the page TITLE.
    """
    org = (org or "").strip()
    if not re.fullmatch(r"[A-Za-z]{3,5}", org):
        return False
    return org.isupper()


def org_name_in_text(org, text):
    """True when the text actually NAMES the company, not merely echoes a word.

    The company's words have to appear together and in order; a page that says
    'design' and 'studio' in unrelated sentences has not named Example Design
    Studio. This is the check that turns a guessed domain into a verified one.
    """
    org = (org or "").strip()
    if not org or not text:
        return False
    hay = " " + re.sub(r"[^a-z0-9]+", " ", fold_accents(text).lower()).strip() + " "
    flat = hay.replace(" ", "")
    for slug in org_slug_variants(org):
        if len(slug) >= 6 and slug in flat:
            return True
    toks = [t for t in re.split(r"[^a-z0-9]+", fold_accents(org).lower()) if t]
    core = [t for t in toks if t not in _ORG_LEGAL_SUFFIXES]
    if not core:
        return False
    if len(core) >= 2 and (" " + " ".join(core) + " ") in hay:
        return True
    sig = [t for t in core if t not in _ORG_GENERIC_WORDS]
    if len(sig) >= 2 and (" " + " ".join(sig) + " ") in hay:
        return True
    if len(core) == 1 and len(core[0]) >= 5:
        return (" " + core[0] + " ") in hay
    return False


def org_named_in_title(org, title):
    """The stricter test a one-word or acronym employer has to pass.

    A single common word appearing somewhere in a page's body says nothing —
    measured, it accepted an unrelated company for a one-word employer. A page
    that is actually the company's puts the name in its TITLE.
    """
    if org_is_acronym(org):
        return bool(re.search(r"\b" + re.escape(org.strip()) + r"\b", title or ""))
    return org_name_in_text(org, title or "")


def _host_org_match(host, slugs):
    """How strongly a host's own name matches the employer's: '' when it does not."""
    root = _registrable_label(host)
    if not root:
        return ""
    flat_host = re.sub(r"[^a-z0-9]", "", (host or "").lower())
    for s in slugs:
        if root == s:
            return "exact"
    for s in slugs:
        # TRUNCATION only: 'examplecorp' for 'Examplecorp Residential' is the
        # parent company. The reverse — a host that EXTENDS the employer name
        # with another word — is a DIFFERENT organisation that happens to start
        # the same way, and it produced two of the wrong answers measured here
        # (an arena named after a software company, and a manufacturer sharing
        # a founder's surname with a consultancy).
        if len(s) >= 5 and len(root) >= 5 and s.startswith(root) and (
                len(s) - len(root)) <= 4:
            return "prefix"
    for s in slugs:
        if len(s) >= 7 and s in flat_host:
            return "contains"
    return ""


def _is_directory_host(host):
    return any(_host_matches(host or "", d) for d in _DIRECTORY_HOSTS)


def company_domain_from_peers(org, peers):
    """The domain other contacts at the SAME employer are already reachable at.

    This tier needs no network and no guessing, and it is the only one that can
    resolve an employer whose domain is nothing like its name. `peers` is an
    iterable of (org_name, email) or (org_name, email, person_name) the caller
    supplies — scout does not read the address book itself.

    Two guards, both earned: a single colleague's address is not evidence about
    the employer (measured, one contact filed under a well-known employer had a
    VANITY address, and the naive version resolved that employer to that
    person's own site — which would then have been mined for a stranger's
    staff and permuted into invented addresses); and a vanity domain built from
    the peer's own name is their site whatever their employer says, which is
    exactly what employer_from_email already recognises. So a domain is accepted
    on one peer only when it is also NAMED after the employer, and otherwise
    needs two independent colleagues.
    """
    slugs = set(org_slug_variants(org))
    if not slugs:
        return ""
    counts = {}
    for peer in (peers or []):
        try:
            peer_org, peer_email = peer[0], peer[1]
            peer_name = peer[2] if len(peer) > 2 else ""
        except Exception:  # noqa: BLE001
            continue
        if not peer_org or not peer_email or "@" not in peer_email:
            continue
        if not (slugs & set(org_slug_variants(peer_org))):
            continue
        # "" here means free mail or the peer's OWN vanity domain, neither of
        # which names an employer.
        if not employer_from_email(peer_email, peer_name):
            continue
        dom = registrable_domain(peer_email.strip().lower().rsplit("@", 1)[-1])
        if not dom:
            continue
        counts.setdefault(dom, set()).add(peer_email.strip().lower())
    for dom, addrs in sorted(counts.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(addrs) >= 2 or _host_org_match(dom, list(slugs)):
            return dom
    return ""


def verify_company_domain(org, domain, timeout=10):
    """(ok, evidence) — fetch the domain and require the page to name the company."""
    domain = (domain or "").strip().lower().rstrip(".")
    if not domain or "." not in domain:
        return False, "not a domain"
    # Two attempts on https before falling back: a single transient empty read
    # on a company's real domain was measured handing the answer to an unrelated
    # company at the same name on another TLD.
    title, body = "", ""
    for url in ("https://" + domain, "https://" + domain, "http://" + domain):
        title, body = fetch_page_text(url, timeout=timeout)
        if title or body:
            break
    if not (title or body):
        return False, "host did not answer"
    if not title.strip():
        # A company's own site has a title. A page without one is a redirect
        # stub or a placeholder, and one such host verified purely on body text.
        return False, "page has no title"
    hay = (title + " " + body[:8000])
    low = hay.lower()
    for marker in _PARKED_MARKERS:
        if marker in low:
            return False, "for-sale placeholder, not a company site"
    toks = [t for t in re.split(r"[^a-z0-9]+", fold_accents(org).lower()) if t]
    core = [t for t in toks if t not in _ORG_LEGAL_SUFFIXES]
    if len(core) <= 1 or org_is_acronym(org):
        # One common word appearing in a page's body is not evidence. Measured:
        # it accepted an unrelated company for a one-word employer, which would
        # then have sourced that company's staff page.
        if not org_named_in_title(org, title):
            return False, "one-word employer is not named in the page title"
    elif not org_name_in_text(org, hay):
        return False, "page does not name the company"
    return True, (title[:150] or domain)


def company_domain_search_candidates(org, searxng_url=None, limit=8):
    """Hosts a web search associates with the employer name, best-named first.

    RANK IS NOT USED as the discriminator. Measured against this SearXNG: the
    right company site is usually somewhere in the first page but almost never
    first — unrelated popular sites outrank it — while the host's own NAME
    separates them cleanly. So results are re-ordered by how well the host is
    named after the company, and the page fetch still decides.
    """
    slugs = org_slug_variants(org)
    if not slugs:
        return []
    scored, seen = [], set()
    _RANK = {"exact": 0, "prefix": 1, "contains": 2, "": 3}
    for query in ('"%s" official site' % org, "%s official website" % org):
        try:
            hits = searxng_search(query, limit=limit, searxng_url=searxng_url)
        except Exception:  # noqa: BLE001
            hits = []
        for pos, hit in enumerate(hits):
            host = registrable_domain(_host_of(hit.get("url") or ""))
            if not host or host in seen:
                continue
            seen.add(host)
            match = _host_org_match(host, slugs)
            if _is_directory_host(host) and match != "exact":
                continue
            if not match:
                continue          # a host not named after the company is noise
            scored.append((_RANK[match], pos, host, match))
    scored.sort()
    return [(h, m) for _r, _p, h, m in scored]


def company_domain_guesses(org):
    """<flattened employer>.<tld> — the cheapest candidates, always verified."""
    slugs = [s for s in org_slug_variants(org)
             if len(s) >= 4 or org_is_acronym(org)]
    if not slugs:
        return []
    tlds = (_ORG_GUESS_TLDS_EDU
            if any(w in fold_accents(org or "").lower() for w in _ACADEMIC_WORDS)
            else _ORG_GUESS_TLDS)
    out = []
    for slug in slugs[:2]:
        for tld in tlds:
            cand = "%s.%s" % (slug, tld)
            if cand not in out:
                out.append(cand)
    return out


# How much each way of arriving at a domain is worth. A colleague's observed
# address beats a search hit named after the company, which beats the obvious
# guess, which beats a host merely CONTAINING the company's name.
_COMPANY_METHOD_RANK = {
    "peer_email": 0, "search:exact": 1, "guess:primary": 2,
    "search:prefix": 3, "guess:alt": 4, "search:contains": 5,
}
_COMPANY_METHOD_CONFIDENCE = {
    "peer_email": 0.95, "search:exact": 0.9, "guess:primary": 0.85,
    "search:prefix": 0.8, "guess:alt": 0.75, "search:contains": 0.75,
}


def resolve_company_domain(org, peers=None, searxng_url=None, enable_search=True,
                           enable_guess=True, timeout=10, max_verifications=8):
    """(record|None, [PersonToolRecord]) — the employer's real domain.

    Fail-soft everywhere: a dead search container, an unreachable host or a
    malformed employer name costs one tool entry and nothing else. Returns None
    rather than a low-confidence guess, because a wrong domain is consumed by
    every technique downstream and would fabricate data at another company.
    """
    org = (org or "").strip()
    recs = []
    rec = {"tool_name": "company_domain", "invoked_at": _now(),
           "input_type": "org", "input_value": org[:120],
           "status": "error", "findings_count": 0, "error": None}
    ok, why = org_is_resolvable(org)
    if not ok:
        rec["status"] = "skipped"
        rec["error"] = why
        recs.append(rec)
        return None, recs

    peer_dom = ""
    try:
        peer_dom = company_domain_from_peers(org, peers)
    except Exception as e:  # noqa: BLE001
        rec["error"] = str(e)[:200]
    if peer_dom:
        rec["status"] = "success"
        rec["findings_count"] = 1
        recs.append(rec)
        return {"domain": peer_dom, "method": "peer_email", "confidence": 0.95,
                "evidence": "another contact at this employer is reachable "
                            "at this domain", "verified": True}, recs

    # Candidates are tried in order of how much the METHOD is worth, not in the
    # order they arrived. Measured both ways on the same employers: searching
    # first lost a four-letter employer whose obvious domain was never reached,
    # and guessing first resolved three well-known employers to unrelated
    # companies holding the same name on another TLD. Ranking gets both.
    scored = []
    if enable_search:
        try:
            for host, match in company_domain_search_candidates(
                    org, searxng_url=searxng_url):
                scored.append((_COMPANY_METHOD_RANK.get("search:" + match, 9),
                               host, "search:" + match))
        except Exception as e:  # noqa: BLE001
            rec["error"] = str(e)[:200]
    if enable_guess:
        for idx, guess in enumerate(company_domain_guesses(org)):
            method = "guess:primary" if idx == 0 else "guess:alt"
            scored.append((_COMPANY_METHOD_RANK[method], guess, method))
    scored.sort(key=lambda t: t[0])
    candidates, seen_dom = [], set()
    for _rank, host, method in scored:
        host = registrable_domain(host) or host
        if host in seen_dom:
            continue
        seen_dom.add(host)
        candidates.append((host, method))

    tried, dead_slugs = [], set()
    for host, method in candidates[:max_verifications]:
        # An unreachable <employer>.com is not evidence that <employer>.org is
        # the employer — it is evidence that we cannot tell. Measured: two
        # well-known employers whose own site refuses this fetcher were resolved
        # to unrelated companies holding the same name on another TLD. When the
        # primary guess cannot be read, the alternates of that same name are
        # abandoned rather than promoted.
        if method == "guess:alt" and _registrable_label(host) in dead_slugs:
            continue
        try:
            good, evidence = verify_company_domain(org, host, timeout=timeout)
        except Exception as e:  # noqa: BLE001
            tried.append("%s: %s" % (host, str(e)[:40]))
            continue
        if not good:
            tried.append("%s: %s" % (host, evidence))
            if evidence in ("host did not answer", "page has no title"):
                dead_slugs.add(_registrable_label(host))
            continue
        rec["status"] = "success"
        rec["findings_count"] = 1
        recs.append(rec)
        conf = _COMPANY_METHOD_CONFIDENCE.get(method, 0.7)
        return {"domain": host, "method": method, "confidence": conf,
                "evidence": evidence, "verified": True,
                "rejected": tried[:6]}, recs

    rec["status"] = "success" if candidates else "error"
    rec["error"] = ("no candidate domain named the company (%s)"
                    % "; ".join(tried[:4])) if tried else "no candidate domains"
    recs.append(rec)
    return None, recs


# --------------------------------------------------------------------------
# First-party company people pages
# --------------------------------------------------------------------------
# Once the employer's domain is known, the company's own team page is the
# highest-grade source available for someone with no profile anywhere: it is
# first-party, it is not auth-walled, and it usually carries a job title next to
# the name. It is reached ONLY through a verified domain — a page mined from a
# guessed domain would describe a different company's staff.
_COMPANY_PEOPLE_PATHS = (
    "/team", "/about", "/about-us", "/people", "/leadership", "/staff",
    "/our-team", "/who-we-are", "/company/team", "/about/team", "/team/",
    "/contact", "/founders", "/management",
)
_MAX_COMPANY_PAGES = 6

# Measured on four real company domains: GUESSING these paths found nothing.
# Three answered 404 for every one of them, and the fourth linked its
# management page from its own homepage at a nested, extension-bearing path no
# fixed list would ever contain. So the site's own navigation is the primary
# source and the path list is only the fallback.
_TEAM_LINK_RE = re.compile(
    r"(?:^|[/_\-])(?:team|about|about-?us|people|leadership|staff|"
    r"who-?we-?are|our-?story|our-?team|founders|management|bios?)"
    r"(?:$|[/_.?\-])", re.IGNORECASE)


def company_people_page_urls(domain, timeout=12, max_urls=_MAX_COMPANY_PAGES):
    """Where a company lists its people: its own links first, then guesses."""
    domain = (domain or "").strip().lower().rstrip("/")
    if not domain or "." not in domain:
        return []
    base = domain if domain.startswith("http") else "https://" + domain
    host = _host_of(base)
    out, seen = [], set()

    def _add(u):
        u = (u or "").split("#")[0].strip()
        if not u or len(out) >= max_urls:
            return
        key = u.rstrip("/").lower()
        if key in seen:
            return
        seen.add(key)
        out.append(u)

    raw = fetch_page_html(base, timeout=timeout)
    for m in _HREF_RE.finditer(raw or ""):
        href = m.group(1).strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        full = urllib.parse.urljoin(base + "/", href)
        if not full.startswith("http") or _host_of(full) != host:
            continue
        path = urllib.parse.urlparse(full).path or "/"
        if path in ("", "/"):
            continue
        if _TEAM_LINK_RE.search(path):
            _add(full)
    for path in _COMPANY_PEOPLE_PATHS:
        _add(base.rstrip("/") + path)
    return out[:max_urls]


def _name_phrase_spans(name, text, name_given="", name_family="", max_gap=2):
    """Where the text names the contact — [(start, end)], empty when it does not.

    Same standard as _name_phrase_in_text (which delegates here): the given and
    family names have to appear as a name, not merely both somewhere on a page.
    """
    given, family = _split_name(name, name_given, name_family)
    g = re.sub(r"[^a-z0-9]", "", fold_accents(given or "").lower())
    f = re.sub(r"[^a-z0-9]", "", fold_accents(family or "").lower())
    if not g or not f:
        return []
    low = fold_accents(text or "").lower()
    g_spans = [m.span() for m in re.finditer(r"\b" + re.escape(g) + r"\b", low)]
    f_spans = [m.span() for m in re.finditer(r"\b" + re.escape(f) + r"\b", low)]
    if not g_spans or not f_spans:
        return []
    _JOIN = re.compile(r"[\s\-]*")
    _MIDDLE = re.compile(r"[\s\-]*[a-z]{1,12}\.?[\s\-]*")
    _INVERTED = re.compile(r"\s*,\s*")
    out = []
    for gs in g_spans:
        for fs in f_spans:
            if fs[0] >= gs[1]:
                between = low[gs[1]:fs[0]]
                if _JOIN.fullmatch(between) or (
                        max_gap >= 1 and _MIDDLE.fullmatch(between)):
                    out.append((gs[0], fs[1]))
            elif gs[0] >= fs[1]:
                if _INVERTED.fullmatch(low[fs[1]:gs[0]]):
                    out.append((fs[0], gs[1]))
    return sorted(set(out))


def role_near_name(name, text, name_given="", name_family="", window=120):
    """A job title sitting next to the contact's name on a page, or ''.

    Deliberately narrow. Mining arbitrary prose for a title is what previously
    produced nonsense values, so the fragment must start within a short window
    of the name, must contain an actual role word, and must be short enough to
    be a title rather than a sentence.
    """
    spans = _name_phrase_spans(name, text, name_given, name_family)
    if not spans:
        return ""
    for _start, end in spans[:4]:
        tail = (text or "")[end:end + window]
        tail = re.sub(r"\s+", " ", tail).strip(" ,;:|-–—·")
        for frag in [x.strip() for x in _TITLE_SEP.split(tail) if x.strip()]:
            frag = re.split(r"[.!?\n]", frag)[0].strip()
            low = frag.lower()
            if 3 < len(frag) <= 70 and any(w in low for w in _ROLE_WORDS):
                return frag
    return ""


def mine_company_people_page(domain, name, name_given="", name_family="",
                             org="", timeout=12, max_pages=_MAX_COMPANY_PAGES):
    """Find the contact on their employer's own team/about/people page.

    Returns (hit|None, [PersonToolRecord]). A hit means the page NAMES the
    contact by the same adjacency standard every other page faces — it is not
    enough for the page to contain their given name and somebody else's family
    name. Fail-soft: an unreachable path costs nothing but a tool entry.
    """
    domain = (domain or "").strip().lower().rstrip("/")
    recs = []
    if not domain or "." not in domain:
        return None, recs
    checked = 0
    for url in company_people_page_urls(domain, timeout=timeout,
                                        max_urls=max_pages):
        if checked >= max_pages:
            break
        checked += 1
        rec = {"tool_name": "company_people_page", "invoked_at": _now(),
               "input_type": "url", "input_value": url, "status": "success",
               "findings_count": 0, "error": None}
        try:
            title, body = fetch_page_text(url, timeout=timeout)
        except Exception as e:  # noqa: BLE001
            rec["status"] = "error"
            rec["error"] = str(e)[:200]
            recs.append(rec)
            continue
        if not (title or body):
            rec["status"] = "error"
            rec["error"] = "no page"
            recs.append(rec)
            continue
        hay = title + " " + body
        if not _name_phrase_in_text(name, hay, name_given, name_family):
            recs.append(rec)
            continue
        rec["findings_count"] = 1
        recs.append(rec)
        emails = []
        given, family = _split_name(name, name_given, name_family)
        for em in set(re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", body)):
            low = em.lower()
            if low in _PLACEHOLDER_EMAILS:
                continue
            local = re.sub(r"[^a-z0-9]", "", low.split("@")[0])
            # Only an address built from THIS contact's name. A team page also
            # lists everyone else's, and a generic info@ belongs to nobody.
            if (given and family and local
                    and (family in local or (given in local and len(given) >= 4))):
                emails.append(low)
        return ({
            "url": url,
            "title": title[:150],
            "occupation": role_near_name(name, hay, name_given, name_family),
            "emails": sorted(emails)[:2],
            "domain": domain,
            "org": org,
        }, recs)
    return None, recs


# --------------------------------------------------------------------------
# Additional site: tiers
# --------------------------------------------------------------------------
# The site: tier previously covered only LinkedIn and GitHub. These are the
# other places a person with no address is actually indexed, chosen PER CONTACT
# from what the record already says — sweeping all of them for everyone would
# multiply the query budget for no yield.
# MEASURED, and this is why the list is short. A candidate is only ever
# promoted if the PAGE ITSELF names the contact, so a site this fetcher cannot
# read can never produce anything but an unverifiable candidate. Fetched
# directly: crunchbase.com and muckrack.com return nothing at all (bot-walled),
# behance.net returns nothing, and orcid.org returns a five-byte JavaScript
# shell. Querying them would spend the search budget on results that cannot
# clear our own gate, so they are deliberately NOT here. dribbble.com,
# speakerdeck.com, wellfound.com and university hosts all return real text and
# are kept.
_DESIGN_WORDS = ("designer", "design", "illustrator", "artist", "animator",
                 "photographer", "art director", "creative", "ux", "ui")
_ACADEMIC_ROLE_WORDS = ("professor", "researcher", "scientist", "phd", "postdoc",
                        "lecturer", "fellow", "faculty", "research")
_STARTUP_WORDS = ("founder", "co-founder", "ceo", "cto", "coo", "cfo",
                  "investor", "partner", "president", "head of", "vp")

MAX_TARGETED_SITE_QUERIES = 4


def build_targeted_site_queries(name, org="", occupation="", org_domain="",
                                limit=MAX_TARGETED_SITE_QUERIES):
    """site: queries chosen from what the contact record already says.

    Each is a filter, not a guess: a hit is a page on a site that indexes people
    of that kind, and it still has to pass the same page-level name gate as
    every other candidate.
    """
    name = (name or "").strip()
    if not name:
        return []
    role = " ".join([(occupation or ""), (org or "")]).lower()
    out = []

    def _add(q):
        q = re.sub(r"\s+", " ", q).strip()
        if q and q not in out:
            out.append(q)

    # The employer's own domain: the most specific filter available, and the
    # only one that is first-party.
    if org_domain:
        _add('site:%s "%s"' % (org_domain, name))
    if (any(w in role for w in _ACADEMIC_ROLE_WORDS)
            or any(w in role for w in _ACADEMIC_WORDS)):
        if org_domain and org_domain.endswith((".edu", ".ac.uk", ".ac.jp")):
            _add('site:%s "%s" profile' % (org_domain, name))
    if any(w in role for w in _DESIGN_WORDS):
        _add('site:dribbble.com "%s"' % name)
    if org and any(w in role for w in _STARTUP_WORDS):
        _add('site:wellfound.com "%s"' % name)
    if any(w in role for w in ("engineer", "developer", "programmer",
                               "architect", "data", "software")):
        _add('site:speakerdeck.com "%s"' % name)
    return out[:limit]


# --------------------------------------------------------------------------
# GitHub commit-author addresses
# --------------------------------------------------------------------------
# A GitHub profile carries no email field, but git does: every commit records
# the address its author configured. For a contact with a confirmed GitHub
# account and no address on file, this converts a profile into a real, reachable
# one. Addresses GitHub SYNTHESISES for privacy (the noreply host) are not
# addresses and are dropped.
_GITHUB_API = "https://api.github.com"
_GH_NOREPLY_HOSTS = ("users.noreply.github.com", "noreply.github.com")
_GH_BOT_LOCALS = ("actions-user", "github-actions", "dependabot", "renovate",
                  "greenkeeper", "semantic-release", "bot", "noreply", "root",
                  "runner", "circleci", "travis", "netlify", "vercel")


def _github_token():
    """A GitHub token from the environment or the profile .env, or ''.

    Unauthenticated GitHub allows 60 requests an hour, which one nightly run
    over a whole address book exhausts in minutes; a token raises that to 5000.
    The value is never logged and never appears in a tool record.
    """
    for var in ("SCOUT_GITHUB_TOKEN", "GITHUB_TOKEN", "GH_TOKEN"):
        v = (os.environ.get(var) or "").strip()
        if v:
            return v
    root = (os.environ.get("AGENT_ROOT") or "").strip()
    if not root:
        return ""
    try:
        raw = Path(root, ".env").read_text(errors="ignore")
    except Exception:  # noqa: BLE001
        return ""
    found = ""
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        if key.strip() in ("GITHUB_TOKEN", "GH_TOKEN"):
            val = val.strip().strip('"').strip("'")
            if val:
                found = val          # last definition wins, as a shell would
    return found


def _github_headers():
    headers = {"User-Agent": "hermes-scout/1.0",
               "Accept": "application/vnd.github+json"}
    token = _github_token()
    if token:
        headers["Authorization"] = "Bearer " + token
    return headers


def _github_json(path, timeout=10):
    try:
        req = urllib.request.Request(_GITHUB_API + path, headers=_github_headers())
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return None


def _usable_commit_email(email):
    email = (email or "").strip().lower()
    if not email or not _EMAIL_RE.match(email):
        return False
    local, _, host = email.partition("@")
    if any(host == h or host.endswith("." + h) for h in _GH_NOREPLY_HOSTS):
        return False
    if any(b in local for b in _GH_BOT_LOCALS):
        return False
    if host.endswith((".local", ".localdomain", ".invalid", ".example")):
        return False
    return True


def github_commit_emails(handle, timeout=10, max_repos=2, max_events=100):
    """Addresses a GitHub account has authored commits from.

    Returns ([{email, author_name, source}], PersonToolRecord). The public
    events feed covers roughly the last 90 days, so a quieter account falls back
    to its most recently pushed repositories. Fail-soft: an API error, a rate
    limit or a private account yields [] and a tool entry saying so.
    """
    rec = {"tool_name": "github_commit_emails", "invoked_at": _now(),
           "input_type": "handle", "input_value": handle, "status": "error",
           "findings_count": 0, "error": None,
           "authenticated": bool(_github_token())}
    handle = (handle or "").strip()
    if not handle or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\-]*", handle):
        rec["error"] = "not a github handle"
        return [], rec

    found, seen = [], set()

    def _take(email, author_name, source):
        low = (email or "").strip().lower()
        if not _usable_commit_email(low) or low in seen:
            return
        seen.add(low)
        found.append({"email": low, "author_name": (author_name or "").strip(),
                      "source": source})

    events = _github_json("/users/%s/events/public?per_page=%d"
                          % (urllib.parse.quote(handle), max_events), timeout)
    if events is None:
        rec["error"] = "events API unavailable (rate limit, private or missing)"
    elif isinstance(events, list):
        rec["status"] = "success"
        for ev in events:
            if not isinstance(ev, dict) or ev.get("type") != "PushEvent":
                continue
            for commit in ((ev.get("payload") or {}).get("commits") or []):
                author = (commit or {}).get("author") or {}
                _take(author.get("email"), author.get("name"), "push_event")

    if not found:
        repos = _github_json("/users/%s/repos?sort=pushed&per_page=%d&type=owner"
                             % (urllib.parse.quote(handle), max(1, max_repos)),
                             timeout)
        if isinstance(repos, list):
            rec["status"] = "success"
            for repo in repos[:max_repos]:
                full = (repo or {}).get("full_name") or ""
                if not full or (repo or {}).get("fork"):
                    continue
                commits = _github_json(
                    "/repos/%s/commits?author=%s&per_page=10"
                    % (full, urllib.parse.quote(handle)), timeout)
                if not isinstance(commits, list):
                    continue
                for c in commits:
                    author = ((c or {}).get("commit") or {}).get("author") or {}
                    _take(author.get("email"), author.get("name"),
                          "repo_commits")
                if found:
                    break
    rec["findings_count"] = len(found)
    if found and rec["status"] != "success":
        rec["status"] = "success"
    return found[:5], rec


# --------------------------------------------------------------------------
# Reverse image search on an avatar — NOT IMPLEMENTED, and why
# --------------------------------------------------------------------------
def reverse_image_search(image_url, timeout=10):
    """Always ({}, record) — there is no key-free reverse-image service to use.

    Checked rather than assumed: TinEye, Bing Visual Search and Google Vision
    all require an API key; Google Lens and Yandex expose no documented
    endpoint and gate the web form behind bot detection; and SearXNG searches
    images BY QUERY, not by image, so the local container cannot stand in for
    one. The two avatars this pipeline already holds also need it least — a
    Gravatar is keyed on the md5 of the address it belongs to, and a GitHub
    avatar URL carries that account's numeric id, so both are already bound to
    an identity without any lookup. Kept as an explicit negative so the next
    pass does not re-derive it.
    """
    return {}, {"tool_name": "reverse_image", "invoked_at": _now(),
                "input_type": "url", "input_value": (image_url or "")[:200],
                "status": "unavailable", "findings_count": 0,
                "error": "no key-free reverse-image endpoint exists"}


# --------------------------------------------------------------------------
# Known-URL short circuit
# --------------------------------------------------------------------------
def expand_known_urls(name, known_urls):
    """Turn hand-entered contact URLs into profile records.

    Cheap fetches only: GitHub via its users API, an unknown host via <title>.
    LinkedIn is auth-walled and is recorded WITHOUT any fetch attempt.
    Returns (profile_records, website_candidates, tool_records).

    Only real sites/blogs become website candidates. A profile page is not the
    person's website — it is surfaced through known_profiles / social_profiles
    instead, so nothing writes a LinkedIn URL into a `website` field.
    """
    profiles, websites, tools = [], [], []
    seen = set()
    for raw in known_urls or []:
        parsed = parse_profile_url(raw)
        if not parsed:
            continue
        key = parsed["url"].rstrip("/").lower()
        if key in seen:
            continue
        seen.add(key)
        pending_websites = []

        prof = {
            "site": parsed["platform"],
            "handle": parsed["handle"],
            "url": parsed["url"],
            "fullname": "",
            "location": "",
            "bio": "",
            "blog_url": "",
            "provenance": "contact_record",
            "curated": True,
            "kind": parsed["kind"],
            "handle_origin": "known_url",
        }

        if parsed["platform"] == "GitHub" and parsed["handle"]:
            rec = {"tool_name": "github_api", "invoked_at": _now(),
                   "input_type": "handle", "input_value": parsed["handle"],
                   "status": "success", "findings_count": 0, "error": None}
            gh = github_api_fields(parsed["handle"]) or {}
            if not gh:
                rec["status"] = "error"
                rec["error"] = "no data"
            for k in ("fullname", "org", "location", "blog_url", "bio"):
                if gh.get(k):
                    prof[k] = gh[k]
            rec["findings_count"] = len([k for k in gh if gh.get(k)])
            tools.append(rec)
            if prof.get("blog_url"):
                pending_websites.append((prof["blog_url"], "github_blog", prof["url"]))
        elif parsed["platform"] == "LinkedIn":
            # Auth-walled. Record the anchor; never scrape. A LinkedIn profile
            # is NOT a website candidate.
            prof["fetch_skipped"] = "auth_walled"
        elif parsed["kind"] == "website":
            rec = {"tool_name": "page_title", "invoked_at": _now(),
                   "input_type": "url", "input_value": parsed["url"],
                   "status": "success", "findings_count": 0, "error": None}
            title = fetch_page_title(parsed["url"]) or ""
            if title:
                prof["title"] = title
                rec["findings_count"] = 1
            else:
                rec["status"] = "error"
                rec["error"] = "no title"
            tools.append(rec)
            pending_websites.append((parsed["url"], "curated", parsed["url"]))
        # Any other recognised platform is a profile page, not a website.

        shared, fam = _name_agreement(name, prof.get("fullname", ""))

        prof["name_shared_tokens"] = shared
        prof["family_present"] = fam
        # This disagreement used to be measured here and then never consulted.
        # A hand-entered URL whose fetched profile names SOMEONE ELSE is
        # evidence AGAINST the URL, so it contributes nothing downstream.
        prof["name_conflict"] = bool(prof.get("fullname") and shared == 0 and not fam)
        if not prof["name_conflict"]:
            websites.extend(pending_websites)
        profiles.append(prof)
    return profiles, websites, tools


# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------
def research_person(name, email="", employer="", handles=None, phone="",
                    maigret_timeout=200, top_sites=300, *,
                    org="", occupation="", location_city="",
                    known_urls=None, name_given="", name_family="",
                    enable_search=True, searxng_url=None,
                    max_search_queries=MAX_SEARCH_QUERIES,
                    enable_whois=True, enable_email_permutation=True,
                    email_permutation_limit=MAX_EMAIL_PERMUTATIONS,
                    enable_company_domain=True, org_domain="", peer_emails=None,
                    enable_company_pages=True, enable_github_emails=True,
                    enable_targeted_site_search=True, enable_user_scanner=True,
                    missing_fields=None, enable_github_user_search=True):
    """Run the Tier-1 person pipeline. Returns a structured research result.

    The first seven parameters keep their original positional order so existing
    callers — notably weave_enrich.scout_research_contact — keep working. All
    new context is keyword-only.
    """
    org = (org or employer or "").strip()
    employer = employer or org
    occupation = (occupation or "").strip()
    location_city = (location_city or "").strip()
    known_urls = [u for u in (known_urls or []) if u]

    # Which of the five target fields this contact still lacks. The caller
    # (weave_enrich) knows, because it holds the record; None means "assume all
    # are missing", which is what the CLI and any older caller want. Every
    # expensive technique below is gated on a field it can actually fill, so a
    # contact missing only a LinkedIn URL no longer pays for whois, email
    # permutation and a company-domain resolution that cannot help them.
    _missing = (set(missing_fields) if missing_fields is not None
                else set(TARGET_FIELDS))
    result_missing = sorted(_missing)

    def _wants(*fields):
        return any(f in _missing for f in fields)

    # Region for libphonenumber. A number already on file settles it; otherwise
    # fall back to US, which is what the previous code assumed everywhere.
    _region_hint = "US"
    try:
        _pi0 = phone_intel(phone) if phone else {}
        if _pi0.get("region_code"):
            _region_hint = _pi0["region_code"]
    except Exception:  # noqa: BLE001
        pass

    result = {
        "subject": {"name": name, "email": email, "employer": employer,
                    "phone": phone, "org": org, "occupation": occupation,
                    "location_city": location_city,
                    "known_urls": list(known_urls)},
        "as_of": _now(),
        "tools": [],
        "profiles": [],
        "known_profiles": [],
        "search_candidates": [],
        "registrations": [],
        "email_candidates": [],
        "company": {},
        "company_pages": [],
        "harvested_emails": [],
        "accounts": [],
        "phone_intel": {},
        "findings": [],
        "enrichment": {},
        "identity": {"level": "none", "corroborating_sites": [],
                     "curated_sites": [], "reason": ""},
        # Everything mined out of pages that were fetched anyway. These are
        # CANDIDATES carrying their own provenance; the promotion rules at the
        # bottom of this function decide which become enrichment values.
        "mined": {"phones": [], "emails": [], "cities": [], "websites": []},
        "linkedin_candidates": [],
        "linkedin_rejected": [],
        "linkedin": None,
        "missing_fields": result_missing,
    }

    def _absorb_page(url, raw, text, first_party=False, why="",
                     name_confirmed=False):
        """Mine one already-fetched page for the five target fields.

        `first_party` means the page has ALREADY been confirmed to be the
        contact's own, which is what licenses attributing a phone number or an
        address anywhere on it to them, and what makes a LinkedIn link found
        here the strongest tie available (linkedin_tie -> 'first_party').

        `name_confirmed` is the weaker case: the page NAMES the contact but is
        not theirs -- a staff directory, a conference programme, a news piece.
        A directory lists many people's numbers, so a value anywhere on the page
        cannot be attributed to this one; only values sitting NEXT TO the
        contact's name are taken, using the same adjacency machinery
        (_name_phrase_spans) that role_near_name already relies on. Page-wide
        signals -- tel: links, mailto:, schema.org -- are deliberately not read
        in that case, because they describe the page's owner, not its subject.
        """
        try:
            mined = mine_contact_fields(raw, text, name, name_given, name_family,
                                        region_hint=_region_hint, page_url=url)
        except Exception:  # noqa: BLE001
            return {}
        for u in mined.get("linkedin", []):
            result["linkedin_candidates"].append({
                "url": u, "context": text[:1500],
                "source": "first_party" if first_party else "page",
                "found_on": url, "why": why})
        if not first_party:
            if not name_confirmed:
                return mined
            try:
                spans = _name_phrase_spans(name, text, name_given, name_family)
            except Exception:  # noqa: BLE001
                spans = []
            if not spans:
                return mined
            near = " \n ".join(
                text[max(0, a - 300):b + 300] for a, b in spans[:6])
            try:
                for hit in mine_phones("", near, _region_hint):
                    result["mined"]["phones"].append(
                        {"phone": hit["phone"], "how": "near_name",
                         "source_url": url})
                for hit in mine_emails(near, name):
                    result["mined"]["emails"].append(
                        {"email": hit["email"], "how": "near_name",
                         "source_url": url})
                for hit in mine_city("", near):
                    result["mined"]["cities"].append(
                        {"city": hit["city"], "how": "near_name",
                         "source_url": url})
            except Exception:  # noqa: BLE001
                pass
            return mined
        for hit in mined.get("phones", []):
            result["mined"]["phones"].append(
                {"phone": hit["phone"], "how": hit["how"], "source_url": url})
        for hit in mined.get("emails", []):
            result["mined"]["emails"].append(
                {"email": hit["email"], "how": hit["how"], "source_url": url})
        for hit in mined.get("cities", []):
            result["mined"]["cities"].append(
                {"city": hit["city"], "how": hit["how"], "source_url": url})
        for w in mined.get("websites", []):
            result["mined"]["websites"].append({"website": w, "source_url": url})
        return mined

    # Known phone is an identity anchor already on file. PhoneInfoga is a Go
    # binary and this box has no Go toolchain, but its only offline scanner is
    # libphonenumber, which the agent venv already ships — so carrier, line
    # type, region and timezone are derived directly instead (see phone_intel).
    if phone:
        try:
            pi = phone_intel(phone)
        except Exception:  # noqa: BLE001
            pi = {}
        result["phone_intel"] = pi
        _bits = []
        for _k in ("region_code", "line_type", "carrier", "geo"):
            if pi.get(_k):
                _bits.append("%s=%s" % (_k, pi[_k]))
        result["findings"].append({
            "finding_id": "PH001",
            "claim": ("Contact has a phone number on file (%s)%s." % (
                phone, (" — " + ", ".join(_bits)) if _bits else "")),
            "confidence": "high",
            "source_refs": [{"url": "contact_record", "retrieved_at": _now(),
                             "quote": phone}],
        })
        # The number's registered region is a CANDIDATE for the city, never a
        # value: US numbers are portable, so an area code corroborates a city
        # already on file and cannot establish one on its own.
        if pi.get("geo"):
            _agree = _place_agrees(pi["geo"], location_city)
            result["findings"].append({
                "finding_id": "PH002",
                "claim": (("Phone number's registered region agrees with the "
                           "city on file: %s" % pi["geo"]) if _agree else
                          ("UNVERIFIED CANDIDATE (phone number is registered in "
                           "%s; numbers are portable, so this is not the "
                           "contact's city)" % pi["geo"])),
                "confidence": "med" if _agree else "low",
                "unverified": not _agree,
                "source_refs": [{"url": "libphonenumber:" + (pi.get("e164") or phone),
                                 "retrieved_at": _now(), "quote": pi["geo"]}],
            })

    # ---- Holehe first: it needs only the email. The old code hid it behind
    # the handle-quality gate below, so a generic/absent handle suppressed a
    # tool that never depended on a handle at all.
    if email:
        sites, rec = run_holehe(email)
        result["tools"].append(rec)
        # A second, independently benchmarked source. Kept in the SAME finding
        # because the claim is the same claim — this address is registered
        # there — while result["accounts"] preserves which tool saw what.
        us_sites = []
        if enable_user_scanner:
            try:
                us_sites, us_rec = run_user_scanner(email)
            except Exception as _e:  # noqa: BLE001
                us_sites, us_rec = [], {
                    "tool_name": "user_scanner", "invoked_at": _now(),
                    "input_type": "email", "input_value": email,
                    "status": "error", "findings_count": 0,
                    "error": str(_e)[:200]}
            result["tools"].append(us_rec)
        _h = {s.lower() for s in sites}
        _u = {s.lower() for s in us_sites}
        merged = []
        for site in list(sites) + [s for s in us_sites if s.lower() not in _h]:
            low = site.lower()
            if not _account_site_ok(low, email) or low in {m.lower() for m in merged}:
                continue
            merged.append(site)
            result["accounts"].append({
                "site": site,
                "source": ("both" if (low in _h and low in _u)
                           else ("holehe" if low in _h else "user_scanner")),
            })
        if merged:
            result["findings"].append({
                "finding_id": "H001",
                "claim": f"Email {email} is registered on: {', '.join(merged)}.",
                "confidence": "med",
                "source_refs": [{"url": f"holehe:{email}", "retrieved_at": _now(),
                                 "quote": ", ".join(merged)}],
            })

    # ---- Known-URL short circuit: ground truth the user hand-entered.
    curated_profiles, website_candidates, curated_tools = expand_known_urls(
        name, known_urls)
    result["tools"].extend(curated_tools)
    result["known_profiles"] = [
        {"site": p["site"], "url": p["url"], "handle": p["handle"],
         "kind": p["kind"], "provenance": "contact_record",
         "fullname": p.get("fullname", "")}
        for p in curated_profiles
    ]
    for kidx, prof in enumerate(curated_profiles, start=1):
        result["findings"].append({
            "finding_id": f"K{kidx:03d}",
            "claim": (f"{prof['site']} URL on the contact record: {prof['url']}"
                      + (f" (names '{prof['fullname']}')" if prof.get("fullname") else "")),
            "confidence": "high",
            "source_refs": [{"url": "contact_record", "retrieved_at": _now(),
                             "quote": prof["url"]}],
        })

    # ---- The contact's OWN pages, mined. A URL on the contact record is the
    # owner's assertion that the page is theirs, so it is first-party by the
    # same standard as expand_known_urls already applies. Until now these pages
    # were fetched for their <title> alone and thrown away, which is the most
    # expensive way to learn the least: the contact's own site is where their
    # phone number, their address and their other profiles actually live.
    _fp_seen = set()
    for _prof in curated_profiles:
        if _prof.get("name_conflict"):
            continue
        _u = _prof.get("url") or ""
        _cands = [_u] if _prof.get("kind") == "website" else []
        if _prof.get("blog_url"):
            _cands.append(_prof["blog_url"])
        for _cu in _cands:
            _k = (_cu or "").rstrip("/").lower()
            if not _k or _k in _fp_seen or _host_is_unfetchable(_cu):
                continue
            _fp_seen.add(_k)
            try:
                _t, _b, _r = fetch_page_text(_cu, with_raw=True)
                if _r:
                    _absorb_page(_cu, _r, (_t or "") + " " + (_b or ""),
                                 first_party=True,
                                 why="URL on the contact record")
            except Exception as _e:  # noqa: BLE001
                result["tools"].append({
                    "tool_name": "first_party_mine", "invoked_at": _now(),
                    "input_type": "url", "input_value": _cu[:200],
                    "status": "error", "findings_count": 0,
                    "error": str(_e)[:200]})

    # ---- Handle candidates: explicit, then URL slugs, then email, then name.
    handle_candidates = []
    handle_origin = {}

    def _seed(values, origin):
        for v in values:
            v = (v or "").strip()
            if not v or v in handle_origin:
                continue
            handle_candidates.append(v)
            handle_origin[v] = origin

    _seed(list(handles or []), "explicit")
    _seed(handles_from_urls(known_urls), "known_url")
    email_variants = email_handle_variants(email)
    _seed(email_variants, "email")
    if not email_variants:
        # Generic or absent email local — fall back to name combinations. Same
        # corroboration gate applies; these are only extra things to test.
        _seed(name_handle_variants(name, name_given, name_family), "name")

    # A bare first or last name is not an anchor: maigret reports that the handle
    # exists, and a bare name part exists nearly everywhere owned by strangers,
    # so sweeping it manufactures namesakes. Skipping it outright is both safer
    # and cheaper than discounting 127 profiles afterwards. Curated URLs are not
    # affected — expand_known_urls() reads them without maigret.
    _sweepable, _bare = [], []
    for h in handle_candidates:
        if not _handle_ok(h):
            continue
        if _handle_is_bare_name_part(h, name, name_given, name_family):
            _bare.append(h)
        else:
            _sweepable.append(h)
    maigret_handles = _sweepable[:MAX_MAIGRET_HANDLES]
    result["skipped_handles"] = [
        {"handle": h, "reason": "bare name part — sweeping it finds namesakes"}
        for h in _bare]
    if _bare and not maigret_handles:
        result["identity"]["reason"] = (
            "no searchable handle: %s %s only the contact's own name, which "
            "matches strangers on every site"
            % (", ".join(_bare[:3]), "are" if len(_bare) > 1 else "is"))

    # ---- Maigret across each handle candidate; collect claimed profiles.
    all_profiles = {}  # site -> profile (curated wins, then first handle)
    for prof in curated_profiles:
        all_profiles.setdefault(prof["site"], prof)

    for handle in maigret_handles:
        profiles, rec = run_maigret(handle, timeout=maigret_timeout,
                                    top_sites=top_sites)
        result["tools"].append(rec)
        for site, prof in profiles.items():
            prof["site"] = site
            prof["handle"] = handle
            prof["provenance"] = "maigret"
            prof["curated"] = False
            prof["kind"] = "profile"
            # A handle seeded from a known URL does NOT make its maigret hits
            # trustworthy — record where the handle came from and let the name
            # gate below decide, exactly as for any other handle.
            prof["handle_origin"] = handle_origin.get(handle, "explicit")
            # GitHub structured enrichment.
            if site.lower() == "github":
                gh = github_api_fields(handle)
                for k in ("fullname", "org", "location", "blog_url", "bio"):
                    if gh.get(k) and not prof.get(k):
                        prof[k] = gh[k]
            all_profiles.setdefault(site, prof)

    if not maigret_handles:
        result["identity"]["reason"] = "no distinctive handle to anchor on"

    # ---- Corroboration: which profiles agree with the contact's name?
    corroborating = []
    fnc = 0  # full-name (given+family) corroborations
    curated_anchors = []
    for site, prof in all_profiles.items():
        shared, fam = _name_agreement(name, prof.get("fullname", ""))

        # A handle MANUFACTURED from the contact's own name cannot corroborate
        # that name: pivot and check are the same signal, so every namesake
        # passes. Report zero corroboration to consumers (weave_enrich filters
        # on name_shared_tokens / family_present) and keep the raw measurement
        # under *_raw for audit.
        _is_maigret = prof.get("provenance") == "maigret"
        if _is_maigret and prof.get("handle_origin") == "name":
            prof["circular_anchor"] = True
            prof["name_shared_tokens_raw"] = shared
            prof["family_present_raw"] = fam
            prof["corroboration_note"] = (
                "handle derived from the contact's name — name agreement here "
                "is circular, not independent evidence")
            shared, fam = 0, False
        elif (_is_maigret and shared < 2
              and _handle_is_bare_name_part(prof.get("handle", ""), name,
                                            name_given, name_family)):
            # An observed handle was trusted as an independent anchor regardless
            # of how generic it was. A bare surname is shared by thousands, so
            # family-name agreement is the same signal checking itself. Full-name
            # agreement (shared >= 2) is exempt above: the given name is not
            # derivable from a surname handle, so a profile showing both is
            # genuine corroboration.
            prof["circular_anchor"] = True
            prof["name_shared_tokens_raw"] = shared
            prof["family_present_raw"] = fam
            prof["corroboration_note"] = (
                "handle carries no more signal than the surname, so family-name "
                "agreement is not independent evidence; only a profile naming "
                "the contact in full would count")
            shared, fam = 0, False

        # A site that serves the same page for a handle nobody owns cannot
        # attribute an account to this contact or to anyone else. Separately, a
        # well-behaved site may still report that this particular account is gone.
        if _is_maigret and site_answers_for_any_handle(prof.get("url", ""),
                                                       prof.get("handle", "")):
            prof["site_answers_for_any_handle"] = True
            prof.setdefault("name_shared_tokens_raw", shared)
            prof.setdefault("family_present_raw", fam)
            prof["corroboration_note"] = (
                "the site returns an identical page for a handle that cannot "
                "exist, so finding this handle there is not evidence of an account")
            shared, fam = 0, False

        prof["name_shared_tokens"] = shared
        prof["family_present"] = fam

        if prof.get("curated") and prof.get("kind") == "profile":
            # Curated URL whose FETCHED name names someone else: the URL is
            # wrong, so it anchors nothing and sources nothing.
            if prof.get("name_conflict"):
                pass
            else:
                curated_anchors.append(prof)

        # The family name must be one of the shared tokens. Without that, a given
        # name plus a middle initial agreeing was enough to count as a full-name
        # match even when the surnames differed — two shared tokens, two different
        # people.
        if shared >= 2 and fam:
            corroborating.append(prof)
            fnc += 1
        elif fam:
            corroborating.append(prof)
        if prof.get("blog_url") and not prof.get("name_conflict") and not prof.get("circular_anchor"):
            website_candidates.append(
                (prof["blog_url"],
                 "github_blog" if site.lower() == "github" else "profile_blog",
                 prof.get("url", "")))
        result["profiles"].append(prof)

    corr_sites = [p["site"] for p in corroborating]
    curated_sites = [p["site"] for p in curated_anchors]
    # A hand-entered URL whose FETCHED name is the contact's name: the URL and
    # the third-party profile are two independent things that agree, which is
    # real corroboration (unlike the URL existing on its own).
    curated_confirmed = [p for p in curated_anchors
                         if p.get("fullname") and _name_confirms(name, p["fullname"])]

    if fnc >= 2:
        level = "high"
        reason = f"{fnc} sites match full name"
    elif curated_anchors and (fnc >= 1 or curated_confirmed):
        level = "high"
        n_conf = fnc or len(curated_confirmed)
        reason = (f"profile URL on file ({', '.join(curated_sites)}) plus "
                  f"{n_conf} name-corroborated site(s)")
    elif fnc == 1 or len(corroborating) >= 2:
        level = "med"
        reason = (f"{fnc} site(s) match full name, "
                  f"{len(corroborating)} match family name")
    elif curated_anchors and any(_host_is_unfetchable(p.get("url")) for p in curated_anchors):
        # The owner typed this profile URL. Normally a curated URL stays below
        # the write gate until the page is fetched and its name matches -- the
        # URL asserts which ACCOUNT is theirs, not what the page says. But for
        # LinkedIn, Instagram and the rest of the login-walled set that fetch can
        # never succeed, so "unconfirmed" here means "unreadable", not "checked
        # and found wanting". Treating those as equivalent pinned 34 contacts
        # below the gate permanently, discarding the highest-provenance signal in
        # the system: the owner's own assertion.
        #
        # Promoted to 'med' (the write gate) and no further. An owner-entered URL
        # is good evidence that the account is theirs; it is still not two
        # independent sources agreeing, which is what 'high' means.
        level = "med"
        _walled = [p.get("site") for p in curated_anchors
                   if _host_is_unfetchable(p.get("url"))]
        reason = (f"profile URL on file ({', '.join(str(x) for x in _walled)}) "
                  f"that this pipeline cannot fetch; accepted as owner-provided")
    elif len(corroborating) == 1:
        level = "low"
        reason = "1 site matches family name only"
    elif curated_anchors:
        # A hand-entered URL is an assertion about which ACCOUNT belongs to the
        # contact. On its own it verifies nothing about what any third-party
        # profile says, so it stays BELOW the write gate (min_identity='med')
        # rather than promoting the whole result to 'high'. The URL itself is
        # still returned in known_profiles/curated_sites, and google_sync
        # imports the address-book URL into weave directly.
        level = "low"
        reason = (f"profile URL on file ({', '.join(curated_sites)}); "
                  "no independent corroboration")
    else:
        level = "none"
        reason = (result["identity"]["reason"]
                  or "no profile corroborated the contact name")

    result["identity"] = {
        "level": level,
        "corroborating_sites": corr_sites,
        "curated_sites": curated_sites,
        "anchor": "contact_record" if (curated_anchors and fnc < 2) else "name_corroboration",
        "reason": reason,
    }

    # ---- Findings: one per corroborating profile (provenance for identity).
    fid = 1
    for prof in corroborating:
        parts = []
        if prof.get("location"):
            parts.append(f"location={prof['location']}")
        if prof.get("org"):
            parts.append(f"org={prof['org']}")
        quote = prof.get("bio") or prof.get("fullname") or ""
        result["findings"].append({
            "finding_id": f"P{fid:03d}",
            "claim": (f"{prof['site']} profile of handle '{prof['handle']}' "
                      f"names '{prof.get('fullname','?')}'"
                      + (f" ({'; '.join(parts)})" if parts else "")),
            "confidence": "high" if prof.get("name_shared_tokens", 0) >= 2 else "med",
            "source_refs": [{"url": prof["url"], "retrieved_at": _now(),
                             "quote": quote[:300]}],
        })
        fid += 1

    # ---- Name+org search fallback: ONLY when nothing corroborated, and never
    # allowed to raise the identity level. Output is candidate evidence for a
    # human/LLM verification pass, per the 2026-08-14 fail-closed rebuild.
    # ---- Gravatar: the email's own profile. Keyed on md5(email), so a hit
    # belongs to this address by construction. Location and linked accounts are
    # taken; displayName is NOT written as the person's name because it is
    # frequently just a handle.
    grav = gravatar_profile(email) if email else None
    if grav and (grav["location"] or grav["accounts"] or grav["urls"] or grav["bio"]):
        result["profiles"].append({
            "site": "Gravatar", "handle": "", "url": grav["profile_url"] or "",
            "fullname": grav["display_name"], "location": grav["location"],
            "bio": grav["bio"], "blog_url": (grav["urls"] or [""])[0],
            "provenance": "gravatar", "curated": False, "kind": "profile",
            "handle_origin": "email_hash",
        })
        result["findings"].append({
            "finding_id": "GR001",
            "claim": ("Gravatar profile registered to %s%s" % (
                email, (" — location: " + grav["location"]) if grav["location"] else "")),
            "confidence": "high",
            "source_refs": [{"url": grav["profile_url"] or "https://gravatar.com",
                             "retrieved_at": _now(),
                             "quote": (grav["bio"] or grav["location"] or "")[:300]}],
        })
        if grav["location"]:
            result["enrichment"].setdefault("location_city", grav["location"])
            result["enrichment"].setdefault("location_city_source", "gravatar")
            result["enrichment"].setdefault("location_city_confidence", 0.8)
        for u in (grav["accounts"] + grav["urls"]):
            # Gravatar is keyed on md5(the contact's own address), so a URL the
            # profile lists is the contact's own assertion about themselves —
            # first-party, the strongest LinkedIn tie there is.
            if linkedin_slug(u):
                result["linkedin_candidates"].append({
                    "url": u, "context": "", "source": "first_party",
                    "found_on": grav.get("profile_url") or "gravatar",
                    "why": "listed on the gravatar keyed to the contact's email"})
            parsed = parse_profile_url(u)
            if parsed and not any((p.get("url") or "").rstrip("/") == u.rstrip("/")
                                  for p in result["profiles"]):
                result["profiles"].append({
                    "site": parsed["platform"], "handle": parsed["handle"],
                    "url": u, "fullname": "", "location": "", "bio": "",
                    "blog_url": "", "provenance": "gravatar_linked",
                    "curated": False, "kind": parsed["kind"],
                    "handle_origin": "gravatar",
                })
        # An email-anchored profile is real corroboration of the ADDRESS, which
        # is what the contact record actually asserts.
        if level == "none":
            level = "med"
            result["identity"]["level"] = level
            result["identity"]["reason"] = "gravatar profile registered to the contact's email"

    # ---- Email-domain probe: a non-freemail address often IS the person's
    # website ('ana@anaperez.example' -> anaperez.example). The local part
    # can be too short to be a handle while the DOMAIN identifies them exactly,
    # so this runs before falling back to search.
    # Gated on the FIELD it can fill, not on the identity level. The old
    # condition ("only when identity is still weak") optimised for corroborating
    # who someone is; once that succeeded the run stopped, so a contact with a
    # confirmed identity and no phone number never had one looked for. Identity
    # is the admission ticket to WRITING a value, not a reason to stop looking
    # for one.
    if level not in ("high", "med") or _wants("site", "phone", "city", "linkedin"):
        site = email_domain_site(email)
        if site and site.rstrip("/").lower() not in {
                (p.get("url") or "").rstrip("/").lower() for p in result["profiles"]}:
            title, body, _raw = fetch_page_text(site, with_raw=True)
            # A personal domain that stopped resolving is the commonest way a
            # contact's only first-party page disappears. The archived copy
            # still names them, which is exactly what corroboration needs, and
            # costs one unauthenticated API call.
            archived = None
            if not (title or body):
                try:
                    title, body, archived = archived_page_text(site)
                except Exception as _e:  # noqa: BLE001
                    result["tools"].append({
                        "tool_name": "wayback", "invoked_at": _now(),
                        "input_type": "url", "input_value": site,
                        "status": "error", "findings_count": 0,
                        "error": str(_e)[:200]})
            if title or body:
                shared, fam = _name_agreement(name, title + " " + body)
                if shared >= 2:
                    # A domain that no longer answers is not a URL to publish
                    # on the contact record. The archived page still corroborates
                    # WHO they are — which is what this block is for — so the
                    # profile is recorded without a live url, and the address is
                    # kept under source_url for audit only.
                    result["profiles"].append({
                        "site": "Website", "handle": "",
                        "url": "" if archived else site,
                        "fullname": title[:120], "location": "", "bio": "",
                        "blog_url": "" if archived else site,
                        "provenance": ((archived or {}).get("source", "wayback")
                                       if archived else "email_domain"),
                        "curated": False, "kind": "website",
                        "handle_origin": "email_domain",
                        "name_shared_tokens": shared, "family_present": fam,
                        "archived": bool(archived),
                        "archived_at": (archived or {}).get("timestamp", ""),
                        "archived_url": (archived or {}).get("url", ""),
                        "source_url": site,
                    })
                    result["findings"].append({
                        "finding_id": "ED001",
                        "claim": (("Email domain's ARCHIVED site (%s) names the "
                                   "contact: %s" % ((archived or {}).get("timestamp", "?"),
                                                    title or site))
                                  if archived else
                                  f"Email domain resolves to a site naming the contact: {title or site}"),
                        "confidence": "high",
                        "source_refs": [{"url": site, "retrieved_at": _now(),
                                         "quote": title[:300]}],
                    })
                    # A dead domain is not a website to publish on the record;
                    # the archive corroborates who they are, nothing more.
                    if not archived:
                        result["enrichment"].setdefault("website", site)
                        result["enrichment"].setdefault("website_source", site)
                        result["enrichment"].setdefault("website_confidence", 0.9)

                    # The site is confirmed to be theirs, so mine it: the links
                    # a person publishes about themselves are the highest-grade
                    # signal available, better than anything inferred.
                    if not archived:
                        # The domain is the contact's own address domain and the
                        # page names them: first-party by both tests, so the
                        # whole page may be mined.
                        _absorb_page(site, _raw, (title or "") + " " + (body or ""),
                                     first_party=True,
                                     why="the contact's own email domain")
                    mined = (mine_personal_site(site, name,
                                                region_hint=_region_hint)
                             if not archived
                             else {"links": [], "occupation": "", "tagline": "",
                                   "emails": [], "phones": [], "cities": [],
                                   "linkedin": [], "websites": []})
                    for parsed in mined["links"]:
                        if any((p.get("url") or "").rstrip("/") ==
                               parsed["url"].rstrip("/") for p in result["profiles"]):
                            continue
                        result["profiles"].append({
                            "site": parsed["platform"], "handle": parsed["handle"],
                            "url": parsed["url"], "fullname": "", "location": "",
                            "bio": "", "blog_url": "",
                            "provenance": "self_published",
                            "curated": False, "kind": parsed["kind"],
                            "handle_origin": "personal_site",
                        })
                    if mined["links"]:
                        result["findings"].append({
                            "finding_id": "PS001",
                            "claim": ("Contact's own site links %d profile(s): %s"
                                      % (len(mined["links"]),
                                         ", ".join(p["platform"] for p in mined["links"]))),
                            "confidence": "high",
                            "source_refs": [{"url": site, "retrieved_at": _now(),
                                             "quote": title[:300]}],
                        })
                    if mined["occupation"]:
                        result["enrichment"].setdefault("occupation", mined["occupation"])
                        result["enrichment"].setdefault("occupation_source", site)
                        result["enrichment"].setdefault("occupation_confidence", 0.85)
                    if mined["tagline"]:
                        result["enrichment"].setdefault("bio_summary", mined["tagline"])
                        result["enrichment"].setdefault("bio_summary_source", site)
                        result["enrichment"].setdefault("bio_summary_confidence", 0.8)
                    for em in mined["emails"][:2]:
                        if em != (email or "").lower():
                            result["findings"].append({
                                "finding_id": "PS002",
                                "claim": "Additional email published on own site: %s" % em,
                                "confidence": "med",
                                "source_refs": [{"url": site, "retrieved_at": _now(),
                                                 "quote": em}],
                            })
                    level = "med" if level == "none" else level
                    result["identity"]["level"] = level
                    result["identity"]["reason"] = (
                        "email domain is an archived personal site naming the contact"
                        if archived else
                        "email domain is a personal site naming the contact")

    # ---- Domain registration. A vanity domain is the contact's OWN, and its
    # registration is one of the very few sources carrying a second email
    # address and a phone number for someone with no profile anywhere. Most
    # registrations are privacy-proxied; whois_domain reports nothing at all in
    # that case rather than attributing the registrar's details to the person.
    if enable_whois:
        whois_targets = []
        _vanity = email_domain_site(email) if email else None
        if _vanity and not employer_from_email(email, name):
            _h = _host_of(_vanity)
            if _h:
                whois_targets.append(_h)
        for _p in result["profiles"]:
            if _p.get("kind") != "website":
                continue
            _h = _host_of(_p.get("url") or "")
            if _h and _h not in whois_targets and _host_class(_h) == _HOST_RANK_PERSONAL:
                whois_targets.append(_h)
        for _dom in whois_targets[:2]:
            # Its own try/except: a registry that hangs, answers garbage or is
            # simply unreachable must cost this contact nothing but one tool
            # entry saying so.
            try:
                _fields, _rec = whois_domain(_dom)
            except Exception as _e:  # noqa: BLE001
                result["tools"].append({
                    "tool_name": "whois", "invoked_at": _now(),
                    "input_type": "domain", "input_value": _dom,
                    "status": "error", "findings_count": 0,
                    "error": str(_e)[:200]})
                continue
            result["tools"].append(_rec)
            if not _fields:
                continue
            _confirmed = whois_confirms(name, _fields)
            _reg = {
                "domain": _dom,
                "confirms_contact": _confirmed,
                "registrant_name": _fields.get("registrant_name", ""),
                "registrant_org": _fields.get("registrant_org", ""),
                "registrant_email": _fields.get("registrant_email", ""),
                "registrant_phone": _fields.get("registrant_phone", ""),
                "registrant_city": _fields.get("registrant_city", ""),
                "registrar": _fields.get("registrar", ""),
            }
            result["registrations"].append(_reg)
            _n = len(result["registrations"])
            _who = _reg["registrant_name"] or _reg["registrant_org"]
            _f = {
                "finding_id": "WD%03d" % _n,
                "claim": (("Domain %s on the contact's own email address is "
                           "registered to '%s'" % (_dom, _who)) if _confirmed else
                          ("UNVERIFIED CANDIDATE (domain registration names "
                           "someone else): %s is registered to '%s'"
                           % (_dom, _who))),
                "confidence": "high" if _confirmed else "low",
                "source_refs": [{"url": "whois:" + _dom, "retrieved_at": _now(),
                                 "quote": _who[:300]}],
            }
            if not _confirmed:
                _f["unverified"] = True
            result["findings"].append(_f)
            if not _confirmed:
                continue
            # Only a name-confirmed record may source anything: in a proxied or
            # third-party record the phone and address are the registrar's.
            if (_reg["registrant_email"]
                    and _reg["registrant_email"].lower() != (email or "").lower()):
                result["findings"].append({
                    "finding_id": "WD%03dE" % _n,
                    "claim": ("Additional email on the contact's domain "
                              "registration: %s" % _reg["registrant_email"]),
                    "confidence": "med",
                    "source_refs": [{"url": "whois:" + _dom,
                                     "retrieved_at": _now(),
                                     "quote": _reg["registrant_email"]}],
                })
            if _reg["registrant_phone"]:
                result["findings"].append({
                    "finding_id": "WD%03dP" % _n,
                    "claim": ("Phone on the contact's domain registration: %s"
                              % _reg["registrant_phone"]),
                    "confidence": "med",
                    "source_refs": [{"url": "whois:" + _dom,
                                     "retrieved_at": _now(),
                                     "quote": _reg["registrant_phone"]}],
                })
            # The domain came from the contact's own address on file and the
            # registrant name is independent third-party data that agrees with
            # it — the same shape of evidence as a gravatar keyed on the email.
            if level == "none":
                level = "med"
                result["identity"]["level"] = level
                result["identity"]["reason"] = (
                    "the registration of the contact's own email domain names them")
                result["identity"]["anchor"] = "domain_registration"

    # ---- Employer NAME -> company DOMAIN, and then the company's own pages.
    # This is the block that reaches the population the rest of the pipeline
    # cannot: no address, no profile URL, but an employer on file. Everything
    # downstream of it (a first-party team page, a site: filter, address
    # permutation) needs a domain, and the employer name alone is not one.
    # A wrong domain is worse than none, so resolve_company_domain returns
    # nothing rather than an unverified guess.
    _company_domain = (org_domain or "").strip().lower().lstrip("@").rstrip("/")
    if _company_domain:
        result["company"] = {"domain": _company_domain, "method": "caller",
                             "confidence": 0.9, "verified": False,
                             "evidence": "supplied by the caller"}
    elif enable_company_domain and org and (
            level not in ("high", "med") or _wants("email", "phone", "site")):
        try:
            _cdom, _crecs = resolve_company_domain(
                org, peers=peer_emails, searxng_url=searxng_url,
                enable_search=enable_search)
        except Exception as _e:  # noqa: BLE001
            _cdom, _crecs = None, [{
                "tool_name": "company_domain", "invoked_at": _now(),
                "input_type": "org", "input_value": org[:120],
                "status": "error", "findings_count": 0, "error": str(_e)[:200]}]
        result["tools"].extend(_crecs)
        if _cdom:
            result["company"] = _cdom
            _company_domain = _cdom["domain"]
            result["findings"].append({
                "finding_id": "CD001",
                "claim": ("Employer '%s' resolves to the domain %s (%s): %s"
                          % (org, _cdom["domain"], _cdom["method"],
                             _cdom.get("evidence", ""))),
                "confidence": "high" if _cdom["confidence"] >= 0.9 else "med",
                "source_refs": [{"url": "https://" + _cdom["domain"],
                                 "retrieved_at": _now(),
                                 "quote": (_cdom.get("evidence") or "")[:300]}],
            })

    # The employer's own team / about / people page. First-party, not
    # auth-walled, and it is where a job title actually lives. It still has to
    # NAME the contact by the same adjacency standard as any other page — the
    # page listing everyone at the company is not evidence about this one
    # person until their name is on it.
    if enable_company_pages and _company_domain and (
            level not in ("high", "med") or _wants("email", "phone", "city")):
        try:
            _cpage, _precs = mine_company_people_page(
                _company_domain, name, name_given=name_given,
                name_family=name_family, org=org)
        except Exception as _e:  # noqa: BLE001
            _cpage, _precs = None, [{
                "tool_name": "company_people_page", "invoked_at": _now(),
                "input_type": "domain", "input_value": _company_domain,
                "status": "error", "findings_count": 0, "error": str(_e)[:200]}]
        result["tools"].extend(_precs)
        if _cpage:
            result["company_pages"].append(_cpage)
            # Real corroboration, and not circular: the domain came from the
            # employer on the contact record, the name was found on a third
            # party's page. Two people of one name at one small company is the
            # residual risk, and it is the same risk the search tier already
            # accepts for "family name + employer on page".
            result["profiles"].append({
                "site": "CompanyPage", "handle": "", "url": _cpage["url"],
                "fullname": _cpage["title"] or name, "location": "", "bio": "",
                "blog_url": "", "provenance": "company_site", "curated": False,
                "kind": "company_page", "handle_origin": "org_domain",
                "name_shared_tokens": 2, "family_present": True,
                "org_present": True,
            })
            result["findings"].append({
                "finding_id": "CP001",
                "claim": ("Employer's own page names the contact: %s%s"
                          % (_cpage["url"],
                             (" — " + _cpage["occupation"]) if _cpage["occupation"]
                             else "")),
                "confidence": "high",
                "source_refs": [{"url": _cpage["url"], "retrieved_at": _now(),
                                 "quote": (_cpage["occupation"]
                                           or _cpage["title"])[:300]}],
            })
            for _i, _em in enumerate(_cpage["emails"], start=1):
                result["harvested_emails"].append(
                    {"email": _em, "source": "company_page",
                     "source_url": _cpage["url"], "name_confirmed": True})
                result["findings"].append({
                    "finding_id": "CP%03dE" % _i,
                    "claim": ("Address published next to the contact's name on "
                              "the employer's own page: %s" % _em),
                    "confidence": "high",
                    "source_refs": [{"url": _cpage["url"],
                                     "retrieved_at": _now(), "quote": _em}],
                })
            if _cpage["occupation"]:
                result["enrichment"].setdefault("occupation", _cpage["occupation"])
                result["enrichment"].setdefault("occupation_source", _cpage["url"])
                result["enrichment"].setdefault("occupation_confidence", 0.75)
            if level == "none":
                level = "med"
            result["identity"]["level"] = level
            result["identity"]["reason"] = (
                "the employer's own site names the contact")
            result["identity"]["anchor"] = "company_page"
            result["identity"]["corroborating_sites"] = (
                list(result["identity"].get("corroborating_sites") or [])
                + ["CompanyPage"])

    # ---- GitHub commit-author addresses. A GitHub profile carries no address
    # field, but every commit records the one its author configured, so a
    # confirmed account converts into a reachable address. Only accounts that
    # already passed the identity gate are harvested — reading a stranger's
    # commits would attribute a stranger's address.
    if enable_github_emails and ("email" in _missing or not email):
        # Reach an account for a contact who has no email to pivot from. Without
        # this the harvest below had no GitHub profile to read for exactly the
        # population it exists to serve -- see github_user_search.
        # Only an account we could ACTUALLY harvest suppresses the search.
        _have_usable_gh = any(github_profile_is_harvestable(p)
                              for p in result["profiles"])
        if enable_github_user_search and not email and not _have_usable_gh:
            try:
                _ghu, _ghrec = github_user_search(
                    name, org=org, location_city=location_city)
            except Exception as _e:  # noqa: BLE001
                _ghu, _ghrec = [], {
                    "tool_name": "github_user_search", "invoked_at": _now(),
                    "input_type": "name", "input_value": name[:120],
                    "status": "error", "findings_count": 0,
                    "error": str(_e)[:200]}
            result["tools"].append(_ghrec)
            for _u in _ghu:
                # name_shared_tokens/family_present are set because this account
                # passed _name_confirms on its OWN profile name AND agreed with
                # the employer or city on the contact record -- two independent
                # facts, which is the same bar a corroborating profile clears.
                result["profiles"].append({
                    "site": "GitHub", "handle": _u["handle"],
                    "url": "https://github.com/" + _u["handle"],
                    "fullname": _u["fullname"], "location": _u["location"],
                    "bio": _u["bio"], "blog_url": _u["blog_url"],
                    "org": _u["company"], "provenance": "github_user_search",
                    "curated": False, "kind": "profile",
                    "handle_origin": "github_search",
                    "name_shared_tokens": 2, "family_present": True,
                })
                result["findings"].append({
                    "finding_id": "GS%03d" % (len(result["findings"]) + 1),
                    "claim": ("GitHub account '%s' names the contact and %s"
                              % (_u["handle"], _u["why"])),
                    "confidence": "high",
                    "source_refs": [
                        {"url": "https://github.com/" + _u["handle"],
                         "retrieved_at": _now(),
                         "quote": (_u["fullname"] + " | " + _u["company"]
                                   + " | " + _u["location"])[:300]}],
                })
                if level == "none":
                    level = "med"
                    result["identity"]["level"] = level
                    result["identity"]["reason"] = (
                        "a GitHub account naming the contact agrees with the "
                        "employer or city on their record")
        _gh_seen = set()
        for _prof in list(result["profiles"]):
            if not github_profile_is_harvestable(_prof):
                continue
            _h = (_prof.get("handle") or "").strip()
            if _h.lower() in _gh_seen:
                continue
            _gh_seen.add(_h.lower())
            try:
                _emails, _grec = github_commit_emails(_h)
            except Exception as _e:  # noqa: BLE001
                _emails, _grec = [], {
                    "tool_name": "github_commit_emails", "invoked_at": _now(),
                    "input_type": "handle", "input_value": _h,
                    "status": "error", "findings_count": 0,
                    "error": str(_e)[:200]}
            result["tools"].append(_grec)
            for _i, _hit in enumerate(_emails, start=1):
                _confirmed = _name_confirms(name, _hit.get("author_name", ""))
                result["harvested_emails"].append({
                    "email": _hit["email"], "source": "github_commits",
                    "source_url": _prof.get("url", ""),
                    "author_name": _hit.get("author_name", ""),
                    "name_confirmed": _confirmed,
                })
                result["email_candidates"].append(
                    {"email": _hit["email"], "sites": ["github"],
                     "source": "github_commits", "verified": _confirmed})
                result["findings"].append({
                    "finding_id": "GE%03d" % len(result["harvested_emails"]),
                    "claim": (("Address this contact's GitHub account authors "
                               "commits from (commit author '%s'): %s"
                               % (_hit.get("author_name", ""), _hit["email"]))
                              if _confirmed else
                              ("UNVERIFIED CANDIDATE (address on a commit "
                               "authored through the contact's GitHub account, "
                               "but the commit names '%s'): %s"
                               % (_hit.get("author_name", "?"), _hit["email"]))),
                    "confidence": "high" if _confirmed else "low",
                    "unverified": not _confirmed,
                    "source_refs": [{"url": _prof.get("url", "")
                                     or ("https://github.com/" + _h),
                                     "retrieved_at": _now(),
                                     "quote": _hit["email"]}],
                })
                if _confirmed:
                    result["enrichment"].setdefault("email", _hit["email"])
                    result["enrichment"].setdefault(
                        "email_source", _prof.get("url", "") or "github_commits")
                    result["enrichment"].setdefault("email_confidence", 0.85)

    # ---- Corporate email permutation. For a contact reachable only at an
    # employer's domain, the standard address shapes are the cheapest way to
    # find a mailbox that is actually registered somewhere. CANDIDATES ONLY:
    # holehe proves an address exists, never whose it is, so these never raise
    # the identity level and never source a field.
    # Measured negative, kept only for the population it was built for: a prior
    # pass found address permutation worth 1 hit in 35 probes. It never sources
    # a field, so it now runs ONLY when the email is the missing field.
    if enable_email_permutation and "email" in _missing and level not in ("high", "med"):
        _emp_dom = ""
        if email and "@" in email and employer_from_email(email, name):
            _emp_dom = email.split("@", 1)[1].strip().lower()
        elif _company_domain and result["company"].get("confidence", 0) >= 0.85:
            # Previously unreachable by construction: this probe needed a
            # CORPORATE ADDRESS to learn the domain, so it could only ever run
            # for contacts who already had one — never for the contacts with no
            # address at all, who are the ones it was meant to help. A resolved
            # employer domain is that missing input. Only a high-confidence
            # domain is used: permuting names at a wrongly-resolved company
            # invents addresses at a company the contact has no connection to.
            _emp_dom = _company_domain
        if _emp_dom:
            try:
                _found, _recs = probe_email_permutations(
                    name, _emp_dom, known_email=email, name_given=name_given,
                    name_family=name_family, limit=email_permutation_limit)
            except Exception as _e:  # noqa: BLE001
                _found, _recs = [], [{
                    "tool_name": "holehe", "invoked_at": _now(),
                    "input_type": "email_permutation", "input_value": _emp_dom,
                    "status": "error", "findings_count": 0,
                    "error": str(_e)[:200]}]
            result["tools"].extend(_recs)
            for _i, _hit in enumerate(_found, start=1):
                result["email_candidates"].append(_hit)
                result["findings"].append({
                    "finding_id": "EP%03d" % _i,
                    "claim": ("UNVERIFIED CANDIDATE (an address shape for this "
                              "name at the employer domain is registered on %s): %s"
                              % (", ".join(_hit["sites"][:6]), _hit["email"])),
                    "confidence": "low",
                    "unverified": True,
                    "source_refs": [{"url": "holehe:" + _hit["email"],
                                     "retrieved_at": _now(),
                                     "quote": ", ".join(_hit["sites"])[:300]}],
                })

    if enable_search and (level not in ("high", "med") or _missing):
        queries = build_search_queries(name, name_given, name_family, org,
                                       occupation, location_city,
                                       email=email, phone=phone,
                                       missing_fields=result_missing
                                       )[:max_search_queries]
        # The site: tier reached only LinkedIn and GitHub. These are the other
        # places a person with no address is actually indexed, and each one is
        # chosen from what the contact record already says rather than swept for
        # everybody — an academic gets ORCID, a designer gets the portfolio
        # sites, and anyone with a resolved employer domain gets that domain.
        _cand_cap, _verify_cap = MAX_SEARCH_CANDIDATES, MAX_SEARCH_VERIFY
        if enable_targeted_site_search:
            _targeted = build_targeted_site_queries(
                name, org=org, occupation=occupation,
                org_domain=(result["company"].get("domain") or ""))
            _extra = [q for q in _targeted if q not in queries]
            if _extra:
                queries = queries + _extra
                _cand_cap += 2 * len(_extra)
                _verify_cap += len(_extra)
        seen_urls = {p.get("url", "").rstrip("/").lower() for p in result["profiles"]}
        cid = 1
        for q in queries:
            if len(result["search_candidates"]) >= _cand_cap:
                break
            rec = {"tool_name": "searxng", "invoked_at": _now(),
                   "input_type": "query", "input_value": q,
                   "status": "success", "findings_count": 0, "error": None}
            try:
                hits = searxng_search(q, limit=10, searxng_url=searxng_url)
            except Exception as e:  # noqa: BLE001
                hits = []
                rec["status"] = "error"
                rec["error"] = str(e)[:200]
            for h in hits:
                u = (h.get("url") or "").strip()
                if not u or u.rstrip("/").lower() in seen_urls:
                    continue
                seen_urls.add(u.rstrip("/").lower())
                parsed = parse_profile_url(u)
                # LinkedIn answers HTTP 999 to any server-side fetch, so the
                # verification loop below can never open one of these pages.
                # The search result's OWN title and snippet are the only text
                # about that profile this pipeline will ever see, so they are
                # captured here and handed to linkedin_tie(). Control-tested:
                # the same queries with fabricated names against real employers
                # returned zero results, so this text is the indexed page's, not
                # the engine echoing the query back.
                if linkedin_slug(u):
                    result["linkedin_candidates"].append({
                        "url": u,
                        "context": ((h.get("title") or "") + " "
                                    + (h.get("content") or "")),
                        "source": "search", "found_on": q, "why": "search result"})
                result["search_candidates"].append({
                    "candidate_id": f"SC{cid:03d}",
                    "query": q,
                    "url": u,
                    "title": h.get("title", ""),
                    "snippet": (h.get("content") or "")[:300],
                    "platform": parsed["platform"] if parsed else "Website",
                    "status": "unverified_candidate",
                    "verified": False,
                })
                cid += 1
                if len(result["search_candidates"]) >= _cand_cap:
                    break
            rec["findings_count"] = len(hits)
            result["tools"].append(rec)

        # VERIFY the candidates instead of discarding them. Collecting URLs and
        # never opening them is why contacts with no email but a known employer
        # ("someone at Netflix") failed: the search found them and the result
        # was thrown away. Fetching is cheap and the bar is unchanged — a
        # candidate is promoted only if the PAGE ITSELF names the contact, the
        # same corroboration standard applied to every other profile.
        verified_n = 0
        for cand in result["search_candidates"][:_verify_cap]:
            title, body, _craw = fetch_page_text(cand["url"], with_raw=True)
            if not (title or body):
                continue
            hay = (title + " " + body)
            shared, fam = _name_agreement(name, hay)
            org_ok = bool(org) and org.strip().lower() in hay.lower()
            # Token overlap across a whole page promoted pages that merely contain
            # a <Given> and a <Family> belonging to two different people. Require
            # the name to appear as a name.
            named = _name_phrase_in_text(name, hay, name_given, name_family)
            if not named and not (fam and org_ok):
                continue   # page does not name the contact -> stays unverified
            cand["status"] = "verified_candidate"
            cand["verified"] = True
            cand["verified_by"] = ("full name on page" if named
                                   else "family name + employer on page")
            # A page whose DOMAIN carries the contact's name is theirs, not just
            # about them; anything else is mined only next to their name.
            _clabel = re.sub(r"[^a-z]", "",
                             _registrable_label(_host_of(cand["url"])) or "")
            _nflat = re.sub(r"[^a-z]", "", fold_accents(name).lower())
            _own = bool(_clabel) and bool(_nflat) and (
                _clabel in _nflat or _nflat in _clabel)
            _absorb_page(cand["url"], _craw, hay, first_party=_own,
                         name_confirmed=True,
                         why=("domain carries the contact's name" if _own
                              else "page names the contact"))
            # Only an adjacency match counts as a full-name corroboration, since
            # that is what the level calculation reads.
            shared = 2 if named else min(shared, 1)
            parsed = parse_profile_url(cand["url"])
            result["profiles"].append({
                "site": (parsed["platform"] if parsed else "Website"),
                "handle": (parsed["handle"] if parsed else ""),
                "url": cand["url"],
                "fullname": title[:120],
                "location": "",
                "bio": "",
                "blog_url": "",
                "provenance": "name_search",
                "curated": False,
                "kind": (parsed["kind"] if parsed else "website"),
                "handle_origin": "search",
                "name_shared_tokens": shared,
                "family_present": fam,
                "org_present": org_ok,
            })
            verified_n += 1

        for cand in result["search_candidates"]:
            if cand.get("verified"):
                result["findings"].append({
                    "finding_id": cand["candidate_id"],
                    "claim": (f"Search result names the contact ({cand['verified_by']}): "
                              f"{cand['title'] or cand['url']}"),
                    "confidence": "med",
                    "source_refs": [{"url": cand["url"], "retrieved_at": _now(),
                                     "quote": (cand["title"] or cand["snippet"])[:300]}],
                })
            else:
                result["findings"].append({
                    "finding_id": cand["candidate_id"],
                    "claim": ("UNVERIFIED CANDIDATE (web search, name not "
                              f"corroborated): {cand['title'] or cand['url']}"),
                    "confidence": "low",
                    "unverified": True,
                    "source_refs": [{"url": cand["url"], "retrieved_at": _now(),
                                     "quote": cand["snippet"]}],
                })

        # Re-derive identity now that search may have produced corroboration.
        if verified_n:
            _sp = [p for p in result["profiles"]
                   if p.get("provenance") == "name_search" and p.get("verified") is not False]
            _full = sum(1 for p in _sp if p.get("name_shared_tokens", 0) >= 2)
            if _full >= 2:
                level, reason = "high", f"{_full} search result(s) name the contact"
            elif _full == 1 or any(p.get("family_present") and p.get("org_present")
                                   for p in _sp):
                level, reason = "med", (f"{verified_n} search result(s) corroborate "
                                        "the contact by name" +
                                        (" and employer" if org else ""))
            result["identity"]["level"] = level
            result["identity"]["reason"] = reason
            # corroborating_sites was left at its pre-search value, so a caller
            # could see level "high" next to an empty evidence list.
            _search_sites = [p.get("site") or "Website" for p in _sp
                             if p.get("name_shared_tokens", 0) >= 2
                             or (p.get("family_present") and p.get("org_present"))]
            if _search_sites:
                result["identity"]["corroborating_sites"] = (
                    list(result["identity"].get("corroborating_sites") or [])
                    + _search_sites)
        if result["search_candidates"]:
            result["identity"]["reason"] = (
                "%s; %d unverified search candidate(s) returned — NOT promoted"
                % (result["identity"].get("reason") or reason,
                   len(result["search_candidates"])))

    # ---- Enrichment fields — ONLY from corroborated or hand-entered profiles.
    if level in ("high", "med"):
        enr = {}
        conf = 0.75 if level == "high" else 0.6
        # Verified social presence IS enrichment — a confirmed identity with no
        # employer still yields the person's real profiles. Do not discard them.
        social = {}
        sourced = list(curated_anchors) + [p for p in corroborating
                                           if p not in curated_anchors]
        for prof in sourced:
            site = prof["site"]
            # Per-PROFILE confidence, not the result-wide level: a family-name-
            # only match must not inherit 'high' just because some other source
            # (or a hand-entered URL) lifted the overall level.
            if prof.get("curated"):
                pconf = 0.8
            elif prof.get("name_shared_tokens", 0) >= 2:
                pconf = conf
            else:
                pconf = min(conf, 0.6)
            if prof.get("url") and site not in social:
                social[site] = prof["url"]
            if prof.get("org") and "org" not in enr:
                enr["org"] = prof["org"]
                enr["org_source"] = prof["url"]
                enr["org_confidence"] = pconf
            if prof.get("location") and "location_city" not in enr:
                enr["location_city"] = prof["location"]
                enr["location_city_source"] = prof["url"]
                enr["location_city_confidence"] = pconf
            if "pronouns" not in enr and prof.get("bio"):
                m = _PRONOUN_RE.search(prof["bio"])
                if m:
                    enr["pronouns"] = m.group(1).lower()
                    enr["pronouns_source"] = prof["url"]
                    enr["pronouns_confidence"] = 0.85

        # Website: RANKED, not first-wins. personal domain > github blog >
        # professional profile > portfolio > consumer social.
        cands = list(website_candidates)
        for prof in sourced:
            # Only a real site counts as a website candidate. A profile page
            # (LinkedIn, GitHub, Snapchat...) belongs in social_profiles; the
            # `website` predicate must not be filled with one.
            if prof.get("url") and prof.get("kind") == "website":
                cands.append((prof["url"], "curated" if prof.get("curated")
                              else "profile_url", prof["url"]))
        best = pick_website(cands)
        if best and _host_class(_host_of(best[0])) in (
                _HOST_RANK_PERSONAL, _HOST_RANK_PORTFOLIO):
            enr["website"] = best[0]
            enr["website_source"] = best[2] or best[0]
            enr["website_confidence"] = (
                0.8 if best[1] in ("curated", "github_blog") else conf)

        if social:
            enr["social_profiles"] = social
            enr["social_profiles_confidence"] = conf
        # MERGE, never replace: the gravatar and email-domain probes above
        # already recorded findings (location, website) that this block does
        # not re-derive. Assigning the dict outright silently dropped them.
        for _k, _v in enr.items():
            result["enrichment"][_k] = _v

    # ---- LinkedIn: decide, once, across everything seen for this contact ----
    # Every LinkedIn URL noticed anywhere above arrived here as a candidate. A
    # URL is NOT evidence on its own -- the slug may be an opaque member id, and
    # a name-shaped slug for a common name belongs to thousands of people, which
    # is the namesake failure this pipeline has already suffered. LinkedIn also
    # answers HTTP 999 to any server-side fetch, so the page can never be read
    # to check. resolve_linkedin_candidates() therefore demands an INDEPENDENT
    # tie and refuses outright when two different profiles both look tied.
    try:
        _li, _li_rej = resolve_linkedin_candidates(
            result["linkedin_candidates"], name, name_given=name_given,
            name_family=name_family, org=org, location_city=location_city)
    except Exception as _e:  # noqa: BLE001
        _li, _li_rej = None, []
        result["tools"].append({
            "tool_name": "linkedin_resolve", "invoked_at": _now(),
            "input_type": "name", "input_value": name[:120],
            "status": "error", "findings_count": 0, "error": str(_e)[:200]})
    result["linkedin_rejected"] = _li_rej
    if _li:
        result["linkedin"] = _li
        # JUSTIFICATION for reaching the write gate. The independent evidence is
        # named per tie:
        #   first_party  the contact published the URL on a page already proven
        #                theirs (their own site, or the gravatar keyed on their
        #                own address). Same grade as a hand-entered URL.
        #   context      the indexed page text names the contact by adjacency
        #                AND names their employer or city -- two facts from the
        #                contact record confirmed by a source that is not the
        #                slug. Control-tested against fabricated names.
        #   slug         no independent tie; accepted only for a slug carrying a
        #                full name that is rare on public frequency data, and
        #                only when nothing else competed for this contact.
        _tie_conf = {"first_party": 0.9, "context": 0.75, "slug": 0.6}
        _independent = _li["tie"] in ("first_party", "context")
        _writeable = _independent or (
            _li["tie"] == "slug" and LINKEDIN_ACCEPT_SLUG_ONLY)
        result["profiles"].append({
            "site": "LinkedIn", "handle": _li["slug"], "url": _li["url"],
            "fullname": "", "location": "", "bio": "", "blog_url": "",
            "provenance": "linkedin_" + _li["tie"], "curated": False,
            "kind": "profile", "handle_origin": _li.get("source", ""),
            "linkedin_tie": _li["tie"], "linkedin_tie_reason": _li["reason"],
            # A LinkedIn page cannot be fetched, so these do not record a name
            # read off the profile; they record that an INDEPENDENT tie was
            # established, which is what the consumer's gate is asking about.
            "name_shared_tokens": 2 if _independent else 0,
            "family_present": bool(_independent),
        })
        result["findings"].append({
            "finding_id": "LI001",
            "claim": ("LinkedIn profile tied to the contact (%s): %s — %s"
                      % (_li["tie"], _li["url"], _li["reason"])),
            "confidence": "high" if _li["tie"] == "first_party" else "med",
            "source_refs": [{"url": _li["url"], "retrieved_at": _now(),
                             "quote": _li["reason"][:300]}],
        })
        if _writeable and level in ("high", "med"):
            result["enrichment"]["linkedin_url"] = _li["url"]
            result["enrichment"]["linkedin_url_source"] = _li.get("found_on") or _li["url"]
            result["enrichment"]["linkedin_url_confidence"] = _tie_conf[_li["tie"]]
            # Which tie carried it, so the consumer can tell a profile
            # corroborated by something outside the slug from one resting
            # on the slug alone. They are not the same grade of evidence
            # and must not be stored as though they were.
            result["enrichment"]["linkedin_tie"] = _li["tie"]
    for _r in _li_rej[:6]:
        result["findings"].append({
            "finding_id": "LIX%03d" % (len(result["findings"]) + 1),
            "claim": ("UNVERIFIED CANDIDATE (LinkedIn URL not tied to the "
                      "contact): %s — %s" % (_r["url"], _r["reason"])),
            "confidence": "low", "unverified": True,
            "source_refs": [{"url": _r["url"], "retrieved_at": _now(),
                             "quote": _r["reason"][:300]}],
        })

    # ---- Mined field values -> enrichment ----------------------------------
    # Same invariant as every other sourced field: nothing is promoted unless
    # the contact's identity is corroborated. Within that, the value is chosen
    # by HOW it was found, and two different values found the same way are a
    # collision, so neither is taken -- the cheapest namesake detector there is.
    def _pick(hits, key):
        return pick_mined_value(hits, key)

    if level in ("high", "med"):
        if "phone" in _missing and not phone:
            _p = _pick(result["mined"]["phones"], "phone")
            # A number read out of prose next to a name is the weakest form here
            # and is left as a candidate: on a shared page it may be a
            # colleague's. Only an explicit telephone assertion is promoted.
            if _p and _p["rank"] <= 2:
                result["enrichment"].setdefault("phone", _p["value"])
                result["enrichment"].setdefault(
                    "phone_source", _p["source_url"] or "scout_page_mining")
                result["enrichment"].setdefault(
                    "phone_confidence", 0.85 if _p["rank"] == 0 else 0.7)
                result["findings"].append({
                    "finding_id": "MP001",
                    "claim": ("Phone number published on a page confirmed to be "
                              "the contact's (%s): %s" % (_p["how"], _p["value"])),
                    "confidence": "high" if _p["rank"] == 0 else "med",
                    "source_refs": [{"url": _p["source_url"],
                                     "retrieved_at": _now(),
                                     "quote": _p["value"]}],
                })
        if "email" in _missing and not email:
            _e = _pick(result["mined"]["emails"], "email")
            if _e:
                _local = _e["value"].split("@")[0]
                _name_toks = {t for t in normalize_name(name).split() if len(t) > 2}
                _localish = bool(_name_toks & set(
                    t for t in re.split(r"[^a-z]+", _local) if t))
                # A mailto: on the contact's own page is the page saying "write
                # to me here". Anything weaker has to look like THEIR address,
                # not just an address that happens to sit on the page.
                if _e["rank"] == 0 or _localish:
                    result["enrichment"].setdefault("email", _e["value"])
                    result["enrichment"].setdefault(
                        "email_source", _e["source_url"] or "scout_page_mining")
                    result["enrichment"].setdefault("email_confidence", 0.8)
                    result["findings"].append({
                        "finding_id": "ME001",
                        "claim": ("Address published on a page confirmed to be "
                                  "the contact's (%s): %s"
                                  % (_e["how"], _e["value"])),
                        "confidence": "med",
                        "source_refs": [{"url": _e["source_url"],
                                         "retrieved_at": _now(),
                                         "quote": _e["value"]}],
                    })
        if "city" in _missing and not location_city:
            _c = _pick(result["mined"]["cities"], "city")
            if _c and _c["rank"] <= 2:
                result["enrichment"].setdefault("location_city", _c["value"])
                result["enrichment"].setdefault(
                    "location_city_source", _c["source_url"] or "scout_page_mining")
                result["enrichment"].setdefault("location_city_confidence", 0.7)
        if "site" in _missing:
            for _w in result["mined"]["websites"]:
                _u = _w.get("website") or ""
                if _u and _host_class(_host_of(_u)) == _HOST_RANK_PERSONAL:
                    result["enrichment"].setdefault("website", _u)
                    result["enrichment"].setdefault(
                        "website_source", _w.get("source_url") or _u)
                    result["enrichment"].setdefault("website_confidence", 0.75)
                    break

    return result


def main():
    ap = argparse.ArgumentParser(description="Scout person research (Tier 1)")
    ap.add_argument("--name", required=True)
    ap.add_argument("--email", default="")
    ap.add_argument("--employer", default="")
    ap.add_argument("--org", default="", help="employer/org from the contact record")
    ap.add_argument("--occupation", default="")
    ap.add_argument("--location-city", default="")
    ap.add_argument("--name-given", default="")
    ap.add_argument("--name-family", default="")
    ap.add_argument("--phone", default="")
    ap.add_argument("--handles", default="", help="comma-separated known handles")
    ap.add_argument("--url", action="append", default=[],
                    help="known profile/website URL (repeatable)")
    ap.add_argument("--urls", default="", help="comma-separated known URLs")
    ap.add_argument("--no-search", action="store_true",
                    help="disable the SearXNG name+org fallback")
    ap.add_argument("--no-whois", action="store_true",
                    help="disable the domain-registration lookup")
    ap.add_argument("--no-email-permutation", action="store_true",
                    help="disable holehe probing of employer address shapes")
    ap.add_argument("--org-domain", default="",
                    help="the employer's domain, when the caller already knows it")
    ap.add_argument("--no-company-domain", action="store_true",
                    help="do not resolve the employer name to a domain")
    ap.add_argument("--no-company-pages", action="store_true",
                    help="do not look for the contact on the employer's site")
    ap.add_argument("--no-github-emails", action="store_true",
                    help="do not read commit-author addresses from GitHub")
    ap.add_argument("--no-targeted-sites", action="store_true",
                    help="do not add the per-contact site: queries")
    ap.add_argument("--no-user-scanner", action="store_true",
                    help="use holehe alone for account existence")
    ap.add_argument("--missing", default="",
                    help="comma-separated subset of %s that this contact still "
                         "lacks; queries and techniques are aimed at these. "
                         "Empty means 'assume all five are missing'."
                         % ",".join(TARGET_FIELDS))
    ap.add_argument("--no-github-user-search", action="store_true",
                    help="do not look the contact up in GitHub's user search")
    ap.add_argument("--top-sites", type=int, default=300)
    ap.add_argument("--maigret-timeout", type=int, default=200)
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    a = ap.parse_args()

    urls = list(a.url) + [u.strip() for u in a.urls.split(",") if u.strip()]

    res = research_person(
        a.name, a.email, a.employer,
        handles=[h.strip() for h in a.handles.split(",") if h.strip()],
        phone=a.phone,
        maigret_timeout=a.maigret_timeout, top_sites=a.top_sites,
        org=a.org, occupation=a.occupation, location_city=a.location_city,
        known_urls=urls, name_given=a.name_given, name_family=a.name_family,
        enable_search=not a.no_search,
        enable_whois=not a.no_whois,
        enable_email_permutation=not a.no_email_permutation,
        org_domain=a.org_domain,
        enable_company_domain=not a.no_company_domain,
        enable_company_pages=not a.no_company_pages,
        enable_github_emails=not a.no_github_emails,
        enable_targeted_site_search=not a.no_targeted_sites,
        enable_user_scanner=not a.no_user_scanner,
        enable_github_user_search=not a.no_github_user_search,
        missing_fields=([f.strip() for f in a.missing.split(",") if f.strip()]
                        or None),
    )
    if a.json:
        print(json.dumps(res))
        return 0
    idn = res["identity"]
    print(f"# {a.name}  <{a.email or 'no email'}>")
    print(f"identity: {idn['level']}  ({idn['reason']})")
    print(f"anchor: {idn.get('anchor', '-')}")
    print(f"corroborating sites: {', '.join(idn['corroborating_sites']) or 'none'}")
    print(f"contact-record URLs: {', '.join(idn.get('curated_sites') or []) or 'none'}")
    if res["enrichment"]:
        print("enrichment:")
        for k, v in res["enrichment"].items():
            if k.endswith(("_source", "_confidence")):
                continue
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    print(f"    {kk}: {vv}")
            else:
                print(f"  {k} = {v}")
    if res.get("company", {}).get("domain"):
        _c = res["company"]
        print("employer domain: %s (%s, confidence %s) %s" % (
            _c["domain"], _c.get("method", "?"), _c.get("confidence", "?"),
            _c.get("evidence", "")[:80]))
    for _cp in res.get("company_pages", []):
        print("employer page naming the contact: %s%s" % (
            _cp["url"], ("  [%s]" % _cp["occupation"]) if _cp.get("occupation") else ""))
    for _he in res.get("harvested_emails", []):
        print("harvested email: %s (%s)%s" % (
            _he["email"], _he["source"],
            "" if _he.get("name_confirmed") else "  UNVERIFIED"))
    for reg in res.get("registrations", []):
        print("domain registration: %s -> %s%s" % (
            reg["domain"], reg["registrant_name"] or reg["registrant_org"] or "?",
            "  [CONFIRMS CONTACT]" if reg["confirms_contact"] else "  (other party)"))
    for cand in res.get("email_candidates", []):
        print("email candidate: %s (registered on %s)" % (
            cand["email"], ", ".join(cand["sites"][:5])))
    if res.get("linkedin"):
        _l = res["linkedin"]
        print("linkedin: %s  [tie=%s] %s" % (_l["url"], _l["tie"], _l["reason"]))
    elif res.get("linkedin_candidates"):
        print("linkedin: none accepted from %d candidate(s)"
              % len(res["linkedin_candidates"]))
    _m = res.get("mined") or {}
    for _k in ("phones", "emails", "cities", "websites"):
        for _hit in (_m.get(_k) or [])[:4]:
            print("mined %s: %s" % (_k[:-1], _hit))
    if res.get("phone_intel"):
        _pi = res["phone_intel"]
        print("phone: %s %s %s %s" % (_pi.get("region_code", ""),
                                      _pi.get("line_type", ""),
                                      _pi.get("carrier", ""), _pi.get("geo", "")))
    if res["search_candidates"]:
        print(f"unverified search candidates ({len(res['search_candidates'])}):")
        for c in res["search_candidates"]:
            print(f"  [{c['candidate_id']}] {c['platform']}: {c['url']}")
    print(f"findings: {len(res['findings'])}; profiles: {len(res['profiles'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
