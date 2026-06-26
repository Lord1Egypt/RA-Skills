#!/usr/bin/env python3
"""
PPTUltra - AI 智能演示文稿生成引擎

Powered by pptultra.com
"""
import sys
import os
import json
import uuid
import time
import argparse
import re
import requests

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)
CONFIG_FILE = os.path.join(_SKILL_DIR, ".config.json")
HISTORY_FILE = os.path.join(_SKILL_DIR, ".history.json")
API_URL = "https://www.ultrappt.com/api/v1/agent/skill/chat"
TIMEOUT_SECONDS = 1800

_BRAND_BANNER = r"""
  ╔══════════════════════════════════════════════════════╗
  ║                                                      ║
  ║    ██████╗ ██████╗ ████████╗                         ║
  ║    ██╔══██╗██╔══██╗╚══██╔══╝                         ║
  ║    ██████╔╝██████╔╝   ██║                            ║
  ║    ██╔═══╝ ██╔═══╝    ██║                            ║
  ║    ██║     ██║        ██║                            ║
  ║    ╚═╝     ╚═╝        ╚═╝                            ║
  ║                  ✦ U l t r a ✦                       ║
  ║                                                      ║
  ║    AI-Powered Presentation Engine                    ║
  ║    https://pptultra.com                              ║
  ║                                                      ║
  ╚══════════════════════════════════════════════════════╝
"""

_BRAND_COMPLETE = r"""
  ╔══════════════════════════════════════════════════════╗
  ║  ✦ PPTUltra · 生成完成                               ║
  ╚══════════════════════════════════════════════════════╝"""

FLOW_CONFIGS = {
    "ppt": {
        "display_name": "通用PPT创作",
        "flow_id": "73687",
        "kwargs": {"src": "xie_n_cn"},
        "category": "generate",
        "result_mode": "generate_text",
        "requires_context": False,
    },
    "summary-report": {
        "display_name": "总结汇报",
        "flow_id": "70622",
        "kwargs": {"src": "xie_n_cn"},
        "category": "generate",
        "result_mode": "report_text",
        "requires_context": False,
    },
    "teaching-courseware": {
        "display_name": "教学课件",
        "flow_id": "77952",
        "kwargs": {"src": "xie_n_cn"},
        "category": "generate",
        "result_mode": "generate_text",
        "requires_context": False,
    },
    "public-speaking": {
        "display_name": "公众演讲",
        "flow_id": "70624",
        "kwargs": {"src": "xie_n_cn"},
        "category": "generate",
        "result_mode": "generate_text",
        "requires_context": False,
    },
    "restyle-all": {
        "display_name": "一键换风格",
        "flow_id": "69103",
        "kwargs": {"src": "xie_n_cn"},
        "category": "edit",
        "result_mode": "edit_text",
        "requires_context": True,
    },
    "translate-all": {
        "display_name": "一键换语种",
        "flow_id": "94281",
        "kwargs": {"src": "xie_n_cn"},
        "category": "edit",
        "result_mode": "edit_text",
        "requires_context": True,
    },
    "polish-text": {
        "display_name": "文本润色",
        "flow_id": "75779",
        "kwargs": {"src": "xie_n_cn"},
        "category": "edit",
        "result_mode": "edit_text",
        "requires_context": True,
    },
    "fact-check": {
        "display_name": "信息核验",
        "flow_id": "75483",
        "kwargs": {"src": "xie_n_cn"},
        "category": "edit",
        "result_mode": "edit_text",
        "requires_context": True,
    },
}
DEFAULT_FLOW_KEY = "ppt"


# ─────────────────────────────────────────
# API Key 管理
# ─────────────────────────────────────────

def load_api_key() -> str:
    """按优先级加载 API Key（环境变量 > 配置文件）"""
    # 1. 环境变量
    key = os.environ.get("PPT_API_KEY", "").strip()
    if key:
        return key
    # 2. 配置文件
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
                key = cfg.get("api_key", "").strip()
                if key:
                    return key
        except (json.JSONDecodeError, OSError):
            pass
    return ""


def save_api_key(api_key: str):
    """将 API Key 保存到配置文件"""
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
        except Exception:
            pass
    cfg["api_key"] = api_key
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    print("[配置] API Key 已保存")


def get_api_key(cli_key: str = "") -> str:
    """获取 API Key，优先级：命令行 > 环境变量 > 配置文件。当前无 Key 也允许继续请求。"""
    if cli_key:
        return cli_key
    key = load_api_key()
    if key:
        return key
    return ""


# ─────────────────────────────────────────
# 生成历史管理
# ─────────────────────────────────────────

def _save_history(flow_key: str, prompt: str, result: dict):
    """保存生成结果到历史文件，供后续编辑类功能读取。"""
    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "flow_key": flow_key,
        "prompt": prompt,
        "share_id": result.get("share_id", ""),
        "share_url": result.get("share_url", ""),
        "ppt_url": result.get("ppt_url", ""),
        "page_urls": result.get("page_urls", []),
        "summary": result.get("summary", ""),
    }
    history = _load_history_list()
    history.append(record)
    # 只保留最近 20 条
    history = history[-20:]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _load_history_list() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _load_last_history() -> dict | None:
    """读取最近一条有效的生成记录。"""
    history = _load_history_list()
    for record in reversed(history):
        if record.get("share_url") or record.get("ppt_url"):
            return record
    return None


# ─────────────────────────────────────────
# 内容提取工具
# ─────────────────────────────────────────

def _extract_share_id(text: str) -> str:
    if not text:
        return ""
    compact = re.sub(r"\s+", "", text)
    match = re.search(r"(?:[?&](?:id|key)=|\"(?:id|key|shareid|sharekey)\":\"|\b(?:id|key|shareid|sharekey)[:=])([a-f0-9]{32})", compact, re.IGNORECASE)
    return match.group(1) if match else ""


def _build_share_url(share_id: str) -> str:
    return f"https://ultrappt.com/share?id={share_id}&src=skill" if share_id else ""


