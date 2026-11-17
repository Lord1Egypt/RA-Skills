#!/usr/bin/env python3
"""Gate for the interview mode.

Usage:
    python3 scripts/check_mock.py --workspace <application dir> --round <n>
                                  [--answer-bank <path>] [--today YYYY-MM-DD]

exit 0 — the round holds up.
exit 1 — findings printed to stdout, one per line, each with a stable UPPERCASE code.
exit 2 — could not run (a required input is missing, or a cross-plan module is absent);
         message to stderr. Never a silent skip: a check that did not run must not look
         like a check that passed.

Every exit path appends exactly one receipt to <workspace>/journal.jsonl, with verdict
"pass", "fail" or "could_not_run". Two exceptions, both deliberate: if the workspace
directory does not exist there is nowhere to append to, so the gate prints to stderr and
exits 2 with no receipt (creating the directory would materialise a workspace on a typo);
and if the receipt write itself fails, the gate exits 2 with RECEIPT_WRITE_FAILED rather
than exiting 0 having recorded nothing, because a gate that leaves no receipt is
indistinguishable from a gate nobody ran.

Required *inputs* are the transcript and the assessment. Everything else this gate reads
(question-log.yaml, answer-bank.md, interview-brief.md, claims.yaml) is a required
*output* of the mode — its absence is the defect, so it is a finding, not an exit 2.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import sys


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import enter_mode
import journal
import mock_blocks as MB
import mock_vocab as V
import paths

GATE = "check_mock"
MODE = "interview"
_AUTO = object()


class ReceiptFailed(RuntimeError):
    """The receipt could not be written — the run has no evidence it happened."""


class InputMissing(RuntimeError):
    """A required input file is absent — the gate has nothing to check."""


class MissingDependency(RuntimeError):
    """A cross-plan module is absent — the gate cannot honestly claim to have run."""


# ----------------------------------------------------------------- transcript helpers

# `Q\d+[A-Za-z]?` so a sub-question heading (`## Q3b — follow-up`) is seen.
# With `Q\d+\b` the reconciliation stated as fact something the reader can see
# is false ("has no '## Q3b' heading"), and the Q3b answer became unquotable at
# the same time — a bypass and a cry-wolf from one regex.
_Q_HEADING = re.compile(r"^##\s+(Q\d+[A-Za-z]?)\b", re.M)


def transcript_refs(text: str) -> set:
    return set(_Q_HEADING.findall(text))


# ----------------------------------------------------------------- the layer-1.5 backstop

def check_mode_entry(workspace: pathlib.Path, skill_root: pathlib.Path) -> list:
    """modes/interview.md is loaded unconditionally on entering the mode, and the
    journal record is the only thing that reports it if it was not. Mirrors
    check_apply.py exactly — one mechanism, four modes."""
    entry = enter_mode.latest_mode_entry(workspace, MODE)
    mode_path = paths.mode_file(MODE, skill_root)
    if entry is None:
        return [
            f"NO_MODE_ENTRY: journal.jsonl has no mode_entry for {MODE} — "
            f"modes/{MODE}.md is loaded unconditionally on entering the mode; run "
            f"scripts/enter_mode.py --mode {MODE} and read it"
        ]
    findings = [
        f"RECEIPT_UNVERIFIED: the {gate_name!r} receipt at gate-record {line_no} "
        f"does not match its own receipt_hash — it was hand-written or edited "
        f"after the gate ran, so it is not evidence that the gate ran"
        for gate_name, line_no in journal.unverified_receipts(workspace)]
    if not mode_path.exists():
        return findings + [
            f"MODE_FILE_MISSING: {mode_path} is not on disk, so the hash recorded "
            f"at mode entry could not be checked against it. `mode_path.exists()` "
            f"was a silent skip: a wrong --skill-root disabled the layer-1.5 "
            f"backstop entirely and the gate reported nothing"
        ]
    if entry.get("mode_file_sha256") != journal.sha256_file(mode_path):
        return findings + [
            f"MODE_FILE_CHANGED: modes/{MODE}.md changed after this run entered the "
            "mode, so what was read is not what is on disk — re-enter the mode and "
            "re-read it"
        ]
    return findings


# ----------------------------------------------------------------- assessment checks

def _check_headers(block, round_no: int, findings: list) -> None:
    label = block.kind
    raw = block.header.get("ROUND", "")
    if not raw.isdigit():
        findings.append(f"BAD_ROUND: {label}: ROUND: {raw!r} is not an integer")
    elif int(raw) != round_no:
        findings.append(
            f"ROUND_MISMATCH: {label}: ROUND: {raw}, but the gate was run with "
            f"--round {round_no} — one of the two is looking at the wrong round"
        )
    if block.kind != MB.ASSESSMENT:
        return
    round_type = block.header.get("ROUND-TYPE", "")
    if round_type not in V.ROUND_TYPES:
        findings.append(
            f"UNKNOWN_ROUND_TYPE: {round_type!r} is not one of "
            + " | ".join(V.ROUND_TYPES)
        )
    market = block.header.get("MARKET", "")
    if market not in V.MOCK_MARKET_KEYS:
        findings.append(
            f"UNKNOWN_MARKET: {market!r} is not one of "
            + " | ".join(V.MOCK_MARKET_KEYS)
        )
    if not block.header.get("FAMILY", "").strip():
        findings.append(
            "NO_FAMILY: the assessment block has an empty FAMILY line — the "
            "family-conditional tags cannot be checked without it"
        )


def _check_quote(record, label: str, transcript: str, refs: set, findings: list) -> None:
    what = record.fields.get("tag") or record.fields.get("dimension") or record.kind
    quote = record.fields.get("quote", "")
    ref_field = record.fields.get("ref", "")
    # The quote must come from the answer it cites, spoken by the candidate.
    # Searching the whole transcript let a Q1 finding be evidenced by Q3's words,
    # or by the interviewer's own question — and the candidate then edits a real
    # CV bullet against a sentence they never said. When the ref is unusable the
    # whole transcript is still the haystack: UNKNOWN_REF below reports the ref
    # itself, and reporting the same defect twice trains both findings away.
    haystack, where = transcript, "the transcript"
    if ref_field and ref_field in refs:
        section = MB.transcript_sections(transcript).get(ref_field)
        if section is not None:
            haystack = MB.candidate_only(section)
            where = f"the candidate's answer at {ref_field}"
    if not MB.normalize_quote(quote):
        findings.append(
            f"NO_QUOTE: {label} line {record.line_no}: {record.kind} {what} has an "
            "empty quote= — no quote, no tag"
        )
    elif not MB.quote_is_in(quote, haystack):
        findings.append(
            f"QUOTE_NOT_IN_TRANSCRIPT: {label} line {record.line_no}: "
            f"{MB.normalize_quote(quote)[:70]!r} does not appear, in that order, in "
            f"{where}"
        )
    ref = ref_field
    # `refs` empty means the transcript has no question headings at all; that is
    # reported once, by check_assessment, rather than N times here.
    if refs and ref not in refs:
        findings.append(
            f"UNKNOWN_REF: {label} line {record.line_no}: {ref!r} is not a question "
            "heading in the transcript"
        )


def _check_tag(record, block, findings: list) -> None:
    label = block.kind
    tag = record.fields["tag"]
    allowed = V.TRANSCRIPT_TAGS if label == MB.ASSESSMENT else V.PROVENANCE_TAGS
    if tag not in V.ALL_TAGS:
        findings.append(
            f"UNKNOWN_TAG: {label} line {record.line_no}: {tag!r} is not in the closed "
            "set — see references/interview-shapes.md"
        )
        return
    if tag not in allowed:
        findings.append(
            f"WRONG_PASS: {label} line {record.line_no}: {tag} may only be emitted by "
            + ("the provenance pass" if label == MB.ASSESSMENT else "the transcript pass")
            + " — that pass holds the inputs this tag is decided from"
        )
        return
    if label != MB.ASSESSMENT:
        return
    market = block.header.get("MARKET", "")
    family = block.header.get("FAMILY", "").strip().lower()
    markets = V.MARKET_CONDITIONAL.get(tag)
    if markets and market not in markets:
        findings.append(
            f"TAG_NOT_APPLICABLE: {label} line {record.line_no}: {tag} applies only in "
            f"market(s) {', '.join(markets)}, this round is MARKET: {market}"
        )
    families = V.FAMILY_CONDITIONAL.get(tag)
    if families and family not in families:
        findings.append(
            f"TAG_NOT_APPLICABLE: {label} line {record.line_no}: {tag} applies only to "
            f"family {', '.join(families)}, this round is FAMILY: {family}"
        )


def _check_band(record, label: str, findings: list) -> None:
    dimension = record.fields["dimension"]
    value = record.fields["value"]
    if dimension not in V.DIMENSIONS:
        findings.append(
            f"UNKNOWN_DIMENSION: {label} line {record.line_no}: {dimension!r} is not "
            "one of " + " | ".join(V.DIMENSIONS)
        )
    if value == V.NON_BAND_FLAG:
        findings.append(
            f"NOT_A_BAND: {label} line {record.line_no}: {V.NON_BAND_FLAG!r} is a flag, "
            "not a band — emit it as tag=CONTRADICTED from the provenance pass"
        )
    elif value not in V.BANDS:
        findings.append(
            f"UNKNOWN_BAND: {label} line {record.line_no}: {value!r} is not one of "
            + " | ".join(V.BANDS)
            + " (the bands are unnumbered on purpose)"
        )


def _must_haves(workspace: pathlib.Path) -> tuple:
    """(must-haves from posting.yaml, findings about the posting itself).

    Read rather than counted. A bare "the block must carry at least one COVERAGE
    row" pressures an under-producing assessor to invent a must-have to satisfy it;
    naming the one that has no row does not, and it is the same list modes/
    interview.md §2 tells the round to build its questions from.
    """
    path = workspace / "posting.yaml"
    if not path.exists():
        return [], [
            f"NO_POSTING: {path} is missing — modes/interview.md reads posting.yaml, "
            "the transcript pass is handed it, and without it the round's COVERAGE "
            "rows cannot be checked against anything at all"
        ]
    try:
        posting = journal.load_yaml(path)
        journal.require_lists(posting, path, must_haves=str)
    except journal.YamlUnreadable as exc:
        return [], [f"POSTING_UNPARSEABLE: {exc}"]
    rows = [str(m).strip() for m in (posting.get("must_haves") or []) if str(m).strip()]
    if not rows:
        return [], [
            f"NO_MUST_HAVES: {path.name} lists no must_haves, so there is nothing for "
            "the round's coverage to be checked against — re-extract the posting "
            "(references/job-posting-extraction.md defaults an unqualified "
            "requirement to must_have)"
        ]
    return rows, []


def _coverage_findings(block, must_haves: list) -> list:
    """One COVERAGE row per must-have, matched loosely on purpose.

    The assessor copies the must-have out of posting.yaml by hand, so a trailing
    period or a collapsed line wrap is not a missing row — and a check that fires on
    those is one the reader learns to skip. Same tolerance check_letter.py already
    uses for the employer name: normalise, then accept either containment direction.
    """
    def norm(text: str) -> str:
        return MB.collapse_ws(str(text)).strip(" .。;；,，").casefold()

    covered = [norm(r.fields["must_have"]) for r in block.records
               if r.kind == "COVERAGE" and norm(r.fields["must_have"])]
    findings = []
    for must in must_haves:
        wanted = norm(must)
        if not any(wanted in row or row in wanted for row in covered):
            findings.append(
                f"NO_COVERAGE_ROW: no COVERAGE row for the must-have {must!r} — the "
                "round either did not ask about it or the assessor did not say so, "
                "and `not_asked` is a status the block can state"
            )
    return findings


def check_assessment(assessment_text: str, transcript_text: str, round_no: int,
                     must_haves=None):
    """Returns ({block kind: Block}, findings)."""
    findings: list = []
    blocks: dict = {}
    for kind in (MB.ASSESSMENT, MB.PROVENANCE):
        if kind not in assessment_text:
            findings.append(
                f"MISSING_BLOCK: {kind} — that assessment pass did not run, or its "
                "block was not copied into the file verbatim"
            )
            continue
        try:
            blocks[kind] = MB.parse_block(assessment_text, kind)
        except MB.BlockParseError as exc:
            findings.append(
                f"PARSE_FAIL: {exc} — the round is void; re-dispatch that pass rather "
                "than hand-editing its block"
            )
    refs = transcript_refs(transcript_text)
    if not refs and any(block.records for block in blocks.values()):
        # Without headings the ref= check has nothing to compare against and would
        # pass everything in silence. The headings are required by modes/interview.md,
        # so their absence is the defect — not a licence to skip the check.
        findings.append(
            "NO_QUESTION_HEADINGS: the transcript has no '## Q<n>' headings, so every "
            "ref= in the assessment is unverifiable — modes/interview.md §3 requires "
            "one heading per question"
        )
    for kind, block in blocks.items():
        _check_headers(block, round_no, findings)
        for record in block.records:
            if record.kind == "FINDING":
                _check_tag(record, block, findings)
                _check_quote(record, kind, transcript_text, refs, findings)
            elif record.kind == "BAND":
                _check_band(record, kind, findings)
                _check_quote(record, kind, transcript_text, refs, findings)
            elif record.kind == "COVERAGE":
                if record.fields["status"] not in V.COVERAGE_STATUS:
                    findings.append(
                        f"UNKNOWN_STATUS: {kind} line {record.line_no}: COVERAGE "
                        f"status {record.fields['status']!r} is not one of "
                        + " | ".join(V.COVERAGE_STATUS)
                    )
            elif record.kind == "SHAPE":
                if record.fields["status"] not in V.SHAPE_STATUS:
                    findings.append(
                        f"UNKNOWN_STATUS: {kind} line {record.line_no}: SHAPE status "
                        f"{record.fields['status']!r} is not one of "
                        + " | ".join(V.SHAPE_STATUS)
                    )

    # ── the assessment must actually assess something ──────────────────────────
    #
    # Headers plus `FINDINGS: none` in both blocks used to be a fully passing round,
    # and modes/interview.md §7 tells the model to read that exit 0 as "the round
    # holds up". Nothing required a BAND, a COVERAGE row or a SHAPE row, so an
    # assessor that produced nothing produced a pass — and emptying the block also
    # disarmed NO_QUESTION_HEADINGS above, which is gated on `any(block.records)`.
    #
    # ON THE ASSESSMENT BLOCK ONLY. MOCK-PROVENANCE-V1 legitimately carries ROUND:
    # plus FINDINGS: none — that is its documented clean shape, and BAND and SHAPE
    # are not even in its ALLOWED_RECORDS. Firing on it would be the cry-wolf that
    # makes both codes noise on every honest round.
    #
    # Gated on the block having PARSED, so a timed-out assessor keeps reporting only
    # MISSING_BLOCK: three more codes beside it would send the reader looking for a
    # half-written block that is not there at all.
    block = blocks.get(MB.ASSESSMENT)
    if block is not None:
        if not any(r.kind == "BAND" for r in block.records):
            findings.append(
                "NO_BANDS: the assessment block carries no BAND line. The five "
                "dimensions in references/interview-shapes.md are what the candidate "
                "rehearses against — an assessment with none of them has reported "
                "nothing about how the answers were shaped, only whether a defect was "
                "spotted"
            )
        if not any(r.kind == "SHAPE" for r in block.records):
            findings.append(
                "NO_SHAPE: the assessment block carries no SHAPE line. The loop shape "
                "is half of what this mode is for, and `cannot_simulate` is an "
                "accepted status — saying a round could not be run here is the honest "
                "answer, saying nothing is not"
            )
        if must_haves:
            findings += _coverage_findings(block, must_haves)
    return blocks, findings


# ----------------------------------------------------------------- question-log.yaml

def _parse_stamp(raw: str):
    """`opencli nowcoder detail` returns an ISO-8601 timestamp; accept a bare date too."""
    text = str(raw).strip().replace("Z", "")
    for cut in (len(text), 19, 10):
        try:
            return datetime.datetime.fromisoformat(text[:cut]).date()
        except ValueError:
            continue
    return None


def check_question_log(path: pathlib.Path, today: datetime.date,
                       refs: set = None) -> list:
    if not path.exists():
        return [
            f"NO_QUESTION_LOG: {path} is missing — modes/interview.md requires the log "
            "seeded before the round, and it is the only record of where a question came from"
        ]
    # A finding, not exit 2: the docstring's split holds — question-log.yaml is a
    # required OUTPUT of the mode, so anything wrong with it is the defect being
    # reported, not a reason the gate could not run.
    try:
        data = journal.load_yaml(path)
        journal.require_lists(data, path, rejected=dict)
    except journal.YamlUnreadable as exc:
        return [f"QUESTION_LOG_UNPARSEABLE: {exc}"]

    findings: list = []
    posting_country = str(data.get("posting_country") or "").strip().upper()
    if not posting_country:
        findings.append(
            "NO_POSTING_COUNTRY: question-log.yaml must record posting_country: <ISO-2>. "
            "Without it the country rule cannot fire, and a same-name different-entity "
            "post looks exactly like a right one"
        )
    questions = data.get("questions") or []
    if not isinstance(questions, list) or not questions:
        findings.append(f"QUESTION_LOG_EMPTY: {path} has no questions: list")
        questions = []

    for entry in questions:
        if not isinstance(entry, dict):
            findings.append(f"QUESTION_LOG_UNPARSEABLE: {path}: a questions: row is not a mapping")
            continue
        qid = entry.get("id", "?")
        source = entry.get("source")
        if source not in V.QUESTION_SOURCES:
            findings.append(
                f"UNKNOWN_QUESTION_SOURCE: {qid}: {source!r} is not one of "
                + " | ".join(V.QUESTION_SOURCES)
            )
        if source != "scraped":
            continue
        if not str(entry.get("source_id") or "").strip():
            findings.append(
                f"NO_SOURCE_ID: {qid}: a scraped question needs the id that "
                "`opencli nowcoder detail <id>` was called with"
            )
        use = str(entry.get("use") or "").strip()
        if use not in ("shape", "question"):
            findings.append(f"UNKNOWN_USE: {qid}: use: must be 'shape' or 'question'")
        stamp = str(entry.get("source_time") or "").strip()
        if not stamp:
            findings.append(
                f"NO_SOURCE_TIME: {qid}: copy the `time` field from `detail` — a search "
                "row is elided and undated, and one result set held posts 3 days and "
                "9.5 months old"
            )
        else:
            when = _parse_stamp(stamp)
            if when is None:
                findings.append(f"BAD_SOURCE_TIME: {qid}: {stamp!r} is not an ISO-8601 timestamp")
            elif (today - when).days > V.SCRAPED_SPECIFIC_MAX_AGE_DAYS and use == "question":
                findings.append(
                    f"STALE_SPECIFIC: {qid}: {stamp} is {(today - when).days} days old — "
                    "it may set shape only, never be quoted as a specific question"
                )
        entity = str(entry.get("entity_country") or "").strip().upper()
        if not entity:
            findings.append(
                f"NO_ENTITY_COUNTRY: {qid}: record which country's entity the post "
                "describes; the company name matching is not evidence that the process does"
            )
        elif posting_country and entity != posting_country and not entry.get("country_named_in_post"):
            findings.append(
                f"WRONG_COUNTRY: {qid}: the source describes the {entity} entity and the "
                f"posting is {posting_country} — move it to rejected: with "
                "reason: wrong_country unless the post itself names the posting's country"
            )

    for entry in data.get("rejected") or []:
        if not isinstance(entry, dict):
            continue
        reason = str(entry.get("reason") or "")
        if reason not in V.REJECT_REASONS:
            findings.append(
                f"UNKNOWN_REJECT_REASON: {entry.get('id', '?')}: {reason!r} is not one of "
                + " | ".join(V.REJECT_REASONS)
            )

    # Reconcile the log against what was actually asked. Without this the log is
    # only ever checked against itself, so every rule above — the country rule
    # included, which modes/interview.md calls the most dangerous failure this
    # source offers — binds only the rows the model chose to write down. Omitting
    # the row, or typing `source: generated` on a scraped one, switched all of
    # them off, and the agent deciding that is the same one that would make the
    # mistake.
    if refs is not None:
        logged = {str(e.get("id") or "").strip()
                  for e in questions if isinstance(e, dict)}
        for ref in sorted(refs - logged):
            findings.append(
                f"LOG_MISSING_QUESTION: {ref} was asked in the transcript but has no "
                f"questions: row in question-log.yaml — an unlogged question is one "
                f"whose source nobody recorded"
            )
        asked = {str(e.get("id") or "").strip() for e in questions
                 if isinstance(e, dict) and e.get("asked")}
        for qid in sorted(asked - refs):
            findings.append(
                f"LOG_QUESTION_NOT_ASKED: {qid} is logged with asked: true but has no "
                f"'## {qid}' heading in the transcript"
            )
    return findings


# ----------------------------------------------------------------- answer-bank.md

# `[ \t]` throughout, never `\s`: `\s` matches a newline, so `^\s*-\s*source:\s*\S+`
# happily matches an EMPTY "- source:" line by borrowing the "-" from the next bullet.
# That is the exact defect this check exists to catch, passing itself.
_AB_HEADING = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
_AB_SOURCE = re.compile(r"^[ \t]*-[ \t]*source:[ \t]*\S+", re.M)


def check_answer_bank(path: pathlib.Path) -> list:
    if not path.exists():
        return [
            f"NO_ANSWER_BANK: {path} is missing — the answer bank is the only artifact "
            "that compounds across applications, and modes/interview.md requires one "
            "entry per story banked this round (--answer-bank to point elsewhere)"
        ]
    text = path.read_text(encoding="utf-8")
    marks = list(_AB_HEADING.finditer(text))
    if not marks:
        return [f"NO_ANSWER_BANK_ENTRIES: {path} has no '## ' entries"]
    findings = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        body = text[mark.end():end]
        if not _AB_SOURCE.search(body):
            findings.append(
                f"ANSWER_NO_SOURCE: answer-bank.md entry {mark.group(1)!r} has no "
                "'- source:' line — an entry whose fact cannot be traced is worse than "
                "no entry, because the candidate will say it out loud believing it was vetted"
            )
    return findings


# ---------------------------------------------------------------- answer-guide.md

# Same `[ \t]` discipline as the answer bank above, and for the same measured
# reason: `\s` matches a newline, so an EMPTY "- source:" line passes by borrowing
# the hyphen from the next bullet.
_AG_HEADING = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
_AG_SOURCE = re.compile(r"^[ \t]*-[ \t]*source:[ \t]*\S+", re.M)
# `(\S.*?)` not `(\S+)`: an entry may serve several rows ("row: R1, R2"), and
# stopping at the first space would leave every row after the first unchecked --
# which is exactly the "launder the gap through the evidenced row" path.
_AG_ROW = re.compile(r"^[ \t]*-[ \t]*row:[ \t]*(\S.*?)[ \t]*$", re.M)
_AG_BASIS = re.compile(r"^[ \t]*-[ \t]*basis:[ \t]*(\S+)", re.M)
_AG_BASES = ("evidenced", "honest_gap")
# The two match values that mean the candidate has NOT done the thing. Kept as a
# tuple rather than inlined so the assessment schema and this gate name the same
# set in one place.
_UNEVIDENCED = ("gap", "no_evidence")


def _norm_row_id(value) -> str:
    """Row ids compare on trimmed casefold. `R1`, `r1` and `'R3 '` name one row to
    every human reading the file, and treating them as three was a silent skip:
    the lookup missed, `None` is not in `_UNEVIDENCED`, and the entry passed."""
    return " ".join(str(value or "").split()).casefold()


def _assessment_matches(workspace: pathlib.Path):
    """({normalised id: match}, duplicate_ids, error) from fit-assessment.yaml.

    Three outcomes, kept apart because they need different answers. No file at all
    is legitimate -- interview mode can be entered on a posting plus a CV -- and
    the caller says so. A file that will not parse is NOT that: `except Exception:
    return {}` turned a broken assessment into "there is no assessment", disabling
    GUIDE_GAP_AS_EVIDENCED while stderr reported the wrong reason. Duplicate ids
    make the lookup ambiguous, so they are reported rather than resolved by
    last-one-wins.
    """
    path = workspace / "fit-assessment.yaml"
    if not path.is_file():
        return {}, [], None
    try:
        data = journal.load_yaml(path)
    except Exception as exc:                       # noqa: BLE001 - reported, not swallowed
        return {}, [], f"{type(exc).__name__}: {exc}"
    rows = (data or {}).get("requirements")
    if not isinstance(rows, list):
        return {}, [], "requirements is not a list"
    matches, seen, duplicates = {}, set(), []
    for row in rows:
        if not isinstance(row, dict) or row.get("id") is None:
            continue
        key = _norm_row_id(row.get("id"))
        if key in seen and key not in duplicates:
            duplicates.append(str(row.get("id")).strip())
        seen.add(key)
        matches[key] = str(row.get("match"))
    return matches, duplicates, None


def check_answer_guide(path: pathlib.Path, workspace: pathlib.Path) -> tuple:
    """Findings, plus notices for what could not be cross-checked.

    The load-bearing check is the last one. Answer guidance is the step where the
    pressure to be USEFUL runs straight into the load-bearing rule: the questions
    that most need a good answer are exactly the ones the candidate has no evidence
    for, and a satisfying answer to those can only be written by inventing the
    experience. So an entry that serves a requirement the assessment scored `gap`
    or `no_evidence` may only be an honest-gap framing, and saying so is mechanical
    rather than a matter of tone.
    """
    findings: list = []
    notices: list = []
    if not path.exists():
        return findings, notices          # NO_ANSWER_GUIDE already covers absence
    text = path.read_text(encoding="utf-8")
    marks = list(_AG_HEADING.finditer(text))
    if not marks:
        return ([f"NO_ANSWER_GUIDE_ENTRIES: {path} has no '## ' entries"], notices)
    matches, duplicates, error = _assessment_matches(workspace)
    if error:
        findings.append(
            f"ASSESSMENT_UNREADABLE: fit-assessment.yaml could not be parsed "
            f"({error}), so no answer-guide.md entry could be checked for a gap "
            f"written up as evidenced experience. A check that could not run must "
            f"not look like one that passed")
    elif duplicates:
        findings.append(
            f"DUPLICATE_ROW_ID: fit-assessment.yaml declares {', '.join(duplicates)} "
            f"more than once, so an answer-guide entry naming it has no single match "
            f"value to be checked against")
    elif not matches:
        notices.append(
            "NO_ASSESSMENT_TO_CHECK_AGAINST: fit-assessment.yaml is absent or has no "
            "requirement rows, so answer-guide.md entries could not be checked for a "
            "gap written up as evidenced experience. The shape checks still ran.")
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        body, title = text[mark.end():end], mark.group(1)
        if not _AG_SOURCE.search(body):
            findings.append(
                f"GUIDE_NO_SOURCE: answer-guide.md entry {title!r} has no "
                "'- source:' line — guidance the candidate cannot trace is guidance "
                "they will repeat in the real room believing it was vetted")
        row = _AG_ROW.search(body)
        if not row:
            findings.append(
                f"GUIDE_NO_ROW: answer-guide.md entry {title!r} has no '- row:' line "
                "naming the requirement it serves, so nothing can check it against "
                "what the assessment found")
        basis = _AG_BASIS.search(body)
        if not basis or basis.group(1) not in _AG_BASES:
            findings.append(
                f"GUIDE_BAD_BASIS: answer-guide.md entry {title!r} must carry "
                f"'- basis:' with one of {list(_AG_BASES)} — the whole honesty "
                "distinction in this artifact rides on that token")
            continue
        if not row or not matches:
            continue
        for raw_id in [part.strip() for part in row.group(1).split(",") if part.strip()]:
            rid = _norm_row_id(raw_id)
            if rid not in matches:
                findings.append(
                    f"GUIDE_UNKNOWN_ROW: answer-guide.md entry {title!r} names row "
                    f"{raw_id!r}, which fit-assessment.yaml does not declare. An id "
                    f"nothing resolves is an entry nothing checks, and it looked "
                    f"exactly like a checked one")
                continue
            if matches[rid] in _UNEVIDENCED and basis.group(1) == "evidenced":
                findings.append(
                    f"GUIDE_GAP_AS_EVIDENCED: answer-guide.md entry {title!r} serves "
                    f"{raw_id}, which fit-assessment.yaml scored {matches[rid]!r}, but is "
                    "written as 'evidenced'. An answer that satisfies an interviewer on "
                    "a requirement the candidate has no evidence for can only be "
                    "invented experience; the honest form of this entry is basis: "
                    "honest_gap")
    return findings, notices


# ----------------------------------------------------------------- banned vocabulary

def _default_scanner(workspace: pathlib.Path):
    """scripts/lint_no_prediction.py is Plan 2's. This is the ONLY adapter point —
    if its function is named differently there, change it here and nowhere else.

    Resolved with getattr, not attribute access: a rename in Plan 2 must produce a
    MissingDependency and exit 2, not an AttributeError traceback with no receipt and
    no stable exit code. Returning None IS the "could not run" signal.
    """
    try:
        import lint_no_prediction
    except ImportError:
        return None
    scanner = getattr(lint_no_prediction, "scan_text", None)
    capture_corpus = getattr(lint_no_prediction, "capture_corpus", None)
    if scanner is None or capture_corpus is None:
        return None
    # Use the same verified source corpus as the standalone lint and assessment
    # gate. Without it, true historical metrics pass there but fail in mock guides.
    corpus = capture_corpus(workspace)
    return lambda text, source: scanner(text, source, corpus)


def check_vocabulary(paths: list, scanner) -> list:
    if scanner is None:
        raise MissingDependency(
            "scripts/lint_no_prediction.py (Plan 2) is not importable — refusing to "
            "report a vocabulary check that did not run"
        )
    findings = []
    for path in paths:
        # Still `if path.exists()`, but no longer the only thing that notices: a file
        # that is not there is now its own finding from check_session_artifacts, so
        # this skip reports "nothing to scan" rather than standing in for "clean".
        if path.exists():
            findings.extend(scanner(path.read_text(encoding="utf-8"), str(path)))
    return findings


# ----------------------------------------------------------------- session artifacts

# modes/interview.md §5 requires both, and each has a distinct job: open-loops.md
# splits what the candidate could not answer into three buckets with three different
# actions, and cheatsheet.md is the one page they carry into the real room.
SESSION_ARTIFACTS = (
    ("NO_OPEN_LOOPS", "open-loops.md",
     "modes/interview.md §5 requires the three buckets — a fact not recalled, a "
     "genuine gap, and a tailoring error — because they have three completely "
     "different actions and merging them destroys the artifact"),
    ("NO_ANSWER_GUIDE", "answer-guide.md",
     "modes/interview.md §5 requires the per-question answer guidance: a question "
     "list with no account of what a good answer contains is half a deliverable, "
     "and the guidance is what the honesty rules have to bind on"),
    ("NO_CHEATSHEET", "cheatsheet.md",
     "modes/interview.md §5 requires the one page the candidate carries into the "
     "real room: the stories, the honest gaps with their framing, what is still "
     "unanswered, and the loop shape in the local vocabulary"),
)


def check_session_artifacts(mock_dir: pathlib.Path) -> list:
    """The two round outputs whose absence check_vocabulary used to swallow.

    It scanned them `if path.exists()`, which is a SKIP that looks exactly like a
    pass: delete the file and the vocabulary lint reports nothing, the gate reports
    nothing, and the round is recorded as holding up with two of its five required
    artifacts never written. An empty file counts as absent for the same reason —
    exists() is not the property anyone cared about.
    """
    findings = []
    for code, name, why in SESSION_ARTIFACTS:
        path = mock_dir / name
        if not path.exists():
            findings.append(f"{code}: {path} was never written — {why}")
        elif not path.read_text(encoding="utf-8").strip():
            findings.append(f"{code}: {path} is empty — {why}")
    return findings


# ----------------------------------------------------------------- write-backs

_WB_SECTION = "## Walk-back list"
_WB_HEADING = re.compile(r"^###\s+(WB-\d+)\s*(.*)$", re.M)
_CLAIM_FIELDS = ("term", "where", "source_kind", "source_ref", "session_date", "retracted")


def walkback_entries(brief_text: str) -> list:
    if _WB_SECTION not in brief_text:
        return []
    body = brief_text.split(_WB_SECTION, 1)[1]
    following = re.search(r"^##\s+", body, re.M)
    if following:
        body = body[:following.start()]
    marks = list(_WB_HEADING.finditer(body))
    entries = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(body)
        chunk = body[mark.end():end]
        entry = {"id": mark.group(1), "claim": mark.group(2).strip(" —-")}
        for field in ("quote", "softened", "defect", "transcript", "status"):
            found = re.search(rf"^\s*-\s*{field}:\s*(.+)$", chunk, re.M)
            entry[field] = found.group(1).strip() if found else ""
        entries.append(entry)
    return entries


def _phrase_in(term: str, text: str) -> bool:
    """Whole-token containment, reusing check_claims' implementation.

    Imported rather than re-spelled: check_claims.phrase_in already handles the
    part that is easy to get wrong — CJK, Thai and other unsegmented scripts have
    no word boundaries, so a token test there would report every skill on every
    Chinese CV as unsourced. Two copies of that reasoning is one copy that drifts.
    """
    try:
        import check_claims
    except ImportError:  # pragma: no cover - both live in scripts/
        return MB.collapse_ws(term).lower() in MB.collapse_ws(text).lower()
    return check_claims.phrase_in(term, text)


def _promotion_ref_resolves(row: dict, workspace: pathlib.Path) -> bool:
    """Whether `source_ref` names a file that actually exists in the workspace.

    `source_ref` was never resolved by any script in this skill — not here, not in
    check_claims — so one row citing a transcript was enough to silence UNSOURCED
    for any term, whether or not the cited file existed or contained anything.
    The ref carries a `#Q<n>` fragment by convention, which is stripped before the
    path is tested.
    """
    ref = str(row.get("source_ref", "")).strip()
    if not ref:
        return False
    path_part = ref.split("#", 1)[0].strip()
    if not path_part:
        return False
    candidate = pathlib.Path(path_part)
    if candidate.is_absolute():
        return candidate.is_file()
    # Workspace-relative, exactly as modes/interview.md:329 writes it
    # (`mock/transcript-2.md#Q1`). Deliberately NOT a search for the basename
    # anywhere under the workspace: that fallback would resolve any wrong
    # directory to the right file and leave this check unable to fail, which is
    # the shape of gate this audit spent its time finding.
    return (workspace / candidate).is_file()


def _candidate_words(transcript_text: str) -> str:
    """Only the candidate's own turns, across every section of a transcript."""
    sections = MB.transcript_sections(transcript_text or "")
    if not sections:
        return transcript_text or ""
    return "\n".join(MB.candidate_only(body) for body in sections.values())


