#!/usr/bin/env python3
"""Create a non-blocking delivery report for a fingering result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from plan_io import load_plan
from validate_recognition import validate_recognition


LEVELS = {
    "complete": "Complete result",
    "review": "Review-required result",
    "partial": "Partial result",
}

USER_SUMMARIES = {
    "complete": ("Ready to use", "Recognition, fingering, and layout checks completed."),
    "review": ("Available for trial; review recommended", "Fingerings generated; some review items remain."),
    "partial": ("Incomplete result; files retained", "Some notes are unassigned or could not be printed safely. Use these files to locate issues and continue repair."),
}


def audit_status(path: Path | None, label: str) -> tuple[bool, str]:
    if path is None:
        return False, f"{label}: not supplied"
    if not path.is_file():
        return False, f"{label}: file not found"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        accuracy = float(payload["placement_accuracy"])
        failures = payload.get("failures", [])
        if not isinstance(failures, list):
            raise ValueError("failures must be a list")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return False, f"{label}: cannot read a valid audit result ({exc})"
    passed = accuracy >= 0.90 and not failures
    return passed, f"{label}: {'Passed' if passed else 'Failed'}({accuracy:.1%}, failures:  {len(failures)} items)"


def stability_status(path: Path | None) -> tuple[bool, str, int, list[dict]]:
    if path is None:
        return False, "Fingering stability audit: not supplied", 0, []
    if not path.is_file():
        return False, "Fingering stability audit: file not found", 0, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        accuracy = float(payload["stability_accuracy"])
        passed = payload.get("passed") is True
        shallow_depth = int(payload.get("shallow_depth", 4))
        deep_depth = int(payload.get("deep_depth", 7))
        unstable = payload.get("unstable_notes", [])
        if not isinstance(unstable, list):
            raise ValueError("unstable_notes must be a list")
        reviewed = payload.get("reviewed_unstable_notes", [])
        if not isinstance(reviewed, list):
            raise ValueError("reviewed_unstable_notes must be a list")
        scopes = payload.get("review_scopes", [])
        if not isinstance(scopes, list):
            raise ValueError("review_scopes must be a list")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return False, f"Fingering stability audit: cannot read a valid result ({exc})", 0, []
    return (
        passed,
        f"Fingering stability audit ({shallow_depth}/{deep_depth} -event search): "
        f"{'Passed' if passed else 'Needs review'}({accuracy:.1%}, pending:  {len(unstable)} notes"
        + (f", resolved:  {len(reviewed)} items)" if reviewed else ")"),
        len(unstable),
        scopes,
    )


def fingering_quality_status(path: Path | None) -> tuple[bool, str]:
    """Read the mechanical fingering-quality gate without calling it exact editorial truth."""
    if path is None:
        return False, "Fingering rule-compliance audit: not supplied"
    if not path.is_file():
        return False, "Fingering rule-compliance audit: file not found"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        accuracy = float(payload["quality_accuracy"])
        violations = payload.get("violations", {})
        if not isinstance(violations, dict):
            raise ValueError("violations must be an object")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return False, f"Fingering rule-compliance audit: cannot read a valid result ({exc})"
    passed = accuracy >= 0.80 and not violations
    return passed, f"Fingering rule-compliance audit: {'Passed' if passed else 'Needs review'}({accuracy:.1%}, violations:  {len(violations)} notes)"


def phrase_risk_status(path: Path | None) -> tuple[bool, str, int, list[dict]]:
    """Read conservative phrase-entry/reposition risk without calling it an error."""
    if path is None:
        return False, "Phrase hand-position audit: not supplied", 0, []
    if not path.is_file():
        return False, "Phrase hand-position audit: file not found", 0, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        passed = payload.get("passed") is True
        risks = payload.get("risk_notes", [])
        scopes = payload.get("review_scopes", [])
        if not isinstance(risks, list) or not isinstance(scopes, list):
            raise ValueError("risk_notes and review_scopes must be lists")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return False, f"Phrase hand-position audit: cannot read a valid result ({exc})", 0, []
    return passed, f"Phrase hand-position audit: {'Passed' if passed else 'Needs review'}({len(risks)} unreviewed hand repositions)", len(risks), scopes


def hand_size_status(path: Path | None) -> tuple[bool, str, int, list[dict]]:
    """Read optional local hand-size sensitivity without treating it as an error."""
    if path is None or not path.is_file():
        return True, "Hand-size sensitivity audit: not run", 0, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        accuracy = float(payload["stability_accuracy"])
        unstable = payload.get("unstable_notes", [])
        scopes = payload.get("review_scopes", [])
        alternate = str(payload.get("alternate_hand_size", "adjacent preset"))
        if not isinstance(unstable, list) or not isinstance(scopes, list):
            raise ValueError("unstable_notes and review_scopes must be lists")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return False, f"Hand-size sensitivity audit: cannot read a valid result ({exc})", 0, []
    return True, f"Hand-size sensitivity audit: agreement with  {alternate} agreement {accuracy:.1%} (disagreements:  {len(unstable)} notes)", len(unstable), scopes


def editorial_reference_status(path: Path | None) -> str | None:
    """Return optional exact-match evidence without treating it as universal truth."""
    if path is None:
        return None
    if not path.is_file():
        return "Editorial comparison: file not found"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        accuracy = float(payload["accuracy"])
        anchors = int(payload["anchors"])
        matches = int(payload["matches"])
        if anchors < 1 or not 0 <= accuracy <= 1:
            raise ValueError("invalid anchor count or accuracy")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return f"Editorial comparison: cannot read a valid result ({exc})"
    return (
        f"Editorial comparison: {matches} / {anchors}({accuracy:.1%}); "
        "This is exact agreement with the selected editorial version; alternative fingerings may remain playable."
    )


def review_manifest_status(path: Path | None) -> tuple[int, str | None]:
    """Expose a concrete local-review artifact without treating it as a failure.

    A search disagreement needs musical judgement, but it must never leave the
    recipient with a vague instruction to "review the piece".  The manifest
    keeps only affected measure/hand scopes plus surrounding events.
    """
    if path is None:
        return 0, None
    if not path.is_file():
        return 0, "Local fingering review tasks: file not found"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        tasks = payload.get("tasks", [])
        if not isinstance(tasks, list):
            raise ValueError("tasks must be a list")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return 0, f"Local fingering review tasks: cannot read ({exc})"
    return len(tasks), f"Local fingering review tasks: generated  {len(tasks)} measures/hand scopes"


def omr_risk_lines(plan: dict) -> list[str]:
    """Summarise only the OMR receipt's declared risks for a human handoff.

    These are not score facts and must not be turned into invented measure
    numbers.  They are nevertheless more actionable than a generic
    "candidate" warning when an engine already says that, for example, octave
    symbols or rhythm links need attention.
    """
    context = plan.get("source", {}).get("omr_candidate", {})
    if not isinstance(context, dict):
        return []
    raw_report = str(context.get("report", "")).strip()
    report_path = Path(raw_report) if raw_report else None
    if not report_path or not report_path.is_file():
        return []
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        risks = payload.get("semantic_risk_signals", [])
        if not isinstance(risks, list):
            return []
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return []
    lines: list[str] = []
    for risk in risks[:8]:
        if not isinstance(risk, dict):
            continue
        code = str(risk.get("code", "unknown risk"))
        try:
            count = int(risk.get("count", 0))
        except (TypeError, ValueError):
            count = 0
        examples = risk.get("examples", [])
        detail = ""
        if isinstance(examples, list) and examples and isinstance(examples[0], str):
            # Keep the receipt readable, not a pasted engine log.
            detail = f" (example: {examples[0].split('|')[-1].strip()[:160]})"
        lines.append(f"- Local  OMR report flagged  **{code}**: {count} items{detail}")
    return lines


def user_scope(recognition: dict, visual_source: bool) -> str:
    """Turn internal recognition scope into a short user-facing description."""
    scopes = recognition.get("measure_scope", [])
    if visual_source and isinstance(scopes, list) and scopes:
        pages: set[int] = set()
        measures = 0
        for item in scopes:
            if not isinstance(item, dict):
                continue
            try:
                pages.add(int(item["page"]))
                measures += int(item["measure_end"]) - int(item["measure_start"]) + 1
            except (KeyError, TypeError, ValueError):
                continue
        if pages and measures:
            page_text = ", ".join(str(page) for page in sorted(pages))
            return f"Pages {page_text}; {measures} measures"
    return str(recognition.get("scope", "All notes in the plan"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--source-score", type=Path, help="immutable source copy preserved for a review/blocked run")
    parser.add_argument("--musicxml", type=Path)
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--collisions", type=int, default=0)
    parser.add_argument("--placement-audit", type=Path, help="audit_annotation_layout.py from JSON Result")
    parser.add_argument("--source-anchor-audit", type=Path, help="audit_source_noteheads.py from JSON Result")
    parser.add_argument("--source-clearance-audit", type=Path, help="audit_source_clearance.py from JSON Result")
    parser.add_argument("--rendered-placement-audit", type=Path, help="audit_rendered_labels.py from JSON Result")
    parser.add_argument("--stability-audit", type=Path, help="audit_fingering_stability.py from JSON Result")
    parser.add_argument("--fingering-quality", type=Path, help="evaluate_fingering_quality.py from JSON Result")
    parser.add_argument("--phrase-risk-audit", type=Path, help="audit_phrase_risk.py from JSON Result")
    parser.add_argument("--hand-size-audit", type=Path, help="audit_hand_size_stability.py from JSON Result")
    parser.add_argument("--fingering-review", type=Path, help="Optional: local phrase review tasks for search disagreements")
    parser.add_argument("--editorial-comparison", type=Path, help="Optional: compare_reference_fingerings.py from JSON Result")
    args = parser.parse_args()

    plan = load_plan(args.plan)
    recognition_errors, recognition_warnings = validate_recognition(plan, strict=True)
    recognition_passed = not recognition_errors
    notes = plan.get("notes", [])
    recognition = plan.get("recognition", {})
    expected = int(recognition.get("expected_note_count", len(notes)))
    expected = max(expected, len(notes), 1)
    assigned = sum(1 for note in notes if int(note.get("finger", 0)) in {1, 2, 3, 4, 5})
    unresolved = int(recognition.get("unresolved_note_count", 0))
    low_confidence = [
        note for note in notes
        if float(note.get("confidence", 1.0)) < 0.8 or note.get("review_reason")
    ]
    coverage = assigned / expected
    source_type = str(plan.get("source", {}).get("type", "musicxml")).lower()
    hand_size = str(plan.get("settings", {}).get("hand_size", "M")).upper()
    if hand_size not in {"XXS", "XS", "S", "M", "L", "XL", "XXL"}:
        hand_size = "M"
    visual_source = source_type in {"pdf", "image"}
    omr_candidate = source_type == "omr_candidate"
    provisional_state = recognition.get("provisional_omr", {}) if isinstance(recognition, dict) else {}
    provisional_pdf = (
        omr_candidate
        and isinstance(provisional_state, dict)
        and provisional_state.get("status") == "review_required"
        and bool(args.pdf and args.pdf.is_file())
    )
    provisional_labelled = int(provisional_state.get("labelled_noteheads", assigned) or 0) if provisional_pdf else 0
    provisional_unlabelled = int(
        provisional_state.get("unlabelled_notes", max(0, expected - provisional_labelled)) or 0
    ) if provisional_pdf else 0
    source_label = "Local  OMR candidate (source verification incomplete)" if omr_candidate else "Structured  MusicXML"
    selected_piano_parts = plan.get("source", {}).get("selected_piano_parts", [])
    if not isinstance(selected_piano_parts, list):
        selected_piano_parts = []
    piano_part_line = (
        ", ".join(str(part) for part in selected_piano_parts if str(part).strip())
        or "Unspecified (legacy plan)"
    )
    audit_inputs = (
        (args.placement_audit, "Planned label ownership audit"),
        (args.source_anchor_audit, "Source notehead anchor audit"),
        (args.source_clearance_audit, "Source notation clearance audit"),
        (args.rendered_placement_audit, "Final rendered-output audit"),
    )
    audit_lines = [audit_status(path, label) for path, label in audit_inputs]
    stability_passed, stability_line, unstable_count, unstable_scopes = stability_status(args.stability_audit)
    quality_passed, quality_line = fingering_quality_status(args.fingering_quality)
    phrase_risk_passed, phrase_risk_line, phrase_risk_count, phrase_risk_scopes = phrase_risk_status(args.phrase_risk_audit)
    _, hand_size_line, hand_size_count, hand_size_scopes = hand_size_status(args.hand_size_audit)
    editorial_line = editorial_reference_status(args.editorial_comparison)
    review_task_count, review_manifest_line = review_manifest_status(args.fingering_review)
    visual_audits_passed = all(passed for passed, _ in audit_lines) if visual_source else True
    symbol_checks = recognition.get("measure_symbol_checks", [])
    count_sources = {
        str(check.get("source", "unknown"))
        for check in symbol_checks
        if isinstance(check, dict)
    }
    independent_visual_counts = bool(symbol_checks) and count_sources == {"independent_visual_review"}
    requested = str(recognition.get("delivery_level", "complete")).lower()
    # OMR candidate notes are intentionally present in the plan so their
    # measure/hand scope can be inspected.  They are not resolved score facts:
    # reporting "0 unresolved" here made a blocked run look healthier than it
    # was.  Keep the stored recognition counter intact, but expose the number
    # of candidate notes still requiring raw-page confirmation to the user.
    pending_visual_confirmation = expected if omr_candidate else 0
    # A threshold pass can still conceal a meaningful set of alternate
    # fingerings.  Present that case as review-level rather than giving users
    # an unconditional "ready to use" headline; it is a confidence signal,
    # not proof that every phrase has a uniquely good solution.
    if recognition_passed and coverage >= 1 and unresolved == 0 and args.collisions == 0 and not low_confidence and quality_passed and stability_passed and unstable_count == 0 and phrase_risk_passed and phrase_risk_count == 0 and visual_audits_passed and (not visual_source or independent_visual_counts):
        level = "complete"
    # Missing even one score-note fingering is an incomplete deliverable.
    # The old 80% cutoff let 83/84 labels appear as a general review result,
    # although the user had explicitly asked for a complete score.
    elif requested == "partial" or coverage < 1:
        level = "partial"
    else:
        level = "review"

    # The plan itself is always the first deliverable.  Do not call a draft
    # recognition plan a fingering result: this was a recurring source of
    # confusing reports after a recognition gate correctly stopped the solver.
    plan_label = "Fingering plan JSON" if assigned else "Current recognition plan JSON"
    plan_state = (
        f"Generated with  {assigned} finger assignments"
        if args.plan.is_file() and assigned
        else "Generated; fingering generation has not started"
        if args.plan.is_file()
        else "Path recorded; file not found"
    )
    artifacts = [(plan_label, args.plan, plan_state)]
    if args.source_score:
        state = "Preserved without added fingerings" if args.source_score.is_file() else "Path recorded; file not found"
        artifacts.append(("Source score copy", args.source_score, state))
    for label, path in (("PDF", args.pdf), ("MusicXML", args.musicxml), ("PNG preview", args.preview)):
        if path:
            state = "Generated" if path.is_file() else "Path recorded; file not found"
            artifacts.append((label, path, state))
    if args.fingering_review:
        state = "Generated; includes only measures requiring decisions" if args.fingering_review.is_file() else "Path recorded; file not found"
        artifacts.append(("Local fingering review tasks", args.fingering_review, state))

    review_lines = []
    for note in low_confidence[:30]:
        reason = note.get("review_reason", "Low-confidence recognition")
        review_lines.append(f"- `{note.get('note_id', 'unknown')}`: {reason}")
    if len(low_confidence) > 30:
        review_lines.append(f"- Additionally,  {len(low_confidence) - 30} low-confidence notes; see the plan")
    if unresolved:
        review_lines.append(f"- Within the target scope,  {unresolved} notes remain unresolved")
    if pending_visual_confirmation:
        review_lines.append(f"- {pending_visual_confirmation} candidate notes still require source-measure verification")
    for error in recognition_errors[:30]:
        review_lines.append(f"- Recognition gate failed: {error}")
    if len(recognition_errors) > 30:
        review_lines.append(f"- Additionally,  {len(recognition_errors) - 30} additional recognition-gate errors; see the plan")
    for warning in recognition_warnings[:10]:
        review_lines.append(f"- Recognition warning: {warning}")
    if visual_source:
        for passed, line in audit_lines:
            if not passed:
                review_lines.append(f"- {line}")
        if not independent_visual_counts:
            sources = ", ".join(sorted(count_sources)) if count_sources else "Not supplied"
            review_lines.append(f"- Measure note//rest count sources: {sources}; incomplete independent visual review excludes this from complete visual acceptance")
    if not stability_passed:
        review_lines.append(f"- {stability_line}")
        if review_manifest_line:
            review_lines.append(f"- {review_manifest_line}; review these local phrases before recomputing other scopes")
    elif unstable_count:
        formatted_scopes = []
        for scope in unstable_scopes[:8]:
            try:
                page = int(scope.get("page", 0))
                measure = int(scope["measure"])
                hand = str(scope["hand"])
                count = int(scope["unstable_notes"])
                prefix = f"No.  {page} page, " if page else ""
                formatted_scopes.append(f"{prefix}No.  {measure} measure {hand}({count} items)")
            except (AttributeError, KeyError, TypeError, ValueError):
                continue
        suffix = "; ".join(formatted_scopes)
        review_lines.append(
            f"- Search stability passed, with  {unstable_count} notes have different fingers at different search depths"
            + (f": {suffix}" if suffix else "; prioritize play-through//review these measures")
        )
        if review_manifest_line:
            review_lines.append(f"- {review_manifest_line}; choose one complete candidate per task without mixing digits")
    if not quality_passed:
        review_lines.append(f"- {quality_line}")
    if not phrase_risk_passed:
        review_lines.append(f"- {phrase_risk_line}")
    elif phrase_risk_count:
        scope_text = []
        for scope in phrase_risk_scopes[:8]:
            try:
                page = int(scope.get("page", 0))
                prefix = f"No.  {page} page, " if page else ""
                scope_text.append(f"{prefix}No.  {int(scope['measure'])} measure {scope['hand']}({int(scope['risk_notes'])} items)")
            except (AttributeError, KeyError, TypeError, ValueError):
                continue
        review_lines.append(f"- {phrase_risk_line}" + (f": {'; '.join(scope_text)}" if scope_text else ""))
    if hand_size_count:
        scope_text = []
        for scope in hand_size_scopes[:6]:
            try:
                page = int(scope.get("page", 0))
                prefix = f"No.  {page} page, " if page else ""
                scope_text.append(f"{prefix}No.  {int(scope['measure'])} measure {scope['hand']}({int(scope['unstable_notes'])} items)")
            except (AttributeError, KeyError, TypeError, ValueError):
                continue
        review_lines.append(f"- {hand_size_line}" + (f"; review first: {'; '.join(scope_text)}" if scope_text else ""))
    if editorial_line and "file not found" in editorial_line.lower():
        review_lines.append(f"- {editorial_line}")
    if not review_lines:
        review_lines.append("- None")
    if omr_candidate:
        context = plan.get("source", {}).get("omr_candidate", {})
        engine = str(context.get("engine", "local_omr")) if isinstance(context, dict) else "local_omr"
        candidate_line = (
            f"- Current source:  {engine} Local  OMR candidate; "
            + (
                f"Temporarily printed  {provisional_labelled} candidate labels printed for page-by-page review."
                if provisional_pdf else "Use it for measure-by-measure comparison before formal fingering generation."
            )
        )
        review_lines.insert(
            0,
            candidate_line,
        )
        review_lines[1:1] = omr_risk_lines(plan)

    if provisional_pdf:
        next_action = (
            "Prioritize verification of  OMR risk measures and withheld scopes; verify source facts before producing a complete formal  PDF."
            if provisional_unlabelled else
            "Prioritize verification of  OMR risk measures; verify source facts before producing a formal  PDF."
        )
    elif recognition_errors:
        next_action = "Use page+measure+hand to locate failed gates; repair, relock facts, and rerun downstream checks."
    elif visual_source and not visual_audits_passed:
        next_action = "Repair failed labels or anchors, rerender, and audit the output. Preserve unrelated measure fingerings."
    elif not stability_passed:
        next_action = "Open the review tasks, resolve measures with search disagreements, then rerun hard validation and stability checks."
    elif not quality_passed:
        next_action = "Locate hard-rule violations by note, repair them, and rerun quality and stability checks."
    elif not phrase_risk_passed or phrase_risk_count:
        next_action = "Review the listed connected phrases for necessary repositioning; resolve these scopes and recheck."
    elif unresolved or low_confidence:
        next_action = "Recheck low-confidence source measures independently before continuing."
    elif unstable_count:
        next_action = "Compare candidates and neighboring phrases in the local review tasks; preserve unaffected scopes."
    else:
        next_action = "No recovery is required."

    headline, explanation = USER_SUMMARIES[level]
    if omr_candidate:
        explanation = "The local OMR candidate and risk scopes are retained. Source verification is incomplete, so no fingerings or page annotations were generated."
        if provisional_pdf:
            explanation = "Produced a candidate notehead-anchored  PDF; whole-page recognition still requires source verification."
            if provisional_unlabelled:
                explanation = (
                    f"Produced a candidate notehead-anchored  PDF; {provisional_unlabelled} labels with unsafe placement were withheld; "
                    "and whole-page recognition still requires source verification."
                )
    elif not visual_source and level == "complete":
        explanation = "Structured score and fingering checks completed; original-page annotation was not performed."
    elif not visual_source and level == "review":
        explanation = "Structured fingerings generated; original-page annotation was not performed and review items remain."
    audit_rows = [
        ("Assigned fingerings", f"{assigned} / {expected} notes ({coverage:.0%})"),
        ("Hand-size preset", hand_size),
        ("Score facts", "Confirmed" if recognition_passed else "Unconfirmed items remain"),
        ("Fingering rules", "Passed" if quality_passed else "Needs review"),
        ("Fingering stability", "Passed" if stability_passed else "Needs review"),
        ("Local review tasks", f"{review_task_count} items" if review_manifest_line else "Not generated"),
        ("Phrase hand-position risk", "Passed" if phrase_risk_passed and not phrase_risk_count else "Needs review"),
        ("Hand-size sensitivity", "Disagreements found" if hand_size_count else "No disagreements found"),
    ]
    if editorial_line:
        audit_rows.append(("Editorial reference", editorial_line.replace("Editorial comparison: ", "").split("; ", 1)[0]))
    if visual_source:
        audit_rows.extend((
            ("Notehead placement", "Passed" if audit_lines[1][0] else "Needs repair"),
            ("Notation clearance", "Passed" if audit_lines[2][0] else "Needs repair"),
            ("Placement after export", "Passed" if audit_lines[3][0] else "Needs repair"),
        ))
    detail_lines = [f"| {label} | {result} |" for label, result in audit_rows]
    artifact_lines = [
        f"- **{label}**: `{path}`({state})" if path else f"- **{label}**: {state}"
        for label, path, state in artifacts
    ]
    attention_title = "Items to review" if review_lines != ["- None"] else "Items to review"
    attention_lines = review_lines if review_lines != ["- None"] else ["- No additional issues require attention."]

    text = "\n".join([
        "# Piano Fingering Results",
        "",
        f"> **{headline}** · {explanation}",
        "",
        "## Deliverables",
        "",
        *artifact_lines,
        "",
        "## Processing scope",
        "",
        f"- Scope: {user_scope(recognition, visual_source)}",
        f"- Hand-size preset: **{hand_size}** (default when unspecified:  M)",
        f"- Assigned fingerings: **{assigned} / {expected}** notes",
        (
            f"- Pending source verification: **{pending_visual_confirmation} / {expected}** notes; "
            + (
                f"{provisional_labelled} candidate labels printed; "
                + (f"Additionally,  {provisional_unlabelled} labels not printed" if provisional_unlabelled else "No labels withheld for layout")
                if provisional_pdf else "Fingerings and page annotations have not yet been generated"
            )
            if pending_visual_confirmation else
            f"- Unresolved fingerings: **{unresolved}** items; low confidence: **{len(low_confidence)}** items"
        ),
        "",
        "## Quick checks",
        "",
        "| Item | Result |",
        "| --- | --- |",
        *detail_lines,
        "",
        f"## {attention_title}",
        "",
        *attention_lines,
        "",
        "## Next steps",
        "",
        f"- {next_action}",
        *( ["- If score facts remain unclear, provide the affected crop and a focused question so review can continue from that scope."] if level != "complete" else []),
        "",
        "---",
        "",
        "### Technical check details",
        "",
        f"- Delivery level: {LEVELS[level]}",
        f"- Measure note/rest counts: {'Independent visual review' if independent_visual_counts else 'Independent visual review incomplete'}" if visual_source else f"- Source: {source_label}",
        f"- Selected piano parts: {piano_part_line}",
        f"- {stability_line}",
        f"- {phrase_risk_line}",
        f"- {hand_size_line}",
        f"- {quality_line}",
        *( [f"- {editorial_line}"] if editorial_line else []),
        *( [f"- {line}" for _, line in audit_lines] if visual_source else []),
        f"- Label collisions: {max(args.collisions, 0)}",
        "",
        "",
    ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Created {LEVELS[level]} report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
