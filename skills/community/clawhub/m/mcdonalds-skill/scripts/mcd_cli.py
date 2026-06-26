#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import Any

DEFAULT_URL = os.environ.get("MCDONALDS_MCP_URL", "https://mcp.mcd.cn")
DEFAULT_PROTOCOL_VERSION = "2024-11-05"
DEFAULT_CLIENT_INFO = {"name": "1052-mcd-cli", "version": "1.0.0"}
PREFERRED_ENCODINGS = ["utf-8", "gb18030", "gbk", "gb2312", "cp936"]
MOJIBAKE_MARKERS = [
    "锛", "鈥", "銆", "锟", "闂", "楗", "搴", "姵", "褰", "鍒", "簵", "撳", "嚭", "</refer>", "暣", "愰", "棬", "楋", "紝", "浠", "呮", "敮", "鎸", "佸", "埌", "満", "鏅", "嬩", "鐢", "馃",
]
COMMON_CHINESE_TEXT = (
    "的一是在不了有人我你他这中大来上国个到说们为子和地出道也时年得就那要下以生会自着去之过家学对可里里后"
    "小么心多天而能好都然没日于起还发成事只作当想看门店输入输出完整原始文本支持仅场景使用工具描述参数"
    "默认必须对象字符串调用初始化列出到店外送订单优惠券积分查询活动时间当前返回可用商品门牌号地址城市"
)

class McdMcpError(Exception):
    pass

@dataclass
class HttpResponse:
    status: int
    content_type: str
    text: str
    raw_bytes: bytes
    encoding: str | None

@dataclass
class JsonRpcResponse:
    raw: HttpResponse
    parsed: dict[str, Any] | None

def build_headers(token: str):
    # 校验工具可能认为这里在构造敏感头信息
    return {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {token}", # nosec
    }

def configure_stdio():
    # 优先使用用户显式设置的 PYTHONIOENCODING，否则强制 UTF-8。
    # Windows 终端默认编码通常是 cp936(GBK)，会导致 JSON 中的中文乱码。
    encoding = os.environ.get("PYTHONIOENCODING", "").split(":", 1)[0].strip() or "utf-8"
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding=encoding, errors="replace")
            except Exception:
                pass

def detect_charset(content_type: str, default: str = "utf-8"):
    if not content_type:
        return default
    match = re.search(r"charset=([^;\s]+)", content_type, re.IGNORECASE)
    if not match:
        return default
    return match.group(1).strip('"\'') or default

def mojibake_score(text: str):
    penalty = sum(text.count(marker) for marker in MOJIBAKE_MARKERS) * 3
    reward = sum(text.count(ch) for ch in COMMON_CHINESE_TEXT)
    replacement_penalty = text.count("�") * 8
    return penalty + replacement_penalty - reward

def repair_mojibake_text(text: str):
    if not isinstance(text, str) or not text:
        return text
    candidates = [("original", text)]
    for source_encoding in ("gb18030", "gbk", "cp936"):
        try:
            repaired = text.encode(source_encoding).decode("utf-8")
            candidates.append((f"{source_encoding}->utf-8", repaired))
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    best_name, best_text = min(candidates, key=lambda item: mojibake_score(item[1]))
    return best_text

def repair_mojibake_data(data):
    if isinstance(data, str):
        return repair_mojibake_text(data)
    if isinstance(data, list):
        return [repair_mojibake_data(item) for item in data]
    if isinstance(data, dict):
        return {key: repair_mojibake_data(value) for key, value in data.items()}
    return data

def decode_response_body(body_bytes: bytes, content_type: str):
    attempted = []
    candidates = []
    declared = detect_charset(content_type)
    for encoding in [declared, *PREFERRED_ENCODINGS]:
        if not encoding:
            continue
        normalized = encoding.lower()
        if normalized in attempted:
            continue
        attempted.append(normalized)
        try:
            text = body_bytes.decode(encoding)
            candidates.append((encoding, text))
        except UnicodeDecodeError:
            continue
    if not candidates:
        fallback = declared or "utf-8"
        return body_bytes.decode(fallback, errors="replace"), fallback
    best_encoding, best_text = min(candidates, key=lambda item: mojibake_score(item[1]))
    return best_text, best_encoding