def _read_cited(ref: str, workspace: pathlib.Path) -> str:
    """The text of the transcript a claims row cites, or "" if it resolves to none."""
    path_part = str(ref).split("#", 1)[0].strip()
    if not path_part:
        return ""
    candidate = pathlib.Path(path_part)
    target = candidate if candidate.is_absolute() else workspace / candidate
    try:
        return target.read_text(encoding="utf-8") if target.is_file() else ""
    except OSError:
        return ""


def _check_promotions(claims_path: pathlib.Path, transcript_name: str,
                      transcript_text: str, workspace: pathlib.Path):
    """Validate every `session-answer` row citing this transcript.

    Returns `(findings, promoted)` — `promoted` holding only the rows that
    survived, so nothing downstream can discharge a fact with a row this
    function rejected.
    """
    findings: list = []
    promoted = []
    if claims_path.exists():
        try:
            rows = journal.load_yaml(claims_path, expect=list)
        except journal.YamlUnreadable as exc:
            findings.append(f"CLAIMS_UNPARSEABLE: {exc}")
            rows = []
        for row in rows:
            if not isinstance(row, dict) or row.get("source_kind") != "session-answer":
                continue
            ref = str(row.get("source_ref", ""))
            # A row citing ANOTHER round is still a claim that the candidate said
            # something, and after a second mock that is the NORMAL shape. Skipping
            # it made the "unconditional" validation conditional on which round
            # happens to be gated — so a row could cite a transcript that does not
            # exist and never be looked at by anything.
            this_round = transcript_name in ref
            if not this_round and "transcript-" not in ref:
                continue
            missing = [f for f in _CLAIM_FIELDS if f not in row]
            if missing:
                findings.append(
                    f"CLAIM_ROW_INCOMPLETE: the promotion row for "
                    f"{row.get('term', '?')!r} is missing {', '.join(missing)}"
                )
            term = str(row.get("term", "")).strip()
            # These three run for EVERY promotion row, not only when an
            # UNSOURCED-FACT happens to have fired. They used to sit inside the
            # `for record in unsourced:` loop below, so on the documented clean
            # round — `FINDINGS: none` — a row claiming the transcript as its
            # source got no scrutiny at all, and check_claims then treated it as
            # provenance for putting the term on the tailored CV.
            if row.get("retracted"):
                # check_claims.py:415 already sorts rows this way. A claim the
                # candidate withdrew is the strongest possible evidence AGAINST
                # it, and reading that record as the claim's source is the worst
                # version of this defect: the workspace contains the retraction.
                findings.append(
                    f"PROMOTION_RETRACTED: the promotion row for {term!r} is marked "
                    "retracted, so it cannot source anything — a withdrawn claim is "
                    "evidence against the fact, not for it"
                )
                continue
            if not term:
                findings.append(
                    "PROMOTION_NO_TERM: a session-answer row citing "
                    f"{transcript_name} has an empty term"
                )
                continue
            if not _promotion_ref_resolves(row, workspace):
                findings.append(
                    f"PROMOTION_REF_MISSING: the promotion row for {term!r} cites "
                    f"source_ref {str(row.get('source_ref', ''))!r}, which names no "
                    f"file that exists under {workspace} — an unresolvable source is "
                    "not a source"
                )
                continue
            # Read the transcript the row actually cites, and only the
            # candidate's own turns in it. Matching the whole file let any skill,
            # employer or number the INTERVIEWER put in a question — exactly what
            # a persona does when it probes "did you use X?" — be promoted onto
            # the tailored CV as something the candidate said.
            cited_text = transcript_text if this_round else _read_cited(ref, workspace)
            spoken = _candidate_words(cited_text)
            if not _phrase_in(term, spoken):
                where = transcript_name if this_round else ref
                extra = (" — it appears only in the interviewer's words"
                         if _phrase_in(term, cited_text) else "")
                findings.append(
                    f"PROMOTION_NOT_IN_TRANSCRIPT: the promotion row for {term!r} "
                    f"cites {where}, but {term!r} is not in what the candidate "
                    f"said there{extra}"
                )
                continue
            promoted.append(row)

    return findings, promoted


