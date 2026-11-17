#!/usr/bin/env python3
"""Run local fingering stages with bounded time and an always-written report.

This is a coordinator, not another solver.  It prevents a long-running stage
from leaving the user with only terminal output: every started run records its
stage logs, last usable plan, and a readable delivery report.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import math
import shutil
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_stage(name: str, command: list[str], directory: Path, timeout: int) -> dict:
    started = time.time()
    record: dict[str, object] = {"name": name, "command": command, "started_at": started}
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        record.update({
            "status": "passed" if completed.returncode == 0 else "failed",
            "return_code": completed.returncode,
            "stdout": completed.stdout[-12000:],
            "stderr": completed.stderr[-12000:],
        })
    except subprocess.TimeoutExpired as exc:
        record.update({
            "status": "timed_out",
            "return_code": None,
            "stdout": (exc.stdout or "")[-12000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-12000:] if isinstance(exc.stderr, str) else "",
            "timeout_seconds": timeout,
        })
    record["elapsed_seconds"] = round(time.time() - started, 3)
    (directory / f"{name}.log.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return record


def skipped_stage(name: str, command: list[str], directory: Path, reason: str) -> dict:
    """Persist a skipped stage so a capped run still has a complete receipt."""
    record = {
        "name": name, "command": command, "status": "skipped", "return_code": None,
        "elapsed_seconds": 0.0, "reason": reason,
    }
    (directory / f"{name}.log.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return record


def write_fallback_report(path: Path, input_plan: Path, stages: list[dict]) -> None:
    """Leave a readable handoff even if the normal report cannot parse a plan."""
    failed = [str(stage["name"]) for stage in stages if stage.get("status") != "passed"]
    lines = [
        "# Piano Fingering Results", "",
        "> **Review-required result** · Not all stages completed. Current run records have been retained.", "",
        "## Deliverables", "",
        f"- **Input plan**: `{input_plan}`", "- **Stage logs**: in this report directory:  `*.log.json`", "",
        "## What happened", "",
        f"- Failed stages: {(', '.join(failed) if failed else 'delivery report parsing')}",
        "- The source score and existing results are preserved.", "",
        "## Next steps", "",
        "- Open the stage log, repair its page/measure/hand scopes, and rerun affected stages.", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_running_report(path: Path, input_plan: Path, source_score: Path | None) -> None:
    """Create a readable handoff before any bounded stage starts.

    A host may interrupt a long task independently of the coordinator's own
    timeout. In that case stage logs can exist while the final report has not
    yet been assembled. This small report is deliberately written at startup
    and later replaced by the normal delivery report.
    """
    lines = [
        "# Piano Fingering Results", "",
        "> **Processing** · Run directory created. If interrupted, retain this report, current plan, and stage logs, then resume unfinished stages.", "",
        "## Current artifacts", "",
        f"- **Input plan**: `{input_plan}`",
        f"- **Source score copy**: `{source_score}`" if source_score else "- **Source score copy**: no copyable source score is linked to this plan",
        "- **Stage logs**: in this directory:  `*.log.json` (updated as stages complete)", "",
        "## Resume after interruption", "",
        "- Check the latest stage log and current  `fingered-plan.json` / `placed-plan.json`.",
        "- Resume unfinished stages and preserve the source and current run directory.", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def preserve_source_score(plan_path: Path, directory: Path) -> Path | None:
    """Copy the immutable visual source into a run directory when available.

    A recognition gate is intentionally allowed to stop downstream fingering.
    It must not, however, leave the person with only logs or a JSON plan they
    cannot visually inspect.  This is a *source copy*, never an annotated
    substitute, and is therefore safe to create before recognition succeeds.
    """
    try:
        payload = json.loads(plan_path.read_text(encoding="utf-8"))
        source = payload.get("source", {})
        raw = str(source.get("path", "")).strip() if isinstance(source, dict) else ""
        candidate = Path(raw) if raw else None
        if candidate and not candidate.is_absolute():
            candidate = plan_path.parent / candidate
        # An OMR candidate's direct source is normally its generated MXL.
        # Its report retains the original upload path, which is the only file
        # useful to the person reviewing a stopped run.
        if not candidate or not candidate.is_file() or candidate.suffix.lower() not in {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            context = source.get("omr_candidate", {}) if isinstance(source, dict) else {}
            report_raw = str(context.get("report", "")).strip() if isinstance(context, dict) else ""
            report_path = Path(report_raw) if report_raw else None
            if report_path and report_path.is_file():
                try:
                    report = json.loads(report_path.read_text(encoding="utf-8"))
                    original = Path(str(report.get("input", "")).strip())
                    candidate = original if original.is_file() else None
                except (OSError, ValueError, TypeError, json.JSONDecodeError):
                    candidate = None
        if not candidate or not candidate.is_file() or candidate.suffix.lower() not in {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            return None
        target = directory / f"source-score{candidate.suffix.lower()}"
        shutil.copy2(candidate, target)
        return target
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None


def combine_rendered_audits(paths: list[Path], output: Path) -> None:
    """Combine one per-page PDF readback audit into report-compatible evidence."""
    reports = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    labels = sum(int(report.get("labels", 0)) for report in reports)
    recovered = sum(int(report.get("recovered_labels", 0)) for report in reports)
    unexpected = sum(int(report.get("unexpected_label_ink_pixels", 0)) for report in reports)
    failures: list[str] = []
    for report in reports:
        failures.extend(f"page {report.get('page', '?')}: {item}" for item in report.get("failures", []))
    output.write_text(json.dumps({
        "metric": "all-page rendered coloured-label recovery at planned anchors",
        "pages": len(reports), "labels": labels, "recovered_labels": recovered,
        "unexpected_label_ink_pixels": unexpected,
        "placement_accuracy": recovered / labels if labels else 0.0,
        "failures": failures,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def combine_page_count_audits(
    paths: list[Path], output: Path, *, numerator: str, denominator: str, metric: str,
) -> None:
    """Combine per-page source audits while preserving their real counts."""
    reports = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    total = sum(int(report.get(denominator, 0)) for report in reports)
    passed = sum(int(report.get(numerator, 0)) for report in reports)
    failures: list[str] = []
    for report in reports:
        failures.extend(f"page {report.get('page', '?')}: {item}" for item in report.get("failures", []))
    output.write_text(json.dumps({
        "metric": metric, "pages": len(reports), denominator: total, numerator: passed,
        "placement_accuracy": passed / total if total else 0.0, "failures": failures,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="current source plan (locked for generation; draft is reported for review)")
    parser.add_argument("--out-dir", type=Path, required=True, help="new directory for this one run")
    parser.add_argument("--max-auto-depth", type=int, default=4, choices=range(4, 8))
    parser.add_argument("--stage-timeout", type=int, default=180, help="per-stage ceiling in seconds")
    parser.add_argument("--run-timeout", type=int, default=480, help="whole-run ceiling in seconds, including reports")
    parser.add_argument("--visual-dpi", type=float,
                        help="DPI of visual plan pages; defaults to source.render_dpi or 144")
    parser.add_argument("--skip-stability", action="store_true", help="use only for a quick draft; report remains review-level")
    parser.add_argument(
        "--provisional-omr",
        action="store_true",
        help=(
            "for an attached local OMR candidate only: produce a review-required PDF using "
            "only transactionally anchored labels; normal verified delivery remains unchanged"
        ),
    )
    args = parser.parse_args()
    if args.stage_timeout < 10:
        parser.error("--stage-timeout must be at least 10 seconds")
    if args.run_timeout < 30:
        parser.error("--run-timeout must be at least 30 seconds")
    if args.visual_dpi is not None and not 36 <= args.visual_dpi <= 600:
        parser.error("--visual-dpi must be between 36 and 600")
    if not args.plan.is_file():
        parser.error(f"plan not found: {args.plan}")
    if args.out_dir.exists():
        parser.error(f"output directory already exists: {args.out_dir}")

    args.out_dir.mkdir(parents=True)
    current_plan = args.plan.resolve()
    try:
        initial_payload = json.loads(current_plan.read_text(encoding="utf-8"))
        initial_source_type = str(initial_payload.get("source", {}).get("type", "")).lower()
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        initial_source_type = ""
    if args.provisional_omr and initial_source_type != "omr_candidate":
        parser.error("--provisional-omr requires an attached source.type=omr_candidate plan")
    fingered = args.out_dir / "fingered-plan.json"
    provisional = args.out_dir / "provisional-placed-plan.json"
    quality = args.out_dir / "fingering-quality.json"
    stability = args.out_dir / "fingering-stability.json"
    fingering_review = args.out_dir / "fingering-review.json"
    hand_size_stability = args.out_dir / "hand-size-stability.json"
    phrase_risk = args.out_dir / "phrase-risk-audit.json"
    musicxml = args.out_dir / "fingered-score.musicxml"
    placed = args.out_dir / "placed-plan.json"
    placement = args.out_dir / "placement-audit.json"
    anchors = args.out_dir / "source-anchor-audit.json"
    clearance = args.out_dir / "source-clearance-audit.json"
    pdf = args.out_dir / "fingered-score.pdf"
    rendered_audit = args.out_dir / "rendered-placement-audit.json"
    report = args.out_dir / "result-report.md"
    stages: list[dict] = []
    run_started = time.monotonic()
    manifest = {
        "status": "running", "input_plan": str(current_plan), "out_dir": str(args.out_dir.resolve()),
        "stage_timeout_seconds": args.stage_timeout, "run_timeout_seconds": args.run_timeout,
        "max_auto_depth": args.max_auto_depth, "stages": stages,
    }
    write_json(args.out_dir / "run-manifest.json", manifest)

    # Preserve a viewable, immutable source at the start of every run.  This
    # also makes a bounded/blocked run inspectable without reopening the
    # original upload location.
    source_copy = preserve_source_score(current_plan, args.out_dir)
    manifest["current_plan"] = str(current_plan)
    manifest["artifacts"] = {
        "source_score": str(source_copy) if source_copy and source_copy.is_file() else None,
        "report": str(report),
    }
    manifest["next_action"] = "Pipeline is running; inspect result-report.md and the newest stage log if the host interrupts it."
    write_json(args.out_dir / "run-manifest.json", manifest)
    write_running_report(report, current_plan, source_copy)

    def limited_stage(name: str, command: list[str]) -> dict:
        remaining = args.run_timeout - (time.monotonic() - run_started)
        if remaining <= 0:
            return skipped_stage(name, command, args.out_dir, "whole-run timeout exhausted before this stage")
        return run_stage(name, command, args.out_dir, min(args.stage_timeout, max(1, math.ceil(remaining))))

    # Stop before the expensive solver when facts are draft, stale or
    # contradictory.  The delivery report below still gives the user the
    # current plan, exact gate failures and a local next action.
    stages.append(limited_stage(
        "recognition",
        [sys.executable, str(SCRIPT_DIR / "validate_recognition.py"), str(current_plan)],
    ))
    recognition_passed = stages[-1]["status"] == "passed"
    if recognition_passed or args.provisional_omr:
        generate_command = [
            sys.executable, str(SCRIPT_DIR / "generate_fingering_plan.py"), str(current_plan), "-o", str(fingered),
            "--max-auto-depth", str(args.max_auto_depth), "--quiet",
        ]
        if args.provisional_omr:
            generate_command.append("--provisional-omr")
        stages.append(limited_stage(
            "generate",
            generate_command,
        ))
    else:
        stages.append(skipped_stage(
            "generate",
            [sys.executable, str(SCRIPT_DIR / "generate_fingering_plan.py"), str(current_plan), "-o", str(fingered)],
            args.out_dir, "recognition gate did not pass",
        ))
    if fingered.is_file():
        current_plan = fingered

    if args.provisional_omr and fingered.is_file():
        stages.append(limited_stage(
            "restrict_provisional_anchors",
            [sys.executable, str(SCRIPT_DIR / "build_provisional_omr_output.py"), str(fingered), "-o", str(provisional)],
        ))
        if provisional.is_file():
            current_plan = provisional

    if stages[-1]["status"] == "passed" and not args.provisional_omr:
        stages.append(limited_stage(
            "validate_fingering",
            [sys.executable, str(SCRIPT_DIR / "validate_fingering_plan.py"), str(current_plan), "--require-complete"],
        ))
        stages.append(limited_stage(
            "quality",
            [sys.executable, str(SCRIPT_DIR / "evaluate_fingering_quality.py"), str(current_plan), "--minimum", "0.80", "-o", str(quality)],
        ))
        if not args.skip_stability:
            stages.append(limited_stage(
                "stability",
                [sys.executable, str(SCRIPT_DIR / "audit_fingering_stability.py"), str(current_plan), "--minimum", "0.90", "-o", str(stability)],
            ))
            # Preserve concrete alternative fingers and nearby context whenever
            # the two bounded searches disagree.  This is a small review task,
            # not a second automatic rewrite: the selected plan stays intact
            # until a model or person actually inspects the marked phrase.
            if stability.is_file():
                stages.append(limited_stage(
                    "build_fingering_review",
                    [sys.executable, str(SCRIPT_DIR / "build_fingering_review_manifest.py"),
                     str(current_plan), str(stability), "-o", str(fingering_review)],
                ))
            # Keep the selected fingering authoritative. This only identifies
            # scopes that depend on the default hand-size assumption, so the
            # delivery report can ask for a focused review instead of silently
            # presenting one calibration as universal.
            stages.append(limited_stage(
                "hand_size_stability",
                [sys.executable, str(SCRIPT_DIR / "audit_hand_size_stability.py"), str(args.plan), str(current_plan), "-o", str(hand_size_stability)],
            ))
        stages.append(limited_stage(
            "phrase_risk",
            [sys.executable, str(SCRIPT_DIR / "audit_phrase_risk.py"), str(current_plan), "-o", str(phrase_risk)],
        ))
    elif stages[-1]["status"] == "passed":
        # A provisional OMR preview is not allowed to become a formal result,
        # but it should still disclose solver uncertainty. The stability audit
        # now explicitly supports candidate plans, so users receive focused
        # alternate-search scopes instead of only a generic "needs review".
        # Rule compliance is also useful diagnostic evidence here. It cannot
        # certify the candidate's score facts, but it prevents a vague
        # “not checked” report when a concrete same-finger/chord violation is
        # already visible in the generated candidate plan.
        stages.append(limited_stage(
            "quality",
            [sys.executable, str(SCRIPT_DIR / "evaluate_fingering_quality.py"), str(current_plan), "--minimum", "0.80", "-o", str(quality)],
        ))
        if not args.skip_stability:
            stages.append(limited_stage(
                "stability",
                [sys.executable, str(SCRIPT_DIR / "audit_fingering_stability.py"), str(current_plan), "--minimum", "0.90", "-o", str(stability)],
            ))
            if stability.is_file():
                stages.append(limited_stage(
                    "build_fingering_review",
                    [sys.executable, str(SCRIPT_DIR / "build_fingering_review_manifest.py"),
                     str(current_plan), str(stability), "-o", str(fingering_review)],
                ))
        stages.append(limited_stage(
            "phrase_risk",
            [sys.executable, str(SCRIPT_DIR / "audit_phrase_risk.py"), str(current_plan), "-o", str(phrase_risk)],
        ))

    visual_source = False
    structured_source = False
    structured_input: Path | None = None
    visual_dpi = args.visual_dpi or 144.0
    if fingered.is_file():
        try:
            generated_payload = json.loads(current_plan.read_text(encoding="utf-8"))
            source = generated_payload.get("source", {})
            source_type = str(source.get("type", "")).lower() if isinstance(source, dict) else ""
            visual_source = source_type in {"pdf", "image"} or (
                args.provisional_omr and source_type == "omr_candidate"
            )
            raw_input = str(source.get("path", "")).strip() if isinstance(source, dict) else ""
            candidate_input = Path(raw_input) if raw_input else None
            if candidate_input and not candidate_input.is_absolute():
                candidate_input = current_plan.parent / candidate_input
            if source_type == "musicxml" and candidate_input and candidate_input.is_file():
                structured_source = True
                structured_input = candidate_input
            if args.visual_dpi is None:
                visual_dpi = float(source.get("render_dpi", 144.0)) if isinstance(source, dict) else 144.0
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            # The existing delivery report will expose malformed plans.  Do
            # not hide its fallback by attempting visual work with unknown
            # geometry.
            visual_source = False

    # A structured input must yield a directly usable annotated score, not
    # merely an internal JSON plan.  This export is independent of any later
    # confidence warning: if generation produced a valid plan, keep the
    # MusicXML for inspection and let the report describe remaining review.
    if fingered.is_file() and structured_source and structured_input:
        stages.append(limited_stage(
            "write_musicxml",
            [sys.executable, str(SCRIPT_DIR / "apply_fingerings.py"), str(structured_input), str(current_plan), "-o", str(musicxml)],
        ))
    if not 36 <= visual_dpi <= 600:
        visual_source = False

    # Visual scores used to stop at a fingered JSON even though the requested
    # deliverable was a readable PDF.  Keep the source page immutable, repair
    # labels only, and preserve whatever current plan exists if a repair fails.
    if fingered.is_file() and visual_source:
        stages.append(limited_stage(
            "repair_label_clearance",
            [sys.executable, str(SCRIPT_DIR / "repair_label_clearance.py"), str(current_plan), "-o", str(placed),
             "--dpi", str(visual_dpi),
             "--step", str(4 if args.provisional_omr else 6),
             "--max-horizontal-shift", str(9 if args.provisional_omr else 5),
             "--max-extra-offset", str(96 if args.provisional_omr else 120),
             "--report", str(args.out_dir / "clearance-repair.json")]
             + (["--allow-provisional-omr", "--hide-unresolved"] if args.provisional_omr else []),
        ))
        if placed.is_file():
            current_plan = placed
        if args.provisional_omr:
            stages.append(limited_stage(
                "layout_audit",
                [sys.executable, str(SCRIPT_DIR / "audit_annotation_layout.py"), str(current_plan),
                 "--allow-provisional-omr", "-o", str(placement)],
            ))
            try:
                candidate_payload = json.loads(current_plan.read_text(encoding="utf-8"))
                candidate_pages = sorted(int(page["page"]) for page in candidate_payload.get("pages", []))
            except (OSError, ValueError, TypeError, json.JSONDecodeError, KeyError):
                candidate_pages = []
            anchor_pages: list[Path] = []
            clearance_pages: list[Path] = []
            for page_number in candidate_pages:
                anchor_page = args.out_dir / f"source-anchor-page-{page_number:03d}.json"
                clearance_page = args.out_dir / f"source-clearance-page-{page_number:03d}.json"
                stages.append(limited_stage(
                    f"source_anchor_audit_page_{page_number}",
                    [sys.executable, str(SCRIPT_DIR / "audit_source_noteheads.py"), str(current_plan),
                     "--page", str(page_number), "--candidate-diagnostic", "-o", str(anchor_page)],
                ))
                stages.append(limited_stage(
                    f"source_clearance_audit_page_{page_number}",
                    [sys.executable, str(SCRIPT_DIR / "audit_source_clearance.py"), str(current_plan),
                     "--page", str(page_number), "--dpi", str(visual_dpi), "--candidate-diagnostic",
                     "-o", str(clearance_page)],
                ))
                if anchor_page.is_file():
                    anchor_pages.append(anchor_page)
                if clearance_page.is_file():
                    clearance_pages.append(clearance_page)
            if candidate_pages and len(anchor_pages) == len(candidate_pages):
                combine_page_count_audits(
                    anchor_pages, anchors, numerator="valid_anchors", denominator="anchors",
                    metric="all-page candidate-anchor source-ink diagnostic",
                )
            if candidate_pages and len(clearance_pages) == len(candidate_pages):
                combine_page_count_audits(
                    clearance_pages, clearance, numerator="clear_labels", denominator="labels",
                    metric="all-page candidate source-clearance diagnostic",
                )
        else:
            stages.append(limited_stage(
                "layout_audit",
                [sys.executable, str(SCRIPT_DIR / "audit_annotation_layout.py"), str(current_plan), "-o", str(placement)],
            ))
            stages.append(limited_stage(
                "source_anchor_audit",
                [sys.executable, str(SCRIPT_DIR / "audit_source_noteheads.py"), str(current_plan), "-o", str(anchors)],
            ))
            stages.append(limited_stage(
                "source_clearance_audit",
                [sys.executable, str(SCRIPT_DIR / "audit_source_clearance.py"), str(current_plan), "--dpi", str(visual_dpi), "-o", str(clearance)],
            ))
        stages.append(limited_stage(
            "render_pdf",
            [sys.executable, str(SCRIPT_DIR / "render_fingering_pdf.py"), str(current_plan), "-o", str(pdf), "--dpi", str(visual_dpi)],
        ))
        if pdf.is_file():
            stages.append(limited_stage(
                "verify_pdf",
                [sys.executable, str(SCRIPT_DIR / "verify_output.py"), str(current_plan), str(pdf)],
            ))
            # This is optional: do not install or download a renderer.  If
            # common local Poppler is already available, read every output
            # page back so final placement is evidence rather than intent.
            pdftoppm = shutil.which("pdftoppm")
            if pdftoppm:
                try:
                    rendered_plan = json.loads(current_plan.read_text(encoding="utf-8"))
                    page_numbers = sorted(int(page["page"]) for page in rendered_plan.get("pages", []))
                except (OSError, ValueError, TypeError, json.JSONDecodeError, KeyError):
                    page_numbers = []
                per_page_audits: list[Path] = []
                for page_number in page_numbers:
                    image_base = args.out_dir / f"rendered-page-{page_number:03d}"
                    rendered_png = image_base.with_suffix(".png")
                    stages.append(limited_stage(
                        f"render_output_page_{page_number}",
                        [pdftoppm, "-f", str(page_number), "-l", str(page_number), "-r", str(visual_dpi),
                         "-png", "-singlefile", str(pdf), str(image_base)],
                    ))
                    if rendered_png.is_file():
                        page_audit = args.out_dir / f"rendered-placement-page-{page_number:03d}.json"
                        stages.append(limited_stage(
                            f"rendered_output_audit_page_{page_number}",
                            [sys.executable, str(SCRIPT_DIR / "audit_rendered_labels.py"), str(current_plan),
                             str(rendered_png), "--page", str(page_number), "--source-dpi", str(visual_dpi),
                             "-o", str(page_audit)],
                        ))
                        if page_audit.is_file():
                            per_page_audits.append(page_audit)
                if page_numbers and len(per_page_audits) == len(page_numbers):
                    try:
                        combine_rendered_audits(per_page_audits, rendered_audit)
                    except (OSError, ValueError, TypeError, json.JSONDecodeError):
                        pass

    report_command = [
        sys.executable, str(SCRIPT_DIR / "create_delivery_report.py"), str(current_plan), "-o", str(report),
    ]
    if quality.is_file():
        report_command.extend(["--fingering-quality", str(quality)])
    if stability.is_file():
        report_command.extend(["--stability-audit", str(stability)])
    if phrase_risk.is_file():
        report_command.extend(["--phrase-risk-audit", str(phrase_risk)])
    if hand_size_stability.is_file():
        report_command.extend(["--hand-size-audit", str(hand_size_stability)])
    if fingering_review.is_file():
        report_command.extend(["--fingering-review", str(fingering_review)])
    if pdf.is_file():
        report_command.extend(["--pdf", str(pdf)])
    if musicxml.is_file():
        report_command.extend(["--musicxml", str(musicxml)])
    if source_copy and source_copy.is_file():
        report_command.extend(["--source-score", str(source_copy)])
    if placement.is_file():
        report_command.extend(["--placement-audit", str(placement)])
    if anchors.is_file():
        report_command.extend(["--source-anchor-audit", str(anchors)])
    if clearance.is_file():
        report_command.extend(["--source-clearance-audit", str(clearance)])
    if rendered_audit.is_file():
        report_command.extend(["--rendered-placement-audit", str(rendered_audit)])
    stages.append(limited_stage("delivery_report", report_command))
    if not report.is_file():
        write_fallback_report(report, current_plan, stages)

    failed = [stage["name"] for stage in stages if stage["status"] != "passed"]
    # A visual plan without the final raster readback has produced useful
    # artifacts, but it is not a fully verified delivery.  Mirror the report
    # level in the machine-readable manifest so callers do not mistake a
    # successful subprocess sequence for a finished user result.
    report_complete = False
    if report.is_file():
        try:
            report_complete = "> **Ready to use**" in report.read_text(encoding="utf-8")
        except OSError:
            report_complete = False
    manifest["status"] = "complete" if not failed and report_complete else "review_required"
    manifest["current_plan"] = str(current_plan)
    manifest["artifacts"] = {
        "fingering_plan": str(fingered) if fingered.is_file() else None,
        "placed_plan": str(placed) if placed.is_file() else None,
        "pdf": str(pdf) if pdf.is_file() else None,
        "musicxml": str(musicxml) if musicxml.is_file() else None,
        "source_score": str(source_copy) if source_copy and source_copy.is_file() else None,
        "placement": str(placement) if placement.is_file() else None,
        "source_anchor": str(anchors) if anchors.is_file() else None,
        "source_clearance": str(clearance) if clearance.is_file() else None,
        "rendered_placement": str(rendered_audit) if rendered_audit.is_file() else None,
        "quality": str(quality) if quality.is_file() else None,
        "stability": str(stability) if stability.is_file() else None,
        "fingering_review": str(fingering_review) if fingering_review.is_file() else None,
        "hand_size_stability": str(hand_size_stability) if hand_size_stability.is_file() else None,
        "phrase_risk": str(phrase_risk) if phrase_risk.is_file() else None,
        "report": str(report) if report.is_file() else None,
    }
    manifest["failed_stages"] = failed
    manifest["elapsed_seconds"] = round(time.monotonic() - run_started, 3)
    manifest["next_action"] = (
        "Open result-report.md and the failed stage log; retain the current plan and repair only the reported scope."
        if failed else (
            "PDF and source-page audits are ready; render the output PDF to PNG and run audit_rendered_labels.py before claiming final visual placement."
            if visual_source else "Proceed to the source-page annotation and four visual audits when this is a PDF/image score."
        )
    )
    write_json(args.out_dir / "run-manifest.json", manifest)
    print(f"Pipeline {manifest['status']}: {args.out_dir}")
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
