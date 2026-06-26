from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


REQUIRED_RELATIVE_PATHS = [
    Path("reports"),
    Path("reports/per_paper"),
    Path("reports/stage_delivery_handoff.md"),
    Path("reports/project_directory_index.md"),
    Path("metadata/query_spec.json"),
    Path("metadata/paper_batch_manifest.json"),
    Path("metadata/delivery_bundle_manifest.json"),
    Path("metadata/routing_status.json"),
    Path("metadata/project_directory_annotations.json"),
    Path("metadata/project_directory_index.json"),
]

REQUIRED_SOURCE_RECORD_FIELDS = [
    "canonical_paper_page_url",
    "conference_paper_url",
    "conference_pdf_url",
    "openreview_forum_url",
    "openreview_pdf_url",
    "arxiv_abs_url",
    "arxiv_pdf_url",
    "arxiv_latex_url",
    "preferred_source_type",
    "preferred_local_source_path",
    "local_latex_dir",
    "local_pdf_path",
    "local_openreview_pdf_path",
    "local_official_pdf_path",
    "local_arxiv_pdf_path",
    "review_bundle_dir",
    "review_digest_path",
    "canonical_review_source_type",
    "retrieval_sources",
    "verification_state",
    "verification_checks",
    "source_acquisition_status",
    "source_stage",
    "artifact_status",
    "review_bundle_completeness",
]

REQUIRED_UPSTREAM_BUNDLE_CONTEXT_FIELDS = [
    "routing_status_json",
    "project_directory_index_json",
    "project_directory_index_md",
    "paper_batch_manifest_json",
    "openreview_rebuttal_digest_json",
    "stage_delivery_handoff_md",
    "delivery_bundle_manifest_json",
]


def load_required_headings() -> list[str]:
    path = Path(__file__).resolve().parents[1] / "schemas" / "detailed_report_required_sections.json"
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return [
        str(section.get("heading", "")).strip()
        for section in payload.get("required_sections", [])
        if str(section.get("heading", "")).strip()
    ]


def resolve_relative_path(root: Path, raw: str) -> Path | None:
    raw = str(raw).strip()
    if not raw or raw.lower() == "string" or raw.startswith("[fill"):
        return None
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return root / candidate


def validate_report_structure(report_path: Path, required_headings: list[str], label: str) -> list[str]:
    errors: list[str] = []
    if not report_path.exists():
        return [f"{label}: missing authoritative report -> {report_path.as_posix()}"]

    text = report_path.read_text(encoding="utf-8-sig")
    for heading in required_headings:
        if heading not in text:
            errors.append(f"{label}: authoritative report is missing required section heading -> {heading}")
    if "[fill" in text:
        errors.append(f"{label}: authoritative report still contains '[fill' placeholders")
    dangling_prompt_bullets = [
        line_no
        for line_no, line in enumerate(text.splitlines(), start=1)
        if line.lstrip().startswith("- ")
        and line.rstrip().endswith((":", "?"))
        and len(line.strip()) <= 120
    ]
    if dangling_prompt_bullets:
        preview = ", ".join(str(n) for n in dangling_prompt_bullets[:12])
        errors.append(f"{label}: authoritative report still contains unfinished prompt bullets at lines {preview}")
    empty_bullets = [
        line_no
        for line_no, line in enumerate(text.splitlines(), start=1)
        if line.strip() in {"-", "*", "- ", "* "}
    ]
    if empty_bullets:
        preview = ", ".join(str(n) for n in empty_bullets[:12])
        errors.append(f"{label}: authoritative report still contains empty bullet placeholders at lines {preview}")
    non_whitespace_chars = len("".join(text.split()))
    if non_whitespace_chars < 5000:
        errors.append(
            f"{label}: authoritative report is too short for a top-conference deepread ({non_whitespace_chars} non-whitespace chars)"
        )
    return errors


