#!/usr/bin/env python3
"""Small CLI for the 票IN PAT invoice API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import mimetypes
import os
import platform
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


DEFAULT_BASE_URL = "https://admin.piaoin.cn"
ENV_FILE = ".piaoin_evn"
LEGACY_ENV_FILE = ".piaoin_env"
DATA_DIR = "piaoin_invoice"
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".pdf"}


def load_env(root: Path) -> tuple[dict[str, str], Path]:
    env_path = root / ENV_FILE
    if not env_path.exists() and (root / LEGACY_ENV_FILE).exists():
        env_path = root / LEGACY_ENV_FILE
    data: dict[str, str] = {}
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data, env_path


def save_env(root: Path, data: dict[str, str], env_path: Path | None = None) -> Path:
    path = env_path or (root / ENV_FILE)
    order = ["API_KEY", "BASE_URL", "USER_ROLE", "LAST_SYNC_DATE", "RUNTIME_MODE", "LAST_RUNTIME"]
    lines = []
    for key in order:
        if key in data and data[key] != "":
            lines.append(f"{key}={data[key]}")
    for key in sorted(k for k in data if k not in order):
        lines.append(f"{key}={data[key]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def detect_runtime(mode: str) -> str:
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    shell = os.environ.get("SHELL") or os.environ.get("ComSpec") or os.environ.get("PSModulePath", "")
    shell_name = Path(shell).name if shell else "unknown"
    curl_path = shutil.which("curl") or shutil.which("curl.exe")
    parts = [
        now,
        f"os={platform.system() or 'unknown'} {platform.release() or ''}".strip(),
        f"shell={shell_name}",
        f"python={platform.python_version()}",
        f"http_client=python-urllib",
    ]
    if curl_path:
        parts.append(f"curl={curl_path}")
    return "; ".join(parts)


def record_runtime(root: Path, env: dict[str, str], env_path: Path, mode: str = "python-cli") -> None:
    env["RUNTIME_MODE"] = mode
    env["LAST_RUNTIME"] = detect_runtime(mode)
    save_env(root, env, env_path if env_path.exists() else root / ENV_FILE)


def require_api_key(env: dict[str, str]) -> str:
    key = env.get("API_KEY") or os.environ.get("PIAOIN_API_KEY")
    if not key:
        raise SystemExit("Missing API key. Run: piaoin_invoice.py config --api-key py_xxx")
    return key


def base_url(env: dict[str, str]) -> str:
    return (env.get("BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def role(env: dict[str, str]) -> str:
    return env.get("USER_ROLE", "unknown")


def mask_key(key: str) -> str:
    if len(key) <= 10:
        return "***"
    return f"{key[:3]}...{key[-4:]}"


def http_json(method: str, url: str, api_key: str, body: bytes | None = None, headers: dict[str, str] | None = None) -> dict:
    request_headers = {"X-API-Key": api_key, "Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {text}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON response from {url}") from exc
    if payload.get("code") != 200:
        raise SystemExit(f"API error code={payload.get('code')} msg={payload.get('msg')}")
    return payload


def safe_part(value: object, fallback: str = "unknown") -> str:
    text = str(value or fallback).strip()
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", text)
    text = re.sub(r"\s+", "_", text)
    return text[:80] or fallback


def month_for(row: dict) -> str:
    value = row.get("createTime") or row.get("invoiceDate") or dt.date.today().isoformat()
    return str(value)[:7]


def date_for(row: dict) -> str:
    value = row.get("invoiceDate") or row.get("createTime") or dt.date.today().isoformat()
    return str(value)[:10]


def extension_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower()
    return ext if ext in ALLOWED_EXTS else ".pdf"


def append_jsonl(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def md_cell(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return text.strip()


def money(value: object) -> str:
    if value is None or value == "":
        return ""
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def detail_summary(row: dict) -> str:
    for key in ("detailSummary", "detailsSummary", "itemSummary", "goodsSummary", "remark"):
        if row.get(key):
            return str(row[key])
    for key in ("details", "detailList", "items", "invoiceDetails", "invoiceDetailList"):
        items = row.get(key)
        if isinstance(items, list) and items:
            parts = []
            for item in items[:5]:
                if isinstance(item, dict):
                    name = item.get("goodsName") or item.get("itemName") or item.get("name") or item.get("cargoName") or item.get("projectName")
                    amount = item.get("amount") or item.get("invoiceAmount") or item.get("totalAmount")
                    if name and amount:
                        parts.append(f"{name}({money(amount)})")
                    elif name:
                        parts.append(str(name))
                elif item:
                    parts.append(str(item))
            if parts:
                extra = f" 等{len(items)}项" if len(items) > len(parts) else ""
                return "、".join(parts) + extra
    seller = row.get("seller")
    buyer = row.get("buyer")
    if seller or buyer:
        return f"{seller or ''} -> {buyer or ''}".strip()
    return ""


def summary_markdown(rows: list[dict], scope: str) -> str:
    generated_at = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    total_amount = sum(float(row.get("invoiceAmount") or 0) for row in rows if str(row.get("invoiceAmount") or "").replace(".", "", 1).isdigit())
    lines = [
        "# 票IN发票下载汇总",
        "",
        f"- 生成时间：{generated_at}",
        f"- 查询范围：{'全企业/全租户' if scope == 'tenant' else '当前用户'}",
        f"- 发票数量：{len(rows)}",
        f"- 金额合计：{total_amount:.2f}",
        "",
    ]
    if scope == "tenant":
        headers = ["发票用户名", "发票类型", "开票日期", "发票号码", "发票代码", "金额", "明细汇总", "上传日期"]
    else:
        headers = ["发票类型", "开票日期", "发票号码", "发票代码", "金额", "明细汇总", "上传日期"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" if h != "金额" else "---:" for h in headers) + " |")
    for row in rows:
        values = []
        if scope == "tenant":
            values.append(row.get("userName"))
        values.extend([
            row.get("invoiceTypeName"),
            row.get("invoiceDate"),
            row.get("invoiceNumber"),
            row.get("invoiceCode"),
            money(row.get("invoiceAmount")),
            detail_summary(row),
            row.get("createTime"),
        ])
        lines.append("| " + " | ".join(md_cell(v) for v in values) + " |")
    lines.append("")
    return "\n".join(lines)


def write_summary(root: Path, rows: list[dict], scope: str) -> Path:
    data_dir = root / DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = data_dir / f"summary_{stamp}.md"
    path.write_text(summary_markdown(rows, scope), encoding="utf-8")
    return path


def download_file(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return False
    req = urllib.request.Request(url, headers={"User-Agent": "piaoin-invoice-skill/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())
    return True


def list_page(env: dict[str, str], page_num: int, args: argparse.Namespace) -> dict:
    params = {
        "pageNum": str(page_num),
        "pageSize": str(args.page_size),
        "allTenant": "true" if args.scope == "tenant" else "false",
    }
    if args.start_date:
        params["startDate"] = args.start_date
    if args.end_date:
        params["endDate"] = args.end_date
    if args.invoice_type:
        params["invoiceTypeName"] = args.invoice_type
    query = urllib.parse.urlencode(params)
    url = f"{base_url(env)}/api/v1/pat/invoices/list?{query}"
    return http_json("GET", url, require_api_key(env))


def cmd_config(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    env, env_path = load_env(root)
    if args.api_key:
        env["API_KEY"] = args.api_key
    if args.base_url:
        env["BASE_URL"] = args.base_url.rstrip("/")
    elif "BASE_URL" not in env:
        env["BASE_URL"] = DEFAULT_BASE_URL
    if args.role:
        env["USER_ROLE"] = args.role
    elif "USER_ROLE" not in env:
        env["USER_ROLE"] = "unknown"
    env["RUNTIME_MODE"] = "python-cli"
    env["LAST_RUNTIME"] = detect_runtime("python-cli")
    path = save_env(root, env, env_path if env_path.exists() else root / ENV_FILE)
    shown_key = mask_key(env["API_KEY"]) if env.get("API_KEY") else "(missing)"
    print(f"Saved {path}")
    print(f"API_KEY={shown_key}")
    print(f"BASE_URL={env.get('BASE_URL')}")
    print(f"USER_ROLE={env.get('USER_ROLE')}")
    print(f"RUNTIME_MODE={env.get('RUNTIME_MODE')}")


def cmd_download(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    env, env_path = load_env(root)
    record_runtime(root, env, env_path)
    require_api_key(env)
    if args.scope == "tenant" and role(env) != "tenantAdmin" and not args.confirm_all_tenant:
        raise SystemExit("Refusing all-tenant download: set USER_ROLE=tenantAdmin or pass --confirm-all-tenant after confirming permissions.")
    if args.since_last and not args.start_date and env.get("LAST_SYNC_DATE"):
        args.start_date = env["LAST_SYNC_DATE"]

    total_rows = 0
    downloaded = 0
    all_rows: list[dict] = []
    max_date = env.get("LAST_SYNC_DATE", "")
    page_num = 1
    while True:
        payload = list_page(env, page_num, args)
        data = payload.get("data") or {}
        rows = data.get("rows") or []
        all_rows.extend(rows)
        total_rows += len(rows)
        rows_by_month: dict[str, list[dict]] = {}
        for row in rows:
            month = month_for(row)
            rows_by_month.setdefault(month, []).append(row)
            create_date = str(row.get("createTime") or "")[:10]
            invoice_date = str(row.get("invoiceDate") or "")[:10]
            max_date = max(max_date, create_date, invoice_date)

            invoice_url = row.get("invoiceUrl")
            if invoice_url:
                month_dir = root / DATA_DIR / month
                month_dir.mkdir(parents=True, exist_ok=True)
                name = "_".join([
                    safe_part(date_for(row)),
                    safe_part(row.get("invoiceNumber") or row.get("id")),
                    safe_part(row.get("seller"), "seller"),
                ])
                dest = month_dir / f"{name}{extension_from_url(invoice_url)}"
                try:
                    if download_file(invoice_url, dest):
                        downloaded += 1
                except Exception as exc:  # noqa: BLE001 - keep syncing other invoices
                    print(f"Download failed for invoice {row.get('id')}: {exc}", file=sys.stderr)

        for month, month_rows in rows_by_month.items():
            month_dir = root / DATA_DIR / month
            month_dir.mkdir(parents=True, exist_ok=True)
            append_jsonl(month_dir / "invoices.jsonl", month_rows)

        total_page = int(data.get("totalPage") or 0)
        print(f"Fetched page {page_num}/{total_page or '?'} rows={len(rows)}")
        if not rows or page_num >= total_page:
            break
        page_num += 1

    if max_date:
        env["LAST_SYNC_DATE"] = max_date
        save_env(root, env, env_path if env_path.exists() else root / ENV_FILE)
    summary_path = write_summary(root, all_rows, args.scope)
    print(f"Done. rows={total_rows} downloaded_files={downloaded} scope={args.scope} last_sync={env.get('LAST_SYNC_DATE', '')}")
    print(f"Summary: {summary_path}")


def encode_multipart(fields: dict[str, str], files: dict[str, Path]) -> tuple[bytes, str]:
    boundary = f"----piaoin-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")
    for name, path in files.items():
        filename = path.name
        ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
        chunks.append(f"Content-Type: {ctype}\r\n\r\n".encode())
        chunks.append(path.read_bytes())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def print_upload_result(payload: dict) -> None:
    data = payload.get("data") or {}
    invoices = data.get("invoices") or []
    print(f"batchNo={data.get('batchNo', '')} invoices={len(invoices)}")
    for item in invoices:
        parts = [
            f"invoiceId={item.get('invoiceId')}",
            f"number={item.get('invoiceNumber')}",
            f"amount={item.get('invoiceAmount')}",
            f"state={item.get('invoiceStateName')}",
            f"verification={item.get('isVerification')}",
        ]
        if item.get("checkResultInfo"):
            parts.append(f"check={item.get('checkResultInfo')}")
        print(" ".join(parts))


def cmd_upload(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    env, env_path = load_env(root)
    record_runtime(root, env, env_path)
    file_path = Path(args.file).resolve()
    if not file_path.exists() or not file_path.is_file():
        raise SystemExit(f"File not found: {file_path}")
    if file_path.suffix.lower() not in ALLOWED_EXTS:
        raise SystemExit("Only jpg/jpeg/png/pdf files are supported.")
    body, ctype = encode_multipart({}, {"file": file_path})
    url = f"{base_url(env)}/api/v1/pat/invoices/upload"
    payload = http_json("POST", url, require_api_key(env), body=body, headers={"Content-Type": ctype})
    print_upload_result(payload)


def cmd_upload_url(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    env, env_path = load_env(root)
    record_runtime(root, env, env_path)
    parsed = urllib.parse.urlparse(args.file_url)
    if parsed.scheme not in {"http", "https"}:
        raise SystemExit("fileUrl must be http or https.")
    body, ctype = encode_multipart({"fileUrl": args.file_url}, {})
    url = f"{base_url(env)}/api/v1/pat/invoices/upload"
    payload = http_json("POST", url, require_api_key(env), body=body, headers={"Content-Type": ctype})
    print_upload_result(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="票IN PAT invoice downloader/uploader")
    parser.add_argument("--root", default=".", help="Project root containing .piaoin_evn")
    sub = parser.add_subparsers(dest="command", required=True)

    config = sub.add_parser("config", help="Create or update .piaoin_evn")
    config.add_argument("--api-key")
    config.add_argument("--base-url", choices=[DEFAULT_BASE_URL, "https://admintest.piaoin.cn"])
    config.add_argument("--role", choices=["user", "tenantAdmin", "unknown"])
    config.set_defaults(func=cmd_config)

    download = sub.add_parser("download", help="Page through invoices and download invoiceUrl files")
    download.add_argument("--scope", choices=["own", "tenant"], default="own")
    download.add_argument("--page-size", type=int, default=50)
    download.add_argument("--start-date")
    download.add_argument("--end-date")
    download.add_argument("--invoice-type")
    download.add_argument("--since-last", action="store_true")
    download.add_argument("--confirm-all-tenant", action="store_true", help="Bypass local role guard after confirming tenant admin permission")
    download.set_defaults(func=cmd_download)

    upload = sub.add_parser("upload", help="Upload a local jpg/jpeg/png/pdf invoice")
    upload.add_argument("file")
    upload.set_defaults(func=cmd_upload)

    upload_url = sub.add_parser("upload-url", help="Upload a trusted remote invoice URL")
    upload_url.add_argument("file_url")
    upload_url.set_defaults(func=cmd_upload_url)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
