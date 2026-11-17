#!/usr/bin/env python3
"""Render a canonical profile.yaml to Markdown / .docx / PDF (via LaTeX).

Usage:
  python render_cv.py PROFILE.yaml --format md|docx|pdf --out OUTPATH

Three things this renderer is opinionated about, because they materially affect
how a CV reads:

1. Links show a friendly label ("Google Scholar", "GitHub"), never a raw URL.
   A naked `scholar.google.com/citations?user=AbC123` is noise to a human eye;
   the label carries the meaning and the URL rides underneath as the hyperlink
   target (and stays recoverable in the Markdown source / docx relationship for
   any ATS that strips links). See `link_label`.

2. Section order adapts to the candidate. A PhD/researcher or current student
   leads with Education (their primary credential); everyone else leads with
   Experience. `meta.section_order` overrides the heuristic entirely. See
   `section_order`.

3. A PDF always leaves its `.tex` source next to it, so the candidate can hand-
   tune typography or recompile later without rerunning this tool.
"""
import argparse
import datetime
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata


# journal.py owns load_yaml — the one reader that turns an unparseable, wrongly
# shaped or unreadable input into a single comprehensible failure instead of a
# traceback. Imported here even though a renderer writes no receipt: one dialect for
# "this file is not usable" across the whole skill is the point of having one reader.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal  # noqa: E402
from docx_content import DocxMarkupError, save_clean_docx  # noqa: E402
from host_execution import HOST_EXECUTION_REQUIRED, tectonic_needs_host_execution  # noqa: E402


# ── i18n headings ────────────────────────────────────────────────────────────

HEADINGS = {
    "en": {
        "internships": "Internships",
        "summary":        "Summary",
        "experience":     "Experience",
        "education":      "Education",
        "skills":         "Skills",
        "projects":       "Projects",
        "publications":   "Publications",
        "awards":         "Awards",
        "certifications": "Certifications",
        "achievements":   "Selected Achievements",
        "board":          "Board & Advisory",
        "volunteer":      "Volunteer",
    },
    "nl": {
        "internships": "Stages",
        "summary":        "Samenvatting",
        "experience":     "Werkervaring",
        "education":      "Opleiding",
        "skills":         "Vaardigheden",
        "projects":       "Projecten",
        "publications":   "Publicaties",
        "awards":         "Prijzen",
        "certifications": "Certificeringen",
        "volunteer":      "Vrijwilligerswerk",
    },
    "de": {
        "internships": "Praktika",
        "summary": "Profil", "experience": "Berufserfahrung", "education": "Ausbildung",
        "skills": "Kenntnisse", "projects": "Projekte", "publications": "Publikationen",
        "awards": "Auszeichnungen", "certifications": "Zertifizierungen", "volunteer": "Ehrenamt",
    },
    "fr": {
        "internships": "Stages",
        "summary": "Profil", "experience": "Expérience professionnelle", "education": "Formation",
        "skills": "Compétences", "projects": "Projets", "publications": "Publications",
        "awards": "Distinctions", "certifications": "Certifications", "volunteer": "Bénévolat",
    },
    "es": {
        "internships": "Prácticas",
        "summary": "Perfil", "experience": "Experiencia profesional", "education": "Formación",
        "skills": "Competencias", "projects": "Proyectos", "publications": "Publicaciones",
        "awards": "Premios", "certifications": "Certificaciones", "volunteer": "Voluntariado",
    },
    "it": {
        "internships": "Tirocini",
        "summary": "Profilo", "experience": "Esperienza professionale", "education": "Formazione",
        "skills": "Competenze", "projects": "Progetti", "publications": "Pubblicazioni",
        "awards": "Riconoscimenti", "certifications": "Certificazioni", "volunteer": "Volontariato",
    },
    "zh": {
        "internships": "实习经历",
        "summary": "个人简介", "experience": "工作经历", "education": "教育背景",
        "skills": "专业技能", "projects": "项目经历", "publications": "论文发表",
        "awards": "获奖经历", "certifications": "证书", "volunteer": "志愿服务",
        "achievements": "主要成就", "board": "董事会与顾问",
    },
    "ja": {
        "internships": "インターンシップ",
        "summary": "概要", "experience": "職務経歴", "education": "学歴",
        "skills": "スキル", "projects": "プロジェクト", "publications": "論文",
        "awards": "受賞歴", "certifications": "資格", "volunteer": "ボランティア",
        "achievements": "主な実績", "board": "役員・顧問",
    },
    "ko": {
        "internships": "인턴 경력",
        "summary": "소개", "experience": "경력", "education": "학력",
        "skills": "기술", "projects": "프로젝트", "publications": "출판물",
        "awards": "수상 경력", "certifications": "자격증", "volunteer": "봉사활동",
        "achievements": "주요 성과", "board": "이사회 및 자문",
    },
}


# One warning per (profile, language). Same reason as _MARKET_WARNED below: an
# md + docx + pdf run renders from one profile object three times, and the
# identical line printed three times is how a warning gets trained away.
_HEADING_WARNED = []


def _warn_once(seen, key, message):
    if key in seen:
        return
    seen.append(key)
    print(message, file=sys.stderr)


def headings(profile):
    """Section labels for the profile's language (default 'en').

    Built-ins cover the common cluster languages (en, nl, de, fr, es, it). For
    any other language — including CJK — set `meta.headings` to a dict of
    {section_key: localized_label}; it overrides/extends the built-in set, so a
    Korean or Japanese CV can localize its headings without a code change. The
    model populates `meta.headings` when rendering in a language with no built-in.
    """
    meta = profile.get("meta") or {}
    # English is the floor: start from it, then overlay the target language's
    # table. Any key a language table doesn't translate falls back to the English
    # label instead of raising — so adding a new section never needs all nine
    # tables updated at once, and a partially-localized language degrades cleanly.
    language = str(meta.get("language") or "en").strip().lower()[:2]
    base = dict(HEADINGS["en"])
    if language not in HEADINGS and not (meta.get("headings") or {}):
        # Documented, and until now silent. A Polish, Vietnamese, Thai, Arabic,
        # Swedish, Portuguese or Russian CV rendered with ENGLISH section
        # headings above its own-language content and said nothing, so the first
        # person to notice was the recruiter.
        _warn_once(_HEADING_WARNED, (id(profile), language),
                   f"WARNING: no built-in section headings for meta.language "
                   f"{language!r}; the CV will use ENGLISH headings above "
                   f"{language!r} content. Set meta.headings to a "
                   f"{{section_key: label}} map to localize them. Built-in: "
                   f"{', '.join(sorted(HEADINGS))}.")
    base.update(HEADINGS.get(language, {}))
    override = meta.get("headings") or {}
    if isinstance(override, dict):
        unknown = sorted(k for k in override if k not in base)
        if unknown:
            print(f"WARNING: meta.headings key(s) "
                  f"{', '.join(repr(k) for k in unknown)} are not section keys and "
                  f"were ignored — the section keeps its default label. Valid keys: "
                  f"{', '.join(sorted(base))}.", file=sys.stderr)
        base.update({k: v for k, v in override.items() if k in base and v})
    return base


# ── URL helpers ───────────────────────────────────────────────────────────────

def normalize_url(u):
    """Ensure URL has a scheme; strip trailing whitespace. Coerces non-string
    inputs (a YAML link that parsed as a number/date) so a malformed profile
    never crashes the render."""
    u = str(u or "").strip()
    if u and "://" not in u:
        return "https://" + u
    return u


def display_url(u):
    """Return a human-readable URL (no scheme prefix). Kept for callers that
    want the bare URL; the CV itself prefers `link_label` instead."""
    for prefix in ("https://", "http://"):
        if u.startswith(prefix):
            return u[len(prefix):]
    return u


# Friendly labels keyed by the contact.links key (normalised: lowercase, no
# separators) or by the URL's host. The point is that a reader scanning the
# header sees "Google Scholar", not a query-string-laden URL.
_LABELS_BY_KEY = {
    "scholar": "Google Scholar",
    "googlescholar": "Google Scholar",
    "github": "GitHub",
    "gitlab": "GitLab",
    "bitbucket": "Bitbucket",
    "linkedin": "LinkedIn",
    "orcid": "ORCID",
    "website": "Website",
    "homepage": "Website",
    "site": "Website",
    "portfolio": "Portfolio",
    "blog": "Blog",
    "twitter": "Twitter",
    "x": "X",
    "mastodon": "Mastodon",
    "researchgate": "ResearchGate",
    "semanticscholar": "Semantic Scholar",
    "youtube": "YouTube",
    "medium": "Medium",
    "substack": "Substack",
    "kaggle": "Kaggle",
    "huggingface": "Hugging Face",
    "stackoverflow": "Stack Overflow",
    "devpost": "Devpost",
    "dribbble": "Dribbble",
    "behance": "Behance",
}

_LABELS_BY_HOST = {
    "scholar.google.com": "Google Scholar",
    "github.com": "GitHub",
    "gitlab.com": "GitLab",
    "bitbucket.org": "Bitbucket",
    "linkedin.com": "LinkedIn",
    "orcid.org": "ORCID",
    "twitter.com": "Twitter",
    "x.com": "X",
    "researchgate.net": "ResearchGate",
    "semanticscholar.org": "Semantic Scholar",
    "youtube.com": "YouTube",
    "youtu.be": "YouTube",
    "medium.com": "Medium",
    "substack.com": "Substack",
    "kaggle.com": "Kaggle",
    "huggingface.co": "Hugging Face",
    "stackoverflow.com": "Stack Overflow",
    "devpost.com": "Devpost",
    "dribbble.com": "Dribbble",
    "behance.net": "Behance",
}


def _host(url):
    """Bare host of a URL, lowercased, without leading www / userinfo / port."""
    s = str(url or "")
    host = s.split("://", 1)[-1].split("/", 1)[0].split("?", 1)[0]
    host = host.split("@", 1)[-1].split(":", 1)[0]   # drop user@ and :port
    if host.startswith("www."):
        host = host[4:]
    return host.lower()


def link_label(url, key=None, explicit=None):
    """Human-readable label for a link.

    Priority: an explicit label the profile supplied → a known key (e.g. the
    `scholar:` field) → a known host → a title-cased key → the bare host. We
    never fall back to the full URL: the whole point is to keep it off the page.
    """
    if explicit:
        return explicit
    url = str(url or "")
    if key:
        norm = "".join(ch for ch in key.lower() if ch.isalnum())
        if norm in _LABELS_BY_KEY:
            return _LABELS_BY_KEY[norm]
    host = _host(url)
    if host in _LABELS_BY_HOST:
        return _LABELS_BY_HOST[host]
    for known_host, label in _LABELS_BY_HOST.items():
        if host == known_host or host.endswith("." + known_host):
            return label
    if key:
        return key.replace("_", " ").replace("-", " ").title()
    return host or url


def resolve_link(item, key=None):
    """Turn a link entry into ``(label, url)``.

    An entry may be a bare URL string or a ``{label, url}`` mapping — the latter
    lets a profile override the auto-label (e.g. label a personal domain
    "Portfolio"). Returns ``(None, None)`` for an empty entry so callers can skip.
    """
    explicit = None
    if isinstance(item, dict):
        explicit = item.get("label") or item.get("text")
        raw = item.get("url") or item.get("href") or ""
    else:
        raw = item or ""
    if not raw:
        return None, None
    url = normalize_url(raw)
    return link_label(url, key=key, explicit=explicit), url


# ── Section ordering ──────────────────────────────────────────────────────────

# Two sensible defaults. Industry leads with Experience (recruiters spend
# seconds on the first pass and want impact up top); academic leads with
# Education and surfaces Publications early (the primary credentials of a
# researcher). Empty sections are skipped regardless, so an order may safely
# list sections a given profile doesn't have.
# `achievements` (a "Selected Achievements" band) and `board` (board/advisory
# roles) exist mainly for senior/executive CVs; they sit near the end of the
# default orders (empty → skipped for everyone else), and an exec promotes them
# via meta.section_order. They must appear here so section_order accepts them.
_INDUSTRY_ORDER = ["summary", "achievements", "experience", "internships", "education", "skills",
                   "projects", "publications", "awards", "certifications", "board",
                   "volunteer"]
_ACADEMIC_ORDER = ["summary", "achievements", "education", "experience", "internships", "publications",
                   "skills", "projects", "awards", "certifications", "board", "volunteer"]
_ALL_SECTIONS = _INDUSTRY_ORDER  # canonical set of known section keys

_ACADEMIC_TITLE_SIGNALS = (
    "phd", "ph.d", "ph. d", "doctoral", "postdoc", "post-doc", "postdoctoral",
    "research fellow", "research scientist", "research associate",
    "research assistant", "researcher", "lecturer", "professor",
)


# Word-boundary match so an end date that is genuinely ongoing ("present",
# "2027 (est.)", "expected 2027") reads as current, while substrings inside
# ordinary words ("greatest", "invested", "West") do not.
# "still there", in the languages this skill renders CVs in. English-only, the
# consequence was silent and ran two ways: `is_academic_profile` decides where
# Education sits, and render_rirekisho printed a 履歴書 row reading 退社 — "left
# the company" — for a candidate whose end date said 現在 ("present").
#
# The ASCII half keeps `\b`; the CJK half must not use it, because there is no
# word boundary between 現在 and the character beside it (see
# check_evidence_refs.REF_RE for the same rule and the same bug).
_ONGOING_RE = re.compile(
    r"\b(present|current|ongoing|now|expected|anticipated|est|"
    r"heden|nu|heute|derzeit|laufend|aktuell|"
    r"actuel|actuellement|aujourd'hui|"
    r"actualidad|actualmente|presente|attuale|oggi)\b"
    r"|至今|迄今|现在|現在|在职|在職|在读|在讀|至现在|"
    r"在職中|現在に至る|現職|"
    r"재직|재직중|현재")


def _field_text(value) -> str:
    """One single-value field (a `start`/`end` date, a phone number) as the text a
    reader should see.

    Profiles are hand-written YAML, and YAML types a bare `end: 2023` as an int and
    `end: 2023-06-30` as a date. Both are ordinary ways to write a date, and both
    crashed every format with `AttributeError: ... has no attribute 'strip'` (exit
    1, which this script reserves for "the PDF step failed") while check_claims,
    check_personal_data and check_pages accepted the same file. A date object comes
    back as the ISO text the user typed, not as Python's repr.

    Anything that is not one value (a list, a mapping, a YAML boolean) is a shape
    problem, and `profile_shape_problems` refuses it before rendering starts; this
    function only has to stay total for direct callers.
    """
    if value is None:
        return ""
    if isinstance(value, datetime.datetime):
        if value.time() == datetime.time(0, 0):
            return value.date().isoformat()
        return value.isoformat(sep=" ")
    if isinstance(value, datetime.date):
        return value.isoformat()
    return str(value).strip()


def _is_current(entry):
    """True if an experience/education entry is ongoing (no real end date)."""
    end = _field_text(journal.as_mapping(entry).get("end")).lower()
    return end == "" or bool(_ONGOING_RE.search(end))


def is_academic_profile(profile):
    """Heuristic: should this CV lead with Education?

    Conservative on purpose — a senior engineer who happens to have a paper is
    not 'academic'. We flip only when the candidate's *current* situation is
    academic: a current research/PhD role, or a current student with no
    professional experience yet. Anything finer, the profile sets
    `meta.section_order` explicitly.
    """
    experience = _entries(profile, "experience")
    for ex in experience:
        title = str(ex.get("title") or "").lower()
        if _is_current(ex) and any(sig in title for sig in _ACADEMIC_TITLE_SIGNALS):
            return True
    currently_studying = any(_is_current(ed) for ed in _entries(profile, "education"))
    has_pro_experience = any((ex.get("bullets") or []) for ex in experience)
    return currently_studying and not has_pro_experience


