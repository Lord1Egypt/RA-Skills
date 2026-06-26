#!/usr/bin/env python3
"""
奇安信 Hunter 批量查询命令行脚本。

功能说明：
- 通过交互方式输入请求参数；
- 使用 POST /openApi/search/batch 创建导出任务；
- 不使用文件上传模式；
- 自动将 search 按 RFC 4648 进行 base64url 编码；
- 自动轮询任务进度并下载最终导出文件。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import requests


API_URL = "https://hunter.qianxin.com/openApi/search/batch"
DOWNLOAD_BASE_URL = "https://hunter.qianxin.com/openApi/search/download"
# Hunter 可选导出字段白名单，用于入参校验避免请求被服务端拒绝
ALLOWED_FIELDS = {
    "ip",
    "port",
    "domain",
    "ip_tag",
    "url",
    "web_title",
    "is_risk_protocol",
    "protocol",
    "base_protocol",
    "status_code",
    "os",
    "company",
    "number",
    "icp_exception",
    "country",
    "province",
    "city",
    "is_web",
    "isp",
    "as_org",
    "cert_sha256",
    "ssl_certificate",
    "component",
    "asset_tag",
    "updated_at",
    "header",
    "header_server",
    "banner",
}


def _prompt_required(prompt_text: str) -> str:
    """读取必填参数，直到用户输入非空内容。"""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("该参数必填，请重新输入。")


def _prompt_optional(prompt_text: str) -> Optional[str]:
    """读取可选参数，空输入返回 None。"""
    value = input(prompt_text).strip()
    return value or None


def _validate_date(date_str: str) -> bool:
    """校验日期格式是否为 YYYY-MM-DD。"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def _encode_base64url(text: str) -> str:
    # Hunter 要求 search 按 RFC 4648 base64url 编码，且去掉末尾填充 "="
    raw = text.encode("utf-8")
    encoded = base64.urlsafe_b64encode(raw).decode("utf-8")
    return encoded.rstrip("=")


def _extract_task_id(data: Dict) -> Optional[str]:
    # 兼容不同返回结构：顶层 / data 内层
    for key in ("task_id", "taskId", "id"):
        if key in data:
            return str(data[key])
    nested_data = data.get("data")
    if isinstance(nested_data, dict):
        for key in ("task_id", "taskId", "id"):
            if key in nested_data:
                return str(nested_data[key])
    return None


def _extract_progress(data: Dict) -> Optional[int]:
    # 兼容 progress/percent/rate 等不同字段命名
    source = data.get("data") if isinstance(data.get("data"), dict) else data
    for key in ("progress", "percent", "rate", "progress_rate"):
        value = source.get(key)
        if value is None:
            continue
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            matched = re.search(r"\d+", value)
            if matched:
                return int(matched.group(0))
    return None


def _is_task_finished(data: Dict) -> bool:
    # 服务端状态字段存在多种形式，这里统一做宽松判断
    source = data.get("data") if isinstance(data.get("data"), dict) else data

    for key in ("is_finish", "is_finished", "finished", "done", "completed"):
        value = source.get(key)
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return int(value) == 1
        if isinstance(value, str):
            if value.lower() in {"1", "true", "yes", "done", "success", "finished", "completed"}:
                return True

    status = source.get("status")
    if isinstance(status, str) and status.lower() in {"done", "success", "finished", "completed"}:
        return True
    if isinstance(status, (int, float)) and int(status) in {2, 3, 100}:
        return True

    progress = _extract_progress(data)
    return progress == 100


