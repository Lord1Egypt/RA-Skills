"""Strict parser for the two mock-assessor output blocks.

Fail-closed, for the same reason parse_verdicts.py is: a block we can only partly read
is not a block with a few odd lines, it is an assessment that did not happen. The
caller re-dispatches the pass rather than accepting a half-read one — and in
particular, a block with neither FINDING lines nor the explicit "FINDINGS: none"
marker is an error, because silence and "nothing found" must not look the same.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

ASSESSMENT = "MOCK-ASSESSMENT-V1"
PROVENANCE = "MOCK-PROVENANCE-V1"
BLOCK_KINDS = (ASSESSMENT, PROVENANCE)

HEADER_KEYS = {
    ASSESSMENT: ("ROUND", "ROUND-TYPE", "MARKET", "FAMILY"),
    PROVENANCE: ("ROUND",),
}
ALLOWED_RECORDS = {
    ASSESSMENT: ("FINDING", "BAND", "COVERAGE", "SHAPE"),
    PROVENANCE: ("FINDING",),
}
# Exactly one free-text field per record, and it is always last, so it may contain
# the pipe character a real quote sometimes contains.
RECORD_FIELDS = {
    "FINDING": ("tag", "ref", "quote"),
    "BAND": ("dimension", "value", "ref", "quote"),
    "COVERAGE": ("status", "must_have"),
    "SHAPE": ("status", "round_name"),
}
NONE_MARKER = "FINDINGS: none"


class BlockParseError(ValueError):
    """The block is not exactly the contracted shape."""


@dataclass(frozen=True)
class Record:
    kind: str
    fields: dict
    line_no: int


@dataclass(frozen=True)
class Block:
    kind: str
    header: dict
    records: tuple
    findings_none: bool


def extract_block(text: str, kind: str) -> list[str]:
    if kind not in BLOCK_KINDS:
        raise ValueError(f"unknown block kind {kind!r}")
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.strip() == kind]
    ends = [i for i, ln in enumerate(lines) if ln.strip() == "END-" + kind]
    if len(starts) != 1 or len(ends) != 1:
        raise BlockParseError(
            f"{kind}: expected exactly one start and one end sentinel, "
            f"found {len(starts)} start and {len(ends)} end"
        )
    if ends[0] < starts[0]:
        raise BlockParseError(f"{kind}: END sentinel appears before the start sentinel")
    return lines[starts[0] + 1:ends[0]]


def _parse_record(key: str, payload: str, line_no: int) -> Record:
    names = RECORD_FIELDS[key]
    parts = payload.split(" | ", len(names) - 1)
    if len(parts) != len(names):
        raise BlockParseError(
            f"line {line_no}: {key} must have fields "
            + " | ".join(n + "=" for n in names)
        )
    fields = {}
    for position, (name, part) in enumerate(zip(names, parts), start=1):
        prefix = name + "="
        if not part.startswith(prefix):
            raise BlockParseError(
                f"line {line_no}: expected field {name!r} at position {position}, "
                f"got {part[:24]!r}"
            )
        fields[name] = part[len(prefix):].strip()
    return Record(key, fields, line_no)


def parse_block(text: str, kind: str) -> Block:
    body = extract_block(text, kind)
    header: dict = {}
    records: list = []
    findings_none = False
    for offset, raw in enumerate(body, start=1):
        line = raw.strip()
        if not line:
            continue
        if line == NONE_MARKER:
            findings_none = True
            continue
        if ":" not in line:
            raise BlockParseError(f"line {offset}: not a record: {line[:40]!r}")
        key, payload = line.split(":", 1)
        key, payload = key.strip(), payload.strip()
        if key in HEADER_KEYS[kind]:
            if key in header:
                raise BlockParseError(f"line {offset}: duplicate header {key}")
            header[key] = payload
            continue
        if key in ALLOWED_RECORDS[kind]:
            records.append(_parse_record(key, payload, offset))
            continue
        raise BlockParseError(
            f"line {offset}: unknown record {key!r} in {kind} (allowed: "
            + ", ".join(HEADER_KEYS[kind] + ALLOWED_RECORDS[kind])
            + ")"
        )
    missing = [k for k in HEADER_KEYS[kind] if k not in header]
    if missing:
        raise BlockParseError(f"{kind}: missing header line(s) {', '.join(missing)}")
    has_findings = any(r.kind == "FINDING" for r in records)
    if has_findings == findings_none:
        raise BlockParseError(
            f"{kind}: emit either FINDING lines or the single line '{NONE_MARKER}' "
            "— never both and never neither"
        )
    return Block(kind, header, tuple(records), findings_none)


_WS = re.compile(r"\s+")
_ELLIPSIS = re.compile(r"\.\.\.|…|\[\.\.\.\]")
MIN_SEGMENT = 8
# The question headings a transcript is divided by. check_mock.transcript_refs
# uses the same shape to collect the ref set; this copy exists because the
# splitting has to happen where the quote helpers live, and both are pinned
# against each other by test_mock_blocks.py.
# `Q\d+[A-Za-z]?` so a sub-question heading (`## Q3b — follow-up`) is seen.
# With `Q\d+\b` the reconciliation stated as fact something the reader can see
# is false ("has no '## Q3b' heading"), and the Q3b answer became unquotable at
# the same time — a bypass and a cry-wolf from one regex.
_Q_HEADING_FULL = re.compile(r"^##\s+(Q\d+[A-Za-z]?)\b", re.M)


def collapse_ws(s: str) -> str:
    return _WS.sub(" ", s).strip()


def normalize_quote(s: str) -> str:
    """Collapse whitespace and strip one layer of surrounding quotation marks."""
    s = collapse_ws(s)
    if len(s) >= 2 and s[0] in "\"“'‘" and s[-1] in "\"”'’":
        s = collapse_ws(s[1:-1])
    return s


def quote_segments(quote: str) -> list[str]:
    """Every non-empty piece of the quote, split on the assessor's elisions.

    Nothing is discarded for being short. The previous version kept only segments
    of at least MIN_SEGMENT characters *whenever a longer one existed*, so
    `"I owned the recon pipeline ... at NASA ... and shipped it in March"` was
    checked as its two long halves and `at NASA` was never compared to anything.
    Every fabricated number, employer and acronym is short: `40%`, `n=200`,
    `MDR`, `p<0.05`, `at GE`. In Chinese the threshold was worse than in English —
    `带过五人团队` is a complete claim in six characters.

    A short quote is still a quote: `"we did"` is terse, not fabricated, and
    rejecting it would report honest assessors as liars. The defect was never
    that short text is unconvincing — it is that short text went UNCHECKED.
    Every segment is now compared; MIN_SEGMENT is retained only as documentation
    of the old threshold and for tests that pin this history.
    """
    whole = normalize_quote(quote)
    if not whole:
        return []
    return [s for s in (collapse_ws(p) for p in _ELLIPSIS.split(whole)) if s]


def quote_is_in(quote: str, haystack: str) -> bool:
    """True when the quote's segments appear in `haystack`, IN ORDER.

    Two changes from the substring-anywhere test this replaces, both of which were
    reachable with the gate green:

      * order. `all(seg in hay)` accepted a sentence assembled backwards out of
        two different answers — Q3's clause followed by Q1's — as a verbatim
        quote. An elision means "I left something out here", not "these phrases
        occur somewhere in this document", so the segments must advance.
      * no length filter (see `quote_segments`).

    Scoping the haystack to the cited answer is the caller's job — `_check_quote`
    in check_mock.py — because only the caller knows which `ref=` was given.
    """
    segments = quote_segments(quote)
    if not segments:
        return False
    hay = collapse_ws(haystack)
    at = 0
    for seg in segments:
        found = hay.find(seg, at)
        if found < 0:
            return False
        at = found + len(seg)
    return True


_SPEAKER = re.compile(r"^\*\*([^*:]+):\*\*", re.M)
CANDIDATE_SPEAKER = "candidate"


def transcript_sections(text: str) -> dict:
    """`{"Q1": "<the text under that heading>", ...}`.

    A quote has to come from the answer it cites. Searching the whole transcript
    let a finding about Q1 be "evidenced" by words the candidate said in Q3 — or
    by the interviewer's own question, which is the worst version, because the
    candidate then rewrites a real CV bullet against a sentence they never said.
    """
    sections: dict = {}
    matches = list(_Q_HEADING_FULL.finditer(text or ""))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[m.group(1)] = text[m.end():end]
    return sections


def candidate_only(section: str) -> str:
    """The candidate's own turns within one section.

    Falls back to the whole section when the transcript carries no `**Speaker:**`
    markers at all. That fallback is deliberate: the marker convention is
    described in modes/interview.md but enforced nowhere, and a stricter reading
    would report every quote in an otherwise valid round as fabricated — the
    cry-wolf failure, which is how a gate gets switched off. Section scoping
    still applies in that case, so the cross-answer splice stays closed.
    """
    speakers = list(_SPEAKER.finditer(section or ""))
    if not speakers:
        return section or ""
    out = []
    for i, m in enumerate(speakers):
        if m.group(1).strip().lower() != CANDIDATE_SPEAKER:
            continue
        end = speakers[i + 1].start() if i + 1 < len(speakers) else len(section)
        out.append(section[m.end():end])
    if not out:
        # Markers exist but none of them says "Candidate" — a transcript that
        # labels its turns by persona name, by role, or in another language.
        # Returning "" here made EVERY quote in an otherwise honest round fail
        # at once, with the loudest possible accusation ("does not appear in the
        # candidate's answer"). That is the cry-wolf this fallback exists to
        # prevent, and it has to key on "no candidate turn was FOUND", not on
        # "no markers at all" — the narrower condition was the bug.
        return section or ""
    return "\n".join(out)