def _entries(profile, section):
    """The mapping entries of a list section; `profile_shape_problems` has already
    refused any other shape on the CLI path, this keeps direct callers total."""
    entries = journal.as_mapping(profile).get(section)
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def experience_entries(profile, section):
    # Keep the evidence schema intact: only the display group changes.
    return [entry for entry in _entries(profile, "experience")
            if entry.get("section", "experience") == section]


def experience_heading(profile, section):
    return headings(profile)[section]


def section_order(profile):
    """Resolve the order of body sections for this profile.

    `meta.section_order` wins if present (unknown keys ignored; any known
    section the profile omitted is appended in default order so a section with
    real content is never silently dropped — order is for sequencing, not
    hiding). Otherwise pick the academic or industry default.
    """
    default = _ACADEMIC_ORDER if is_academic_profile(profile) else _INDUSTRY_ORDER
    explicit = journal.as_mapping(
        journal.as_mapping(profile).get("meta")).get("section_order")
    if not explicit:
        return default
    if isinstance(explicit, str):       # tolerate a single key written as a scalar
        explicit = [explicit]
    unknown = [s for s in explicit if s not in _ALL_SECTIONS]
    if unknown:
        print(f"WARNING: meta.section_order entr(ies) "
              f"{', '.join(repr(s) for s in unknown)} are not section keys and were "
              f"ignored. Valid keys: {', '.join(_ALL_SECTIONS)}.", file=sys.stderr)
    order = []
    for s in list(explicit) + default:           # explicit first, then any omitted
        if s in _ALL_SECTIONS and s not in order:  # known-only, de-duplicated
            order.append(s)
    return order


# ── Shared helpers ────────────────────────────────────────────────────────────

# assets/profile.example.yaml:2 — "All fields optional except meta.name and
# contact.email." Nothing enforced that. A profile missing meta.name rendered a CV
# with an EMPTY name block in all three formats — `{\LARGE \textbf{}}` in LaTeX,
# a bare `#` in Markdown — printed "Wrote cv.pdf", and exited 0. A CV with no name
# on it is worthless to the reader and invisible to every gate downstream:
# check_pages cannot require a name the profile never supplied, the judges read a
# cv.md that is wrong in the same way, and the candidate sees a filename, not a page.
# Refusing to render is right here rather than a warning: unlike a missing LaTeX
# engine, there is no partial output worth having.
REQUIRED_PROFILE_FIELDS = (("meta", "name"), ("contact", "email"))


def missing_required_fields(profile) -> list:
    """The declared-required fields this profile does not supply, as 'a.b' strings."""
    # `(x or {}).get` guards None and every falsy value and NOT a non-empty
    # string, a list, an int or True — so `meta: "us"` in hand-written YAML
    # raised AttributeError inside the function whose whole job is to REPORT a
    # malformed profile. The boundary check crashed before it could say what was
    # wrong. `journal.as_mapping` is the idiom written for exactly this.
    missing = []
    for section, key in REQUIRED_PROFILE_FIELDS:
        value = journal.as_mapping(
            journal.as_mapping(profile).get(section)).get(key)
        if not (str(value).strip() if value is not None else ""):
            missing.append(f"{section}.{key}")
    return missing


# A field that must hold ONE value. int/float/date are accepted because YAML types
# `end: 2023` and `end: 2023-06-30` that way and the gates accept them; a bool is
# not, because `end: no` meaning a date is never what the writer meant.
_ONE_VALUE = (str, int, float, datetime.date)

# Per list section: the fields printed as one piece of text. `location` is left
# out on purpose — the legacy `{city, country}` mapping has its own documented
# warn-and-omit path in `scalar_field`.
_ENTRY_FIELDS = {
    "experience": ("title", "org", "start", "end"),
    "education": ("degree", "institution", "start", "end"),
    "projects": ("name", "role", "description"),
}
_DATE_HINT = 'one value such as "2023-06", 2023 or "present"'


def _shape_name(value) -> str:
    """'a list', 'a mapping', 'a true/false value' … — for "X is <this>"."""
    if isinstance(value, bool):
        return "a true/false value"
    return {dict: "a mapping", list: "a list", tuple: "a list", str: "a string",
            int: "a number", float: "a number"}.get(type(value),
                                                    f"a {type(value).__name__}")


def _one_value(value) -> bool:
    return value is None or (isinstance(value, _ONE_VALUE)
                             and not isinstance(value, bool))


def profile_shape_problems(profile) -> list:
    """Every place this profile has a shape the renderers cannot print, as text.

    The renderer used to find these by crashing: `skills: [Python, SQL]` raised
    `'list' object has no attribute 'values'` and an entry written as a bare string
    raised inside a builder, both as a traceback at exit 1 — the code main() keeps
    for "rendered, and the PDF step failed". What can be read sensibly is read
    (an int or a YAML date, a plain list of skills, a list `details`); this lists
    only what has no sensible reading, so main() can refuse once, at exit 2, with
    a sentence that names the field.
    """
    profile = journal.as_mapping(profile)
    problems = []
    meta = journal.as_mapping(profile.get("meta"))
    contact = journal.as_mapping(profile.get("contact"))
    for where, value in (("meta.name", meta.get("name")),
                         ("meta.headline", meta.get("headline")),
                         ("contact.email", contact.get("email")),
                         ("contact.phone", contact.get("phone"))):
        if not _one_value(value):
            problems.append(f"{where} is {_shape_name(value)}; it must be one value")
    summary = profile.get("summary")
    if isinstance(summary, dict) or isinstance(summary, bool):
        problems.append(f"summary is {_shape_name(summary)}; it must be text")
    for section, fields in _ENTRY_FIELDS.items():
        entries = profile.get(section)
        if entries in (None, "", [], {}):
            continue
        if not isinstance(entries, list):
            problems.append(f"{section} is {_shape_name(entries)}; it must be a "
                            f"list of entries, each one starting with `- `")
            continue
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                problems.append(f"{section}[{i}] is {_shape_name(entry)}, not a "
                                f"mapping of fields such as `{fields[0]}:`")
                continue
            for field in fields:
                value = entry.get(field)
                if not _one_value(value):
                    hint = _DATE_HINT if field in ("start", "end") else "one value"
                    problems.append(f"{section}[{i}].{field} is "
                                    f"{_shape_name(value)}; it must be {hint}")
    skills = profile.get("skills")
    if skills not in (None, "") and not isinstance(skills, (dict, list, str)):
        problems.append(f"skills is {_shape_name(skills)}; it must be a mapping "
                        f"of group: [items], or a list of items")
    return problems


def load_profile(path):
    """The profile as a mapping. Raises journal.YamlUnreadable on an unusable file.

    A renderer is NOT a gate: there is no workspace, so there is no receipt and no
    exit-2-with-a-receipt available to it. What is available is the exit code, and
    main() spends it — 2 for "could not read the input", which stays distinct from
    1, "rendered, and the PDF step failed". That distinction is the whole reason
    this does not just let a yaml traceback out: a traceback exits 1, which for this
    script already means something else.
    """
    profile = journal.load_yaml(path)
    missing = missing_required_fields(profile)
    if missing:
        raise ValueError(
            f"{path}: missing required field(s) {', '.join(missing)} — "
            f"assets/profile.example.yaml declares these the only two required fields, "
            f"and rendering without them produces a CV with a blank name or no way to "
            f"reply to it. Add them to the profile; do not work around this by editing "
            f"the rendered output, which the next re-render discards.")
    problems = profile_shape_problems(profile)
    if problems:
        raise ValueError(f"{path}: the profile has a shape the renderer cannot "
                         f"print: {'; '.join(problems)}.")
    return profile


def _contact_links(profile):
    """Yield (label, url) for each non-empty contact link, in profile order.

    `links` is documented as a mapping, but a plain list of URLs is the other
    obvious way to write it and used to raise AttributeError; each item is then
    labelled by its host, exactly as a project link is."""
    links = journal.as_mapping(
        journal.as_mapping(profile).get("contact")).get("links") or {}
    pairs = links.items() if isinstance(links, dict) else (
        (None, item) for item in as_list(links))
    for key, item in pairs:
        label, url = resolve_link(item, key=None if key is None else str(key))
        if url:
            yield label, url


def _contact_bits(profile):
    """email, phone, location — as display text, in that order, empties dropped.

    `phone: 31612345678` is an int in YAML, and `" · ".join` raised TypeError on it."""
    c = journal.as_mapping(journal.as_mapping(profile).get("contact"))
    bits = [_field_text(c.get("email")), _field_text(c.get("phone")),
            scalar_field(c.get("location"), "contact.location")]
    return [b for b in bits if b]


# Which regional CV convention a `meta.target_market` string belongs to.
#   1 = US/CA/UK/IE/AU/NZ — a photo/DOB/nationality is a liability there; many
#       employers route such CVs straight to rejection because considering that
#       data exposes them to discrimination-law claims.
#   2 = EU/EEA, 3 = East & SE Asia — the same fields are a normal convention.
#   None = not recognised, which is NOT the same as "safe".
#
# Full names are matched as whole-word phrases anywhere in a segment, so
# "United States of America" and "London, United Kingdom" both resolve. Two-letter
# codes are matched only when they are the WHOLE segment: otherwise "Remote in
# Berlin" would resolve to India via "in", and a false resolution is worse than
# none — it silences the warning.
# ENDONYMS ARE IN HERE, and that is not decoration. `Nederland`, `Österreich`,
# `España`, `Suomi`, `Sverige`, `한국` and `Việt Nam` all resolved to None on
# 2026-09-05 — so a profile written in its own market's language got no cluster,
# and the personal-data interlock could not fire on it at all. A candidate
# writing their own country's name for their own country is the ordinary case,
# not the exotic one.
_CLUSTER_NAMES = {
    1: ["united states of america", "united states", "u s a", "america", "canada",
        "united kingdom", "great britain", "britain", "england", "scotland", "wales",
        "northern ireland", "republic of ireland", "ireland", "australia",
        "new zealand", "u k", "u s", "etats unis", "états unis", "estados unidos",
        "vereinigte staaten", "verenigde staten", "royaume uni", "reino unido",
        "grossbritannien", "großbritannien", "groot brittannie", "eire",
        "nouvelle zelande", "nouvelle zélande", "irlande", "australie",
        "nueva zelanda", "irlanda", "australien", "kanada", "canada"],
    2: ["the netherlands", "netherlands", "holland", "germany", "deutschland",
        "france", "belgium", "spain", "italy", "portugal", "austria", "switzerland",
        "sweden", "norway", "denmark", "finland", "poland", "czechia",
        "czech republic", "luxembourg", "greece", "romania", "hungary",
        # `ireland eu` used to sit here and could never resolve: `ireland` is
        # Cluster 1 and matches the same string, and resolve_cluster takes
        # min() because suppression is the safe direction. An entry listed
        # under a cluster it can never reach is a table that lies to its
        # reader — and an Irish CV is an anglophone CV, so Cluster 1 was the
        # right answer all along.
        "european union", "eea",
        # endonyms
        "nederland", "belgie", "belgië", "belgique", "osterreich", "österreich",
        "schweiz", "suisse", "svizzera", "espana", "españa", "italia", "portugal",
        "suomi", "sverige", "norge", "danmark", "polska", "cesko", "česko",
        "ellada", "elláda", "magyarorszag", "magyarország", "romania", "românia",
        "luxemburg", "letzebuerg", "lëtzebuerg", "europese unie", "union europeenne",
        "europaische union", "europäische union", "frankreich", "duitsland",
        "allemagne", "alemania", "germania", "pays bas", "paises bajos",
        "niederlande", "olanda", "autriche", "suede", "suède", "norvege",
        "norvège", "danemark", "finlande", "pologne", "grece", "grèce",
        "belgien", "spanien", "italien", "schweden", "polen", "griechenland"],
    3: ["mainland china", "china", "hong kong", "taiwan", "japan", "south korea",
        "republic of korea", "korea", "singapore", "malaysia", "thailand", "vietnam",
        "indonesia", "philippines", "india",
        # endonyms
        "nippon", "nihon", "hanguk", "한국", "대한민국", "viet nam", "việt nam",
        "zhongguo", "malaysia", "singapura", "prathet thai", "bharat",
        "pilipinas", "indonesia",
        "coree du sud", "corée du sud", "japon", "chine", "inde", "singapour",
        "japan", "korea del sur", "giappone", "cina", "china"],
}
_CLUSTER_CODES = {
    1: ["us", "usa", "ca", "can", "uk", "gb", "ie", "irl", "au", "aus", "nz"],
    2: ["nl", "de", "fr", "be", "es", "it", "pt", "at", "ch", "se", "no", "dk",
        "fi", "pl", "cz", "lu", "gr", "ro", "hu", "eu"],
    3: ["cn", "prc", "hk", "tw", "jp", "kr", "sg", "my", "th", "vn", "id", "ph", "in"],
}
# CJK market names have no word boundaries to split on, so they are matched by
# substring. Without these a Chinese-language profile resolves to None and the
# unknown-market warning fires on a perfectly ordinary Chinese CV.
_CLUSTER_CJK = {
    1: ["美国", "美國", "英国", "英國", "加拿大", "澳大利亚", "澳大利亞",
        "新西兰", "紐西蘭", "爱尔兰", "愛爾蘭", "アメリカ", "イギリス", "カナダ",
        "미국", "영국", "캐나다", "호주"],
    2: ["荷兰", "荷蘭", "德国", "德國", "法国", "法國", "比利时", "比利時",
        "西班牙", "意大利", "瑞士", "瑞典", "挪威", "丹麦", "丹麥", "芬兰", "芬蘭",
        "波兰", "波蘭", "奥地利", "奧地利", "葡萄牙", "欧盟", "歐盟",
        "オランダ", "ドイツ", "フランス", "독일", "네덜란드", "프랑스"],
    3: ["中国", "中國", "中华人民共和国", "中華人民共和國",
        "中国大陆", "中國大陸", "香港", "台湾", "台灣",
        "日本", "韩国", "韓国", "韓國", "新加坡", "马来西亚", "馬來西亞",
        "泰国", "泰國", "印度", "越南", "印度尼西亚", "菲律宾",
        "한국", "대한민국", "일본", "중국", "싱가포르"],
}

_NAME_CLUSTER, _CODE_CLUSTER, _CJK_CLUSTER = {}, {}, {}
for _c, _names in _CLUSTER_NAMES.items():
    for _n in _names:
        _NAME_CLUSTER.setdefault(_n, _c)
for _c, _codes in _CLUSTER_CODES.items():
    for _n in _codes:
        _CODE_CLUSTER.setdefault(_n, _c)
for _c, _names in _CLUSTER_CJK.items():
    for _n in _names:
        _CJK_CLUSTER.setdefault(_n, _c)
_MAX_NAME_WORDS = max(len(_n.split()) for _n in _NAME_CLUSTER)

# A plain hyphen is NOT a separator. `États-Unis`, `Pays-Bas`,
# `Nouvelle-Zélande` and `Corée-du-Sud` are how those countries are spelled, and
# splitting on it meant every hyphenated country name resolved to nothing.
# The DASHES stay: `Remote — EU` really does use one to separate two facts.
_MARKET_SEP = re.compile(r"[,()\[\]/|;·–—]+")
_MARKET_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)

# The protected fields, in the order they are reported. `contact.personal` is a
# free-form dict, so any key in it is treated as protected — the risk is the
# category, not a fixed list of key names.
_PHOTO_FIELD = "meta.photo"