def review_context_files_exist(workspace_dir: Path) -> bool:
    review_root = workspace_dir / "inputs" / "review_context"
    return review_root.exists() and any(path.is_file() for path in review_root.rglob("*"))


def validate_focus_spec(workspace_dir: Path, focus_spec_path: Path, label: str) -> list[str]:
    errors: list[str] = []
    if not focus_spec_path.exists():
        return [f"{label}: missing focus_spec_json -> {focus_spec_path.as_posix()}"]

    try:
        payload = json.loads(focus_spec_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"{label}: invalid JSON in focus_spec_json -> {exc}"]

    source_record = payload.get("source_record")
    if not isinstance(source_record, dict):
        errors.append(f"{label}: focus spec is missing source_record")
    else:
        missing = [field for field in REQUIRED_SOURCE_RECORD_FIELDS if field not in source_record]
        if missing:
            errors.append(f"{label}: focus spec source_record is missing fields -> {', '.join(missing)}")
        for field in [
            "preferred_local_source_path",
            "local_latex_dir",
            "local_pdf_path",
            "local_openreview_pdf_path",
            "local_official_pdf_path",
            "local_arxiv_pdf_path",
            "review_bundle_dir",
            "review_digest_path",
        ]:
            resolved = resolve_relative_path(workspace_dir, source_record.get(field, ""))
            if resolved and not resolved.exists():
                errors.append(f"{label}: missing source artifact referenced by source_record.{field} -> {source_record.get(field, '')}")

        venue = str(payload.get("venue", "")).strip().casefold()
        if "iclr" in venue and not review_context_files_exist(workspace_dir):
            review_bundle_dir = resolve_relative_path(workspace_dir, source_record.get("review_bundle_dir", ""))
            if not review_bundle_dir or not review_bundle_dir.exists():
                errors.append(
                    f"{label}: ICLR paper requires a downloaded local OpenReview review/rebuttal bundle"
                )

    upstream_bundle_context = payload.get("upstream_bundle_context")
    if not isinstance(upstream_bundle_context, dict):
        errors.append(f"{label}: focus spec is missing upstream_bundle_context")
    else:
        missing = [field for field in REQUIRED_UPSTREAM_BUNDLE_CONTEXT_FIELDS if field not in upstream_bundle_context]
        if missing:
            errors.append(f"{label}: focus spec upstream_bundle_context is missing fields -> {', '.join(missing)}")

    return errors


def validate_manifest_entries(workspace_dir: Path) -> list[str]:
    errors: list[str] = []
    required_headings = load_required_headings()
    path = workspace_dir / "metadata" / "paper_batch_manifest.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"invalid JSON in metadata/paper_batch_manifest.json: {exc}"]

    papers = list(payload.get("papers", []))
    if not papers:
        return ["metadata/paper_batch_manifest.json: missing papers"]

    for idx, item in enumerate(papers, start=1):
        label = str(item.get("paper_title", "")).strip() or f"paper-{idx}"
        report_md = resolve_relative_path(workspace_dir, item.get("authoritative_report_md", ""))
        report_pdf = resolve_relative_path(workspace_dir, item.get("authoritative_report_pdf", ""))
        focus_spec = resolve_relative_path(workspace_dir, item.get("focus_spec_json", ""))
        intermediate = resolve_relative_path(workspace_dir, item.get("intermediate_json", ""))

        if not report_md:
            errors.append(f"{label}: missing authoritative_report_md")
        elif not report_md.exists():
            errors.append(f"{label}: missing authoritative_report_md -> {item.get('authoritative_report_md', '')}")
        else:
            errors.extend(validate_report_structure(report_md, required_headings, label))

        if not report_pdf:
            errors.append(f"{label}: missing authoritative_report_pdf")
        elif not report_pdf.exists():
            errors.append(f"{label}: missing authoritative_report_pdf -> {item.get('authoritative_report_pdf', '')}")

        if not focus_spec:
            errors.append(f"{label}: missing focus_spec_json")
        else:
            errors.extend(validate_focus_spec(workspace_dir, focus_spec, label))

        if not intermediate:
            errors.append(f"{label}: missing intermediate_json")
        elif not intermediate.exists():
            errors.append(f"{label}: missing intermediate_json -> {item.get('intermediate_json', '')}")

    return errors


