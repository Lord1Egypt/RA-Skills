#!/usr/bin/env python3
"""Gate the evidence behind discovery-stage CV-to-job recommendations.

The gate does not estimate an interview or offer outcome.  It verifies a more
modest and useful claim: a row shown as a default recommendation was read as a
full job description, its requirements are quoted from that retrieval, and its
claimed CV evidence is present in the profile frozen for this search round.

Exit codes follow every other gate: 0 clean, 1 findings, 2 could not run.  A
normal invocation writes one receipt; ``--render`` is deliberately receipt-free
so an agent can obtain the exact reader-facing summaries before authoring the
shortlist that the normal invocation verifies.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import candidate_match as matching  # noqa: E402
import journal  # noqa: E402
from record_browser_capture import read_retrieval_calls  # noqa: E402
import report_locales as locales  # noqa: E402
import vocab  # noqa: E402


GATE = "check_candidate_match"
MATCH_FILE = "candidate-match.yaml"
PROFILE_SNAPSHOT = "candidate-profile.yaml"
SHORTLIST_FILE = "shortlist.yaml"
BRIEF_FILE = "brief.yaml"
SHORTLIST_MD = "shortlist.md"
MAX_MATCH_REVIEWS = 5

KIND = ("must_have", "responsibility")
_SPACE = re.compile(r"\s+")
_ENTRY = re.compile(r"^\s*\d+\.\s+", re.M)


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def _normalise(value: object) -> str:
    return _SPACE.sub(" ", str(value or "")).strip().casefold()


def _safe_path(workspace: pathlib.Path, name: object, *, raw: bool = False) -> pathlib.Path | None:
    """A real workspace file, never an absolute path or a symlink escape."""
    if not isinstance(name, str) or not name.strip():
        return None
    relative = pathlib.PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or (raw and relative.parts[:1] != ("raw",)):
        return None
    root = workspace.resolve()
    path = (root / pathlib.Path(*relative.parts)).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path if path.is_file() else None


def _capture_strings(text: str) -> list[str]:
    """Raw text plus JSON string leaves when an adapter escaped Unicode in JSON."""
    values = [text]
    try:
        parsed = json.loads(text)
    except (TypeError, ValueError):
        return values

    def walk(value):
        if isinstance(value, str):
            values.append(value)
        elif isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(parsed)
    return values


def _quote_in_capture(quote: object, text: str) -> bool:
    needle = _normalise(quote)
    if len(needle) < 2:
        return False
    return any(needle in _normalise(value) for value in _capture_strings(text))


def _pointer_value(document: object, pointer: object) -> tuple[object | None, str | None]:
    """Resolve an RFC 6901 JSON Pointer to one scalar profile leaf."""
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        return None, "pointer must start with '/'; use /experience/0/bullets/0"
    value = document
    for encoded in pointer.split("/")[1:]:
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            if token not in value:
                return None, f"key {token!r} does not exist"
            value = value[token]
        elif isinstance(value, list):
            if not token.isdigit() or int(token) >= len(value):
                return None, f"index {token!r} does not exist"
            value = value[int(token)]
        else:
            return None, f"{token!r} is below a scalar value"
    if isinstance(value, (dict, list)) or value is None:
        return None, "pointer must resolve to a scalar profile value"
    return value, None


def _detail_files(calls: list[dict], workspace: pathlib.Path | None = None) -> dict[str, list[dict]]:
    """Successful detail captures, including browser snapshot files."""
    out: dict[str, list[dict]] = {}
    for raw_record in calls:
        record = journal.as_mapping(raw_record)
        # Browser captures normalize this operation to ``detail``; some
        # OpenCLI adapters expose it as ``job-detail`` (LinkedIn) or ``job``
        # (Indeed). These are detail retrievals, unlike a search card.
        command = record.get("command")
        if command not in ("detail", "job-detail") and not (
                record.get("site") == "indeed" and command == "job"):
            continue
        if record.get("classification") != "ok" or record.get("exit_code") != 0:
            continue
        for field in ("stdout_file", "snapshot_file", "rows_file"):
            name = record.get(field)
            if isinstance(name, str) and pathlib.Path(name).is_absolute() and workspace is None:
                continue
            name = workspace_relative(workspace, name) if workspace is not None else name
            if isinstance(name, str) and name.startswith("raw/"):
                out.setdefault(name, []).append(record)
    return out


def workspace_relative(workspace: pathlib.Path, name: object) -> object:
    """A journaled capture path in the workspace-relative spelling gates compare.

    The classifier preserves the caller's path spelling. An absolute capture is
    accepted only when it resolves inside this workspace; anything else returns
    None. Relative names pass through unchanged for ``_safe_path`` to validate.
    """
    if isinstance(name, str) and pathlib.Path(name).is_absolute():
        try:
            return pathlib.Path(name).resolve().relative_to(workspace.resolve()).as_posix()
        except (OSError, ValueError, RuntimeError):
            return None
    return name


def _record_mentions_row(record: dict, row: dict, source_text: str) -> bool:
    source_id = str(row.get("source_id") or "").strip()
    url = str(row.get("url") or "").strip().rstrip("/")
    haystack = "\n".join(str(record.get(field) or "") for field in
                          ("command_line", "url", "stdout_file", "snapshot_file", "rows_file"))
    if source_id and (source_id in source_text or source_id in haystack):
        return True
    return bool(url and (url in source_text or url in haystack))


class EvidenceContext:
    def __init__(self, workspace: pathlib.Path, profile: dict, detail_files: dict[str, list[dict]]):
        self.workspace = workspace
        self.profile = profile
        self.detail_files = detail_files
        self.sources: dict[str, str] = {}
        self.read_files: set[str] = set()

    def capture(self, name: object) -> tuple[str | None, str | None]:
        path = _safe_path(self.workspace, name, raw=True)
        if path is None:
            return None, "must name an existing raw/<capture> file inside this workspace"
        relative = path.relative_to(self.workspace.resolve()).as_posix()
        self.read_files.add(relative)
        if relative not in self.sources:
            try:
                self.sources[relative] = path.read_bytes().decode("utf-8", errors="replace")
            except OSError as exc:
                return None, str(exc)
        return self.sources[relative], None


def _check_cv_evidence(evidence: object, context: EvidenceContext, label: str,
                       required: bool) -> list[str]:
    findings = []
    if not isinstance(evidence, list):
        return [f"CV_EVIDENCE_INVALID: {label} cv_evidence must be a list"]
    if required and not evidence:
        findings.append(f"CV_EVIDENCE_MISSING: {label} claims a match but cites no CV evidence")
    for index, item in enumerate(evidence):
        entry = journal.as_mapping(item)
        pointer, quote = entry.get("path"), entry.get("quote")
        value, error = _pointer_value(context.profile, pointer)
        if error:
            findings.append(f"CV_EVIDENCE_PATH_INVALID: {label} cv_evidence[{index}].path "
                            f"{pointer!r}: {error}")
            continue
        if not isinstance(quote, str) or len(_normalise(quote)) < 2:
            findings.append(f"CV_EVIDENCE_QUOTE_INVALID: {label} cv_evidence[{index}] "
                            "needs a non-trivial quote")
        elif _normalise(quote) not in _normalise(value):
            findings.append(f"CV_EVIDENCE_QUOTE_MISSING: {label} cv_evidence[{index}] "
                            f"quote {quote!r} is not in {pointer!r}")
    return findings


def _check_job_evidence(evidence: object, text: object | None, context: EvidenceContext,
                        row: dict, label: str) -> list[str]:
    findings = []
    if not isinstance(evidence, list) or not evidence:
        return [f"JOB_EVIDENCE_MISSING: {label} needs one or more quoted detail captures"]
    quoted = []
    for index, item in enumerate(evidence):
        entry = journal.as_mapping(item)
        filename, quote = entry.get("file"), entry.get("quote")
        source, error = context.capture(filename)
        if error:
            findings.append(f"JOB_EVIDENCE_PATH_INVALID: {label} job_evidence[{index}].file "
                            f"{filename!r}: {error}")
            continue
        assert source is not None
        path = _safe_path(context.workspace, filename, raw=True)
        relative = path.relative_to(context.workspace.resolve()).as_posix() if path else ""
        records = context.detail_files.get(relative, [])
        if not records:
            findings.append(f"JOB_EVIDENCE_NOT_DETAIL: {label} cites {relative!r}, which is "
                            "not a successful journaled detail capture")
        elif not any(_record_mentions_row(record, row, source) for record in records):
            findings.append(f"JOB_EVIDENCE_WRONG_ROW: {label} cites {relative!r}, but its "
                            "detail retrieval cannot be tied to this listing")
        if not isinstance(quote, str) or len(_normalise(quote)) < 2:
            findings.append(f"JOB_EVIDENCE_QUOTE_INVALID: {label} job_evidence[{index}] "
                            "needs a non-trivial quote")
        elif not _quote_in_capture(quote, source):
            findings.append(f"JOB_EVIDENCE_QUOTE_MISSING: {label} job_evidence[{index}] "
                            f"quote {quote!r} is absent from {relative!r}")
        else:
            quoted.append(quote)
    if text is not None:
        if not isinstance(text, str) or len(_normalise(text)) < 2:
            findings.append(f"MATCH_TEXT_INVALID: {label} needs the posting's requirement text")
        elif not any(_normalise(text) in _normalise(quote) for quote in quoted):
            findings.append(f"MATCH_TEXT_NOT_QUOTED: {label} text {text!r} is not contained "
                            "in any quoted job evidence; keep the requirement wording verbatim")
    return findings


def _check_requirement(item: object, context: EvidenceContext, row: dict,
                       seen: set[str], index: int) -> list[str]:
    requirement = journal.as_mapping(item)
    label = f"match {row.get('id')!r} requirement #{index + 1}"
    identifier = requirement.get("id")
    findings = []
    if not isinstance(identifier, str) or not identifier.strip():
        findings.append(f"MATCH_REQUIREMENT_ID_MISSING: {label} needs an id")
    elif identifier in seen:
        findings.append(f"MATCH_REQUIREMENT_ID_DUPLICATE: {label} repeats {identifier!r}")
    else:
        seen.add(identifier)
    for field, allowed in (("kind", KIND), ("screening", vocab.SCREENING),
                           ("match", vocab.MATCH), ("recency", vocab.RECENCY),
                           ("effort", vocab.EFFORT)):
        if requirement.get(field) not in allowed:
            findings.append(f"MATCH_REQUIREMENT_BAD_ENUM: {label} {field}="
                            f"{requirement.get(field)!r}, not one of {allowed}")
    findings.extend(_check_job_evidence(requirement.get("job_evidence"),
                                        requirement.get("text"), context, row, label))
    outcome = requirement.get("match")
    evidence = requirement.get("cv_evidence")
    if outcome == "no_evidence":
        if evidence not in ([], None):
            findings.append(f"NO_EVIDENCE_HAS_CV_REF: {label} says no_evidence but carries "
                            "CV evidence; choose strong, partial, or gap instead")
        elif evidence is None:
            findings.append(f"CV_EVIDENCE_INVALID: {label} cv_evidence must be [] for no_evidence")
    else:
        findings.extend(_check_cv_evidence(evidence, context, label, required=True))
    return findings


def _check_alignment(alignment: object, context: EvidenceContext, row: dict) -> list[str]:
    label = f"match {row.get('id')!r} alignment"
    value = journal.as_mapping(alignment)
    if not isinstance(alignment, dict):
        return [f"ALIGNMENT_MISSING: {label} needs level_direction, domain_fit and evidence"]
    findings = []
    if value.get("level_direction") not in vocab.LEVEL_DIRECTION:
        findings.append(f"ALIGNMENT_BAD_LEVEL: {label} level_direction="
                        f"{value.get('level_direction')!r}, not one of {vocab.LEVEL_DIRECTION}")
    if value.get("domain_fit") not in vocab.DOMAIN_FIT:
        findings.append(f"ALIGNMENT_BAD_DOMAIN: {label} domain_fit={value.get('domain_fit')!r}, "
                        f"not one of {vocab.DOMAIN_FIT}")
    # Alignment's source quote identifies role and level; unlike an individual
    # requirement, it need not contain a generated label.
    findings.extend(_check_job_evidence(value.get("job_evidence"), None, context, row,
                                        label))
    findings.extend(_check_cv_evidence(value.get("cv_evidence"), context, label, required=True))
    return findings


def _entry_blocks(markdown: str) -> list[str]:
    """Numbered candidate blocks from §1, matching check_shortlist's scope."""
    marks = list(re.finditer(r"^##\s*§\S*", markdown or "", re.M))
    section = ""
    for index, mark in enumerate(marks):
        if mark.group(0).startswith("## §1"):
            end = marks[index + 1].start() if index + 1 < len(marks) else len(markdown)
            section = markdown[mark.start():end]
            break
    entries = list(_ENTRY.finditer(section))
    return [section[entry.start():entries[index + 1].start() if index + 1 < len(entries)
                    else len(section)]
            for index, entry in enumerate(entries)]