def _extract_share_fields(value, result: dict):
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if isinstance(item, str):
                if lowered in {"share_url", "shareurl", "share_link", "sharelink", "jumpurl"}:
                    share_url = _recover_share_url(item) or item.strip()
                    if share_url and not result.get("share_url"):
                        result["share_url"] = share_url
                        result["share_id"] = result.get("share_id") or _extract_share_id(share_url)
                if lowered in {"shareid", "share_id", "key", "id", "sharekey"}:
                    share_id = _extract_share_id(item) or (item.strip() if re.fullmatch(r"[a-f0-9]{32}", item.strip(), re.IGNORECASE) else "")
                    if share_id and not result.get("share_id"):
                        result["share_id"] = share_id
                        result["share_url"] = result.get("share_url") or _build_share_url(share_id)
            elif isinstance(item, (dict, list)):
                _extract_share_fields(item, result)
        return
    if isinstance(value, list):
        for item in value:
            _extract_share_fields(item, result)


def _extract_urls(data: dict, result: dict):
    """从任意JSON中递归提取分享页与PPT相关URL"""
    _extract_share_fields(data, result)
    text = json.dumps(data, ensure_ascii=False)
    share_id = _extract_share_id(text)
    if share_id and not result.get("share_id"):
        result["share_id"] = share_id
        result["share_url"] = _build_share_url(share_id)

    urls = re.findall(r'https?://[^\s\'"]+', text)
    prefer_final_fields = bool(result.get("share_url"))
    for url in urls:
        if "ultrappt.com/share?" in url:
            if not result.get("share_url"):
                result["share_url"] = _recover_share_url(url)
                result["share_id"] = result["share_id"] or _extract_share_id(url)
            continue
        if url.endswith(".html") and ("xstore" in url or "mcp" in url or "ppt" in url.lower()):
            normalized_url = _normalize_recovered_url(url)
            if not normalized_url:
                continue
            if not prefer_final_fields and not result["ppt_url"]:
                result["ppt_url"] = normalized_url
            if not prefer_final_fields and normalized_url not in result["page_urls"]:
                result["page_urls"].append(normalized_url)


def _parse_json_string(value):
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None

    decoder = json.JSONDecoder(strict=False)
    original_text = text
    while text:
        if text[0] not in '{[':
            brace_positions = [pos for pos in (text.find('{'), text.find('[')) if pos >= 0]
            if not brace_positions:
                break
            text = text[min(brace_positions):]
        try:
            obj, _ = decoder.raw_decode(text)
            if isinstance(obj, str) and obj.strip() and obj != original_text:
                nested = _parse_json_string(obj)
                if nested is not None:
                    return nested
            return obj
        except json.JSONDecodeError:
            text = text[1:].lstrip()

    if original_text[:1] in {'"', "'"}:
        try:
            unescaped = json.loads(original_text, strict=False)
        except (json.JSONDecodeError, ValueError):
            unescaped = None
        if isinstance(unescaped, str) and unescaped.strip() and unescaped != original_text:
            nested = _parse_json_string(unescaped)
            if nested is not None:
                return nested
    return None


def _unwrap_zhiyue_candidate(value):
    current = _parse_json_string(value)
    visited = set()
    while isinstance(current, dict):
        marker = id(current)
        if marker in visited:
            break
        visited.add(marker)

        if current.get("url") or current.get("list"):
            return current

        for key in ("content", "result", "data"):
            nested_value = current.get(key)
            nested = _parse_json_string(nested_value)
            if nested is None and isinstance(nested_value, str):
                try:
                    nested = _parse_json_string(nested_value.encode("utf-8").decode("unicode_escape"))
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass
            if isinstance(nested, dict):
                current = nested
                break
        else:
            break
    return current if isinstance(current, dict) else None



def _iter_sse_events(response):
    event = {"event": "", "id": "", "retry": "", "data_lines": []}

    def flush_event():
        if not event["event"] and not event["id"] and not event["retry"] and not event["data_lines"]:
            return None
        flushed = {
            "event": event["event"],
            "id": event["id"],
            "retry": event["retry"],
            "data": "\n".join(event["data_lines"]),
        }
        event["event"] = ""
        event["id"] = ""
        event["retry"] = ""
        event["data_lines"] = []
        return flushed

    for raw_line in response.iter_lines(decode_unicode=True):
        line = raw_line if raw_line is not None else ""
        if line.endswith("\r"):
            line = line[:-1]

        if line == "":
            flushed = flush_event()
            if flushed is not None:
                yield flushed
            continue

        if line.startswith(":"):
            continue
        if line.startswith("event:"):
            event["event"] = line[6:].lstrip()
            continue
        if line.startswith("id:"):
            event["id"] = line[3:].lstrip()
            continue
        if line.startswith("retry:"):
            event["retry"] = line[6:].lstrip()
            continue
        if line.startswith("data:"):
            event["data_lines"].append(line[5:].lstrip())
            continue

        event["data_lines"].append(line)

    flushed = flush_event()
    if flushed is not None:
        yield flushed



def _looks_like_json_fragment(text: str) -> bool:
    if not isinstance(text, str):
        return False
    stripped = text.strip()
    if not stripped:
        return False
    return stripped.startswith(("{", "[", "data: {", "data: ["))



def _is_incomplete_json(text: str) -> bool:
    """检查文本是否是不完整的 JSON（开括号多于闭括号）"""
    if not text:
        return False
    opens = text.count("{") + text.count("[")
    closes = text.count("}") + text.count("]")
    return opens > closes and text.lstrip()[:1] in ("{", "[")


_XSTORE_URL_RE = re.compile(r"https?://[a-z0-9.-]*xstore[a-z0-9.-]*/mcp-yue-tool/[a-f0-9]{32}\.html", re.IGNORECASE)

_NOISE_LINE_RE = re.compile(
    r"^(?:DONE|\[DONE\]|ping|CONVERSATIONID[:#A-Z0-9_-]*|MESSAGEID[:#A-Z0-9_-]*"
    r"|思考下一步已确定下一步任务，即将执行.*|tool[_ -]?call.*|function[_ -]?call.*|```.*)$",
    re.IGNORECASE,
)


def _scan_raw_ppt_urls(raw_data: str, result: dict):
    """从原始 SSE 数据中正则提取 xstore HTML URL（兜底方案）。"""
    urls = _XSTORE_URL_RE.findall(raw_data)
    if not urls:
        return

    is_final = '"action":"final"' in raw_data or '"action": "final"' in raw_data
    is_replace = '"action":"replace"' in raw_data or '"action": "replace"' in raw_data

    for url in urls:
        if url not in result["page_urls"]:
            result["page_urls"].append(url)

    if (is_final or is_replace) and not result.get("ppt_url"):
        result["ppt_url"] = urls[-1]
        result["_structured_ppt_hit"] = True