def _poll_task(task_id: str, api_key: str, interval_sec: int = 5, timeout_sec: int = 300) -> bool:
    # 轮询导出任务，直到完成或超时
    status_url = f"{API_URL}/{task_id}"
    params = {"api-key": api_key}
    deadline = time.time() + timeout_sec

    print("\n开始轮询任务进度...")
    while time.time() < deadline:
        try:
            # 查询当前任务进度
            resp = requests.get(status_url, params=params, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as exc:
            print(f"查询进度失败: {exc}")
            time.sleep(interval_sec)
            continue
        except json.JSONDecodeError:
            print("进度接口返回非 JSON，继续重试...")
            time.sleep(interval_sec)
            continue

        progress = _extract_progress(payload)
        if progress is not None:
            print(f"任务 {task_id} 当前进度: {progress}%")
        else:
            print(f"任务 {task_id} 进度响应: {json.dumps(payload, ensure_ascii=False)}")

        if _is_task_finished(payload):
            print("任务已完成。")
            return True

        time.sleep(interval_sec)

    print(f"任务轮询超时（>{timeout_sec}秒），请稍后手动查询：{API_URL}/{task_id}?api-key=你的key")
    return False


def _guess_filename(resp: requests.Response, fallback_name: str) -> str:
    # 优先从响应头提取服务端建议文件名
    cd = resp.headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', cd)
    if match:
        return match.group(1)
    return fallback_name


def _download_result(task_id: str, api_key: str, output_file: Optional[str] = None) -> Optional[Path]:
    """下载导出结果文件，成功返回本地文件路径。"""
    download_url = f"{DOWNLOAD_BASE_URL}/{task_id}"
    params = {"api-key": api_key}
    fallback_name = output_file or f"hunter_task_{task_id}.csv"

    try:
        resp = requests.get(download_url, params=params, timeout=60, stream=True)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"下载失败: {exc}")
        return None

    # 兼容下载接口在未完成时返回 JSON 错误消息
    content_type = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" in content_type:
        try:
            payload = resp.json()
            print("下载接口返回 JSON（可能任务尚未完成）:")
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print("下载接口返回 JSON 解析失败。")
        return None

    filename = _guess_filename(resp, fallback_name)
    # 下载接口通常会重定向到对象存储，这里按流式写入避免大文件占内存
    path = Path(filename)
    with path.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return path


def _build_params_from_args(args: argparse.Namespace) -> Dict[str, str]:
    """从命令行参数构建请求参数。"""
    params: Dict[str, str] = {}
    api_key = args.api_key or os.getenv("HUNTER_API_KEY")
    if not api_key:
        if args.no_interactive:
            raise ValueError("缺少 api-key，请通过 --api-key 或环境变量 HUNTER_API_KEY 提供")
        api_key = _prompt_required("api-key（必填）: ")
    params["api-key"] = api_key

    search_raw = args.search
    if search_raw is None and not args.no_interactive:
        search_raw = _prompt_optional("搜索语法 search（可选，输入原始语法）: ")
    if search_raw:
        params["search"] = _encode_base64url(search_raw)

    start_time = args.start_time
    if start_time is None and not args.no_interactive:
        start_time = _prompt_optional("开始时间 start_time（可选，格式 YYYY-MM-DD）: ")
    if start_time:
        if not _validate_date(start_time):
            raise ValueError("start_time 格式错误，应为 YYYY-MM-DD")
        params["start_time"] = start_time

    end_time = args.end_time
    if end_time is None and not args.no_interactive:
        end_time = _prompt_optional("结束时间 end_time（可选，格式 YYYY-MM-DD）: ")
    if end_time:
        if not _validate_date(end_time):
            raise ValueError("end_time 格式错误，应为 YYYY-MM-DD")
        params["end_time"] = end_time

    is_web = args.is_web
    if is_web is None and not args.no_interactive:
        is_web = _prompt_optional("是否网站资产 is_web（可选，1=是，2=否）: ")
    if is_web:
        if is_web not in {"1", "2"}:
            raise ValueError("is_web 仅允许 1 或 2")
        params["is_web"] = is_web

    status_code = args.status_code
    if status_code is None and not args.no_interactive:
        status_code = _prompt_optional("状态码 status_code（可选，逗号分隔，如 200,401）: ")
    if status_code:
        params["status_code"] = status_code

    fields = args.fields
    if fields is None and not args.no_interactive:
        fields = _prompt_optional("返回字段 fields（可选，逗号分隔）: ")
    if fields:
        field_list = [f.strip() for f in fields.split(",") if f.strip()]
        invalid = [f for f in field_list if f not in ALLOWED_FIELDS]
        if invalid:
            raise ValueError(f"fields 包含不支持字段: {', '.join(invalid)}")
        params["fields"] = ",".join(field_list)

    assets_limit = args.assets_limit
    if assets_limit is None and not args.no_interactive:
        assets_limit = _prompt_optional("导出资产数量 assets_limit（可选，整数）: ")
    if assets_limit:
        if not str(assets_limit).isdigit():
            raise ValueError("assets_limit 必须为整数")
        params["assets_limit"] = str(assets_limit)

    return params


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="奇安信 Hunter 资产批量导出")
    parser.add_argument("--api-key", help="Hunter API key（可配合环境变量 HUNTER_API_KEY）")
    parser.add_argument("--search", help="原始搜索语法（脚本会自动 base64url 编码）")
    parser.add_argument("--start-time", help="开始时间，格式 YYYY-MM-DD")
    parser.add_argument("--end-time", help="结束时间，格式 YYYY-MM-DD")
    parser.add_argument("--is-web", choices=["1", "2"], help="是否网站资产：1=是，2=否")
    parser.add_argument("--status-code", help="状态码，逗号分隔")
    parser.add_argument("--fields", help="返回字段，逗号分隔")
    parser.add_argument("--assets-limit", help="导出资产数量，整数")
    parser.add_argument("--output-file", help="下载文件名")
    parser.add_argument("--no-interactive", action="store_true", help="启用无交互模式")
    parser.add_argument("--check-delay", type=int, default=10, help="创建任务后等待多少秒再首次尝试下载")
    parser.add_argument("--poll-interval", type=int, default=5, help="任务轮询间隔秒数")
    parser.add_argument("--poll-timeout", type=int, default=300, help="任务轮询超时时间秒数")
    parser.add_argument("--json-output", action="store_true", help="输出机器可读 JSON 结果")
    return parser.parse_args()