def _report_language(markdown: str, rows: list[dict]) -> str | None:
    """Infer the native report language from the required discover stamp.

    A normal gate cannot rely on a command-line default: a Chinese default would
    let an English report pass with a Chinese match summary. The shortlist's
    required provisional stamp already identifies the report language, including
    the card-only/detail-reviewed distinction, so use that shared contract.
    """
    has_detail = any(row.get("quality") == "complete" for row in rows)
    key = "detail_provisional" if has_detail else "provisional"
    lowered = markdown.casefold()
    matches = [lang for lang in locales.LANGUAGES
               if locales.GATE_TEXT[lang][key].casefold() in lowered]
    return matches[0] if len(matches) == 1 else None


def _check_rendered(rows: list[dict], matches: dict[str, dict], markdown: str) -> list[str]:
    if not rows:
        return []  # No job summaries need a language stamp in a direction-only round.
    blocks = _entry_blocks(markdown)
    findings = []
    language = _report_language(markdown, rows)
    if language is None:
        findings.append("MD_MATCH_LANGUAGE_UNCLEAR: shortlist.md must contain exactly one "
                        "native provisional stamp so CV-match summaries can use the "
                        "same report language")
    positions = []
    for row in rows:
        identifier = str(row.get("id") or "")
        url = str(row.get("url") or "")
        block = next((value for value in blocks if url and url in value), "")
        if block:
            positions.append(blocks.index(block))
        match = matches.get(identifier)
        if not match or not block:
            continue
        if language is None:
            continue
        expected = matching.render_summary(match, language)
        if expected not in block:
            if any(summary in block for summary in matching.summaries(match)):
                findings.append(f"MD_MATCH_SUMMARY_WRONG_LANGUAGE: shortlist.md renders "
                                f"the CV-match summary for {identifier!r}, but not in "
                                f"the report language {language!r}")
            else:
                findings.append(f"MD_MATCH_SUMMARY_MISSING: shortlist.md does not render the "
                                f"localized CV-match summary for {identifier!r} beside its link")
    if positions and positions != sorted(positions):
        findings.append("MD_MATCH_ORDER: shortlist.md renders candidate links in a different "
                        "order from the evidence-ranked shortlist.yaml rows")
    return findings


