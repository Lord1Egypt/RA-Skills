#!/usr/bin/env python3
"""Product-specific local validator for Literature Review Paper Screener cloud results.

Reads a LoomLoom result-rows JSON file (or a plain JSON with a `rows` list) that contains
**one row per screened paper** (V1.1 per-paper execution model), merges the screening + build
step artifacts of every completed row into one global view, and checks the product contract:

1. Result parses and matches the declared output shape (screening_records + excluded_records,
   paper_sheet + reading_list) for every completed row.
2. Every included paper in Paper Sheet appears in the screened pool; excluded papers never appear.
3. Evidence availability level is present on every record (A/B/C/D).
4. Content Credibility follows the decision rule: never Fail simply due to lack of evidence.
5. Reading List uses the same pool, one Primary Reading Role per paper, no duplication.
6. Citation / links present where available.
7. No duplicate record IDs across the merged per-paper rows.
8. Failures, incomplete rows, and partial results are explicit: a row that failed, or that is
   `completed` yet lacks a required artifact, is reported rather than silently dropped, and
   every submitted row is accounted for.
9. Findings are reproducible (rerun condition = same evidence records + version).

Rejects fabricated, mismatched, or unreviewable output. Writes review/validation-report.json
and review/local-audit.json. Uses only the Python standard library.
"""

import argparse
import json
import sys
from pathlib import Path

LEVELS = {"A", "B", "C", "D"}
ROLES = {"Foundational", "Core Evidence", "Supporting", "Counterargument", "Recent", "Methodology"}
SCREEN_STEP_IDS = ("stp_screen01", "stp_screen1")  # CogFoundry v1 / ShengSuanYun v2
BUILD_STEP_IDS = ("stp_build01",)  # both platforms use stp_build01


def pick_artifact(arts, step_ids):
    for sid in step_ids:
        if arts.get(sid):
            return arts[sid]
    return ""


def collect_artifacts(rows):
    """Return (sets, incomplete).

    `sets` holds one {step_id: inlineText} dict per auditable row. A row is auditable only when it
    is `completed` AND carries BOTH the screening artifact and the build artifact. A `completed`
    row missing either one is recorded in `incomplete` so that it is reported and blocks the audit,
    instead of being silently dropped from the rows the validator claims to have checked.
    """
    sets = []
    incomplete = []
    for index, row in enumerate(rows):
        if row.get("status") != "completed":
            continue
        arts = {}
        for a in row.get("artifacts", []):
            step = a.get("stepId", "")
            txt = a.get("inlineText", "")
            if step and txt:
                arts[step] = txt
        missing = []
        if not pick_artifact(arts, SCREEN_STEP_IDS):
            missing.append("screening")
        if not pick_artifact(arts, BUILD_STEP_IDS):
            missing.append("build")
        if missing:
            incomplete.append({
                "row": index,
                "recordId": row.get("recordId") or row.get("record_id") or "",
                "missing": missing,
            })
            continue
        sets.append(arts)
    return sets, incomplete


def strip_code_fence(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1]
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def parse_json(text, label):
    try:
        return json.loads(strip_code_fence(text))
    except json.JSONDecodeError as e:
        raise ValueError(f"{label}: result is not valid JSON ({e})")


def merge_sets(sets):
    """Merge per-row step artifacts into global screen/build objects."""
    screen = {"screening_records": [], "excluded_records": []}
    build = {"paper_sheet": [], "reading_list": {}}
    for arts in sets:
        try:
            s = parse_json(pick_artifact(arts, SCREEN_STEP_IDS), "screening step")
        except ValueError as e:
            raise ValueError(f"screening step: {e}")
        try:
            b = parse_json(pick_artifact(arts, BUILD_STEP_IDS), "build step")
        except ValueError as e:
            raise ValueError(f"build step: {e}")
        # Schema guard: an empty/{} artifact must NOT silently pass as an audited row.
        # Each row must carry exactly one screening or exclusion decision and a paper_sheet entry.
        if not s or not isinstance(s, dict):
            raise ValueError("screening step artifact is empty/invalid for this row")
        if not b or not isinstance(b, dict):
            raise ValueError("build step artifact is empty/invalid for this row")
        scr = s.get("screening_records")
        exc = s.get("excluded_records")
        if not isinstance(scr, list) or not isinstance(exc, list):
            raise ValueError("screening_records/excluded_records must be lists")
        n_decisions = len(scr) + len(exc)
        # Exactly one decision per submitted paper (one paper per row). More than one means the
        # artifact was manipulated or mis-assembled and must not be silently merged.
        if n_decisions == 0:
            raise ValueError(
                "row has neither screening_records nor excluded_records — "
                "malformed or empty result must not be counted as audited"
            )
        if n_decisions != 1:
            raise ValueError(
                f"row has {n_decisions} decisions (screening={len(scr)}, excluded={len(exc)}); "
                "exactly one decision per submitted paper is required"
            )
        if not isinstance(b.get("paper_sheet"), list) or not b.get("paper_sheet"):
            raise ValueError("build step artifact has no paper_sheet entry for this row")
        if len(b.get("paper_sheet")) != 1:
            raise ValueError(
                f"row has {len(b.get('paper_sheet'))} paper_sheet entries; expected exactly 1"
            )
        screen["screening_records"].extend(s.get("screening_records", []))
        screen["excluded_records"].extend(s.get("excluded_records", []))
        build["paper_sheet"].extend(b.get("paper_sheet", []))
        for cat, items in b.get("reading_list", {}).items():
            build["reading_list"].setdefault(cat, []).extend(items)
    return screen, build