_MARKET_SEP_HYPHEN = re.compile(r"[,()\[\]/|;·–—-]+")


def _fold_market(text: str) -> str:
    """Lowercase, and strip diacritics from LATIN letters only.

    `Groot-Brittannië` and `Éire` are how a Dutch or Irish candidate really
    spells those, and listing only the ASCII-folded forms meant the accented
    ones — the real ones — resolved to nothing. Folding rather than listing
    covers every accented spelling at once, including ones nobody thought of.
    Non-Latin scripts are left alone: a Thai vowel sign is a letter, not an
    accent (see paths._fold_latin for the same rule and the same reason).
    """
    text = unicodedata.normalize("NFKC", str(text or "")).lower()
    out = []
    for ch in text:
        if unicodedata.name(ch, "").startswith("LATIN"):
            out.append("".join(c for c in unicodedata.normalize("NFKD", ch)
                               if not unicodedata.combining(c)))
        else:
            out.append(ch)
    return "".join(out)


def _market_segments(market):
    """Segments, under BOTH hyphen conventions.

    A plain hyphen joins a country name (`États-Unis`, `Pays-Bas`) and also
    joins a code to a qualifier (`DE-based`, `NL-remote`), so neither treatment
    alone is right. Splitting on it broke the first; not splitting broke the
    second — measured, and the second is worse, because an unresolved market
    now WITHHOLDS personal data and a German candidate writing `DE-based`
    silently lost the photo and date of birth their market expects.

    Both segmentations are yielded and `resolve_cluster` unions the matches.
    """
    text = _fold_market(market)
    seen = set()
    for pattern in (_MARKET_SEP, _MARKET_SEP_HYPHEN):
        for seg in pattern.split(text):
            seg = " ".join(_MARKET_PUNCT.sub(" ", seg).split())
            if seg and seg not in seen:
                seen.add(seg)
                yield seg


# Two-letter codes that are BOTH a country this table knows and a subdivision of
# a Cluster-1 country. Exactly four, computed against the 50 US states, DC, the
# Canadian provinces and the Australian states:
#
#   DE  Germany            / Delaware
#   ID  Indonesia          / Idaho
#   IN  India              / Indiana
#   NL  the Netherlands    / Newfoundland and Labrador
#
# "Wilmington, DE" resolved to cluster 2 and rendered a date of birth, an age, a
# marital status, a nationality and a photo onto a US CV — the exact fields US
# employers bin a CV for carrying. Reproduced 2026-09-06; `check_shortlist.py`
# already carried a US-state regex for this same ambiguity and this module had
# none.
#
# The fix uses the mechanism `resolve_cluster` already has for this: it adds
# cluster 1 as WELL, and `min(found)` picks the safe side. That is the module's
# stated asymmetry — stripping a photo from a German CV is cosmetic and warns;
# leaving a DOB on a US CV is an automatic reject and is silent.
_AMBIGUOUS_SUBDIVISION_CODES = {"de": "Delaware", "id": "Idaho",
                                "in": "Indiana", "nl": "Newfoundland and Labrador"}
_AMBIGUOUS_WARNED: list = []

# A bare code is the COUNTRY. Nobody writes `meta.target_market: "DE"` meaning
# Delaware, and `NL-remote` is a Dutch remote role. The subdivision reading only
# arises in the `<place>, <CODE>` shape — so the code counts as ambiguous only
# when the same string carries another segment that is neither the code itself
# nor one of these work-arrangement words.
#
# `Eindhoven, NL (hybrid)` matches that shape and is Dutch, so it now
# over-strips and warns. That is the trade this module's own docstring names:
# stripping a photo from a Dutch CV is cosmetic and recoverable by writing
# "Netherlands"; leaving a date of birth on a CV for Wilmington, Delaware is an
# automatic rejection and was silent.
_ARRANGEMENT_WORDS = frozenset("""
based remote hybrid onsite on site nationwide wide area region regional metro
greater emea apac only preferred relocation relocate willing anywhere
""".split())


def _looks_like_a_place_plus_code(code, segments) -> bool:
    """Is this the `<place>, <CODE>` shape rather than a bare country code?

    True when some other segment is a word that is neither the code, nor a
    work-arrangement word, nor a country this table already knows. `wilmington`
    qualifies; `based`, `remote` and `hybrid` do not; `nl` alone has no other
    segment at all.
    """
    for other in segments:
        if other == code or code in other.split():
            continue
        words = [w for w in other.split() if w]
        if not words:
            continue
        if all(w in _ARRANGEMENT_WORDS for w in words):
            continue
        if other in _CODE_CLUSTER or other in _NAME_CLUSTER:
            continue
        return True
    return False


def resolve_cluster(market):
    """1, 2, 3 — or None when the string names no market we know.

    When several clusters match (e.g. 'remote (US) / hybrid Berlin') the lowest
    wins: suppression is the safe direction, because the cost of stripping a
    photo from an EU CV is cosmetic and the cost of leaving a DOB on a US CV is
    an automatic rejection at best.
    """
    text = _fold_market(market)
    found = {c for alias, c in _CJK_CLUSTER.items() if alias in text}
    segments = list(_market_segments(market))
    ambiguous = []
    for seg in segments:
        if seg in _CODE_CLUSTER:
            found.add(_CODE_CLUSTER[seg])
            if seg in _AMBIGUOUS_SUBDIVISION_CODES and _looks_like_a_place_plus_code(
                    seg, segments):
                # Also a US/CA subdivision. Add the safe side and let min() win.
                found.add(1)
                ambiguous.append(seg)
        words = seg.split()
        for n in range(_MAX_NAME_WORDS, 0, -1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i + n])
                if phrase in _NAME_CLUSTER:
                    found.add(_NAME_CLUSTER[phrase])
    resolved = min(found) if found else None
    if ambiguous and resolved == 1:
        _warn_once(
            _AMBIGUOUS_WARNED, (str(market),),
            f"WARNING: meta.target_market {market!r} contains "
            + " and ".join(f"{c.upper()!r}" for c in ambiguous)
            + ", which is both a country code and a "
            + " and ".join(_AMBIGUOUS_SUBDIVISION_CODES[c] for c in ambiguous)
            + " abbreviation. It was read as the US/Canada side and personal data "
              "will be WITHHELD, because leaving a date of birth on a US CV is an "
              "auto-reject while omitting a photo from a European one is cosmetic. "
              "If you meant the country, write it out (e.g. 'Germany', "
              "'Netherlands') and re-render.")
    return resolved


_PERSONAL_SHAPE_WARNED: list = []


def _personal_mapping(profile):
    """`contact.personal` as a dict, warning ONCE if it is any other shape.

    A list, a string or a number here made the whole personal block vanish:
    `protected_fields` returned [] and `personal_items` yielded nothing, so a
    Dutch or German CV lost the date of birth and nationality its market
    expects — and said nothing. Every other over-strip in this module is loud;
    the unrecognised-market path prints a full WARNING naming the withheld
    fields. Silence here was the outlier, and the one shape a model gets wrong
    by writing `personal:` as a list of one-key dicts, which reads fine in YAML.

    It is a warning and not a refusal: the rest of the CV is correct and worth
    rendering, and the user can fix one key. Suppression stays the job of
    `_suppress_personal_data`, which is about the MARKET, not the shape.
    """
    contact = journal.as_mapping(journal.as_mapping(profile).get("contact"))
    personal = contact.get("personal")
    if personal in (None, "", [], {}):
        return {}
    if isinstance(personal, dict):
        return personal
    _warn_once(
        _PERSONAL_SHAPE_WARNED, (id(profile), repr(personal)[:80]),
        f"WARNING: contact.personal is a {type(personal).__name__}, not a "
        f"mapping, so no personal data was rendered at all. It must be a dict — "
        f"`personal: {{date_of_birth: ..., nationality: ...}}` — not a list of "
        f"one-key entries. For a market that expects these fields this is a "
        f"silent drop of exactly the data the CV needs; for a US/UK target they "
        f"would have been withheld anyway. Fix the shape and re-render.")
    return {}


def protected_fields(profile):
    """Names of the protected personal-data fields actually present."""
    out = []
    personal = _personal_mapping(profile)
    out += [f"contact.personal.{k}" for k, v in personal.items()
            if v not in (None, "")]
    if journal.as_mapping(journal.as_mapping(profile).get("meta")).get("photo"):
        out.append(_PHOTO_FIELD)
    return out


# One warning per (profile object, market), not per render call. An md + docx
# + pdf run — three invocations, or three direct calls from one process —
# renders from the SAME profile dict, and printing the identical warning three
# times is how a warning gets trained away. (main() takes one --format per
# invocation: md, docx or pdf. There is no `all`.) The profile OBJECT is held
# rather than its id(): an id can be
# reused after garbage collection, and a silently-suppressed leak warning is
# exactly the failure this interlock exists to prevent.
_MARKET_WARNED = []


def reset_market_warnings():
    """Forget which profiles have already warned. main() calls this at the top
    of every CLI run so the guard is per-run, not per-process."""
    _MARKET_WARNED.clear()
    _HEADING_WARNED.clear()


def _warn_unknown_market(profile):
    """Loud when the market is unrecognised AND protected data is present.

    cv-craft.md claims a mis-tailored profile 'physically cannot leak protected
    data onto a US/UK CV'. It could, for five measured spellings. The matcher
    above closes those; this closes the class — an unrecognised market is not
    evidence that rendering a DOB is safe, and silence there is what made the
    original claim false.
    """
    market = journal.as_mapping(
        journal.as_mapping(profile).get("meta")).get("target_market")
    if resolve_cluster(market) is not None:
        return
    fields = protected_fields(profile)
    if not fields:
        return
    if any(p is profile and m == market for p, m in _MARKET_WARNED):
        return
    _MARKET_WARNED.append((profile, market))
    print(f"WARNING: meta.target_market {market!r} matches no known CV-convention "
          f"cluster, so these fields were WITHHELD rather than rendered: "
          f"{', '.join(fields)}. That is the conservative default (SKILL.md): "
          f"leaving a date of birth on a US or UK CV is a discrimination-law "
          f"liability and a common auto-reject, while omitting a photo from a "
          f"European one is cosmetic. If this market does expect them, set "
          f"meta.target_market to a country name this renderer knows and "
          f"re-render.", file=sys.stderr)


def _suppress_personal_data(profile) -> bool:
    """Whether protected personal data must be withheld from this render.

    Cluster 1 (US/CA/UK/IE/AU/NZ) — and ALSO any market this module does not
    recognise, which is the half that was missing. `resolve_cluster` returns
    None for Brazil, Mexico, South Africa, Israel and every Gulf market, and
    None was being read as "not Cluster 1, so print it": the interlock could
    not fire on exactly the markets nobody had thought about.

    SKILL.md:219 already states the rule this now implements — "When in genuine
    doubt about a market, follow the conservative default and omit them" — and
    the cost asymmetry is in `resolve_cluster`'s own docstring: stripping a
    photo from an EU CV is cosmetic, leaving a DOB on a US CV is an automatic
    reject. The unrecognised-market WARNING still prints, so the candidate can
    name a recognised market and get the fields back.
    """
    return resolve_cluster(journal.as_mapping(
        journal.as_mapping(profile).get("meta")).get("target_market")) in (1, None)


# Personal-data labels, in the languages that have a headings table. The label
# used to be `str(key).replace("_", " ").title()` — the ENGLISH YAML key — so a
# Chinese CV printed `Date Of Birth` and `Marital Status` above Chinese values.
# Chinese furniture in an English page is a bug this skill already names; the
# mirror image is the same bug.
#
# `age` was the one key missing from all eight tables, so every CJK CV printed
# the English word above a Chinese, Japanese or Korean value — and `age` is one
# of the five fields SKILL.md's interlock is specified around and the single
# most common personal field on an East Asian résumé. The fallback below is why
# it was silent; `test_every_interlock_field_has_a_label` is why the next one
# will not be.
#
# A key with no translation falls back to the English title-case form rather
# than raising, so adding a `contact.personal` field never needs nine tables
# updated at once — the same rule `headings` uses.
PERSONAL_LABELS = {
    "nl": {"date_of_birth": "Geboortedatum", "age": "Leeftijd", "nationality": "Nationaliteit",
           "hometown": "Woonplaats", "marital_status": "Burgerlijke staat",
           "gender": "Geslacht"},
    "de": {"date_of_birth": "Geburtsdatum", "age": "Alter", "nationality": "Staatsangehörigkeit",
           "hometown": "Wohnort", "marital_status": "Familienstand",
           "gender": "Geschlecht"},
    "fr": {"date_of_birth": "Date de naissance", "age": "Âge", "nationality": "Nationalité",
           "hometown": "Domicile", "marital_status": "Situation familiale",
           "gender": "Sexe"},
    "es": {"date_of_birth": "Fecha de nacimiento", "age": "Edad", "nationality": "Nacionalidad",
           "hometown": "Residencia", "marital_status": "Estado civil",
           "gender": "Sexo"},
    "it": {"date_of_birth": "Data di nascita", "age": "Età", "nationality": "Nazionalità",
           "hometown": "Residenza", "marital_status": "Stato civile",
           "gender": "Sesso"},
    "zh": {"date_of_birth": "出生日期", "age": "年龄", "nationality": "国籍",
           "hometown": "籍贯", "marital_status": "婚姻状况", "gender": "性别",
           "political_status": "政治面貌"},
    "ja": {"date_of_birth": "生年月日", "age": "年齢", "nationality": "国籍",
           "hometown": "出身地", "marital_status": "配偶者", "gender": "性別"},
    "ko": {"date_of_birth": "생년월일", "age": "나이", "nationality": "국적",
           "hometown": "출신지", "marital_status": "결혼 여부", "gender": "성별"},
}


def personal_label(key, language="en") -> str:
    table = PERSONAL_LABELS.get(str(language or "en").strip().lower()[:2], {})
    return table.get(str(key), str(key).replace("_", " ").strip().title())


def personal_items(profile):
    """(label, value) personal-data pairs for the header, in profile order.

    Drawn from ``contact.personal`` (a dict like {date_of_birth, nationality,
    hometown, marital_status}). These are normal on CVs in much of the EU and
    East Asia and absent in the Anglophone world — so they are suppressed
    entirely for a Cluster-1 target — or an unrecognised one — even if present
    (see `_suppress_personal_data`)."""
    if _suppress_personal_data(profile):
        return
    personal = _personal_mapping(profile)
    if not isinstance(personal, dict):
        return
    language = journal.as_mapping(
        journal.as_mapping(profile).get("meta")).get("language", "en")
    for key, value in personal.items():
        if value in (None, ""):
            continue
        yield personal_label(key, language), normalize_text(value)


# Formats BOTH renderers can embed. LaTeX (via graphicx under a Unicode engine)
# takes PDF/PNG/JPEG; python-docx takes PNG/JPEG/GIF/BMP/TIFF. The intersection is
# PNG and JPEG, and the intersection is what may be accepted: anything else means
# the .docx and the .pdf disagree about whether the CV has a photo, which is the
# one outcome nobody can see until a recruiter has one of the two.
_PHOTO_MAGIC = ((b"\x89PNG\r\n\x1a\n", "png"), (b"\xff\xd8\xff", "jpeg"))
SUPPORTED_PHOTO_FORMATS = ("PNG", "JPEG")
_PHOTO_WARNED = []


def reset_photo_warnings():
    _PHOTO_WARNED.clear()


