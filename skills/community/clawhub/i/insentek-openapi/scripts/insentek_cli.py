#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insentek OpenAPI Unified CLI

封装所有 API 调用、认证管理、边界检查与数据导出能力。
Agent 通过调用此脚本执行所有操作，而非直接使用 curl。

凭据请通过 CLI 配置（不要在对话中提供 appid/secret）：
    npx @insentek/openapi-skill login
    npx @insentek/openapi-skill logout
    npx @insentek/openapi-skill auth status

Usage:
    python3 insentek_cli.py devices [--page 1] [--limit 20]
    python3 insentek_cli.py device --sn SN
    python3 insentek_cli.py data --sn SN --range START,END [--include-params moisture,temperature] [--dry-run]
    python3 insentek_cli.py latest --sn SN
    python3 insentek_cli.py export --sn SN --range START,END --format csv --output file.csv [--dry-run]
"""

import argparse
import csv
import json
import os
import platform
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

from credential_store import (
    CREDENTIALS_FILE,
    NOT_CONNECTED_MESSAGE,
    clear_credentials,
    load_credentials,
    mask_secret,
    mask_token,
    update_token,
)

# 边界限制常量
MAX_RANGE_DAYS = 365
MAX_HISTORY_YEARS = 3
MAX_CHAT_ROWS = 200
MAX_EXPORT_ROWS = 50000
DRY_RUN_PREVIEW_ROWS = 5

API_BASE_URL = os.environ.get("INSENTEK_API_BASE", "https://openapi.ecois.info")

AUTH_ERROR_CODES = {401, 403}


def auth_error_response(status: int | None = None):
    payload = {
        "success": False,
        "error": "authentication_required",
        "message": NOT_CONNECTED_MESSAGE,
    }
    if status is not None:
        payload["status"] = status
    return payload


def api_request(path, headers=None, params=None, method="GET", data=None, retry_auth=True, _refreshed=False):
    """
    发送 HTTP 请求并返回 JSON 响应。
    如果返回 401/403 且 retry_auth=True，会自动刷新 token 并重试一次。
    _refreshed 为内部标记，防止无限循环。
    """
    url = f"{API_BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    if data and method in ("POST", "PUT", "PATCH"):
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 认证失败，尝试刷新 token 后重试一次
        if retry_auth and e.code in AUTH_ERROR_CODES and not _refreshed:
            new_token = refresh_token()
            if new_token:
                # 替换 header 中的 token 并重试
                if headers and "Authorization" in headers:
                    headers["Authorization"] = new_token
                return api_request(path, headers=headers, params=params, method=method, data=data, retry_auth=False, _refreshed=True)
        if e.code in AUTH_ERROR_CODES:
            return auth_error_response(e.code)
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body)
        except json.JSONDecodeError:
            err = {"message": body}
        return {"_http_error": True, "status": e.code, "error": err}
    except Exception as e:
        return {"_http_error": True, "status": 0, "error": {"message": str(e)}}


def get_credentials(appid=None, secret=None):
    """
    获取凭据。
    仅允许从本地加密配置文件读取；不接受对话传入的 appid/secret。
    """
    if appid or secret:
        return None

    return load_credentials()


def fetch_token(appid=None, secret=None):
    """
    从 API 获取新 token。
    返回 (token, error_msg)
    """
    creds = get_credentials(appid, secret)
    if not creds:
        return None, NOT_CONNECTED_MESSAGE

    result = api_request("/v3/token", params={"appid": creds["appid"], "secret": creds["secret"]}, retry_auth=False)
    if result.get("error") == "authentication_required":
        return None, NOT_CONNECTED_MESSAGE
    if result.get("_http_error"):
        return None, NOT_CONNECTED_MESSAGE
    
    return result.get("token"), None


def refresh_token():
    """
    刷新 token：获取新 token 并保存到配置文件。
    返回新 token，失败返回 None。
    """
    token, error = fetch_token()
    if error:
        return None
    update_token(token)
    return token


def get_token(appid=None, secret=None):
    """
    获取 token。
    策略：
    1. 优先使用配置文件中的缓存 token
    2. 如果没有缓存 token，或缓存 token 为空，则获取新 token 并保存
    3. 如果缓存 token 使用失败（401/403），会自动刷新
    """
    creds = get_credentials(appid, secret)
    if not creds:
        return None, NOT_CONNECTED_MESSAGE
    cached_token = creds.get("token")
    if cached_token:
        return cached_token, None
    
    # 没有缓存 token，获取新 token 并保存
    token, error = fetch_token(appid, secret)
    if error:
        return None, error
    
    # 保存到配置文件
    update_token(token)
    return token, None


def authenticate(status=False, clear=False):
    """查看或清除本地凭据。写入/更新凭据请使用 npx @insentek/openapi-skill login。"""
    if clear:
        if clear_credentials():
            print(json.dumps({"success": True, "message": "凭据已清除"}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, "message": "没有已保存的凭据"}, ensure_ascii=False, indent=2))
        return

    if status:
        creds = load_credentials()
        if creds:
            print(json.dumps({
                "success": True,
                "connected": True,
                "appid": creds.get("appid"),
                "secret": mask_secret(creds.get("secret")),
                "token": mask_token(creds.get("token")),
                "token_updated_at": creds.get("token_updated_at"),
                "created_at": creds.get("created_at"),
                "encrypted": creds.get("encrypted", False),
                "config_path": str(CREDENTIALS_FILE)
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                "success": False,
                "connected": False,
                "message": NOT_CONNECTED_MESSAGE,
                "config_path": str(CREDENTIALS_FILE)
            }, ensure_ascii=False, indent=2))
        return

    print(json.dumps({
        "success": False,
        "error": "use_cli_login",
        "message": NOT_CONNECTED_MESSAGE
    }, ensure_ascii=False, indent=2))
    sys.exit(1)


def list_devices(token, page=1, limit=20):
    """查询设备列表。"""
    result = api_request("/v3/devices", headers={"Authorization": token}, params={"page": page, "limit": limit})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def get_device(token, sn):
    """查询单个设备详情及参数描述。"""
    detail = api_request(f"/v3/device/{sn}", headers={"Authorization": token})
    desc = api_request(f"/v3/device/{sn}/description", headers={"Authorization": token})
    print(json.dumps({"detail": detail, "description": desc}, ensure_ascii=False, indent=2))


def normalize_error(result):
    """
    把 api_request 的内部错误标记转换为统一的 {"success": false, ...} 形式。
    返回 dict 或 None（None 表示 result 没有错误）。
    """
    if not isinstance(result, dict):
        return None
    if result.get("error") == "authentication_required":
        return {
            "success": False,
            "error": "authentication_required",
            "message": result.get("message") or NOT_CONNECTED_MESSAGE,
        }
    if result.get("_validation_error"):
        return {
            "success": False,
            "error": "validation_error",
            "message": result.get("message") or "请求参数校验失败",
        }
    if result.get("_http_error"):
        err = result.get("error") or {}
        if isinstance(err, dict):
            message = err.get("message") or err.get("error") or f"HTTP {result.get('status')}"
        else:
            message = str(err)
        # 上游 WAF / 反代有时把 HTML 错误页直接返回；截断以避免上下文爆炸
        if isinstance(message, str) and len(message) > 500:
            message = message[:500] + "... [truncated]"
        return {
            "success": False,
            "error": "http_error",
            "status": result.get("status"),
            "message": message,
        }
    return None


def get_latest(token, sn):
    """查询设备实时数据 /v3/device/{sn}/latest。"""
    result = api_request(f"/v3/device/{sn}/latest", headers={"Authorization": token})
    err = normalize_error(result)
    if err is not None:
        print(json.dumps(err, ensure_ascii=False, indent=2))
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def parse_range(range_str):
    """解析 range 字符串为 (start_date, end_date)。"""
    parts = range_str.split(",")
    if len(parts) != 2:
        return None
    try:
        start = datetime.strptime(parts[0], "%Y%m%d").date()
        end = datetime.strptime(parts[1], "%Y%m%d").date()
        return start, end
    except ValueError:
        return None


def validate_range(range_str):
    """
    验证时间范围是否符合边界限制。
    返回 (ok: bool, error_msg: str, start_date, end_date)
    """
    parsed = parse_range(range_str)
    if parsed is None:
        return False, "时间范围格式错误，应为 YYYYMMDD,YYYYMMDD", None, None

    start, end = parsed
    today = date.today()

    if start > end:
        return False, "开始日期不能晚于结束日期", start, end

    span_days = (end - start).days + 1
    if span_days > MAX_RANGE_DAYS:
        return (
            False,
            f"查询跨度为 {span_days} 天，超过最大限制 {MAX_RANGE_DAYS} 天。"
            f"建议拆分为多次查询（如每次查询 3 个月），或缩小时间范围。",
            start,
            end,
        )

    max_history = today - timedelta(days=365 * MAX_HISTORY_YEARS)
    if end < max_history:
        return (
            False,
            f"结束日期 {end} 超过最大历史回溯限制（{MAX_HISTORY_YEARS} 年）。"
            f"最早支持查询到 {max_history.strftime('%Y-%m-%d')}。",
            start,
            end,
        )

    return True, "", start, end


def query_data(token, sn, range_str, include_params=None, include_nodes=None):
    """
    查询设备历史数据，含边界检查。
    返回原始 API 响应字典。
    """
    ok, err_msg, _, _ = validate_range(range_str)
    if not ok:
        return {"_validation_error": True, "message": err_msg}

    params = {"range": range_str}
    if include_params:
        params["includeParameters"] = include_params
    if include_nodes:
        params["includeNodes"] = include_nodes

    return api_request(f"/v3/device/{sn}/data", headers={"Authorization": token}, params=params)


def flatten_data(api_response):
    """
    将 API 嵌套结构扁平化为行列表，便于 JSON 导出。
    输入: {list: [{timestamp, datetime, values: {node: {param: value}}}]}
    输出: [{timestamp, datetime, node, param, value}, ...]
    """
    rows = []
    for item in api_response.get("list", []):
        ts = item.get("timestamp")
        dt = item.get("datetime")
        values = item.get("values", {})
        for node, params in values.items():
            for param, value in params.items():
                rows.append({
                    "timestamp": ts,
                    "datetime": dt,
                    "node": node,
                    "parameter": param,
                    "value": value,
                })
    return rows


def pivot_data(api_response, sn):
    """
    将 API 嵌套结构转换为宽格式（时间 × 参数）。
    输入: {list: [{timestamp, datetime, values: {node: {param: value}}}]}, sn
    输出: (fieldnames: [str], rows: [dict])
    每行代表一个时间点，列包括 SN、datetime、node 和各参数。
    """
    # 收集所有唯一的参数名（按字母序稳定排序）
    param_names = set()
    for item in api_response.get("list", []):
        for node, params in item.get("values", {}).items():
            param_names.update(params.keys())
    param_names = sorted(param_names)

    fieldnames = ["SN", "datetime", "node"] + param_names

    rows = []
    for item in api_response.get("list", []):
        dt = item.get("datetime")
        values = item.get("values", {})
        for node, params in values.items():
            row = {
                "SN": f"\t{sn}",
                "datetime": dt,
                "node": node,
            }
            for param in param_names:
                row[param] = params.get(param, "")
            rows.append(row)

    return fieldnames, rows


def dry_run_summary(result, sn, range_str):
    """
    生成 --dry-run 预览输出：数据条数、时间范围、字段摘要、前 N 条预览。
    不写入文件，仅输出结构化 JSON。
    """
    if result.get("_validation_error") or result.get("_http_error"):
        print(json.dumps({"success": False, "error": result.get("message") or result.get("error")}, ensure_ascii=False, indent=2))
        sys.exit(1)

    total = result.get("total", 0)
    flat = flatten_data(result)

    nodes = sorted(set(r["node"] for r in flat))
    params = sorted(set(r["parameter"] for r in flat))
    preview = flat[:DRY_RUN_PREVIEW_ROWS]

    output = {
        "dry_run": True,
        "total": total,
        "time_range": {
            "start": range_str.split(",")[0] if "," in range_str else "",
            "end": range_str.split(",")[1] if "," in range_str else ""
        },
        "fields": {
            "nodes": nodes,
            "parameters": params
        },
        "preview": preview,
        "message": f"Dry run: {total} records, {len(nodes)} nodes, {len(params)} parameters. First {len(preview)} rows shown. Use without --dry-run to export full data."
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def export_csv(token, sn, range_str, output_path, include_params=None, dry_run=False):
    """导出数据为 CSV 文件（宽格式：每行一个时间点，参数作为列）。"""
    result = query_data(token, sn, range_str, include_params)
    if result.get("_validation_error") or result.get("_http_error"):
        print(json.dumps({"success": False, "error": result.get("message") or result.get("error")}, ensure_ascii=False, indent=2))
        sys.exit(1)

    total = result.get("total", 0)
    if total > MAX_EXPORT_ROWS:
        print(json.dumps({
            "success": False,
            "error": f"数据量 {total} 条超过导出上限 {MAX_EXPORT_ROWS} 条，建议缩小时间范围或分批导出。"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if dry_run:
        dry_run_summary(result, sn, range_str)
        return

    fieldnames, rows = pivot_data(result, sn)
    if not rows:
        print(json.dumps({"success": True, "total": 0, "file": output_path, "message": "无数据"}, ensure_ascii=False, indent=2))
        return

    # UTF-8 BOM for Excel compatibility
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({
        "success": True,
        "total": total,
        "file": str(Path(output_path).resolve()),
        "message": f"成功导出 {total} 条数据到 {output_path}"
    }, ensure_ascii=False, indent=2))


def export_json(token, sn, range_str, output_path, include_params=None, dry_run=False):
    """导出原始 API 响应为 JSON 文件。"""
    result = query_data(token, sn, range_str, include_params)
    if result.get("_validation_error") or result.get("_http_error"):
        print(json.dumps({"success": False, "error": result.get("message") or result.get("error")}, ensure_ascii=False, indent=2))
        sys.exit(1)

    total = result.get("total", 0)
    if total > MAX_EXPORT_ROWS:
        print(json.dumps({
            "success": False,
            "error": f"数据量 {total} 条超过导出上限 {MAX_EXPORT_ROWS} 条，建议缩小时间范围或分批导出。"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if dry_run:
        dry_run_summary(result, sn, range_str)
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "success": True,
        "total": total,
        "file": str(Path(output_path).resolve()),
        "message": f"成功导出 {total} 条数据到 {output_path}"
    }, ensure_ascii=False, indent=2))


def check_environment(api_base=API_BASE_URL):
    """检查运行环境是否满足要求，返回结构化 JSON。"""
    results = {}
    script_dir = Path(__file__).parent.resolve()

    # 1. Python 版本
    py_version = sys.version_info
    py_ok = py_version >= (3, 10)
    results["python"] = {
        "ok": py_ok,
        "version": platform.python_version(),
        "executable": sys.executable,
        "message": f"Python {platform.python_version()} {'满足要求 (>=3.10)' if py_ok else '版本过低，需要 >=3.10（脚本使用了 PEP 604 联合类型语法）'}"
    }

    # 2. 核心脚本存在性
    cli_path = script_dir / "insentek_cli.py"
    results["scripts_cli"] = {
        "ok": cli_path.exists(),
        "path": str(cli_path) if cli_path.exists() else None,
        "message": "核心脚本 insentek_cli.py 已找到" if cli_path.exists() else "未找到 insentek_cli.py"
    }

    # 3. Excel 脚本存在性
    excel_path = script_dir / "export_excel.py"
    results["scripts_excel"] = {
        "ok": excel_path.exists(),
        "path": str(excel_path) if excel_path.exists() else None,
        "message": "Excel 脚本 export_excel.py 已找到" if excel_path.exists() else "未找到 export_excel.py（Excel 导出不可用）"
    }

    # 4. HTML 写入脚本存在性
    write_html_path = script_dir / "write_html.py"
    results["scripts_write_html"] = {
        "ok": write_html_path.exists(),
        "path": str(write_html_path) if write_html_path.exists() else None,
        "message": "HTML 写入脚本 write_html.py 已找到" if write_html_path.exists() else "未找到 write_html.py（HTML 报告写入不可用）"
    }

    # 5. openpyxl 依赖
    try:
        import openpyxl
        results["openpyxl"] = {
            "ok": True,
            "version": openpyxl.__version__,
            "message": f"openpyxl {openpyxl.__version__} 已安装，Excel 导出可用"
        }
    except ImportError:
        results["openpyxl"] = {
            "ok": False,
            "message": "openpyxl 未安装，Excel 导出不可用。安装命令: pip install openpyxl"
        }

    # 6. curl 可用性（fallback）
    try:
        subprocess.run(["curl", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        results["curl"] = {
            "ok": True,
            "message": "curl 可用，可作为脚本不可用时的 fallback"
        }
    except (FileNotFoundError, subprocess.CalledProcessError):
        results["curl"] = {
            "ok": False,
            "message": "curl 不可用，建议安装以保证 fallback 能力"
        }

    # 7. API 可达性（不带认证，只检查服务是否在线）
    try:
        req = urllib.request.Request(f"{api_base}/v3/token", method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            # 400 是正常的（缺少参数），说明服务在线
            results["api_reachable"] = {
                "ok": True,
                "status": resp.status,
                "message": f"API 服务可访问（HTTP {resp.status}）"
            }
    except urllib.error.HTTPError as e:
        # 400/401 说明服务在线只是缺少认证参数
        if e.code in (400, 401, 403):
            results["api_reachable"] = {
                "ok": True,
                "status": e.code,
                "message": f"API 服务可访问（HTTP {e.code}，未提供认证参数）"
            }
        else:
            results["api_reachable"] = {
                "ok": False,
                "status": e.code,
                "message": f"API 服务异常（HTTP {e.code}）"
            }
    except Exception as e:
        results["api_reachable"] = {
            "ok": False,
            "message": f"无法连接到 API 服务: {str(e)}"
        }

    creds = load_credentials()
    results["credentials"] = {
        "ok": creds is not None,
        "path": str(CREDENTIALS_FILE) if CREDENTIALS_FILE.exists() else None,
        "message": (
            f"Insentek API 已连接（appid: {creds.get('appid')}）"
            if creds else NOT_CONNECTED_MESSAGE
        ),
    }

    # 汇总
    critical_ok = results["python"]["ok"] and results["scripts_cli"]["ok"]
    all_ok = all(r["ok"] for r in results.values())

    output = {
        "success": critical_ok,
        "all_checks_passed": all_ok,
        "checks": results,
        "summary": {
            "critical": "通过" if critical_ok else "未通过",
            "optional": "全部通过" if all_ok else "部分未通过",
            "message": (
                "环境检查通过，所有功能可用。" if all_ok else
                "核心环境满足要求，但部分可选功能不可用。" if critical_ok else
                "核心环境未满足要求，请先安装 Python >=3.10 并确保脚本文件存在。"
            )
        }
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


def cmd_data(args):
    """data 子命令：查询数据并以 JSON 输出到 stdout。"""
    token = resolve_token(args.token)
    result = query_data(token, args.sn, args.range, args.include_params, args.include_nodes)
    if args.dry_run:
        dry_run_summary(result, args.sn, args.range)
        return
    err = normalize_error(result)
    if err is not None:
        print(json.dumps(err, ensure_ascii=False, indent=2))
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    global API_BASE_URL
    parser = argparse.ArgumentParser(description="Insentek OpenAPI CLI")
    parser.add_argument("--api-base", default=API_BASE_URL, help="API 基础 URL")
    sub = parser.add_subparsers(dest="command", required=True)

    # auth
    auth_p = sub.add_parser("auth", help="查看或清除本地凭据（配置请用 npx @insentek/openapi-skill login）")
    auth_p.add_argument("--status", action="store_true", help="查看当前保存的凭据状态")
    auth_p.add_argument("--clear", action="store_true", help="清除保存的凭据")

    # devices
    devs_p = sub.add_parser("devices", help="查询设备列表")
    devs_p.add_argument("--token", help="访问令牌（可选，如未提供则自动从配置获取）")
    devs_p.add_argument("--page", type=int, default=1)
    devs_p.add_argument("--limit", type=int, default=20)

    # device
    dev_p = sub.add_parser("device", help="查询设备详情")
    dev_p.add_argument("--token", help="访问令牌（可选，如未提供则自动从配置获取）")
    dev_p.add_argument("--sn", required=True)

    # latest
    latest_p = sub.add_parser("latest", help="查询设备实时数据 /v3/device/{sn}/latest")
    latest_p.add_argument("--token", help="访问令牌（可选，如未提供则自动从配置获取）")
    latest_p.add_argument("--sn", required=True)

    # data
    data_p = sub.add_parser("data", help="查询设备历史数据（含边界检查）")
    data_p.add_argument("--token", help="访问令牌（可选，如未提供则自动从配置获取）")
    data_p.add_argument("--sn", required=True)
    data_p.add_argument("--range", required=True, help="格式: YYYYMMDD,YYYYMMDD")
    data_p.add_argument("--include-params", default=None)
    data_p.add_argument("--include-nodes", default=None)
    data_p.add_argument("--dry-run", action="store_true", help="仅预览数据摘要，不输出全量数据")
    data_p.set_defaults(func=cmd_data)

    # export
    exp_p = sub.add_parser("export", help="导出数据为文件")
    exp_p.add_argument("--token", help="访问令牌（可选，如未提供则自动从配置获取）")
    exp_p.add_argument("--sn", required=True)
    exp_p.add_argument("--range", required=True)
    exp_p.add_argument("--format", choices=["csv", "json"], required=True)
    exp_p.add_argument("--output", required=True)
    exp_p.add_argument("--include-params", default=None)
    exp_p.add_argument("--dry-run", action="store_true", help="仅预览数据摘要，不写入文件")

    # check
    check_p = sub.add_parser("check", help="环境前置检查")
    check_p.add_argument("--api-base", default=API_BASE_URL, help="API 基础 URL")

    args = parser.parse_args()

    API_BASE_URL = args.api_base

    if args.command == "check":
        check_environment(args.api_base)
    elif args.command == "auth":
        if args.status or args.clear:
            authenticate(status=args.status, clear=args.clear)
        else:
            authenticate()
    elif args.command == "devices":
        token = resolve_token(args.token)
        list_devices(token, args.page, args.limit)
    elif args.command == "device":
        token = resolve_token(args.token)
        get_device(token, args.sn)
    elif args.command == "latest":
        token = resolve_token(args.token)
        get_latest(token, args.sn)
    elif args.command == "data":
        args.func(args)
    elif args.command == "export":
        token = resolve_token(args.token)
        if args.format == "csv":
            export_csv(token, args.sn, args.range, args.output, args.include_params, args.dry_run)
        elif args.format == "json":
            export_json(token, args.sn, args.range, args.output, args.include_params, args.dry_run)


def resolve_token(token_arg):
    """解析 token：优先使用命令行参数，其次自动获取。"""
    if token_arg:
        return token_arg
    token, error = get_token()
    if error:
        print(json.dumps({
            "success": False,
            "error": "authentication_required",
            "message": error,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    return token


if __name__ == "__main__":
    main()