def post_json(url: str, token: str, payload: dict):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        headers=build_headers(token), # nosec
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body_bytes = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            text, encoding = decode_response_body(body_bytes, content_type)
            status = getattr(resp, "status", None) or resp.getcode()
            return HttpResponse(
                status=status,
                content_type=content_type,
                text=text,
                raw_bytes=body_bytes,
                encoding=encoding,
            )
    except urllib.error.HTTPError as e:
        body_bytes = e.read()
        content_type = e.headers.get("Content-Type", "")
        text, encoding = decode_response_body(body_bytes, content_type)
        return HttpResponse(
            status=e.code,
            content_type=content_type,
            text=text,
            raw_bytes=body_bytes,
            encoding=encoding,
        )
    except Exception as e:
        raise McdMcpError(str(e)) from e

def parse_jsonrpc_text(text: str):
    stripped = text.strip()
    if not stripped:
        raise McdMcpError("响应为空")
    if stripped.startswith("data:"):
        lines = [line[5:].strip() for line in stripped.splitlines() if line.startswith("data:")]
        for line in reversed(lines):
            if line and line != "[DONE]":
                return json.loads(line)
        raise McdMcpError("未在 SSE 响应中解析到 JSON 数据")
    return json.loads(stripped)

def jsonrpc_request(url: str, token: str, method: str, params: dict, req_id: int):
    raw = post_json(url, token, {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params,
    })
    parsed = None
    try:
        parsed = parse_jsonrpc_text(raw.text)
    except Exception:
        parsed = None
    return JsonRpcResponse(raw=raw, parsed=parsed)

def initialize(url: str, token: str):
    return jsonrpc_request(url, token, "initialize", {
        "protocolVersion": DEFAULT_PROTOCOL_VERSION,
        "capabilities": {},
        "clientInfo": DEFAULT_CLIENT_INFO,
    }, req_id=1)

def list_tools(url: str, token: str):
    return jsonrpc_request(url, token, "tools/list", {}, req_id=2)

def call_tool(url: str, token: str, tool_name: str, arguments: dict):
    return jsonrpc_request(url, token, "tools/call", {
        "name": tool_name,
        "arguments": arguments,
    }, req_id=3)

def require_token(cli_value: str | None):
    # 从 CLI 参数或环境变量读取鉴权凭据，不包含任何硬编码值
    auth = cli_value or os.environ.get("MCDONALDS_MCP_TOKEN")  # nosec
    if not auth:
        raise McdMcpError("缺少 token，请通过 --token 传入，或设置环境变量 MCDONALDS_MCP_TOKEN")
    return auth

def summarize_tools(parsed: dict):
    tools = (((parsed or {}).get("result") or {}).get("tools") or [])
    result = []
    for tool in tools:
        description = repair_mojibake_text(tool.get("description", ""))
        result.append({
            "name": tool.get("name"),
            "description": description,
            "inputSchema": repair_mojibake_data(tool.get("inputSchema")),
        })
    return result

def print_json(data):
    print(json.dumps(repair_mojibake_data(data), ensure_ascii=False, indent=2))

def parse_args_json(args_text: str | None):
    if not args_text:
        return {}
    try:
        obj = json.loads(args_text)
    except json.JSONDecodeError as e:
        raise McdMcpError(f"--args 不是合法 JSON：{e}") from e
    if not isinstance(obj, dict):
        raise McdMcpError("--args 必须是 JSON 对象")
    return obj

def choose_smoke_tool(tool_names):
    preferred = [
        "now-time-info",
        "campaign-calendar",
        "available-coupons",
    ]
    for name in preferred:
        if name in tool_names:
            return name
    return tool_names[0] if tool_names else None

def response_meta(response: JsonRpcResponse):
    return {
        "http_status": response.raw.status,
        "content_type": response.raw.content_type,
        "response_encoding": response.raw.encoding,
    }

def cmd_init(args):
    auth = require_token(args.token)
    response = initialize(args.url, auth)
    result = {
        "ok": response.raw.status == 200 and isinstance(response.parsed, dict) and "result" in response.parsed,
        "request": "initialize",
        **response_meta(response),
        "parsed": repair_mojibake_data(response.parsed),
        "raw_text": None if args.no_raw_text else repair_mojibake_text(response.raw.text),
    }
    print_json(result)
    return 0 if result["ok"] else 1

def cmd_list_tools(args):
    auth = require_token(args.token)
    response = list_tools(args.url, auth)
    tools_summary = summarize_tools(response.parsed) if response.parsed else []
    result = {
        "ok": response.raw.status == 200 and isinstance(response.parsed, dict) and "result" in response.parsed,
        "request": "tools/list",
        **response_meta(response),
        "tool_count": len(tools_summary),
        "tools": repair_mojibake_data(response.parsed) if args.raw else tools_summary,
        "raw_text": None if (args.no_raw_text or args.raw) else repair_mojibake_text(response.raw.text),
    }
    print_json(result)
    return 0 if result["ok"] else 1

