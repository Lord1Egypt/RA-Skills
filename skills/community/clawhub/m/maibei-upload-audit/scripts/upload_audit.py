#!/usr/bin/env python3
import argparse
import json
import mimetypes
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

import requests

try:
    from html_report import generate_html_report
except ImportError:
    # Fallback: try as standalone script
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from html_report import generate_html_report

COPY_EXCEL_ARTIFACT_ID = "69ca226377efb8a1de743d34"
ANALYZE_ARTIFACT_ID = "69c245bca5e657510a37a6a2"
AUDIT_ARTIFACT_ID = "69c6582612aa26396bd2ace7"
FONT_AUDIT_ARTIFACT_ID = "69ccb9d584cf626fe68ff7ea"
SUMMARY_WORKFLOW_ARTIFACT_ID = "69ca16d067a09db8deb145c2"
SOURCE_EXCEL_URL = "https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0"
UPLOAD_URL_ENDPOINT = "https://maibei.maybe.ai/api/trpc/imageGetUploadUrl"
WORKFLOW_DETAIL_ENDPOINT = "https://play-be.omnimcp.ai/api/v1/workflow/detail/public"
WORKFLOW_RUN_ENDPOINT = "https://play-be.omnimcp.ai/api/v1/workflow/run"


def workflow_detail(artifact_id: str):
    r = requests.post(
        WORKFLOW_DETAIL_ENDPOINT,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"artifact_id": artifact_id}),
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def make_auth_headers(token: str, user_id: str, extra: Optional[dict] = None):
    headers = {
        "Authorization": f"Bearer {token}",
        "user-id": user_id,
    }
    if extra:
        headers.update(extra)
    return headers