def photo_format(path):
    """'png'/'jpeg' from the file's magic bytes, or None if it is neither.

    Magic bytes rather than the extension, because the extension is what the
    user's phone or browser happened to write and is routinely wrong — a `.jpg`
    that is really HEIC is exactly the file an iPhone hands over.
    """
    try:
        with pathlib.Path(path).open("rb") as fh:
            head = fh.read(12)
    except OSError:
        return None
    for magic, name in _PHOTO_MAGIC:
        if head.startswith(magic):
            return name
    return None


def photo_path(profile):
    """Resolved filesystem path of the CV photo, or None.

    Suppressed for Cluster-1 targets (a US/UK photo CV invites discrimination-law
    exposure and auto-rejection). Returns None if unset, missing, or in a format
    the renderers do not agree on, so a bad path degrades to a photo-less CV
    rather than a crash — but never SILENTLY, which is what it used to do.

    The silence was the defect. `render_docx` swallowed an unsupported image with
    a bare `except Exception: pass` while the LaTeX path died on the same file
    with an error naming a BoundingBox, so a WebP or HEIC photo — every browser
    download and every iPhone picture — produced a photo-less .docx the candidate
    believed had a photo, and a failed PDF compile that then left the previous
    round's PDF in place. The skill tells the agent to set `meta.photo` for EU
    and Asian markets and never says which formats work; this is that list.
    """
    if _suppress_personal_data(profile):
        return None
    p = journal.as_mapping(journal.as_mapping(profile).get("meta")).get("photo")
    if not p:
        return None
    path = pathlib.Path(str(p)).expanduser()
    if not path.is_file():
        _warn_photo(path, f"meta.photo points at {path}, which is not a file")
        return None
    if photo_format(path) is None:
        _warn_photo(path,
                    f"meta.photo is {path.name}, which is not a "
                    f"{' or '.join(SUPPORTED_PHOTO_FORMATS)} image (checked by "
                    f"content, not by extension). Convert it — e.g. "
                    f"`sips -s format png {path.name} --out photo.png` on macOS "
                    f"— or remove meta.photo. Rendering WITHOUT the photo")
        return None
    return path


def _warn_photo(path, message):
    """One warning per path per run: photo_path is called by all three renderers."""
    if str(path) in _PHOTO_WARNED:
        return
    _PHOTO_WARNED.append(str(path))
    print(f"WARNING: {message}.", file=sys.stderr)


def _photo_include_name(ph, asset_dir=None, asset_stem="cv"):
    """The name to hand `\\includegraphics`, staging the file if we can.

    A photo at `~/Documents/My_Photo #2.png` is an ordinary thing for a user to
    have, and it is unusable as a LaTeX filename: `#` raises "Illegal parameter
    number", `%` starts a comment, `_`/`&`/`~` are special, and spaces end the
    argument. `\\detokenize` is not enough — measured, `#` still halts the
    engine — and `latex_escape` is wrong here because graphicx needs the real
    filename, not `\\_`.

    So when the caller knows where the `.tex` is going, copy the image next to it
    under an ASCII name we choose and reference it relatively. That fixes every
    hostile character at once instead of one class at a time, and it makes the
    `.tex` self-contained — which matters because this repo treats the `.tex` as
    a deliverable the user recompiles elsewhere, and an absolute path into
    someone's home directory does not survive that trip.
    """
    ph = pathlib.Path(ph)
    if asset_dir is None:
        return str(ph)
    suffix = ".png" if photo_format(ph) == "png" else ".jpg"
    staged = pathlib.Path(asset_dir) / f"{asset_stem}-photo{suffix}"
    try:
        if ph.resolve() != staged.resolve():
            shutil.copyfile(ph, staged)
    except OSError as exc:
        _warn_photo(ph, f"could not stage the photo beside the LaTeX source "
                        f"({exc}); referencing it by absolute path, which will "
                        f"break if the .tex is compiled on another machine")
        return str(ph)
    return staged.name


def as_list(v):
    """Coerce a value into a list of items for rendering.

    Profiles are model-authored YAML, so a field that should be a list
    (``bullets``, a skills group, ``publications``) is sometimes written as a
    bare string — e.g. ``languages: "Python, C++"`` instead of a list. Iterating
    that string character-by-character silently renders 'P, y, t, h, …', which
    *looks* like a successful render but is garbage. Coercing a scalar to a
    single-item list turns that mistake into one readable item instead, and
    keeps a genuinely empty field empty.
    """
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return list(v)
    return [v]


def item_str(it):
    """Render one list item (a skill, certification, award, publication) as text.

    These are meant to be plain strings, but a model sometimes writes a list of
    dicts (e.g. ``{name: "RN", id: "12345", status: "active"}``). Plain
    ``str(dict)`` would emit Python's ``{'name': ...}`` repr onto the CV. Instead
    we join the dict's own values into a readable phrase, leading with a name-like
    field when present — strictly better than a repr, and a no-op for strings.
    """
    if isinstance(it, dict):
        lead = next((str(it[k]) for k in ("name", "title", "label", "text") if it.get(k)), None)
        rest = [str(v) for k, v in it.items()
                if k not in ("name", "title", "label", "text") and v not in (None, "")]
        parts = ([lead] if lead else []) + rest
        return " — ".join(parts)
    return str(it)


def group_label(group):
    """Display label for a skills group, preserving the author's intended case.

    The earlier ``str.capitalize()`` lower-cased everything after the first
    letter, which destroys acronyms and intentional casing — "ML/AI" became
    "Ml/ai" and "Programming Languages" became "Programming languages". We only
    upper-case the first character (so a lazily-lowercased "languages" still
    reads as "Languages") and leave the rest exactly as written.

    An underscore is a key separator, never a character to print: a real apply
    run shipped a CV whose skills line read "Llm_and_agents:", because a YAML
    key was printed verbatim onto the page.
    """
    g = str(group).replace("_", " ")
    return g[:1].upper() + g[1:] if g else g


def _is_group_list(skills) -> bool:
    """`[{Languages: [Python]}, {Tools: [Docker]}]` — groups written as a list of
    one-key mappings, each holding a list. `[{name: Python}]` is NOT this: its
    value is one item, and item_str already reads that as "Python"."""
    return bool(skills) and all(
        isinstance(x, dict) and len(x) == 1
        and isinstance(next(iter(x.values())), (list, tuple)) for x in skills)


def skill_groups(profile):
    """The skills section as `(label, items)` pairs; `label` is None for a group
    the profile did not name. One reader, three renderers.

    The documented shape is a mapping of group → list. A plain list —
    `skills: [Python, SQL, PyTorch]` — is the other obvious way to write it, and it
    crashed all three formats on `.values()` while every gate accepted the file.
    It is one unnamed group: a "Skills:" label under a "Skills" heading would say
    the same word twice.
    """
    skills = journal.as_mapping(profile).get("skills")
    if skills in (None, "", [], {}):
        return []
    if isinstance(skills, dict):
        groups = list(skills.items())
    elif isinstance(skills, (list, tuple)) and _is_group_list(skills):
        groups = [pair for group in skills for pair in group.items()]
    else:
        groups = [(None, skills)]
    out = []
    for label, items in groups:
        items = [normalize_text(item_str(i)) for i in as_list(items)
                 if i not in (None, "")]
        if items:
            out.append((None if label is None else group_label(label), items))
    return out


def detail_items(entry):
    """`education[].details` as display lines. A list is several lines — printing
    it whole put Python's `['Thesis on graph databases', 'Grade 1.3']` on the CV
    in all three formats."""
    return [normalize_text(item_str(d)).strip()
            for d in as_list(journal.as_mapping(entry).get("details"))
            if d not in (None, "") and normalize_text(item_str(d)).strip()]


def summary_text(profile) -> str:
    """The summary as one paragraph; a list of lines is joined, not repr'd."""
    summary = journal.as_mapping(profile).get("summary")
    if isinstance(summary, (list, tuple)):
        summary = " ".join(item_str(s) for s in summary if s not in (None, ""))
    return normalize_text(summary).strip()


# ── Markdown renderer ─────────────────────────────────────────────────────────

def render_markdown(profile):
    _warn_unknown_market(profile)
    h = headings(profile)
    meta = profile.get("meta", {}) or {}
    lines = [f"# {meta.get('name', '')}".rstrip()]
    if meta.get("headline"):
        lines.append(f"*{meta['headline']}*")

    # Contact line — links render as [Label](url)
    contact_parts = _contact_bits(profile)
    contact_parts += [f"[{label}]({url})" for label, url in _contact_links(profile)]
    contact_str = " · ".join([p for p in contact_parts if p])
    if contact_str:
        lines.append(contact_str)
    personal = [f"{label}: {value}" for label, value in personal_items(profile)]
    if personal:
        lines.append(" · ".join(personal))
    ph = photo_path(profile)
    if ph:
        lines.append(f"![Photo]({ph})")

    def summary():
        if summary_text(profile):
            return ["", f"## {h['summary']}", summary_text(profile)]
        return []

    def experience(section="experience"):
        out = []
        for e in experience_entries(profile, section):
            if not out:
                out += ["", f"## {experience_heading(profile, section)}"]
            header = f"**{_field_text(e.get('title'))}**, {_field_text(e.get('org'))}"
            dates = _dates(e, meta.get("language", "en"))
            meta_bits = " · ".join(
                b for b in [scalar_field(e.get("location"), "experience[].location"), dates] if b)
            # The leading "" is load-bearing, not cosmetic: without it this
            # header lazily continues the previous entry's last bullet, and a
            # CommonMark parser folds the two into one list item.
            out += ["", header + (f"  \n_{meta_bits}_" if meta_bits else "")]
            bullets = as_list(e.get("bullets"))
            if bullets:
                # Blank line again: a `- item` straight after the metadata line
                # continues that paragraph instead of opening a list, so the
                # whole role reads as one run-on sentence to a parser.
                out += [""] + [f"- {normalize_text(item_str(b))}" for b in bullets]
        return out

    def education():
        out = []
        for ed in _entries(profile, "education"):
            if not out:
                out += ["", f"## {h['education']}"]
            dates = _dates(ed, meta.get("language", "en"))
            # `location` mirrors experience: the schema advertises it (assets/profile.example.yaml)
            # and until now no renderer read it, so it was a field the docs promised and the
            # product silently discarded.
            meta_bits = " · ".join(b for b in
                                   [scalar_field(ed.get("location"), "education[].location"), dates] if b)
            line = f"**{_field_text(ed.get('degree'))}**, {_field_text(ed.get('institution'))}"
            if meta_bits:
                line += f"  \n_{meta_bits}_"
            out += ["", line]          # see the note in experience()
            details = detail_items(ed)
            if details:
                out += [""] + [f"- {d}" for d in details]
        return out

    def skills():
        groups = skill_groups(profile)
        if not groups:
            return []
        out = ["", f"## {h['skills']}"]
        for label, items in groups:
            lead = f"**{label}:** " if label is not None else ""
            out.append(f"- {lead}{', '.join(items)}")
        return out

    def projects():
        prs = _entries(profile, "projects")
        if not prs:
            return []
        out = ["", f"## {h['projects']}"]
        for pr in prs:
            header_parts = [f"**{_field_text(pr.get('name'))}**"]
            if pr.get("role"):
                header_parts.append(_field_text(pr["role"]))
            if pr.get("description"):
                header_parts.append(_field_text(pr["description"]))
            proj_line = " — ".join(header_parts)
            link_strs = [f"[{label}]({url})"
                         for label, url in (resolve_link(x) for x in as_list(pr.get("links")))
                         if url]
            if link_strs:
                proj_line += " — " + ", ".join(link_strs)
            out += ["", proj_line]     # see the note in experience()
            # Bullets are how every other entry carries its detail. Dropping
            # them silently cost a real run its strongest evidence.
            for line in as_list(pr.get("bullets")):
                out.append(f"- {normalize_text(item_str(line))}")
        return out

    def simple_list(key):
        items = as_list(profile.get(key))
        if not items:
            return []
        return ["", f"## {h[key]}"] + [f"- {normalize_text(item_str(it))}" for it in items]

    builders = {
        "summary": summary, "experience": experience, "internships": lambda: experience("internships"), "education": education,
        "skills": skills, "projects": projects,
        "publications": lambda: simple_list("publications"),
        "awards": lambda: simple_list("awards"),
        "certifications": lambda: simple_list("certifications"),
        "achievements": lambda: simple_list("achievements"),
        "board": lambda: simple_list("board"),
        "volunteer": lambda: simple_list("volunteer"),
    }
    for key in section_order(profile):
        lines += builders.get(key, list)()

    return "\n".join(lines) + "\n"


# ── docx renderer ─────────────────────────────────────────────────────────────

def _add_hyperlink(paragraph, text, url):
    """Append a real, clickable hyperlink run (blue + underlined) showing `text`."""
    from docx.oxml.ns import qn
    from docx.oxml.shared import OxmlElement

    r_id = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rpr.append(color)
    underline = OxmlElement("w:u"); underline.set(qn("w:val"), "single"); rpr.append(underline)
    run.append(rpr)
    t = OxmlElement("w:t"); t.text = text; run.append(t)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)
    return hyperlink


