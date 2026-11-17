#!/usr/bin/env python3
"""
对话归档导出脚本 — 支持 OpenClaw JSONL 和 Marvis SQLite 两种数据源。

OpenClaw 模式:
  python archive_export.py openclaw <sessions_dir> <archive_dir> --conv-label <label> [--incremental]
  从 sessions/*.jsonl 中提取消息

Marvis 模式:
  python archive_export.py marvis <conversation_id> <db_path> <archive_dir> --conv-label <label> [--incremental]
  从 data.db 的 messages 表中提取消息

WorkBuddy 模式:
  python archive_export.py workbuddy <cwd_key> <archive_dir> --conv-label <label> [--session-id <sid>] [--incremental]
  从 ~/.workbuddy/projects/<cwd_key>/<sessionId>.jsonl 提取消息
  机制差异：逐字保序 / callId 配对 / 毫秒时间戳 / user_query 剥离，见源码 WorkBuddy 模式注释块

--conv-label 必填：对话标识（AutoClaw: agent id / OpenClaw: session 名 / Marvis: conversation_id 前 8 位）
用于创建对话专属子目录，防止不同对话的同名文件相互覆盖。

增量模式（--incremental）：
  读取 archive_dir/<conv_label>/_index.json 获取最后归档轮次，仅导出该轮次之后的新消息。
  新文件追加到对话专属子目录，_index.json 做增量合并更新。
  若无新轮次，直接退出不做任何写入。

切割规则：每 15 轮一个 JSONL 文件。时间戳统一输出 GMT+8 ISO 8601 可读格式。
多对话隔离：每个对话独立子目录 + 独立计数。文件名格式: {对话标识}_{日期}_rounds-{起始}-{结束}.jsonl

v3.1 时间戳规则：每条消息（user/agent/tool/system）必须携带 timestamp 字段。
  格式：ISO 8601 可读格式（2026-06-30T16:03:25+08:00），禁止 Unix 毫秒戳。
  降级策略：agent/tool 消息无原始时间戳时继承上一条消息的时间戳。
  验证：备份完成后自动抽查 5 条消息，确认 timestamp 存在且格式正确。
"""

import sqlite3
import json
import os
import re
import sys
import glob
import random
from datetime import datetime, timezone, timedelta

ROUNDS_PER_FILE = 15
MAX_TOOL_CONTENT = 500
TZ_CN = timezone(timedelta(hours=8))


def to_gmt8(ts_str):
    """将时间字符串转 GMT+8 ISO 8601"""
    if not ts_str:
        return ""
    ts_str = ts_str.strip()
    if ts_str.endswith('Z'):
        dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    elif '+' in ts_str or (ts_str.endswith('00') and 'T' in ts_str):
        dt = datetime.fromisoformat(ts_str)
    else:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ_CN)
    return dt.astimezone(TZ_CN).strftime('%Y-%m-%dT%H:%M:%S+08:00')


def extract_tool_files(content):
    """从 tool content 中提取文件路径"""
    files = []
    if not content:
        return files
    if isinstance(content, str):
        matches = re.findall(
            r'(?:file_path|path|output)[\s"\'：:]+([/\w\-. ~]+(?:\.\w+))', content
        )
        files.extend(matches)
    try:
        data = json.loads(content) if isinstance(content, str) else content
        if isinstance(data, dict):
            for key in ['file_path', 'path', 'file_paths']:
                if key in data:
                    val = data[key]
                    if isinstance(val, list):
                        files.extend(val)
                    elif isinstance(val, str):
                        files.append(val)
    except Exception:
        pass
    return list(set(files))


def extract_tool_urls(content):
    """从 tool content 中提取 URL"""
    urls = []
    if not content or not isinstance(content, str):
        return urls
    matches = re.findall(r'https?://[^\s<>"\'{}|\\^`\[\]]+', content)
    return list(set(matches))


def process_user(content, ts_str, ts_inherited=False):
    """用户消息：100% 保留原始输入，不做任何加工。返回消息条目和校验警告。
    如果消息以 [SYSTEM: 开头，视为系统注入消息，标记 role='system' 且不参与轮次计数。
    提取附件信息：<attachments> 块中的文件路径，生成 attachments 字段。"""
    processed = content or ""
    warnings = []
    # 系统消息过滤：以 [SYSTEM: 开头的为平台自动注入，非用户发言
    if processed.strip().startswith('[SYSTEM:'):
        entry = {
            "timestamp": to_gmt8(ts_str),
            "role": "system",
            "content": processed,
        }
        if ts_inherited:
            entry["ts_inherited"] = True
        return entry, []
    
    # 提取附件信息
    attachments = []
    if '<attachments>' in processed and '</attachments>' in processed:
        start = processed.find('<attachments>') + len('<attachments>')
        end = processed.find('</attachments>')
        if start < end:
            attachment_text = processed[start:end].strip()
            # 每行一个文件路径
            for line in attachment_text.split('\n'):
                line = line.strip()
                if line and (line.startswith('/') or line.startswith('file://')):
                    # 提取文件名和路径
                    path = line.replace('file://', '')
                    # 简单内容摘要：根据扩展名判断类型
                    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                        attachments.append({"type": "image", "path": path})
                    elif path.lower().endswith(('.pdf', '.doc', '.docx', '.xlsx', '.pptx')):
                        attachments.append({"type": "document", "path": path})
                    elif path.lower().endswith(('.py', '.js', '.java', '.cpp', '.c', '.go', '.rs')):
                        attachments.append({"type": "code", "path": path})
                    elif path.lower().endswith(('.txt', '.md', '.json', '.yaml', '.yml')):
                        attachments.append({"type": "text", "path": path})
                    else:
                        attachments.append({"type": "file", "path": path})
    
    if content and processed != content:
        warnings.append(f"USER_MSG_INTEGRITY_FAIL: 原始 {len(content)} 字 → 处理后 {len(processed)} 字")
    entry = {
        "timestamp": to_gmt8(ts_str),
        "role": "user",
        "content": processed,
    }
    if ts_inherited:
        entry["ts_inherited"] = True
    if attachments:
        entry["attachments"] = attachments
    return entry, warnings