def check_walkback(blocks: dict, brief_path: pathlib.Path, claims_path: pathlib.Path,
                   transcript_name: str, transcript_text: str = "",
                   workspace: pathlib.Path = None) -> list:
    records = [
        record
        for block in blocks.values()
        for record in block.records
        if record.kind == "FINDING"
    ]
    fired = [r for r in records if r.fields["tag"] in V.WALKBACK_TAGS]
    unsourced = [r for r in records if r.fields["tag"] == "UNSOURCED-FACT"]

    workspace = pathlib.Path(workspace) if workspace is not None else claims_path.parent

    # Promotion rows are validated FIRST and UNCONDITIONALLY. This function used
    # to return here when no tag had fired, which meant the documented clean
    # round — both blocks emitting `FINDINGS: none` — never opened claims.yaml at
    # all. A `session-answer` row is a claim that the candidate said something in
    # this transcript, and check_claims treats it as provenance for putting that
    # term on the tailored CV. It has to be true whether or not an assessor
    # happened to flag anything, and the round where nobody flagged anything is
    # exactly the round where nothing else is looking.
    findings, promoted = _check_promotions(
        claims_path, transcript_name, transcript_text, workspace)

    if not fired and not unsourced:
        return findings

    brief_text = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
    entries = walkback_entries(brief_text)
    if fired and _WB_SECTION not in brief_text:
        findings.append(
            "WALKBACK_MISSING: "
            + ", ".join(sorted({r.fields["tag"] for r in fired}))
            + f" fired, but {brief_path.name} has no '{_WB_SECTION}' section — a claim "
            "the candidate cannot defend under one follow-up is a tailoring error, not "
            "a rehearsal topic"
        )
    else:
        for record in fired:
            quote = record.fields["quote"]
            if not any(MB.quote_is_in(quote, e["quote"]) for e in entries):
                findings.append(
                    f"WALKBACK_NO_ENTRY: {record.fields['tag']} at "
                    f"{record.fields['ref']} has no '### WB-' entry quoting "
                    f"{MB.normalize_quote(quote)[:60]!r}"
                )

    for entry in entries:
        for field in ("quote", "softened", "defect"):
            if not entry[field]:
                findings.append(
                    f"WALKBACK_INCOMPLETE: {entry['id']} is missing its '- {field}:' line"
                )
        # Any of the four defect tags may land here: the three that *demand* the
        # section, plus an UNSOURCED-FACT the candidate could not stand behind, which
        # is walked back rather than promoted to claims.yaml.
        if entry["defect"] and entry["defect"] not in V.DEFECT_TAGS:
            findings.append(
                f"WALKBACK_BAD_DEFECT: {entry['id']}: defect: {entry['defect']!r} must "
                "be one of " + " | ".join(V.DEFECT_TAGS)
            )

    for record in unsourced:
        quote = MB.normalize_quote(record.fields["quote"])
        # A proposed edit is still an open question. The same quote appearing
        # under OVER-CLAIM must not silently discharge UNSOURCED-FACT before
        # the claim has actually been withdrawn or the correction applied.
        walked = any(MB.quote_is_in(record.fields["quote"], e["quote"])
                     and e["status"].lower() in {"withdrawn", "applied"}
                     for e in entries)
        # Whole-token matching, borrowed from the gate that already got this
        # right: a bare `in` let an honest `term: Java` row silently discharge an
        # unrelated finding about "the JavaScript dashboard".
        claimed = any(_phrase_in(str(row["term"]), quote) for row in promoted)
        if not (walked or claimed):
            findings.append(
                f"UNRESOLVED_FACT: UNSOURCED-FACT at {record.fields['ref']} "
                f"({quote[:50]!r}) is neither promoted to claims.yaml "
                f"(source_kind: session-answer, source_ref naming {transcript_name}) nor "
                "resolved by a walk-back with status: withdrawn or applied — ask the candidate where it came from before it enters the "
                "answer bank"
            )
    return findings


