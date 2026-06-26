#!/usr/bin/env python3
"""
PDF to Markdown Converter for LLM Researcher

Usage:
    python pdf_to_md.py <pdf_url> [output_path]

Arguments:
    pdf_url     - URL to the PDF file to convert
    output_path - Optional: Path to write output (default: stdout)

Returns:
    Extracted markdown content from the # Introduction section (to stdout or file)
"""

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import zipfile
from io import BytesIO

V4_BASE_URL = "https://mineru.net/api/v4/extract"
DEFAULT_MODEL_VERSION = "vlm"
POLL_TIMEOUT_SECONDS = 300
POLL_INTERVAL_SECONDS = 3
MIN_SLEEP_SECONDS = 1
MAX_SLEEP_SECONDS = 5


def get_api_key():
    api_key = os.environ.get("MINERU_API_KEY")
    if not api_key:
        raise RuntimeError("MINERU_API_KEY environment variable is not set")
    return api_key


def randomized_api_delay(url):
    if not url.startswith(V4_BASE_URL):
        return
    delay_seconds = random.randint(MIN_SLEEP_SECONDS, MAX_SLEEP_SECONDS)
    print(f"Sleeping {delay_seconds}s before MinerU API call: {url}", file=sys.stderr)
    time.sleep(delay_seconds)


def _curl_executable():
    if sys.platform == "win32":
        exe = shutil.which("curl.exe")
        if exe:
            return exe
    return shutil.which("curl") or "curl"


def build_headers(url, method="GET"):
    headers = {"Accept": "*/*"}
    if url.startswith(V4_BASE_URL):
        headers["Authorization"] = f"Bearer {get_api_key()}"
        if method == "POST":
            headers["Content-Type"] = "application/json"
    return headers


def http_json_request(url, method="GET", payload=None, timeout=60):
    randomized_api_delay(url)
    curl = _curl_executable()
    cmd = [
        curl,
        "-sS",
        "-f",
        "-L",
        "--max-time",
        str(timeout),
        "-X",
        method,
    ]
    for key, value in build_headers(url, method=method).items():
        cmd.extend(["-H", f"{key}: {value}"])
    if method == "POST" and payload is not None:
        cmd.extend(["--data-raw", json.dumps(payload)])
    cmd.append(url)
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        err = (e.stderr or b"").decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"curl failed (exit {e.returncode}): {err or 'no stderr'}") from e
    raw = completed.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"curl returned non-JSON response: {raw[:500]}") from e


def http_binary_request(url, timeout=120):
    curl = _curl_executable()
    cmd = [curl, "-sS", "-f", "-L", "--max-time", str(timeout), url]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        err = (e.stderr or b"").decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"curl download failed (exit {e.returncode}): {err or 'no stderr'}") from e
    return completed.stdout


def create_v4_parse_task(file_url):
    payload = {
        "url": file_url,
        "model_version": DEFAULT_MODEL_VERSION,
    }
    result = http_json_request(f"{V4_BASE_URL}/task", method="POST", payload=payload)
    if result.get("code") != 0:
        raise RuntimeError(f"MinerU v4 task creation failed: {result.get('msg', 'unknown error')}")

    data = result.get("data") or {}
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError("MinerU v4 task creation returned incomplete response")
    return task_id


def find_markdown_in_zip(zip_bytes):
    with zipfile.ZipFile(BytesIO(zip_bytes)) as archive:
        markdown_candidates = [
            name for name in archive.namelist()
            if name.lower().endswith(".md") and not name.endswith("/")
        ]
        if not markdown_candidates:
            raise RuntimeError("MinerU result zip does not contain any markdown file")

        preferred_candidates = [
            name for name in markdown_candidates
            if name.lower().endswith(".md") and "content_list" not in name.lower()
        ]
        selected_name = sorted(preferred_candidates or markdown_candidates)[0]
        with archive.open(selected_name) as md_file:
            return md_file.read().decode("utf-8", errors="replace")


def poll_v4_markdown(task_id, timeout=POLL_TIMEOUT_SECONDS, interval=POLL_INTERVAL_SECONDS):
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = http_json_request(f"{V4_BASE_URL}/task/{task_id}", timeout=60)
        if result.get("code") != 0:
            raise RuntimeError(f"MinerU v4 polling failed: {result.get('msg', 'unknown error')}")

        data = result.get("data") or {}
        state = data.get("state")
        elapsed = int(time.time() - start_time)

        if state == "done":
            full_zip_url = data.get("full_zip_url")
            if not full_zip_url:
                raise RuntimeError("MinerU v4 completed without full_zip_url")
            print(f"[{elapsed}s] MinerU v4 parse completed.", file=sys.stderr)
            zip_bytes = http_binary_request(full_zip_url, timeout=120)
            return find_markdown_in_zip(zip_bytes)

        if state == "failed":
            error_message = data.get("err_msg") or "unknown error"
            raise RuntimeError(f"MinerU v4 parse failed: {error_message}")

        print(f"[{elapsed}s] MinerU v4 state: {state}", file=sys.stderr)
        time.sleep(interval)

    raise RuntimeError(f"MinerU v4 parse timed out after {timeout} seconds")


def is_url(value):
    return bool(re.match(r"^https?://", value, flags=re.IGNORECASE))


def parse_pdf(pdf_url, output_path=None):
    del output_path
    task_id = create_v4_parse_task(pdf_url)
    print(f"MinerU v4 task created: {task_id}", file=sys.stderr)
    markdown = poll_v4_markdown(task_id)
    return markdown


def extract_introduction(markdown):
    normalized = markdown.replace("\r\n", "\n").replace("\r", "\n")
    intro_match = re.search(r"(?im)^#\s+.*introduction.*$", normalized)
    if not intro_match:
        raise RuntimeError("No level-1 heading containing 'introduction' found in MinerU markdown")

    section_start = intro_match.end()
    remaining = normalized[section_start:]
    next_heading_match = re.search(r"(?im)^#\s+.+$", remaining)
    section_end = section_start + next_heading_match.start() if next_heading_match else len(normalized)
    introduction_body = normalized[section_start:section_end].strip()
    if not introduction_body:
        raise RuntimeError("The '# Introduction' section is empty")

    return f"# Introduction\n\n{introduction_body}\n"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_url")
    parser.add_argument("output_path", nargs="?")
    parser.add_argument(
        "--range",
        dest="content_range",
        choices=("introduction", "all"),
        default="introduction",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    pdf_url = args.pdf_url
    output_path = args.output_path

    if not is_url(pdf_url):
        print(f"Error: Expected a PDF URL, got: {pdf_url}", file=sys.stderr)
        sys.exit(1)

    try:
        markdown = parse_pdf(pdf_url, output_path)
        if args.content_range == "introduction":
            markdown = extract_introduction(markdown)

        if output_path:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Markdown extracted to: {output_path}", file=sys.stderr)
        else:
            print(markdown)
    except Exception as e:
        print(f"Error parsing PDF: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