def _hashes(workspace: pathlib.Path, names: set[str]) -> dict[str, str]:
    out = {}
    for name in sorted(names):
        path = _safe_path(workspace, name, raw=name.startswith("raw/"))
        if path is not None:
            out[name] = journal.sha256_file(path)
    return out


def check(workspace: pathlib.Path, match_document: dict, profile: dict, shortlist: dict,
          brief: dict, markdown: str = "", verify_rendered: bool = True) -> tuple[list[str], set[str]]:
    """Validate a loaded candidate-match document and return findings/input paths."""
    findings: list[str] = []
    input_files = {MATCH_FILE, SHORTLIST_FILE, BRIEF_FILE}
    profile_name = match_document.get("profile_snapshot")
    if isinstance(profile_name, str):
        input_files.add(profile_name)
    if verify_rendered:
        input_files.add(SHORTLIST_MD)

    short_rows = shortlist.get("rows")
    if not isinstance(short_rows, list):
        return ["SHORTLIST_ROWS_INVALID: shortlist.yaml rows must be a list"], input_files
    rows_by_id: dict[str, dict] = {}
    for index, raw_row in enumerate(short_rows):
        row = journal.as_mapping(raw_row)
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            findings.append(f"SHORTLIST_ROW_ID_INVALID: shortlist row {index + 1} has no usable id")
        elif identifier in rows_by_id:
            findings.append(f"SHORTLIST_ROW_ID_DUPLICATE: shortlist repeats id {identifier!r}")
        else:
            rows_by_id[identifier] = row

    match_rows = match_document.get("rows")
    if not isinstance(match_rows, list):
        return findings + ["MATCH_ROWS_INVALID: candidate-match.yaml rows must be a list"], input_files
    matches: dict[str, dict] = {}
    for index, raw_match in enumerate(match_rows):
        entry = journal.as_mapping(raw_match)
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            findings.append(f"MATCH_ROW_ID_MISSING: candidate-match row {index + 1} needs an id")
        elif identifier in matches:
            findings.append(f"MATCH_ROW_ID_DUPLICATE: candidate-match repeats id {identifier!r}")
        else:
            matches[identifier] = entry
    for identifier in rows_by_id:
        if identifier not in matches:
            findings.append(f"MATCH_ROW_MISSING: shortlist row {identifier!r} has no candidate-match row")
    for identifier in matches:
        if identifier not in rows_by_id:
            findings.append(f"MATCH_ROW_ORPHANED: candidate-match row {identifier!r} is not in shortlist.yaml")

    limit = brief.get("max_match_reviews")
    if type(limit) is not int or limit < 1 or limit > MAX_MATCH_REVIEWS:
        findings.append(f"MATCH_REVIEW_CAP_INVALID: brief.yaml max_match_reviews must be an "
                        f"integer from 1 to {MAX_MATCH_REVIEWS}")
    elif sum(1 for entry in matches.values() if entry.get("basis") == "detail") > limit:
        findings.append(f"MATCH_REVIEWS_ABOVE_CAP: {sum(1 for entry in matches.values() if entry.get('basis') == 'detail')} "
                        f"detail matches exceed brief.yaml max_match_reviews={limit}")

    calls = read_retrieval_calls(workspace)
    context = EvidenceContext(workspace, profile, _detail_files(calls, workspace))
    for identifier, match in matches.items():
        row = rows_by_id.get(identifier)
        if row is None:
            continue
        basis = match.get("basis")
        recommendation = match.get("recommendation")
        if basis not in matching.BASES:
            findings.append(f"MATCH_BASIS_INVALID: {identifier!r} basis={basis!r}, not one of "
                            f"{matching.BASES}")
        if recommendation not in matching.RECOMMENDATIONS:
            findings.append(f"MATCH_RECOMMENDATION_INVALID: {identifier!r} recommendation="
                            f"{recommendation!r}, not one of {matching.RECOMMENDATIONS}")
        requirements = match.get("requirements")
        if not isinstance(requirements, list):
            findings.append(f"MATCH_REQUIREMENTS_INVALID: {identifier!r} requirements must be a list")
            requirements = []
        if basis == "card":
            if row.get("quality") == "complete":
                findings.append(f"CARD_BASIS_STALE: {identifier!r} has a full description; "
                                "use detail_unmapped or a complete detail mapping")
            if recommendation == "recommend":
                findings.append(f"CARD_CANNOT_RECOMMEND: {identifier!r} has only card data; "
                                "read a full detail before making it a default recommendation")
            if requirements:
                findings.append(f"CARD_REQUIREMENTS_UNVERIFIED: {identifier!r} stores requirement "
                                "matches from a card; card-only rows are leads, not JD matches")
            if match.get("alignment") is not None:
                findings.append(f"CARD_ALIGNMENT_UNVERIFIED: {identifier!r} has role alignment "
                                "without a full job description")
        elif basis == "detail_unmapped":
            if row.get("quality") != "complete":
                findings.append(f"DETAIL_MATCH_INCOMPLETE: {identifier!r} has no complete description")
            if recommendation != "review" or requirements or match.get("alignment") is not None:
                findings.append(f"UNMAPPED_DETAIL_HAS_MATCH: {identifier!r} must remain review "
                                "with no requirement matches or alignment until mapped")
            findings.extend(_check_job_evidence(match.get("job_evidence"), None, context,
                                                row, f"{identifier!r} full description"))
        elif basis == "detail":
            if row.get("quality") != "complete":
                findings.append(f"DETAIL_MATCH_INCOMPLETE: {identifier!r} is detail-matched but "
                                f"row quality is {row.get('quality')!r}, not 'complete'")
            if not requirements:
                findings.append(f"DETAIL_REQUIREMENTS_MISSING: {identifier!r} read a detail but "
                                "records no job requirements or responsibilities")
            seen: set[str] = set()
            for index, requirement in enumerate(requirements):
                findings.extend(_check_requirement(requirement, context, row, seen, index))
            findings.extend(_check_alignment(match.get("alignment"), context, row))

        if recommendation == "recommend":
            for reason in matching.recommendation_failures(row, match):
                findings.append(f"RECOMMENDATION_NOT_READY: {identifier!r} {reason}; keep it as "
                                "a review candidate or correct the evidence mapping")
        if (row.get("verdict") in matching.DEFAULT_RECOMMENDATION_VERDICTS
                and recommendation != "recommend"):
            findings.append(f"HIGH_VERDICT_UNVERIFIED: {identifier!r} is {row.get('verdict')!r} "
                            "but is not an evidence-backed default recommendation")

    ordered = [rows_by_id[str(raw.get("id"))] for raw in short_rows
               if isinstance(raw, dict) and str(raw.get("id")) in rows_by_id]
    previous = None
    for row in ordered:
        match = matches.get(str(row.get("id")))
        if match is None:
            continue
        key = matching.ordering_key(row, match)
        if previous is not None and key < previous:
            findings.append("MATCH_ORDER: shortlist.yaml is not ordered as verified "
                            "recommendation, verdict, then effort")
            break
        previous = key
    input_files.update(context.read_files)
    if verify_rendered:
        findings.extend(_check_rendered(ordered, matches, markdown))
    return findings, input_files


