#!/usr/bin/env python3
"""Shared helpers for the One Person Company OS workspace scripts."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Iterable
from copy import deepcopy
from datetime import datetime
from html import escape as html_escape
from pathlib import Path
from typing import Any, Optional, TextIO
from xml.sax.saxutils import escape

import fcntl

from localization import (
    bool_audit_label as localized_bool_audit_label,
    bool_label as localized_bool_label,
    format_list as localized_format_list,
    joined_text as localized_joined_text,
    localized_role_spec,
    mode_label,
    normalize_language,
    normalize_persistence_mode,
    normalize_round_status,
    normalize_stage as localized_normalize_stage,
    persistence_mode_label,
    pick_text,
    round_status_label,
    stage_label as localized_stage_label,
    stage_meta,
    stage_required_outputs,
    step_meta,
    resolve_step_id,
    template_text,
)
from state_v3 import read_state_any_version, sync_legacy_fields, write_state_v3
from workspace_layout import (
    CORE_WORKSPACE_FILE_KEYS,
    ROOT_DOC_KEYS,
    artifact_category_path,
    candidate_container_paths,
    candidate_user_file_paths,
    existing_state_path,
    legacy_container_path,
    legacy_user_file_path,
    legacy_state_paths,
    record_dir_path,
    role_brief_path,
    reading_root_path,
    reading_start_path,
    state_path as layout_state_path,
    user_container_path,
    user_file_path,
)


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = ROOT / "scripts"
TEMPLATE_DIR = ROOT / "assets" / "templates"
ROLE_DIR = ROOT / "agents" / "roles"
ORCHESTRATION_DIR = ROOT / "orchestration"
REQUIRED_SCRIPT_NAMES = (
    "init_company.py",
    "init_business.py",
    "build_agent_brief.py",
    "generate_artifact_document.py",
    "start_round.py",
    "update_round.py",
    "calibrate_round.py",
    "transition_stage.py",
    "update_focus.py",
    "advance_offer.py",
    "advance_pipeline.py",
    "advance_product.py",
    "advance_delivery.py",
    "update_cash.py",
    "record_asset.py",
    "calibrate_business.py",
    "migrate_workspace.py",
    "validate_system.py",
    "preflight_check.py",
    "ensure_python_runtime.py",
    "checkpoint_save.py",
    "validate_release.py",
)
MIN_SUPPORTED_PYTHON = (3, 7)
STATE_BASE_KEY = "__opcos_base_state"
READING_EXTRA_FILE_KEYS = ("delivery_directory",)
PYTHON_CANDIDATE_COMMANDS = (
    "python3.13",
    "python3.12",
    "python3.11",
    "python3.10",
    "python3.9",
    "python3.8",
    "python3.7",
    "python3",
    "python",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def safe_workspace_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", value).strip()
    return cleaned or "未命名公司"


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w]+", "-", value.strip().lower(), flags=re.UNICODE).strip("-_")
    return slug or "record"


def safe_document_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", value).strip()
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "未命名文档"


def numbered_name(index: int, title: str, suffix: str) -> str:
    return f"{index:02d}-{safe_document_name(title)}{suffix}"


def planned_docx_name(index: int, title: str, status: str) -> str:
    _ = status
    return f"{index:02d}-{safe_document_name(title)}.docx"


def parse_planned_docx_name(filename: str) -> Optional[dict[str, Any]]:
    match = re.match(r"^(?P<index>\d{2})-(?:\[(?P<status>待生成|已生成)\])?(?P<title>.+)\.docx$", filename)
    if not match:
        return None
    marker = match.group("status")
    return {
        "index": int(match.group("index")),
        "status": "done" if marker in (None, "已生成") else "pending",
        "legacy_status": marker,
        "title": match.group("title"),
    }


def ensure_planned_docx_path(directory: Path, index: int, title: str, *, completed: bool) -> Path:
    desired = directory / planned_docx_name(index, title, "done" if completed else "pending")
    safe_title = safe_document_name(title)
    existing_matches = []
    if directory.is_dir():
        for path in directory.iterdir():
            parsed = parse_planned_docx_name(path.name)
            if parsed and parsed["index"] == index and parsed["title"] == safe_title:
                existing_matches.append(path)

    for path in existing_matches:
        if path == desired:
            return desired
    if existing_matches:
        source = existing_matches[0]
        if desired.exists():
            source.unlink()
        else:
            source.rename(desired)
    return desired


def planned_docx_path(directory: Path, title: str, *, completed: bool) -> Path:
    safe_title = safe_document_name(title)
    existing_index: Optional[int] = None
    if directory.is_dir():
        for path in directory.iterdir():
            parsed = parse_planned_docx_name(path.name)
            if parsed and parsed["title"] == safe_title:
                existing_index = parsed["index"]
                break
    index = existing_index or next_numbered_index(directory)
    return ensure_planned_docx_path(directory, index, title, completed=completed)


def next_numbered_index(directory: Path) -> int:
    max_index = 0
    if directory.is_dir():
        for path in directory.iterdir():
            match = re.match(r"^(\d{2})-", path.name)
            if match:
                max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def normalize_stage(value: str) -> str:
    return localized_normalize_stage(value)


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def round_id_now() -> str:
    return datetime.now().strftime("R%Y%m%d%H%M")


def format_list(items: list[str], language: str = "zh-CN") -> str:
    return localized_format_list(items, language)


def bool_label(value: bool, language: str = "zh-CN") -> str:
    return localized_bool_label(value, language)


def bool_audit_label(value: bool, language: str = "zh-CN") -> str:
    return localized_bool_audit_label(value, language)


def joined_text(values: Iterable[str], language: str = "zh-CN") -> str:
    return localized_joined_text(values, language)


def display_path(path: Path, root: Optional[Path] = None) -> str:
    if root is not None:
        try:
            return str(path.relative_to(root))
        except ValueError:
            pass
    return str(path)


def ensure_within_directory(path: Path, directory: Path, *, label: str = "path") -> Path:
    resolved_directory = directory.expanduser().resolve()
    resolved_path = path.expanduser().resolve()
    try:
        resolved_path.relative_to(resolved_directory)
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside {resolved_directory}: {resolved_path}") from exc
    return resolved_path


def version_text(version: tuple[int, ...]) -> str:
    return ".".join(str(part) for part in version)


def python_compatibility_label(version: tuple[int, ...]) -> str:
    return f"Python {version_text(version)}"


def is_python_version_supported(version: tuple[int, ...]) -> bool:
    return version >= MIN_SUPPORTED_PYTHON


def probe_python(executable: str) -> Optional[dict[str, Any]]:
    command = [executable, "-c", "import json, sys; print(json.dumps({'executable': sys.executable, 'version': list(sys.version_info[:3])}, ensure_ascii=False))"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError, OSError):
        return None
    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        return None

    version = tuple(int(part) for part in payload.get("version", [])[:3])
    executable_path = str(payload.get("executable", executable))
    if len(version) < 3 or not executable_path:
        return None

    return {
        "executable": executable_path,
        "version": version,
        "supported": is_python_version_supported(version),
    }


def discover_python_runtimes() -> list[dict[str, Any]]:
    candidates = [sys.executable]
    candidates.extend(PYTHON_CANDIDATE_COMMANDS)

    runtimes: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        resolved = candidate
        if not os.path.isabs(candidate):
            located = shutil.which(candidate)
            if not located:
                continue
            resolved = located

        probe = probe_python(resolved)
        if not probe:
            continue

        executable = probe["executable"]
        if executable in seen:
            continue
        seen.add(executable)
        runtimes.append(probe)
    return runtimes


def choose_compatible_runtime(runtimes: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    current = os.path.realpath(sys.executable)
    compatible = [
        runtime
        for runtime in runtimes
        if runtime["supported"] and os.path.realpath(runtime["executable"]) != current
    ]
    if not compatible:
        return None
    compatible.sort(key=lambda runtime: runtime["version"], reverse=True)
    return compatible[0]


def build_agent_action(
    *,
    current_supported: bool,
    compatible_runtime: Optional[dict[str, Any]],
    writable: bool,
    language: str = "zh-CN",
) -> str:
    if current_supported:
        return pick_text(
            language,
            "优先在 OpenClaw 中继续执行当前脚本；若脚本失败，再由智能体切到手动落盘模式。",
            "Prefer continuing with the current script in OpenClaw; if the script fails, have the agent fall back to manual persistence.",
        )

    minimum = version_text(MIN_SUPPORTED_PYTHON)
    if compatible_runtime:
        return pick_text(
            language,
            "优先让 OpenClaw 智能体运行 `scripts/ensure_python_runtime.py --run-script <目标脚本>`，改用兼容解释器 "
            f"{compatible_runtime['executable']} ({python_compatibility_label(compatible_runtime['version'])}) 重跑脚本；"
            "若切换失败，再由智能体在已确认工作区里手动完成脚本任务。",
            "Prefer asking the OpenClaw agent to run `scripts/ensure_python_runtime.py --run-script <target-script>` "
            f"and retry with the compatible interpreter {compatible_runtime['executable']} "
            f"({python_compatibility_label(compatible_runtime['version'])}); if switching fails, let the agent finish the task manually inside the approved workspace.",
        )

    if writable:
        return pick_text(
            language,
            f"先查看 `scripts/ensure_python_runtime.py` 给出的兼容解释器与手动安装方案（目标 {minimum}+）；"
            "marketplace 版不会自动安装系统依赖。若当前环境不便手动安装，则由智能体只在已确认工作区里手动落盘。",
            f"Inspect the compatible-runtime and manual install guidance from `scripts/ensure_python_runtime.py` first (target {minimum}+); "
            "the marketplace build will not auto-install system packages. If manual installation is not practical, let the agent persist files manually inside the approved workspace.",
        )

    return pick_text(
        language,
        f"先查看 `scripts/ensure_python_runtime.py` 的兼容解释器与手动安装方案（目标 {minimum}+）；"
        "如果仍无法写文件，只能继续纯对话推进，并明确当前没有任何内容被保存。",
        f"Review the compatible-runtime and manual install guidance from `scripts/ensure_python_runtime.py` first (target {minimum}+); "
        "if files still cannot be written, continue in chat only and state clearly that nothing was persisted.",
    )


def render_template(template_name: str, values: dict[str, str]) -> str:
    language = values.get("LANGUAGE", "zh-CN")
    template = template_text(template_name, TEMPLATE_DIR, language)
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def docx_content_types_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""


def docx_root_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


def docx_document_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


def docx_styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:sz w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="34"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
</w:styles>
"""


def docx_app_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>One Person Company OS</Application>
</Properties>
"""


def docx_core_xml(title: str) -> str:
    created = iso_now()
    escaped = escape(title)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{escaped}</dc:title>
  <dc:creator>One Person Company OS</dc:creator>
  <cp:lastModifiedBy>One Person Company OS</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>
</cp:coreProperties>
"""


def docx_paragraph_xml(text: str, style: Optional[str] = None) -> str:
    escaped_text = escape(text)
    paragraph_style = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    return (
        "<w:p>"
        f"{paragraph_style}"
        "<w:r><w:t xml:space=\"preserve\">"
        f"{escaped_text}"
        "</w:t></w:r>"
        "</w:p>"
    )


def markdown_to_docx_xml(markdown_text: str) -> str:
    paragraphs: list[str] = []
    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            paragraphs.append("<w:p/>")
            continue
        style = None
        text = line
        if line.startswith("# "):
            style = "Heading1"
            text = line[2:]
        elif line.startswith("## "):
            style = "Heading2"
            text = line[3:]
        elif line.startswith("### "):
            style = "Heading3"
            text = line[4:]
        elif line.startswith("- "):
            text = f"• {line[2:]}"
        paragraphs.append(docx_paragraph_xml(text, style))

    body = "".join(paragraphs) or "<w:p/>"
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
        "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
        "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
        "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
        "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
        "xmlns:wne=\"http://schemas.microsoft.com/office/2006/wordml\" "
        "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
        "mc:Ignorable=\"w14 wp14\">"
        f"<w:body>{body}"
        "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
        "</w:body></w:document>"
    )


