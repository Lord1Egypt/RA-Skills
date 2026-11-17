#!/usr/bin/env python3
"""Gate: is this shortlist real? (spec §5.1, risk register rows 1-3)

A fabricated shortlist is internally consistent, perfectly formatted, and every
field has the right shape — so shape is not what gets checked. What gets checked
is that each row's identifier appears VERBATIM in a raw capture from the site it
claims, because that is the one thing a fabricated row cannot do.

**One field is not enough.** Verifying `source_id` and stopping passed a row that
kept a real jobId and invented title, company, location, salary and `raw_text` —
copying an identifier out of a capture costs nothing. So two more anchors tie the
row to the bytes: `raw_text` must be mostly FOUND in that site's captures, and
`id` must be exactly `<site>-<source_id>` (the format modes/discover.md defines).
`title` is deliberately NOT anchored: step 6 normalises titles on purpose, and a
gate that fires on a normalised title is a gate people route around.

Findings prefixed `WARN_` do not fail the gate — the split is the same one
check_conventions.py and check_assessment.py already make. Market fit is the only
one: an `indeed` search for London returns Columbus, Ohio (measured), so a row
whose location names a country outside `brief.markets` is worth saying out loud,
but deciding "this location is in the Netherlands" needs a gazetteer, and a
gazetteer will be wrong about `Remote in EU`, `Randstad` and `Noord-Holland`. A
check that cries wolf on ordinary output is worse than no check: the reader
learns to skip the line, and it stops working on the run that mattered.

Exit codes: 0 = passed (warnings do not change this), 1 = hard findings on
stdout, 2 = could not run. On exit 2 one receipt with verdict "could_not_run" is
appended — EXCEPT when the workspace directory itself does not exist, because
then there is nothing to append to. If you find no receipt at all, that is the
case you are in.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


import journal  # noqa: E402  (Plan 1)
import enter_mode  # noqa: E402  (Plan 1)
import paths       # noqa: E402  (Plan 1)
import discovery_catalogue  # noqa: E402
from record_browser_capture import (read_retrieval_calls, validate_record,
                                    check_stop_order, ACTION)  # noqa: E402
from vocab import EFFORT, VERDICTS  # noqa: E402  (Plan 1 — the ONE vocabulary)
import report_locales as locales  # noqa: E402

GATE = "check_shortlist"
MODE = "discover"

# The seventeen fields of a shortlist row: the thirteen JobListingEvidence base
# fields, plus the four this skill adds on top of them. This tuple is the single
# enumeration — modes/discover.md documents the same seventeen and the mode-doc
# test asserts every one of them is findable there.
REQUIRED_ROW_FIELDS = (
    "id", "title", "company", "location", "salary", "url", "source_site",
    "source_id", "extraction_method", "retrieved_at", "quality",
    "verification", "raw_text", "why_matched", "verdict", "provisional",
    "effort",
)

# VERDICTS and EFFORT are imported, never re-spelled: a second copy of a closed
# set is a second thing to forget to update. VERDICTS is ordinal, strongest
# first, so the detail-fetch cap is a slice of it rather than a third list that
# could silently disagree with the other two.
TOP_THREE = VERDICTS[:3]
EXTRACTION_METHODS = ("adapter_search", "adapter_detail", "user_paste",
                      "public_page", "browser_page")
QUALITIES = ("complete", "partial", "card_only")
VERIFICATIONS = ("fresh_verified", "collected_unverified", "stale_possible")

# Shorter than this and a verbatim substring search would match almost any
# capture, which makes the provenance check vacuous rather than strict.
MIN_SOURCE_ID_LEN = 4

# `raw_text` is the card text the evaluator actually saw, so it is checked
# against the capture the way source_id is — but in pieces, because a card
# summary is JOINED BY HAND out of adapter fields and is never one contiguous
# substring of the JSON. Split it on the separators people join with, then ask
# how much of it the capture accounts for, weighted by length so that one
# invented sentence outweighs three copied words.
#
# The middle dots are here because an adapter uses them ITSELF: LinkedIn returns
# `"location": "Epona · Breda-Tilburg Area (Hybrid)"`, so `·` is what a card
# copied from that capture is joined with. Measured 2026-09-20, a live NL round
# whose every field was verbatim failed all ten rows at 9-12% coverage, because
# the whole card stayed one segment and no capture holds it contiguously.
# Splitting more finely can only help an honest row: if the capture contains the
# joined whole, it contains each part — so this widens no gap. A segment the
# capture does not hold still fails, which the paired test pins.
_RAW_TEXT_SPLIT = re.compile(r"[|｜,，、;；/·・･‧•\n\r\t]+")
_WHITESPACE = re.compile(r"\s+")
MIN_RAW_TEXT_SEGMENT = 2
# Deliberately below 1.0 — hand-joined summaries lose characters to punctuation
# and re-wrapping — and well above half, because a row that invents most of its
# card text is a fabricated row wearing a real identifier.
RAW_TEXT_FLOOR = 0.7

# Market fit, and why it is only a WARNING. The rule is one-directional in the
# same sense as the count checks below: it fires on POSITIVE evidence that a row
# names a country outside brief.markets, never on failure to recognise the right
# one. `Remote in EU`, `Randstad` and `Noord-Holland` resolve to nothing here and
# stay silent; `Columbus, OH` and `Remote in United States` resolve to `us` and
# speak up. Country-level tokens only: city names are ambiguous across markets
# (London, Ohio is 25 miles from Columbus and is exactly what `opencli indeed
# search --location "London"` returns), which is the reason this check exists.
# City-level tokens, declared rather than mixed in silently. The rule above is
# country-level only, and "the hague" breaks it — deliberately, because it is
# the seat of government and unambiguous in a way `london` is not. Declaring it
# is what lets test_market_vocabularies_agree check every OTHER token against
# render_cv's country table without either hiding this one or failing on it.
CITY_TOKENS = frozenset({"the hague"})

MARKET_TOKENS = {
    "cn": ("china", "中国", "中國", "中华人民共和国"),
    "nl": ("netherlands", "nederland", "holland", "the hague"),
    "de": ("germany", "deutschland"),
    "uk": ("united kingdom", "great britain", "england", "scotland", "wales",
           "northern ireland"),
    "us": ("united states", "u.s.a", "usa"),
}
# Phrases that CONTAIN a country token and name somewhere else. Stripped before
# the token scan, so the longer, more specific name wins — the same
# longest-match rule render_cv.resolve_cluster uses.
#
# Measured 2026-09-05: `Sydney, New South Wales` resolved to `uk` because it
# contains "wales", and `Boston, New England Region` because it contains
# "england". Both then passed a UK brief in silence, on the one check standing
# between a UK user and "there are no London backend roles".
_DECOY_PHRASES = {
    "new south wales": "au",
    "new england": "us",
    # A district, not a country. Amsterdam, London, Berlin and Manchester all
    # have one, and `Zeedijk (Chinatown), Amsterdam` was reading as a China row
    # under a Netherlands brief. None means "strip it and claim nothing".
    "chinatown": None,
    "china town": None,
    "little italy": None,
}

# The 50 states plus DC, matched CASE-SENSITIVELY after a comma, because that is
# how every adapter renders a US location ("Columbus, OH 43215") and because
# lowercase `in`/`or`/`me` are ordinary English words. Two letters are ambiguous
# by nature — "Amsterdam, NH" would read as New Hampshire — and that residue is
# precisely why the finding is a WARN_ the reader may overrule in one line.
_US_STATE = re.compile(
    r",\s*(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|"
    r"N[CDEHJMVY]|OH|OK|OR|P[A]|RI|S[CD]|T[NX]|UT|V[AT]|W[AIVY])\b")

# Wording that asserts the run found nothing. Only consulted when the shortlist
# has ZERO rows: with rows present, "没有匹配到 staff 级别的岗位" is a qualified
# statement about a slice, not a claim that the run came back empty.
EMPTINESS_PHRASES = tuple(phrase for lang in locales.LANGUAGES
                          for phrase in locales.GATE_TEXT[lang]["empty"])

_ABSENCE_NEGATION = re.compile(
    r"(?:不(?:代表|意味着|说明|等于)|并非|不是|"
    r"(?:不能|无法|尚不能|尚无法)(?:据此)?(?:判断|认定|断言|确认|证明|说明))[^。\n]{0,40}$"
    r"|(?:does\s+not\s+mean|doesn['’]t\s+mean|not\s+evidence\s+(?:that|of)|"
    r"(?:cannot|can['’]t)\s+(?:conclude|infer|say|determine)|"
    # The plainest denial there is, and the one the English half was missing
    # while the Chinese half had its twin in `不是`: quote the claim in order
    # to reject it. Found 2026-10-08 by eval-5, whose run wrote `It is not
    # "there are no matching jobs in Shanghai"` — the most careful sentence in
    # the message — and was scored as having claimed an empty market. A gate
    # enforced in one language only is the failure this repo has fixed before.
    r"(?:is|are|was|were)\s+not\s+(?:a|an|the|that)?\s*"
    r"(?:finding|claim|conclusion|statement|the\s+same\s+as)?\s*[\"“']?)"
    r"[^.\n]{0,70}$",
    re.I)


def absence_claims(text):
    """Return asserted empty-result phrases and their lines, not denials of them."""
    found = []
    for phrase in EMPTINESS_PHRASES:
        for match in re.finditer(re.escape(phrase), text, re.I):
            prefix = re.split(r"[。！？.!?；;\n，,]|不过|但是|然而|但|\b(?:but|however|yet)\b",
                              text[:match.start()], flags=re.I)[-1]
            if _ABSENCE_NEGATION.search(prefix):
                continue
            start = text.rfind("\n", 0, match.start()) + 1
            end = text.find("\n", match.end())
            found.append((match.start(), phrase, text[start:end if end >= 0 else None].strip()))
    return [(phrase, line) for _, phrase, line in sorted(found)]

# Required reader-facing text follows the user's report language, not the
# market. Shared translations let native reports pass without foreign labels.
#
# Matching is case-insensitive (see _says) because these strings are sentence- and
# heading-initial in English and "Provisional" is the natural rendering of an
# anchor spelled `provisional`. Case is not the claim.

# The degraded-output disclosure block. The last four answers ship pre-filled as
# 否 / no, so concealing a retry or a bypass has to be an active overwrite rather
# than an omission.
DISCLOSURE_LABELS = tuple(zip(*(locales.GATE_TEXT[lang]["disclosure"]
                                for lang in locales.LANGUAGES)))

# The reader-facing half of the provisional stamp (spec §5.1 step 6: a discover
# verdict 不带这个戳就不许渲染). `provisional: true` in shortlist.yaml is the
# machine half, and nobody reading the round ever sees it — shortlist.md is what
# the user actually reads, so that is where the claim has to be qualified.
PROVISIONAL_STAMP = locales.anchors("provisional")
# A discovery round can read a bounded set of full descriptions to support its
# default recommendations. That is more evidence than a card, but still not the
# complete, application-specific assessment assess mode performs.
DETAIL_PROVISIONAL_STAMP = locales.anchors("detail_provisional")

# The yellow-tier round caps from references/source-policy.md, as numbers,
# because a cap enforced by a paragraph is not a cap. brief.yaml must carry both
# and neither may exceed these. This is that reference file's named backstop.
MAX_ROWS_PER_ROUND_CEILING = 25
MAX_PAGES_PER_SITE_CEILING = 2


def load_raw_texts(workspace):
    """{site: {filename: text}} over raw/<site>-*.json, preserving captured text."""
    out = {}
    raw_dir = pathlib.Path(workspace) / "raw"
    if not raw_dir.is_dir():
        return out
    for path in sorted(raw_dir.glob("*.json")):
        if "-" not in path.name:
            continue
        site = path.name.split("-", 1)[0]
        out.setdefault(site, {})[path.name] = path.read_text(
            encoding="utf-8", errors="replace")
    return out


def _normalise(text):
    """Whitespace and case are not the claim; the words are.

    A card copied through YAML comes back re-wrapped (a block scalar folds its
    newlines into spaces), and demanding the model reproduce the wrap points
    would fail a raw_text copied character-for-character.
    """
    return _WHITESPACE.sub(" ", str(text)).strip().casefold()


# Punctuation that carries no meaning for "does this value come from that
# capture": dash variants, bracket variants, and the fullwidth forms a CJK IME
# produces. `_normalise` deliberately folds only whitespace and case, because
# raw_text is a verbatim copy and its wrap points are not the claim. company and
# salary are different: they are SHORT values re-rendered by hand, so an en dash
# where the capture had an em dash, or `（）` where it had `()`, is the same
# value — and hard-failing on it teaches the reader that this gate is wrong.
_PUNCT_FOLD = str.maketrans({
    "–": "-", "—": "-", "−": "-", "~": "-", "〜": "-", "－": "-",
    "（": "(", "）": ")", "［": "[", "］": "]", "，": ",", "、": ",",
    "：": ":", "；": ";", "％": "%", "／": "/", "　": " ",
})
_DROPPABLE = str.maketrans("", "", " .,()[]-·/")


def _loose(text):
    """`_normalise`, plus punctuation folding, for the short re-rendered fields."""
    return _normalise(str(text).translate(_PUNCT_FOLD)).translate(_DROPPABLE)


def _raw_text_coverage(raw_text, captures):
    """(fraction of raw_text the captures account for, the segments they do not).

    None when raw_text has no segment long enough to search for, which is the
    can't-tell case rather than the it-failed case.
    """
    haystacks = [_normalise(text) for text in captures]
    segments = [seg.strip() for seg in _RAW_TEXT_SPLIT.split(str(raw_text))]
    segments = [seg for seg in segments if len(seg) >= MIN_RAW_TEXT_SEGMENT]
    if not segments:
        return None, []
    missing = [seg for seg in segments
               if not any(_normalise(seg) in hay for hay in haystacks)]
    total = sum(len(seg) for seg in segments)
    lost = sum(len(seg) for seg in missing)
    return (total - lost) / total, missing


def _contains_source_id(source_id, text):
    """Match captured values, without confusing JSON escapes with literal IDs."""
    try:
        value = json.loads(text)
    except ValueError:
        return source_id in text
    pending = [value]
    while pending:
        value = pending.pop()
        if isinstance(value, dict):
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
        elif isinstance(value, (str, int, float)) and source_id in str(value):
            return True
    return False


def _check_provenance(label, row, site, raw_texts):
    findings = []
    source_id = str(row.get("source_id") or "").strip()
    if not source_id:
        findings.append(f"NO_SOURCE_ID: {label} has no source_id")
        return findings
    if len(source_id) < MIN_SOURCE_ID_LEN:
        findings.append(
            f"SUSPICIOUS_SOURCE_ID: {label} source_id {source_id!r} is shorter "
            f"than {MIN_SOURCE_ID_LEN} characters; a verbatim search for it "
            "would match almost any capture")
        return findings
    if not site:
        return findings
    captures = raw_texts.get(site)
    if not captures:
        findings.append(
            f"NO_RAW_CAPTURE_FOR_SITE: {label} claims source_site {site!r} but "
            f"raw/ holds no {site}-*.json capture")
        return findings
    if not any(_contains_source_id(source_id, text) for text in captures.values()):
        findings.append(
            f"SOURCE_ID_NOT_IN_RAW: {label} source_id {source_id!r} does not "
            f"appear verbatim in any of {', '.join(sorted(captures))}")

    # The second anchor. An identifier is one field to copy; the card text is the
    # row's whole claim about what the posting says, and it is the field an
    # invented row has to invent.
    raw_text = str(row.get("raw_text") or "").strip()
    if raw_text:
        covered, missing = _raw_text_coverage(raw_text, captures.values())
        if covered is not None and covered < RAW_TEXT_FLOOR:
            shown = "; ".join(missing[:4]) + ("; …" if len(missing) > 4 else "")
            findings.append(
                f"RAW_TEXT_NOT_IN_RAW: {label} raw_text is only {covered:.0%} "
                f"accounted for by {', '.join(sorted(captures))} (floor "
                f"{RAW_TEXT_FLOOR:.0%}). Not found in any capture: {shown}. "
                "raw_text is the card text the adapter returned, copied — not a "
                "summary, not a translation, and never a posting you did not "
                "retrieve. Your own words belong in why_matched.")

    url = str(row.get("url") or "").strip()
    if not url:
        findings.append(
            f"MISSING_POSTING_URL: {label} has no direct posting URL. A search "
            "result cannot become a user-facing shortlist row without a link the "
            "reader can open.")
    else:
        try:
            parsed = urlsplit(url)
        except ValueError:
            parsed = None
        if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.netloc:
            findings.append(
                f"BAD_POSTING_URL: {label} url {url!r} is not an absolute HTTP(S) "
                "posting URL.")
        else:
            stem = url.split("?", 1)[0].split("#", 1)[0]
            if not any(stem in text for text in captures.values()):
                findings.append(
                    f"URL_NOT_FROM_ADAPTER: {label} url {url!r} was not returned by "
                    f"an adapter ({stem!r} appears in no {site}-*.json capture)")

    # The fields the reader acts on. 55e4f84 anchored the identifier and the card
    # text and stopped there, so `company`, `location` and `salary` stayed free
    # text a row could invent — and could invent in flat contradiction to the
    # very capture it cites. Salary is the one a job-seeker acts on hardest and
    # the one a model most readily hallucinates out of a blank field; measured on
    # both shipped fixtures, a presence check on these passes 4/4, so this costs
    # no false alarms.
    for field, code in (("company", "COMPANY_NOT_IN_RAW"),
                        ("salary", "SALARY_NOT_IN_RAW")):
        value = str(row.get(field) or "").strip()
        if not value:
            continue
        # Anchored to THIS ROW's card text first, not to the whole file. A search
        # capture holds up to 25 cards, so "appears somewhere in any <site>-*.json"
        # made every company name and every salary band in the file a licensed
        # value for every row from that site — a sibling posting vouching for a
        # value this posting never carried. raw_text is itself anchored to the
        # capture by RAW_TEXT_NOT_IN_RAW, so this is strictly narrower, and it
        # falls back to the capture when the row has no raw_text (NO_RAW_TEXT
        # reports that separately).
        row_text = str(row.get("raw_text") or "").strip()
        haystacks = [row_text] if row_text else list(captures.values())
        if not any(_loose(value) in _loose(text) for text in haystacks):
            findings.append(
                f"{code}: {label} {field} {value[:60]!r} does not appear in this "
                f"row's own card text. This is the field the reader "
                "acts on, and the capture this row cites does not support it — "
                "copy what the adapter returned, or leave it empty.")
    return findings


def check_rows(shortlist, raw_texts):
    findings = []
    for index, row in enumerate(shortlist.get("rows") or []):
        if not isinstance(row, dict):
            findings.append(f"BAD_ROW: row {index} is not a mapping")
            continue
        label = f"row {index} (id={row.get('id', '<no id>')!r})"
        for field in REQUIRED_ROW_FIELDS:
            if field not in row:
                findings.append(f"MISSING_FIELD: {label} has no `{field}`")
        site = str(row.get("source_site") or "").strip()
        if not site:
            findings.append(
                f"NO_SOURCE_SITE: {label} has no source_site — the row cannot be "
                "traced back to a capture")
        if not str(row.get("title") or "").strip():
            findings.append(
                f"EMPTY_TITLE: {label} has an empty title — the identifying "
                f"field was never recovered (run the detail command for "
                f"{site or 'this site'})")
        if not str(row.get("raw_text") or "").strip():
            findings.append(
                f"NO_RAW_TEXT: {label} has an empty raw_text — the card text is "
                "what ties the row's claims to the capture, so a row without it "
                "asserts a posting nobody can check")
        if not str(row.get("why_matched") or "").strip():
            findings.append(f"NO_WHY_MATCHED: {label} has no why_matched")
        if not str(row.get("retrieved_at") or "").strip():
            findings.append(f"NO_RETRIEVED_AT: {label} has no retrieved_at")
        if row.get("verdict") not in VERDICTS:
            findings.append(
                f"BAD_VERDICT: {label} verdict {row.get('verdict')!r} is not one "
                f"of {', '.join(VERDICTS)}")
        if row.get("provisional") is not True:
            findings.append(
                f"MISSING_PROVISIONAL: {label} has no `provisional: true` stamp. "
                "A discover verdict is based on a card, not on a full JD, so it "
                "may not be rendered without the stamp and is never carried into "
                "an assessment — assess always recomputes.")
        for field, allowed in (("extraction_method", EXTRACTION_METHODS),
                               ("quality", QUALITIES),
                               ("verification", VERIFICATIONS),
                               ("effort", EFFORT)):
            if field in row and row.get(field) not in allowed:
                findings.append(
                    f"BAD_ENUM: {label} {field}={row.get(field)!r} is not one of "
                    f"{', '.join(allowed)}")
        findings.extend(_check_provenance(label, row, site, raw_texts))

        # The third anchor, and the cheapest: modes/discover.md defines `id` as
        # `<site>-<source_id>`, so an id that is anything else names a posting
        # the provenance chain above never touched. Reported after provenance
        # because a wrong id is the smaller of the two claims.
        row_id = str(row.get("id") or "").strip()
        source_id = str(row.get("source_id") or "").strip()
        if site and source_id and row_id != f"{site}-{source_id}":
            findings.append(
                f"BAD_ROW_ID: {label} must be id {site}-{source_id} — "
                "modes/discover.md defines the row id as `<site>-<source_id>`, "
                "and that is the only thing tying the id a reader quotes to the "
                "capture the row was traced to.")

    # One retrieved row may not become two shortlist rows. Without this, count
    # conservation is decorative: the source report can honestly say "2 rows
    # returned" while the shortlist below it lists the same posting three times.
    seen = {}
    for index, row in enumerate(shortlist.get("rows") or []):
        if not isinstance(row, dict):
            continue
        key = (str(row.get("source_site") or "").strip(),
               str(row.get("source_id") or "").strip())
        if not key[1]:
            continue
        if key in seen:
            findings.append(
                f"DUPLICATE_SOURCE_ID: row {index} (id={row.get('id')!r}) repeats "
                f"source_id {key[1]!r} from row {seen[key]} on the same site — one "
                "retrieved row became two shortlist rows")
        else:
            seen[key] = index
    return findings


def _says(md_text, *spellings):
    """Is any spelling of this anchor in the document? Case is not the claim.

    English anchors are usually
    sentence-initial, so `"provisional, from card data only"` has to match
    「Provisional, from card data only」 too. Casefold does not change the length
    of any spelling here, which is what lets _answer_after slice by offset.
    """
    lowered = md_text.casefold()
    return any(spelling.casefold() in lowered for spelling in spellings)


def _both(pair):
    """Show every accepted translation in a finding.

    Printing only the Chinese one is how the English reader learns the gate does
    not know their language.
    """
    return " / ".join(pair)


def _answer_after(line, label):
    """What follows `label` on this line, matched case-insensitively, or None."""
    index = line.casefold().find(label.casefold())
    if index < 0:
        return None
    return line[index + len(label):].strip()


def _check_disclosure(md_text):
    missing = [pair for pair in DISCLOSURE_LABELS if not _says(md_text, *pair)]
    if len(missing) == len(DISCLOSURE_LABELS):
        return ["DEGRADED_WITHOUT_DISCLOSURE: no adapter exited 0 and the "
                "shortlist is empty, so this run is a degraded output. It must "
                "carry the disclosure block, in the language of the round ("
                + "; ".join(_both(pair) for pair in DISCLOSURE_LABELS)
                + ") with every answer filled in."]
    findings = []
    if missing:
        findings.append("DISCLOSURE_INCOMPLETE: the disclosure block is missing "
                        "these lines: "
                        + "; ".join(_both(pair) for pair in missing))
    for pair in DISCLOSURE_LABELS:
        if pair in missing:
            continue
        # Every spelling that is present is checked for its answer. One line per
        # label is the normal shape, but a bilingual block has two, and the
        # pre-filled answer is the whole point of the block — so neither half
        # gets to be the unchecked one.
        for label in pair:
            for line in md_text.splitlines():
                answer = _answer_after(line, label)
                if answer is None:
                    continue
                if not answer:
                    findings.append(
                        f"DISCLOSURE_INCOMPLETE: disclosure line {label!r} has a "
                        "blank answer. The answers ship pre-filled as 否 / no so "
                        "that concealment has to be an active overwrite, not an "
                        "omission.")
                break
    return findings


def _check_sources(workspace, shortlist, rows, calls):
    findings = []
    reported = {str(entry["site"]): entry
                for entry in (shortlist.get("sources") or [])
                if isinstance(entry, dict) and entry.get("site")}
    used = {str(row.get("source_site")) for row in rows
            if isinstance(row, dict) and row.get("source_site")}
    for site in sorted(used):
        if site not in reported:
            findings.append(
                f"SOURCE_REPORT_MISSING: rows cite source_site {site!r} but "
                "shortlist.yaml `sources:` has no entry for it. That entry needs "
                "the adapter's identity_field and detail_command — for any site "
                "outside the four inlined in modes/discover.md they come from "
                "references/discovery-sources.md.")
    for site, entry in sorted(reported.items()):
        command = entry.get("command")
        matching = [c for c in calls if c.get("site") == site
                    and (command is None or c.get("command") == command)]
        if not matching:
            findings.append(
                f"SOURCE_REPORT_CONTRADICTS_JOURNAL: sources[{site}] reports "
                f"command {command!r} but journal.jsonl records no adapter_call "
                "for that site and command")
            continue
        recorded = {c.get("classification") for c in matching}
        if entry.get("classification") not in recorded:
            findings.append(
                f"SOURCE_REPORT_CONTRADICTS_JOURNAL: sources[{site}] reports "
                f"classification {entry.get('classification')!r} but "
                f"journal.jsonl recorded {sorted(x for x in recorded if x)}")

        # ---- 条数守恒 (spec §5.1) --------------------------------------
        # Each of these fires in ONE direction only — the dishonest one. The
        # opposite direction is either impossible or harmless, and a check that
        # also fires on the harmless case is a check people learn to ignore.
        reported_rows = entry.get("rows_returned")
        retrieved = sum(int(c.get("row_count") or 0) for c in matching)
        if isinstance(reported_rows, int) and reported_rows > retrieved:
            findings.append(
                f"SOURCE_REPORT_COUNT_MISMATCH: sources[{site}] reports "
                f"rows_returned={reported_rows} but journal.jsonl recorded "
                f"{retrieved} row(s) across {len(matching)} adapter_call(s). A "
                "run may not report more rows than the adapter returned.")
        site_rows = [r for r in rows if isinstance(r, dict)
                     and str(r.get("source_site") or "").strip() == site]
        if isinstance(reported_rows, int) and len(site_rows) > reported_rows:
            findings.append(
                f"SOURCE_REPORT_COUNT_MISMATCH: {len(site_rows)} shortlist rows "
                f"cite source_site {site!r} but sources[{site}] reports only "
                f"rows_returned={reported_rows}. De-duplication removes rows; "
                "nothing adds them.")
        reported_calls = entry.get("invocations")
        if isinstance(reported_calls, int) and reported_calls < len(matching):
            findings.append(
                f"SOURCE_REPORT_COUNT_MISMATCH: sources[{site}] reports "
                f"invocations={reported_calls} but journal.jsonl recorded "
                f"{len(matching)}. Under-reporting invocations is how a retry "
                "after a stop-signal disappears from the disclosure block.")
        reported_empty = entry.get("identity_field_empty_rows")
        observed_empty = sum(len(c.get("empty_identity_rows") or [])
                             for c in matching)
        if isinstance(reported_empty, int) and reported_empty < observed_empty:
            findings.append(
                f"SOURCE_REPORT_COUNT_MISMATCH: sources[{site}] reports "
                f"identity_field_empty_rows={reported_empty} but journal.jsonl "
                f"recorded {observed_empty}. Under-reporting a blank identity "
                "field hides exactly the gap needs_detail_recovery exists to "
                "surface.")

        # ONE convention: raw_files entries are workspace-relative and carry the
        # `raw/` prefix, exactly as modes/discover.md writes them. The bare
        # basename resolved to <ws>/51job-1.json, which is not where a capture
        # ever is — so the same correct file, reported the other way, produced
        # SOURCE_REPORT_MISSING_RAW and looked like a missing capture.
        for name in entry.get("raw_files") or []:
            name = str(name)
            if not name.startswith("raw/") or ".." in name.split("/"):
                findings.append(
                    f"SOURCE_REPORT_RAW_PATH: sources[{site}] names {name!r}. "
                    "raw_files entries are workspace-relative paths under the "
                    f"capture directory — write "
                    f"{'raw/' + name.rsplit('/', 1)[-1]!r}. One spelling, so a "
                    "name that resolves is a name that was captured.")
                continue
            if not (workspace / name).is_file():
                findings.append(
                    f"SOURCE_REPORT_MISSING_RAW: sources[{site}] names "
                    f"{name!r}, which does not exist")
    return findings


def _check_listing_sources(workspace, rows, calls):
    """A row claims a posting exists; the source has to be one that publishes them.

    Every other provenance anchor holds for a 面经 thread — the id really is in
    the capture, the raw_text really was copied, the URL really came from the
    adapter — so none of them can tell a vacancy from a write-up of an interview
    someone already sat. Reproduced 2026-09-20: such a row passed this gate in
    silence, carrying `verdict: stretch`.

    Three deliberate choices, each one a false positive avoided:

    * The verdict lives in references/discovery-sources.md, not in a set spelled
      here. A hardcoded {nowcoder, maimai} goes stale the day an adapter is
      added and nothing reports it.
    * An UNCATALOGUED site passes. modes/discover.md routes European rounds to
      Indeed's country sites and to market-native boards through the browser,
      and none of those is an adapter in that file — an allow-list would refuse
      exactly the rows that route was opened for.
    * `listing_commands` includes the DETAIL spellings, and a row is judged by
      the commands whose captures actually hold its id. Ranking mode starts from
      pasted URLs, so its rows appear only in a detail capture; demanding a
      search capture would fire on that whole mode.
    """
    findings = []
    sites = {str(row.get("source_site") or "").strip()
             for row in rows if isinstance(row, dict)}
    if not sites - {""}:
        return findings
    try:
        discovery_catalogue.adapters()
    except discovery_catalogue.CatalogueUnreadable as exc:
        # One finding, not one per row, and never a traceback: this gate's
        # contract is findings on stdout, and a broken install is a fact the
        # reader can act on rather than a stack trace to decode.
        return [f"CATALOGUE_UNREADABLE: {exc}. Without it this run cannot tell "
                "a job board from a forum, so no row's source was checked."]
    # Read each capture once, not once per row: a round with 25 rows and 17
    # captures would otherwise re-read the same megabytes 425 times.
    # Keyed by SITE, the way _check_provenance scopes its captures. Sharing one
    # flat map across sites let another site's capture vouch for this row, and
    # _contains_source_id is a substring search over a 4-character floor, so
    # collisions are ordinary rather than exotic: "9597" sits inside 173199597.
    by_capture = {}
    for call in calls:
        name = call.get("stdout_file") or call.get("snapshot_file")
        site = str(call.get("site") or "").strip().casefold()
        if name and site and call.get("command"):
            key = str(name).replace("\\", "/")
            by_capture.setdefault(site, {}).setdefault(key, set()).add(
                str(call["command"]))
    texts = {}
    for captures in by_capture.values():
        for name in captures:
            if name in texts:
                continue
            try:
                texts[name] = (workspace / name).read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        site = str(row.get("source_site") or "").strip()
        source_id = str(row.get("source_id") or "").strip()
        if not site or not discovery_catalogue.is_catalogued(site):
            continue
        allowed = set(discovery_catalogue.listing_commands(site))
        if not allowed:
            findings.append(
                f"NOT_A_LISTING_SOURCE: row {index} (id={row.get('id')!r}) cites "
                f"source_site {site!r}, which references/discovery-sources.md "
                "records as publishing no job postings — its reads return "
                "threads or people, not vacancies. A row asserts a posting "
                "exists, and this source cannot support that. Keep it as a "
                "pointer in the report instead, or correct the source_site.")
            continue
        if not source_id:
            continue    # NO_SOURCE_ID already owns this row
        used = set()
        for name, commands in by_capture.get(site.casefold(), {}).items():
            if name in texts and _contains_source_id(source_id, texts[name]):
                used |= commands
        if used and not (used & allowed):
            findings.append(
                f"NOT_A_LISTING_SOURCE: row {index} (id={row.get('id')!r}) was "
                f"retrieved by {', '.join(sorted(used))} on {site!r}, and "
                "references/discovery-sources.md lists that site's posting "
                f"commands as {', '.join(sorted(allowed))}. The capture behind "
                "this row is not a job posting.")
    return findings


def _check_market_fit(brief, rows):
    """WARN when a row names a country the brief did not ask for (spec §5.1).

    This exists because `opencli indeed search --location "London"` returns rows
    in Columbus, Ohio — the adapter serves the US site and resolves the place
    name against a US gazetteer, so it succeeds, exits 0, and answers a question
    nobody asked. Nothing else in this gate reads brief.markets at all.

    A WARNING on purpose. It fires only on positive evidence of the wrong
    country, never on failure to recognise the right one, because the second
    shape needs a gazetteer and a gazetteer is wrong about `Remote in EU`,
    `Randstad` and `Noord-Holland`. The learned response to a false hard failure
    would be padding brief.locations until the gate shut up — one silent failure
    traded for a loud one.
    """
    markets = {str(m).strip().casefold() for m in (brief.get("markets") or [])
               if str(m).strip()}
    if not markets or "other" in markets:
        # `other` is a legitimate answer (modes/discover.md) and means there is
        # no convention data for the market. Guessing anyway is what this file
        # keeps telling the reader not to do.
        return []
    findings = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        location = str(row.get("location") or "").strip()
        if not location:
            continue
        lowered = _normalise(location)
        named = set()
        for phrase, actual in _DECOY_PHRASES.items():
            if phrase in lowered:
                lowered = lowered.replace(phrase, " ")
                if actual:
                    named.add(actual)
        named |= {market for market, tokens in MARKET_TOKENS.items()
                  if any(token in lowered for token in tokens)}
        # A two-letter state after a comma is positive evidence of the US, and it
        # outranks a country token the same string happens to contain —
        # `Holland, MI 49423` names the Netherlands by substring and Michigan by
        # structure, and the intersection test read the first and went quiet.
        #
        # But only when the state code comes LATER, because that is how job
        # boards write a location: City, Region, Country. In `Holland, MI 49423`
        # the country token IS the city name and the state follows it; in
        # `Amsterdam, NH, Netherlands` the country is last and settles it. An
        # earlier version of this rule made the state unconditionally definitive
        # and cried wolf on every Dutch row written with a province abbreviation
        # — measured, and the reason the position is checked rather than assumed.
        # It also gets `China, TX` right, which no strong/weak token list would.
        state = _US_STATE.search(location)
        # `DE` is Delaware AND the ISO code for Germany, so `Munich, DE` — how
        # most EU aggregator feeds write a German location — warned under a
        # German brief. Two letters cannot settle that on their own, and the
        # brief can: a code matching the brief's OWN market is evidence FOR the
        # brief, and this check exists to find rows outside it. `Wilmington, DE`
        # under a US brief is unaffected — `us` is in markets either way.
        if state and state.group(1).lower() in markets:
            named.add(state.group(1).lower())
            state = None
        if state:
            named.add("us")
        brief_at = max((lowered.rfind(token) for market in markets
                        for token in MARKET_TOKENS.get(market, ())
                        if token in lowered), default=-1)
        definite_us = bool(state) and brief_at < state.start()
        if not named:
            continue
        if not (definite_us and "us" not in markets) and named & markets:
            continue
        findings.append(
            f"WARN_ROW_OUTSIDE_BRIEF_MARKET: row {index} (id={row.get('id')!r}) "
            f"has location {location!r}, which names {'/'.join(sorted(named))} "
            f"while brief.markets is {sorted(markets)}. Check the adapter's "
            "geography before keeping the row: `indeed` serves the US site only "
            "and resolves --location against a US gazetteer, so a search for "
            "London returns London, Ohio with classification `ok`. If the row "
            "really is in the brief's market, this line is the false alarm — "
            "leave it and say so.")
    return findings


def _check_caps(brief):
    """The yellow-tier caps in references/source-policy.md, as a check.

    This is that reference file's named backstop: its two numbers are the only
    part of the policy a program can decide, and without them the trigger in
    SKILL.md would point at a file nothing reports you for skipping.
    """
    findings = []
    for field, ceiling in (("max_rows_per_round", MAX_ROWS_PER_ROUND_CEILING),
                           ("max_pages_per_site", MAX_PAGES_PER_SITE_CEILING)):
        value = brief.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            findings.append(
                f"CAP_MISSING: brief.yaml has no positive integer `{field}`. "
                "The yellow-tier caps are what keep pagination and detail "
                "fan-out inside references/source-policy.md; a round without "
                "them is an uncapped one.")
        elif value > ceiling:
            findings.append(
                f"CAP_ABOVE_CEILING: brief.yaml {field}={value} exceeds the "
                f"yellow-tier ceiling of {ceiling} in "
                "references/source-policy.md. Read that file before raising "
                "it: the cap is the whole difference between two pages a human "
                "asked for and a crawl.")
    return findings


# The gates modes/discover.md Step 10 runs before this one. check_shortlist is
# the last gate in the mode, so it is the only place that can report a sibling
# that never ran — and until now it reported none of them, which left discover's
# two load-bearing invariants (read-only, and no predicted numbers) resting on
# scripts a run could simply not execute. check_assessment.py:181 does exactly
# this for assess; this is the same mechanism, same reason.
UPSTREAM_GATES = ("check_no_write", "check_candidate_match", "lint_no_prediction")
PASSING_VERDICTS = ("pass", "recorded")


def _check_upstream_receipts(workspace):
    findings = []
    # Every receipt was written by journal.receipt(), not by hand. Reported
    # rather than filtered: dropping a forged PASS would promote an older
    # genuine FAIL into last position and read as the current state.
    for gate_name, line_no in journal.unverified_receipts(workspace):
        findings.append(
            f"RECEIPT_UNVERIFIED: the {gate_name!r} receipt at gate-record "
            f"{line_no} does not match its own receipt_hash — it was hand-written "
            f"or edited after the gate ran, so it is not evidence that the gate ran")

    for gate in UPSTREAM_GATES:
        receipts = journal.read_receipts(workspace, gate)
        if not receipts:
            findings.append(
                f"MISSING_RECEIPT: no journal.jsonl receipt for {gate} — the "
                "gate was never run, and a skipped gate looks exactly like a "
                "clean one. Run the Step 10 block in order.")
            continue
        last = receipts[-1]
        if not journal.receipt_intact(last):
            continue  # Reported above; never promote an older passing receipt.
        if last.get("verdict") not in PASSING_VERDICTS:
            detail = "; ".join(last.get("findings") or []) or "no findings recorded"
            findings.append(
                f"UPSTREAM_FAILED: {gate} verdict={last.get('verdict')} ({detail})")
            continue
        # A verdict is a claim about a MOMENT; the receipt records which bytes it
        # was about. Without re-checking them, "lint_no_prediction passed" could be
        # true of a shortlist.md that has since been rewritten — or of a decoy run
        # against different files entirely — and discover's two load-bearing
        # invariants (read-only, and no predicted numbers) would rest on it.
        # check_apply._stale_inputs already solved this; same rule here.
        for label, recorded in sorted((last.get("input_hashes") or {}).items()):
            # journal.jsonl is excluded and must be: check_no_write records the
            # journal's OWN hash, and the act of writing that receipt appends to
            # the journal — so the recorded value is stale the instant it is
            # written, and every later gate would report STALE_RECEIPT on a
            # perfectly honest run. A self-referential hash is unverifiable by
            # construction, not by defect.
            if pathlib.Path(label).name == "journal.jsonl":
                continue
            candidate = pathlib.Path(label)
            if candidate.is_absolute() or ".." in candidate.parts:
                findings.append(
                    f"RECEIPT_INPUT_OUTSIDE_WORKSPACE: {gate} recorded {label!r}, "
                    f"which is not inside the workspace")
                continue
            path = workspace / label
            if not path.is_file():
                findings.append(
                    f"RECEIPT_INPUT_MISSING: {gate} passed on {label}, which is no "
                    f"longer in the workspace — re-run {gate}")
                continue
            if journal.sha256_file(path) != recorded:
                findings.append(
                    f"STALE_RECEIPT: {gate} passed on {label}@{str(recorded)[:12]} "
                    f"but disk now holds {journal.sha256_file(path)[:12]} — the file "
                    f"changed after the gate read it. Re-run {gate}")
    return findings


_MD_URL = re.compile(r"https?://[^\s)\]>\"'|]+")


_MD_SECTION = re.compile(r"^##\s*(§\S*)", re.M)
_MD_NUMBERED = re.compile(r"^\s*\d+\.\s+\*\*(.+?)\*\*", re.M)


def _md_candidates_section(md_text: str) -> str:
    """The §1 candidates block, or "" if the document has no sections.

    Scoped on purpose. Three of shortlist.md's four required sections are ABOUT
    sources and provenance — §0 names the raw captures, §0.1 the trigger, and the
    disclosure block names what was and was not obtainable — so a URL there is the
    honest thing to write. Treating every URL in the document as a claimed posting
    made the adapter's own documentation, a company careers page, or the raw-capture
    reference a hard failure, and the remedy the finding suggested was to delete the
    round's own provenance.
    """
    marks = list(_MD_SECTION.finditer(md_text or ""))
    for i, m in enumerate(marks):
        if m.group(1).startswith("§1"):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(md_text)
            return md_text[m.start():end]
    return ""


def _check_md_rows(md_text, rows):
    """Every posting rendered in §1 of shortlist.md must exist in shortlist.yaml.

    All of commit 55e4f84's provenance anchors run over `shortlist.yaml`.
    `shortlist.md` — hand-authored, no renderer, the only artifact a human reads
    and acts on — was checked for four narrow things and never reconciled row by
    row. A wholly invented posting present only in the .md passed both discover
    gates with a `pass` receipt.

    The sharpest way in was the gate's own remediation: modes/discover.md told the
    round to "delete the row" on a provenance finding and never said to delete it
    from the .md too, so the documented fix moved a fabricated row OUT of the
    checked file and LEFT it in the read one.

    Every rendered row also exposes its direct posting URL. A URL in YAML is
    evidence for a machine; the reader needs the same actionable link in §1.
    """
    section = _md_candidates_section(md_text)
    if not rows:
        # A "found nothing" round that still renders postings in §1 is the loudest
        # contradiction available, and the old early return made it invisible.
        rendered = len(_MD_NUMBERED.findall(section)) if section else 0
        if rendered:
            return [f"MD_ROW_COUNT_MISMATCH: shortlist.md §1 renders {rendered} "
                    f"posting(s) but shortlist.yaml carries no rows at all"]
        return []
    if not section:
        return []
    known_urls, rendered_stems = set(), set()
    for url in dict.fromkeys(_MD_URL.findall(section)):
        rendered_stems.add(url.split("?", 1)[0].split("#", 1)[0].rstrip("/.,;"))
    for row in rows:
        if not isinstance(row, dict):
            continue
        for field in ("url", "source_id", "id"):
            value = str(row.get(field) or "").strip()
            if value:
                known_urls.add(value)
                known_urls.add(value.split("?", 1)[0].split("#", 1)[0])

    findings = []
    for url in dict.fromkeys(_MD_URL.findall(section)):
        stem = url.split("?", 1)[0].split("#", 1)[0].rstrip("/.,;")
        if any(stem == k or stem in k or k in stem for k in known_urls if k):
            continue
        findings.append(
            f"MD_ROW_NOT_IN_SHORTLIST: shortlist.md §1 links {url!r}, which matches "
            "no row in shortlist.yaml.")
    for row in rows:
        if not isinstance(row, dict):
            continue
        url = str(row.get("url") or "").strip()
        if not url:
            continue  # `check_rows` reports the missing structured URL.
        stem = url.split("?", 1)[0].split("#", 1)[0].rstrip("/.,;")
        if stem not in rendered_stems:
            findings.append(
                f"MD_POSTING_URL_MISSING: shortlist.md §1 does not render the "
                f"direct URL for {row.get('id')!r}. Every candidate must show a "
                "clickable posting link, not only a source or search page.")
    # The COUNT is the anchor, not the title. Step 6 legitimately normalises a
    # row's title (de-duplication compares on a normalised form), which is why
    # `title` is not an anchored field anywhere else in this file and why
    # test_a_title_normalised_in_step_6_stays_quiet exists. Matching on it would
    # hard-fail an honest round that cleaned up a card's title — the cry-wolf this
    # gate cannot afford. A count mismatch still catches both real shapes: a
    # fabricated posting appended to the .md, and a row deleted from the .yaml
    # while left in the .md, which is the remediation trap.
    rendered = len(_MD_NUMBERED.findall(section))
    if rendered and rendered != len(rows):
        findings.append(
            f"MD_ROW_COUNT_MISMATCH: shortlist.md §1 renders {rendered} postings "
            f"but shortlist.yaml carries {len(rows)} rows")
    return findings


# Adapters paginate with different flags, and the repo's OWN linkedin fixture
# uses `--start`, not `--page` — so a `--page`-only reader let 300 result
# slots be crawled off one site under a declared cap of two, using the flag
# the honest fixture uses. `--start`/`--offset` are row offsets: each distinct
# value is a distinct page of results, which is exactly what the cap counts.
_PAGE_ARG = re.compile(r"--(?:page|start|offset|from)[= ]\s*(\d+)")
_OFFSET_ARG = re.compile(r"--(?:start|offset|from)[= ]\s*(\d+)")
_OFFSET_PAGE_SIZES = {"indeed": 10, "linkedin": 25}


def _pages_per_site(calls):
    """{site: {page numbers actually requested}} from the recorded command lines.

    DISTINCT page numbers, not a count of search calls: modes/discover.md Step 3
    tells the round to query in both languages, so two calls landing on page 1
    are two queries and one page. Counting calls would report that honest round
    as a crawl, and a cap that fires on correct behaviour gets raised until it
    fires on nothing.
    """
    pages: dict = {}
    for call in calls:
        site = str(call.get("site") or "").strip().casefold()
        if 'search_pages' in call:
            pages.setdefault(site, set()).update(call['search_pages'])
            continue
        if call.get("command") != "search" or call.get("exit_code") != 0:
            continue
        if call.get("action") == ACTION:
            page = call.get("page")
            if type(page) is int and page > 0:
                pages.setdefault(site, set()).add(page)
            continue
        found = _PAGE_ARG.search(str(call.get("command_line") or ""))
        # A search with no --page is page 1: that is what the platform returns.
        value = int(found.group(1)) if found else 1
        offset = _OFFSET_ARG.search(str(call.get("command_line") or ""))
        if offset:
            start = int(offset.group(1))
            width = _OFFSET_PAGE_SIZES.get(site)
            # Normalise known documented offsets to the same page numbers used
            # by browser captures. Non-aligned offsets must remain DISTINCT,
            # otherwise starts 0, 1, ... 9 all hide inside one counted page.
            if width and start % width == 0:
                value = start // width + 1
            elif start == 0:
                value = 1
            else:
                value = -(start + 1)
        pages.setdefault(site, set()).add(value)
    return pages


def _check_caps_against_the_run(brief, shortlist, rows, calls):
    """The half of the cap check that looks at what the round actually did.

    `_check_caps` validates that brief.yaml DECLARES numbers within the ceilings,
    and that was the whole of it: a round could declare `max_pages_per_site: 2`,
    journal thirteen paginated searches against one site, and exit 0. Only
    under-reporting fired. references/source-policy.md:78 states plainly that
    "the cap is enforced by a script", and it names this one — so the cap has to
    be compared to the run, not only to the ceiling.
    """
    findings = []
    max_pages = brief.get("max_pages_per_site")
    if isinstance(max_pages, int) and not isinstance(max_pages, bool) and max_pages >= 1:
        for site, pages in sorted(_pages_per_site(calls).items()):
            if len(pages) > max_pages:
                findings.append(
                    f"PAGES_ABOVE_CAP: {site} was searched across {len(pages)} "
                    f"pages ({', '.join(str(p) if p > 0 else 'offset:' + str(-p - 1) for p in sorted(pages))}) but "
                    f"brief.yaml declares max_pages_per_site={max_pages}. Two "
                    "pages of a keyword search a human asked for is not a "
                    "scrape; an uncapped crawl is, and the cap is the "
                    "difference — see references/source-policy.md.")
    max_rows = brief.get("max_rows_per_round")
    if isinstance(max_rows, int) and not isinstance(max_rows, bool) and max_rows >= 1:
        returned = {}
        retained = {}
        for row in rows:
            if isinstance(row, dict):
                site = str(row.get("source_site") or "").strip().casefold()
                retained[site] = retained.get(site, 0) + 1
        for call in calls:
            count = call.get("search_row_count", call.get("row_count"))
            if (('search_row_count' in call or
                 (call.get("command") == "search" and call.get("exit_code") == 0))
                    and type(count) is int and count >= 0):
                site = str(call.get("site") or "").strip().casefold()
                returned[site] = returned.get(site, 0) + count
        for site in sorted(set(returned) | set(retained)):
            count = max(returned.get(site, 0), retained.get(site, 0))
            if count > max_rows:
                findings.append(
                    f"ROWS_ABOVE_CAP: {site or '<unknown source>'} returned/retained "
                    f"{count} rows but its per-site max_rows_per_round={max_rows}. "
                    "Dropping rows from the shortlist does not undo retrieval.")
    return findings


def _check_detail_cap(shortlist, rows):
    findings = []
    exempt = {str(entry.get("id"))
              for entry in (shortlist.get("detail_fetch_exceptions") or [])
              if isinstance(entry, dict)}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        fetched = (row.get("quality") == "complete"
                   or row.get("extraction_method") == "adapter_detail")
        if (fetched and row.get("verdict") not in TOP_THREE
                and str(row.get("id")) not in exempt):
            findings.append(
                f"DETAIL_FETCH_OUT_OF_BAND: row {index} (id={row.get('id')!r}) "
                f"carries a detail fetch but verdict {row.get('verdict')!r} is "
                f"outside the top three ({', '.join(TOP_THREE)}). Detail "
                "fan-out is the yellow-layer cap. TWO causes, both recorded the "
                "same way in shortlist.yaml `detail_fetch_exceptions` with a "
                "reason: the user named this row, OR the fetch itself demoted "
                "it — a row fetched while it was still worth_applying, whose "
                "description then revealed a disqualifier, was in band at the "
                "moment it was fetched, and this check reads only the final "
                "verdict so it cannot see that ordering.")
    return findings



def _normalise_query(text) -> str:
    """Casefolded, whitespace-collapsed, for comparing a declared query against
    the command line that ran it.

    Byte equality would be the wrong test. The brief and the command line are
    written by the same model at different moments, so "Machine Learning
    Engineer" in one and "machine learning engineer" in the other is the SAME
    query — and a gate that reported that as a skipped track would be crying
    wolf on a round that did exactly what it declared.
    """
    return " ".join(str(text or "").casefold().split())


def _declared_queries_never_run(brief, shortlist, calls):
    """Declared in brief.target_titles, absent from every adapter command line,
    and not named in shortfall_reason.

    MEASURED: a round declared ten query strings and ran one. The first English
    query reached the per-site row cap on its own, so the Dutch-language and
    medical-imaging queries were never issued — two of the three tracks the user
    asked for. `target_titles` is documented as what makes a round reproducible
    and nothing read it, so the gap surfaced only because the operator wrote it
    into shortfall_reason by hand.

    The rule is not "run everything". A round may hit a cap, lose a source, or
    stop early. It is: if you declared it and did not run it, SAY SO — the same
    bar SHORTFALL_NO_REASON already sets for row counts, applied to coverage.
    """
    # A brief that declares nothing falls out below rather than being guarded
    # here: with no declared queries there is nothing to be missing, so an early
    # return would be a branch no input can distinguish — dead code that reads
    # as a safeguard. (Mutation testing found exactly that: `if False` here
    # changed no result.)
    declared = [q for q in (brief.get("target_titles") or [])
                if _normalise_query(q)]
    ran = " \u0000 ".join(_normalise_query(c.get("query") if c.get("action") in (ACTION, 'search_call')
                                         else c.get("command_line")) for c in calls)
    excused = _normalise_query(shortlist.get("shortfall_reason"))
    missing = [q for q in declared
               if _normalise_query(q) not in ran
               and _normalise_query(q) not in excused]
    if not missing:
        return []
    # ONE finding listing them, not one per query: a round that ran nothing
    # would otherwise bury its real problem under a line per declared title.
    return ["QUERIES_DECLARED_NOT_RUN: brief.target_titles declares "
            f"{len(declared)} quer(ies) and {len(missing)} of them appear in no "
            "adapter call and in no shortfall_reason: "
            + "; ".join(repr(q) for q in missing)
            + ". A declared query that was never issued is a coverage gap the "
              "reader cannot see: the shortlist looks like an answer to the whole "
              "brief. Run them, or name them in shortfall_reason and say why."]


def _check_browser_rows(workspace, rows, calls, brief, exceptions=()):
    findings = []
    evidence = {}
    browser_sites = {c.get("site") for c in calls if c.get("action") == ACTION}
    adapter_sites = {c.get("site") for c in calls if c.get("action") == "adapter_call"}
    detail_ids = set()
    exempt = {str(e.get("id")) for e in exceptions if isinstance(e, dict)}
    for call in calls:
        if call.get("action") != ACTION or validate_record(call, workspace):
            continue
        data = json.loads((workspace / call["rows_file"]).read_text(encoding="utf-8"))
        if call["command"] == "detail":
            detail_ids.update((call["site"], r["source_id"]) for r in data)
        evidence.setdefault(call["site"], []).extend(
            dict(row, retrieved_at=call["retrieved_at"]) for row in data)
    for row in rows:
        if not isinstance(row, dict):
            continue
        if ((row.get("source_site"), row.get("source_id")) in detail_ids
                and row.get("verdict") not in TOP_THREE and str(row.get("id")) not in exempt):
            findings.append("DETAIL_FETCH_OUT_OF_BAND: browser detail fetch requires a top-three verdict or recorded exception")
        if row.get("extraction_method") == "browser_page":
            candidates = evidence.get(row.get("source_site"), [])
            if not any(all(row.get(k) == captured.get(k) for k in
                           ("source_id", "url", "title", "raw_text", "retrieved_at"))
                       for captured in candidates):
                findings.append("BROWSER_ROW_NOT_CAPTURED: browser_page row must match its imported snapshot evidence")
        elif (row.get("source_site") in browser_sites
              and (row.get("extraction_method") == "public_page"
                   or row.get("source_site") not in adapter_sites)):
            findings.append("BROWSER_METHOD_MISMATCH: browser capture rows must use browser_page")
    # Search rows (including repeat pages) are counted by _check_caps_against_the_run.
    # Detail identities remain evidence, not additional search results.
    return findings


def check_run(workspace, shortlist, brief, md_text, calls):
    from search_capture import ACTION as SEARCH_ACTION, validate_record as validate_search
    findings = check_stop_order(calls)
    for call in calls:
        if call.get("action") == ACTION:
            findings.extend(validate_record(call, workspace))
        if call.get('action') == SEARCH_ACTION:
            findings.extend(validate_search(call, workspace))
    rows = shortlist.get("rows") or []
    if any(isinstance(row, dict) and row.get('source_site') == 'anysearch' for row in rows):
        findings.append('SEARCH_LEAD_NOT_POSTING: AnySearch snippets require an original posting capture before shortlisting')
    ok_calls = [c for c in calls
                if c.get("classification") == "ok" and c.get("exit_code") == 0]

    if not calls:
        findings.append(
            "NO_ADAPTER_RECEIPTS: journal.jsonl records no adapter_call, browser_call or search_call at all, "
            "so nothing in this workspace can be traced to a live retrieval. "
            "Every adapter invocation goes through "
            "scripts/check_opencli_result.py; browser snapshots go through "
            "scripts/record_browser_capture.py.")

    if not str(brief.get("trigger_reason") or "").strip():
        findings.append(
            "NO_TRIGGER_REASON: brief.yaml has no trigger_reason. The reason for "
            "searching is stated BEFORE the search and written into the brief.")
    if "§0.1" not in md_text:
        findings.append(
            "NO_TRIGGER_SECTION: shortlist.md has no `§0.1` section carrying the "
            "trigger reason")

    target = brief.get("target_count")
    if isinstance(target, int) and len(rows) < target and not str(
            shortlist.get("shortfall_reason") or "").strip():
        findings.append(
            f"SHORTFALL_NO_REASON: brief.target_count is {target} but the "
            f"shortlist has {len(rows)} rows and shortfall_reason is empty. "
            "Write the reason — never pad the count.")

    findings.extend(_declared_queries_never_run(brief, shortlist, calls))

    findings.extend(_check_caps(brief))

    has_detail = any(isinstance(row, dict) and row.get("quality") == "complete"
                     for row in rows)
    required_stamp = DETAIL_PROVISIONAL_STAMP if has_detail else PROVISIONAL_STAMP
    if rows and not _says(md_text, *required_stamp):
        findings.append(
            "MD_MISSING_PROVISIONAL_STAMP: shortlist.md renders rows without the "
            f"「{_both(required_stamp)}」 label — use the spelling of the "
            "language the round is written in. `provisional: true` in "
            "shortlist.yaml is the machine half of the stamp and no reader ever "
            "sees it; this is the half they do see, and a discover verdict may "
            "not be rendered without it.")

    if not rows:
        claims = absence_claims(md_text)
        hit = claims[0][0] if claims else None
        if hit and not ok_calls:
            findings.append(
                f"EMPTY_RESULT_UNSUPPORTED: shortlist.md says {hit!r} but "
                "journal.jsonl records no adapter call that exited 0. "
                "All-adapters-failed and found-nothing have the identical "
                "shape; only the receipts tell them apart.")
        if not ok_calls:
            findings.extend(_check_disclosure(md_text))

    findings.extend(_check_upstream_receipts(workspace))
    findings.extend(_check_caps_against_the_run(brief, shortlist, rows, calls))
    findings.extend(_check_md_rows(md_text, rows))
    findings.extend(_check_sources(workspace, shortlist, rows, calls))
    findings.extend(_check_detail_cap(shortlist, rows))
    findings.extend(_check_browser_rows(workspace, rows, calls, brief,
                                        shortlist.get("detail_fetch_exceptions") or []))
    findings.extend(_check_listing_sources(workspace, rows, calls))
    findings.extend(_check_market_fit(brief, rows))
    return findings


def _check_mode_entry(workspace, skill_root):
    """modes/discover.md is layer 1.5, and this is what reports it was not read.

    Mirrors check_apply.py deliberately: the same two findings, the same
    meaning, in the gate that belongs to this mode. Four modes with four
    different words for the same failure would be four things to learn.
    """
    findings = []
    entry = enter_mode.latest_mode_entry(workspace, MODE)
    mode_path = paths.mode_file(MODE, skill_root)   # mode first, root second
    if entry is None:
        findings.append(
            "NO_MODE_ENTRY: journal.jsonl has no mode_entry for discover. "
            "modes/discover.md is loaded unconditionally on entering the mode — "
            "it is the only definition of the brief, shortlist and preferences "
            "schemas — and this record is the only thing that reports it was "
            "not. Run `python3 scripts/enter_mode.py --workspace <ws> --mode "
            "discover`, then read the file.")
    elif not mode_path.is_file():
        # `mode_path.is_file()` guarded the comparison, so a wrong --skill-root
        # switched the layer-1.5 backstop off and reported nothing at all.
        findings.append(
            f"MODE_FILE_MISSING: {mode_path} is not on disk, so the hash recorded "
            "at mode entry could not be checked against it; point --skill-root at "
            "the skill")
    elif entry.get("mode_file_sha256") != journal.sha256_file(mode_path):
        findings.append(
            "MODE_FILE_CHANGED: modes/discover.md changed after this run entered "
            "the mode, so the schema that was read is not the schema on disk. "
            "re-enter the mode and re-read it before trusting this shortlist.")
    return findings


def _fail_to_run(workspace, message):
    journal.receipt(workspace, GATE, {}, "could_not_run", [message])
    print(message, file=sys.stderr)
    return 2


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gate: the shortlist is real.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--skill-root", type=pathlib.Path,
                        default=paths.SKILL_ROOT,
                        help="repo root holding modes/ (default: paths.SKILL_ROOT)")
    args = parser.parse_args(argv)
    workspace = args.workspace

    if not workspace.is_dir():
        print(f"workspace not found: {workspace}", file=sys.stderr)
        return 2
    import online_presence
    notice = online_presence.step_notice(workspace)
    if notice:  # stderr only: a notice is not a finding and changes no exit code
        print(notice, file=sys.stderr)
    shortlist_path = workspace / "shortlist.yaml"
    if not shortlist_path.is_file():
        return _fail_to_run(workspace, f"missing input: {shortlist_path}")
    try:
        shortlist = journal.load_yaml(shortlist_path)
        journal.require_lists(shortlist, shortlist_path, rows=None, sources=dict,
                              detail_fetch_exceptions=dict)
    except journal.YamlUnreadable as exc:
        return _fail_to_run(workspace, exc.finding)

    brief_path = workspace / "brief.yaml"
    if not brief_path.is_file():
        return _fail_to_run(workspace, f"missing input: {brief_path}")
    try:
        brief = journal.load_yaml(brief_path)
        journal.require_lists(brief, brief_path, target_titles=str, markets=str)
    except journal.YamlUnreadable as exc:
        return _fail_to_run(workspace, exc.finding)

    md_path = workspace / "shortlist.md"
    md_text = (md_path.read_text(encoding="utf-8", errors="replace")
               if md_path.is_file() else "")
    journal_path = workspace / "journal.jsonl"

    raw_texts = load_raw_texts(workspace)
    findings = _check_mode_entry(workspace, args.skill_root)
    findings.extend(check_rows(shortlist, raw_texts))
    findings.extend(check_run(workspace, shortlist, brief, md_text,
                              read_retrieval_calls(workspace)))

    input_hashes = {"shortlist.yaml": journal.sha256_file(shortlist_path),
                    "brief.yaml": journal.sha256_file(brief_path)}
    if md_path.is_file():
        input_hashes["shortlist.md"] = journal.sha256_file(md_path)
    if journal_path.is_file():
        input_hashes["journal.jsonl"] = journal.sha256_file(journal_path)
    for site in sorted(raw_texts):
        for name in sorted(raw_texts[site]):
            input_hashes[f"raw/{name}"] = journal.sha256_file(
                workspace / "raw" / name)

    # The WARN_ split check_conventions.py and check_assessment.py already make:
    # a warning is recorded in the receipt and printed, and does not fail a run.
    hard = [f for f in findings if not f.startswith("WARN_")]
    journal.receipt(workspace, GATE, input_hashes,
                    "fail" if hard else "pass", findings)
    for line in findings:
        print(line)
    return 1 if hard else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