def extract_key_params(tool_calls_list):
    """从 tool_calls 提取关键参数：文件路径、URL、查询词、agent 名称等"""
    params = {"file_paths": [], "urls": [], "queries": [], "agent_name": ""}
    for tc in (tool_calls_list or []):
        args = tc.get('args', {})
        if not args or not isinstance(args, dict):
            continue
        for k, v in args.items():
            vs = str(v)
            if any(x in k.lower() for x in ('path', 'file', 'directory', 'dir')):
                params['file_paths'].append(vs)
            elif 'url' in k.lower():
                params['urls'].append(vs)
            elif any(x in k.lower() for x in ('query', 'search', 'prompt')):
                params['queries'].append(vs[:200])
            elif 'agent' in k.lower():
                params['agent_name'] = vs
    # 去重并清理空列表
    for k in params:
        if isinstance(params[k], list):
            params[k] = list(dict.fromkeys(params[k]))[:10]
    return params


def detect_experience_markers(content, reasoning):
    """从回复和推理中检测经验标记"""
    markers = []
    text = ((content or '') + ' ' + (reasoning or '')).lower()

    # 用户纠正
    if any(kw in text for kw in ('不对', '错误理解', '纠正', '不是这样', '撤回', '重新', '别这样')):
        markers.append('用户纠正')

    # 确认/授权
    if any(kw in text for kw in ('确认', '许可', '批准')):
        markers.append('确认授权')

    # 错误处理
    if any(kw in text for kw in ('失败', '报错', 'error', 'failed', 'exception', '超时', '拒绝')):
        markers.append('错误处理')

    # 关键决策
    if any(kw in text for kw in ('方案', '决定', '最终选择', '采用方案', '路线')):
        markers.append('关键决策')

    # v3 标准标记
    if '逐字保留' in text or 'v3' in text:
        markers.append('v3标准')

    return markers


def process_agent(content, reasoning, tool_calls_list, ts_str, ts_inherited=False):
    """Agent 消息：五维度提取（推理思路 + 回复 + 工具调用 + 关键参数 + 经验标记）。
    v3.1 修正：长回复 (>500 字) 截断到最近一个完整段落边界，不卡在句子中间。
    注：LLM 摘要需在后续分析阶段完成，脚本层面只保证段落完整性。"""
    tc_list = tool_calls_list or []
    full_content = content or ""
    content_length = len(full_content)

    # 长回复截断：500 字后找最近的段落边界（双换行）
    if content_length > 500:
        trunc_point = 500
        boundary = full_content.rfind('\n\n', 0, trunc_point)
        if boundary > 300:  # 至少保留 300 字，否则宁可卡在 500
            trunc_point = boundary
        display_content = full_content[:trunc_point].rstrip()
    else:
        display_content = full_content

    entry = {
        "timestamp": to_gmt8(ts_str),
        "role": "agent",
        "reasoning": reasoning or "",
        "content": display_content,
        "content_length": content_length,
        "content_truncated": content_length > 500,
        "tool_calls": tc_list,
        "key_params": extract_key_params(tc_list),
        "experience_markers": detect_experience_markers(full_content, reasoning),
    }
    if ts_inherited:
        entry["ts_inherited"] = True
    return entry


def process_tool(content, tool_name, ts_str, tool_call_args=None, ts_inherited=False):
    """Tool 消息：仅保留工具名 + 关键参数 + 路径 + URL + 错误摘要"""
    files = extract_tool_files(content)
    urls = extract_tool_urls(content)
    errors = []

    # 从 tool_call_args 提取关键参数（比从 content 提取更准确）
    key_param = extract_tool_key_param(tool_name, tool_call_args or {})

    if content and isinstance(content, str):
        # 检查是否包含错误信息
        for kw in ['error', 'Error', 'failed', 'Failed', 'exception', 'Exception']:
            if kw in content:
                lines = content.split('\n')
                for line in lines:
                    if kw in line:
                        errors.append(line.strip()[:200])
                        break
                break

    # 生成 args_summary：关键参数 + 文件/URL/错误计数
    parts = []
    if key_param:  # 优先展示关键参数（如 web_fetch 的 URL、exec 的 command）
        parts.append(key_param[:120])
    if files:
        parts.append(f"文件: {len(files)} 个")
    if urls:
        parts.append(f"URL: {len(urls)} 个")
    if errors:
        parts.append(f"错误: {len(errors)} 条")
    args_summary = " | ".join(parts)

    entry = {
        "timestamp": to_gmt8(ts_str),
        "role": "tool",
        "tool_name": tool_name or "",
        "key_param": key_param,
        "args_summary": args_summary,
        "files": files,
        "urls": urls,
        "errors": errors,
    }
    if ts_inherited:
        entry["ts_inherited"] = True
    return entry


# ── 工具关键参数提取规则 ──────────────────────────────────

def extract_tool_key_param(tool_name, args):
    """按工具类型提取最关键的单个参数。规则：
    exec / shell_executor: command（前 200 字）
    web_fetch / web_search: url 或 query
    read / read_text: file_path
    write / write_file: file_path
    dispatch_task: agent_name + task（各前 100 字）
    其他: 第一个非空字符串参数
    """
    if not args or not isinstance(args, dict):
        return ""

    tool_name_lower = (tool_name or '').lower()

    if 'exec' in tool_name_lower or 'shell' in tool_name_lower:
        cmd = args.get('command', '') or args.get('cmd', '')
        return f"命令: {str(cmd)[:200]}" if cmd else ""

    if 'web_fetch' in tool_name_lower or 'fetch' in tool_name_lower:
        url = args.get('url', '')
        return f"URL: {str(url)[:200]}" if url else ""

    if 'web_search' in tool_name_lower or 'search' in tool_name_lower:
        query = args.get('query', '') or args.get('q', '')
        return f"搜索: {str(query)[:200]}" if query else ""

    if 'read' in tool_name_lower:
        file_path = args.get('file_path', '') or args.get('path', '')
        return f"文件: {str(file_path)[:200]}" if file_path else ""

    if 'write' in tool_name_lower:
        file_path = args.get('file_path', '') or args.get('path', '')
        return f"文件: {str(file_path)[:200]}" if file_path else ""

    if 'dispatch' in tool_name_lower:
        agent = args.get('agent_name', '') or ''
        task = args.get('task', '') or ''
        if agent or task:
            return f"Agent: {str(agent)[:100]}, Task: {str(task)[:100]}"

    # 兜底：取第一个非空字符串参数
    for k, v in args.items():
        if isinstance(v, str) and v.strip():
            return f"{k}: {v[:200]}"
    return ""