# ----------------------------------------------------------------- receipts

def _receipt(workspace: pathlib.Path, inputs: dict, verdict: str, findings: list) -> None:
    """Append exactly one receipt. Raises ReceiptFailed rather than warning.

    A warning on stderr followed by exit 0 is the worst available outcome: the caller
    reads a clean exit code, and journal.jsonl — the thing modes/interview.md §7 tells
    the model to quote — has no line for this run at all.
    """
    hashes = {}
    for label, path in inputs.items():
        if path.exists():
            hashes[label] = journal.sha256_file(path)
    try:
        journal.receipt(workspace, GATE, hashes, verdict, findings)
    except OSError as exc:
        raise ReceiptFailed(
            f"RECEIPT_WRITE_FAILED: could not append the {GATE} receipt to "
            f"{workspace}/journal.jsonl: {exc}"
        ) from exc


# ----------------------------------------------------------------- orchestration

def _answer_bank_default(workspace: pathlib.Path) -> pathlib.Path:
    """The profile-level answer bank for the profile that owns this workspace.

    paths.py owns the layout; this gate does not re-derive it. The fallback covers a
    --workspace that is not shaped like a workspace at all, which is a user error the
    answer-bank check should report as NO_ANSWER_BANK rather than crash on.
    """
    try:
        return paths.answer_bank_of(workspace)
    except ValueError:
        return workspace / paths.ANSWER_BANK_NAME