def render_docx(profile, out_path):
    _warn_unknown_market(profile)
    from docx import Document

    h = headings(profile)
    doc = Document()
    from docx.shared import Mm, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    meta = profile.get("meta", {}) or {}
    language = meta.get("language", "en")
    section = doc.sections[0]
    section.page_width, section.page_height = (
        (Mm(215.9), Mm(279.4)) if paper_for(meta) == "letterpaper"
        else (Mm(210), Mm(297)))
    section.top_margin, section.bottom_margin = Mm(10), Mm(12)
    section.left_margin = section.right_margin = Mm(12.7)
    width = section.page_width - section.left_margin - section.right_margin
    east_asia = meta.get("cjk_font") or {"zh": "SimSun", "ja": "Yu Mincho", "ko": "Malgun Gothic"}.get(language)
    body_size = 11
    for name, size, before, after in [("Normal", body_size, 0, 2), ("Title", 16, 0, 4),
                                      ("Heading 1", 11, 9, 3), ("List Bullet", body_size, 0, 2)]:
        style = doc.styles[name]
        style.font.name = meta.get("main_font") or "Times New Roman"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.font.bold = name in {"Title", "Heading 1"}
        # Theme faces override explicit names in Word/LibreOffice, including
        # English Title/Heading styles. Clear them for every language.
        fonts = style.element.get_or_add_rPr().rFonts
        for attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
            fonts.attrib.pop(qn("w:" + attr), None)
        if east_asia:
            fonts.set(qn("w:eastAsia"), east_asia)
        fmt = style.paragraph_format
        fmt.space_before, fmt.space_after = Pt(before), Pt(after)
        fmt.line_spacing = 1.0
        fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
    doc.styles["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bullet_format = doc.styles["List Bullet"].paragraph_format
    bullet_format.left_indent, bullet_format.first_line_indent = Pt(17), Pt(-17)
    # A paragraph border spans the text area; underlined spaces do not reliably
    # print to the right margin in Word. Clear inherited title decoration too.
    heading_pr = doc.styles["Heading 1"].element.get_or_add_pPr()
    for border in list(heading_pr.findall(qn("w:pBdr"))):
        heading_pr.remove(border)
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for key, value in {"val": "single", "sz": "4", "space": "1", "color": "000000"}.items():
        bottom.set(qn("w:" + key), value)
    borders.append(bottom)
    heading_pr.append(borders)
    for border in list(doc.styles["Title"].element.get_or_add_pPr().findall(qn("w:pBdr"))):
        border.getparent().remove(border)
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.comments = ""
    doc.add_heading(_field_text(meta.get("name")), level=0)
    if meta.get("headline"):
        doc.add_paragraph(_field_text(meta["headline"])).alignment = WD_ALIGN_PARAGRAPH.CENTER

    def entry_row(left, right="", right_bold=False):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT)
        paragraph.add_run(_field_text(left)).bold = True
        if right:
            paragraph.add_run("\t" + _field_text(right)).bold = right_bold
        return paragraph

    def bullet(text, emphasize=True):
        text = normalize_text(text)
        paragraph = doc.add_paragraph(style="List Bullet")
        # Only a short explicit label is emphasized; ordinary prose remains plain.
        match = re.match(r"^([^：:]{1,48}(?:：|: ))(.+)$", text) if emphasize else None
        if match:
            paragraph.add_run(match.group(1)).bold = True
            paragraph.add_run(match.group(2))
        else:
            paragraph.add_run(text)
        return paragraph

    # Contact line — plain runs for email/phone/location, real hyperlinks (with
    # the friendly label as visible text) for the rest.
    plain_bits = _contact_bits(profile)
    links = list(_contact_links(profile))
    if plain_bits or links:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        first = True
        for b in plain_bits:
            if not first:
                p.add_run(" · ")
            p.add_run(b)
            first = False
        for label, url in links:
            if not first:
                p.add_run(" · ")
            _add_hyperlink(p, label, url)
            first = False

    personal = [f"{label}: {value}" for label, value in personal_items(profile)]
    if personal:
        doc.add_paragraph(" · ".join(personal)).alignment = WD_ALIGN_PARAGRAPH.CENTER
    ph = photo_path(profile)
    if ph:
        try:
            from docx.shared import Inches
            doc.add_picture(str(ph), width=Inches(1.3))
        except Exception as exc:
            # Still not fatal — a photo is not worth losing the whole .docx over —
            # but no longer silent. `photo_path` has already rejected the formats
            # this is likely to be, so reaching here means something rarer, and a
            # candidate who believes their .docx has a photo when it does not is
            # the exact failure this used to produce.
            _warn_photo(ph, f"the photo {ph.name} could not be embedded in the "
                            f".docx ({type(exc).__name__}: {exc}). The .docx was "
                            f"written WITHOUT it")

    def summary():
        if summary_text(profile):
            doc.add_heading(h["summary"], level=1)
            doc.add_paragraph(summary_text(profile))

    def experience(section="experience"):
        exp = experience_entries(profile, section)
        if not exp:
            return
        doc.add_heading(experience_heading(profile, section), level=1)
        for e in exp:
            dates = _dates(e, language)
            entry_row(e.get("org", ""), dates)
            title = e.get("title", "")
            location = scalar_field(e.get("location"), "experience[].location")
            if title or location:
                entry_row(title, location)
            for b in as_list(e.get("bullets")):
                bullet(item_str(b))

    def education():
        edu = _entries(profile, "education")
        if not edu:
            return
        doc.add_heading(h["education"], level=1)
        for ed in edu:
            location = scalar_field(ed.get("location"), "education[].location")
            entry_row(ed.get("institution", ""), location, right_bold=True)
            degree, dates = ed.get("degree", ""), _dates(ed, language)
            if degree or dates:
                entry_row(degree, dates)
            for detail in detail_items(ed):
                bullet(detail, emphasize=False)

    def skills():
        groups = skill_groups(profile)
        if not groups:
            return
        doc.add_heading(h["skills"], level=1)
        for label, items in groups:
            p = doc.add_paragraph(style="List Bullet")
            if label is not None:
                p.add_run(f"{label}: ").bold = True
            p.add_run(", ".join(items))

    def projects():
        prs = _entries(profile, "projects")
        if not prs:
            return
        doc.add_heading(h["projects"], level=1)
        for pr in prs:
            p = doc.add_paragraph(style="List Bullet")
            p.add_run(_field_text(pr.get("name"))).bold = True
            text_parts = [_field_text(x) for x in [pr.get("role"), pr.get("description")] if x]
            if text_parts:
                p.add_run(": " + " — ".join(text_parts))
            resolved = [(label, url) for label, url in
                        (resolve_link(x) for x in as_list(pr.get("links"))) if url]
            for i, (label, url) in enumerate(resolved):
                p.add_run(" — " if i == 0 else ", ")
                _add_hyperlink(p, label, url)
            for line in as_list(pr.get("bullets")):
                doc.add_paragraph(normalize_text(item_str(line)), style="List Bullet 2")

    def simple_list(key):
        items = as_list(profile.get(key))
        if not items:
            return
        doc.add_heading(h[key], level=1)
        for it in items:
            doc.add_paragraph(normalize_text(item_str(it)), style="List Bullet")

    builders = {
        "summary": summary, "experience": experience, "internships": lambda: experience("internships"), "education": education,
        "skills": skills, "projects": projects,
        "publications": lambda: simple_list("publications"),
        "awards": lambda: simple_list("awards"),
        "certifications": lambda: simple_list("certifications"),
        "achievements": lambda: simple_list("achievements"),
        "board": lambda: simple_list("board"),
        "volunteer": lambda: simple_list("volunteer"),
    }
    for key in section_order(profile):
        builders.get(key, lambda: None)()

    for paragraph in doc.paragraphs:
        if paragraph.style.name == "List Bullet":
            # Direct indents take precedence over the numbering definition.
            paragraph.paragraph_format.left_indent = Pt(17)
            paragraph.paragraph_format.first_line_indent = Pt(-17)
    # Keep section headings with their content via Word's heading style; avoid
    # inferring pagination from run boldness (a skill row may also be all bold).
    save_clean_docx(doc, out_path)


# ── LaTeX helpers ─────────────────────────────────────────────────────────────

_LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    # Common Unicode punctuation that pdfLaTeX (Latin path) cannot typeset as-is —
    # map to LaTeX equivalents so an em-dash or a curly quote pasted from a CV
    # doesn't fail the compile. (XeLaTeX would accept the literals, but the mapped
    # forms render correctly there too.)
    "—": "---", "–": "--", "…": r"\ldots{}", " ": "~",
    "‘": "`", "’": "'", "“": "``", "”": "''",
}

# Whitespace sitting *between* two Han/kana characters is almost always an
# artifact of a YAML folded scalar (`>`), which joins wrapped lines with a space
# — but Chinese and Japanese have no inter-word spaces, so it shows up as a gap
# mid-word. Strip it.
#
# HANGUL IS DELIBERATELY ABSENT from this class, and that is the whole point of
# spelling the blocks out. Korean 띄어쓰기 makes inter-word spacing mandatory
# orthography, not a folded-scalar artifact, so stripping it turns
# `데이터 엔지니어` into `데이터엔지니어` — which reads to a Korean
# recruiter roughly the way `dataengineer` reads to an English one. The previous
# range included Hangul twice: `가-히` named the syllables outright, and
# U+3000-U+9FFF additionally covers U+3130-U+318F, the Hangul compatibility jamo.
# One block per script is the point — the next script added has to be a deliberate
# answer to "does this script use inter-word spaces?", which is the question a
# catch-all range never forces anyone to ask.
#
# `_has_cjk` keeps Hangul on purpose: it answers the *font* question (does this
# document need xeCJK and an installed CJK font), and Korean genuinely does.
_CJK_NO_INTERWORD_SPACE = (
    "\u3000-\u312f"   # CJK punctuation, hiragana, katakana, bopomofo
    "\u3190-\u9fff"   # kanbun → CJK unified  (skips U+3130-318F Hangul jamo)
    "\uf900-\ufaff"   # CJK compatibility ideographs
)
_CJK_GAP_RE = re.compile(
    r"(?<=[%s])[ \t]+(?=[%s])"
    % (_CJK_NO_INTERWORD_SPACE, _CJK_NO_INTERWORD_SPACE))


_SHAPE_WARNED = []


def reset_shape_warnings():
    _SHAPE_WARNED.clear()


def scalar_field(value, where: str) -> str:
    """A field that must be one string, or "" plus one loud warning.

    `location` is the field that made this necessary: SKILL.md typed it BOTH as a
    scalar and as `{city, country, arrangement}` for months, so profiles carrying
    the mapping exist. Rendering `str(mapping)` put a literal
    `{'city': 'Leeds', 'country': 'UK'}` on a CV — quietly wrong output in the one
    artifact an employer reads, which is worse than no output at all. Omit and say
    so, rather than print a Python repr and hope someone notices.
    """
    if value is None:
        return ""
    if isinstance(value, (str, int, float)):
        return str(value).strip()
    key = f"{where}:{type(value).__name__}"
    if key not in _SHAPE_WARNED:
        _SHAPE_WARNED.append(key)
        print(f"WARNING: {where} is a {type(value).__name__}, not one string — "
              f"omitted from the rendered CV rather than printed as a Python "
              f"value. `location` is a scalar string, the posting's own location "
              f"text (see SKILL.md's extraction field table).", file=sys.stderr)
    return ""


_PRESENT = {"en": "Present", "zh": "至今", "ja": "現在", "ko": "현재",
            "es": "Actualidad", "de": "heute", "nl": "heden", "fr": "présent",
            "it": "presente"}


def _date_end(item, language):
    end = _field_text(item.get("end"))
    if end.casefold() in {"present", "current", "now", "ongoing"}:
        return _PRESENT.get(str(language).lower().replace("_", "-").split("-")[0], end)
    return end


def _dates(item, language="en") -> str:
    """`start – end`, with a missing half omitted rather than printed.

    `f"{item.get('start','')} - {item.get('end','')}"` renders an explicit
    `end: null` as the literal string "None", so a CV said the candidate worked
    from 2020 to None — in md, docx AND pdf. `.get(k, "")` only covers a MISSING
    key; a key present and null still yields None, and profiles are
    model-authored YAML where `end: null` is the natural way to write "current".
    """
    start = _field_text(item.get("start"))
    end = _date_end(item, language)
    return " – ".join(b for b in (start, end) if b)


def _dates_tex(item, language="en") -> str:
    """The same, with LaTeX's en dash."""
    start = _field_text(item.get("start"))
    end = _date_end(item, language)
    return " -- ".join(b for b in (start, end) if b)


def normalize_text(text):
    """Clean a user-text string before rendering: drop folded-scalar spaces that
    landed between CJK characters. Format-agnostic, so all renderers can use it."""
    if text is None:
        return ""
    return _CJK_GAP_RE.sub("", str(text))


# A token at least this long has a real chance of not fitting the column; below
# it the inserted break points would be noise in the source for no benefit. The
# measured overflows on an ordinary academic profile came from DOIs of 30-40
# characters, so this sits well under the shortest one that actually broke.
_LONG_TOKEN_CHARS = 24
# Break AFTER these, which is where a reader expects a URL or path to wrap. `\_`
# is matched (not a bare `_`) because escaping has already run by this point.
# Break AFTER a separator — but never in the middle of a RUN of them. `//` in a
# URL and the `---`/`--` that `_LATEX_REPLACEMENTS` produces for em/en dashes are
# single typographic units: breaking inside them shipped `https:/` at a line end
# and decomposed an em dash into three loose hyphens, both silently, in a PDF no
# gate inspects. `(?![/\-.=])` is what makes the run atomic.
_BREAK_AFTER_RE = re.compile(r"(/+|\\_|-+|\.|=|&amp;|\?)(?![/\-.=])")


def _allow_breaks(escaped):
    """Insert `\\allowbreak{}` after the separators inside long unspaced tokens.

    `\\sloppy` and `\\emergencystretch` (see `latex_preamble`) fix an overfull line
    whenever the line has some break point on it. A bare DOI or repo URL is the
    case where it has none: TeX cannot hyphenate a token it has no pattern for,
    so it sets the whole thing past the right margin. Measured on a profile with
    three ordinary publication DOIs: one line 86pt over, which put four digits of
    the DOI off the edge of the sheet, and `check_pages` passed it.

    Scoped to long tokens so an ordinary hyphenated word, a date, or a decimal is
    untouched — inserting break points everywhere would let `co-` / `ordinator`
    split across lines in a job title, which is a different kind of wrong.
    """
    parts = re.split(r"(\s+)", escaped)
    for i, chunk in enumerate(parts):
        if chunk.strip() and len(chunk) >= _LONG_TOKEN_CHARS:
            parts[i] = _BREAK_AFTER_RE.sub(r"\1\\allowbreak{}", chunk)
    return "".join(parts)


def latex_escape(text, keep_cjk_spaces=False):
    """`text` as LaTeX source.

    `keep_cjk_spaces` is for a person's NAME. `normalize_text` strips a space
    between two Han/kana characters because a folded YAML scalar puts one there,
    and a name is never a folded scalar: `山田 太郎` is how a Japanese name is
    written, the .md and .docx kept it, and only the PDF — the copy the employer
    opens — printed `山田太郎`. A Chinese name normally has no space, so nothing
    changes for one that does not; one written with a space keeps it in all three
    formats instead of in two.
    """
    if text is None:
        return ""
    out = []
    for ch in (str(text) if keep_cjk_spaces else normalize_text(text)):
        out.append(_LATEX_REPLACEMENTS.get(ch, ch))
    return _allow_breaks("".join(out))


# Standard install locations searched when an engine isn't on PATH. A
# non-login shell (which is what the renderer often runs inside) frequently
# lacks Homebrew's /opt/homebrew/bin or the MacTeX bin on PATH, so a plain
# shutil.which misses a perfectly good tectonic/xelatex. We fall back to these.
_ENGINE_DIRS = ["/opt/homebrew/bin", "/usr/local/bin", "/Library/TeX/texbin",
                "~/.cargo/bin", "/usr/bin", "/bin"]


def find_latex_engine(cjk=False):
    """Locate a usable LaTeX engine, returning its path (or bare name).

    A CJK CV must be typeset by XeTeX so
    that ``xeCJK`` and system CJK fonts work — ``pdflatex`` cannot do it. So for
    CJK we look only for ``xelatex``/``tectonic`` (tectonic is
    XeTeX-based and handles ``xeCJK``). For Latin scripts, ``pdflatex`` is fine
    and ``tectonic`` is preferred for its self-contained package handling.
    Callers detect the engine *type* from the basename, so a returned absolute
    path works the same as a bare name.
    """
    candidates = ("xelatex", "tectonic") if cjk else ("tectonic", "xelatex", "lualatex", "pdflatex")
    for engine in candidates:
        found = shutil.which(engine)
        if found:
            return found
        for d in _ENGINE_DIRS:
            cand = pathlib.Path(d).expanduser() / engine
            if cand.is_file():
                return str(cand)
    return None


def _engine_cmd(engine, tex_path, out_dir):
    """argv to compile `tex_path` into `out_dir` with `engine`.

    Dispatch on the BASENAME, never on the whole string: find_latex_engine
    returns an absolute path when the engine is not on PATH (measured on this
    machine: '/opt/homebrew/bin/tectonic'), and `engine == "tectonic"` is False
    for it. That comparison shipped in render_letter.py and produced a
    pdflatex-shaped argv handed to tectonic — every letter PDF failed while
    cv.pdf built in the same run, with the whole test suite green.

    One helper, both renderers. Two call sites cannot drift if there is one.
    """
    engine, tex_path, out_dir = str(engine), str(tex_path), str(out_dir)
    if pathlib.Path(engine).stem == "tectonic":
        return [engine, tex_path, "--outdir", out_dir]
    return [engine, "-interaction=nonstopmode", "-output-directory", out_dir, tex_path]


_UNICODE_ENGINES = ("tectonic", "xelatex", "lualatex")