def normalize_level(lvl):
    """Accept 'A', 'A Full Evidence', 'B Extended Evidence', etc. (model style varies)."""
    if not lvl:
        return ""
    return lvl.strip()[0].upper() if lvl.strip() else ""


def audit(screen, build, failed_rows=0, incomplete=None, accounting=None):
    issues = []
    sr = screen.get("screening_records", [])
    er = screen.get("excluded_records", [])
    ps = build.get("paper_sheet", [])
    rl = build.get("reading_list", {})

    # 0. failed rows surfaced
    if failed_rows:
        issues.append(f"{failed_rows} row(s) did not complete — results are partial")

    # 0b. a completed row that lacks a required artifact must never be skipped silently
    for item in incomplete or []:
        label = item.get("recordId") or f"row {item.get('row')}"
        issues.append(
            f"{label}: status=completed but missing required artifact(s) "
            f"({', '.join(item.get('missing', []))}) — row was not audited"
        )

    # 0c. row accounting: every submitted row must be audited, incomplete, or failed
    if accounting:
        total = accounting.get("rowsTotal")
        completed = accounting.get("rowsCompleted")
        audited = accounting.get("rowsAudited")
        incomplete_n = accounting.get("rowsIncomplete", 0)
        if completed is not None and audited is not None and completed != audited + incomplete_n:
            issues.append(
                f"completed-row accounting mismatch: {completed} completed row(s) vs "
                f"{audited} audited + {incomplete_n} incomplete"
            )
        if total is not None and audited is not None:
            accounted = audited + incomplete_n + failed_rows
            if accounted != total:
                issues.append(
                    f"row accounting mismatch: {total} submitted row(s) but only {accounted} "
                    f"accounted for (audited={audited}, incomplete={incomplete_n}, failed={failed_rows})"
                )

    # 1. evidence level + credibility rules on screening records
    for p in sr + er:
        lvl = p.get("evidence_availability_level", "")
        if normalize_level(lvl) not in LEVELS:
            issues.append(f"{p.get('record_id')}: missing/invalid evidence_availability_level {lvl!r}")
        cc = p.get("content_credibility_status", "")
        if not cc:
            issues.append(f"{p.get('record_id')}: missing content_credibility_status")
        else:
            ccl = cc.casefold()
            UNAVAILABLE_MARKERS = ("not available", "unavailable", "cannot assess", "insufficient evidence",
                                   "no content", "unable", "not assessable", "not-assessable")
            is_unavailable = any(m in ccl for m in UNAVAILABLE_MARKERS)
            # Level-D (metadata-only) must be reported as not-assessable, not as a content judgement.
            if normalize_level(lvl) == "D" and not is_unavailable:
                issues.append(
                    f"{p.get('record_id')}: level-D (metadata-only) must use an unavailable/not-assessable "
                    f"content_credibility_status, got {cc!r}"
                )
            # A "Fail" driven solely by missing content must be recorded as not-assessable, not a quality fail.
            if ("fail" in ccl) and is_unavailable:
                issues.append(
                    f"{p.get('record_id')}: credibility marked 'Fail' but reason is unavailable content — "
                    "use a not-assessable outcome instead of failing the paper for missing content"
                )

    # 1b. no duplicate record IDs across merged rows
    seen_ids = {}
    for p in sr + er:
        rid = p.get("record_id")
        if rid in seen_ids:
            issues.append(f"duplicate record_id across rows: {rid}")
        seen_ids[rid] = True

    # 2. excluded never in paper sheet
    excluded_ids = {p.get("record_id") for p in er}
    for p in ps:
        rid = p.get("record_id")
        if rid in excluded_ids:
            issues.append(f"{rid}: excluded paper appears in paper_sheet")

    # 3. paper sheet = subset of screened pool
    screened_ids = {p.get("record_id") for p in sr}
    for p in ps:
        if p.get("record_id") not in screened_ids:
            issues.append(f"{p.get('record_id')}: paper_sheet entry not in screening_records")

    # 4. reading list: same pool (by record_id), one role each, no duplicates
    rl_ids = set()
    for cat, items in rl.items():
        if cat not in ROLES:
            issues.append(f"unknown reading_list category {cat!r}")
        for it in items:
            rid = it.get("record_id")
            if not rid:
                issues.append("reading_list entry missing record_id")
                continue
            if rid in rl_ids:
                issues.append(f"{rid}: duplicated reading_list entry")
            rl_ids.add(rid)
            role = it.get("reading_role")
            if role != cat:
                issues.append(f"{rid}: reading_role {role!r} does not match category {cat!r}")
    paper_ids = {p.get("record_id") for p in ps}
    if paper_ids != rl_ids:
        issues.append(f"paper_sheet and reading_list pools differ by record_id (only_in_sheet={len(paper_ids - rl_ids)}, only_in_reading={len(rl_ids - paper_ids)})")
    if ps and not rl_ids:
        issues.append("paper_sheet has entries but reading_list is empty")

    # 5. citation present on paper sheet entries
    for p in ps:
        if not p.get("citation"):
            issues.append(f"{p.get('record_id')}: missing citation")

    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="result-rows JSON from loomloom run result-rows (may contain many per-paper rows)")
    ap.add_argument("--manifest", default=None, help="optional store-manifest.json for context")
    ap.add_argument("--out-dir", default="review", help="output directory")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = data.get("rows", data if isinstance(data, list) else [])
    rows_total = len(rows)
    completed_rows = sum(1 for r in rows if r.get("status") == "completed")
    failed_rows = sum(1 for r in rows if r.get("status") != "completed")

    sets, incomplete = collect_artifacts(rows)
    if not sets:
        reason = ("no completed row artifacts found" if not incomplete else
                  f"no auditable row: all {len(incomplete)} completed row(s) lack required artifacts")
        print(json.dumps({"result": "FAIL", "reason": reason, "incompleteRows": incomplete}, indent=2))
        sys.exit(1)

    try:
        screen, build = merge_sets(sets)
    except ValueError as e:
        print(json.dumps({"result": "FAIL", "reason": str(e)}, indent=2))
        sys.exit(1)

    accounting = {
        "rowsTotal": rows_total,
        "rowsCompleted": completed_rows,
        "rowsAudited": len(sets),
        "rowsIncomplete": len(incomplete),
    }
    issues = audit(screen, build, failed_rows, incomplete, accounting)
    passed = not issues

    audit_out = {
        "result": "PASS" if passed else "FAIL",
        "issues": issues,
        "rowsTotal": rows_total,
        "rowsCompleted": completed_rows,
        "rowsAudited": len(sets),
        "rowsIncomplete": len(incomplete),
        "incompleteRows": incomplete,
        "rowsFailed": failed_rows,
        "screeningRecords": len(screen.get("screening_records", [])),
        "excludedRecords": len(screen.get("excluded_records", [])),
        "paperSheetEntries": len(build.get("paper_sheet", [])),
        "readingListCategories": {k: len(v) for k, v in build.get("reading_list", {}).items()},
        "rerunCondition": "same per-paper evidence records + template version 4677c008-6780-425e-b2f7-c05bc7caba38",
    }
    report = {
        "result": "PASS" if passed else "FAIL",
        "validator": "literature-review-paper-screener local validator",
        "checks": [
            "parseable structured output (every completed row)",
            "evidence availability levels A-D present",
            "content credibility decision rule respected",
            "paper sheet contains only screened pool",
            "reading list shares the same pool with one role per paper",
            "citations present",
            "no duplicate record IDs across merged rows",
            "explicit failures/partial results (failed rows surfaced)",
            "reproducible rerun condition",
        ],
        "audit": audit_out,
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for target in (out_dir / "local-audit.json", out_dir / "validation-report.json"):
        if target.exists():
            print(f"WARNING: overwriting existing file {target}", file=sys.stderr)
    (out_dir / "local-audit.json").write_text(json.dumps(audit_out, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()