def infer_file_type(path_or_url: str):
    lowered = path_or_url.lower()
    if any(lowered.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".heic"]):
        return "image"
    if any(lowered.endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"]):
        return "video"
    mime, _ = mimetypes.guess_type(path_or_url)
    if mime and mime.startswith("image/"):
        return "image"
    if mime and mime.startswith("video/"):
        return "video"
    return "image"


def upload_file(token: str, user_id: str, file_path: str, filename: Optional[str] = None):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {file_path}")

    filename = filename or path.name
    key = f"superapp/uploads/{int(time.time() * 1000)}-{filename}"

    headers = make_auth_headers(
        token,
        user_id,
        {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://maibei.maybe.ai",
            "referer": "https://maibei.maybe.ai/e-commerce/try-on",
        },
    )

    r = requests.post(
        UPLOAD_URL_ENDPOINT,
        headers=headers,
        data=json.dumps({"key": key}),
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    payload = data.get("result", {}).get("data") or data.get("data") or data
    upload_url = payload["uploadUrl"]
    public_url = payload["url"]

    content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    with path.open("rb") as fh:
        put = requests.put(
            upload_url,
            data=fh,
            headers={"Content-Type": content_type},
            timeout=300,
        )
    put.raise_for_status()

    return {
        "local_path": str(path),
        "file_name": filename,
        "file_type": infer_file_type(filename),
        "key": key,
        "url": public_url,
    }


def run_workflow(token: str, user_id: str, artifact_id: str, variables: list, service: str = "e-commerce", metadata: Optional[dict] = None):
    detail = workflow_detail(artifact_id)
    body = {
        "artifact_id": detail["artifact_id"],
        "interaction": True,
        "task": "",
        "task_id": str(uuid.uuid4()),
        "workflow_id": detail["id"],
        "variables": variables,
        "metadata": metadata or {"case": "upload-audit-file", "title": "上传文件并审核"},
        "service": service,
    }
    r = requests.post(
        WORKFLOW_RUN_ENDPOINT,
        headers=make_auth_headers(
            token,
            user_id,
            {
                "Accept": "text/event-stream",
                "Content-Type": "application/json",
            },
        ),
        data=json.dumps(body),
        timeout=300,
        stream=True,
    )
    r.raise_for_status()
    events = []
    for line in r.iter_lines(decode_unicode=True):
        if line:
            events.append(line)
    return events


def extract_sheet_url(events):
    for line in reversed(events):
        if "dataframe:copy_excel_url_data" in line and "copy_excel_url" in line:
            try:
                payload = json.loads(line.removeprefix("data: "))
                content = payload["data"]["content"]
                inner = json.loads(content)
                content2 = inner.get("content")
                if content2:
                    out = json.loads(content2)
                    data = out.get("output", {}).get("data", [])
                    if data and isinstance(data, list):
                        url = data[0].get("copy_excel_url")
                        if url:
                            return url
            except Exception:
                pass
        if "spreadsheet_url" in line:
            idx = line.find("https://www.maybe.ai/docs/spreadsheets/d/")
            if idx != -1:
                tail = line[idx:]
                end = tail.find('\\"')
                if end != -1:
                    return tail[:end].replace("?gid=0", "").replace("?gid=2", "")
    return None


def print_events(events):
    for e in events:
        print(e)


def normalize_uploaded_rows(rows):
    out = []
    for r in rows:
        out.append(
            {
                "url": r["url"],
                "file_type": r.get("file_type") or infer_file_type(r["url"]),
                "file_name": r.get("file_name") or Path(r["url"]).name,
            }
        )
    return out


def print_summary(sheet_url, uploaded_rows, ran_analyze, ran_audit, ran_font, ran_summary):
    print(
        json.dumps(
            {
                "sheet_url": sheet_url,
                "uploaded_rows": uploaded_rows,
                "ran_analyze": ran_analyze,
                "ran_audit": ran_audit,
                "ran_font": ran_font,
                "ran_summary": ran_summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def shared_sheet_variables(sheet_url):
    return [
        {"name": "variable:scalar:copy_excel_url", "default_value": sheet_url},
        {"name": "variable:scalar:excel_url", "default_value": sheet_url},
        {"name": "variable:dataframe:copy_excel_url_data", "default_value": [{"copy_excel_url": sheet_url}]},
    ]


def share_via_trycloudflare(file_path):
    """Share a local file via trycloudflare tunnel. Returns (url, tunnel_proc, server_proc)."""
    import subprocess, time, socket, os, urllib.request

    def find_free_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    path = os.path.abspath(os.path.expanduser(file_path))
    is_file = os.path.isfile(path)
    if is_file:
        serve_dir = os.path.dirname(path)
        filename_hint = os.path.basename(path)
    else:
        serve_dir = path
        filename_hint = ""

    port = find_free_port()
    server_proc = subprocess.Popen(
        [sys.executable, '-m', 'http.server', str(port)],
        cwd=serve_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(1.5)

    tunnel_proc = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{port}',
         '--no-autoupdate', '--protocol', 'http2'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    url = None
    start = time.time()
    while time.time() - start < 30:
        line = tunnel_proc.stderr.readline()
        if line and 'trycloudflare.com' in line:
            idx = line.find('https://')
            if idx != -1:
                url = line[idx:].split()[0].rstrip()
                break
        time.sleep(0.3)
        if tunnel_proc.poll() is not None:
            break

    if not url:
        tunnel_proc.terminate()
        server_proc.terminate()
        raise RuntimeError("Could not get trycloudflare URL")

    # Verify
    hint = filename_hint if is_file else ''
    target = f"{url}/{hint}" if hint else url
    try:
        req = urllib.request.Request(target)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                print(f"Warning: URL verification returned {resp.status}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: URL verification failed: {e}", file=sys.stderr)

    return url, tunnel_proc, server_proc


def main():
    ap = argparse.ArgumentParser(description="Run Maibei upload-audit workflows end-to-end.")
    ap.add_argument("--token", required=True)
    ap.add_argument("--user-id", required=True)
    ap.add_argument("--mode", choices=["upload", "copy", "analyze", "audit", "font", "summary", "full"], required=True)
    ap.add_argument("--sheet-url", help="Existing working sheet URL")
    ap.add_argument("--source-excel-url", default=SOURCE_EXCEL_URL)
    ap.add_argument("--file", action="append", default=[], help="Local file path to upload; repeatable")
    ap.add_argument("--uploaded-json", help="JSON array of uploaded file rows with url/file_type/file_name")
    ap.add_argument("--print-json", action="store_true")
    ap.add_argument("--skip-analyze", action="store_true", help="In full mode, skip analyze step")
    ap.add_argument("--skip-audit", action="store_true", help="In full mode, skip audit step")
    ap.add_argument("--skip-font", action="store_true", help="In full mode, skip font-audit step")
    ap.add_argument("--skip-summary", action="store_true", help="In full mode, skip final summary workflow")
    ap.add_argument("--html", action="store_true", help="Generate HTML report after workflows complete")
    ap.add_argument("--share", action="store_true", help="Share HTML report via trycloudflare tunnel")
    ap.add_argument("--html-only", action="store_true", help="Skip workflows, generate HTML from prior --sheet-url and --uploaded-json")
    ap.add_argument("--html-output", default="audit_report.html", help="Output HTML filename (default: audit_report.html)")
    args = ap.parse_args()

    uploaded_rows = []
    if args.uploaded_json:
        uploaded_rows = json.loads(args.uploaded_json)

    if args.mode in {"upload", "full"} and args.file:
        for f in args.file:
            uploaded_rows.append(upload_file(args.token, args.user_id, f))
        if args.mode == "upload":
            if args.print_json:
                print(json.dumps(uploaded_rows, ensure_ascii=False, indent=2))
            else:
                for row in uploaded_rows:
                    print(row["url"])
            return

    if args.mode == "copy":
        events = run_workflow(args.token, args.user_id, COPY_EXCEL_ARTIFACT_ID, [
            {"name": "variable:scalar:source_excel_url", "default_value": args.source_excel_url}
        ])
        print_events(events)
        return

    sheet_url = args.sheet_url

    if args.mode == "full":
        copy_events = run_workflow(args.token, args.user_id, COPY_EXCEL_ARTIFACT_ID, [
            {"name": "variable:scalar:source_excel_url", "default_value": args.source_excel_url}
        ])
        sheet_url = extract_sheet_url(copy_events)
        if not sheet_url:
            print_events(copy_events)
            raise SystemExit("failed to extract copied sheet url from copy workflow")

        ran_analyze = False
        ran_audit = False
        ran_font = False
        ran_summary = False

        if not args.skip_analyze:
            if not uploaded_rows:
                raise SystemExit("full mode requires uploaded files or --uploaded-json unless --skip-analyze is used")
            analyze_events = run_workflow(args.token, args.user_id, ANALYZE_ARTIFACT_ID, [
                {"name": "variable:scalar:copy_excel_url", "default_value": sheet_url},
                {"name": "variable:dataframe:product_images", "default_value": normalize_uploaded_rows(uploaded_rows)},
            ])
            ran_analyze = True
            if not args.print_json:
                print_events(analyze_events)

        audit_events = None
        font_events = None
        with ThreadPoolExecutor(max_workers=2) as ex:
            futures = {}
            if not args.skip_audit:
                futures["audit"] = ex.submit(run_workflow, args.token, args.user_id, AUDIT_ARTIFACT_ID, shared_sheet_variables(sheet_url))
            if not args.skip_font:
                futures["font"] = ex.submit(run_workflow, args.token, args.user_id, FONT_AUDIT_ARTIFACT_ID, [
                    {"name": "variable:scalar:copy_excel_url", "default_value": sheet_url}
                ])
            for name, fut in futures.items():
                result = fut.result()
                if name == "audit":
                    audit_events = result
                    ran_audit = True
                    if not args.print_json:
                        print_events(audit_events)
                elif name == "font":
                    font_events = result
                    ran_font = True
                    if not args.print_json:
                        print_events(font_events)

        if not args.skip_summary:
            summary_events = run_workflow(args.token, args.user_id, SUMMARY_WORKFLOW_ARTIFACT_ID, shared_sheet_variables(sheet_url))
            ran_summary = True
            if not args.print_json:
                print_events(summary_events)

        print_summary(sheet_url, uploaded_rows, ran_analyze, ran_audit, ran_font, ran_summary)

        # Post-processing: HTML report and sharing
        if args.html:
            html_output = args.html_output
            generate_html_report(sheet_url, uploaded_rows, html_output)
            if args.share:
                print("\n🌐 正在分享到公网...")
                url, tunnel_proc, server_proc = share_via_trycloudflare(html_output)
                print(f"✅ 报告已发布: {url}")
                # Keep processes alive
                try:
                    tunnel_proc.wait()
                except KeyboardInterrupt:
                    tunnel_proc.terminate()
                    server_proc.terminate()

        return

    if not sheet_url:
        raise SystemExit("--sheet-url is required for analyze/audit/font/summary modes")

    if args.mode == "analyze":
        if not uploaded_rows and not args.file:
            raise SystemExit("--uploaded-json or --file is required for analyze")
        events = run_workflow(args.token, args.user_id, ANALYZE_ARTIFACT_ID, [
            {"name": "variable:scalar:copy_excel_url", "default_value": sheet_url},
            {"name": "variable:dataframe:product_images", "default_value": normalize_uploaded_rows(uploaded_rows)},
        ])
        print_events(events)
        return

    if args.mode == "audit":
        events = run_workflow(args.token, args.user_id, AUDIT_ARTIFACT_ID, shared_sheet_variables(sheet_url))
        print_events(events)
        return

    if args.mode == "font":
        events = run_workflow(args.token, args.user_id, FONT_AUDIT_ARTIFACT_ID, [
            {"name": "variable:scalar:copy_excel_url", "default_value": sheet_url}
        ])
        print_events(events)
        return

    if args.mode == "summary":
        events = run_workflow(args.token, args.user_id, SUMMARY_WORKFLOW_ARTIFACT_ID, shared_sheet_variables(sheet_url))
        print_events(events)
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
