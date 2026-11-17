"""Small artifact CLI for payloads that should not cross the MCP context."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from .client import get, post, post_files, require_token
from .import_contract import (
    IMPORT_REVIEW_SCHEMA_VERSION,
    normalize_import_review_items,
)
from .validation import (
    MAX_IMAGE_SIZE,
    MAX_UPLOAD_FILES,
    MAX_UPLOAD_TOTAL_SIZE,
    summarize_import_items,
    validate_fund_code,
    validate_image_file,
)


class _JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(f"参数错误：{message}")


def _write_json(path_value: str, payload: Any) -> Path:
    path = Path(path_value).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(encoded)
        temporary.replace(path)
    except Exception:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise
    return path


def _read_json(path_value: str) -> Any:
    path = Path(path_value).expanduser().resolve()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"文件不存在：{path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 文件格式无效：{path}（{exc.msg}）") from None


def _read_images(path_values: list[str]) -> list[tuple[str, bytes, str]]:
    if not path_values or len(path_values) > MAX_UPLOAD_FILES:
        raise ValueError(f"请提供 1-{MAX_UPLOAD_FILES} 张图片")
    files = []
    total_size = 0
    declared_total_size = 0
    for path_value in path_values:
        path = Path(path_value).expanduser().resolve()
        try:
            declared_size = path.stat().st_size
        except FileNotFoundError:
            raise ValueError(f"图片不存在：{path}") from None
        if declared_size > MAX_IMAGE_SIZE:
            raise ValueError(
                f"图片文件过大：{declared_size / 1024 / 1024:.1f}MB，最大允许 10MB"
            )
        declared_total_size += declared_size
        if declared_total_size > MAX_UPLOAD_TOTAL_SIZE:
            raise ValueError("单次上传图片总大小不能超过 50MB")
        try:
            content = path.read_bytes()
        except FileNotFoundError:
            raise ValueError(f"图片不存在：{path}") from None
        mime = validate_image_file(path.name, content, "")
        total_size += len(content)
        if total_size > MAX_UPLOAD_TOTAL_SIZE:
            raise ValueError("单次上传图片总大小不能超过 50MB")
        files.append((path.name, content, mime))
    return files


async def _doctor(_args: argparse.Namespace) -> dict:
    require_token()
    user, version = await asyncio.gather(get("/api/auth/me"), get("/api/version"))
    return {
        "status": "ok",
        "api": "reachable",
        "user": {
            "uid": user.get("uid") if isinstance(user, dict) else None,
            "nickname": user.get("nickname") if isinstance(user, dict) else None,
        },
        "appVersion": version.get("version") if isinstance(version, dict) else None,
    }


async def _import_screenshots(args: argparse.Namespace) -> dict:
    input_paths = {Path(value).expanduser().resolve() for value in args.file}
    result_path = Path(args.result).expanduser().resolve()
    if result_path in input_paths:
        raise ValueError("--result 不能与输入截图使用同一路径")
    require_token()
    files = _read_images(args.file)
    import_type = args.type.upper()
    if import_type == "TRANSACTIONS":
        raw = await post_files("/api/import_transactions", files)
    else:
        mode = "watchlist" if import_type == "WATCHLIST" else "holdings"
        raw = await post_files("/api/import_screenshot", files, form_data={"mode": mode})
    items = raw if isinstance(raw, list) else []
    result = {
        "schema_version": IMPORT_REVIEW_SCHEMA_VERSION,
        "import_type": import_type,
        "source_kind": "screenshot",
        "items": items,
    }
    output = _write_json(args.result, result)
    return {
        "status": "recognized",
        "result_file": str(output),
        "summary": summarize_import_items(items),
        "next_step": "检查未匹配项后运行 huahua import review；当前尚未写入 App。",
    }


async def _import_review(args: argparse.Namespace) -> dict:
    require_token()
    raw = _read_json(args.input)
    schema_version = str(raw.get("schema_version") or "").strip() if isinstance(raw, dict) else ""
    if schema_version and schema_version != IMPORT_REVIEW_SCHEMA_VERSION:
        raise ValueError(
            f"不支持的结果文件 schema_version：{schema_version}；"
            f"当前仅支持 {IMPORT_REVIEW_SCHEMA_VERSION}"
        )
    items = raw.get("items") if isinstance(raw, dict) else raw
    requested_type = args.type.upper()
    file_type = str(raw.get("import_type") or "").strip().upper() if isinstance(raw, dict) else ""
    if file_type and file_type != requested_type:
        raise ValueError(f"结果文件类型为 {file_type}，不能按 {requested_type} 提交")
    normalized_type, normalized_items = normalize_import_review_items(requested_type, items)
    source_kind = str(raw.get("source_kind") or "file").strip().lower() if isinstance(raw, dict) else "file"
    if source_kind not in {"text", "table", "json", "screenshot", "file"}:
        raise ValueError("结果文件 source_kind 无效")
    body = {
        "import_type": normalized_type,
        "source_kind": source_kind,
        "source_note": args.source_note,
        "items": normalized_items,
    }
    if args.client_request_id:
        body["client_request_id"] = args.client_request_id
    result = await post("/api/agent/import-reviews", body)
    return {
        **(result if isinstance(result, dict) else {}),
        "next_step": "请在花花日记 App 中检查并确认；当前尚未写入持仓或交易。",
    }


async def _export_portfolio(args: argparse.Namespace) -> dict:
    require_token()
    payload = await get("/api/sync/v3/state")
    output = _write_json(args.output, payload)
    return {"status": "ok", "output": str(output)}


async def _export_nav_history(args: argparse.Namespace) -> dict:
    require_token()
    codes = list(dict.fromkeys(validate_fund_code(code) for code in args.codes.split(",") if code.strip()))
    if not 1 <= len(codes) <= 20:
        raise ValueError("codes 需要包含 1-20 个基金代码")
    payload = await post("/api/funds/nav-history/batch", {
        "codes": codes,
        "start_date": args.start_date or None,
        "end_date": args.end_date or None,
        "order": args.order,
    })
    output = _write_json(args.output, payload)
    return {"status": "ok", "output": str(output), "codes": codes}


async def _submit_report(args: argparse.Namespace) -> dict:
    require_token()
    body = _read_json(args.file)
    if not isinstance(body, dict):
        raise ValueError("报告文件必须是 JSON 对象")
    return await post("/api/agent/messages", body)


def _parser() -> argparse.ArgumentParser:
    parser = _JsonArgumentParser(prog="huahua", description="花花日记文件、完整导出与诊断 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="检查 Token、网络和后端版本")
    doctor.set_defaults(handler=_doctor)

    imports = subparsers.add_parser("import", help="处理文件导入")
    import_commands = imports.add_subparsers(dest="import_command", required=True)
    screenshots = import_commands.add_parser("screenshots", help="直接上传本地截图进行识别")
    screenshots.add_argument("--type", required=True, choices=("holdings", "watchlist", "transactions"))
    screenshots.add_argument("--file", action="append", required=True)
    screenshots.add_argument("--result", required=True)
    screenshots.set_defaults(handler=_import_screenshots)
    review = import_commands.add_parser("review", help="从结构化结果文件创建 App 待确认请求")
    review.add_argument("--type", required=True, choices=("holdings", "watchlist", "transactions"))
    review.add_argument("--input", required=True)
    review.add_argument("--source-note", default="Agent 文件导入")
    review.add_argument("--client-request-id", default="")
    review.set_defaults(handler=_import_review)

    exports = subparsers.add_parser("export", help="把完整结果写入文件")
    export_commands = exports.add_subparsers(dest="export_command", required=True)
    portfolio = export_commands.add_parser("portfolio", help="导出完整组合主数据")
    portfolio.add_argument("--output", required=True)
    portfolio.set_defaults(handler=_export_portfolio)
    nav = export_commands.add_parser("nav-history", help="导出基金历史净值")
    nav.add_argument("--codes", required=True, help="逗号分隔的 1-20 个基金代码")
    nav.add_argument("--start-date", default="")
    nav.add_argument("--end-date", default="")
    nav.add_argument("--order", choices=("asc", "desc"), default="asc")
    nav.add_argument("--output", required=True)
    nav.set_defaults(handler=_export_nav_history)

    report = subparsers.add_parser("report", help="从文件投递个人报告")
    report_commands = report.add_subparsers(dest="report_command", required=True)
    submit = report_commands.add_parser("submit")
    submit.add_argument("--file", required=True)
    submit.set_defaults(handler=_submit_report)
    return parser


async def _run(args: argparse.Namespace) -> int:
    result = await args.handler(args)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


def main() -> None:
    try:
        raise SystemExit(asyncio.run(_run(_parser().parse_args())))
    except (ValueError, RuntimeError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