def _is_unicode_engine(engine):
    """True when `engine` reads its input as Unicode and wants `fontspec`.

    tectonic is XeTeX-based, so it belongs here with xelatex and lualatex; only
    pdflatex wants the 8-bit `inputenc`/`fontenc` preamble. `None` — no engine
    installed — resolves to True, because the `.tex` we leave behind in that case
    is the one `modes/apply.md` tells the user to compile after installing
    **tectonic**; handing them a pdfLaTeX preamble to compile with the engine we
    just recommended is how this went wrong in the first place.

    Dispatch on the BASENAME, for the same reason `_engine_cmd` does:
    find_latex_engine returns an absolute path when the engine is not on PATH.
    """
    if engine is None:
        return True
    return pathlib.Path(str(engine)).stem in _UNICODE_ENGINES


def _has_cjk(text):
    """True if text contains CJK / Hangul / Thai characters.

    Narrow on purpose, and NOT the test for "needs a Unicode font" — that is
    `_needs_unicode_font`. What this answers is the narrower question "does this
    document need the ``xeCJK`` package and an installed CJK font on top of a
    Unicode engine", which really is script-specific: xeCJK exists to fix CJK
    line-breaking and inter-script spacing, and pdflatex cannot typeset these
    scripts at any font. Do not reach for this function to decide anything about
    encodings or Latin fonts — see the comment on `_needs_unicode_font`.
    """
    return any("　" <= ch <= "鿿" or "가" <= ch <= "힣"
               or "฀" <= ch <= "๿" for ch in text)


def _needs_unicode_font(text):
    """True if text contains any character above U+00FF.

    A THRESHOLD, not a script list, and that distinction is the whole bug this
    function was added to close. `_has_cjk` used to be asked "does this need the
    Unicode/fontspec path?", and because it enumerates scripts — CJK, Hangul,
    Thai — everything in Latin Extended-A and beyond fell through to the 8-bit
    T1 path: `Łukasz Wójcik` compiled, exit 0, and reached the recruiter as
    `ukasz Wójcik`. That is Polish, Czech, Slovak, Croatian, Hungarian, Turkish,
    Romanian and Latvian names and employers, in exactly the nl/de/uk markets
    this skill is built for. Enumerating scripts is what produced it; the next
    script would produce it again, so the test is a boundary instead: U+00FF is
    where an 8-bit font's coverage stops being something you can assume.
    """
    return any(ord(ch) > 0xFF for ch in text)


def profile_has_cjk(profile):
    """Whether any rendered text in the profile is CJK/Hangul/Thai. Drives the
    xeCJK/CJK-font half of the preamble and the engine requirement. A flat string
    dump is enough — we only need to know whether such characters appear."""
    return _has_cjk(str(profile))


def profile_needs_unicode_font(profile):
    """Whether any rendered text in the profile sits above U+00FF."""
    return _needs_unicode_font(str(profile))


# The engine prints one of these per dropped glyph and still exits 0 — so this
# is a *warning* that destroys the artifact. Two dialects, both covered:
#   XeTeX/tectonic:  `Missing character: There is no Ł (U+0141) in font [lmroman10-regular]…`
#   pdfTeX/8-bit:    `Missing character: There is no Ł ("141) in font ec-lmr10!`
_MISSING_CHAR_RE = re.compile(
    r"Missing character: There is no (.+?) in font ([^\n!]*)")
# Measured: tectonic 0.16.9 writes the character itself as U+FFFD U+FFFD in its
# own log — `There is no �� ("141)` — so the character is already lost
# before this code sees it and only the codepoint is trustworthy. Read that, and
# rebuild the character from it, or the message names the dropped glyph as "??".
_CODEPOINT_RE = re.compile(r'\((?:U\+|")([0-9A-Fa-f]{2,6})\)')


def missing_characters(log):
    """Every distinct `Missing character` the engine reported, in order.

    The information was always there — `render_pdf` captured the engine output
    and threw it away, which is why a CV whose name had lost a letter reported
    success and printed "Wrote cv.pdf". Returns a list of
    "U+0141 'Ł' in font ec-lmbx12" strings.
    """
    seen, out = set(), []
    for described, font in _MISSING_CHAR_RE.findall(log or ""):
        m = _CODEPOINT_RE.search(described)
        if m:
            code = int(m.group(1), 16)
            try:
                what = f"U+{code:04X} {chr(code)!r}"
            except ValueError:
                what = f"U+{code:04X}"
        else:
            what = described.strip()
        item = f"{what} in font {font.strip().rstrip(':;')}"
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


_OVERFULL_RE = re.compile(r"Overfull \\hbox \(([0-9]+(?:\.[0-9]+)?)pt too wide\)")

# The geometry margin latex_preamble sets by default. An overfull box narrower
# than this still lands on the paper (inside the margin): ugly, and worth saying
# so, but the reader can read it. One WIDER than the margin has run off the edge
# of the sheet, and the characters past the edge are simply gone from the printed
# and on-screen page — the same class of loss as a dropped glyph, arrived at from
# the other direction, so it gets the same treatment.
_PT_PER_CM = 28.4527559
_PT_PER_UNIT = {"cm": _PT_PER_CM, "mm": _PT_PER_CM / 10.0, "in": 72.27,
                "pt": 1.0}
OFF_PAGE_PT = 2.0 * _PT_PER_CM          # the CV default; letters use 2.5cm
_MARGIN_RE = re.compile(r"margin=\s*([0-9.]+)\s*(cm|mm|in|pt)\b")


def off_page_pt(tex: str = "") -> float:
    """How far a line must overflow before it is off the SHEET, for this document.

    Read from the document's own geometry rather than assumed, because the two
    renderers do not share a margin: render_cv sets 2cm and render_letter sets
    2.5cm. With the threshold hard-coded to 2cm there was a 14.2pt band in which
    a letter whose text is entirely on the paper was declared "off the edge of
    the page" and its PDF deleted — a correct artifact destroyed by the gate
    meant to protect it.
    """
    found = _MARGIN_RE.search(tex or "")
    if not found:
        return OFF_PAGE_PT
    try:
        return float(found.group(1)) * _PT_PER_UNIT[found.group(2)]
    except (ValueError, KeyError):
        return OFF_PAGE_PT


def overfull_boxes(log):
    """Every `Overfull \\hbox` the engine reported, widest first, in points.

    The engine already writes this into the same log string `missing_characters`
    reads, and it was already being captured and dropped — the identical mistake,
    on the identical data. A bare DOI, a repo URL, a long file path or a German/
    Dutch compound is one unbreakable token, and when it does not fit, TeX does
    not shrink it: it prints it past the right edge of the text block, warns, and
    exits 0. Measured on a three-publication academic profile: overflows of 28,
    50 and 79pt, and one of 86pt that put four digits of a DOI off the sheet.
    """
    return sorted((float(pt) for pt in _OVERFULL_RE.findall(log or "")), reverse=True)


_OVERFULL_AT_RE = re.compile(
    r"Overfull \\hbox \(([0-9]+(?:\.[0-9]+)?)pt too wide\) in \w+ at lines? (\d+)")


def overfull_source_lines(log, min_pt=0.0):
    """The `.tex` line numbers of the overfull boxes at least `min_pt` wide.

    The engine names them ("in paragraph at lines 22--22"), and naming them is
    the difference between "shorten something" and "shorten this": the offending
    line is the entry-header row as often as a DOI."""
    return sorted({int(line) for pt, line in _OVERFULL_AT_RE.findall(log or "")
                   if float(pt) >= min_pt})


# Cross-platform CJK font fallback. xeCJK needs a real installed CJK font, and
# the right name differs per OS (macOS PingFang, Windows YaHei/Malgun, Linux
# Noto). We emit a nested \IfFontExistsTF chain that picks the first font that
# is actually installed, so the same .tex compiles on a typical mac, Windows or
# Linux box without hand-editing. `meta.cjk_font` jumps the queue. If none is
# found, xeCJK falls back to its own default (and may error — the .tex is still
# delivered for the user to point at a font they have).
# Keyed by `meta.language`, because a flat list silently resolves to the wrong
# script. The old list was Chinese-first and consulted no language at all, so on
# a stock macOS the Korean chain reached PingFang SC first — a font with no
# Hangul — and every Hangul codepoint was dropped, which `compile_latex` then
# correctly refused, leaving `ko` with NO PDF at all despite
# `references/cv-craft.md:104` promising one wherever a CJK font is installed.
# (Measured: `\setCJKmainfont{Apple SD Gothic Neo}` typesets the same profile
# perfectly, so the font was there all along; only the ordering was wrong.)
# Japanese resolved to a Chinese face, which is subtler: the shared kanji differ
# in stroke shape and a Japanese reader sees it immediately.
_CJK_FONTS_BY_LANG = {
    "zh": ["SimSun", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC",
           "Hiragino Sans GB", "Microsoft YaHei"],
    "ja": ["Noto Sans CJK JP", "Source Han Sans JP", "Hiragino Sans W3",
           "Hiragino Kaku Gothic ProN", "Hiragino Sans",
           "Yu Gothic", "MS Gothic"],
    "ko": ["Noto Sans CJK KR", "Source Han Sans KR", "Apple SD Gothic Neo",
           "Malgun Gothic", "NanumGothic"],
}
# Every font, in the historical zh → ja → ko order. Used as the tail after the
# language's own fonts, so an unset or non-CJK `meta.language` behaves exactly as
# it did before and a CV that mixes scripts still finds *something*.
_CJK_FONT_FALLBACKS = [f for lang in ("zh", "ja", "ko")
                       for f in _CJK_FONTS_BY_LANG[lang]]


def _cjk_fonts_for(meta):
    """The CJK font chain for this profile: its own language's faces first."""
    lang = str((meta or {}).get("language") or "").lower().replace("_", "-")
    preferred = _CJK_FONTS_BY_LANG.get(lang.split("-")[0], [])
    return preferred + [f for f in _CJK_FONT_FALLBACKS if f not in preferred]


def _font_chain(fonts, setter):
    """A nested `\\IfFontExistsTF` chain: the first font actually installed wins,
    and the innermost branch is empty, leaving the engine's own default.

    `\\IfFontExistsTF` is used rather than a bare `\\setmainfont`/`\\setCJKmainfont`
    because naming a font that is not installed is a FATAL fontspec error, not a
    fallback — measured under tectonic 0.16.9, `\\setmainfont{Latin Modern Roman}`
    halts with "The font ... cannot be found" even though Latin Modern is the very
    font the engine is about to use by default. A `.tex` is a deliverable that gets
    recompiled on other machines, so it must not name a font it cannot check for.

    One chain builder, two callers (main font and CJK font), for the reason
    `_engine_cmd` gives: two copies is two things to be wrong.
    """
    setup = "{}"
    for f in reversed(list(fonts)):
        setup = r"\IfFontExistsTF{%s}{\%s{%s}}{%s}" % (f, setter, f, setup)
    return setup


def _cjk_font_setup(meta):
    fonts = [str(meta["cjk_font"])] if meta.get("cjk_font") else []
    return _font_chain(fonts + _cjk_fonts_for(meta), "setCJKmainfont")


def _main_font_setup(meta):
    """Prefer the client English typeface; explicit profile fonts still win."""
    fonts = [str(meta["main_font"])] if meta.get("main_font") else ["Times New Roman"]
    return _font_chain(fonts, "setmainfont")


# ---------------------------------------------------------------------------
# Paper size. Not the same axis as the CV-convention cluster, and reusing the
# cluster would have been wrong: Cluster 1 is US/CA/UK/IE/AU/NZ, but the UK,
# Ireland, Australia and New Zealand all print on A4. Letter is a North
# American convention, not an Anglophone one.
#
# Only the two markets this skill has convention tables and cluster codes for
# are asserted here. Other Letter-using countries exist; naming them from memory
# in a file that is meant to be checkable is exactly the kind of unsourced claim
# this skill bans elsewhere, so they set `meta.paper` instead.
_LETTER_CODES = {"us", "usa", "ca", "can"}
_LETTER_NAMES = {"united states of america", "united states", "u s a", "u s",
                 "america", "canada"}
_LETTER_CJK = ("美国", "美國", "加拿大")
PAPERS = {"a4": "a4paper", "letter": "letterpaper"}


def paper_for(meta) -> str:
    """The LaTeX documentclass paper option for this profile.

    `meta.paper` wins when set — it is the escape hatch for Mexico, the
    Philippines and anywhere else that prints Letter, without this module
    claiming a list it has not verified. Otherwise US and Canada get Letter and
    everything else A4, which was hard-coded for every market until 2026-09-05:
    every US and Canadian CV this skill has ever produced came out on A4.
    """
    meta = meta if isinstance(meta, dict) else {}
    declared = str(meta.get("paper") or "").strip().lower()
    if declared:
        if declared not in PAPERS:
            raise ValueError(
                f"meta.paper must be one of {sorted(PAPERS)}, got {declared!r}")
        return PAPERS[declared]
    return PAPERS["letter"] if north_america(meta.get("target_market")) else PAPERS["a4"]


def north_america(market) -> bool:
    """Whether `market` names the US or Canada.

    Extracted from `paper_for` so the page-length gate can ask the same
    question. cv-craft.md gives US/CA their own résumé length (1 page, 2 only
    at 10+ years), which is stricter than the generic career-stage ladder, and
    a second hand-rolled country list would drift from this one.
    """
    text = unicodedata.normalize("NFKC", str(market or "")).lower()
    if any(name in text for name in _LETTER_CJK):
        return True
    for seg in _market_segments(market):
        if seg in _LETTER_CODES or seg in _LETTER_NAMES:
            return True
        words = seg.split()
        for n in range(len(words), 0, -1):
            for i in range(len(words) - n + 1):
                if " ".join(words[i:i + n]) in _LETTER_NAMES:
                    return True
    return False


def latex_preamble(engine=None, cjk=False, meta=None, margin="2cm"):
    """The documentclass + encoding/font lines, chosen by ENGINE, not by content.

    This is the fix for the defect that shipped a recruiter a CV missing letters
    out of the candidate's own name. The preamble has to match the engine that
    will compile it, because that is what decides how the bytes are read:

      * tectonic / xelatex / lualatex read the file as Unicode and hand each
        codepoint straight to the font, so they need **fontspec**. Given
        `inputenc`+`fontenc` instead they load an 8-bit T1 font, silently drop
        every glyph it lacks, print `Missing character`, and exit 0.
      * pdflatex needs **inputenc + fontenc**, and with them genuinely does
        handle Latin Extended-A (inputenc composes `Ś` as `\\'S`). Emitting
        fontspec for pdflatex would trade a silent glyph drop for a hard compile
        failure, which is why this is not decided by looking at the text.

    `find_latex_engine` prefers tectonic and `modes/apply.md` tells the user to
    install it, so the Unicode branch is the one taken on a normal machine — and
    it is also what an unknown engine (`None`) gets, since the `.tex` left behind
    when nothing is installed is meant to be compiled with tectonic later.

    One preamble builder, both renderers: render_letter.py had its own copy of
    the pdfLaTeX lines and therefore its own copy of this bug.
    """
    meta = meta or {}
    lines = [r"\documentclass[11pt,%s]{article}" % paper_for(meta)]
    if _is_unicode_engine(engine):
        lines.append(r"\usepackage{fontspec}")
        main = _main_font_setup(meta)
        if main != "{}":
            lines.append(main)
        if cjk:
            # `CJKspace` is not optional here. xeCJK defaults to CJKspace=false,
            # which DISCARDS whitespace adjacent to a CJK glyph at typeset time —
            # so removing Hangul from `_CJK_GAP_RE` (which fixed .md and .docx)
            # left the PDF still reading `데이터엔지니어`. Korean 띄어쓰기 is
            # mandatory orthography, and the PDF is the artifact the recruiter
            # opens. Harmless for zh/ja: `normalize_text` has already removed
            # their folded-scalar spaces before the text reaches LaTeX, so there
            # is nothing left for CJKspace to preserve.
            lines += [r"\usepackage[CJKspace]{xeCJK}", _cjk_font_setup(meta)]
    else:
        lines += [r"\usepackage[utf8]{inputenc}", r"\usepackage[T1]{fontenc}"]
    lines.append(r"\usepackage[margin=%s]{geometry}" % margin)
    # Line-breaking safety net, and it is a net rather than one setting because
    # the failure has two halves. TeX does not shrink a line that is too wide: it
    # sets it past the right edge, warns `Overfull \hbox`, and exits 0.
    #   * `\sloppy` + `\emergencystretch` let it stretch inter-word space instead,
    #     which fixes every case where SOME break point exists on the line.
    #   * Neither can break a single token with no break point in it — a bare DOI,
    #     a repo URL, a Dutch/German compound. That half is `_allow_breaks` in
    #     `latex_escape`, which inserts the break opportunities.
    # `url` is loaded for `\UrlBreaks`-style tolerance and because it is the
    # package anything later wanting real `\url{}` handling will expect.
    lines += [r"\usepackage[hyphens]{url}",
              r"\setlength{\emergencystretch}{3em}",
              r"\sloppy"]
    return lines