def write_docx(path: Path, markdown_text: str, *, title: Optional[str] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc_title = title or path.stem
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", docx_content_types_xml())
        archive.writestr("_rels/.rels", docx_root_rels_xml())
        archive.writestr("docProps/app.xml", docx_app_xml())
        archive.writestr("docProps/core.xml", docx_core_xml(doc_title))
        archive.writestr("word/_rels/document.xml.rels", docx_document_rels_xml())
        archive.writestr("word/styles.xml", docx_styles_xml())
        archive.writestr("word/document.xml", markdown_to_docx_xml(markdown_text))


def read_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml").decode("utf-8")


def artifact_maturity_label(path: Path, language: str = "zh-CN") -> str:
    parsed = parse_planned_docx_name(path.name)
    legacy_status = parsed.get("legacy_status") if parsed else None
    if legacy_status == "已生成":
        return pick_text(language, "交付就绪版", "Delivery-Ready")
    if legacy_status == "待生成":
        return pick_text(language, "起始版", "Starter Formal Doc")

    try:
        text = read_docx_text(path)
    except (KeyError, OSError, zipfile.BadZipFile):
        return pick_text(language, "已建档", "Filed")

    if "交付就绪版" in text or "Delivery-Ready" in text:
        return pick_text(language, "交付就绪版", "Delivery-Ready")
    if "起始版" in text or "Starter Formal Doc" in text:
        return pick_text(language, "起始版", "Starter Formal Doc")
    return pick_text(language, "已建档", "Filed")


def load_role_specs() -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for path in sorted(ROLE_DIR.glob("*.json")):
        spec = load_json(path)
        specs[spec["role_id"]] = spec
    return specs


def load_stage_defaults() -> dict[str, Any]:
    return load_json(ORCHESTRATION_DIR / "stage-defaults.json")


def default_role_ids_for_stage(stage_id: str) -> list[str]:
    return list(load_stage_defaults()["stage_defaults"][stage_id])


def stage_label(stage_id: str, language: str = "zh-CN") -> str:
    return localized_stage_label(stage_id, language)


def state_path(company_dir: Path) -> Path:
    return layout_state_path(company_dir)


def root_doc_path(company_dir: Path, doc_key: str, language: str) -> Path:
    return user_file_path(company_dir, doc_key, language)


def workspace_file_path(company_dir: Path, file_key: str, language: str) -> Path:
    return user_file_path(company_dir, file_key, language)


def workspace_dir_path(company_dir: Path, dir_key: str, language: str) -> Path:
    return user_container_path(company_dir, dir_key, language)


def artifact_dir_path(company_dir: Path, category: str, language: str) -> Path:
    return artifact_category_path(company_dir, category, language)


def reading_dir_path(company_dir: Path, language: str) -> Path:
    return reading_root_path(company_dir, language)


def reading_entry_path(company_dir: Path, language: str) -> Path:
    return reading_start_path(company_dir, language)


def reading_export_path(company_dir: Path, source_path: Path, language: str) -> Path:
    return reading_dir_path(company_dir, language) / f"{source_path.stem}.html"


def workspace_core_paths(company_dir: Path, language: str) -> list[Path]:
    paths = [root_doc_path(company_dir, key, language) for key in CORE_WORKSPACE_FILE_KEYS]
    paths.append(state_path(company_dir))
    return paths


def _existing_language(company_dir: Path) -> Optional[str]:
    path = existing_state_path(company_dir)
    if path.is_file():
        try:
            return normalize_language(load_json(path).get("language"))
        except (json.JSONDecodeError, OSError, ValueError, AttributeError):
            return None
    return None


def workspace_persisted(company_dir: Optional[Path], language: Optional[str] = None) -> bool:
    if company_dir is None:
        return False
    active_language = normalize_language(language, _existing_language(company_dir))
    if all(path.is_file() for path in workspace_core_paths(company_dir, active_language)):
        return True
    legacy_core = [legacy_user_file_path(company_dir, key) for key in CORE_WORKSPACE_FILE_KEYS]
    legacy_core.extend(path for path in legacy_state_paths(company_dir))
    return all(path.is_file() for path in legacy_core)


def _move_path(source: Path, target: Path) -> None:
    if source == target or not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if source.is_dir() and target.is_dir():
            for child in sorted(source.iterdir()):
                _move_path(child, target / child.name)
            try:
                source.rmdir()
            except OSError:
                pass
        return
    source.rename(target)


def _cleanup_empty_dirs(paths: list[Path]) -> None:
    for path in sorted(paths, key=lambda item: len(item.parts), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                continue


def harmonize_workspace_layout(company_dir: Path, language: str) -> None:
    container_keys = [
        "product_demo",
        "records_progress",
        "records_decision",
        "records_calibration",
        "records_checkpoint",
        "legacy_root",
        "reading_root",
        "visual_kit",
        "artifact_delivery",
        "artifact_software",
        "artifact_business",
        "artifact_ops",
        "artifact_growth",
        "sales",
        "product",
        "delivery",
        "ops",
        "assets",
        "records",
        "roles",
        "flows",
        "artifacts_root",
    ]
    touched_dirs: list[Path] = []
    for key in container_keys:
        target = workspace_dir_path(company_dir, key, language)
        for candidate in candidate_container_paths(company_dir, key):
            if candidate == target:
                continue
            _move_path(candidate, target)
            touched_dirs.append(candidate)

    for key in [
        *ROOT_DOC_KEYS,
        "record_snapshot",
        "sales_actions",
        "sales_landing",
        "sales_interview",
        "sales_trial_application",
        "product_checklist",
        "product_demo_index",
        "delivery_tracker",
        "delivery_directory",
        "delivery_feedback",
        "ops_launch_checklist",
        "assets_inventory",
        "automation_notes",
        "role_index",
        "flow_bootstrap",
        "flow_round",
        "flow_calibration",
        "flow_stage",
        "automation_reminders",
        "automation_scheduler",
    ]:
        target = workspace_file_path(company_dir, key, language)
        for candidate in candidate_user_file_paths(company_dir, key):
            if candidate == target:
                continue
            _move_path(candidate, target)
            touched_dirs.append(candidate.parent)

    target_automation_dir = workspace_dir_path(company_dir, "automation", language)
    legacy_automation_dir = legacy_container_path(company_dir, "automation")
    if legacy_automation_dir != target_automation_dir:
        for filename in ("提醒规则.md", "定时任务定义.md"):
            _move_path(legacy_automation_dir / filename, target_automation_dir / filename)
        touched_dirs.append(legacy_automation_dir)

    _cleanup_empty_dirs(touched_dirs + [legacy_automation_dir])


def ensure_workspace_dirs(company_dir: Path, language: str) -> None:
    directories = [
        company_dir,
        workspace_dir_path(company_dir, "sales", language),
        workspace_dir_path(company_dir, "product", language),
        workspace_dir_path(company_dir, "product_demo", language),
        workspace_dir_path(company_dir, "delivery", language),
        workspace_dir_path(company_dir, "ops", language),
        workspace_dir_path(company_dir, "assets", language),
        workspace_dir_path(company_dir, "records", language),
        workspace_dir_path(company_dir, "records_progress", language),
        workspace_dir_path(company_dir, "records_decision", language),
        workspace_dir_path(company_dir, "records_calibration", language),
        workspace_dir_path(company_dir, "records_checkpoint", language),
        workspace_dir_path(company_dir, "legacy_root", language),
        workspace_dir_path(company_dir, "roles", language),
        workspace_dir_path(company_dir, "flows", language),
        workspace_dir_path(company_dir, "automation", language),
        workspace_dir_path(company_dir, "reading_root", language),
        workspace_dir_path(company_dir, "visual_kit", language),
        workspace_dir_path(company_dir, "artifacts_root", language),
        artifact_dir_path(company_dir, "delivery", language),
        artifact_dir_path(company_dir, "software", language),
        artifact_dir_path(company_dir, "business", language),
        artifact_dir_path(company_dir, "ops", language),
        artifact_dir_path(company_dir, "growth", language),
        state_path(company_dir).parent,
    ]
    for path in directories:
        path.mkdir(parents=True, exist_ok=True)


def _strip_internal_state(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _strip_internal_state(item) for key, item in value.items() if key != STATE_BASE_KEY}
    if isinstance(value, list):
        return [_strip_internal_state(item) for item in value]
    return value


def _merge_state_changes(base: Any, updated: Any, latest: Any) -> Any:
    if isinstance(base, dict) and isinstance(updated, dict) and isinstance(latest, dict):
        merged = deepcopy(latest)
        for key, value in updated.items():
            if key == STATE_BASE_KEY:
                continue
            if key not in base:
                merged[key] = deepcopy(value)
                continue
            base_value = base.get(key)
            latest_value = latest.get(key)
            if value == base_value:
                merged[key] = deepcopy(latest_value)
                continue
            if isinstance(base_value, dict) and isinstance(value, dict) and isinstance(latest_value, dict):
                merged[key] = _merge_state_changes(base_value, value, latest_value)
            else:
                merged[key] = deepcopy(value)
        return merged
    return deepcopy(updated if updated != base else latest)


def save_state(company_dir: Path, state: dict[str, Any]) -> None:
    language = normalize_language(state.get("language"))
    harmonize_workspace_layout(company_dir, language)
    ensure_workspace_dirs(company_dir, language)
    path = state_path(company_dir)
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    prepared = _strip_internal_state(state)
    base_state = deepcopy(state.get(STATE_BASE_KEY)) if isinstance(state.get(STATE_BASE_KEY), dict) else None
    with lock_path.open("w", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        if base_state is not None and path.exists():
            latest = read_state_any_version(company_dir)
            merged_state = _merge_state_changes(base_state, prepared, latest)
        else:
            merged_state = prepared
        saved_state = write_state_v3(company_dir, merged_state)
        for legacy_path in legacy_state_paths(company_dir):
            if legacy_path != path and legacy_path.exists():
                legacy_path.unlink()
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass
    state.clear()
    state.update(saved_state)
    state[STATE_BASE_KEY] = deepcopy(saved_state)


def load_state(company_dir: Path) -> dict[str, Any]:
    state = read_state_any_version(company_dir)
    state[STATE_BASE_KEY] = deepcopy(_strip_internal_state(state))
    return state


def role_display_names(role_ids: list[str], role_specs: dict[str, dict[str, Any]], language: str = "zh-CN") -> list[str]:
    names: list[str] = []
    for role_id in role_ids:
        if role_id in role_specs:
            names.append(localized_role_spec(role_specs[role_id], language)["display_name"])
    return names


def role_spec(role_id: str, role_specs: dict[str, dict[str, Any]], language: str = "zh-CN") -> dict[str, Any]:
    if role_id not in role_specs:
        raise ValueError(f"unknown role id: {role_id}")
    return localized_role_spec(role_specs[role_id], language)


def write_record(company_dir: Path, subdir: str, suffix: str, title: str, lines: list[str]) -> Path:
    language = _existing_language(company_dir) or "zh-CN"
    record_aliases = {
        "经营日志": "progress",
        "business-log": "progress",
        "推进日志": "progress",
        "progress-log": "progress",
        "经营决策": "decision",
        "business-decision": "decision",
        "决策记录": "decision",
        "decision-log": "decision",
        "校准记录": "calibration",
        "calibration-log": "calibration",
        "检查点": "checkpoint",
        "checkpoints": "checkpoint",
    }
    record_key = record_aliases.get(subdir, subdir)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = record_dir_path(company_dir, record_key, language) / f"{timestamp}-{suffix}.md"
    content = "\n".join([f"# {title}", "", *lines]) + "\n"
    write_text(path, content)
    return path


def preflight_status(company_dir: Optional[Path] = None, language: Optional[str] = None) -> dict[str, Any]:
    if company_dir and existing_state_path(company_dir).is_file():
        language = normalize_language(language, load_json(existing_state_path(company_dir)).get("language"))
    language = normalize_language(language)
    current_version = tuple(sys.version_info[:3])
    current_supported = is_python_version_supported(current_version)
    runtimes = discover_python_runtimes()
    compatible_runtime = choose_compatible_runtime(runtimes)

    required_paths = [SCRIPT_DIR / name for name in REQUIRED_SCRIPT_NAMES]
    required_paths.extend(
        [
            TEMPLATE_DIR / "company-overview-template.md",
            TEMPLATE_DIR / "artifact-output-guide-template.md",
            TEMPLATE_DIR / "artifact-docx-ready-template.md",
            TEMPLATE_DIR / "artifact-delivery-index-template.md",
            TEMPLATE_DIR / "artifact-software-delivery-template.md",
            TEMPLATE_DIR / "artifact-non-software-delivery-template.md",
            TEMPLATE_DIR / "artifact-quality-template.md",
            TEMPLATE_DIR / "artifact-deployment-template.md",
            TEMPLATE_DIR / "artifact-production-template.md",
            TEMPLATE_DIR / "artifact-launch-feedback-template.md",
            TEMPLATE_DIR / "artifact-validate-evidence-template.md",
            TEMPLATE_DIR / "artifact-growth-template.md",
            TEMPLATE_DIR / "stage-role-deliverable-matrix-template.md",
            TEMPLATE_DIR / "current-stage-deliverable-template.md",
            ORCHESTRATION_DIR / "stage-defaults.json",
            ORCHESTRATION_DIR / "handoff-schema.json",
        ]
    )
    missing = [display_path(path, ROOT) for path in required_paths if not path.exists()]
    installed = ROLE_DIR.is_dir() and not missing

    runtime_error = pick_text(language, "无", "None")
    runnable = False

    if company_dir is None:
        writable_target = ROOT
    elif company_dir.exists():
        writable_target = company_dir
    else:
        writable_target = company_dir.parent
    writable = writable_target.exists() and os.access(writable_target, os.W_OK)

    if not current_supported:
        minimum = version_text(MIN_SUPPORTED_PYTHON)
        if compatible_runtime:
            runtime_error = pick_text(
                language,
                f"当前解释器 {python_compatibility_label(current_version)} 不在兼容范围内；"
                f"可改用 {compatible_runtime['executable']} ({python_compatibility_label(compatible_runtime['version'])})。",
                f"The current interpreter {python_compatibility_label(current_version)} is outside the supported range; "
                f"you can switch to {compatible_runtime['executable']} ({python_compatibility_label(compatible_runtime['version'])}).",
            )
        else:
            runtime_error = pick_text(
                language,
                f"当前解释器 {python_compatibility_label(current_version)} 不在兼容范围内；"
                f"未发现可直接切换的 Python {minimum}+。",
                f"The current interpreter {python_compatibility_label(current_version)} is outside the supported range; "
                f"no directly switchable Python {minimum}+ runtime was found.",
            )
    elif installed:
        try:
            load_stage_defaults()
            load_role_specs()
            render_template("company-overview-template.md", {"COMPANY_NAME": "Preflight", "LANGUAGE": language})
        except Exception as exc:
            runtime_error = f"{type(exc).__name__}: {exc}"
        else:
            runnable = True
    else:
        runtime_error = pick_text(
            language,
            f"缺少文件: {joined_text(missing, language)}",
            f"Missing files: {joined_text(missing, language)}",
        )

    workspace_created = bool(company_dir and company_dir.exists())
    persisted = workspace_persisted(company_dir, language)

    if runnable and writable:
        recommended_mode_id = "script-execution"
    elif compatible_runtime and installed and writable:
        recommended_mode_id = "script-execution-switch-python"
    elif writable:
        recommended_mode_id = "manual-persistence"
    else:
        recommended_mode_id = "chat-only"

    if company_dir is None:
        unsaved_reason = pick_text(language, "尚未指定目标工作区", "No target workspace has been specified yet")
    elif not workspace_created:
        unsaved_reason = pick_text(language, "目标工作区尚未创建", "The target workspace has not been created yet")
    elif not persisted:
        unsaved_reason = pick_text(language, "工作区已存在，但关键文件未全部落盘", "The workspace exists, but not all core files have been persisted")
    else:
        unsaved_reason = pick_text(language, "无", "None")

    agent_action = build_agent_action(
        current_supported=current_supported,
        compatible_runtime=compatible_runtime,
        writable=writable,
        language=language,
    )
    return {
        "language": language,
        "installed": installed,
        "runnable": runnable,
        "python_supported": current_supported,
        "python_minimum": version_text(MIN_SUPPORTED_PYTHON),
        "current_python_version": version_text(current_version),
        "current_python_label": python_compatibility_label(current_version),
        "compatible_python_found": compatible_runtime is not None,
        "compatible_python_path": compatible_runtime["executable"] if compatible_runtime else pick_text(language, "无", "None"),
        "compatible_python_version": version_text(compatible_runtime["version"]) if compatible_runtime else pick_text(language, "无", "None"),
        "recovery_script": "scripts/ensure_python_runtime.py",
        "agent_action": agent_action,
        "workspace_created": workspace_created,
        "persisted": persisted,
        "writable": writable,
        "writable_target": str(writable_target),
        "python_path": sys.executable,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "recommended_mode_id": recommended_mode_id,
        "recommended_mode": persistence_mode_label(recommended_mode_id, language),
        "runtime_error": (
            pick_text(language, f"{runtime_error} 建议动作: {agent_action}", f"{runtime_error} Recommended action: {agent_action}")
            if runtime_error != pick_text(language, "无", "None")
            else runtime_error
        ),
        "missing_files": joined_text(missing, language),
        "unsaved_reason": unsaved_reason,
    }


def print_step(
    step: int,
    total: int,
    title: str,
    *,
    status: str = "已完成",
    stream: TextIO = sys.stdout,
    language: str = "zh-CN",
) -> None:
    resolved_step_id = resolve_step_id(title)
    step_id = resolved_step_id or step
    meta = step_meta(step_id, language) or {"human": title, "system": title}
    human_label = meta["human"]
    system_label = meta["system"]
    if status == "已完成" and language != "zh-CN":
        status = "Completed"
    if resolved_step_id == 0 and title not in (human_label, system_label):
        status = f"{status}（{title}）" if language == "zh-CN" else f"{status} ({title})"
    print(f"Step {step}/{total} {human_label} [{system_label}]: {status}", file=stream)


def print_block(title: str, items: list[tuple[str, str]], *, stream: TextIO = sys.stdout) -> None:
    print(f"{title}:", file=stream)
    for label, value in items:
        print(f"- {label}: {value}", file=stream)


def step_display(step_number: int, phase: str, language: str = "zh-CN") -> str:
    step_id = resolve_step_id(phase) or step_number
    meta = step_meta(step_id, language) or {"human": phase, "system": phase}
    return f"Step {step_number}/5 {meta['human']} [{meta['system']}]"


def explain_save_status(
    *,
    saved: bool,
    save_path: str,
    filenames: str,
    save_details: str,
    unsaved_reason: str,
    persistence_mode: str,
    language: str,
) -> list[tuple[str, str]]:
    if saved:
        return [
            (
                pick_text(language, "保存结论", "Persistence Result"),
                pick_text(language, "本次关键内容已经真实写入工作区，不只是停留在聊天里。", "The key output from this run has been written into the workspace instead of staying only in chat."),
            ),
            (pick_text(language, "你可以去哪里看", "Where To Look"), save_path),
            (pick_text(language, "这次写入了什么", "Files Written"), filenames),
            (pick_text(language, "写入明细", "Write Details"), save_details),
            (pick_text(language, "当前保存方式", "Current Persistence Mode"), persistence_mode),
        ]

    mode_id = normalize_persistence_mode(persistence_mode)
    save_next = {
        "script-execution": pick_text(language, "先修复脚本执行问题，再重跑当前步骤。", "Fix the script-execution issue first, then rerun this step."),
        "script-execution-switch-python": pick_text(language, "先切换到兼容 Python，再重跑当前步骤。", "Switch to a compatible Python runtime first, then rerun this step."),
        "manual-persistence": pick_text(language, "当前适合直接手动写入 markdown/json 到工作区。", "This environment is better suited for writing markdown/json directly into the workspace."),
        "chat-only": pick_text(language, "当前只能在对话里推进；如果要落盘，需要先确认创建或恢复写入能力。", "This run can only progress in chat; to persist output, confirm workspace creation or restore write access first."),
    }.get(mode_id, pick_text(language, "先确认是否允许写文件，再决定脚本执行或手动落盘。", "Confirm whether file writing is allowed before choosing script execution or manual persistence."))

    return [
        (pick_text(language, "保存结论", "Persistence Result"), pick_text(language, "本次内容还没有真实写入工作区。", "This run has not written the output into the workspace yet.")),
        (pick_text(language, "为什么还没保存", "Why It Is Not Persisted Yet"), unsaved_reason),
        (pick_text(language, "现在内容在哪里", "Where The Content Is Now"), pick_text(language, "当前内容只存在于本次输出或标准输出里。", "The current content only exists in this output or standard output.")),
        (pick_text(language, "如果你要保存", "How To Persist It"), save_next),
        (pick_text(language, "当前保存方式", "Current Persistence Mode"), persistence_mode),
    ]


def explain_runtime_status(runtime: dict[str, Any], language: str) -> list[tuple[str, str]]:
    if runtime["runnable"]:
        runtime_summary = pick_text(language, "当前环境可以直接运行脚本，适合走模式 A。", "The current environment can run the scripts directly, so Mode A is appropriate.")
    elif runtime["compatible_python_found"]:
        runtime_summary = pick_text(language, "当前解释器不理想，但已经找到可切换的兼容 Python。", "The current interpreter is not ideal, but a compatible Python runtime is available.")
    elif runtime["writable"]:
        runtime_summary = pick_text(language, "脚本暂时不稳，但当前环境还能直接写文件，适合走手动落盘。", "Script execution is not reliable right now, but the environment can still write files directly, so manual persistence is appropriate.")
    else:
        runtime_summary = pick_text(language, "当前环境既不适合直接跑脚本，也不适合直接写文件，只能先纯对话推进。", "The environment is not suitable for direct script execution or direct file writes, so chat-only progression is the only safe option for now.")

    install_summary = (
        pick_text(language, "技能文件齐全，可以继续恢复运行。", "The skill files are complete, so recovery can continue.")
        if runtime["installed"]
        else pick_text(language, "技能文件还不完整，先补齐缺失文件。", "The skill files are incomplete, so fill the missing files first.")
    )
    persistence_summary = (
        pick_text(language, "当前工作区已经具备核心落盘文件。", "The current workspace already contains the core persisted files.")
        if runtime["persisted"]
        else runtime["unsaved_reason"]
    )

    return [
        (pick_text(language, "运行结论", "Runtime Summary"), runtime_summary),
        (pick_text(language, "安装情况", "Installation Status"), install_summary),
        (
            pick_text(language, "工作区情况", "Workspace Status"),
            pick_text(language, "目标工作区已存在。", "The target workspace already exists.") if runtime["workspace_created"] else pick_text(language, "目标工作区还没有创建。", "The target workspace has not been created yet."),
        ),
        (pick_text(language, "落盘情况", "Persistence Status"), persistence_summary),
        (pick_text(language, "Python 兼容", "Python Compatibility"), pick_text(language, f"当前是 {runtime['current_python_label']}；兼容目标是 Python {runtime['python_minimum']}+。", f"The current runtime is {runtime['current_python_label']}; the compatibility target is Python {runtime['python_minimum']}+.")),
        (pick_text(language, "推荐动作", "Recommended Action"), runtime["agent_action"]),
    ]


def build_operating_snapshot(
    *,
    company_dir: Optional[Path],
    stage: str,
    round_name: str,
    role: str,
    artifact: str,
    next_action: str,
    language: str,
) -> list[tuple[str, str]]:
    if company_dir is not None:
        state_file = state_path(company_dir)
        if state_file.is_file():
            state = load_state(company_dir)
            focus = state.get("focus", {})
            product = state.get("product", {})
            pipeline = state.get("pipeline", {}).get("stage_summary", {})
            delivery_state = state.get("delivery", {})
            return [
                (pick_text(language, "当前经营模型", "Current Operating Model"), stage),
                (pick_text(language, "当前主目标", "Current Goal"), focus.get("primary_goal", stage)),
                (pick_text(language, "当前主战场", "Primary Arena"), primary_arena_label(focus.get("primary_arena", "sales"), language)),
                (pick_text(language, "产品状态", "Product State"), product_state_label(product.get("state", "idea"), language)),
                (pick_text(language, "成交概览", "Revenue Pipeline"), f"{pick_text(language, '对话', 'Talking')} {pipeline.get('talking', 0)} / {pick_text(language, '报价', 'Proposal')} {pipeline.get('proposal', 0)} / {pick_text(language, '成交', 'Won')} {pipeline.get('won', 0)}"),
                (pick_text(language, "交付状态", "Delivery Status"), delivery_state.get("delivery_status", pick_text(language, "待确认", "Pending"))),
                (pick_text(language, "当前瓶颈", "Current Bottleneck"), focus.get("primary_bottleneck", pick_text(language, "无", "None"))),
                (pick_text(language, "下一步最短动作", "Shortest Next Action"), focus.get("today_action", next_action)),
            ]

    return [
        (pick_text(language, "当前经营模型", "Current Operating Model"), stage),
        (pick_text(language, "当前主目标", "Current Goal"), round_name),
        (pick_text(language, "当前主战场", "Primary Arena"), primary_arena_label("sales", language)),
        (pick_text(language, "产品状态", "Product State"), product_state_label("idea", language)),
        (pick_text(language, "成交概览", "Revenue Pipeline"), pick_text(language, "待确认", "Pending")),
        (pick_text(language, "交付状态", "Delivery Status"), pick_text(language, "待确认", "Pending")),
        (pick_text(language, "当前瓶颈", "Current Bottleneck"), pick_text(language, "待确认", "Pending")),
        (pick_text(language, "下一步最短动作", "Shortest Next Action"), next_action),
    ]


def default_work_scope(artifact: str, language: str) -> list[str]:
    return [
        pick_text(language, f"说明本次与 {artifact} 相关的关键结果。", f"Explain the key results from this run related to {artifact}."),
        pick_text(language, "明确这次是否真正保存、保存到哪里。", "Explain clearly whether this run persisted output and where it was written."),
        pick_text(language, "明确当前环境该继续脚本执行、手动落盘，还是只做对话推进。", "Explain whether the current environment should continue with script execution, manual persistence, or chat-only progression."),
    ]


def default_non_scope(mode: str, language: str) -> list[str]:
    if mode == "创建公司" or mode == "Create Company":
        return [pick_text(language, "不会在未确认前假装已经完成正式创建。", "Do not pretend the formal creation already happened before approval.")]
    return [pick_text(language, "不会把未执行的动作说成已经完成。", "Do not claim unfinished actions are already complete.")]


def emit_runtime_report(
    *,
    mode: str,
    phase: str,
    stage: str,
    round_name: str,
    role: str,
    artifact: str,
    next_action: str,
    needs_confirmation: str,
    persistence_mode: str,
    company_dir: Optional[Path],
    saved_paths: list[Path],
    unsaved_reason: str = "无",
    work_scope: Optional[list[str]] = None,
    non_scope: Optional[list[str]] = None,
    changes: Optional[list[str]] = None,
    output_view: str = "both",
    step_number: int = 5,
    stream: TextIO = sys.stdout,
    language: Optional[str] = None,
) -> None:
    language = normalize_language(language, stage, round_name, role, artifact, next_action)
    runtime = preflight_status(company_dir, language=language)
    saved = bool(saved_paths) and all(path.exists() for path in saved_paths)
    save_path = str(company_dir) if company_dir is not None else "未指定"
    if company_dir is None:
        save_path = pick_text(language, "未指定", "Unspecified")
    save_details = joined_text((display_path(path, company_dir) for path in saved_paths), language)
    filenames = joined_text((path.name for path in saved_paths), language)

    if not saved and unsaved_reason == pick_text(language, "无", "None"):
        unsaved_reason = runtime["unsaved_reason"]
    work_scope = work_scope or default_work_scope(artifact, language)
    non_scope = non_scope or default_non_scope(mode, language)
    changes = changes or (
        [pick_text(language, f"已更新或写入 {joined_text((path.name for path in saved_paths), language)}。", f"Updated or wrote {joined_text((path.name for path in saved_paths), language)}.")] if saved_paths else [pick_text(language, "本次没有写入新文件。", "No new files were written in this run.")]
    )
    step_label = step_display(step_number, phase, language)
    localized_mode = mode_label(mode, language)
    localized_persistence_mode = persistence_mode_label(persistence_mode, language)
    operating_snapshot = build_operating_snapshot(
        company_dir=company_dir,
        stage=stage,
        round_name=round_name,
        role=role,
        artifact=artifact,
        next_action=next_action,
        language=language,
    )
    save_explanation = explain_save_status(
        saved=saved,
        save_path=save_path,
        filenames=filenames,
        save_details=save_details,
        unsaved_reason=unsaved_reason,
        persistence_mode=localized_persistence_mode,
        language=language,
    )
    runtime_explanation = explain_runtime_status(runtime, language)
    review_guidance = [
        (pick_text(language, "查看路径", "Review Path"), save_path),
        (pick_text(language, "重点文件", "Key Files"), save_details or pick_text(language, "本次没有新增保存文件", "No files were persisted in this run")),
        (
            pick_text(language, "如需继续改进", "If You Want Changes"),
            pick_text(language, "如果有不合适的地方，直接告诉我你想调整哪一项，我会继续改进。", "If anything feels off, tell me what to adjust and I will continue improving it."),
        ),
    ]

    if output_view in ("both", "navigation"):
        print(pick_text(language, "用户导航版:", "User Navigation View:"), file=stream)
        print_block(
            pick_text(language, "经营导航条", "Operating Navigation"),
            [
                (pick_text(language, "经营模型", "Operating Model"), stage),
                (pick_text(language, "推进面", "Operating Surface"), round_name),
                (pick_text(language, "本次 Step", "Current Step"), step_label),
            ],
            stream=stream,
        )
        print_block(
            pick_text(language, "本次范围", "Scope This Run"),
            [
                (pick_text(language, "本次会做", "Will Do"), joined_text(work_scope, language)),
                (pick_text(language, "本次不会做", "Will Not Do"), joined_text(non_scope, language)),
            ],
            stream=stream,
        )
        print_block(
            pick_text(language, "本次变化", "Changes This Run"),
            [
                (pick_text(language, f"变化 {index}", f"Change {index}"), value)
                for index, value in enumerate(changes, start=1)
            ],
            stream=stream,
        )
        print_block(pick_text(language, "经营快照", "Operating Snapshot"), operating_snapshot, stream=stream)
        print_block(pick_text(language, "查看与改进", "Review And Improve"), review_guidance, stream=stream)
        print_block(pick_text(language, "保存解释", "Persistence Explanation"), save_explanation, stream=stream)
        print_block(pick_text(language, "运行解释", "Runtime Explanation"), runtime_explanation, stream=stream)
        if output_view == "both":
            print("", file=stream)

    if output_view in ("both", "audit"):
        print(pick_text(language, "审计版:", "Audit View:"), file=stream)
        print_block(
            pick_text(language, "状态栏", "Status Bar"),
            [
                (pick_text(language, "当前模式", "Current Mode"), localized_mode),
                (pick_text(language, "当前步骤", "Current Step"), step_label),
                (pick_text(language, "当前经营模型", "Current Operating Model"), stage),
                (pick_text(language, "当前推进面", "Current Operating Surface"), round_name),
                (pick_text(language, "当前角色", "Current Role"), role),
                (pick_text(language, "当前产物", "Current Artifact"), artifact),
                (pick_text(language, "当前保存模式", "Current Persistence Mode"), localized_persistence_mode),
                (pick_text(language, "下一步动作", "Next Action"), next_action),
                (pick_text(language, "是否需要确认", "Needs Confirmation"), needs_confirmation),
            ],
            stream=stream,
        )
        print_block(
            pick_text(language, "保存状态", "Persistence Status"),
            [
                (pick_text(language, "是否已保存", "Persisted"), bool_label(saved, language)),
                (pick_text(language, "保存路径", "Save Path"), save_path),
                (pick_text(language, "文件名", "File Names"), filenames),
                (pick_text(language, "保存明细", "Save Details"), save_details),
                (pick_text(language, "未保存原因", "Unsaved Reason"), pick_text(language, "无", "None") if saved else unsaved_reason),
            ],
            stream=stream,
        )
        print_block(
            pick_text(language, "运行状态", "Runtime Status"),
            [
                ("installed", bool_audit_label(runtime["installed"], language)),
                ("runnable", bool_audit_label(runtime["runnable"], language)),
                ("python_supported", bool_audit_label(runtime["python_supported"], language)),
                ("workspace_created", bool_audit_label(runtime["workspace_created"], language)),
                ("persisted", bool_audit_label(runtime["persisted"], language)),
                ("writable", bool_audit_label(runtime["writable"], language)),
                (pick_text(language, "当前 Python", "Current Python"), f"{runtime['python_path']} ({runtime['python_version']})"),
                (pick_text(language, "兼容目标", "Compatibility Target"), f"Python {runtime['python_minimum']}+"),
                (pick_text(language, "可切换解释器", "Switchable Interpreter"), pick_text(language, "无", "None") if not runtime["compatible_python_found"] else f"{runtime['compatible_python_path']} ({runtime['compatible_python_version']})"),
                (pick_text(language, "恢复脚本", "Recovery Script"), runtime["recovery_script"]),
                (pick_text(language, "推荐模式", "Recommended Mode"), runtime["recommended_mode"]),
                (pick_text(language, "智能体建议动作", "Suggested Agent Action"), runtime["agent_action"]),
                (pick_text(language, "环境异常", "Runtime Error"), runtime["runtime_error"]),
            ],
            stream=stream,
        )


def build_matrix_values(role_specs: dict[str, dict[str, Any]], language: str) -> dict[str, str]:
    defaults = load_stage_defaults()
    values: dict[str, str] = {}
    for stage_id in ("validate", "build", "launch", "operate", "grow"):
        stage_upper = stage_id.upper()
        stage_roles = role_display_names(defaults["stage_defaults"][stage_id], role_specs, language)
        optional_roles = role_display_names(defaults["stage_optional_roles"].get(stage_id, []), role_specs, language)
        values[f"{stage_upper}_DEFAULT_ROLES"] = format_list(stage_roles, language)
        values[f"{stage_upper}_OPTIONAL_ROLES"] = format_list(optional_roles, language)
        values[f"{stage_upper}_REQUIRED_OUTPUTS"] = format_list(stage_required_outputs(stage_id, language), language)
    return values


def stage_artifact_specs(stage_id: str, language: str = "zh-CN") -> list[dict[str, str]]:
    def spec(category: str, subdir: str, index: str, title_zh: str, title_en: str, template: str) -> dict[str, str]:
        return {
            "category": category,
            "subdir": subdir,
            "index": index,
            "title": pick_text(language, title_zh, title_en),
            "template": template,
        }

    common_specs = [
        spec("delivery", "01-实际交付", "01", "实际产出总表", "actual-deliverables-index", "artifact-delivery-index-template.md"),
        spec("software", "02-软件与代码", "01", "代码与功能交付清单", "software-and-code-delivery-checklist", "artifact-software-delivery-template.md"),
        spec("business", "03-非软件与业务", "01", "非软件交付清单", "business-and-service-delivery-checklist", "artifact-non-software-delivery-template.md"),
    ]
    stage_specific = {
        "validate": [
            spec("delivery", "01-实际交付", "02", "问题与用户证据包", "problem-and-user-evidence-pack", "artifact-validate-evidence-template.md"),
        ],
        "build": [
            spec("software", "02-软件与代码", "02", "测试与验收记录", "test-and-acceptance-record", "artifact-quality-template.md"),
        ],
        "launch": [
            spec("software", "02-软件与代码", "02", "测试与验收记录", "test-and-acceptance-record", "artifact-quality-template.md"),
            spec("ops", "04-部署与生产", "01", "部署与回滚清单", "deployment-and-rollback-checklist", "artifact-deployment-template.md"),
            spec("ops", "04-部署与生产", "02", "生产观测与告警清单", "production-observability-and-alerting-checklist", "artifact-production-template.md"),
            spec("growth", "05-上线与增长", "01", "上线公告与反馈回收清单", "launch-announcement-and-feedback-capture-checklist", "artifact-launch-feedback-template.md"),
        ],
        "operate": [
            spec("ops", "04-部署与生产", "01", "部署与回滚清单", "deployment-and-rollback-checklist", "artifact-deployment-template.md"),
            spec("ops", "04-部署与生产", "02", "生产观测与告警清单", "production-observability-and-alerting-checklist", "artifact-production-template.md"),
            spec("ops", "04-部署与生产", "03", "事故响应与复盘记录", "incident-response-and-retrospective-record", "artifact-production-template.md"),
            spec("growth", "05-上线与增长", "01", "上线公告与反馈回收清单", "launch-announcement-and-feedback-capture-checklist", "artifact-launch-feedback-template.md"),
        ],
        "grow": [
            spec("ops", "04-部署与生产", "01", "部署与回滚清单", "deployment-and-rollback-checklist", "artifact-deployment-template.md"),
            spec("ops", "04-部署与生产", "02", "生产观测与告警清单", "production-observability-and-alerting-checklist", "artifact-production-template.md"),
            spec("growth", "05-上线与增长", "01", "增长实验与经营复盘", "growth-experiments-and-business-retrospective", "artifact-growth-template.md"),
        ],
    }
    return common_specs + stage_specific.get(stage_id, [])


def artifact_template_values(common_values: dict[str, str], state: dict[str, Any]) -> dict[str, str]:
    language = state.get("language", "zh-CN")
    focus = state.get("focus", {})
    return {
        **common_values,
        "ARTIFACT_TITLE": pick_text(language, "正式交付文件", "Formal Deliverable"),
        "ARTIFACT_TYPE": pick_text(language, "正式交付文档", "Formal Deliverable Document"),
        "ARTIFACT_OWNER": pick_text(language, "经营总控", "Operating Lead"),
        "ARTIFACT_OBJECTIVE": focus.get("week_outcome", pick_text(language, "沉淀一个可直接继续补齐的正式交付文档", "Create a formal deliverable that can be completed directly in place")),
        "ARTIFACT_SUMMARY": pick_text(language, "这份文档已经按最终交付文件命名落盘，接下来直接在原文件里补齐真实产出、证据、责任人和下一步动作。", "This document already uses its final deliverable name. Continue refining the real outputs, evidence, owner, and next action in place."),
        "ARTIFACT_SCOPE_IN": format_list(
            [
                pick_text(language, "实际软件产出或实际非软件产出", "Real software outputs or real non-software outputs"),
                pick_text(language, "验收证据与责任人", "Acceptance evidence and accountable owners"),
                pick_text(language, "与当前经营闭环匹配的部署/生产资料", "Deployment or production materials that match the current business loop"),
            ],
            language,
        ),
        "ARTIFACT_SCOPE_OUT": format_list(
            [
                pick_text(language, "只有聊天记录、没有文件或链接的伪交付", "Fake deliverables that only exist in chat without files or links"),
                pick_text(language, "缺少证据路径的空泛总结", "Vague summaries without evidence paths"),
            ],
            language,
        ),
        "ARTIFACT_DELIVERABLES": format_list(
            [
                pick_text(language, "真实产品、服务或业务交付证据", "Real product, service, or business delivery evidence"),
                pick_text(language, "客户、收入、交付或资产闭环的当前事实", "Current facts from the customer, revenue, delivery, or asset loop"),
                pick_text(language, "下一步经营动作与负责人", "The next operating action and owner"),
            ],
            language,
        ),
        "ARTIFACT_CHANGES": format_list(
            [
                pick_text(language, "文件名使用两位序号开头。", "File names should start with a two-digit index."),
                pick_text(language, "文件名直接使用最终交付名，不再把状态写进文件名。", "Use the final deliverable name directly instead of encoding document status in the file name."),
                pick_text(language, "产物目录默认只落 DOCX。", "Artifact directories default to DOCX-only formal outputs."),
                pick_text(language, "v1.0 不再把阶段/回合写进状态文件。", "v1.0 no longer writes stage or round fields into the state file."),
            ],
            language,
        ),
        "ARTIFACT_DECISIONS": format_list(
            [
                pick_text(language, "关键产物统一进入正式交付文档路径。", "Critical artifacts should enter the formal deliverable path."),
                pick_text(language, "软件和非软件产出都必须可被审计。", "Both software and non-software outputs must remain auditable."),
            ],
            language,
        ),
        "ARTIFACT_RISKS": format_list(
            [pick_text(language, "没有真实文件、代码、配置、材料或证据时，不应视为完成交付。", "If there are no real files, code, configuration, materials, or evidence, the work should not be treated as a completed delivery.")],
            language,
        ),
        "ARTIFACT_NEXT_ACTION": focus.get("today_action", pick_text(language, "补齐真实交付与证据。", "Fill in the real deliverables and evidence.")),
        "ARTIFACT_STATUS": pick_text(language, "起始版", "Starter Formal Doc"),
        "ARTIFACT_PROGRESS_SUMMARY": pick_text(language, "当前已经生成正式文档起始版，文件名和目录均按最终交付结构落盘，后续直接在原文件内补齐实际内容。", "A starter formal document has been created in the final folder and with the final file name. Continue completing the real content in place."),
        "ARTIFACT_MISSING_ITEMS": format_list(
            [
                pick_text(language, "真实文件、代码、材料或业务证据", "Real files, code, materials, or business evidence"),
                pick_text(language, "责任人与验收结论", "Owner and acceptance conclusion"),
                pick_text(language, "与当前主瓶颈匹配的下一步动作", "A next action that matches the current bottleneck"),
            ],
            language,
        ),
        "ARTIFACT_FILE_PATH": pick_text(language, "落盘后回填", "Filled after the file is written"),
    }


def build_founder_start_here(language: str) -> str:
    if language == "en-US":
        return "\n".join(
            [
                "# Founder Start Card",
                "",
                "## Reply Burden: Keep It To One Sentence",
                "",
                "- Tell me the founder idea in one sentence, or pick one direction below.",
                "- If you are not ready, reply with a single number and I will turn it into the first company draft.",
                "",
                "## Default AI-Era Path",
                "",
                "- Start from one narrow pain, not from a full business plan.",
                "- Validate demand quickly, ship the smallest useful MVP, launch narrowly, then improve from feedback.",
                "- Treat stages as lightweight bottleneck labels, not as bureaucracy.",
                "",
                "## Suggested Directions",
                "",
                "- 1. Sell an AI efficiency tool to a narrow professional role.",
                "- 2. Turn your own workflow into a reusable AI product.",
                "- 3. Build an AI service-plus-software hybrid for a niche industry.",
                "- 4. Build a small launchable product first and expand later.",
                "",
                "## Minimum Input Format",
                "",
                "- Idea: what you want to sell",
                "- User: who pays first",
                "- Problem: what pain is urgent",
                "",
                "## Good Enough Example",
                "",
                '- "I want to build an AI copilot for cross-border sellers who spend too much time writing product listings."',
                "",
                "## After You Reply",
                "",
                "- I will propose the company direction, the current bottleneck stage, the first round, and the first set of formal deliverable documents.",
                "- Review `11-交付目录总览.md` and `12-AI时代快循环.md` in this workspace next.",
                "- If the files, naming, or scope feel off, tell me what to tighten and I will keep refining it.",
            ]
        ) + "\n"
    return "\n".join(
        [
            "# 创始人启动卡",
            "",
            "## 你的回复负担只要一句话",
            "",
            "- 直接说一句你想做什么，或者从下面选一个方向。",
            "- 如果你还没想清楚，只回一个数字也可以，我会把它展开成第一版公司草案。",
            "",
            "## 默认 AI 时代路径",
            "",
            "- 先从一个足够窄的痛点开始，不先写一套大商业计划。",
            "- 先快速验证需求，再做最小可上线 MVP，上线后靠反馈迭代。",
            "- 阶段只是当前主瓶颈标签，不是官僚流程。",
            "",
            "## 可直接选的创业方向",
            "",
            "- 1. 给某个细分职业卖 AI 效率工具。",
            "- 2. 把你自己正在用的工作流产品化。",
            "- 3. 做一个“服务 + 软件”混合型 AI 业务。",
            "- 4. 先做一个可上线的小产品，再逐步扩展。",
            "",
            "## 最小输入格式",
            "",
            "- 想卖什么",
            "- 谁会先付费",
            "- 他现在最痛的点是什么",
            "",
            "## 合格示例",
            "",
            '- “我想做一个给跨境卖家的 AI 上架助手，帮他们更快写标题和描述。”',
            "",
            "## 你回复后我会做什么",
            "",
            "- 我会给出方向建议、当前主瓶颈阶段、首个回合和首批正式交付文档。",
            "- 你可以先看 `11-交付目录总览.md` 和 `12-AI时代快循环.md`，再告诉我还要怎么收紧或改进。",
        ]
    ) + "\n"


def build_ai_fast_loop(language: str) -> str:
    if language == "en-US":
        return "\n".join(
            [
                "# AI-Era Solo Company Fast Loop",
                "",
                "## Core Principle",
                "",
                "- Do not run a solo company like a heavy startup bureaucracy.",
                "- Move through a fast loop: narrow pain, validate demand, ship the smallest useful MVP, launch narrowly, collect feedback, improve, then scale what works.",
                "- Internal stages exist to mark the current bottleneck, not to force unnecessary ceremony.",
                "",
                "## Recommended Loop",
                "",
                "- 1. Narrow the user and pain: make the first buyer and urgent pain concrete.",
                "- 2. Validate with real evidence: interviews, waitlist, pre-sales, manual service, or usage signals.",
                "- 3. Ship the smallest launchable MVP: solve one valuable path end to end.",
                "- 4. Launch narrowly: release to a small user set and a small channel mix first.",
                "- 5. Capture feedback and production reality: keep notes on behavior, objections, bugs, support, and metrics.",
                "- 6. Improve before scaling: fix retention, value delivery, and reliability before widening distribution.",
                "",
                "## How Internal Stages Map To The Loop",
                "",
                "- Validation: find a sharp problem and real demand signals.",
                "- Build: ship the minimum MVP that proves value.",
                "- Launch: put the MVP in front of real users with deployment and feedback paths.",
                "- Operate: keep improving the product through feedback, support, and production stability.",
                "- Grow: scale only after value, retention, and delivery quality are real enough.",
                "",
                "## How To Use This Workspace",
                "",
                "- Start from `10-创始人启动卡.md` if the idea is still fuzzy.",
                "- Use `11-交付目录总览.md` to see which formal documents already exist and which one to improve next.",
                "- Keep one round to roughly 2 to 3 hours, then update the current state.",
                "- Trigger calibration when blocked, drifting, or when a key artifact has just completed.",
                "- Keep formal outputs in `产物/`, and keep software, non-software, and post-launch operations evidence auditable.",
            ]
        ) + "\n"
    return "\n".join(
        [
            "# AI 时代一人公司快循环",
            "",
            "## 核心原则",
            "",
            "- 不要把一人公司跑成重型创业官僚流程。",
            "- 默认走一条快循环：收窄痛点，快速验证，做最小可上线 MVP，小范围上线，收反馈，再迭代，然后再放大。",
            "- 内部阶段只用来标记当前主瓶颈，不用来制造额外手续。",
            "",
            "## 推荐循环",
            "",
            "- 1. 收窄用户和痛点：先说清谁最痛、为什么现在痛、谁会先付费。",
            "- 2. 快速验证需求：用访谈、预约、预售、手动服务或真实使用信号验证。",
            "- 3. 产出最小可上线 MVP：只打通一个真正有价值的闭环。",
            "- 4. 小范围上线：先推给一小批目标用户和少量渠道，不求铺满。",
            "- 5. 回收反馈与生产现实：持续记录使用行为、异议、故障、支持和关键指标。",
            "- 6. 先改再放大：先把价值交付、留存和稳定性修稳，再谈大规模增长。",
            "",
            "## 内部阶段如何映射到这条快循环",
            "",
            "- 验证期：找到尖锐问题和真实需求信号。",
            "- 构建期：做出能证明价值的最小 MVP。",
            "- 上线期：把 MVP 推到真实用户面前，并补齐部署和反馈链路。",
            "- 运营期：围绕反馈、支持和生产稳定性持续修产品。",
            "- 增长期：只在价值、留存和交付质量足够真实后再放大渠道和收益。",
            "",
            "## 在这个工作区里怎么跑",
            "",
            "- 如果想法还模糊，先看 `10-创始人启动卡.md`。",
            "- 用 `11-交付目录总览.md` 看当前正式文档目录、文档成熟度和下一步要补哪一份。",
            "- 单个回合建议控制在 2 到 3 小时，再回来更新当前状态。",
            "- 卡住、偏航或刚完成关键产物时再触发校准。",
            "- 正式件统一进 `产物/`，软件、非软件和上线后生产资料都必须可审计。",
        ]
    ) + "\n"


def primary_arena_label(arena: str, language: str) -> str:
    labels = {
        "sales": pick_text(language, "卖前", "Sales"),
        "product": pick_text(language, "产品", "Product"),
        "delivery": pick_text(language, "交付", "Delivery"),
        "cash": pick_text(language, "现金", "Cash"),
        "asset": pick_text(language, "资产", "Asset"),
    }
    return labels.get(arena, arena)


def product_state_label(state_id: str, language: str) -> str:
    labels = {
        "idea": pick_text(language, "只有想法", "Idea Only"),
        "defined": pick_text(language, "已定义范围", "Scope Defined"),
        "prototype": pick_text(language, "原型中", "In Prototype"),
        "internal": pick_text(language, "内部可用", "Internally Usable"),
        "external": pick_text(language, "外部可测", "Externally Testable"),
        "launchable": pick_text(language, "可上线售卖", "Launchable"),
        "live": pick_text(language, "已上线运行", "Live"),
    }
    return labels.get(state_id, state_id)


def write_text_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        write_text(path, text)


def build_operating_dashboard(state: dict[str, Any], company_dir: Path) -> str:
    language = state["language"]
    focus = state["focus"]
    offer = state["offer"]
    pipeline = state["pipeline"]["stage_summary"]
    product = state["product"]
    delivery = state["delivery"]
    cash = state["cash"]
    lines = [
        pick_text(language, "# 经营总盘", "# Operating Dashboard"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 当前结论", "## Current Read"),
        "",
        f"- {pick_text(language, '公司', 'Company')}: {state['company_name']}",
        f"- {pick_text(language, '产品', 'Product')}: {state['product_name']}",
        f"- {pick_text(language, '头号目标', 'Primary Goal')}: {focus['primary_goal']}",
        f"- {pick_text(language, '当前主瓶颈', 'Primary Bottleneck')}: {focus['primary_bottleneck']}",
        f"- {pick_text(language, '当前主战场', 'Primary Arena')}: {primary_arena_label(focus['primary_arena'], language)}",
        f"- {pick_text(language, '今天最短动作', 'Shortest Action Today')}: {focus['today_action']}",
        f"- {pick_text(language, '本周唯一结果', 'Single Weekly Outcome')}: {focus['week_outcome']}",
        "",
        pick_text(language, "## 闭环健康", "## Loop Health"),
        "",
        f"- {pick_text(language, '价值承诺', 'Offer Promise')}: {offer['promise']}",
        f"- {pick_text(language, '目标客户', 'Target Customer')}: {offer['target_customer']}",
        f"- {pick_text(language, '产品状态', 'Product State')}: {product_state_label(product['state'], language)} | {pick_text(language, '版本', 'Version')}: {product['current_version']}",
        f"- {pick_text(language, '成交管道', 'Pipeline')}: {pick_text(language, '发现', 'Discovering')} {pipeline['discovering']} / {pick_text(language, '对话', 'Talking')} {pipeline['talking']} / {pick_text(language, '试用', 'Trial')} {pipeline['trial']} / {pick_text(language, '报价', 'Proposal')} {pipeline['proposal']} / {pick_text(language, '成交', 'Won')} {pipeline['won']}",
        f"- {pick_text(language, '客户交付', 'Delivery')}: {delivery['delivery_status']}",
        f"- {pick_text(language, '现金面', 'Cash')}: in {cash['cash_in']} | out {cash['cash_out']} | {pick_text(language, '待回款', 'Receivable')} {cash['receivable']}",
        "",
        pick_text(language, "## 现在先看哪里", "## Where To Look Next"),
        "",
        f"- [{root_doc_path(company_dir, 'founder_constraints', language).name}]({display_path(root_doc_path(company_dir, 'founder_constraints', language), company_dir)})",
        f"- [{root_doc_path(company_dir, 'offer', language).name}]({display_path(root_doc_path(company_dir, 'offer', language), company_dir)})",
        f"- [{root_doc_path(company_dir, 'pipeline', language).name}]({display_path(root_doc_path(company_dir, 'pipeline', language), company_dir)})",
        f"- [{root_doc_path(company_dir, 'product_status', language).name}]({display_path(root_doc_path(company_dir, 'product_status', language), company_dir)})",
        f"- [{root_doc_path(company_dir, 'delivery_cash', language).name}]({display_path(root_doc_path(company_dir, 'delivery_cash', language), company_dir)})",
        "",
        pick_text(language, "## 关键支撑文档", "## Key Support Documents"),
        "",
        f"- [{pick_text(language, '对外落地页文案', 'Landing Page Copy')}]({display_path(workspace_file_path(company_dir, 'sales_landing', language), company_dir)})",
        f"- [{pick_text(language, '访谈冲刺看板', 'Interview Sprint Board')}]({display_path(workspace_file_path(company_dir, 'sales_interview', language), company_dir)})",
        f"- [{pick_text(language, '试用申请问卷', 'Trial Application Form')}]({display_path(workspace_file_path(company_dir, 'sales_trial_application', language), company_dir)})",
        f"- [{pick_text(language, '可演示静态页', 'Demo Page')}]({display_path(workspace_file_path(company_dir, 'product_demo_index', language), company_dir)})",
        f"- [{pick_text(language, 'MVP 与上线清单', 'MVP And Launch Checklist')}]({display_path(workspace_file_path(company_dir, 'product_checklist', language), company_dir)})",
        f"- [{pick_text(language, '上线检查清单', 'Launch Checklist')}]({display_path(workspace_file_path(company_dir, 'ops_launch_checklist', language), company_dir)})",
        f"- [{pick_text(language, '试用反馈回收表', 'Trial Feedback Capture')}]({display_path(workspace_file_path(company_dir, 'delivery_feedback', language), company_dir)})",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_founder_constraints_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    founder = state["founder"]
    lines = [
        pick_text(language, "# 创始人约束", "# Founder Constraints"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 经营方式", "## Founder Operating Mode"),
        "",
        f"- {pick_text(language, '当前模式', 'Current Mode')}: {founder['working_mode']}",
        f"- {pick_text(language, '目标模式', 'Goal Mode')}: {founder['goal_mode']}",
        f"- {pick_text(language, '时间预算', 'Time Budget')}: {founder['time_budget']}",
        f"- {pick_text(language, '现金压力', 'Cash Pressure')}: {founder['cash_pressure']}",
        "",
        pick_text(language, "## 优势", "## Strengths"),
        "",
        format_list(founder.get("strengths", []), language),
        "",
        pick_text(language, "## 约束", "## Constraints"),
        "",
        format_list(founder.get("constraints", []), language),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_offer_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    offer = state["offer"]
    lines = [
        pick_text(language, "# 价值承诺与报价", "# Value Promise And Pricing"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 当前可卖承诺", "## Current Sellable Promise"),
        "",
        f"- {pick_text(language, '卖什么结果', 'Promised Result')}: {offer['promise']}",
        f"- {pick_text(language, '卖给谁', 'Target Buyer')}: {offer['target_customer']}",
        f"- {pick_text(language, '高频场景', 'High-Frequency Scenario')}: {offer['scenario']}",
        f"- {pick_text(language, '定价方式', 'Pricing')}: {offer['pricing']}",
        "",
        pick_text(language, "## 为什么现在值得买", "## Why It Is Worth Buying Now"),
        "",
        format_list(offer.get("proof", []), language),
        "",
        pick_text(language, "## 当前缺口", "## Current Gap"),
        "",
        f"- {pick_text(language, '如果还卖不动，优先补价值表达、试用路径和报价，而不是盲加功能。', 'If this still does not sell, improve the value story, trial path, and pricing before adding more features.')}",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_pipeline_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    pipeline = state["pipeline"]
    summary = pipeline["stage_summary"]
    opportunities = pipeline.get("opportunities", [])
    lines = [
        pick_text(language, "# 机会与成交管道", "# Opportunity And Revenue Pipeline"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 管道概览", "## Pipeline Summary"),
        "",
        f"- {pick_text(language, '发现', 'Discovering')}: {summary['discovering']}",
        f"- {pick_text(language, '对话', 'Talking')}: {summary['talking']}",
        f"- {pick_text(language, '试用', 'Trial')}: {summary['trial']}",
        f"- {pick_text(language, '报价', 'Proposal')}: {summary['proposal']}",
        f"- {pick_text(language, '成交', 'Won')}: {summary['won']}",
        f"- {pick_text(language, '丢失', 'Lost')}: {summary['lost']}",
        "",
        f"{pick_text(language, '下一条真实成交动作', 'Next Real Revenue Action')}: {pipeline['next_revenue_action']}",
        "",
        pick_text(language, "## 当前机会", "## Current Opportunities"),
        "",
    ]
    if opportunities:
        for item in opportunities:
            lines.extend(
                [
                    f"- {item.get('name', pick_text(language, '未命名机会', 'Untitled Opportunity'))} | "
                    f"{pick_text(language, '阶段', 'Stage')}: {item.get('stage', pick_text(language, '待确认', 'TBD'))} | "
                    f"{pick_text(language, '下一步', 'Next Step')}: {item.get('next_action', pick_text(language, '待补充', 'Add next step'))}",
                ]
            )
    else:
        lines.append(pick_text(language, "- 还没有录入具体机会。先补最早能推进收入的一条。", "- No concrete opportunity is recorded yet. Add the earliest revenue-moving one first."))
    lines.extend(["", ""])
    return "\n".join(lines)


def build_product_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    product = state["product"]
    lines = [
        pick_text(language, "# 产品与上线状态", "# Product And Launch Status"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 当前状态", "## Current State"),
        "",
        f"- {pick_text(language, '产品状态', 'Product State')}: {product_state_label(product['state'], language)}",
        f"- {pick_text(language, '当前版本', 'Current Version')}: {product['current_version']}",
        f"- {pick_text(language, '上线阻塞', 'Launch Blocker')}: {product['launch_blocker']}",
        f"- {pick_text(language, '仓库', 'Repository')}: {product['repository'] or pick_text(language, '待补充', 'Add repository path')}",
        f"- {pick_text(language, '上线入口', 'Launch Entry')}: {product['launch_path'] or pick_text(language, '待补充', 'Add launch path')}",
        "",
        pick_text(language, "## 核心能力", "## Core Capability"),
        "",
        format_list(product.get("core_capability", []), language),
        "",
        pick_text(language, "## 当前缺口", "## Current Gap"),
        "",
        format_list(product.get("current_gap", []), language),
        "",
        pick_text(language, "## 当前产品策略", "## Current Product Strategy"),
        "",
        pick_text(language, "- 先做一个端到端可证明价值的最小工作流，不先铺满全部功能。", "- Start with one end-to-end workflow that proves value before broadening scope."),
        pick_text(language, "- 先做创始人可交付的 demo + 试用闭环，再决定哪些环节值得自动化。", "- Run a founder-deliverable demo and trial loop first, then decide what is worth automating."),
        pick_text(language, "- 先验证首批买家的 willingness to pay，再考虑扩展到更多人群、渠道或套餐。", "- Validate willingness to pay with the first buyer segment before expanding to more audiences, channels, or plans."),
        "",
        pick_text(language, "## 现在直接打开", "## Open Next"),
        "",
        f"- [{display_path(workspace_file_path(Path('.'), 'product_checklist', language), Path('.'))}]({display_path(workspace_file_path(Path('.'), 'product_checklist', language), Path('.'))})",
        f"- [{display_path(workspace_file_path(Path('.'), 'product_demo_index', language), Path('.'))}]({display_path(workspace_file_path(Path('.'), 'product_demo_index', language), Path('.'))})",
        f"- [{display_path(workspace_file_path(Path('.'), 'ops_launch_checklist', language), Path('.'))}]({display_path(workspace_file_path(Path('.'), 'ops_launch_checklist', language), Path('.'))})",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_delivery_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    delivery = state["delivery"]
    cash = state["cash"]
    lines = [
        pick_text(language, "# 客户交付与回款", "# Delivery And Cash Collection"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        f"- {pick_text(language, '活跃客户数', 'Active Customers')}: {delivery['active_customers']}",
        f"- {pick_text(language, '当前交付状态', 'Delivery Status')}: {delivery['delivery_status']}",
        f"- {pick_text(language, '交付阻塞', 'Delivery Blocker')}: {delivery['blocking_issue']}",
        f"- {pick_text(language, '下一步交付动作', 'Next Delivery Action')}: {delivery['next_delivery_action']}",
        f"- {pick_text(language, '待回款', 'Receivable')}: {cash['receivable']}",
        "",
        pick_text(language, "## 原则", "## Principle"),
        "",
        pick_text(
            language,
            "- 一人公司不是卖完就结束。这里要持续看交付质量、回款速度、复购机会和口碑风险。",
            "- A solo company does not end at the sale. Track delivery quality, collection speed, renewal opportunity, and reputation risk here.",
        ),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_mvp_checklist_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    product = state["product"]
    focus = state["focus"]
    lines = [
        pick_text(language, "# MVP 与上线清单", "# MVP And Launch Checklist"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 这版先交付什么", "## What This Version Must Deliver"),
        "",
        f"- {pick_text(language, '当前版本', 'Current Version')}: {product['current_version']}",
        f"- {pick_text(language, '当前状态', 'Current State')}: {product_state_label(product['state'], language)}",
        f"- {pick_text(language, '当前主瓶颈', 'Primary Bottleneck')}: {focus['primary_bottleneck']}",
        "",
        pick_text(language, "## Demo 必须出现", "## Demo Must Show"),
        "",
        format_list(product.get("core_capability", []), language),
        "",
        pick_text(language, "## 上线前必须补齐", "## Must Be Closed Before Launch"),
        "",
        format_list(product.get("current_gap", []), language),
        "",
        pick_text(language, "## 当前发版原则", "## Current Release Principle"),
        "",
        pick_text(language, "- 先做能演示、能试用、能收反馈的最小版本，不先堆完整功能。", "- Ship the smallest version that can be demoed, trialed, and observed before building out the full product."),
        pick_text(language, "- 先把价值边界、试用入口、反馈闭环跑通，再决定要不要重投入工程化。", "- Get the value boundary, trial entry, and feedback loop working before committing to heavy engineering."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_sales_action_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    pipeline = state["pipeline"]
    summary = pipeline["stage_summary"]
    lines = [
        pick_text(language, "# 成交动作清单", "# Revenue Action Checklist"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 当前漏斗", "## Current Funnel"),
        "",
        f"- {pick_text(language, '发现', 'Discovering')}: {summary['discovering']}",
        f"- {pick_text(language, '对话', 'Talking')}: {summary['talking']}",
        f"- {pick_text(language, '试用', 'Trial')}: {summary['trial']}",
        f"- {pick_text(language, '报价', 'Proposal')}: {summary['proposal']}",
        f"- {pick_text(language, '成交', 'Won')}: {summary['won']}",
        "",
        f"- {pick_text(language, '下一条真实成交动作', 'Next Real Revenue Action')}: {pipeline['next_revenue_action']}",
        "",
        pick_text(language, "## 本周必须推进", "## Must Move This Week"),
        "",
        pick_text(language, "- 锁定 10 个真实目标客户或渠道对象。", "- Lock 10 real target buyers or channel partners."),
        pick_text(language, "- 完成 5 次深访，记录原话、卡点和付费信号。", "- Run 5 interviews and capture exact words, blockers, and buying signals."),
        pick_text(language, "- 约出至少 3 个愿意看 demo 的对象。", "- Book at least 3 people willing to watch the demo."),
        pick_text(language, "- 给每个机会都写清楚下一步，而不是只记名字。", "- Give every opportunity a next step instead of just a name."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_landing_copy_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    offer = state["offer"]
    product = state["product"]
    product_name = state["product_name"]
    scenario = offer["scenario"]
    modules = product.get("core_capability", [])[:5]
    pains = [
        pick_text(language, "现有替代方案往往靠手工、碎片工具或零散服务拼起来，推进慢且质量不稳。", "Current alternatives are usually stitched together from manual work, fragmented tools, or ad hoc services, which makes execution slow and inconsistent."),
        pick_text(language, f"{offer['target_customer']} 已经能感受到这个问题，但还缺一个能真正跑通结果的闭环。", f"{offer['target_customer']} already feels this pain, but still lacks one loop that reliably produces the desired outcome."),
        pick_text(language, f"如果 {scenario} 继续靠临时方案处理，时间、机会和交付质量都会继续流失。", f"If {scenario} keeps being handled with temporary workarounds, time, opportunity, and delivery quality will keep leaking."),
    ]
    lines = [
        pick_text(language, "# 对外落地页文案", "# Landing Page Copy"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## Hero", "## Hero"),
        "",
        f"- {pick_text(language, '标题', 'Headline')}: {product_name}：{offer['promise']}",
        f"- {pick_text(language, '副标题', 'Subheadline')}: {offer['promise']}",
        f"- {pick_text(language, '主 CTA', 'Primary CTA')}: {pick_text(language, '预约 20 分钟演示', 'Book a 20-minute demo')}",
        f"- {pick_text(language, '次 CTA', 'Secondary CTA')}: {pick_text(language, '申请 14 天试用', 'Apply for a 14-day trial')}",
        "",
        pick_text(language, "## 适合谁", "## Who This Is For"),
        "",
        f"- {offer['target_customer']}",
        pick_text(language, f"- 当前正被 {scenario} 反复拖慢，希望先把一个高频关键动作跑顺。", f"- People currently slowed down by {scenario} and looking to make one high-frequency workflow reliable first."),
        pick_text(language, "- 愿意先用一个更小、更快、更可验证的版本换取真实结果和反馈。", "- People willing to start with a smaller, faster, more testable version in exchange for real outcomes and feedback."),
        "",
        pick_text(language, "## 你现在为什么会卡住", "## Why You Are Stuck Today"),
        "",
        format_list(pains, language),
        "",
        pick_text(language, "## 产品怎么帮你推进", "## How The Product Moves You Forward"),
        "",
        format_list(modules, language),
        "",
        pick_text(language, "## 14 天试用里你会拿到什么", "## What The 14-Day Trial Delivers"),
        "",
        pick_text(language, f"- 第 1 天：创始人访谈，确认 {scenario}、成功指标和当前最大阻塞。", f"- Day 1: founder interview to confirm {scenario}, the success metric, and the biggest blocker."),
        pick_text(language, "- 第 2-7 天：跑完 1 条端到端试用任务，记录真实使用行为、阻碍和价值感知。", "- Days 2-7: run one end-to-end trial workflow and record real behavior, blockers, and perceived value."),
        pick_text(language, "- 第 7 天：拿到中期反馈，知道最需要补的是哪一步，而不是继续泛泛加功能。", "- Day 7: receive a midpoint review that shows which step needs work most instead of continuing with vague feature expansion."),
        pick_text(language, "- 第 14 天：收到结果复盘，决定继续月付、项目制、顾问式服务，还是暂停。", "- Day 14: receive a result review and decide whether to continue via monthly plan, project engagement, concierge support, or pause."),
        "",
        pick_text(language, "## 定价", "## Pricing"),
        "",
        f"- {offer['pricing']}",
        "",
        pick_text(language, "## 边界说明", "## Product Boundary"),
        "",
        pick_text(language, "- 首版只解决一个高频关键工作流，不承诺一次覆盖所有边缘场景。", "- The first version solves one high-frequency critical workflow rather than covering every edge case at once."),
        pick_text(language, "- 需要人工判断、定制交付或高风险决策的环节，仍由创始人或客户明确确认。", "- Any step that still needs human judgment, custom delivery, or high-risk decisions stays behind explicit founder or customer confirmation."),
        pick_text(language, "- 在真实付费和留存被验证前，不默认扩展到更重、更广、更复杂的产品边界。", "- Do not widen the product boundary by default until real payment and retention have been validated."),
        "",
        pick_text(language, "## 页尾 CTA", "## Footer CTA"),
        "",
        pick_text(language, "- 想确认你离第一个可复用结果还差哪一步？先约一次 20 分钟演示。", "- Want to know which step still blocks your first repeatable result? Start with a 20-minute demo."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_interview_sprint_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    target_customer = state["offer"]["target_customer"]
    scenario = state["offer"]["scenario"]
    lines = [
        pick_text(language, "# 访谈冲刺看板", "# Interview Sprint Board"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 本轮目标", "## Sprint Goal"),
        "",
        pick_text(language, "- 7 天内约到 10 个访谈对象，完成 5 次深访，拿到 3 个愿意看 demo 的对象。", "- Book 10 interview targets within 7 days, complete 5 interviews, and secure 3 people willing to watch the demo."),
        "",
        pick_text(language, "## 10 个目标席位", "## 10 Target Slots"),
        "",
        pick_text(language, f"1. {target_customer} | 来源: 现有朋友 / 同事转介绍 | 条件: 现在就有 {scenario} | 下一步: 发首轮邀约", f"1. {target_customer} | Source: warm referrals from friends or colleagues | Criteria: already dealing with {scenario} | Next: send first outreach"),
        pick_text(language, f"2. {target_customer} | 来源: 相关社群 / 群组 | 条件: 最近公开提过这个问题 | 下一步: 约 20 分钟访谈", f"2. {target_customer} | Source: relevant communities or groups | Criteria: publicly mentioned this problem recently | Next: book a 20-minute interview"),
        pick_text(language, f"3. {target_customer} | 来源: 老客户 / 老同事 / 校友 | 条件: 你已有一定信任基础 | 下一步: 请求 2 个转介绍", f"3. {target_customer} | Source: ex-customers, former colleagues, or alumni | Criteria: you already have baseline trust | Next: ask for 2 referrals"),
        pick_text(language, "4. 公开内容评论者 | 来源: 公众号 / 小红书 / LinkedIn / X | 条件: 明确表达过相关痛点 | 下一步: 私信邀约", "4. Public content commenters | Source: newsletters / social posts / LinkedIn / X | Criteria: explicitly described the same pain | Next: direct-message outreach"),
        pick_text(language, "5. 邮件订阅者或表单线索 | 来源: 现有名单 | 条件: 点开过相关主题 | 下一步: 发试用申请链接", "5. Newsletter subscribers or form leads | Source: existing list | Criteria: already clicked related topics | Next: send the trial application link"),
        pick_text(language, "6. 渠道伙伴 | 来源: 服务商 / 顾问 / 社群组织者 | 条件: 服务同类人群 | 下一步: 约渠道访谈", "6. Channel partners | Source: agencies / consultants / community operators | Criteria: already serve the same audience | Next: schedule a partner interview"),
        pick_text(language, "7. 互补服务提供者 | 来源: 公开服务页 | 条件: 能补足你暂时不做的环节 | 下一步: 讨论联合试用", "7. Complementary service providers | Source: public service pages | Criteria: they cover adjacent steps you are not solving yet | Next: discuss a joint trial"),
        pick_text(language, "8. 预算决策人 | 来源: 公开团队页 / 公司页 | 条件: 可能买单或推动试点 | 下一步: 验证预算与采购路径", "8. Budget owners | Source: public team or company pages | Criteria: likely to sponsor or approve a pilot | Next: validate budget and buying path"),
        pick_text(language, "9. 行业内内容创作者 | 来源: 公开账号 | 条件: 持续分享该问题的经验 | 下一步: 邀请做顾问访谈", "9. Industry creators | Source: public accounts | Criteria: regularly share experience about this problem | Next: invite them to an advisor interview"),
        pick_text(language, "10. 早期采用者候选 | 来源: 你自己的工作流或关系网 | 条件: 愿意接受不完美版本换更快结果 | 下一步: 约 demo", "10. Early adopter candidates | Source: your own workflow or network | Criteria: willing to trade polish for faster results | Next: book a demo"),
        "",
        pick_text(language, "## 每次访谈必须产出", "## Every Interview Must Produce"),
        "",
        pick_text(language, "- 当前工作流和触发场景", "- the current workflow and triggering scenario"),
        pick_text(language, "- 最贵、最慢、最焦虑的一步", "- the most expensive, slowest, and most anxiety-inducing step"),
        pick_text(language, "- 是否愿意看 demo", "- whether they will watch the demo"),
        pick_text(language, "- 是否愿意试用或付订金", "- whether they will trial or place a deposit"),
        "",
        pick_text(language, "## 结束标准", "## Exit Criteria"),
        "",
        pick_text(language, "- 访谈原话足够支撑落地页改写和 demo 收口。", "- the exact user language is strong enough to rewrite the landing page and tighten the demo."),
        pick_text(language, "- 至少 3 个对象愿意进入 demo 或试用。", "- at least 3 people agree to enter the demo or trial."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_trial_application_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    product_name = state["product_name"]
    lines = [
        pick_text(language, "# 试用申请问卷", "# Trial Application Form"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 开场说明", "## Intro"),
        "",
        f"- {product_name} 当前只开放给问题明确、愿意在 14 天内完成试用任务并给出真实反馈的首批对象。",
        pick_text(language, "- 目标不是广撒网，而是筛出 5-10 位最可能给出高质量反馈和转化信号的人。", "- The goal is not broad lead capture. It is to identify 5-10 early users who will generate strong feedback and conversion signals."),
        "",
        pick_text(language, "## 必填字段", "## Required Fields"),
        "",
        pick_text(language, "1. 姓名或称呼", "1. Name"),
        pick_text(language, "2. 当前角色 / 团队 / 公司", "2. Current role / team / company"),
        pick_text(language, "3. 你现在最想跑通的工作流是什么", "3. Which workflow you most want to fix right now"),
        pick_text(language, "4. 这个问题现在有多紧急，为什么", "4. How urgent this problem is right now and why"),
        pick_text(language, "5. 你当前最大的卡点排序", "5. Rank your biggest blockers"),
        pick_text(language, "6. 最近 6 个月你已经为此花了多少钱和多少时间", "6. Money and time already spent in the last 6 months"),
        pick_text(language, "7. 你希望 14 天试用先帮你解决哪一步", "7. Which step you want the 14-day trial to solve first"),
        pick_text(language, "8. 是否愿意完成 14 天内的固定试用任务", "8. Whether you will complete the fixed tasks within 14 days"),
        pick_text(language, "9. 是否愿意接受 20 分钟访谈和第 14 天复盘", "9. Whether you accept a 20-minute interview and a day-14 review"),
        pick_text(language, "10. 联系方式", "10. Contact info"),
        "",
        pick_text(language, "## 筛选规则", "## Screening Rules"),
        "",
        pick_text(language, "- 优先收：问题明确、时间窗明确、愿意在近期真的推进的人。", "- Prioritize applicants with a clear problem, clear timing, and real intent to move soon."),
        pick_text(language, "- 优先收：已经为这个问题投入过时间、金钱或内部资源的人。", "- Prioritize people who have already invested real time, money, or internal resources into this problem."),
        pick_text(language, "- 延后收：只是泛泛咨询、没有具体使用场景、也不愿完成试用任务的人。", "- Delay applicants who are only browsing, have no concrete use case, and will not complete the trial tasks."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_trial_feedback_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    lines = [
        pick_text(language, "# 试用反馈回收表", "# Trial Feedback Capture"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 第 7 天必须回收", "## Must Capture On Day 7"),
        "",
        pick_text(language, "- 哪个模块最有帮助：路径导航 / 沟通训练 / 面试模拟 / 文书表达", "- Which module helped most: pathway guidance / communication drill / interview simulation / documentation"),
        pick_text(language, "- 你实际花了多少分钟使用", "- How many minutes you actually spent"),
        pick_text(language, "- 你最不愿意继续用的是哪一步，为什么", "- Which step you are least willing to continue and why"),
        pick_text(language, "- 如果今天结束试用，你会不会付费继续", "- If the trial ended today, would you pay to continue"),
        "",
        pick_text(language, "## 第 14 天必须回收", "## Must Capture On Day 14"),
        "",
        pick_text(language, "- 哪个结果指标最明显提升", "- Which outcome metric improved the most"),
        pick_text(language, "- 哪个环节仍然没有解决", "- Which part remains unsolved"),
        pick_text(language, "- 你觉得合理的付费方式是月订阅、训练营还是按次陪跑", "- Which payment mode feels right: monthly, cohort sprint, or concierge support"),
        pick_text(language, "- 你愿不愿意推荐给另一个也有同类问题的人", "- Whether you would recommend it to another person with the same problem"),
        "",
        pick_text(language, "## 结果记录", "## Outcome Record"),
        "",
        pick_text(language, "- 是否转化为继续试用 / 月付 / 冲刺营 / 退出", "- Whether the user converted into continued trial / monthly / sprint / exit"),
        pick_text(language, "- 如果退出，退出原因只写原话，不写自我解释", "- If they exit, record the exact reason in their words instead of your interpretation"),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_demo_html(state: dict[str, Any]) -> str:
    language = state["language"]
    product_name = escape(state["product_name"])
    company_name = escape(state["company_name"])
    offer = state["offer"]
    product = state["product"]
    promise = escape(offer["promise"])
    target = escape(offer["target_customer"])
    pricing = escape(offer["pricing"])
    proof_source = offer.get("proof", []) or [
        pick_text(language, "已经明确首批买家与高频使用场景。", "The first buyer and high-frequency scenario are already defined."),
        pick_text(language, "当前版本只承诺一个可验证结果，不承诺解决全部问题。", "The current version promises one testable result rather than everything at once."),
        pick_text(language, "试用、反馈、成交动作会在同一个经营闭环里推进。", "Trial, feedback, and revenue actions move inside the same operating loop."),
    ]
    proof_items = "".join(f"<li>{escape(item)}</li>" for item in proof_source)
    capability_source = product.get("core_capability", [])[:5] or [pick_text(language, "补充首个端到端能力描述", "Add the first end-to-end capability")]
    capability_cards = "".join(
        f"<article class=\"card\"><h3>{escape(pick_text(language, '模块', 'Module'))} {index + 1}</h3><p>{escape(item)}</p></article>"
        for index, item in enumerate(capability_source)
    )
    gap_source = product.get("current_gap", [])[:5] or [pick_text(language, "补充当前最关键的上线阻塞", "Add the most important current launch blocker")]
    gap_items = "".join(f"<li>{escape(item)}</li>" for item in gap_source)
    eyebrow = escape(pick_text(language, "Founder Demo", "Founder Demo"))
    audience_label = escape(pick_text(language, "面向人群：", "For:"))
    primary_cta = escape(pick_text(language, "预约 20 分钟演示", "Book a 20-minute demo"))
    secondary_cta = escape(pick_text(language, "申请 14 天试用", "Apply for a 14-day trial"))
    metric_1_label = escape(pick_text(language, "条核心工作流先跑通", "core workflow first"))
    metric_2_label = escape(pick_text(language, "首轮试用与反馈闭环", "trial and feedback loop"))
    metric_3_label = escape(pick_text(language, "个区块先证明价值", "blocks to prove value"))
    panel_title = escape(pick_text(language, "这不是另一个空泛工具壳", "This Is Not Another Vague Tool Shell"))
    panel_body = escape(
        pick_text(
            language,
            "它把价值承诺、产品体验、试用入口和反馈回收放进同一个闭环里。先帮创始人把一个高频关键动作跑顺，再决定要不要扩功能、扩渠道或扩交付。",
            "It puts the promise, product experience, trial entry, and feedback capture into one loop. First help the founder make one high-frequency critical workflow reliable, then decide whether to expand features, channels, or delivery.",
        )
    )
    panel_bullets = [
        escape(pick_text(language, "首版先跑通一个高频关键工作流", "The first version proves one high-frequency critical workflow")),
        escape(pick_text(language, "暂时需要人工补位的环节可以保留人工", "Human support can remain where automation is still premature")),
        escape(pick_text(language, "先证明价值和回款，再扩大产品边界", "Prove value and revenue before widening the product boundary")),
    ]
    section_modules = escape(pick_text(language, "核心模块", "Core Modules"))
    section_why = escape(pick_text(language, "为什么现在先做这个版本", "Why This Version Goes First"))
    section_trial = escape(pick_text(language, "14 天试用路径", "14-Day Trial Path"))
    section_pricing = escape(pick_text(language, "定价与当前阻塞", "Pricing And Current Blockers"))
    pricing_label = escape(pick_text(language, "定价：", "Pricing:"))
    blocker_label = escape(pick_text(language, "当前还要补齐：", "Still needs to close:"))
    join_cta = escape(pick_text(language, "加入首批试用名单", "Join the first trial group"))
    form_label_timing = escape(pick_text(language, "你希望多快把这个问题解决", "How quickly do you want to solve this"))
    form_label_blocker = escape(pick_text(language, "你最卡的一步", "Your biggest blocker"))
    form_label_goal = escape(pick_text(language, "你希望 14 天试用先帮你解决什么", "What should the 14-day trial solve first"))
    form_default_blocker = escape(pick_text(language, "获客 / 转化 / 交付 / 上线 / 留存", "acquisition / conversion / delivery / launch / retention"))
    form_default_goal = escape(pick_text(language, "我最想先把一个高频关键动作跑顺，并确认用户是否愿意继续付费。", "I want to make one high-frequency critical workflow reliable first and confirm whether users will keep paying."))
    step_titles = [
        escape(pick_text(language, "创始人访谈", "Founder Interview")),
        escape(pick_text(language, "试用任务", "Trial Workflow")),
        escape(pick_text(language, "中期反馈", "Midpoint Review")),
        escape(pick_text(language, "结果复盘", "Outcome Review")),
    ]
    step_bodies = [
        escape(pick_text(language, "确认当前工作流、成功指标和最大阻塞。", "Confirm the current workflow, success metric, and biggest blocker.")),
        escape(pick_text(language, "跑完一条端到端任务，记录真实行为、问题和价值感知。", "Run one end-to-end workflow and capture behavior, blockers, and perceived value.")),
        escape(pick_text(language, "第 7 天收口问题，明确最需要补的下一步。", "On day 7, tighten the problem and define the next fix with the highest leverage.")),
        escape(pick_text(language, "第 14 天决定继续月付、项目制、顾问式支持，还是暂停。", "On day 14, decide whether to continue with monthly, project-based, concierge support, or pause.")),
    ]
    return f"""<!doctype html>
<html lang="{escape('zh-CN' if language == 'zh-CN' else 'en')}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{product_name} Demo</title>
  <style>
    :root {{
      --bg: #f5efe4;
      --ink: #17211d;
      --muted: #51605a;
      --accent: #c95f35;
      --panel: #fffaf2;
      --line: #d9ccb9;
      --ok: #2f7d4d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Noto Sans SC", "PingFang SC", "Helvetica Neue", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top right, rgba(201,95,53,.12), transparent 28%),
        linear-gradient(180deg, #f8f3ea 0%, #efe5d4 100%);
    }}
    .shell {{ max-width: 1120px; margin: 0 auto; padding: 40px 20px 72px; }}
    .hero {{
      display: grid;
      grid-template-columns: 1.1fr .9fr;
      gap: 24px;
      align-items: stretch;
    }}
    .panel {{
      background: rgba(255,250,242,.92);
      border: 1px solid var(--line);
      border-radius: 28px;
      padding: 28px;
      box-shadow: 0 24px 60px rgba(40,31,20,.08);
    }}
    h1, h2, h3 {{ font-family: "Sora", "Avenir Next", sans-serif; margin: 0 0 12px; }}
    h1 {{ font-size: clamp(32px, 6vw, 62px); line-height: 1.02; letter-spacing: -.04em; }}
    h2 {{ font-size: 28px; }}
    p {{ line-height: 1.65; color: var(--muted); }}
    .eyebrow {{
      display: inline-block; padding: 6px 12px; border-radius: 999px;
      background: rgba(201,95,53,.12); color: var(--accent); font-size: 13px; font-weight: 700;
      letter-spacing: .04em; text-transform: uppercase;
    }}
    .cta-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; }}
    .btn {{
      display: inline-flex; align-items: center; justify-content: center;
      padding: 12px 18px; border-radius: 999px; text-decoration: none; font-weight: 700;
      border: 1px solid var(--ink); color: var(--ink);
    }}
    .btn.primary {{ background: var(--ink); color: #fffdf7; border-color: var(--ink); }}
    .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 20px; }}
    .metric {{ background: #f1e5d3; border-radius: 18px; padding: 16px; }}
    .metric strong {{ display: block; font-size: 26px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; margin-top: 28px; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 22px; padding: 20px; }}
    ul {{ margin: 0; padding-left: 20px; color: var(--muted); }}
    li {{ margin: 0 0 10px; line-height: 1.6; }}
    .steps {{ counter-reset: step; display: grid; gap: 14px; }}
    .step {{ position: relative; padding: 18px 18px 18px 64px; }}
    .step::before {{
      counter-increment: step; content: counter(step);
      position: absolute; left: 18px; top: 16px; width: 32px; height: 32px;
      border-radius: 50%; background: var(--accent); color: white;
      display: grid; place-items: center; font-weight: 700;
    }}
    .footer-note {{ font-size: 14px; color: var(--muted); margin-top: 24px; }}
    .form {{ display: grid; gap: 12px; margin-top: 16px; }}
    label {{ font-size: 14px; color: var(--ink); font-weight: 600; }}
    input, textarea, select {{
      width: 100%; margin-top: 6px; padding: 12px 14px; border-radius: 14px;
      border: 1px solid var(--line); background: #fffdf8; color: var(--ink);
      font: inherit;
    }}
    textarea {{ min-height: 110px; resize: vertical; }}
    @media (max-width: 860px) {{
      .hero, .grid {{ grid-template-columns: 1fr; }}
      .metrics {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="panel">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{product_name}</h1>
        <p>{promise}</p>
        <p>{audience_label} {target}</p>
        <div class="cta-row">
          <a class="btn primary" href="#trial">{primary_cta}</a>
          <a class="btn" href="#pricing">{secondary_cta}</a>
        </div>
        <div class="metrics">
          <div class="metric"><strong>1</strong><span>{metric_1_label}</span></div>
          <div class="metric"><strong>14</strong><span>{metric_2_label}</span></div>
          <div class="metric"><strong>3</strong><span>{metric_3_label}</span></div>
        </div>
      </div>
      <div class="panel">
        <h2>{panel_title}</h2>
        <p>{panel_body}</p>
        <ul>
          <li>{panel_bullets[0]}</li>
          <li>{panel_bullets[1]}</li>
          <li>{panel_bullets[2]}</li>
        </ul>
        <p class="footer-note">{escape(pick_text(language, '公司：', 'Company:'))} {company_name}</p>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>{section_modules}</h2>
        <div class="grid">{capability_cards}</div>
      </div>
      <div class="card">
        <h2>{section_why}</h2>
        <ul>{proof_items}</ul>
      </div>
    </section>

    <section class="grid" id="trial">
      <div class="card">
        <h2>{section_trial}</h2>
        <div class="steps">
          <div class="card step"><h3>{step_titles[0]}</h3><p>{step_bodies[0]}</p></div>
          <div class="card step"><h3>{step_titles[1]}</h3><p>{step_bodies[1]}</p></div>
          <div class="card step"><h3>{step_titles[2]}</h3><p>{step_bodies[2]}</p></div>
          <div class="card step"><h3>{step_titles[3]}</h3><p>{step_bodies[3]}</p></div>
        </div>
      </div>
      <div class="card" id="pricing">
        <h2>{section_pricing}</h2>
        <p><strong>{pricing_label}</strong>{pricing}</p>
        <p><strong>{blocker_label}</strong></p>
        <ul>{gap_items}</ul>
        <div class="cta-row">
          <a class="btn primary" href="#trial">{join_cta}</a>
        </div>
        <form class="form">
          <label>{form_label_timing}
            <select>
              <option>{escape(pick_text(language, '1-2 周', '1-2 weeks'))}</option>
              <option>{escape(pick_text(language, '30 天内', 'within 30 days'))}</option>
              <option>{escape(pick_text(language, '90 天内', 'within 90 days'))}</option>
              <option>{escape(pick_text(language, '只是先了解', 'just exploring'))}</option>
            </select>
          </label>
          <label>{form_label_blocker}
            <input type="text" value="{form_default_blocker}">
          </label>
          <label>{form_label_goal}
            <textarea>{form_default_goal}</textarea>
          </label>
        </form>
      </div>
    </section>
  </div>
</body>
</html>
"""


def build_launch_checklist_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    product = state["product"]
    offer = state["offer"]
    lines = [
        pick_text(language, "# 上线检查清单", "# Launch Checklist"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 上线前要确认", "## Confirm Before Launch"),
        "",
        f"- {pick_text(language, '卖什么结果', 'Promised Result')}: {offer['promise']}",
        f"- {pick_text(language, '面向谁', 'Target Buyer')}: {offer['target_customer']}",
        f"- {pick_text(language, '上线入口', 'Launch Entry')}: {product['launch_path'] or pick_text(language, '待补充', 'Add launch path')}",
        f"- {pick_text(language, '当前阻塞', 'Current Blocker')}: {product['launch_blocker']}",
        "",
        pick_text(language, "## 最低上线标准", "## Minimum Launch Bar"),
        "",
        pick_text(language, "- 能被解释清楚：用户 30 秒内知道你解决什么问题。", "- Explainable: the user understands the promised result within 30 seconds."),
        pick_text(language, "- 能被试用：有明确 demo、表单、预约或开通入口。", "- Trialable: there is a clear demo, form, booking, or activation path."),
        pick_text(language, "- 能被收集反馈：知道看什么数据、问什么问题。", "- Observable: you know which feedback and signals to collect."),
        pick_text(language, "- 能解释边界：不做什么、风险在哪里、谁来承担最终决策。", "- Bounded: you can explain what the product does not do, the risks, and who keeps final responsibility."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_cash_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    cash = state["cash"]
    lines = [
        pick_text(language, "# 现金流与经营健康", "# Cashflow And Business Health"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        f"- cash in: {cash['cash_in']}",
        f"- cash out: {cash['cash_out']}",
        f"- {pick_text(language, '待回款', 'Receivable')}: {cash['receivable']}",
        f"- {pick_text(language, '月目标收入', 'Monthly Target')}: {cash['monthly_target']}",
        f"- runway: {cash['runway_note']}",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_asset_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    assets = state["assets"]
    lines = [
        pick_text(language, "# 资产与自动化", "# Assets And Automation"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        "## SOP",
        "",
        format_list(assets.get("sops", []), language),
        "",
        pick_text(language, "## 模板", "## Templates"),
        "",
        format_list(assets.get("templates", []), language),
        "",
        pick_text(language, "## 案例", "## Cases"),
        "",
        format_list(assets.get("cases", []), language),
        "",
        pick_text(language, "## 自动化", "## Automations"),
        "",
        format_list(assets.get("automations", []), language),
        "",
        pick_text(language, "## 可复用代码", "## Reusable Code"),
        "",
        format_list(assets.get("reusable_code", []), language),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_risk_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    risk = state["risk"]
    lines = [
        pick_text(language, "# 风险与关键决策", "# Risks And Key Decisions"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        pick_text(language, "## 顶级风险", "## Top Risks"),
        "",
        format_list(risk.get("top_risks", []), language),
        "",
        pick_text(language, "## 待决策", "## Pending Decisions"),
        "",
        format_list(risk.get("pending_decisions", []), language),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_week_focus_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    focus = state["focus"]
    lines = [
        pick_text(language, "# 本周唯一主目标", "# Single Weekly Goal"),
        "",
        f"- {pick_text(language, '主目标', 'Primary Goal')}: {focus['primary_goal']}",
        f"- {pick_text(language, '主战场', 'Primary Arena')}: {primary_arena_label(focus['primary_arena'], language)}",
        f"- {pick_text(language, '本周唯一结果', 'Weekly Outcome')}: {focus['week_outcome']}",
        f"- {pick_text(language, '为什么现在先做这个', 'Why This Comes First')}: {focus['primary_bottleneck']}",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_today_action_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    focus = state["focus"]
    lines = [
        pick_text(language, "# 今日最短动作", "# Shortest Action Today"),
        "",
        f"- {pick_text(language, '今天只推进这一件事', 'Only Push This Today')}: {focus['today_action']}",
        f"- {pick_text(language, '当前主瓶颈', 'Primary Bottleneck')}: {focus['primary_bottleneck']}",
        f"- {pick_text(language, '完成标准', 'Definition Of Done')}: {pick_text(language, '今天结束前，当前主瓶颈至少向前推进一格。', 'By the end of today, the current bottleneck should move forward by at least one step.')}",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_collaboration_memory_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    lines = [
        pick_text(language, "# 协作记忆", "# Collaboration Memory"),
        "",
        pick_text(language, "- 每次用户纠偏、风格偏好或交付约束，都要及时补到这里。", "- Record every user correction, delivery preference, and collaboration constraint here."),
        pick_text(language, "- 开工前先读这个文件，再读会话交接。", "- Read this file before starting, then read the session handoff."),
        pick_text(language, "- 不要把文档规范当成最终文档输出。", "- Do not output document specifications instead of final documents."),
        pick_text(language, "- 已完成的文件名不要加状态词。", "- Do not add status words to completed file names."),
        "",
    ]
    return "\n".join(lines) + "\n"


def build_session_handoff_doc(state: dict[str, Any]) -> str:
    language = state["language"]
    focus = state["focus"]
    lines = [
        pick_text(language, "# 会话交接", "# Session Handoff"),
        "",
        f"{pick_text(language, '更新时间', 'Updated At')}: {now_string()}",
        "",
        f"- {pick_text(language, '当前主目标', 'Current Primary Goal')}: {focus['primary_goal']}",
        f"- {pick_text(language, '当前主瓶颈', 'Current Primary Bottleneck')}: {focus['primary_bottleneck']}",
        f"- {pick_text(language, '当前主战场', 'Current Primary Arena')}: {primary_arena_label(focus['primary_arena'], language)}",
        f"- {pick_text(language, '下一步最短动作', 'Shortest Next Action')}: {focus['today_action']}",
        "",
    ]
    return "\n".join(lines) + "\n"


def reading_source_paths(company_dir: Path, language: str) -> list[Path]:
    return [root_doc_path(company_dir, key, language) for key in ROOT_DOC_KEYS] + [
        workspace_file_path(company_dir, file_key, language) for file_key in READING_EXTRA_FILE_KEYS
    ]


def relative_href(target: Path, current_dir: Path) -> str:
    return os.path.relpath(target, start=current_dir).replace(os.sep, "/")


def reading_export_map(company_dir: Path, language: str) -> dict[Path, Path]:
    mapping: dict[Path, Path] = {}
    for source in reading_source_paths(company_dir, language):
        mapping[source.resolve()] = reading_export_path(company_dir, source, language)
    return mapping


def resolve_reading_href(
    href: str,
    *,
    source_path: Path,
    output_path: Path,
    company_dir: Path,
    language: str,
) -> str:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href

    target_path = (source_path.parent / href).resolve()
    export_target = reading_export_map(company_dir, language).get(target_path)
    if export_target is not None:
        return relative_href(export_target, output_path.parent)
    if target_path == company_dir or company_dir in target_path.parents:
        return relative_href(target_path, output_path.parent)
    return href


def render_inline_markdown(
    text: str,
    *,
    source_path: Path,
    output_path: Path,
    company_dir: Path,
    language: str,
) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`|\*\*([^*]+)\*\*")
    parts: list[str] = []
    cursor = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > cursor:
            parts.append(html_escape(text[cursor:start]))
        link_label, link_href, code_text, bold_text = match.groups()
        if link_label is not None:
            resolved_href = resolve_reading_href(
                link_href,
                source_path=source_path,
                output_path=output_path,
                company_dir=company_dir,
                language=language,
            )
            parts.append(
                f'<a href="{html_escape(resolved_href, quote=True)}">{html_escape(link_label)}</a>'
            )
        elif code_text is not None:
            parts.append(f"<code>{html_escape(code_text)}</code>")
        elif bold_text is not None:
            parts.append(f"<strong>{html_escape(bold_text)}</strong>")
        cursor = end
    if cursor < len(text):
        parts.append(html_escape(text[cursor:]))
    return "".join(parts)


def markdown_to_html_fragment(
    markdown_text: str,
    *,
    source_path: Path,
    output_path: Path,
    company_dir: Path,
    language: str,
) -> str:
    lines = markdown_text.splitlines()
    blocks: list[str] = []
    index = 0

    def render_inline(text: str) -> str:
        return render_inline_markdown(
            text,
            source_path=source_path,
            output_path=output_path,
            company_dir=company_dir,
            language=language,
        )

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        if stripped.startswith("```"):
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            blocks.append(f"<pre><code>{html_escape(chr(10).join(code_lines))}</code></pre>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            index += 1
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip()[2:].strip())
                index += 1
            blocks.append(
                "<ul>\n"
                + "\n".join(f"  <li>{render_inline(item)}</li>" for item in items)
                + "\n</ul>"
            )
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            items: list[str] = []
            while index < len(lines):
                current = lines[index].strip()
                match = re.match(r"^\d+\.\s+(.+)$", current)
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            blocks.append(
                "<ol>\n"
                + "\n".join(f"  <li>{render_inline(item)}</li>" for item in items)
                + "\n</ol>"
            )
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            current = lines[index].strip()
            if not current or current.startswith("- ") or current.startswith("```") or re.match(r"^(#{1,6})\s+", current) or re.match(r"^\d+\.\s+", current):
                break
            paragraph_lines.append(current)
            index += 1
        blocks.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")

    return "\n".join(blocks)


def reading_navigation_items(company_dir: Path, language: str) -> list[tuple[str, Path]]:
    items = [
        (pick_text(language, "经营驾驶舱", "Operating Cockpit"), reading_entry_path(company_dir, language)),
    ]
    for key in ROOT_DOC_KEYS:
        source = root_doc_path(company_dir, key, language)
        items.append((source.stem, reading_export_path(company_dir, source, language)))
    extra_source = workspace_file_path(company_dir, "delivery_directory", language)
    items.append((extra_source.stem, reading_export_path(company_dir, extra_source, language)))
    return items


def render_reading_shell(
    *,
    title: str,
    subtitle: str,
    body_html: str,
    language: str,
    company_name: str,
    current_path: Path,
    navigation_items: list[tuple[str, Path]],
) -> str:
    nav_links = []
    for label, path in navigation_items:
        href = relative_href(path, current_path.parent)
        is_current = path == current_path
        class_name = "nav-link is-current" if is_current else "nav-link"
        nav_links.append(
            f'<a class="{class_name}" href="{html_escape(href, quote=True)}">{html_escape(label)}</a>'
        )
    language_tag = "zh-CN" if language == "zh-CN" else "en"
    footer_text = pick_text(
        language,
        "阅读版适合下载直接查看；原始 Markdown 继续保留为工作底稿；正式对外交付仍以 DOCX 为准。",
        "The reading layer is for direct viewing after download; the original markdown remains the working source; formal external deliverables still live in DOCX files.",
    )
    return f"""<!doctype html>
<html lang="{html_escape(language_tag, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_escape(title)} - {html_escape(company_name)}</title>
  <style>
    :root {{
      --bg: #f6f3ec;
      --surface: rgba(255, 252, 247, 0.94);
      --surface-strong: #fffdf8;
      --line: #ded5c6;
      --ink: #1f1a14;
      --ink-soft: #5f5448;
      --accent: #b85c38;
      --accent-deep: #8d4024;
      --success: #2f7d5b;
      --shadow: 0 18px 44px rgba(57, 39, 22, 0.12);
      --radius: 20px;
      --radius-pill: 999px;
      --max: 1120px;
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(184, 92, 56, 0.16), transparent 34%),
        radial-gradient(circle at top right, rgba(47, 125, 91, 0.11), transparent 26%),
        linear-gradient(180deg, #faf7f1 0%, var(--bg) 100%);
    }}
    a {{ color: var(--accent-deep); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{
      border-radius: 8px;
      padding: 0.12rem 0.38rem;
      background: rgba(31, 26, 20, 0.07);
      font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
      font-size: 0.92em;
    }}
    pre {{
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 1rem 1.1rem;
      background: #f4efe5;
    }}
    .page {{
      width: min(calc(100% - 32px), var(--max));
      margin: 0 auto;
      padding: 28px 0 48px;
    }}
    .hero {{
      padding: 28px 30px;
      border: 1px solid rgba(184, 92, 56, 0.18);
      border-radius: 28px;
      background:
        linear-gradient(145deg, rgba(255, 251, 244, 0.96), rgba(250, 243, 233, 0.92)),
        linear-gradient(120deg, rgba(184, 92, 56, 0.10), transparent 55%);
      box-shadow: var(--shadow);
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 0.55rem;
      margin-bottom: 0.9rem;
      border-radius: var(--radius-pill);
      padding: 0.42rem 0.82rem;
      background: rgba(184, 92, 56, 0.12);
      color: var(--accent-deep);
      font-size: 0.84rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(2rem, 4vw, 3.2rem);
      line-height: 1.03;
      font-family: "Alegreya", Georgia, serif;
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      margin: 0.9rem 0 0;
      max-width: 760px;
      color: var(--ink-soft);
      font-size: 1rem;
      line-height: 1.65;
    }}
    .nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.7rem;
      margin: 1rem 0 0;
    }}
    .nav-link {{
      display: inline-flex;
      align-items: center;
      min-height: 40px;
      padding: 0.55rem 0.88rem;
      border: 1px solid var(--line);
      border-radius: var(--radius-pill);
      background: rgba(255, 253, 248, 0.88);
      color: var(--ink-soft);
      font-weight: 600;
      text-decoration: none;
    }}
    .nav-link:hover {{
      color: var(--ink);
      text-decoration: none;
    }}
    .nav-link.is-current {{
      border-color: rgba(184, 92, 56, 0.26);
      background: rgba(184, 92, 56, 0.14);
      color: var(--accent-deep);
    }}
    .content {{
      margin-top: 22px;
      padding: 28px 30px;
      border: 1px solid var(--line);
      border-radius: 28px;
      background: var(--surface);
      box-shadow: 0 10px 28px rgba(57, 39, 22, 0.08);
    }}
    .content h2, .content h3, .content h4 {{
      margin: 1.4rem 0 0.7rem;
      font-family: "Alegreya", Georgia, serif;
      line-height: 1.16;
    }}
    .content h2:first-child,
    .content h3:first-child,
    .content h4:first-child {{
      margin-top: 0;
    }}
    .content p, .content li {{
      color: var(--ink);
      line-height: 1.72;
      font-size: 1rem;
    }}
    .content ul, .content ol {{
      padding-left: 1.2rem;
    }}
    .footer {{
      margin-top: 18px;
      color: var(--ink-soft);
      font-size: 0.95rem;
      line-height: 1.65;
    }}
    .card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin: 1.2rem 0 0;
    }}
    .card {{
      padding: 16px 18px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: var(--surface-strong);
    }}
    .card-label {{
      display: block;
      color: var(--ink-soft);
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .card strong {{
      display: block;
      margin-top: 0.5rem;
      font-size: 1rem;
      line-height: 1.5;
    }}
    .visual-block {{
      overflow-x: auto;
      margin: 1.1rem 0;
      border-radius: 18px;
    }}
    .visual-block svg {{
      max-width: 100%;
      height: auto;
      display: block;
    }}
    @media (max-width: 720px) {{
      .page {{ width: min(calc(100% - 20px), var(--max)); padding-top: 14px; }}
      .hero, .content {{ padding: 20px 18px; border-radius: 22px; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="eyebrow">{html_escape(pick_text(language, "下载阅读版", "Download Reading Layer"))}</div>
      <h1>{html_escape(title)}</h1>
      <p class="subtitle">{html_escape(subtitle)}</p>
      <nav class="nav">
        {"".join(nav_links)}
      </nav>
    </section>
    <section class="content">
      {body_html}
    </section>
    <p class="footer">{html_escape(footer_text)}</p>
  </main>
</body>
</html>
"""


def render_markdown_reading_page(
    markdown_text: str,
    *,
    source_path: Path,
    output_path: Path,
    company_dir: Path,
    language: str,
    state: dict[str, Any],
) -> str:
    title = source_path.stem
    subtitle = pick_text(
        language,
        "这是面向下载查看的阅读版页面，对应的 Markdown 工作文件仍保留在原工作区中。",
        "This is the download-friendly reading page. The original markdown working file remains in the workspace.",
    )
    body_html = markdown_to_html_fragment(
        markdown_text,
        source_path=source_path,
        output_path=output_path,
        company_dir=company_dir,
        language=language,
    )
    return render_reading_shell(
        title=title,
        subtitle=subtitle,
        body_html=body_html,
        language=language,
        company_name=state["company_name"],
        current_path=output_path,
        navigation_items=reading_navigation_items(company_dir, language),
    )


def _svg_text(value: Any) -> str:
    return html_escape(str(value), quote=True)


def build_business_loop_svg(state: dict[str, Any], language: str) -> str:
    offer = state.get("offer", {})
    product = state.get("product", {})
    delivery = state.get("delivery", {})
    cash = state.get("cash", {})
    learning = state.get("learning", {})
    assets = state.get("assets", {})
    labels = [
        (pick_text(language, "价值承诺", "Promise"), offer.get("promise", pick_text(language, "待补充", "To be added"))),
        (pick_text(language, "买家", "Buyer"), offer.get("target_customer", pick_text(language, "待确认", "To be confirmed"))),
        (pick_text(language, "产品能力", "Product"), ", ".join(product.get("core_capability", [])[:1]) or product.get("state", "idea")),
        (pick_text(language, "交付", "Delivery"), delivery.get("delivery_status", pick_text(language, "待启动", "Not started"))),
        (pick_text(language, "回款", "Cash"), cash.get("receivable", 0)),
        (pick_text(language, "学习", "Learning"), learning.get("latest_signal", pick_text(language, "待记录", "To be recorded"))),
        (pick_text(language, "资产", "Asset"), sum(len(assets.get(key, [])) for key in ("sops", "templates", "cases", "automations", "reusable_code"))),
    ]
    xs = [92, 250, 408, 566, 724, 882, 1040]
    cards = []
    arrows = []
    for index, ((title, body), x) in enumerate(zip(labels, xs)):
        cards.append(
            f'<g><rect x="{x}" y="92" width="126" height="92" rx="14" fill="#fffdf8" stroke="#d8c9b8"/>'
            f'<text x="{x + 14}" y="124" font-size="16" font-weight="700" fill="#1f1a14">{_svg_text(title)}</text>'
            f'<text x="{x + 14}" y="154" font-size="12" fill="#5f5448">{_svg_text(str(body)[:16])}</text></g>'
        )
        if index < len(xs) - 1:
            arrows.append(
                f'<path d="M{x + 132} 138 L{xs[index + 1] - 12} 138" stroke="#b85c38" stroke-width="3" marker-end="url(#arrow)"/>'
            )
    title = pick_text(language, "一人公司经营闭环", "One-Person Company Loop")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img">'
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" fill="#b85c38"/></marker></defs>'
        '<rect width="1200" height="320" rx="28" fill="#f6f3ec"/>'
        f'<text x="64" y="58" font-size="28" font-weight="800" fill="#1f1a14">{_svg_text(title)}</text>'
        f'{"".join(arrows)}{"".join(cards)}'
        '</svg>'
    )


def build_pipeline_svg(state: dict[str, Any], language: str) -> str:
    summary = state.get("pipeline", {}).get("stage_summary", {})
    stages = [
        ("discovering", pick_text(language, "发现", "Discovering")),
        ("talking", pick_text(language, "对话", "Talking")),
        ("trial", pick_text(language, "试用", "Trial")),
        ("proposal", pick_text(language, "报价", "Proposal")),
        ("won", pick_text(language, "成交", "Won")),
    ]
    max_value = max([int(summary.get(key, 0) or 0) for key, _ in stages] + [1])
    rows = []
    for index, (key, label) in enumerate(stages):
        value = int(summary.get(key, 0) or 0)
        width = 50 + int((value / max_value) * 620)
        y = 78 + index * 48
        rows.append(
            f'<text x="56" y="{y + 18}" font-size="16" fill="#1f1a14">{_svg_text(label)}</text>'
            f'<rect x="190" y="{y}" width="{width}" height="24" rx="12" fill="#2f7d5b"/>'
            f'<text x="{205 + width}" y="{y + 18}" font-size="15" fill="#5f5448">{value}</text>'
        )
    title = pick_text(language, "成交管道", "Revenue Pipeline")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360" role="img">'
        '<rect width="900" height="360" rx="28" fill="#fffdf8" stroke="#d8c9b8"/>'
        f'<text x="56" y="44" font-size="26" font-weight="800" fill="#1f1a14">{_svg_text(title)}</text>'
        f'{"".join(rows)}</svg>'
    )


def render_visual_kit(company_dir: Path, state: dict[str, Any]) -> None:
    language = state["language"]
    visual_dir = workspace_dir_path(company_dir, "visual_kit", language)
    visual_dir.mkdir(parents=True, exist_ok=True)
    write_text(visual_dir / "business-loop.svg", build_business_loop_svg(state, language))
    write_text(visual_dir / "revenue-pipeline.svg", build_pipeline_svg(state, language))
    prompt_title = pick_text(language, "# AI 图片创作提示词", "# AI Image Creative Prompts")
    hero_prompt = pick_text(
        language,
        "为 One Person Company OS 生成一张宣发封面：一个单人创始人在安静的工作台前，通过可视化经营驾驶舱同时看到价值承诺、买家、产品、交付、回款和资产。风格专业、清晰、有现代软件产品感，不包含虚构品牌标志，不承载具体经营数字。",
        "Create a promotional cover for One Person Company OS: a solo founder at a focused workstation, looking at a visual operating cockpit that connects promise, buyer, product, delivery, cash, and assets. Professional modern software-product style, no fake brand logos, no precise operating numbers.",
    )
    social_prompt = pick_text(
        language,
        "生成一张社媒配图：中心是一条清晰的经营闭环路径，周围是产品、成交、交付、回款和资产的抽象界面片段。画面直观、有趣但不花哨，适合 GitHub/ClawHub 发布。",
        "Create a social image: a clear operating loop in the center, surrounded by abstract product, sales, delivery, cash, and asset interface fragments. Direct, interesting, restrained, suitable for GitHub and ClawHub launch posts.",
    )
    write_text(
        visual_dir / "ai-image-prompts.md",
        "\n".join(
            [
                prompt_title,
                "",
                pick_text(language, "## 宣发封面", "## Promotional Cover"),
                "",
                hero_prompt,
                "",
                pick_text(language, "## 社媒配图", "## Social Image"),
                "",
                social_prompt,
                "",
                pick_text(language, "说明：AI 图片只用于可选创作层，不承载精确经营数据；精确数据图使用本目录 SVG。", "Note: AI images are optional creative assets and should not carry precise operating data; use the SVG files in this directory for exact visuals."),
                "",
            ]
        ),
    )


def build_reading_start_page(state: dict[str, Any], company_dir: Path) -> str:
    language = state["language"]
    focus = state["focus"]
    offer = state["offer"]
    product = state["product"]
    delivery = state["delivery"]
    cash = state["cash"]
    pipeline_svg = build_pipeline_svg(state, language)
    loop_svg = build_business_loop_svg(state, language)
    body_parts = [
        '<div class="visual-block">',
        loop_svg,
        "</div>",
        "<div class=\"card-grid\">",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '当前主目标', 'Primary Goal'))}</span><strong>{html_escape(focus['primary_goal'])}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '当前主瓶颈', 'Primary Bottleneck'))}</span><strong>{html_escape(focus['primary_bottleneck'])}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '当前主战场', 'Primary Arena'))}</span><strong>{html_escape(primary_arena_label(focus['primary_arena'], language))}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '今天最短动作', 'Shortest Action Today'))}</span><strong>{html_escape(focus['today_action'])}</strong></article>",
        "</div>",
        f"<h2>{html_escape(pick_text(language, '当前成交图', 'Current Revenue Picture'))}</h2>",
        '<div class="visual-block">',
        pipeline_svg,
        "</div>",
        f"<h2>{html_escape(pick_text(language, '下载后先怎么用', 'How To Use This Download'))}</h2>",
        "<ul>",
        f"<li>{html_escape(pick_text(language, '先从本页进入阅读版主工作面，快速理解当前经营状态。', 'Start from this page to open the reading layer and understand the current business state quickly.'))}</li>",
        f"<li>{html_escape(pick_text(language, '如果只是查看，优先打开 HTML；如果要继续协作和更新，再回到原始 Markdown。', 'If you only want to review the workspace, open the HTML pages first. Return to the original markdown files when you need to keep editing or collaborating.'))}</li>",
        f"<li>{html_escape(pick_text(language, '正式对外交付请看产物目录里的 DOCX 文件。', 'For formal external deliverables, use the DOCX files under the artifacts directory.'))}</li>",
        "</ul>",
        f"<h2>{html_escape(pick_text(language, '当前经营闭环', 'Current Business Loop'))}</h2>",
        "<div class=\"card-grid\">",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '价值承诺', 'Promise'))}</span><strong>{html_escape(offer['promise'])}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '买家', 'Buyer'))}</span><strong>{html_escape(offer['target_customer'])}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '产品能力', 'Product Capability'))}</span><strong>{html_escape(', '.join(product.get('core_capability', [])[:2]) or pick_text(language, '待补充', 'Add the core capability'))}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '交付', 'Delivery'))}</span><strong>{html_escape(delivery['delivery_status'])}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '回款', 'Cash Collection'))}</span><strong>{html_escape(str(cash['receivable']))}</strong></article>",
        f"<article class=\"card\"><span class=\"card-label\">{html_escape(pick_text(language, '学习与资产', 'Learning And Assets'))}</span><strong>{html_escape(state['focus']['week_outcome'])}</strong></article>",
        "</div>",
        f"<h2>{html_escape(pick_text(language, '推荐先看的页面', 'Open These Pages First'))}</h2>",
        "<ul>",
    ]
    preferred_keys = (
        "dashboard",
        "offer",
        "pipeline",
        "product_status",
        "delivery_cash",
        "cash_health",
        "assets_automation",
    )
    for key in preferred_keys:
        source = root_doc_path(company_dir, key, language)
        target = reading_export_path(company_dir, source, language)
        href = relative_href(target, reading_entry_path(company_dir, language).parent)
        body_parts.append(
            f"<li><a href=\"{html_escape(href, quote=True)}\">{html_escape(source.stem)}</a></li>"
        )
    deliverables_source = workspace_file_path(company_dir, "delivery_directory", language)
    deliverables_target = reading_export_path(company_dir, deliverables_source, language)
    deliverables_href = relative_href(deliverables_target, reading_entry_path(company_dir, language).parent)
    body_parts.extend(
        [
            f"<li><a href=\"{html_escape(deliverables_href, quote=True)}\">{html_escape(deliverables_source.stem)}</a></li>",
            "</ul>",
            f"<h2>{html_escape(pick_text(language, '文件分层说明', 'Output Layer Guide'))}</h2>",
            "<ul>",
            f"<li>{html_escape(pick_text(language, '阅读版 HTML：适合下载后直接双击查看。', 'Reading HTML: open these first after download.'))}</li>",
            f"<li>{html_escape(pick_text(language, '工作层 Markdown：适合继续修改、追踪和协作。', 'Working markdown: keep using these for editing, tracking, and collaboration.'))}</li>",
            f"<li>{html_escape(pick_text(language, '正式交付 DOCX：适合发给客户、合作方或归档。', 'Formal DOCX deliverables: use these for customers, collaborators, or archival handoff.'))}</li>",
            "</ul>",
        ]
    )
    return render_reading_shell(
        title=pick_text(language, "经营驾驶舱", "Operating Cockpit"),
        subtitle=pick_text(
            language,
            "这是下载后的经营驾驶舱。先看懂当前闭环、主瓶颈和下一步动作，再继续推进。",
            "This is the operating cockpit after download. Understand the loop, bottleneck, and next action before editing anything.",
        ),
        body_html="\n".join(body_parts),
        language=language,
        company_name=state["company_name"],
        current_path=reading_entry_path(company_dir, language),
        navigation_items=reading_navigation_items(company_dir, language),
    )


def render_reading_exports(company_dir: Path, state: dict[str, Any]) -> None:
    language = state["language"]
    reading_dir_path(company_dir, language).mkdir(parents=True, exist_ok=True)
    for source_path in reading_source_paths(company_dir, language):
        if not source_path.is_file() or source_path.suffix.lower() != ".md":
            continue
        output_path = reading_export_path(company_dir, source_path, language)
        html_text = render_markdown_reading_page(
            source_path.read_text(encoding="utf-8"),
            source_path=source_path,
            output_path=output_path,
            company_dir=company_dir,
            language=language,
            state=state,
        )
        write_text(output_path, html_text)
    write_text(reading_entry_path(company_dir, language), build_reading_start_page(state, company_dir))


def artifact_status_summary_markdown(company_dir: Path, language: str) -> str:
    category_names = {
        "delivery": pick_text(language, "实际交付", "Actual Deliverables"),
        "software": pick_text(language, "软件与代码", "Software And Code"),
        "business": pick_text(language, "非软件与业务", "Non-Software And Business"),
        "ops": pick_text(language, "部署与生产", "Deployment And Production"),
        "growth": pick_text(language, "上线与增长", "Launch And Growth"),
    }
    lines = [
        pick_text(language, "# 交付目录总览", "# Deliverable Directory Overview"),
        "",
        f"{pick_text(language, '更新于', 'Updated At')}: {now_string()}",
        "",
        pick_text(
            language,
            "- 这里列的是当前工作区内已经落盘的正式交付文档，以及每份文档当前的成熟度。",
            "- This page lists the formal deliverable documents already written into the workspace and the current maturity of each one.",
        ),
        pick_text(
            language,
            "- 文件名直接使用最终交付名，不再额外写 `[待生成]` 或 `[已生成]`。",
            "- File names use the final deliverable name directly instead of carrying `[待生成]` or `[已生成]` markers.",
        ),
        "",
    ]

    for category, label in category_names.items():
        lines.extend([f"## {label}", ""])
        artifact_dir = artifact_dir_path(company_dir, category, language)
        entries = []
        if artifact_dir.is_dir():
            for path in sorted(artifact_dir.glob("*.docx")):
                status_text = artifact_maturity_label(path, language)
                entries.append(
                    pick_text(
                        language,
                        f"- {path.name} | 文档成熟度: {status_text} | 路径: {display_path(path, company_dir)}",
                        f"- {path.name} | Document Maturity: {status_text} | Path: {display_path(path, company_dir)}",
                    )
                )
        if not entries:
            entries.append(pick_text(language, "- 当前目录还没有 DOCX 文件。", "- No DOCX files exist in this directory yet."))
        lines.extend(entries)
        lines.append("")

    lines.extend(
        [
            pick_text(language, "## 使用方式", "## How To Use"),
            "",
            pick_text(language, "- 先打开本文件看清当前有哪些正式件，再进入对应目录直接补齐内容。", "- Open this file first to see the formal documents that already exist, then continue refining the matching files directly."),
            pick_text(language, "- 如果文件名、顺序或内容边界不合适，直接告诉我你要怎么改，我会继续收口。", "- If the file names, ordering, or scope feel wrong, tell me what to adjust and I will tighten the system further."),
            "",
        ]
    )
    return "\n".join(lines)


def render_workspace(company_dir: Path, state: dict[str, Any]) -> None:
    role_specs = load_role_specs()
    language = normalize_language(state.get("language"), state.get("company_name"), state.get("product_name"))
    state["language"] = language
    state = sync_legacy_fields(state)
    harmonize_workspace_layout(company_dir, language)
    ensure_workspace_dirs(company_dir, language)

    legacy_root_dir = workspace_dir_path(company_dir, "legacy_root", language)
    legacy_root_dir.mkdir(parents=True, exist_ok=True)
    for legacy_name in [
        "00-公司总览.md",
        "01-产品定位.md",
        "02-当前阶段.md",
        "03-组织架构.md",
        "04-当前回合.md",
        "05-推进规则.md",
        "06-触发器与校准规则.md",
        "07-文档产物规范.md",
        "07-交付物地图.md",
        "08-阶段角色与交付矩阵.md",
        "09-当前阶段交付要求.md",
        "10-创始人启动卡.md",
        "11-交付状态总览.md",
        "11-交付目录总览.md",
        "12-AI时代快循环.md",
    ]:
        legacy_path = company_dir / legacy_name
        if legacy_path.exists():
            target = legacy_root_dir / legacy_name
            if target.exists():
                legacy_path.unlink()
            else:
                legacy_path.rename(target)

    artifact_dir = workspace_dir_path(company_dir, "artifacts_root", language)
    if artifact_dir.is_dir():
        for path in sorted(artifact_dir.rglob("*.docx")):
            parsed = parse_planned_docx_name(path.name)
            if not parsed or parsed.get("legacy_status") is None:
                continue
            desired = path.with_name(f"{parsed['index']:02d}-{parsed['title']}.docx")
            if desired.exists():
                path.unlink()
            else:
                path.rename(desired)

    focus = state.get("focus", {})
    offer = state.get("offer", {})
    stage_label_text = pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop")
    stage_goal = focus.get("primary_goal", pick_text(language, "先跑通最小价值闭环", "Run the smallest value loop first"))
    active_roles = state.get("active_roles") or ["founder-ceo", "control-tower", "product-strategist"]
    active_display = role_display_names(active_roles, role_specs, language)
    available_display = [
        localized_role_spec(spec, language)["display_name"]
        for role_id, spec in sorted(role_specs.items())
        if role_id not in active_roles
    ]
    round_name = pick_text(language, "经营推进", "Operating Push")
    round_next_action = focus.get("today_action", pick_text(language, "待定义", "Undefined"))

    common_values = {
        "LANGUAGE": language,
        "COMPANY_NAME": state["company_name"],
        "PRODUCT_NAME": state["product_name"],
        "STAGE_LABEL": stage_label_text,
        "UPDATED_AT": now_string(),
        "COMPANY_GOAL": stage_goal,
        "CURRENT_BOTTLENECK": focus.get("primary_bottleneck", pick_text(language, "待识别", "To be identified")),
        "CURRENT_ROUND_NAME": round_name,
        "CURRENT_NEXT_ACTION": round_next_action,
        "TARGET_USER": offer.get("target_customer", pick_text(language, "待确认", "To be confirmed")),
        "CORE_PROBLEM": offer.get("scenario", pick_text(language, "待确认", "To be confirmed")),
        "PRODUCT_PITCH": offer.get("promise", pick_text(language, "待补充", "To be added")),
        "STAGE_GOAL": stage_goal,
        "STAGE_EXIT_CRITERIA": pick_text(language, "价值、买家、产品、交付、回款和资产至少向前推进一格。", "Move promise, buyer, product, delivery, cash, and assets forward by at least one step."),
        "NEXT_STAGE_REQUIREMENTS": pick_text(language, "v1.0 不再使用阶段切换；只看当前主瓶颈和下一步经营动作。", "v1.0 no longer uses stage transitions; use the current bottleneck and next operating action."),
        "STAGE_RISKS": format_list(state.get("risk", {}).get("top_risks", []), language),
        "CURRENT_STAGE_REQUIRED_OUTPUTS": format_list(
            [
                pick_text(language, "经营驾驶舱", "Operating cockpit"),
                pick_text(language, "可编辑工作底稿", "Editable working surfaces"),
                pick_text(language, "正式交付 DOCX", "Formal DOCX deliverables"),
            ],
            language,
        ),
        "ACTIVE_ROLE_LIST": format_list(active_display, language),
        "AVAILABLE_ROLE_LIST": format_list(available_display, language),
        "ACTIVE_ROLE_INLINE": ("、".join(active_display) if language == "zh-CN" else ", ".join(active_display)) or pick_text(language, "无", "None"),
    }

    write_text(root_doc_path(company_dir, "dashboard", language), build_operating_dashboard(state, company_dir))
    write_text(root_doc_path(company_dir, "founder_constraints", language), build_founder_constraints_doc(state))
    write_text(root_doc_path(company_dir, "offer", language), build_offer_doc(state))
    write_text(root_doc_path(company_dir, "pipeline", language), build_pipeline_doc(state))
    write_text(root_doc_path(company_dir, "product_status", language), build_product_doc(state))
    write_text(root_doc_path(company_dir, "delivery_cash", language), build_delivery_doc(state))
    write_text(root_doc_path(company_dir, "cash_health", language), build_cash_doc(state))
    write_text(root_doc_path(company_dir, "assets_automation", language), build_asset_doc(state))
    write_text(root_doc_path(company_dir, "risks", language), build_risk_doc(state))
    write_text(root_doc_path(company_dir, "week_focus", language), build_week_focus_doc(state))
    write_text(root_doc_path(company_dir, "today_action", language), build_today_action_doc(state))
    write_text_if_missing(root_doc_path(company_dir, "collaboration_memory", language), build_collaboration_memory_doc(state))
    write_text_if_missing(root_doc_path(company_dir, "session_handoff", language), build_session_handoff_doc(state))

    write_text(workspace_file_path(company_dir, "record_snapshot", language), build_operating_dashboard(state, company_dir))
    write_text(workspace_file_path(company_dir, "sales_actions", language), build_sales_action_doc(state))
    write_text(workspace_file_path(company_dir, "sales_landing", language), build_landing_copy_doc(state))
    write_text(workspace_file_path(company_dir, "sales_interview", language), build_interview_sprint_doc(state))
    write_text(workspace_file_path(company_dir, "sales_trial_application", language), build_trial_application_doc(state))
    write_text(workspace_file_path(company_dir, "product_checklist", language), build_mvp_checklist_doc(state))
    write_text(workspace_file_path(company_dir, "product_demo_index", language), build_demo_html(state))
    write_text(workspace_file_path(company_dir, "delivery_tracker", language), build_delivery_doc(state))
    write_text(workspace_file_path(company_dir, "delivery_feedback", language), build_trial_feedback_doc(state))
    write_text(workspace_file_path(company_dir, "ops_launch_checklist", language), build_launch_checklist_doc(state))
    write_text(workspace_file_path(company_dir, "assets_inventory", language), build_asset_doc(state))
    write_text(
        workspace_file_path(company_dir, "automation_notes", language),
        "\n".join(
            [
                pick_text(language, "# 状态说明", "# State Notes"),
                "",
                f"- {pick_text(language, '主状态文件', 'Primary State File')}: {display_path(state_path(company_dir), company_dir)}",
                f"- {pick_text(language, '当前主战场', 'Current Primary Arena')}: {primary_arena_label(state['focus']['primary_arena'], language)}",
                f"- {pick_text(language, '今天最短动作', 'Shortest Action Today')}: {state['focus']['today_action']}",
                "",
            ]
        )
        + "\n",
    )

    write_text(workspace_file_path(company_dir, "role_index", language), render_template("role-index-template.md", common_values))
    for role_id in active_roles:
        spec = role_spec(role_id, role_specs, language)
        role_values = {
            "LANGUAGE": language,
            "ROLE_NAME": spec["display_name"],
            "ROLE_MISSION": spec["mission"],
            "ROLE_OWNS": format_list(spec["owns"], language),
            "ROLE_INPUTS": format_list(spec["inputs_required"], language),
            "ROLE_OUTPUTS": format_list(spec["outputs_required"], language),
            "ROLE_GUARDRAILS": format_list(spec["do_not_do"], language),
            "ROLE_APPROVALS": format_list(spec["approval_required_for"], language),
            "ROLE_HANDOFFS": format_list(role_display_names(spec["handoff_to"], role_specs, language), language),
        }
        filename = spec.get("workspace_filename", spec["display_name"])
        target_role_path = role_brief_path(company_dir, filename, language)
        write_text(target_role_path, render_template("role-brief-template.md", role_values))
        for other_language in ("zh-CN", "en-US"):
            other_spec = role_spec(role_id, role_specs, other_language)
            other_filename = other_spec.get("workspace_filename", other_spec["display_name"])
            other_path = role_brief_path(company_dir, other_filename, other_language)
            if other_path != target_role_path and other_path.exists():
                other_path.unlink()

    write_text(workspace_file_path(company_dir, "flow_bootstrap", language), render_template("bootstrap-flow-template.md", common_values))
    for old_flow_key in ("flow_round", "flow_calibration", "flow_stage"):
        old_flow_path = workspace_file_path(company_dir, old_flow_key, language)
        if old_flow_path.exists():
            old_flow_path.unlink()
    write_text(workspace_file_path(company_dir, "automation_reminders", language), render_template("reminder-rules-template.md", common_values))
    write_text(workspace_file_path(company_dir, "automation_scheduler", language), render_template("scheduler-spec-template.md", common_values))

    for spec in stage_artifact_specs("build", language):
        output_dir = artifact_dir_path(company_dir, spec["category"], language)
        output_path = ensure_planned_docx_path(output_dir, int(spec["index"]), spec["title"], completed=False)
        docx_values = {
            **artifact_template_values(common_values, state),
            "ARTIFACT_TITLE": spec["title"],
            "ARTIFACT_STATUS": pick_text(language, "起始版", "Starter Formal Doc"),
            "ARTIFACT_PROGRESS_SUMMARY": pick_text(language, "当前已经生成正式文档起始版，可直接在本文件继续补齐真实内容、证据和验收结论。", "A starter formal document has been created. Continue filling in the real content, evidence, and acceptance result in this file directly."),
            "ARTIFACT_FILE_PATH": display_path(output_path, company_dir),
        }
        rendered = render_template(spec["template"], docx_values)
        write_docx(output_path, rendered, title=spec["title"])

    write_text(workspace_file_path(company_dir, "delivery_directory", language), artifact_status_summary_markdown(company_dir, language))
    render_visual_kit(company_dir, state)
    render_reading_exports(company_dir, state)
