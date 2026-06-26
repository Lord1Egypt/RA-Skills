#!/usr/bin/env python3
"""
Leap 文件传输脚本 — 上传 & 下载。
封装了 multipart/form-data 上传和二进制文件下载，
替代原生 curl 以避免 Windows 下通配符 / 转义兼容问题。

用法:
  上传文件:
    python scripts/file_transfer.py --mode upload --file-path "<文件路径>"
  下载结果文件:
    python scripts/file_transfer.py --mode download --result-id <id> --filename <name> [--output <保存路径>]

零外部依赖 — 仅使用 Python 标准库。
"""
import argparse
import json
import mimetypes
import os
import sys
import uuid
import urllib.request
import urllib.error

DEFAULT_BASE_URL = "https://platform.daofeiai.com"


def _build_multipart(file_path: str):
    """构造 multipart/form-data 请求体，仅依赖标准库。"""
    boundary = uuid.uuid4().hex
    filename = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n"
        f"\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


def _upload_single(base_url: str, api_key: str, abs_path: str) -> dict:
    """上传单个文件到 Leap 平台，返回结果 dict。"""
    body, content_type = _build_multipart(abs_path)

    url = f"{base_url}/api/v1/files/upload"
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type,
        "Accept": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", "replace")
        return {"status": "error", "http_code": e.code, "error_message": body_text,
                "file_path": abs_path}
    except urllib.error.URLError as e:
        return {"status": "error", "error_message": f"连接失败: {e}",
                "file_path": abs_path}


def upload_files(base_url: str, api_key: str, file_paths: list):
    """上传一个或多个文件到 Leap 平台。"""
    results = []
    errors = []

    for fp in file_paths:
        abs_path = os.path.abspath(fp)
        if not os.path.isfile(abs_path):
            errors.append({"status": "error", "error_message": f"文件不存在: {abs_path}",
                           "file_path": abs_path})
            continue
        result = _upload_single(base_url, api_key, abs_path)
        if "error_message" in result:
            errors.append(result)
        else:
            results.append(result)

    # 单文件：直接输出原始结果（保持向后兼容）
    if len(file_paths) == 1:
        output = results[0] if results else errors[0]
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(0 if results else 1)

    # 多文件：输出汇总
    output = {
        "status": "success" if not errors else ("partial" if results else "error"),
        "uploaded": results,
        "errors": errors,
        "total_uploaded": len(results),
        "total_errors": len(errors),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)


def download_file(base_url: str, api_key: str, result_id: str,
                  filename: str, output_path: str | None):
    """从 Leap 平台下载结果文件。"""
    url = f"{base_url}/api/v1/results/{result_id}/files/{filename}"
    save_path = output_path if output_path else filename

    req = urllib.request.Request(url, method="GET", headers={
        "Authorization": f"Bearer {api_key}",
    })

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(save_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

        abs_save = os.path.abspath(save_path)
        file_size = os.path.getsize(abs_save)
        print(json.dumps({
            "status": "success",
            "saved_to": abs_save,
            "file_size_bytes": file_size,
            "filename": filename,
        }, ensure_ascii=False, indent=2))
        sys.exit(0)
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", "replace")
        print(json.dumps({
            "status": "error",
            "http_code": e.code,
            "error_message": body_text,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({
            "status": "error",
            "error_message": f"连接失败: {e}",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Leap 文件上传 / 下载工具")
    parser.add_argument("--mode", required=True, choices=["upload", "download"],
                        help="操作模式: upload=上传文件, download=下载结果文件")
    parser.add_argument("--file-path", action="append", default=[],
                        help="待上传的文件路径 (upload 模式，可多次指定批量上传)")
    parser.add_argument("--result-id", help="任务 result_id (download 模式必填)")
    parser.add_argument("--filename", help="要下载的文件名 (download 模式必填)")
    parser.add_argument("--output", help="下载文件保存路径 (download 模式可选，默认当前目录)")
    args = parser.parse_args()

    api_key = os.environ.get("LEAP_API_KEY", "")
    base_url = DEFAULT_BASE_URL

    if not api_key:
        print(json.dumps({
            "status": "error",
            "error_message": (
                "LEAP_API_KEY 未配置。\n"
                "请在 OpenClaw skill 设置界面配置 LEAP_API_KEY 环境变量。"
            )
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.mode == "upload":
        if not args.file_path:
            print("错误: upload 模式必须提供至少一个 --file-path", file=sys.stderr)
            sys.exit(1)
        upload_files(base_url, api_key, args.file_path)

    elif args.mode == "download":
        if not args.result_id or not args.filename:
            print("错误: download 模式必须提供 --result-id 和 --filename", file=sys.stderr)
            sys.exit(1)
        download_file(base_url, api_key, args.result_id, args.filename, args.output)


if __name__ == "__main__":
    main()