def _inputs(workspace: pathlib.Path, round_no: int, answer_bank: pathlib.Path) -> dict:
    return {
        f"mock/assessment-{round_no}.md": workspace / "mock" / f"assessment-{round_no}.md",
        f"mock/transcript-{round_no}.md": workspace / "mock" / f"transcript-{round_no}.md",
        "mock/question-log.yaml": workspace / "mock" / "question-log.yaml",
        "mock/open-loops.md": workspace / "mock" / "open-loops.md",
        "mock/cheatsheet.md": workspace / "mock" / "cheatsheet.md",
        "mock/answer-guide.md": workspace / "mock" / "answer-guide.md",
        "fit-assessment.yaml": workspace / "fit-assessment.yaml",
        # The coverage check is now a claim about THESE bytes: "every must-have has a
        # row" is only auditable against the list it was checked against.
        "posting.yaml": workspace / "posting.yaml",
        "interview-brief.md": workspace / "interview-brief.md",
        "claims.yaml": workspace / "claims.yaml",
        "answer-bank.md": answer_bank,
    }


def _skill_root_default() -> pathlib.Path:
    # Ask paths.py rather than re-deriving `.parent.parent` here (R4). A
    # hand-derived root is correct until someone moves one file.
    return paths.SKILL_ROOT