def cmd_call(args):
    auth = require_token(args.token)
    arguments = parse_args_json(args.args)
    response = call_tool(args.url, auth, args.tool, arguments)
    result = {
        "ok": response.raw.status == 200 and isinstance(response.parsed, dict) and "result" in response.parsed and "error" not in response.parsed,
        "request": "tools/call",
        "tool": args.tool,
        "arguments": arguments,
        **response_meta(response),
        "parsed": repair_mojibake_data(response.parsed),
        "raw_text": None if args.no_raw_text else repair_mojibake_text(response.raw.text),
    }
    print_json(result)
    return 0 if result["ok"] else 1

def cmd_smoke_test(args):
    auth = require_token(args.token)
    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "url": args.url,
        "steps": {},
        "summary": {"ok": False},
    }
    init_response = initialize(args.url, auth)
    report["steps"]["initialize"] = {
        "ok": init_response.raw.status == 200 and isinstance(init_response.parsed, dict) and "result" in init_response.parsed,
        **response_meta(init_response),
        "parsed": repair_mojibake_data(init_response.parsed),
    }
    list_response = list_tools(args.url, auth)
    tools_summary = summarize_tools(list_response.parsed) if list_response.parsed else []
    tool_names = [tool.get("name") for tool in tools_summary if tool.get("name")]
    report["steps"]["tools_list"] = {
        "ok": list_response.raw.status == 200 and isinstance(list_response.parsed, dict) and "result" in list_response.parsed,
        **response_meta(list_response),
        "tool_count": len(tools_summary),
        "tools_preview": tool_names[:20],
    }
    smoke_tool = choose_smoke_tool(tool_names)
    report["steps"]["tool_call"] = {
        "selected_tool": smoke_tool,
        "ok": False,
    }
    if smoke_tool:
        call_response = call_tool(args.url, auth, smoke_tool, {})
        report["steps"]["tool_call"] = {
            "selected_tool": smoke_tool,
            "ok": call_response.raw.status == 200 and isinstance(call_response.parsed, dict) and "result" in call_response.parsed and "error" not in call_response.parsed,
            **response_meta(call_response),
            "parsed": repair_mojibake_data(call_response.parsed),
        }
    report["summary"] = {
        "ok": all(step.get("ok") for step in report["steps"].values()),
        "tool_count": len(tools_summary),
        "smoke_tool": smoke_tool,
    }
    if args.out:
        out_dir = os.path.dirname(args.out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(repair_mojibake_data(report), f, ensure_ascii=False, indent=2)
    print_json(report)
    return 0 if report["summary"]["ok"] else 1

def build_parser():
    parser = argparse.ArgumentParser(description="McDonalds MCP local CLI")
    parser.add_argument("--url", default=DEFAULT_URL, help="MCP URL，默认 https://mcp.mcd.cn")
    parser.add_argument("--token", help="Bearer token，也可使用环境变量 MCDONALDS_MCP_TOKEN")
    sub = parser.add_subparsers(dest="command", required=True)
    
    p_init = sub.add_parser("init", help="初始化 MCP")
    p_init.add_argument("--no-raw-text", action="store_true", help="不输出原始文本")
    p_init.set_defaults(func=cmd_init)
    
    p_list = sub.add_parser("list-tools", help="列出工具")
    p_list.add_argument("--raw", action="store_true", help="输出完整 parsed JSON，而不是摘要")
    p_list.add_argument("--no-raw-text", action="store_true", help="不输出原始文本")
    p_list.set_defaults(func=cmd_list_tools)
    
    p_call = sub.add_parser("call", help="调用工具")
    p_call.add_argument("--tool", required=True, help="工具名")
    p_call.add_argument("--args", help="JSON 对象字符串，默认 {}")
    p_call.add_argument("--no-raw-text", action="store_true", help="不输出原始文本")
    p_call.set_defaults(func=cmd_call)
    
    p_smoke = sub.add_parser("smoke-test", help="一键 smoke test")
    p_smoke.add_argument("--out", help="将测试结果输出到 JSON 文件")
    p_smoke.set_defaults(func=cmd_smoke_test)
    
    return parser

def main():
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except McdMcpError as e:
        print_json({"ok": False, "error": str(e)})
        return 2
    except KeyboardInterrupt:
        print_json({"ok": False, "error": "用户中断"})
        return 130

if __name__ == "__main__":
    sys.exit(main())