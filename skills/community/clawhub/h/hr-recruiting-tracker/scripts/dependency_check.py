#!/usr/bin/env python3
"""检查 hr-recruiting-tracker 工作流所需的能力。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import resume_extract  # noqa: E402


@dataclass
class Check:
    name: str
    available: bool
    detail: str
    required: bool = False


def has_module(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def find_command(command_name: str) -> str | None:
    found = shutil.which(command_name)
    if found:
        return found
    user_local = Path.home() / ".local" / "bin" / command_name
    if user_local.exists() and user_local.is_file():
        return str(user_local)
    return None


def command_runs(command_name: str, *args: str, timeout_seconds: int = 30) -> tuple[bool, str]:
    command = find_command(command_name)
    if not command:
        return False, f"未找到命令：{command_name}"
    try:
        proc = subprocess.run(
            [command, *args],
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except Exception as exc:
        return False, f"{command} 启动失败：{exc}"
    output = (proc.stdout or proc.stderr or "").strip().splitlines()
    detail = output[0] if output else command
    return proc.returncode == 0, detail


def availability_detail(label: str, available: bool) -> str:
    return f"{label} 可用" if available else f"{label} 未安装"


def find_tencent_docs_skill_dir() -> Path | None:
    """Locate the tencent-docs skill without assuming a single deployment root."""
    candidates = []
    env_path = os_environ_get("TENCENT_DOCS_SKILL_DIR")
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates.extend(
        [
            SKILL_DIR.parent / "tencent-docs",
            Path.home() / ".openclaw" / "workspace" / "skills" / "tencent-docs",
            Path.home() / ".codex" / "skills" / "tencent-docs",
        ]
    )
    for candidate in candidates:
        if (candidate / "SKILL.md").exists():
            return candidate
    return None


def os_environ_get(name: str) -> str | None:
    import os

    value = os.environ.get(name)
    return value or None


def build_resume_ingest_checks() -> list[Check]:
    docling_cli_ready, docling_cli_detail = command_runs("docling", "--version")
    pypdf_ready = has_module("pypdf")
    pypdf2_ready = has_module("PyPDF2")
    pymupdf_ready = has_module("fitz")
    pdftotext_ready = find_command("pdftotext") is not None
    fallback_pdf = pypdf_ready or pypdf2_ready or pymupdf_ready or pdftotext_ready
    fallback_docx = has_module("docx")
    docling_python_ready = has_module("docling")
    checks = [
        Check("python.version", sys.version_info >= (3, 9), platform.python_version(), required=True),
        Check("plain_text", True, "内置 TXT/Markdown 读取器", required=True),
        Check(
            "fallback.pdf_text",
            fallback_pdf,
            "pypdf / PyPDF2 / PyMuPDF / pdftotext 任一可用" if fallback_pdf else "pypdf / PyPDF2 / PyMuPDF / pdftotext 均未安装",
        ),
        Check("fallback.docx_text", fallback_docx, availability_detail("python-docx", fallback_docx)),
        Check("docling.python_import", docling_python_ready, availability_detail("Python 包 docling", docling_python_ready)),
        Check("docling.cli_startup", docling_cli_ready, docling_cli_detail),
        Check(
            "docling.pdf_conversion",
            False,
            "未探测真实 PDF 转换；使用 --probe-file <pdf> --probe-parser docling 验证。",
        ),
        Check("pypdf.python", pypdf_ready, availability_detail("回退 PDF 文本提取器 pypdf", pypdf_ready)),
        Check("pymupdf.python", pymupdf_ready, availability_detail("回退 PDF 文本提取器 PyMuPDF/fitz", pymupdf_ready)),
        Check("pypdf2.python", pypdf2_ready, availability_detail("回退 PDF 文本提取器 PyPDF2", pypdf2_ready)),
        Check("pdftotext.cli", pdftotext_ready, availability_detail("回退 PDF 文本提取器 pdftotext", pdftotext_ready)),
        Check("python-docx.python", fallback_docx, availability_detail("回退 DOCX 文本提取器 python-docx", fallback_docx)),
    ]
    checks.append(
        Check(
            "resume.parse",
            True,
            "该工作流至少可解析 TXT/Markdown；PDF/DOCX 能力见 fallback/docling 检查。",
            required=True,
        )
    )
    return checks


def probe_file(path: Path, parser: str) -> dict[str, Any]:
    started_at = resume_extract.utc_now()
    try:
        result = resume_extract.extract_resume(path, parser=parser, allow_model_downloads=(parser == "docling"))
        markdown = resume_extract.normalize_text(result.markdown) + "\n"
        stats = resume_extract.compute_text_stats(markdown, result.raw, path.suffix.lower())
        return {
            "status": "succeeded",
            "started_at": started_at,
            "finished_at": resume_extract.utc_now(),
            "parser": result.parser,
            "quality": result.quality,
            "warnings": result.warnings,
            "parser_attempts": [asdict(attempt) for attempt in result.parser_attempts],
            "text_stats": asdict(stats),
        }
    except resume_extract.ExtractionError as exc:
        return {
            "status": "failed",
            "started_at": started_at,
            "finished_at": resume_extract.utc_now(),
            "parser": None,
            "quality": "unavailable",
            "error": resume_extract.truncate_detail(str(exc)),
            "parser_attempts": [asdict(attempt) for attempt in exc.parser_attempts],
        }
    except Exception as exc:
        return {
            "status": "failed",
            "started_at": started_at,
            "finished_at": resume_extract.utc_now(),
            "parser": None,
            "quality": "unavailable",
            "error": resume_extract.truncate_detail(str(exc)),
            "parser_attempts": [],
        }


def quality_from_checks(checks: list[Check], probe: dict[str, Any] | None) -> str:
    if probe:
        return str(probe.get("quality", "unavailable"))
    by_name = {check.name: check.available for check in checks}
    if by_name.get("fallback.pdf_text") or by_name.get("fallback.docx_text"):
        return "fallback"
    return "text-only"


def build_candidate_upload_checks(probe_remote: bool = False) -> list[Check]:
    mcporter_ready = shutil.which("mcporter") is not None
    tencent_docs_skill_dir = find_tencent_docs_skill_dir()
    tencent_docs_skill_ready = tencent_docs_skill_dir is not None
    tencent_docs_ready = False
    tencent_docs_detail = "未远程探测；使用 --probe-remote 验证腾讯文档 MCP 和授权。"
    if mcporter_ready and probe_remote:
        try:
            proc = subprocess.run(
                ["mcporter", "call", "tencent-docs", "smartsheet.list_tables",
                 "--args", '{"file_id":"_check_"}'],
                text=True, capture_output=True, timeout=15, check=False,
            )
            combined = proc.stdout + proc.stderr
            if "400006" in combined:
                tencent_docs_detail = "MCP 可达但 Token 鉴权失败（需授权）"
            elif "code:40" in combined:
                # 40xxxx = 腾讯文档业务错误码（非鉴权），说明认证已通过
                import re
                match = re.search(r"code:(\d+)", combined)
                code = match.group(1) if match else "unknown"
                tencent_docs_ready = True
                tencent_docs_detail = f"MCP 已认证（业务错误 {code}，测试用 file_id 不存在属正常）"
            elif "trace_id" in combined:
                # 有 trace_id 说明服务端已处理请求
                tencent_docs_ready = True
                tencent_docs_detail = "MCP 已认证"
            else:
                tencent_docs_detail = f"MCP 响应异常: {(proc.stderr or proc.stdout)[:200]}"
        except Exception as exc:
            tencent_docs_detail = f"检测异常: {exc}"

    checks = [
        Check(
            "tencent_docs.skill",
            tencent_docs_skill_ready,
            str(tencent_docs_skill_dir) if tencent_docs_skill_dir else "未找到 tencent-docs skill；可用 openclaw skills install 或当前 registry 安装",
            required=True,
        ),
        Check("mcporter.cli", mcporter_ready, shutil.which("mcporter") or "未安装", required=True),
        Check("tencent_docs.mcp", tencent_docs_ready, tencent_docs_detail, required=probe_remote),
        Check(
            "tencent_docs.auth",
            tencent_docs_ready,
            "已授权" if tencent_docs_ready else ("需运行 tdoc_check_and_start_auth" if probe_remote else "未远程探测"),
            required=probe_remote,
        ),
    ]
    return checks


def build_payload(
    workflow: str,
    probe_path: Path | None = None,
    probe_parser: str = "auto",
    probe_remote: bool = False,
) -> dict[str, Any]:
    if workflow in {"candidate-upload", "job-management"}:
        checks = build_candidate_upload_checks(probe_remote=probe_remote)
        probe = None  # 腾讯文档写入类工作流不需要文件探测
    else:
        checks = build_resume_ingest_checks()
        probe = probe_file(probe_path, probe_parser) if probe_path else None
        if probe and probe.get("parser") in {"docling-python", "docling-cli"}:
            checks = [
                Check("docling.pdf_conversion", True, "真实文件 Docling 转换成功")
                if check.name == "docling.pdf_conversion"
                else check
                for check in checks
            ]

    required_missing = [check.name for check in checks if check.required and not check.available]
    quality = quality_from_checks(checks, probe) if workflow == "resume-ingest" else "not-applicable"
    return {
        "workflow": workflow,
        "ready": not required_missing,
        "quality": quality,
        "checks": [asdict(check) for check in checks],
        "probe": probe,
        "missing_required": required_missing,
    }


def render_text(payload: dict[str, Any]) -> None:
    print(f"工作流：{payload['workflow']}")
    for check in payload["checks"]:
        marker = "OK" if check["available"] else ("MISS" if check["required"] else "WARN")
        required = "必需" if check["required"] else "可选"
        print(f"[{marker}] {check['name']} ({required}) - {check['detail']}")

    probe = payload.get("probe")
    if probe:
        print("\n真实文件探测：")
        print(f"- status: {probe['status']}")
        print(f"- parser: {probe.get('parser')}")
        print(f"- quality: {probe.get('quality')}")
        if probe.get("error"):
            print(f"- error: {probe['error']}")

    if payload["missing_required"]:
        print("\n缺失必需能力：")
        for name in payload["missing_required"]:
            print(f"- {name}")
    elif payload["workflow"] == "resume-ingest" and payload["quality"] != "high":
        print("\n当前默认质量不是 high。PDF/DOCX 可走本地回退解析，写入候选人库前需要 HR 审核。")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workflow",
        default="resume-ingest",
        choices=["resume-ingest", "candidate-upload", "job-management"],
        help="要检查的工作流能力组。",
    )
    parser.add_argument("--probe-file", help="可选：用真实文件做非破坏性解析探测。")
    parser.add_argument("--probe-remote", action="store_true", help="对腾讯文档写入类工作流执行 MCP 远程授权探测。")
    parser.add_argument(
        "--probe-parser",
        default="auto",
        choices=["auto", "local", "docling"],
        help="真实文件探测使用的解析器策略。",
    )
    parser.add_argument("--json", action="store_true", help="打印机器可读的 JSON。")
    args = parser.parse_args()

    probe_path = Path(args.probe_file).expanduser().resolve() if args.probe_file else None
    if probe_path and not probe_path.exists():
        print(f"探测文件不存在：{probe_path}", file=sys.stderr)
        return 2

    payload = build_payload(
        args.workflow,
        probe_path=probe_path,
        probe_parser=args.probe_parser,
        probe_remote=args.probe_remote,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        render_text(payload)

    return 0 if payload["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