def _iter_json_payloads(response):
    fragment_buffer = ""

    def flush_fragment_buffer(force=False):
        nonlocal fragment_buffer
        if not fragment_buffer:
            return None
        if not force and _is_incomplete_json(fragment_buffer):
            return None
        candidate = fragment_buffer.strip()
        fragment_buffer = ""
        return candidate or None

    for sse_event in _iter_sse_events(response):
        raw_data = sse_event.get("data", "")
        if not raw_data:
            flushed = flush_fragment_buffer()
            if flushed is not None:
                yield flushed
            continue

        normalized = raw_data.strip()
        if normalized.startswith("data:"):
            normalized = normalized[5:].lstrip()
        if not normalized:
            flushed = flush_fragment_buffer()
            if flushed is not None:
                yield flushed
            continue
        if normalized in ("[DONE]", "ping", "pong"):
            flushed = flush_fragment_buffer(force=True)
            if flushed is not None:
                yield flushed
            yield normalized
            continue
        if normalized.startswith(("CONVERSATIONID####", "MESSAGEID####")):
            flushed = flush_fragment_buffer(force=True)
            if flushed is not None:
                yield flushed
            yield normalized
            continue

        payload = normalized
        if fragment_buffer:
            payload = fragment_buffer + "\n" + normalized

        parsed = _parse_json_string(payload)
        if parsed is not None:
            fragment_buffer = ""
            yield payload
            continue

        if _looks_like_json_fragment(normalized) or fragment_buffer:
            fragment_buffer = payload
            continue

        flushed = flush_fragment_buffer(force=True)
        if flushed is not None:
            yield flushed
        yield normalized

    flushed = flush_fragment_buffer(force=True)
    if flushed is not None:
        yield flushed



STRICT_FLOW_RULES = {
    "ppt": {
        "agents": {"NewAllGenerate"},
        "tool": "zhiyue_html_batch_stream",
        "hit_key": "_structured_ppt_hit",
    },
    "summary-report": {
        "agents": {"NewAllGenerate"},
        "tool": "zhiyue_html_batch_stream",
        "hit_key": "_structured_ppt_hit",
    },
    "teaching-courseware": {
        "agents": {"NewAllGenerate"},
        "tool": "zhiyue_html_batch_stream",
        "hit_key": "_structured_ppt_hit",
    },
    "public-speaking": {
        "agents": {"NewAllGenerate"},
        "tool": "zhiyue_html_batch_stream",
        "hit_key": "_structured_ppt_hit",
    },
    "restyle-all": {
        "agents": {"EditAllGenerate"},
        "tool": "zhiyue_html_batch_stream",
        "hit_key": "_structured_ppt_hit",
    },
    "translate-all": {
        "agents": {"EditPartGenerate"},
        "tool": "zhiyue_html_edit",
        "hit_key": "_structured_ppt_hit",
    },
    "polish-text": {
        "agents": {"EditAllGenerate_2", "EditPartGenerate"},
        "tool": "zhiyue_data_format",
        "hit_key": "_strict_result_hit",
    },
    "fact-check": {
        "agents": {"chat"},
        "tool": "simple_summary",
        "hit_key": "_strict_result_hit",
    },
}



def _extract_zhiyue_ppt_result(payload, result: dict, expected_tool: str) -> bool:
    if not isinstance(payload, dict):
        return False

    has_expected_tool = payload.get("tool") == expected_tool and payload.get("status") == "success"
    candidate_sources = []
    if has_expected_tool:
        candidate_sources.append(payload.get("tool_respond"))
    candidate_sources.extend([
        payload.get("tool_respond"),
        payload.get("result"),
        payload.get("content"),
    ])

    message = payload.get("message")
    if isinstance(message, dict):
        if message.get("tool") == expected_tool and message.get("status") == "success":
            has_expected_tool = True
        candidate_sources.extend([
            message.get("tool_respond"),
            message.get("content"),
            message.get("result"),
        ])

    candidate = None
    for source in candidate_sources:
        candidate = _unwrap_zhiyue_candidate(source)
        if isinstance(candidate, dict):
            break
    if not isinstance(candidate, dict):
        return False
    if not (candidate.get("url") or candidate.get("list")):
        return False

    main_url = _normalize_recovered_url(candidate.get("url", ""))
    if main_url and not result.get("ppt_url"):
        result["ppt_url"] = main_url
    for item in candidate.get("list", []):
        if not isinstance(item, dict):
            continue
        url = _normalize_recovered_url(item.get("data", {}).get("url", ""))
        if item.get("errno", 1) == 0 and url and url not in result["page_urls"]:
            result["page_urls"].append(url)
    _extract_urls(candidate, result)
    if candidate.get("title"):
        result["_message_final_candidates"].append(str(candidate.get("title", "")).strip())
    if main_url:
        result["_message_final_candidates"].append(main_url)
    return bool(main_url or result["page_urls"] or result.get("share_url") or has_expected_tool)



def _extract_strict_text_result(payload, result: dict, expected_agents: set[str], expected_tool: str) -> bool:
    if not isinstance(payload, dict):
        return False
    agent_desc = str(payload.get("agent_desc", "")).strip()
    if expected_agents and agent_desc not in expected_agents:
        return False
    if payload.get("tool") != expected_tool or payload.get("status") != "success":
        return False

    tool_respond = payload.get("tool_respond")
    chunks = []
    parsed = _parse_json_string(tool_respond)
    if parsed is not None:
        _collect_text_chunks(parsed, chunks)
    if not chunks and isinstance(tool_respond, str) and tool_respond.strip():
        chunks.append(tool_respond.strip())

    cleaned_chunks = []
    for chunk in chunks:
        if isinstance(chunk, str):
            cleaned = clean_stream_text(chunk)
            if cleaned:
                cleaned_chunks.append(cleaned)
    if not cleaned_chunks:
        return False

    result["_strict_final_candidates"].extend(cleaned_chunks)
    return True



def _is_noise_ai_agent_message(message: dict) -> bool:
    if not isinstance(message, dict):
        return False
    if message.get("action") != "append":
        return False
    if str(message.get("agent_desc", "")).strip():
        return False
    content = message.get("content")
    return isinstance(content, str)



def _match_strict_flow_result(flow_key: str, message: dict, result: dict) -> bool:
    rule = STRICT_FLOW_RULES.get(flow_key)
    if not rule or not isinstance(message, dict):
        return False

    if flow_key in _STRUCTURED_PPT_FLOWS:
        hit = _extract_zhiyue_ppt_result(message, result, rule["tool"])
    else:
        hit = _extract_strict_text_result(message, result, rule["agents"], rule["tool"])

    if hit:
        result[rule["hit_key"]] = True
    return hit