def main() -> None:
    # 流程：创建任务 -> 轮询进度 -> 下载文件
    args = parse_args()
    try:
        params = _build_params_from_args(args)
    except ValueError as exc:
        print(f"\n参数错误: {exc}")
        return

    print("\n正在提交批量查询任务...")
    try:
        response = requests.post(API_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"请求失败: {exc}")
        return

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("响应不是 JSON，原始内容如下：")
        print(response.text)
        return

    task_id = _extract_task_id(data)
    print("\n请求成功。")
    if task_id:
        print(f"任务 ID: {task_id}")
    else:
        print("未在响应中识别到任务 ID，请检查完整响应。")

    print("\n完整响应:")
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if not task_id:
        return

    api_key = params["api-key"]
    saved_path: Optional[Path] = None
    if args.check_delay > 0:
        print(f"\n等待 {args.check_delay} 秒后尝试下载...")
        time.sleep(args.check_delay)
        saved_path = _download_result(task_id=task_id, api_key=api_key, output_file=args.output_file)

    if saved_path is None:
        poll_ok = _poll_task(
            task_id=task_id,
            api_key=api_key,
            interval_sec=args.poll_interval,
            timeout_sec=args.poll_timeout,
        )
        if not poll_ok:
            return

        output_name = args.output_file
        if output_name is None and not args.no_interactive:
            output_name = _prompt_optional("下载文件名（可选，默认自动命名）: ")
        saved_path = _download_result(task_id=task_id, api_key=api_key, output_file=output_name)

    if saved_path:
        print(f"\n下载成功，文件已保存到: {saved_path.resolve()}")
        if args.json_output:
            result = {
                "ok": True,
                "task_id": task_id,
                "file": str(saved_path.resolve()),
            }
            print(json.dumps(result, ensure_ascii=False))
    elif args.json_output:
        result = {
            "ok": False,
            "task_id": task_id,
            "file": None,
        }
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