def _load_workspace(workspace: pathlib.Path, *, need_markdown: bool) -> tuple[dict, dict, dict, dict, str]:
    match = journal.load_yaml(workspace / MATCH_FILE)
    shortlist = journal.load_yaml(workspace / SHORTLIST_FILE)
    brief = journal.load_yaml(workspace / BRIEF_FILE)
    profile_name = match.get("profile_snapshot")
    if profile_name != PROFILE_SNAPSHOT:
        raise ValueError(f"PROFILE_SNAPSHOT_INVALID: profile_snapshot must be "
                         f"{PROFILE_SNAPSHOT!r}, not {profile_name!r}")
    path = _safe_path(workspace, profile_name)
    if path is None:
        raise ValueError(f"PROFILE_SNAPSHOT_INVALID: profile_snapshot {profile_name!r} must name "
                         "an existing workspace YAML file")
    profile = journal.load_yaml(path)
    markdown = ""
    if need_markdown:
        markdown = (workspace / SHORTLIST_MD).read_text(encoding="utf-8")
    return match, profile, shortlist, brief, markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--render", action="store_true", help="print exact per-row summaries without a receipt")
    parser.add_argument("--lang", choices=locales.LANGUAGES, default="zh")
    args = parser.parse_args(argv)
    workspace = args.workspace
    if not workspace.is_dir():
        return cannot_run(workspace, f"workspace {workspace} does not exist")
    for name in (MATCH_FILE, SHORTLIST_FILE, BRIEF_FILE):
        if not (workspace / name).is_file():
            return cannot_run(workspace, f"{name} not found at {workspace / name}")
    if not args.render and not (workspace / SHORTLIST_MD).is_file():
        return cannot_run(workspace, f"{SHORTLIST_MD} not found at {workspace / SHORTLIST_MD}")
    try:
        match, profile, shortlist, brief, markdown = _load_workspace(
            workspace, need_markdown=not args.render)
    except journal.YamlUnreadable as exc:
        return cannot_run(workspace, str(exc), journal.UNREADABLE_INPUT)
    except (OSError, ValueError) as exc:
        if args.render:
            print(str(exc), file=sys.stderr)
            return 2
        findings = [str(exc)]
        journal.receipt(workspace, GATE,
                        _hashes(workspace, {MATCH_FILE, SHORTLIST_FILE, BRIEF_FILE}),
                        "fail", findings)
        print(*findings, sep="\n")
        return 1

    findings, inputs = check(workspace, match, profile, shortlist, brief, markdown,
                             verify_rendered=not args.render)
    if args.render:
        if findings:
            print(*findings, sep="\n")
            return 1
        for entry in match.get("rows") or []:
            row = journal.as_mapping(entry)
            print(f"{row.get('id')}: {matching.render_summary(row, args.lang)}")
        return 0

    hashes = _hashes(workspace, inputs)
    journal.receipt(workspace, GATE, hashes, "fail" if findings else "pass", findings)
    if findings:
        print(*findings, sep="\n")
        return 1
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