# ── LaTeX renderer ────────────────────────────────────────────────────────────


# A two-column entry heading, and the reason it is neither a bare `\hfill` nor a
# pair of fixed fractions.
#
# `\textbf{title}, org \hfill meta\\` reaches the right margin only while the whole
# thing fits on one line. Let the title grow and the line wraps; `\hfill` then
# collapses at the break, so the organisation and the location collide and the
# dates orphan onto a line of their own. Measured on a real CV:
#     "... - Cum Laude, Leiden University  Leiden, NL"
#     "2021-09 - 2023-02"
#
# Fixed fractions fix that and cost more than they save. At 0.60/0.38 the dates
# stayed put and headings that had fitted on one line began wrapping three ways
# ("PhD Researcher - Deep Learning for Cardiac MRI / Reconstruction, Leiden
# University Medical Center / (LUMC)"), because the right column was reserved at
# its worst case on every row.
#
# So the right column takes its NATURAL width and the left takes whatever is
# left. `\setbox` measures the metadata, `\dimexpr` subtracts it, and the title
# gets the largest column it can have on that particular row. The metadata is a
# single box, so it cannot wrap or be split from its heading. `\smallskip` is
# what separates one entry from the next: entries used to be joined by a bare
# `\\`, which is a line break, not a gap, so four jobs read as one block.
#
# When the metadata is too wide to share the row — the title would get less than
# `_ENTRY_MIN_LEFT` of the line — it moves to a line of its own under the title,
# still flush right, and may wrap there. This used to CLAMP the title column to
# the floor instead and set the unbreakable metadata box beside it anyway, so the
# row ran past the margin: "Amsterdam, North Holland, Netherlands (Hybrid)" put
# "Present" 4mm from the paper edge (a WARNING, exit 0), and a longer German
# location ran off the sheet entirely (TEXT_OFF_PAGE, no PDF). Rows that fit are
# laid out exactly as before; only the rows that used to overflow change.
_ENTRY_GAP = "1em"          # minimum space between the two columns
_ENTRY_MIN_LEFT = "0.45"    # below this share of the line, the metadata gets its own line


def _tex_entry_heading(left, right):
    """One entry heading: `left` wraps into the room that is actually left over,
    `right` keeps its natural width at the margin — or, when that would leave the
    title less than `_ENTRY_MIN_LEFT` of the line, goes on the next line."""
    if not right:
        return r"\smallskip\noindent %s\par" % left
    return (
        r"\smallskip\noindent"
        r"\setbox0=\hbox{%(right)s}"
        r"\dimen0=\dimexpr\linewidth-\wd0-%(gap)s\relax"
        r"\ifdim\dimen0<%(min)s\linewidth "
        r"\parbox[t]{\linewidth}{\raggedright %(left)s}\par\nobreak"
        r"{\raggedleft %(right)s\par}"
        r"\else "
        r"\parbox[t]{\dimen0}{\raggedright %(left)s}"
        r"\hfill\box0\par"
        r"\fi"
        % {"left": left, "right": right, "gap": _ENTRY_GAP, "min": _ENTRY_MIN_LEFT})


def build_latex(profile, cjk=None, engine=None, asset_dir=None, asset_stem="cv"):
    """Assemble the LaTeX source.

    `engine` is the engine that will compile this file, and it selects the
    encoding/font half of the preamble — see `latex_preamble` for why that has to
    be an engine decision and not a content one. `None` means "unknown", which
    resolves to the Unicode/fontspec preamble because tectonic is what
    `find_latex_engine` prefers and what `modes/apply.md` tells the user to
    install. `render_pdf` always passes the engine it actually resolved.

    `cjk` adds xeCJK and a system CJK font on top: that part IS content-driven,
    because xeCJK exists for CJK line-breaking and needs a CJK font installed.
    When `cjk` is None we auto-detect from the profile content.
    """
    _warn_unknown_market(profile)
    e = latex_escape
    # Escape headings for LaTeX up front: section labels can legitimately contain
    # LaTeX-special characters — the regulated-profession recipes use headers like
    # "Licenses & Certifications" and "Board & Advisory", and a raw "&" is a fatal
    # alignment-tab error. (Markdown/docx use the unescaped headings.)
    h = {k: e(v) for k, v in headings(profile).items()}
    meta = profile.get("meta", {}) or {}
    if cjk is None:
        cjk = profile_has_cjk(profile)
    preamble = latex_preamble(engine=engine, cjk=cjk, meta=meta, margin="2cm")
    parts = preamble + [
        r"\usepackage{enumitem}",
        r"\usepackage[hidelinks]{hyperref}",
        r"\usepackage{graphicx}",
        r"\setlist{nosep,leftmargin=*}",
        r"\pagestyle{empty}",
        r"\begin{document}",
        r"\begin{center}",
    ]
    # A passport-style photo above the name is the common layout for the EU/Asia
    # photo-CV; suppressed entirely for Cluster-1 targets by photo_path().
    ph = photo_path(profile)
    if ph:
        parts.append(r"\includegraphics[height=3cm]{%s}\\[6pt]"
                     % _photo_include_name(ph, asset_dir, asset_stem))
    parts.append(r"{\LARGE \textbf{%s}}\\[2pt]"
                 % e(meta.get("name", ""), keep_cjk_spaces=True))
    if meta.get("headline"):
        parts.append(r"{\large %s}\\[2pt]" % e(meta["headline"]))

    # Contact line — \textbullet{} separators; links via \href{url}{Label}.
    contact_parts = [e(b) for b in _contact_bits(profile)]
    contact_parts += [r"\href{%s}{%s}" % (url, e(label))
                      for label, url in _contact_links(profile)]
    if contact_parts:
        parts.append(r" \textbullet{} ".join(contact_parts))
    personal_parts = [e(f"{label}: {value}") for label, value in personal_items(profile)]
    if personal_parts:
        parts.append(r"\\[2pt]" + r" \textbullet{} ".join(personal_parts))
    parts.append(r"\end{center}")

    def summary():
        if summary_text(profile):
            parts.extend([r"\section*{%s}" % h["summary"], e(summary_text(profile))])

    def experience(section="experience"):
        exp = experience_entries(profile, section)
        if not exp:
            return
        parts.append(r"\section*{%s}" % e(experience_heading(profile, section)))
        for ex in exp:
            dates = _dates_tex(ex, meta.get("language", "en"))
            # `location` is on the right with the dates, matching the `location ·
            # dates` line render_markdown and render_docx already emit. It used
            # to be dropped here and only here, so a candidate whose two jobs
            # were in different cities kept that in the .md the judges read and
            # lost it from the PDF the employer opens — the whole class of defect
            # this file's audit was about.
            bits = [b for b in (scalar_field(ex.get("location"), "experience[].location"), dates) if b]
            # `\textbullet{}` is this file's separator, and it has to be joined
            # AFTER escaping: a raw U+00B7 does not typeset on the T1 pdflatex
            # path, which is exactly what test_latex_no_raw_middot pins.
            right = r" \textbullet{} ".join(e(b) for b in bits)
            parts.append(_tex_entry_heading(
                r"\textbf{%s}, %s" % (e(ex.get("title", "")), e(ex.get("org", ""))),
                right))
            bullets = as_list(ex.get("bullets"))
            if bullets:
                parts.append(r"\begin{itemize}")
                parts.extend(r"\item %s" % e(item_str(b)) for b in bullets)
                parts.append(r"\end{itemize}")

    def education():
        edu = _entries(profile, "education")
        if not edu:
            return
        parts.append(r"\section*{%s}" % h["education"])
        for ed in edu:
            dates = _dates_tex(ed, meta.get("language", "en"))
            bits = [b for b in (scalar_field(ed.get("location"), "education[].location"), dates) if b]
            right = r" \textbullet{} ".join(e(b) for b in bits)
            parts.append(_tex_entry_heading(
                r"\textbf{%s}, %s" % (e(ed.get("degree", "")), e(ed.get("institution", ""))),
                right))
            details = detail_items(ed)
            if len(details) == 1:
                parts.append(e(details[0]) + r"\\")
            elif details:
                parts.append(r"\begin{itemize}")
                parts.extend(r"\item %s" % e(d) for d in details)
                parts.append(r"\end{itemize}")

    def skills():
        groups = skill_groups(profile)
        if not groups:
            return
        parts.append(r"\section*{%s}" % h["skills"])
        for label, items in groups:
            lead = r"\textbf{%s:} " % e(label) if label is not None else ""
            parts.append(r"%s%s\\" % (lead, e(", ".join(items))))

    def projects():
        prs = _entries(profile, "projects")
        if not prs:
            return
        parts.append(r"\section*{%s}" % h["projects"])
        for pr in prs:
            line_parts = [r"\textbf{%s}" % e(pr.get("name", ""))]
            if pr.get("role"):
                line_parts.append(e(pr["role"]))
            if pr.get("description"):
                line_parts.append(e(pr["description"]))
            proj_line = ", ".join(line_parts)
            link_strs = [r"\href{%s}{%s}" % (url, e(label))
                         for label, url in (resolve_link(x) for x in as_list(pr.get("links")))
                         if url]
            if link_strs:
                proj_line += " --- " + ", ".join(link_strs)
            parts.append(proj_line + r"\\")
            lines = as_list(pr.get("bullets"))
            if lines:
                parts.append(r"\begin{itemize}[leftmargin=*,itemsep=1pt,topsep=2pt]")
                parts.extend(r"\item %s" % e(normalize_text(item_str(line))) for line in lines)
                parts.append(r"\end{itemize}")

    def simple_list(key):
        items = as_list(profile.get(key))
        if not items:
            return
        parts.append(r"\section*{%s}" % h[key])
        parts.append(r"\begin{itemize}")
        parts.extend(r"\item %s" % e(item_str(it)) for it in items)
        parts.append(r"\end{itemize}")

    builders = {
        "summary": summary, "experience": experience, "internships": lambda: experience("internships"), "education": education,
        "skills": skills, "projects": projects,
        "publications": lambda: simple_list("publications"),
        "awards": lambda: simple_list("awards"),
        "certifications": lambda: simple_list("certifications"),
        "achievements": lambda: simple_list("achievements"),
        "board": lambda: simple_list("board"),
        "volunteer": lambda: simple_list("volunteer"),
    }
    for key in section_order(profile):
        builders.get(key, lambda: None)()

    parts.append(r"\end{document}")
    return "\n".join(parts) + "\n"


# ── PDF renderer ──────────────────────────────────────────────────────────────

# Why a PDF was not produced.
NO_ENGINE, UNSUPPORTED_SCRIPT, COMPILE_FAILED, MISSING_CHARACTERS, TEXT_OFF_PAGE = (
    "NO_ENGINE", "UNSUPPORTED_SCRIPT", "COMPILE_FAILED", "MISSING_CHARACTERS",
    "TEXT_OFF_PAGE")

# The first two are limitations of the machine or the template that modes/apply.md
# documents and expects the run to continue past on .md/.docx, so they keep exit 0.
# The other two mean a machine that CAN build PDFs did not build a correct one —
# exiting 0 on that is how the CV with the missing letters got delivered.
TOLERATED_PDF_FAILURES = (NO_ENGINE, UNSUPPORTED_SCRIPT)


def pdf_failure_is_tolerated(reasons):
    return bool(reasons) and all(r in TOLERATED_PDF_FAILURES for r in reasons)


def _note(reasons, reason):
    if reasons is not None:
        reasons.append(reason)
    return False


def _discard_pdf(out_path, tex_path=None):
    """Remove any PDF left at the output name, on EVERY path that fails to write
    a correct new one.

    The `Missing character` branch has always done this, and its reasoning —
    a wrong PDF is worse than no PDF, because neither the recruiter nor the
    candidate can see that it is wrong — applies unchanged to every other way a
    render can fail. It was not applied there, and that is a live defect: the
    tailoring loop in modes/apply.md re-renders every round, so one failed round
    left the PREVIOUS round's `cv.pdf` sitting under the same filename while
    `cv.md`, `cv.docx` and `cv.tex` all held the new text. `check_pages` then
    read that stale file, found `meta.name` and the orgs in it (they had not
    changed), and wrote a `pass` receipt over its sha — so a claim that had been
    walked back, or an employer name that had been corrected, shipped inside a
    fully-gated package.

    Deleting is right rather than leaving-and-warning: a warning on stderr is
    read by the agent, but the file is read by the employer, and only one of
    those two is still around at submission time. The `.tex` stays unless the
    RTL branch explicitly refuses it too; otherwise it is a deliverable in its
    own right and it is what the user recompiles.
    """
    out_path = pathlib.Path(out_path)
    candidates = [out_path]
    if tex_path is not None:
        candidates.append(pathlib.Path(tex_path).with_suffix(".pdf"))
    for path in candidates:
        try:
            if path.exists():
                path.unlink()
        except OSError:
            # Best-effort: a PDF we cannot remove is reported by the caller's own
            # failure message, and raising here would replace a specific
            # diagnosis ("compile failed, here is the log") with an unrelated one.
            pass