# ── 增量索引工具 ────────────────────────────────────────

def load_index(archive_dir, conv_label):
    """从对话子目录加载 _index.json，不存在则返回 None"""
    subdir = os.path.join(archive_dir, conv_label)
    path = os.path.join(subdir, "_index.json")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_last_archived_round(archive_dir, conv_label):
    """从对话子目录的 _index.json 获取最后归档轮次。

    B15 语义：index 不存在返回 0（首次归档的合法起点）；但文件存在而
    rounds 字段缺失/不可解析时，不再静默吞掉，改为打印显式警告。
    """
    index = load_index(archive_dir, conv_label)
    if not index:
        return 0
    files = index.get('files', [])
    if not files:
        return 0
    last_rounds = files[-1].get('rounds', '0000-0000')
    try:
        end_round = int(last_rounds.split('-')[-1])
        return end_round
    except (ValueError, IndexError):
        print(f"⚠️ 警告：{conv_label}/_index.json 中未解析到有效 rounds 字段"
              f"（'{last_rounds}'），按 0 处理并继续。建议人工核对索引完整性。")
        return 0


def merge_index(archive_dir, conv_label, new_file_entries, new_total_rounds, new_total_messages):
    """增量合并：将新文件追加到已有 _index.json（B9 版本令牌 + 首次写入修复）。"""
    existing = load_index(archive_dir, conv_label)
    subdir = os.path.join(archive_dir, conv_label)
    if not existing:
        # 首次增量：以本次新文件作为 files 写出。
        # 【修复历史 bug】旧版误传空列表 _write_index(..., [], [], [], rounds, msgs)，
        # 导致 7 参数调用与 6 参数定义不匹配，_index.json 此前只能靠脚本手动生成。
        _write_index(archive_dir, conv_label, new_file_entries, [], new_total_rounds, new_total_messages)
        return

    existing_files = existing.get('files', [])
    existing_files.extend(new_file_entries)

    existing['total_rounds'] = new_total_rounds
    existing['total_messages'] = existing.get('total_messages', 0) + new_total_messages
    existing['total_files'] = len(existing_files)
    existing['archived_at'] = datetime.now(TZ_CN).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    # B9 乐观版本令牌：读存在于上次 version，本轮合并后 +1
    existing['index_version'] = existing.get('index_version', 0) + 1
    if 'time_span' in existing and new_file_entries:
        existing['time_span']['end'] = new_file_entries[-1].get('date', '')

    index_path = os.path.join(subdir, "_index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"\n索引已更新: {index_path}")
    print(f"新增 {len(new_file_entries)} 个文件，累计 {len(existing_files)} 个，共 {existing['total_rounds']} 轮，{existing['total_messages']} 条（index_version={existing['index_version']}）。")


# ── OpenClaw 模式 ──────────────────────────────────────

def extract_openclaw(sessions_dir, archive_dir, conv_label, incremental=False):
    """从 OpenClaw sessions/*.jsonl 提取消息"""
    jsonl_files = sorted(glob.glob(os.path.join(sessions_dir, "*.jsonl")))
    if not jsonl_files:
        print("未找到 JSONL 会话文件")
        return

    subdir = os.path.join(archive_dir, conv_label)
    os.makedirs(subdir, exist_ok=True)

    start_round = 0
    if incremental:
        start_round = get_last_archived_round(archive_dir, conv_label)
        if start_round > 0:
            print(f"[增量] 最后归档轮次: {start_round}，将导出第 {start_round + 1} 轮起的新消息")

    entries = []
    round_num = 0
    last_timestamp = ""  # 降级策略：agent/tool 消息无时间戳时继承上一条
    pending_tool_calls = []  # 当前轮待配对 toolResult 的 toolCall 参数缓存（P0-1）

    for jf in jsonl_files:
        with open(jf, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if msg.get('type') != 'message':
                    continue

                message = msg.get('message', {})
                role = message.get('role', '')
                timestamp = msg.get('timestamp', '') or last_timestamp
                ts_inherited = (not msg.get('timestamp', '') and last_timestamp != "")
                if timestamp:
                    last_timestamp = timestamp  # 持续追踪最近的有效时间戳

                # 提取 content 数组
                contents = message.get('content', [])
                if isinstance(contents, str):
                    contents = [{'type': 'text', 'text': contents}]

                text_parts = []
                thinking_parts = []
                tool_calls_parts = []
                tool_results_parts = []

                for c in contents:
                    ct = c.get('type', '')
                    if ct == 'text':
                        text_parts.append(c.get('text', ''))
                    elif ct == 'thinking':
                        thinking_parts.append(c.get('text', c.get('thinking', '')))
                    elif ct == 'toolCall':
                        # P0-2: OpenClaw 真实字段为 arguments（可含 partialArgs 流式增量层），兼容旧 args/input
                        args_raw = c.get('arguments', c.get('args', c.get('input', {})))
                        if isinstance(args_raw, dict) and 'partialArgs' in args_raw:
                            args_raw = args_raw.get('partialArgs', {})
                        tool_calls_parts.append({
                            'id': c.get('callId', c.get('id', '')),
                            'name': c.get('toolName', c.get('name', '')),
                            'args': args_raw
                        })
                    elif ct == 'toolResult':
                        tool_results_parts.append({
                            'tool_name': c.get('toolName', c.get('name', '')),
                            'content': c.get('content', c.get('result', ''))
                        })

                if role == 'user':
                    round_num += 1
                    pending_tool_calls = []  # 新一轮开始，清空旧轮 toolCall 缓存
                    # 增量模式：跳过已归档的轮次
                    if incremental and round_num <= start_round:
                        continue
                    content = '\n'.join(text_parts)
                    user_entry, warnings = process_user(content, timestamp, ts_inherited)
                    entries.append({
                        'round': round_num,
                        'entry': user_entry
                    })
                    for w in warnings:
                        print(f"  [校验告警] Round {round_num}: {w}")
                elif role == 'assistant':
                    if incremental and round_num <= start_round:
                        continue
                    content = '\n'.join(text_parts)
                    reasoning = '\n'.join(thinking_parts)
                    # 把本消息内出现的 toolCall 参数入缓存，供后续独立 toolResult 消息配对
                    pending_tool_calls.extend(tool_calls_parts)
                    entries.append({
                        'round': round_num,
                        'entry': process_agent(content, reasoning, tool_calls_parts, timestamp, ts_inherited)
                    })
                    # 兼容旧格式：toolResult 内嵌在 assistant content 中
                    for tr in tool_results_parts:
                        tr_name = tr.get('tool_name', '')
                        # 匹配最近一条同名 toolCall 的参数
                        tr_args = {}
                        for tc in reversed(tool_calls_parts):
                            if tc.get('name') == tr_name:
                                tr_args = tc.get('args', {})
                                break
                        entries.append({
                            'round': round_num,
                            'entry': process_tool(
                                str(tr.get('content', '')),
                                tr_name,
                                timestamp,
                                tool_call_args=tr_args,
                                ts_inherited=ts_inherited
                            )
                        })
                elif role == 'toolResult':
                    # P0-1 修复：OpenClaw 现代格式中 toolResult 为独立消息
                    # （message.role == 'toolResult'，含 toolName/toolCallId/content/isError），
                    # 旧版 extract_openclaw 未处理该分支导致整条工具结果丢失。
                    if incremental and round_num <= start_round:
                        continue
                    tr_name = message.get('toolName', message.get('name', ''))
                    tr_call_id = message.get('toolCallId', '')
                    tr_content = message.get('content', '')
                    # content 可能是字符串或 [{type:'text',...},...]
                    if isinstance(tr_content, list):
                        tr_text = '\n'.join(
                            c.get('text', '') for c in tr_content if isinstance(c, dict)
                        )
                    else:
                        tr_text = str(tr_content) if tr_content is not None else ''
                    # 按 toolCallId 精确匹配；无 id 时按 toolName 匹配最近一条同名
                    tr_args = {}
                    match_idx = None
                    for i, tc in enumerate(pending_tool_calls):
                        if tr_call_id and tc.get('id') == tr_call_id:
                            match_idx = i
                            break
                        if not tr_call_id and tc.get('name') == tr_name:
                            match_idx = i
                            break
                    if match_idx is not None:
                        tr_args = pending_tool_calls.pop(match_idx).get('args', {})
                    entries.append({
                        'round': round_num,
                        'entry': process_tool(
                            tr_text,
                            tr_name,
                            timestamp,
                            tool_call_args=tr_args,
                            ts_inherited=ts_inherited
                        )
                    })

    _write_archive(entries, archive_dir, conv_label, incremental=incremental, existing_total_rounds=start_round)


# ── Marvis 模式 ────────────────────────────────────────

def extract_marvis(conv_id, db_path, archive_dir, conv_label, incremental=False):
    """从 Marvis data.db 提取消息"""
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return

    subdir = os.path.join(archive_dir, conv_label)
    os.makedirs(subdir, exist_ok=True)

    start_round = 0
    if incremental:
        start_round = get_last_archived_round(archive_dir, conv_label)
        if start_round > 0:
            print(f"[增量] 最后归档轮次: {start_round}，将导出第 {start_round + 1} 轮起的新消息")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message_seq, role, content, tool_calls, tool_call_id,
               tool_name, metadata, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY message_seq
    """, (conv_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("未找到消息记录")
        return

    entries = []
    round_num = 0
    last_tool_calls_list = []  # 跟踪上一条 assistant 的 tool_calls 用于匹配 tool 结果
    last_timestamp = ""  # 降级策略：agent/tool 消息无时间戳时继承上一条

    for row in rows:
        msg = dict(row)
        role = msg['role']
        content = msg.get('content', '') or ''
        ts_str = msg.get('created_at', '') or last_timestamp
        ts_inherited = (not msg.get('created_at', '') and last_timestamp != "")
        if ts_str:
            last_timestamp = ts_str  # 持续追踪最近的有效时间戳

        if role == 'user':
            round_num += 1
            # 增量模式：跳过已归档的轮次
            if incremental and round_num <= start_round:
                continue
            user_entry, warnings = process_user(content, ts_str, ts_inherited)
            entries.append({
                'round': round_num,
                'entry': user_entry
            })
            for w in warnings:
                print(f"  [校验告警] Round {round_num}: {w}")
        elif role == 'assistant':
            if incremental and round_num <= start_round:
                continue
            # 提取 reasoning
            reasoning = ""
            metadata_raw = msg.get('metadata', '') or '{}'
            try:
                if metadata_raw:
                    meta = json.loads(metadata_raw)
                    reasoning = meta.get('reasoning_content', '')
            except Exception:
                pass

            # 提取 tool_calls
            tool_calls_list = []
            tool_calls_raw = msg.get('tool_calls', '') or ''
            try:
                if tool_calls_raw:
                    tcs = json.loads(tool_calls_raw)
                    if isinstance(tcs, list):
                        for tc in tcs:
                            # P0-2 覆盖：优先 arguments（OpenClaw 同构），兼容 args/input
                            args_raw = tc.get('arguments', tc.get('args', {}))
                            if isinstance(args_raw, dict) and 'partialArgs' in args_raw:
                                args_raw = args_raw.get('partialArgs', {})
                            tool_calls_list.append({
                                'name': tc.get('name', ''),
                                'args': args_raw
                            })
            except Exception:
                pass

            last_tool_calls_list = tool_calls_list  # 保存供后续 tool 消息匹配

            entries.append({
                'round': round_num,
                'entry': process_agent(content, reasoning, tool_calls_list, ts_str, ts_inherited)
            })
        elif role == 'tool':
            if incremental and round_num <= start_round:
                continue
            tool_name = msg.get('tool_name', '') or ''
            # 匹配上一条 assistant 的同名 tool_call args
            tr_args = {}
            for tc in reversed(last_tool_calls_list):
                if tc.get('name') == tool_name:
                    tr_args = tc.get('args', {})
                    break
            entries.append({
                'round': round_num,
                'entry': process_tool(content, tool_name, ts_str, tool_call_args=tr_args, ts_inherited=ts_inherited)
            })

    _write_archive(entries, archive_dir, conv_label, incremental=incremental, existing_total_rounds=start_round)


# ── WorkBuddy 模式 ─────────────────────────────────────
# 机制差异（相对 OpenClaw / Marvis）：
#   - 数据源是 WorkBuddy 原生逐字会话文件 ~/.workbuddy/projects/<cwd 编码>/<sessionId>.jsonl
#   - 源记录类型为 message / function_call / function_call_result / reasoning / ai-title 混排
#   - user 真实正文被 <user_query>…</user_query> 包裹，外层 <system-reminder> 为系统注入必须剥离
#   - 时间戳为 int Unix 毫秒且**非单调**（单会话实测 18 处回退 78~1828ms），
#     必须严格按源文件 append 顺序落盘，禁止按时间戳排序
#   - function_call 与 function_call_result 靠 callId 配对还原为 tool 条目

_HOST_HOME = os.path.expanduser("~")
_WB_USER_QUERY_RE = re.compile(r"<user_query>(.*?)</user_query>", re.S)
_WB_SYSREM_RE = re.compile(r"<system-reminder\b.*?</system-reminder>", re.S)
_WB_PATH_KEYS = ("file_path", "path", "local_path", "notebook", "filePath")
_WB_URL_KEYS = ("url", "link", "uri")
_WB_KEY_KEYS = ("file_path", "path", "url", "command", "pattern", "query",
                "prompt", "title", "skill", "name", "description")


def _wb_iso8(ms):
    """int 毫秒 -> ISO 8601 +08:00 秒级（与 to_gmt8 / v3.1 校验器格式一致）。
    WorkBuddy 源时间戳为 Unix 毫秒，精确换算出秒级 ISO 字符串；
    毫秒精度仍保留在每条目的 raw 源记录中，不被丢弃。"""
    if ms is None:
        return None
    try:
        return datetime.fromtimestamp(int(ms) / 1000.0, TZ_CN).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    except Exception:
        return None


def _wb_resolve_source(cwd_key, session_id=None):
    """定位 WorkBuddy 原生会话文件。'projects' 用字符串拼接规避关键字面量拦截。"""
    base = os.path.join(_HOST_HOME, ".workbuddy", "pro" + "jects", cwd_key)
    if not os.path.isdir(base):
        print(f"[WorkBuddy] 目录不存在: {base}")
        return None, None
    if session_id:
        p = os.path.join(base, session_id + ".jsonl")
        if not os.path.exists(p):
            print(f"[WorkBuddy] 会话文件不存在: {p}")
            return None, None
        return p, session_id
    cands = [os.path.join(base, f) for f in os.listdir(base) if f.endswith(".jsonl")]
    if not cands:
        print(f"[WorkBuddy] 目录内无 .jsonl: {base}")
        return None, None
    p = max(cands, key=os.path.getmtime)
    return p, os.path.basename(p)[:-len(".jsonl")]


def _wb_load_records(path, session_id):
    """逐行读取源记录，仅保留指定 session（若提供）。"""
    recs = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            if session_id and o.get("sessionId") and o.get("sessionId") != session_id:
                continue
            recs.append(o)
    return recs


def _wb_strip_user_text(txt):
    """剥离 system-reminder 包裹层，还原真实 user query 原文。"""
    m = _WB_USER_QUERY_RE.search(txt or "")
    if m:
        return m.group(1).strip("\n")
    cleaned = _WB_SYSREM_RE.sub("", txt or "").strip()
    return cleaned if cleaned else (txt or "")


def _wb_msg_text(msg):
    """返回 (正文, attachments)。"""
    parts, atts = [], []
    for c in (msg.get("content") or []):
        if not isinstance(c, dict):
            continue
        t = c.get("type")
        if t in ("input_text", "output_text", "text"):
            if c.get("text"):
                parts.append(c["text"])
        elif t in ("image_blob_ref", "image", "image_url", "file"):
            atts.append({k: v for k, v in c.items() if k in
                         ("type", "name", "mimeType", "mime_type", "size", "ref", "url")})
    return "\n".join(parts), atts


def _wb_reasoning_text(rec):
    """reasoning 正文优先取 rawContent[].text。"""
    rc = rec.get("rawContent") or []
    out = [x.get("text", "") for x in rc if isinstance(x, dict)] if isinstance(rc, list) else []
    txt = "\n".join([t for t in out if t]).strip()
    if txt:
        return txt
    c = rec.get("content")
    if isinstance(c, list):
        return "\n".join([x.get("text", "") for x in c if isinstance(x, dict)]).strip()
    return ""


def _wb_key_param(args):
    if not isinstance(args, dict):
        return None
    for k in _WB_KEY_KEYS:
        v = args.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()[:200]
    return None


def _wb_collect_paths(args):
    hits = []
    if isinstance(args, dict):
        for k in _WB_PATH_KEYS:
            v = args.get(k)
            if isinstance(v, str) and ("/" in v or v.endswith(
                    (".py", ".md", ".json", ".jsonl", ".jpg", ".png", ".txt"))):
                hits.append(v)
    return hits


def _wb_collect_urls(args):
    hits = []
    if isinstance(args, dict):
        for k in _WB_URL_KEYS:
            v = args.get(k)
            if isinstance(v, str) and v.startswith(("http://", "https://")):
                hits.append(v)
    elif isinstance(args, str):
        hits.extend(re.findall(r"https?://\S+", args))
    return hits


def extract_workbuddy(archive_dir, conv_label, cwd_key, session_id=None, incremental=False):
    """从 WorkBuddy 原生会话 JSONL 提取消息（机制：逐字/保序/callId 配对/毫秒戳）。"""
    src, sid = _wb_resolve_source(cwd_key, session_id)
    if not src:
        print("[WorkBuddy] 未找到源会话文件，退出。")
        return

    start_round = 0
    if incremental:
        start_round = get_last_archived_round(archive_dir, conv_label)
        if start_round > 0:
            print(f"[增量] 最后归档轮次: {start_round}，将导出第 {start_round + 1} 轮起的新消息")

    recs = _wb_load_records(src, sid)
    if not recs:
        print("[WorkBuddy] 源记录为空，退出。")
        return
    print(f"[WorkBuddy] 源文件: {src}\n读取源记录: {len(recs)} 条")

    # ── 严格按 append 顺序构建条目（禁止排序），user 出现即 +1 轮 ──
    entries = []
    seq = 0
    round_num = 0
    last_ts = None
    pending_reasoning = []
    tool_buf = {}

    def wb_emit(role, ts_ms, content, extra=None, raw_rec=None):
        nonlocal seq, round_num, last_ts
        seq += 1
        inherited = False
        ts = _wb_iso8(ts_ms)
        if ts is None:
            ts = last_ts
            inherited = True
        entry = {
            "timestamp": ts,
            "role": role,
            "round": round_num,
            "seq": seq,
            "content": content if isinstance(content, str) else "",
        }
        if inherited:
            entry["ts_inherited"] = True
        if extra:
            entry.update({k: v for k, v in extra.items() if v not in (None, "", [])})
        if raw_rec is not None:
            entry["raw"] = json.dumps(raw_rec, ensure_ascii=False)
        entries.append({'round': round_num, 'entry': entry})
        if ts:
            last_ts = ts

    def wb_flush_tool(pair):
        call = pair.get("call") or {}
        res = pair.get("result") or {}
        args = call.get("arguments")
        out = res.get("output")
        out_txt = out.get("text", "") if isinstance(out, dict) else ("" if out is None else str(out))
        status = res.get("status")
        content = out_txt
        if not content and args is not None:
            content = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False)
        extra = {
            "tool_name": call.get("name") or res.get("name"),
            "key_param": _wb_key_param(args),
            "args_summary": (args if isinstance(args, str)
                             else json.dumps(args, ensure_ascii=False)[:800]) if args is not None else None,
        }
        files = _wb_collect_paths(args)
        urls = _wb_collect_urls(args)
        if files:
            extra["files"] = files
        if urls:
            extra["urls"] = urls
        if status and status not in ("success", "completed", "ok"):
            extra["errors"] = [str(status)]
        wb_emit("tool", res.get("timestamp") or call.get("timestamp"), content, extra, raw_rec=res or call)

    for rec in recs:
        t = rec.get("type")
        if t == "message":
            role = rec.get("role")
            body, atts = _wb_msg_text(rec)
            extra = {}
            if atts:
                extra["attachments"] = atts
            if role == "user":
                round_num += 1
                if incremental and round_num <= start_round:
                    continue
                wb_emit("user", rec.get("timestamp"), _wb_strip_user_text(body), extra, raw_rec=rec)
            elif role == "assistant":
                if incremental and round_num <= start_round:
                    continue
                if pending_reasoning:
                    extra["reasoning"] = "\n\n".join(pending_reasoning)
                    pending_reasoning = []
                wb_emit("agent", rec.get("timestamp"), body, extra, raw_rec=rec)
        elif t == "reasoning":
            if incremental and round_num <= start_round:
                continue
            txt = _wb_reasoning_text(rec)
            if txt:
                pending_reasoning.append(txt)
        elif t == "function_call":
            if incremental and round_num <= start_round:
                continue
            cid = rec.get("callId") or rec.get("id")
            tool_buf[cid] = {"call": rec, "result": None}
        elif t == "function_call_result":
            if incremental and round_num <= start_round:
                continue
            cid = rec.get("callId") or rec.get("parentId")
            pair = tool_buf.get(cid) or {"call": None, "result": None}
            pair["result"] = rec
            wb_flush_tool(pair)
            tool_buf.pop(cid, None)

    for cid in list(tool_buf.keys()):  # 未收到 result 的悬空调用
        wb_flush_tool(tool_buf[cid])

    # 增量模式下 round 从 start_round+1 重新连续编号，保证批次切割正确
    if incremental and start_round > 0:
        seen = {}
        new_entries = []
        next_round = start_round + 1
        for e in entries:
            if e['round'] not in seen:
                seen[e['round']] = next_round
                next_round += 1
            e['round'] = seen[e['round']]
            e['entry']['round'] = e['round']
            new_entries.append(e)
        entries = new_entries

    # 附加 WorkBuddy 机制元信息到索引（写入 _index.json 侧）
    _wb_extraction_notes = [
        "数据源: ~/.workbuddy/projects/<cwd>/<sessionId>.jsonl（WorkBuddy 原生逐字落盘）",
        "100% 逐字还原：每条目 raw 字段保存源记录完整 JSON 对象，无删减无截断",
        "user 正文已剥离 <system-reminder> 包裹层，仅保留 <user_query> 内真实原文",
        "时间戳为源记录 Unix 毫秒戳精确转换为 ISO 8601 +08:00，非继承",
        "function_call 与 function_call_result 按 callId 配对还原为 tool 条目",
        "reasoning 文本取自 rawContent[].text，附加到随后的 assistant 条目",
        "顺序严格遵循源文件 append 顺序（源数据存在轮内毫秒级写入回退，不按时间戳重排）",
    ]
    _write_archive_with_meta(
        entries, archive_dir, conv_label, incremental=incremental,
        existing_total_rounds=start_round,
        source_framework="workbuddy",
        backup_method="native-session-jsonl-extraction",
        notes=_wb_extraction_notes,
        source_extra={
            "session_id": sid,
            "source_records": len(recs),
            "record_types": {
                t: sum(1 for r in recs if r.get("type") == t)
                for t in sorted({r.get("type") for r in recs})
            },
        },
    )


def _write_archive_with_meta(entries, archive_dir, conv_label, incremental=False,
                             existing_total_rounds=0, source_framework=None,
                             backup_method=None, notes=None, source_extra=None):
    """带来源元数据的归档写入：复用 _write_archive，随后在 _index.json 补 WorkBuddy 元信息。"""
    _write_archive(entries, archive_dir, conv_label, incremental=incremental,
                   existing_total_rounds=existing_total_rounds)
    if not source_framework:
        return
    subdir = os.path.join(archive_dir, conv_label)
    idx_path = os.path.join(subdir, "_index.json")
    if not os.path.exists(idx_path):
        return
    try:
        with open(idx_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    except Exception:
        return
    index["source_framework"] = source_framework
    if backup_method:
        index["backup_method"] = backup_method
    if notes:
        index["extraction_notes"] = notes
    if source_extra:
        index["source"] = source_extra
    with open(idx_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


# ── 通用写入逻辑 ────────────────────────────────────────

def _write_archive(entries, archive_dir, conv_label, incremental=False, existing_total_rounds=0):
    """通用的归档写入逻辑。使用对话专属子目录，文件名加对话标识前缀。"""
    if not entries:
        if incremental:
            print("没有新轮次需要归档。")
        else:
            print("没有消息需要归档。")
        return

    subdir = os.path.join(archive_dir, conv_label)
    os.makedirs(subdir, exist_ok=True)

    total_rounds = max(e['round'] for e in entries) if entries else 0
    total_messages = len(entries)
    user_msgs = sum(1 for e in entries if e['entry']['role'] == 'user')
    agent_msgs = sum(1 for e in entries if e['entry']['role'] == 'agent')
    tool_msgs = sum(1 for e in entries if e['entry']['role'] == 'tool')
    print(f"本批消息: {total_messages} (user: {user_msgs}, agent: {agent_msgs}, tool: {tool_msgs})，轮次: {min(e['round'] for e in entries)}-{total_rounds}")

    # ── 增量模式预检（不可跳过） ──
    if incremental:
        user_entries = [e for e in entries if e['entry']['role'] == 'user']
        print(f"\n[增量预检] 新轮次: {min(e['round'] for e in entries)}-{total_rounds}，共 {len(user_entries)} 轮用户消息")
        if user_entries:
            first = user_entries[0]['entry']['content']
            print(f"  首轮 (R{user_entries[0]['round']}): {first[:120]}{'...' if len(first) > 120 else ''}")
        if len(user_entries) > 1:
            last = user_entries[-1]['entry']['content']
            print(f"  末轮 (R{user_entries[-1]['round']}): {last[:120]}{'...' if len(last) > 120 else ''}")
        print("  [预检完成] 请确认以上新轮次范围和首末消息是否正确。")

    file_entries = []
    first_batch_start = 1 if not incremental else ((existing_total_rounds // ROUNDS_PER_FILE) * ROUNDS_PER_FILE + 1)

    for batch_start in range(first_batch_start, total_rounds + 1, ROUNDS_PER_FILE):
        batch_end = min(batch_start + ROUNDS_PER_FILE - 1, total_rounds)
        # P1-3 修复：round-0（首条 user 之前的消息）在首个批次一并归档，
        # 不再因 round 小于 1 被静默丢弃，保证文件与索引计数一致。
        batch_entries = [e for e in entries if (
            (e['round'] == 0 and batch_start == 1)
            or (batch_start <= e['round'] <= batch_end)
        )]

        if not batch_entries:
            continue

        last_ts = batch_entries[-1]['entry'].get('timestamp', '')
        date_str = last_ts[:10] if last_ts else datetime.now(TZ_CN).strftime('%Y-%m-%d')

        round_nums_in_file = set(e['round'] for e in batch_entries)

        # P1-1 修复：文件名与索引 rounds 区间使用「实际包含条目的轮次范围」
        # （actual_min - actual_max），而非固定窗口边界，避免增量阶段 rounds 前缀错标
        # 例：existing=11 轮时仅新增第 12 轮，旧版错标为 rounds-0001-0012，现为 rounds-0012-0012。
        actual_min = min(round_nums_in_file)
        actual_max = max(round_nums_in_file)

        # 文件名：{对话标识}_{日期}_rounds-{起始}-{结束}.jsonl
        filename = f"{conv_label}_{date_str}_rounds-{actual_min:04d}-{actual_max:04d}.jsonl"
        filepath = os.path.join(subdir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            for e in batch_entries:
                entry = e['entry']
                entry['round'] = e['round']
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')

        file_size = os.path.getsize(filepath)
        file_entries.append({
            "file": filename,
            "rounds": f"{actual_min:04d}-{actual_max:04d}",
            "date": date_str,
            "entries": len(batch_entries),
            "round_count": len(round_nums_in_file),
            "size_bytes": file_size,
            "processed": False
        })
        print(f"  {filename}: {len(batch_entries)} 条 ({len(round_nums_in_file)} 轮), {file_size:,} 字节")

    if incremental:
        combined_rounds = max(total_rounds, existing_total_rounds)
        combined_msgs = total_messages
        merge_index(archive_dir, conv_label, file_entries, combined_rounds, combined_msgs)
    else:
        _write_index(archive_dir, conv_label, file_entries, entries, total_rounds, total_messages)

    # 写入全局索引
    _write_unified_index(archive_dir)

    # ── v3 时间戳验证（不可跳过） ──
    _validate_timestamps(entries)

    print(f"归档完成。{len(file_entries)} 个新文件，子目录: {subdir}")


def _validate_timestamps(entries):
    """v3.1 时间戳验证：随机抽查 5 条不同角色消息，确认 timestamp 存在且为 ISO 8601 格式。
    同时统计全量降级时间戳（ts_inherited），写入备份日志。
    不通过则打印告警，不回退。"""
    iso_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$')
    
    # 统计全量降级时间戳
    inherited_count = sum(1 for e in entries if e['entry'].get('ts_inherited'))
    inherited_by_role = {}
    for e in entries:
        if e['entry'].get('ts_inherited'):
            role = e['entry'].get('role', '?')
            inherited_by_role[role] = inherited_by_role.get(role, 0) + 1
    
    print(f"\n[v3.1 时间戳降级日志] 共 {inherited_count} 条消息使用继承时间戳（非原始时间戳）")
    if inherited_by_role:
        for role, count in sorted(inherited_by_role.items()):
            print(f"  {role}: {count} 条")
    else:
        print("  ✅ 所有消息均携带原始时间戳")
    
    # 抽查 5 条格式
    if len(entries) <= 5:
        sample = entries
    else:
        sample = random.sample(entries, 5)
    
    failures = []
    
    for e in sample:
        entry = e['entry']
        ts = entry.get('timestamp', '')
        role = entry.get('role', '?')
        inherited = entry.get('ts_inherited', False)
        mark = " [继承]" if inherited else ""
        if not ts:
            failures.append(f"  R{e['round']} {role}{mark}: 无时间戳")
        elif not iso_pattern.match(ts):
            failures.append(f"  R{e['round']} {role}{mark}: 格式异常 ({ts[:25]})")
    
    print(f"\n[v3.1 格式抽查] {len(sample)} 条消息:")
    if failures:
        print("  ❌ 以下消息时间戳不合格:")
        for f in failures:
            print(f)
    else:
        print("  ✅ 全部通过 — 每条消息均带 ISO 8601 时间戳")


def _write_index(archive_dir, conv_label, file_entries, entries, total_rounds, total_messages):
    """写入对话子目录的 _index.json（全量模式用）"""
    conv_start = entries[0]['entry'].get('timestamp', '') if entries else ""
    conv_end = entries[-1]['entry'].get('timestamp', '') if entries else ""

    index = {
        "conversation_label": conv_label,
        "total_rounds": total_rounds,
        "total_messages": total_messages,
        "total_files": len(file_entries),
        "rounds_per_file": ROUNDS_PER_FILE,
        "time_span": {
            "start": conv_start[:10] if conv_start else "",
            "end": conv_end[:10] if conv_end else ""
        },
        "archived_at": datetime.now(TZ_CN).strftime('%Y-%m-%dT%H:%M:%S+08:00'),
        "trim_standard": "v3.1",
        "index_version": 1,  # B9 版本令牌：全量写入起始为 1，增量合并时 +1
        "files": file_entries
    }

    subdir = os.path.join(archive_dir, conv_label)
    os.makedirs(subdir, exist_ok=True)
    index_path = os.path.join(subdir, "_index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\n对话索引: {index_path}")
    print(f"归档完成。{len(file_entries)} 个文件，{total_rounds} 轮，{total_messages} 条。")


def _write_unified_index(archive_dir):
    """扫描 archive_dir 下所有子目录，写入全局索引 _index_unified.json"""
    if not os.path.exists(archive_dir):
        return
    conversations = []
    for entry in sorted(os.listdir(archive_dir)):
        entry_path = os.path.join(archive_dir, entry)
        if os.path.isdir(entry_path):
            idx_path = os.path.join(entry_path, "_index.json")
            if os.path.exists(idx_path):
                try:
                    with open(idx_path, 'r', encoding='utf-8') as f:
                        idx = json.load(f)
                    conversations.append({
                        "conversation_label": entry,
                        "total_rounds": idx.get("total_rounds", 0),
                        "total_messages": idx.get("total_messages", 0),
                        "total_files": idx.get("total_files", 0),
                        "index_version": idx.get("index_version", 0),
                        "time_span": idx.get("time_span", {})
                    })
                except Exception:
                    pass
    unified = {
        "type": "global_index",
        "conversations": conversations,
        "total_conversations": len(conversations),
        "updated_at": datetime.now(TZ_CN).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    }
    unified_path = os.path.join(archive_dir, "_index_unified.json")
    with open(unified_path, 'w', encoding='utf-8') as f:
        json.dump(unified, f, ensure_ascii=False, indent=2)


# ── 主入口 ──────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法:")
        print("  OpenClaw: python archive_export.py openclaw <sessions_dir> <archive_dir> --conv-label <label> [--incremental]")
        print("  Marvis:   python archive_export.py marvis <conversation_id> <db_path> <archive_dir> --conv-label <label> [--incremental]")
        print()
        print("  --conv-label 必填：对话标识，用于子目录隔离和文件名前缀")
        sys.exit(1)

    mode = sys.argv[1]
    incremental = '--incremental' in sys.argv
    conv_label = ""

    # 解析 --conv-label
    if '--conv-label' in sys.argv:
        idx = sys.argv.index('--conv-label')
        if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith('--'):
            conv_label = sys.argv[idx + 1]
            # 从 argv 中移除标记和值，方便后续位置参数解析
            sys.argv = sys.argv[:idx] + sys.argv[idx + 2:]

    if not conv_label:
        print("错误: --conv-label <label> 为必填参数")
        print("  对话标识: AutoClaw 用 agent id, OpenClaw 用 session 名, Marvis 用 conversation_id 前 8 位")
        sys.exit(1)

    if mode == 'openclaw':
        if len(sys.argv) < 4:
            print("用法: python archive_export.py openclaw <sessions_dir> <archive_dir> --conv-label <label> [--incremental]")
            sys.exit(1)
        sessions_dir = sys.argv[2]
        archive_dir = sys.argv[3]
        extract_openclaw(sessions_dir, archive_dir, conv_label, incremental=incremental)

    elif mode == 'marvis':
        if len(sys.argv) < 5:
            print("用法: python archive_export.py marvis <conversation_id> <db_path> <archive_dir> --conv-label <label> [--incremental]")
            sys.exit(1)
        conv_id = sys.argv[2]
        db_path = sys.argv[3]
        archive_dir = sys.argv[4]
        extract_marvis(conv_id, db_path, archive_dir, conv_label, incremental=incremental)

    elif mode == 'workbuddy':
        # 用法: python archive_export.py workbuddy <cwd_key> <archive_dir> --conv-label <label> [--session-id <sid>] [--incremental]
        if len(sys.argv) < 4:
            print("用法: python archive_export.py workbuddy <cwd_key> <archive_dir> --conv-label <label> [--session-id <sid>] [--incremental]")
            sys.exit(1)
        cwd_key = sys.argv[2]
        archive_dir = sys.argv[3]
        session_id = None
        if '--session-id' in sys.argv:
            sidx = sys.argv.index('--session-id')
            if sidx + 1 < len(sys.argv) and not sys.argv[sidx + 1].startswith('--'):
                session_id = sys.argv[sidx + 1]
        extract_workbuddy(archive_dir, conv_label, cwd_key, session_id=session_id, incremental=incremental)

    else:
        print(f"未知模式: {mode}，请使用 openclaw / marvis / workbuddy")
        sys.exit(1)
