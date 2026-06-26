from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_required_headings() -> list[str]:
    path = Path(__file__).resolve().parents[1] / "schemas" / "detailed_report_required_sections.json"
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return [
        str(section.get("heading", "")).strip()
        for section in payload.get("required_sections", [])
        if str(section.get("heading", "")).strip()
    ]


def is_iclr_report(text: str) -> bool:
    return "ICLR" in text or "iclr" in text


def review_context_files_exist(workspace_dir: Path) -> bool:
    review_root = workspace_dir / "inputs" / "review_context"
    if not review_root.exists():
        return False
    return any(path.is_file() for path in review_root.rglob("*"))


def load_manifest_entries(workspace_dir: Path) -> list[dict]:
    manifest_path = workspace_dir / "metadata" / "paper_batch_manifest.json"
    if not manifest_path.exists():
        return []
    payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    return list(payload.get("papers", []))


def discover_reports(workspace_dir: Path) -> list[Path]:
    manifest_path = workspace_dir / "metadata" / "paper_batch_manifest.json"
    reports: list[Path] = []
    if manifest_path.exists():
        payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        for item in payload.get("papers", []):
            report_md = str(item.get("authoritative_report_md", "")).strip()
            if report_md:
                reports.append(Path(report_md))

    if reports:
        return reports

    reports.extend(sorted((workspace_dir / "reports" / "per_paper").glob("*/*_detailed_cn.md")))
    reports.extend(sorted((workspace_dir / "reports").glob("*_detailed_cn.md")))
    return reports


def validate_report(report_path: Path, required_headings: list[str]) -> list[str]:
    errors: list[str] = []
    if not report_path.exists():
        return [f"missing report: {report_path.as_posix()}"]

    text = report_path.read_text(encoding="utf-8-sig")
    for heading in required_headings:
        if heading not in text:
            errors.append(f"{report_path.as_posix()}: missing required section heading -> {heading}")

    if "[fill" in text:
        errors.append(f"{report_path.as_posix()}: contains scaffold placeholder '[fill'")

    dangling_prompt_bullets = [
        line_no
        for line_no, line in enumerate(text.splitlines(), start=1)
        if line.lstrip().startswith("- ")
        and line.rstrip().endswith((":", "：", "?", "？"))
        and len(line.strip()) <= 120
    ]
    if dangling_prompt_bullets:
        preview = ", ".join(str(n) for n in dangling_prompt_bullets[:12])
        errors.append(f"{report_path.as_posix()}: contains unfinished prompt bullets at lines {preview}")

    empty_bullets = [
        line_no
        for line_no, line in enumerate(text.splitlines(), start=1)
        if line.strip() in {"-", "*", "- ", "* "}
    ]
    if empty_bullets:
        preview = ", ".join(str(n) for n in empty_bullets[:12])
        errors.append(f"{report_path.as_posix()}: contains empty bullet placeholders at lines {preview}")

    non_whitespace_chars = len("".join(text.split()))
    if non_whitespace_chars < 5000:
        errors.append(
            f"{report_path.as_posix()}: report is too short for a top-conference deepread ({non_whitespace_chars} non-whitespace chars)"
        )

    return errors


def validate_report_with_workspace(workspace_dir: Path, report_path: Path, required_headings: list[str]) -> list[str]:
    errors = validate_report(report_path, required_headings)
    if not report_path.exists():
        return errors

    text = report_path.read_text(encoding="utf-8-sig")
    if is_iclr_report(text) and not review_context_files_exist(workspace_dir):
        errors.append(
            f"{report_path.as_posix()}: ICLR paper requires downloaded OpenReview review/rebuttal files under inputs/review_context/"
        )

    return errors


def validate_manifest_coverage(workspace_dir: Path) -> list[str]:
    errors: list[str] = []
    entries = load_manifest_entries(workspace_dir)
    if not entries:
        return errors

    for idx, item in enumerate(entries, start=1):
        label = str(item.get("paper_title", "")).strip() or f"paper-{idx}"
        report_md = str(item.get("authoritative_report_md", "")).strip()
        if not report_md:
            errors.append(
                f"{label}: missing authoritative_report_md in metadata/paper_batch_manifest.json; every batch paper must have one authoritative detailed report"
            )
            continue
        report_path = Path(report_md)
        resolved = report_path if report_path.is_absolute() else workspace_dir / report_path
        if not resolved.exists():
            errors.append(
                f"{label}: authoritative detailed report is missing -> {report_md}; selective reading is not allowed for handoff"
            )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_dir", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    required_headings = load_required_headings()
    manifest_errors = validate_manifest_coverage(args.workspace_dir)
    reports = [args.report] if args.report else discover_reports(args.workspace_dir)
    if not reports:
        payload = {
            "workspace_dir": str(args.workspace_dir.resolve()),
            "validated_reports": [],
            "validation_errors": manifest_errors + ["no authoritative detailed reports found"],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)

    errors: list[str] = list(manifest_errors)
    for report in reports:
        report_path = report if report.is_absolute() else args.workspace_dir / report
        errors.extend(validate_report_with_workspace(args.workspace_dir, report_path, required_headings))

    payload = {
        "workspace_dir": str(args.workspace_dir.resolve()),
        "validated_reports": [str((r if r.is_absolute() else args.workspace_dir / r).resolve()) for r in reports],
        "validation_errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