def _collect_text_chunks(value, chunks: list):
    """从嵌套结构中提取文本片段"""
    if isinstance(value, str):
        text = value.strip()
        if text:
            chunks.append(text)
        return
    if isinstance(value, dict):
        for key in ("summary", "content", "text", "answer", "message", "delta", "output", "result"):
            if key in value:
                _collect_text_chunks(value[key], chunks)
        return
    if isinstance(value, list):
        for item in value:
            _collect_text_chunks(item, chunks)


def _extract_message_payload(message):
    if isinstance(message, dict):
        return message
    if isinstance(message, str):
        parsed = _parse_json_string(message)
        if isinstance(parsed, dict):
            return parsed
    return None


def _collect_message_result_candidates(flow_key: str, message, result: dict) -> dict:
    status = {"structured": False, "text": False, "tail": False}
    payload = _extract_message_payload(message)

    if isinstance(message, str) and message.strip():
        result["_raw_messages"].append(message.strip())

    if payload is None:
        return status

    if flow_key == "ppt" and _extract_zhiyue_ppt_result(payload, result, STRICT_FLOW_RULES["ppt"]["tool"]):
        status["structured"] = True

    for key in ("content", "text", "answer", "result", "output", "message", "delta"):
        value = payload.get(key)
        if value in (None, ""):
            continue

        parsed_value = _parse_json_string(value)
        if flow_key == "ppt" and isinstance(parsed_value, dict):
            if _extract_zhiyue_ppt_result(parsed_value, result, STRICT_FLOW_RULES["ppt"]["tool"]):
                status["structured"] = True

        chunks = []
        if parsed_value is not None:
            _collect_text_chunks(parsed_value, chunks)
        else:
            _collect_text_chunks(value, chunks)

        for chunk in chunks:
            if not isinstance(chunk, str):
                continue
            cleaned = clean_stream_text(chunk)
            if not cleaned:
                continue
            result["_message_final_candidates"].append(cleaned)
            status["text"] = True
            if "技能调用结果" in cleaned or "我已经为您生成" in cleaned:
                status["tail"] = True

    return status


def _normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def _repair_mojibake(text: str) -> str:
    if not text:
        return ""
    suspicious = ("æ", "ç", "è", "é", "ï", "â", "ã", "å", "ä", "ð", "Ð")
    if not any(token in text for token in suspicious):
        return text
    try:
        repaired = text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
    return repaired if repaired.count("�") <= text.count("�") else text