def validate_delivery_manifest(workspace_dir: Path) -> list[str]:
    path = workspace_dir / "metadata" / "delivery_bundle_manifest.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"invalid JSON in metadata/delivery_bundle_manifest.json: {exc}"]

    errors: list[str] = []
    for field in [
        "stage_name",
        "workspace_root",
        "resume_from_bundle_only_supported",
        "status_artifacts",
        "directory_description_artifacts",
        "authoritative_handoff_artifacts",
    ]:
        if field not in payload:
            errors.append(f"metadata/delivery_bundle_manifest.json: missing field -> {field}")
    for rel in payload.get("status_artifacts", []):
        resolved = resolve_relative_path(workspace_dir, rel)
        if not resolved or not resolved.exists():
            errors.append(f"metadata/delivery_bundle_manifest.json: missing status artifact -> {rel}")
    for rel in payload.get("directory_description_artifacts", []):
        resolved = resolve_relative_path(workspace_dir, rel)
        if not resolved or not resolved.exists():
            errors.append(f"metadata/delivery_bundle_manifest.json: missing directory description artifact -> {rel}")
    for rel in payload.get("authoritative_handoff_artifacts", []):
        resolved = resolve_relative_path(workspace_dir, rel)
        if not resolved or not resolved.exists():
            errors.append(f"metadata/delivery_bundle_manifest.json: missing authoritative artifact -> {rel}")
    return errors


def validate_routing_status(workspace_dir: Path) -> list[str]:
    path = workspace_dir / "metadata" / "routing_status.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"invalid JSON in metadata/routing_status.json: {exc}"]

    errors: list[str] = []
    for field in [
        "current_stage",
        "recommended_next_skill",
        "resume_from_bundle_only_supported",
        "status_artifacts",
        "directory_description_artifacts",
        "authoritative_handoff_artifacts",
        "key_artifacts",
    ]:
        if field not in payload:
            errors.append(f"metadata/routing_status.json: missing field -> {field}")
    for rel in payload.get("status_artifacts", []):
        resolved = resolve_relative_path(workspace_dir, rel)
        if not resolved or not resolved.exists():
            errors.append(f"metadata/routing_status.json: missing status artifact -> {rel}")
    for rel in payload.get("directory_description_artifacts", []):
        resolved = resolve_relative_path(workspace_dir, rel)
        if not resolved or not resolved.exists():
            errors.append(f"metadata/routing_status.json: missing directory description artifact -> {rel}")
    return errors


def validate_workspace_dir(workspace_dir: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_RELATIVE_PATHS:
        if not (workspace_dir / rel).exists():
            errors.append(f"missing required path: {rel.as_posix()}")
    errors.extend(validate_routing_status(workspace_dir))
    errors.extend(validate_delivery_manifest(workspace_dir))
    errors.extend(validate_manifest_entries(workspace_dir))
    return errors


def build_zip(workspace_dir: Path, output_zip: Path) -> dict[str, object]:
    errors = validate_workspace_dir(workspace_dir)
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(workspace_dir.rglob("*")):
            if path.is_dir():
                continue
            zf.write(path, arcname=path.relative_to(workspace_dir).as_posix())
    return {
        "workspace_dir": str(workspace_dir.resolve()),
        "output_zip": str(output_zip.resolve()),
        "validation_errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_dir", type=Path)
    parser.add_argument("output_zip", type=Path)
    args = parser.parse_args()
    print(json.dumps(build_zip(args.workspace_dir, args.output_zip), ensure_ascii=False))


if __name__ == "__main__":
    main()