def run(workspace, round_no: int, answer_bank=None, today=None, vocab_scanner=_AUTO,
        skill_root=None):
    workspace = pathlib.Path(workspace)
    answer_bank = pathlib.Path(answer_bank) if answer_bank else _answer_bank_default(workspace)
    skill_root = pathlib.Path(skill_root) if skill_root else _skill_root_default()
    today = today or datetime.date.today()
    scanner = _default_scanner(workspace) if vocab_scanner is _AUTO else vocab_scanner

    assessment_path = workspace / "mock" / f"assessment-{round_no}.md"
    transcript_path = workspace / "mock" / f"transcript-{round_no}.md"
    for path in (assessment_path, transcript_path):
        if not path.exists():
            raise InputMissing(f"{path} is missing — nothing to check")

    assessment_text = assessment_path.read_text(encoding="utf-8")
    transcript_text = transcript_path.read_text(encoding="utf-8")

    # Reported whatever the assessor produced: posting.yaml is a required input of
    # the mode, and its absence is not conditional on the block having parsed.
    must_haves, posting_findings = _must_haves(workspace)
    findings = check_mode_entry(workspace, skill_root) + posting_findings
    blocks, block_findings = check_assessment(
        assessment_text, transcript_text, round_no, must_haves=must_haves)
    findings += block_findings
    findings += check_question_log(workspace / "mock" / "question-log.yaml", today,
                                  refs=transcript_refs(transcript_text))
    findings += check_answer_bank(answer_bank)
    findings += check_session_artifacts(workspace / "mock")
    guide_findings, guide_notices = check_answer_guide(
        workspace / "mock" / "answer-guide.md", workspace)
    findings += guide_findings
    for notice in guide_notices:
        print(notice, file=sys.stderr)
    findings += check_vocabulary(
        [
            assessment_path,
            workspace / "mock" / "open-loops.md",
            workspace / "mock" / "cheatsheet.md",
            # The guide is what the candidate says out loud. It shipped scanned by
            # nothing, so a "70% chance" line in it passed every gate in the skill.
            workspace / "mock" / "answer-guide.md",
        ],
        scanner,
    )
    findings += check_walkback(
        blocks,
        workspace / "interview-brief.md",
        workspace / "claims.yaml",
        f"transcript-{round_no}.md",
        transcript_text=transcript_text,
        workspace=workspace,
    )
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Gate for one mock-interview round.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--round", required=True, type=int)
    parser.add_argument("--answer-bank", type=pathlib.Path, default=None)
    parser.add_argument("--skill-root", type=pathlib.Path, default=None)
    parser.add_argument(
        "--today",
        default=None,
        help="ISO date used for staleness arithmetic; defaults to the system date",
    )
    args = parser.parse_args(argv)

    # The one place a receipt is impossible: there is nothing to append to, and
    # creating the directory would materialise a workspace on a typo.
    if not args.workspace.is_dir():
        print(f"cannot run {GATE}: workspace {args.workspace} does not exist",
              file=sys.stderr)
        return 2

    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
    answer_bank = args.answer_bank or _answer_bank_default(args.workspace)
    inputs = _inputs(args.workspace, args.round, answer_bank)

    try:
        findings = run(
            args.workspace,
            args.round,
            answer_bank=answer_bank,
            today=today,
            vocab_scanner=_AUTO,
            skill_root=args.skill_root,
        )
    except (InputMissing, MissingDependency, journal.YamlUnreadable, OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        try:
            _receipt(args.workspace, inputs, "could_not_run", [str(exc)])
        except ReceiptFailed as fail:
            print(str(fail), file=sys.stderr)
        return 2

    verdict = "fail" if findings else "pass"
    try:
        _receipt(args.workspace, inputs, verdict, findings)
    except ReceiptFailed as fail:
        print(str(fail), file=sys.stderr)
        return 2
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