def _looks_like_url_fragment(line: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+", line))


def _merge_fragment_lines(lines: list[str]) -> list[str]:
    merged = []
    buffer = []

    def flush_buffer():
        if not buffer:
            return
        merged.append("".join(buffer))
        buffer.clear()

    for line in lines:
        token = line.strip()
        if not token:
            flush_buffer()
            continue
        if token.lower() in {"http", "https", "://", ".html", "www", "cn", "com", "net", "org"} or _looks_like_url_fragment(token):
            buffer.append(token)
            continue
        if len(token) <= 12 and re.fullmatch(r"[A-Za-z0-9_-]+", token):
            buffer.append(token)
            continue
        flush_buffer()
        merged.append(token)
    flush_buffer()
    return merged


def _extract_urls_from_text(text: str) -> list[str]:
    compact = re.sub(r"\s+", "", text)
    urls = [
        _normalize_recovered_url(url)
        for url in re.findall(r"https?://[^\s\"'<>]+?\.html", compact)
    ]
    return [url for url in urls if url]


def _is_valid_ppt_host(url: str) -> bool:
    match = re.match(r"^https?://([^/]+)/", url, re.IGNORECASE)
    if not match:
        return False
    host = match.group(1).lower()
    if host.endswith(".xstore.qihu.com"):
        return True
    return False


def _normalize_recovered_url(url: str) -> str:
    if not url:
        return ""
    normalized = url.strip().strip('"\'')
    normalized = re.sub(r"^https?://URL", "https://", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"^URL", "", normalized, flags=re.IGNORECASE)
    if normalized.startswith(("http://", "https://")) and normalized.endswith(".html") and not _is_valid_ppt_host(normalized):
        return ""
    return normalized


def _recover_ppt_url(text: str) -> str:
    compact = re.sub(r"\s+", "", text)
    match = re.search(r"((?:https?://)?(?:URL)?[a-z0-9.-]*xstore(?:\.[a-z0-9.-]+)*/[a-z0-9/_-]*mcp[a-z0-9/_-]*\.html)", compact, re.IGNORECASE)
    if not match:
        return ""
    url = match.group(1)
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    normalized = _normalize_recovered_url(url)
    return normalized if _is_valid_ppt_host(normalized) else ""


def _recover_share_url(text: str) -> str:
    share_id = _extract_share_id(text)
    if share_id:
        return _build_share_url(share_id)
    compact = re.sub(r"\s+", "", text)
    match = re.search(r"https?://ultrappt\.com/share\?(?:id|key)=[a-f0-9]{32}", compact, re.IGNORECASE)
    if not match:
        return ""
    return _build_share_url(_extract_share_id(match.group(0)))


def _specialize_candidate(flow_key: str, text: str) -> str:
    if not text:
        return ""

    specialized = text
    if flow_key == "ppt":
        specialized = re.sub(r"<seed[_a-z-]*>.*?</seed[_a-z-]*>", "", specialized, flags=re.IGNORECASE | re.DOTALL)
        lines = []
        for line in specialized.splitlines():
            normalized = line.strip()
            if not normalized:
                continue
            lowered = normalized.lower()
            if lowered in {"glitch", "blob", "false", "true"}:
                continue
            if re.search(r"seed|function|parameter|rootz-index|unapplied_experience", lowered):
                continue
            lines.append(normalized)
        tail = "\n".join(lines[-30:]).strip()
        final_hint = re.findall(r"我已经为您生成[^\n]+最终结果", tail)
        share_url = _recover_share_url(tail)
        share_id = _extract_share_id(tail)
        recovered_url = _recover_ppt_url(tail)
        parts = []
        if final_hint:
            parts.append(final_hint[-1])
        if share_url:
            parts.append(f"分享页：{share_url}")
        # 不再输出 share_id 和 xstore 内部 URL
        if parts:
            return "\n".join(parts)
        return tail

    if flow_key == "summary-report":
        lines = []
        for line in specialized.splitlines():
            normalized = line.strip()
            if not normalized:
                continue
            lowered = normalized.lower()
            if re.search(r"^图片\d+", normalized):
                continue
            if any(token in lowered for token in ("width", "height", "site=", "seedream", "图片", ".jpg", ".png", "比例")):
                continue
            if re.search(r"https?://|t0[0-9a-f]{6,}", lowered):
                continue
            lines.append(normalized)
        filtered = "\n".join(lines[-40:]).strip()
        final_hint = re.findall(r"我已经为您生成[^\n]+最终结果", specialized)
        if final_hint:
            if filtered:
                return filtered + "\n" + final_hint[-1]
            return final_hint[-1]
        return filtered

    if flow_key == "polish-text":
        lines = []
        in_operations = False
        for line in specialized.splitlines():
            normalized = line.strip()
            if not normalized:
                continue
            lowered = normalized.lower()
            if normalized.startswith("## operations"):
                in_operations = True
                lines.append(normalized)
                continue
            if normalized.startswith("## 整体PPT"):
                in_operations = False
                continue
            if any(token in lowered for token in ("原始ppt", "修改后未提供有效url", '"size"', '"input"', 'json')):
                continue
            if in_operations or normalized.startswith("### operation") or normalized.startswith("op:") or normalized.startswith("target:") or normalized.startswith("pages:"):
                lines.append(normalized)
        return "\n".join(lines[-30:]).strip()

    return specialized


def _is_garbled_line(line: str) -> bool:
    if len(line) < 12:
        return False
    strange_chars = sum(1 for ch in line if ord(ch) == 65533 or (not ch.isalnum() and ch not in "，。！？；：,.!?;:()（）[]【】{}<>《》\"'“”‘’、-_/\\|@#%&*+=~` \t" and not ('\u4e00' <= ch <= '\u9fff')))
    return strange_chars / max(len(line), 1) > 0.35


def clean_stream_text(text: str) -> str:
    """对流式文本做最小必要清洗"""
    if not text:
        return ""

    repaired_text = _repair_mojibake(text)
    lines = []
    seen = set()

    for raw_line in repaired_text.splitlines():
        line = _repair_mojibake(raw_line.strip())
        if not line:
            continue
        if _NOISE_LINE_RE.match(line):
            continue
        normalized = _normalize_line(line)
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered in {"tool", "call", "blob", "done"}:
            continue
        if _is_garbled_line(normalized):
            continue
        if normalized in seen:
            continue
        if len(set(normalized)) <= 2 and len(normalized) > 20:
            continue
        seen.add(normalized)
        lines.append(normalized)

    if not lines:
        return ""

    merged_lines = _merge_fragment_lines(lines)
    tail_lines = merged_lines[-80:]
    return "\n".join(tail_lines).strip()


def _extract_attachment_payloads(attachments, result: dict):
    for attachment in attachments or []:
        payload = attachment.get("payload", "")
        if not payload:
            continue
        result["_attachments"].append(attachment)
        if not isinstance(payload, str):
            continue
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            cleaned = clean_stream_text(payload)
            if cleaned:
                result["_final_candidates"].append(cleaned)
            continue

        if isinstance(payload_data, dict):
            if payload_data.get("url") or payload_data.get("list"):
                result["ppt_url"] = result["ppt_url"] or payload_data.get("url", "")
                for item in payload_data.get("list", []):
                    url = item.get("data", {}).get("url")
                    if item.get("errno", 1) == 0 and url and url not in result["page_urls"]:
                        result["page_urls"].append(url)
            chunks = []
            _collect_text_chunks(payload_data, chunks)
            result["_final_candidates"].extend(chunks)


def _truncate_text(text: str, limit: int = 600) -> str:
    if not text or len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...(已截断)"


_STRUCTURED_PPT_FLOWS = {"ppt", "summary-report", "teaching-courseware", "public-speaking", "restyle-all", "translate-all"}

_FLOW_DISPLAY_PREFIX = {
    "ppt": "生成成功",
    "summary-report": "总结汇报已生成",
    "teaching-courseware": "教学课件已生成",
    "public-speaking": "演讲PPT已生成",
    "restyle-all": "风格切换已完成",
    "translate-all": "语种切换已完成",
}


_INTERNAL_URL_RE = re.compile(
    r"https?://[a-z0-9.-]*(?:xstore|qihu)[a-z0-9.-]*/[^\s））\]]*",
    re.IGNORECASE,
)


_SANITIZE_SKIP_PREFIXES = ("HTML URL：", "HTML 原始页")


def _sanitize_user_output(text: str, extra_skip_prefixes: tuple[str, ...] = ()) -> str:
    """统一过滤用户可见文本中的内部 URL 和标识符。"""
    if not text:
        return text
    skip = _SANITIZE_SKIP_PREFIXES + extra_skip_prefixes
    lines = []
    seen = set()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if _INTERNAL_URL_RE.fullmatch(stripped):
            continue
        if stripped.startswith(skip):
            continue
        if _XSTORE_URL_RE.search(stripped):
            continue
        cleaned = _INTERNAL_URL_RE.sub("", line).strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            lines.append(cleaned)
    return "\n".join(lines).strip()


def _format_final_output(flow_key: str, result: dict) -> dict:
    summary = result.get("summary", "").strip()

    if flow_key in _STRUCTURED_PPT_FLOWS:
        prefix = _FLOW_DISPLAY_PREFIX.get(flow_key, "生成成功")
        if result.get("_structured_ppt_hit"):
            lines = [prefix]
            if result.get("share_url"):
                lines.append(f"- PPT访问链接（推荐）：{result['share_url']}")
            if summary:
                cleaned_summary = summary
                for p in _FLOW_DISPLAY_PREFIX.values():
                    if cleaned_summary.startswith(p):
                        cleaned_summary = cleaned_summary[len(p):].strip()
                cleaned_summary = _sanitize_user_output(
                    cleaned_summary,
                    extra_skip_prefixes=("分享页：", "分享 ID：", "PPT访问链接（推荐）："),
                )
                if cleaned_summary:
                    lines.append("- 结果摘要：")
                    lines.append(_truncate_text(cleaned_summary, 400))
            result["summary"] = "\n".join(lines).strip()
            return result
        if summary:
            result["summary"] = _sanitize_user_output(prefix + "\n" + _truncate_text(summary, 500))
        return result

    if flow_key == "polish-text":
        if summary:
            result["summary"] = _sanitize_user_output("文本润色结果\n" + _truncate_text(summary, 500))
        return result

    result["summary"] = _sanitize_user_output(_truncate_text(summary, 600))
    return result


def finalize_result(flow_config: dict, result: dict) -> dict:
    """统一从收集到的候选结果中产出最终摘要"""
    flow_key = flow_config.get("flow_key", "")
    structured_hit = bool(result.get("_structured_ppt_hit"))
    strict_hit = bool(result.get("_strict_result_hit"))

    def prepare_candidates(values) -> list[str]:
        prepared = []
        for value in values:
            if isinstance(value, str):
                cleaned = clean_stream_text(value)
                specialized = _specialize_candidate(flow_key, cleaned)
                if specialized:
                    prepared.append(specialized)
        return prepared

    strict_candidates = prepare_candidates(result.get("_strict_final_candidates", []))
    message_candidates = prepare_candidates(result.get("_message_final_candidates", []))
    final_candidates = prepare_candidates(result.get("_final_candidates", []))
    raw_message_candidates = prepare_candidates(result.get("_raw_messages", []))

    text_chunk_candidates = []
    joined_chunks = clean_stream_text("\n".join(result.get("_text_chunks", [])))
    specialized_chunks = _specialize_candidate(flow_key, joined_chunks)
    if specialized_chunks:
        text_chunk_candidates.append(specialized_chunks)

    # ── chat 流累积文本：修复 mojibake 后作为高优候选 ──
    # 只取有明确 agent_desc 的桶，_default（空 agent_desc）通常是中间处理噪音
    chat_candidates = []
    for acc_key, fragments in result.get("_chat_accumulators", {}).items():
        if not fragments or acc_key == "_default":
            continue
        joined = "".join(fragments)
        repaired = _repair_mojibake(joined)
        cleaned = clean_stream_text(repaired)
        if cleaned and len(cleaned) > 20:
            chat_candidates.append(cleaned)

    candidates = message_candidates + final_candidates + raw_message_candidates + text_chunk_candidates

    if flow_key not in _STRUCTURED_PPT_FLOWS or structured_hit:
        for candidate in strict_candidates + candidates:
            share_id = _extract_share_id(candidate)
            share_url = _recover_share_url(candidate)
            if share_id and not result.get("share_id"):
                result["share_id"] = share_id
            if share_url and not result.get("share_url"):
                result["share_url"] = share_url

    if flow_key not in _STRUCTURED_PPT_FLOWS:
        candidate_urls = []
        for candidate in strict_candidates + candidates:
            candidate_urls.extend(_extract_urls_from_text(candidate))
            recovered_url = _recover_ppt_url(candidate)
            if recovered_url:
                candidate_urls.append(recovered_url)
        for url in candidate_urls:
            if result.get("share_url"):
                break
            if not result["ppt_url"]:
                result["ppt_url"] = url
            if url not in result["page_urls"]:
                result["page_urls"].append(url)

    def candidate_score(text: str) -> tuple:
        share_bonus = (3 if _recover_share_url(text) else 0) + (2 if _extract_share_id(text) else 0)
        url_bonus = len(_extract_urls_from_text(text)) + (1 if _recover_ppt_url(text) else 0)
        chinese_chars = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
        mojibake_penalty = sum(text.count(token) for token in ("æ", "ç", "è", "é", "ï", "â", "ã", "å", "ä"))
        final_hint_bonus = 2 if "我已经为您生成" in text else 0
        result_block_bonus = 3 if "技能调用结果" in text else 0
        share_line_bonus = 2 if any(token in text for token in ("分享 ID：", "分享页：", "HTML URL：", "PPT访问链接（推荐）：")) else 0
        noise_penalty = 2 if any(token in text.lower() for token in ("width", "height", "site=", ".jpg", ".png")) else 0
        return (share_bonus, result_block_bonus, final_hint_bonus, share_line_bonus, url_bonus, chinese_chars, -noise_penalty, -mojibake_penalty, len(text))

    mode = flow_config.get("result_mode", "auto")
    if strict_hit and strict_candidates:
        result["summary"] = max(strict_candidates, key=candidate_score)
    elif chat_candidates and not structured_hit:
        # 结构化 PPT 已命中时不用 chat 累积文本（那些是 agent 处理噪音）
        result["summary"] = max(chat_candidates, key=candidate_score)
    elif message_candidates:
        result["summary"] = max(message_candidates, key=candidate_score)
    elif mode in {"report_text", "edit_text", "generate_text", "auto"}:
        ordered_candidates = final_candidates + raw_message_candidates + text_chunk_candidates
        if ordered_candidates:
            result["summary"] = max(ordered_candidates, key=candidate_score)

    # 兜底：从 ppt_url 文件名提取 share_id 并构建分享链接
    if not result.get("share_id") and result.get("ppt_url"):
        match = re.search(r"/([a-f0-9]{32})\.html", result["ppt_url"], re.IGNORECASE)
        if match:
            result["share_id"] = match.group(1)
            result["share_url"] = _build_share_url(match.group(1))

    result = _format_final_output(flow_key, result)
    for key in (
        "_text_chunks", "_raw_messages", "_final_candidates",
        "_message_final_candidates", "_strict_final_candidates",
        "_attachments", "_chat_accumulators",
        "_structured_ppt_hit", "_strict_result_hit",
    ):
        result.pop(key, None)
    return result


def build_prompt(flow_config: dict, user_prompt: str, current_ppt: str = "", operations: str = "", size: str = "") -> str:
    """根据 flow 类型组装最小输入 prompt"""
    if flow_config.get("category") != "edit":
        return user_prompt

    sections = [f"## 当前问题\n{user_prompt.strip()}"]
    if operations.strip():
        sections.append(f"## 操作说明\n{operations.strip()}")
    if current_ppt.strip() or size.strip():
        ppt_section = []
        if size.strip():
            ppt_section.append(f"当前PPT的尺寸为 {size.strip()}")
        if current_ppt.strip():
            ppt_section.append(current_ppt.strip())
        sections.append("## 当前PPT\n" + "\n".join(ppt_section))
    return "\n\n".join(sections).strip()


# ─────────────────────────────────────────
# PPT 生成主逻辑
# ─────────────────────────────────────────

def get_flow_config(flow_key: str) -> dict:
    config = FLOW_CONFIGS.get(flow_key)
    if not config:
        supported = ", ".join(sorted(FLOW_CONFIGS.keys()))
        raise ValueError(f"不支持的功能: {flow_key}。可选值: {supported}")
    merged = dict(config)
    merged["flow_key"] = flow_key
    return merged


def generate_ppt(
    prompt: str,
    api_key: str,
    flow_key: str = DEFAULT_FLOW_KEY,
    current_ppt: str = "",
    operations: str = "",
    size: str = "",
) -> dict:
    """
    调用流式API执行指定 flow，收集完整输出。
    Returns: dict包含 summary、ppt_url、page_urls
    """
    flow_config = get_flow_config(flow_key)
    final_prompt = build_prompt(flow_config, prompt, current_ppt=current_ppt, operations=operations, size=size)
    request_id = uuid.uuid4().hex
    headers = {
        "Request-Id": request_id,
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Qid"] = api_key
    payload = {
        "ai_agent_flow_id": flow_config["flow_id"],
        "prompt": final_prompt,
        "kwargs": dict(flow_config.get("kwargs", {})),
    }

    print(f"正在生成{flow_config['display_name']}，请耐心等待...\n")

    result = {
        "summary": "",
        "ppt_url": "",
        "share_id": "",
        "share_url": "",
        "page_urls": [],
        "_text_chunks": [],
        "_raw_messages": [],
        "_final_candidates": [],
        "_message_final_candidates": [],
        "_strict_final_candidates": [],
        "_attachments": [],
        "_chat_accumulators": {},
        "_structured_ppt_hit": False,
        "_strict_result_hit": False,
    }
    start_time = time.time()
    chunk_count = 0

    try:
        with requests.post(
            API_URL, headers=headers, json=payload,
            stream=True, timeout=TIMEOUT_SECONDS,
        ) as response:
            response.raise_for_status()
            # SSE Content-Type 通常为 text/event-stream 不带 charset，
            # requests 默认回退 ISO-8859-1 导致中文乱码，强制 UTF-8。
            response.encoding = "utf-8"

            for raw_data in _iter_json_payloads(response):
                elapsed = time.time() - start_time
                if not raw_data or raw_data in ("[DONE]", "ping", "pong"):
                    continue

                chunk_count += 1

                # 兜底：JSON 解析前先用正则扫描 xstore URL
                if flow_key in _STRUCTURED_PPT_FLOWS and "xstore" in raw_data:
                    _scan_raw_ppt_urls(raw_data, result)

                parsed = _parse_json_string(raw_data)
                if parsed is None:
                    continue
                data = parsed

                if not isinstance(data, dict):
                    continue

                event_type = data.get("type", "")
                action = data.get("action", "")

                # ── 格式1: agentSimpleResult (agent 69418风格) ──
                if event_type == "agentSimpleResult" and action == "final":
                    summary = data.get("summary", "")
                    if isinstance(summary, str) and summary.strip():
                        result["_final_candidates"].append(summary)
                    _extract_attachment_payloads(data.get("attachments", []), result)

                # ── 格式2: ai_agent流式 (agent 73687风格) ──
                if event_type == "ai_agent":
                    message = data.get("message")
                    strict_hit = False
                    allow_fallback = True
                    if isinstance(message, dict):
                        agent_desc = str(message.get("agent_desc", "")).strip()
                        msg_type = str(message.get("type", "")).strip()
                        msg_action = str(message.get("action", "")).strip()

                        # ── chat 流式累积：逐字符流的 content 按 agent_desc 分桶 ──
                        if msg_type == "chat" and msg_action == "append":
                            chat_content = message.get("content", "")
                            if isinstance(chat_content, str) and chat_content:
                                acc_key = agent_desc or "_default"
                                acc = result["_chat_accumulators"]
                                if acc_key not in acc:
                                    acc[acc_key] = []
                                acc[acc_key].append(chat_content)

                        strict_hit = _match_strict_flow_result(flow_key, message, result)
                        if strict_hit:
                            if flow_key in _STRUCTURED_PPT_FLOWS:
                                result["share_id"] = result.get("share_id") or _extract_share_id(result.get("ppt_url", ""))
                                if result.get("share_id") and not result.get("share_url"):
                                    result["share_url"] = _build_share_url(result["share_id"])
                        elif _is_noise_ai_agent_message(message):
                            allow_fallback = False

                        if message.get("type") == "toolStatus":
                            share_url = message.get("share_url", "")
                            if isinstance(share_url, str) and share_url.strip() and not result.get("share_url"):
                                result["share_url"] = share_url.strip()
                                result["share_id"] = result.get("share_id") or _extract_share_id(share_url)
                            final_url = message.get("url", "")
                            if isinstance(final_url, str) and final_url.strip() and not strict_hit:
                                result["_final_candidates"].append(final_url.strip())

                        if agent_desc == "chatMarkdown" and allow_fallback:
                            for attachment in message.get("attachments", []) or []:
                                if attachment.get("type") != "attachments" or attachment.get("status") != "success":
                                    continue
                                content = attachment.get("content")
                                if isinstance(content, str) and content.strip():
                                    result["_message_final_candidates"].append(content.strip())

                    if allow_fallback:
                        _collect_message_result_candidates(flow_key, message, result)

                        chunks = []
                        for key in ("content", "text", "answer", "message", "delta", "output", "result"):
                            if key in data:
                                _collect_text_chunks(data.get(key), chunks)
                        if chunks:
                            result["_text_chunks"].extend(chunks)
                        if isinstance(data.get("message"), str) and data.get("message", "").strip():
                            result["_raw_messages"].append(data["message"])

                # ── 格式2b: 无type包装的message事件 ──
                # 服务端对 zhiyue_html_batch_stream 返回的事件外层为
                # {"message": {"agent_desc":"NewAllGenerate","content":"...", ...}}
                # 不含 "type":"ai_agent"，需要单独处理。
                if not event_type and flow_key in _STRUCTURED_PPT_FLOWS:
                    message = data.get("message")
                    if isinstance(message, dict):
                        agent_desc = str(message.get("agent_desc", "")).strip()
                        msg_action = str(message.get("action", "")).strip()
                        content_raw = message.get("content")

                        # 尝试从 message.content 解析内嵌 JSON（PPT 结构化数据）
                        content_parsed = None
                        if isinstance(content_raw, str) and content_raw.strip():
                            content_parsed = _parse_json_string(content_raw)

                        if isinstance(content_parsed, dict) and (content_parsed.get("url") or content_parsed.get("list")):
                            # action=final 包含完整 list + url
                            if content_parsed.get("action") == "final" or msg_action == "final":
                                main_url = _normalize_recovered_url(content_parsed.get("url", ""))
                                if main_url and not result.get("ppt_url"):
                                    result["ppt_url"] = main_url
                                for item in content_parsed.get("list", []):
                                    if isinstance(item, dict):
                                        url = _normalize_recovered_url(item.get("data", {}).get("url", ""))
                                        if item.get("errno", 1) == 0 and url and url not in result["page_urls"]:
                                            result["page_urls"].append(url)
                                _extract_urls(content_parsed, result)
                                result["_structured_ppt_hit"] = True

                            # action=replace 包含合并后的 url
                            elif content_parsed.get("action") == "replace" or msg_action == "replace":
                                url = _normalize_recovered_url(content_parsed.get("url", ""))
                                if url and not result.get("ppt_url"):
                                    result["ppt_url"] = url
                                    result["_structured_ppt_hit"] = True

                            # action=append 包含逐页 URL
                            elif content_parsed.get("action") == "append":
                                for item in content_parsed.get("list", []):
                                    if isinstance(item, dict):
                                        url = _normalize_recovered_url(item.get("data", {}).get("url", ""))
                                        if item.get("errno", 1) == 0 and url and url not in result["page_urls"]:
                                            result["page_urls"].append(url)

                            # 提取标题
                            title = content_parsed.get("title", "")
                            if title and isinstance(title, str):
                                result["_message_final_candidates"].append(title.strip())

                # ── progress 事件补充候选结果 ──
                if event_type == "progress":
                    for key in ("content", "text", "answer", "result"):
                        if key in data:
                            chunks = []
                            _collect_text_chunks(data.get(key), chunks)
                            result["_final_candidates"].extend(chunks)

                # ── 通用URL提取（非结构化PPT flow） ──
                if flow_key not in _STRUCTURED_PPT_FLOWS:
                    _extract_urls(data, result)

                # ── 流完成信号 ──
        return finalize_result(flow_config, result)

    except requests.exceptions.Timeout:
        return finalize_result(flow_config, result)
    except requests.exceptions.RequestException as e:
        print(f"[错误] 请求失败: {e}", file=sys.stderr)
        raise


# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────

def _load_current_ppt_input(value: str) -> str:
    if not value:
        return ""
    expanded = os.path.expanduser(value)
    if os.path.isfile(expanded):
        with open(expanded, "r", encoding="utf-8") as f:
            return f.read().strip()
    return value.strip()


def main():
    print(_BRAND_BANNER)
    parser = argparse.ArgumentParser(
        description="PPTUltra - AI 智能演示文稿生成引擎"
    )
    parser.add_argument("prompt", nargs="?", default="",
                        help="功能对应的输入内容，例如 PPT 主题、润色指令或编辑要求")
    parser.add_argument("--skill", "--flow-key", dest="flow_key",
                        choices=sorted(FLOW_CONFIGS.keys()), default=DEFAULT_FLOW_KEY,
                        help="选择要调用的功能，默认 ppt")
    parser.add_argument("--api-key", "-k", default="",
                        help="API Key（QID），也可通过环境变量 PPT_API_KEY 配置")
    parser.add_argument("--setup", action="store_true",
                        help="配置/更新 API Key")
    parser.add_argument("--history", action="store_true",
                        help="查看最近的 PPT 生成历史")
    parser.add_argument("--current-ppt", default="",
                        help="编辑类 flow 使用的当前 PPT 内容，可直接传 JSON 字符串或文件路径")
    parser.add_argument("--operations", default="",
                        help="编辑类 flow 使用的操作说明，如“第2页标题润色”")
    parser.add_argument("--size", default="",
                        help="当前 PPT 尺寸，如 1366*768")
    args = parser.parse_args()

    # setup 模式：可选保存 API Key 供鉴权场景使用
    if args.setup:
        key = input("请输入要保存的 API Key（可留空取消）：").strip()
        if key:
            save_api_key(key)
        else:
            print("[取消] 未保存 API Key")
        return

    # 查看历史
    if args.history:
        history = _load_history_list()
        if not history:
            print("暂无生成历史。")
        else:
            print(f"最近 {len(history)} 条生成记录：\n")
            for i, rec in enumerate(history, 1):
                url = rec.get("share_url") or rec.get("ppt_url") or "-"
                print(f"  {i}. [{rec.get('timestamp', '?')}] {rec.get('flow_key', '?')} - {rec.get('prompt', '')[:40]}")
                print(f"     链接：{url}")
        return

    if not args.prompt:
        parser.print_help()
        print("\n可用功能：")
        for key, config in FLOW_CONFIGS.items():
            print(f"  - {key}: {config['display_name']}")
        sys.exit(0)

    # 获取 API Key（允许为空，由服务端决定是否要求鉴权）
    api_key = get_api_key(args.api_key)
    flow_config = get_flow_config(args.flow_key)
    current_ppt = _load_current_ppt_input(args.current_ppt)

    # 编辑类：未指定 --current-ppt 时自动从历史读取
    if flow_config.get("requires_context") and not current_ppt:
        last = _load_last_history()
        if last:
            current_ppt = json.dumps(last, ensure_ascii=False)
            print(f"[自动加载] 使用最近一次生成记录：{last.get('prompt', '')[:30]}... ({last.get('timestamp', '')})")
        else:
            print("[提示] 未找到历史生成记录，建议先生成一份 PPT 或通过 --current-ppt 传入内容。")

    try:
        result = generate_ppt(
            args.prompt,
            api_key=api_key,
            flow_key=args.flow_key,
            current_ppt=current_ppt,
            operations=args.operations,
            size=args.size,
        )

        print(_BRAND_COMPLETE)
        print(f"  功能：{flow_config['display_name']}")

        if result["summary"]:
            print(f"\n{result['summary']}")

        if result["share_url"]:
            print(f"\n  PPT访问链接：\n  {result['share_url']}")

        if result["page_urls"]:
            print(f"\n  总页数：{len(result['page_urls'])} 页")

        if not result["summary"] and not result["share_url"] and not result.get("ppt_url"):
            print("\n  (未收到有效内容，请稍后重试)")
        else:
            _save_history(args.flow_key, args.prompt, result)

    except Exception as e:
        print(f"[错误] 生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