def compile_latex(engine, tex_path, out_path, reasons=None):
    """Run `engine` on `tex_path` and land the result at `out_path`.

    Returns True only if a PDF was produced AND every glyph in it survived. One
    compile helper, both renderers — the same reason `_engine_cmd` is shared.
    `reasons`, if given, collects the failure token (see above) for a caller that
    needs to pick an exit code.

    The `Missing character` scan is the point of this function. The engine prints
    one such warning per dropped glyph and still exits 0, and the old code ran
    `subprocess.run(..., capture_output=True)` and discarded the output — so a CV
    whose name had lost a letter printed "Wrote cv.pdf" and passed every gate.
    A PDF with dropped glyphs is a WRONG artifact, not a degraded one: the
    recruiter cannot tell it is wrong, and the candidate cannot tell either
    because cv.md is intact. So the file is deleted rather than left to be sent,
    and the `.tex` (always a deliverable here) stays behind.
    """
    tex_path, out_path = pathlib.Path(tex_path), pathlib.Path(out_path)
    cmd = _engine_cmd(engine, tex_path, out_path.parent)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except (OSError, subprocess.CalledProcessError):
        # OSError is the real one: find_latex_engine can return a path from
        # _ENGINE_DIRS that turns out not to be executable. CalledProcessError
        # cannot come from this call (there is no check=True — the output is
        # needed on the failure path too, and check=True would throw it away),
        # but it is caught so a caller that stubs subprocess.run the old way
        # still degrades instead of crashing.
        proc = None
    if proc is None or getattr(proc, "returncode", 1) != 0:
        log = "" if proc is None else _engine_log(proc)
        # Before anything else: a PDF at this name is now, by definition, from an
        # earlier run — this one produced nothing.
        _discard_pdf(out_path, tex_path)
        print(f"WARNING: LaTeX compile failed. PDF could not be produced. "
              f"Any PDF from a previous run at {out_path} has been removed so it "
              f"cannot be sent by mistake. LaTeX source is at: {tex_path}",
              file=sys.stderr)
        if tectonic_needs_host_execution(engine, log):
            print(f"NOTICE_{HOST_EXECUTION_REQUIRED}: Tectonic is installed, but "
                  "this restricted macOS process cannot initialize "
                  "SystemConfiguration. Rerun only TeX rendering and PDF "
                  "verification through the host's approved trusted or elevated "
                  "execution route. Do not reinstall Tectonic or reuse an older PDF.",
                  file=sys.stderr)
        for line in log.strip().splitlines()[-15:]:
            print(f"  | {line}", file=sys.stderr)
        return _note(reasons, COMPILE_FAILED)

    # If the engine wrote the PDF next to the .tex but the caller requested a
    # different name, move it into place.
    produced = tex_path.with_suffix(".pdf")
    if not out_path.exists() and produced.exists():
        produced.replace(out_path)

    dropped = missing_characters(_engine_log(proc))
    if dropped:
        _discard_pdf(out_path, tex_path)
        print(f"ERROR: {len(dropped)} character(s) could not be typeset and were "
              f"DROPPED from the PDF — the engine reported this and exited 0, so "
              f"the file would have looked fine while a recruiter read a name with "
              f"letters missing. No PDF was written. The LaTeX source is at "
              f"{tex_path}.", file=sys.stderr)
        for item in dropped[:20]:
            print(f"  missing: {item}", file=sys.stderr)
        if len(dropped) > 20:
            print(f"  … and {len(dropped) - 20} more", file=sys.stderr)
        print("Fix it by pointing the renderer at a font that covers these "
              "characters: set `meta.main_font` (Latin) or `meta.cjk_font` (CJK) "
              "in the profile to a font installed on this machine. Markdown and "
              ".docx are unaffected.", file=sys.stderr)
        return _note(reasons, MISSING_CHARACTERS)

    # Same log, same exit-0 silence, same class of loss: text that ran off the
    # sheet is unreadable for exactly the reason a dropped glyph is.
    overfull = overfull_boxes(_engine_log(proc))
    margin_pt = off_page_pt(tex_path.read_text(encoding="utf-8", errors="replace")
                            if tex_path.exists() else "")
    off_page = [pt for pt in overfull if pt >= margin_pt]
    if off_page:
        _discard_pdf(out_path, tex_path)
        print(f"ERROR: {len(off_page)} line(s) ran off the edge of the page — "
              f"the widest by {off_page[0]:.1f}pt, past a {margin_pt:.0f}pt "
              f"margin — so the characters beyond the edge are missing from the "
              f"PDF. The engine reported this and exited 0. No PDF was written; "
              f"the LaTeX source is at {tex_path}.", file=sys.stderr)
        # The hint used to say "almost always one unbreakable token: a bare DOI…",
        # and the case that actually reached it was an entry header — a long
        # location beside the dates — so it sent the reader hunting for a URL
        # that was not there. It names both, and the lines the engine named.
        where = overfull_source_lines(_engine_log(proc), margin_pt)
        print("Two things cause this. One unbreakable token — a bare DOI, a repo "
              "URL, a long file path, a compound word — anywhere on the page; or a "
              "very long field in an entry header (title, organisation, location), "
              "which shares one row with the dates. Shorten it, add a space, or "
              "(for a URL) let it wrap."
              + (f" The engine places it at {tex_path.name} line(s) "
                 f"{', '.join(str(n) for n in where)}." if where else ""),
              file=sys.stderr)
        return _note(reasons, TEXT_OFF_PAGE)
    if overfull:
        # On the paper but into the margin. Loud, because nothing downstream
        # looks at the PDF's geometry — but not fatal, because it is still
        # readable and refusing here would block a deliverable over kerning.
        print(f"WARNING: {len(overfull)} line(s) overflow the text block into "
              f"the margin (widest {overfull[0]:.1f}pt). The PDF is readable and "
              f"was written, but check {out_path} before sending it.",
              file=sys.stderr)
    return True


def _engine_log(proc):
    """stdout + stderr of a finished engine run, as one string."""
    return "".join(str(getattr(proc, s, "") or "") for s in ("stdout", "stderr"))


# Right-to-left scripts. The preamble loads neither `bidi` nor `polyglossia` and
# sets no script direction, so once a font covers Arabic the compile SUCCEEDS and
# produces a page that is reversed and unshaped: `أحمد الفارسي` came back out of
# pdftotext as `ﺍﻝﻑﺍﺭﺱﻱ ﺃﺡﻡﺩ` — isolated presentation forms, left to right.
# (The forms above are listed in the order pdftotext emitted them, left to
# right. No BiDi control character is used to display them: an invisible
# reordering mark in a comment is the Trojan Source vector, and
# scripts/check_hidden_chars.py refuses one tree-wide.)
# Exit 0, "Wrote cv.pdf", and a document no reader of the language can use.
#
# Worse, the documented remedy led straight into it: without a font the renderer
# refuses loudly and says "set meta.main_font", and doing that turned a loud
# refusal into a silent wrong artifact.
#
# So the PDF is refused as UNSUPPORTED_SCRIPT, which is a TOLERATED failure —
# .md and .docx carry RTL text correctly and still ship, exit code unchanged.
# Supporting it properly means a bidi-aware preamble, which is a real change to
# the template rather than a regex.
_RTL_RANGES = (
    ("\u0590", "\u05ff"),   # Hebrew
    ("\u0600", "\u06ff"),   # Arabic
    ("\u0700", "\u074f"),   # Syriac
    ("\u0750", "\u077f"),   # Arabic Supplement
    ("\u0780", "\u07bf"),   # Thaana
    ("\u07c0", "\u07ff"),   # N'Ko
    ("\u0800", "\u083f"),   # Samaritan
    ("\u08a0", "\u08ff"),   # Arabic Extended-A
    ("\ufb1d", "\ufb4f"),   # Hebrew presentation forms
    ("\ufb50", "\ufdff"),   # Arabic presentation forms A
    ("\ufe70", "\ufeff"),   # Arabic presentation forms B
)


def has_rtl(text) -> bool:
    return any(any(lo <= ch <= hi for lo, hi in _RTL_RANGES) for ch in str(text))


def profile_has_rtl(profile) -> bool:
    """Whether any rendered text in the profile is written right-to-left."""
    return has_rtl(str(profile))


def render_pdf(profile, out_path, reasons=None):
    """Build PDF via LaTeX. Always writes the `.tex` next to out_path (it is a
    deliverable in its own right, not just a failure breadcrumb). Returns True
    on success, False if no engine / compile failed / glyphs were dropped;
    `reasons`, if given, collects which of the three it was."""
    out_path = pathlib.Path(out_path)
    tex_path = out_path.with_suffix(".tex")
    # Any PDF sitting here belongs to an earlier run. Every path out of this
    # function either writes a new one or must leave none — see `_discard_pdf`.
    # Doing it up front rather than per-branch means a future early return cannot
    # reintroduce the stale-PDF defect by forgetting the call.
    _discard_pdf(out_path, tex_path)

    if profile_has_rtl(profile):
        # A prior non-RTL render may have left a compilable source here. RTL
        # refuses that artifact too; retaining it would also make the CLI claim
        # it had just written a source for this profile.
        tex_path.unlink(missing_ok=True)
        print("WARNING: this profile contains right-to-left text (Arabic, Hebrew "
              "or similar). The LaTeX template has no bidi support, so a PDF "
              "built from it would come out reversed and unshaped — a document "
              "the reader cannot use, produced with no error. No PDF was "
              "written; Markdown and .docx carry the text correctly.",
              file=sys.stderr)
        _note(reasons, UNSUPPORTED_SCRIPT)
        return False

    cjk = profile_has_cjk(profile)

    # Resolve the engine BEFORE building the source: the preamble has to match
    # the engine that will compile it, and getting that pairing wrong is what
    # dropped Latin Extended-A out of every PDF this renderer produced.
    engine = find_latex_engine(cjk=cjk)
    # The .tex lands next to the PDF, so that is where a photo has to be staged
    # for the source to stay self-contained and compilable elsewhere.
    tex = build_latex(profile, cjk=cjk, engine=engine,
                      asset_dir=tex_path.parent, asset_stem=tex_path.stem)
    tex_path.write_text(tex, encoding="utf-8")

    if engine is None:
        if cjk:
            print("WARNING: no Unicode LaTeX engine found for this CJK CV. "
                  "A CJK PDF needs XeLaTeX (xelatex) or tectonic plus an "
                  "installed CJK font; pdflatex cannot do it. Markdown and "
                  f".docx still render correctly. Wrote the XeLaTeX source to "
                  f"{tex_path} — compile it with `xelatex` once an engine and a "
                  "CJK font are available.", file=sys.stderr)
        elif profile_needs_unicode_font(profile):
            print("WARNING: no LaTeX engine (tectonic/pdflatex) found, and this "
                  "CV contains characters above U+00FF (accented or non-Latin "
                  f"letters). Wrote the XeLaTeX source to {tex_path}: compile it "
                  "with `tectonic` (or xelatex/lualatex), NOT pdflatex — the "
                  "source uses fontspec so those characters survive.",
                  file=sys.stderr)
        else:
            print("WARNING: no LaTeX engine (tectonic/pdflatex) found. "
                  f"Wrote {tex_path}; install tectonic to produce a PDF.",
                  file=sys.stderr)
        return _note(reasons, NO_ENGINE)

    return compile_latex(engine, tex_path, out_path, reasons=reasons)


# ── CLI ───────────────────────────────────────────────────────────────────────

# What each format's bytes must actually start with. The check is on content, not
# on the extension, for the same reason `photo_format` is.
_FORMAT_MAGIC = {"docx": b"PK\x03\x04", "pdf": b"%PDF"}
_FORMAT_SUFFIX = {"md": ".md", "docx": ".docx", "pdf": ".pdf"}


def confirm_written(out, fmt):
    """True when `out` really is a non-empty file of format `fmt`.

    `main` used to print `Wrote {out}` without stat-ing the path, so a renderer
    that wrote nothing — or wrote the wrong format, which `render_letter --format
    md` could do by emitting a PDF into a `.md` — still reported success and
    exited 0. The agent then recorded the deliverable as produced and the user
    found out at upload time. Neither renderer's CLI format dispatch had a test,
    so nothing else was watching this.
    """
    out = pathlib.Path(out)
    if not out.is_file():
        print(f"ERROR: {fmt} render reported success but {out} does not exist.",
              file=sys.stderr)
        return False
    if out.stat().st_size == 0:
        print(f"ERROR: {fmt} render wrote {out} but it is empty.", file=sys.stderr)
        return False
    magic = _FORMAT_MAGIC.get(fmt)
    head = out.open("rb").read(8)
    if magic and not head.startswith(magic):
        print(f"ERROR: {out} was written for --format {fmt} but does not start "
              f"with {magic!r}. The file is not a {fmt}.", file=sys.stderr)
        return False
    if not magic:  # md: must be readable text, not a binary blob
        try:
            out.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"ERROR: --format md wrote non-text bytes to {out}.",
                  file=sys.stderr)
            return False
    expected = _FORMAT_SUFFIX.get(fmt)
    if expected and out.suffix.lower() != expected:
        # Not fatal: the caller may have a reason. But an ATS portal rejects on
        # extension, so silence here is not free either.
        print(f"WARNING: --format {fmt} wrote {out.name}; most upload portals "
              f"expect a {expected} extension.", file=sys.stderr)
    return True


def main(argv=None):
    reset_market_warnings()
    reset_photo_warnings()
    reset_shape_warnings()
    ap = argparse.ArgumentParser()
    ap.add_argument("profile")
    ap.add_argument("--format", choices=["md", "docx", "pdf"], default="md")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    try:
        profile = load_profile(args.profile)
    except journal.YamlUnreadable as exc:
        # Exit 2 = "could not run", the same meaning it carries in every gate. A
        # renderer has no receipt to leave, so the exit code and this line are the
        # whole of the report — which is why it must not be a traceback.
        print(f"cannot render: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        # A profile that PARSES but is the wrong shape — `meta: "us"`, a missing
        # required field — is also "could not run", not "rendered and something
        # failed". It was escaping as a traceback at exit 1, which in this script
        # already means the PDF step failed.
        print(f"cannot render: {exc}", file=sys.stderr)
        return 2

    # `meta.paper` is validated HERE, for every format, and not left to the one
    # that happens to read it. `paper_for` runs only on the LaTeX path, so a
    # typo'd override rendered .md and .docx happily and then failed the PDF with
    # a raw traceback — the same profile behaving three ways, and the one report
    # the user gets being a stack trace. It stays FATAL rather than falling back
    # to the market default: silently ignoring an override is how a US CV goes
    # out on A4, which is the defect the override exists to prevent.
    try:
        paper_for((profile or {}).get("meta"))
    except ValueError as exc:
        print(f"cannot render: {exc}", file=sys.stderr)
        return 2

    out = pathlib.Path(args.out)
    try:
        return _render_format(args.format, profile, out)
    except (AttributeError, TypeError) as exc:
        # `profile_shape_problems` names every shape known to be unprintable. This
        # is the net under it: a field shape nobody listed must still end as
        # "could not run" with one readable line, not as a traceback at exit 1 —
        # the code this script keeps for "rendered, and the PDF step failed".
        print(f"cannot render: {args.profile}: the renderer could not read this "
              f"profile ({type(exc).__name__}: {exc}). This is usually a field of "
              f"the wrong shape: sections such as experience must be lists of "
              f"mappings, and each date one value.", file=sys.stderr)
        return 2


def _render_format(fmt, profile, out):
    """Write `profile` as `fmt` to `out`; the exit code main() returns."""
    if fmt == "md":
        out.write_text(render_markdown(profile), encoding="utf-8")
    elif fmt == "docx":
        try:
            render_docx(profile, out)
        except DocxMarkupError as exc:
            print(f"cannot render Word: {exc}", file=sys.stderr)
            return 1
    elif fmt == "pdf":
        reasons = []
        ok = render_pdf(profile, out, reasons=reasons)
        tex = out.with_suffix(".tex")
        if ok:
            if not confirm_written(out, "pdf"):
                return 1
            # The .tex is delivered alongside every PDF, by design.
            print(f"Wrote {out} (LaTeX source alongside it: {tex})")
            return 0
        # Deliberately does NOT name a cause: render_pdf already printed the
        # specific one (no engine / compile failed / glyphs dropped) and this
        # line used to assert "no LaTeX engine found" for all three, which told
        # a user whose glyphs had just been dropped to install an engine they
        # already had.
        # And it does not claim a .tex that is not there. The RTL refusal
        # returns before the source is built, on purpose: a LaTeX source for
        # right-to-left text is exactly the artifact that compiles to a reversed
        # page, so handing it over is handing over the same defect one step back.
        where = (f"LaTeX source written to: {tex}" if tex.exists()
                 else "No LaTeX source was written.")
        print(f"PDF could not be built — see the warning above. {where}",
              file=sys.stderr)
        return 0 if pdf_failure_is_tolerated(reasons) else 1
    if not confirm_written(out, fmt):
        return 1
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
