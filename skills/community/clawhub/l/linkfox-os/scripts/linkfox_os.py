#!/usr/bin/env python3
"""
linkfox-os CLI - AgentStudio 异步任务 Agent.

通过 AgentStudio 异步任务接口（/agent-studio/task/create + /agent-studio/task/get）
提交 prompt 并轮询结果：
  - 提交入参 {prompt, modelId}，返回任务 ID 字段为 "id"
  - 轮询返回 {message, eventList}，message.stopReason 非空即终态
  - 结果在 message.agentMessageChunks[].content

Default mode is background: submit task and return the task id immediately,
so the caller can continue while the task runs (tasks typically take 1-5 min).
Use --status for a quick non-blocking progress check, --poll to keep waiting,
or --wait to block until done.

Usage:
    linkfox_os.py "<task>"                       # Submit in background, return task id (default)
    linkfox_os.py --wait "<task>"                # Submit and wait for result (blocking)
    linkfox_os.py --status <messageId>           # One-shot status & progress check (NO polling)
    linkfox_os.py --poll <messageId>             # Poll result for a messageId until terminal
    linkfox_os.py --cancel <messageId>           # Cancel a running task
    linkfox_os.py --list-recent [N]              # Show the N most recent local tasks (default 30, capped at 30)
    linkfox_os.py --timeout 600 --poll <id>      # Custom timeout when polling (seconds)
    linkfox_os.py --format json --poll <id>      # Output raw JSON

Every successful submission immediately writes $PWD/.linkfox-os/output/{ts}/result.json
containing the messageId (from create response `id`) + original prompt text —
so even if the background mode's stdout is not captured, you can recover the
messageId later with --list-recent. Override with env LINKFOX_OS_OUTPUT_DIR
if you want to force an absolute location instead of CWD.

While polling, the script streams each new acpEvent (the Agent's live thinking +
tool calls, extracted from eventList) to stderr with [思考]/[工具]/[消息] prefixes,
and folds the last one into the 30s heartbeat. These stderr lines ARE the live process —
in Codex they surface in the terminal as the task runs; the final result is on
stdout. Pass --no-stream-events to silence.

Environment:
    LINKFOXAGENT_API_KEY  - API key (required)
    LINKFOXAGENT_BASE_URL - Base URL. Default: https://agent-api.linkfox.com/
    LINKFOX_OS_OUTPUT_DIR - 覆盖产物目录（缺省 $PWD/.linkfox-os/output/）
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from urllib.request import urlopen, Request, urlretrieve
from urllib.error import HTTPError, URLError


# 从环境变量取 BASE_URL，默认生产环境
LINKFOXAGENT_BASE_URL = os.environ.get("LINKFOXAGENT_BASE_URL", "https://agent-api.linkfox.com/")
SUBMIT_ENDPOINT = "agent-studio/task/create"
POLL_ENDPOINT = "agent-studio/task/get"
CANCEL_ENDPOINT = "agent-studio/task/cancel"
SHARE_URL_ENDPOINT = "agent-studio/task/getShareUrl"

DEFAULT_MODEL_ID = "default"

# stopReason 非空即终态；end_turn 视为正常完成，其余视为可能异常但仍输出结果。
SUCCESS_STOP_REASONS = {"end_turn"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolve_output_root() -> str:
    """决定 output 目录：
    1) 环境变量 LINKFOX_OS_OUTPUT_DIR（显式覆盖，比如指定绝对路径统一收拢）
    2) 当前工作目录下的 .linkfox-os/output/（默认，兼容 CC / Codex / workbuddy）

    刻意用 CWD 而非 SCRIPT_DIR：这个 skill 可能被安装到 /root/.linkfox/workspaces/... 或
    ~/.claude/plugins/... 等对用户不可见的系统位置；把产物落盘到这些地方，用户在 CC / Codex
    里根本读不到。落在 CWD 下的 .linkfox-os/ 隐藏目录，与用户当前项目同 workspace，可读可提交。
    """
    env_dir = os.environ.get("LINKFOX_OS_OUTPUT_DIR")
    if env_dir:
        return os.path.abspath(env_dir)
    return os.path.join(os.getcwd(), ".linkfox-os", "output")


OUTPUT_ROOT = _resolve_output_root()
META_FILENAME = "result.json"

# stdout 中 chunk 预览截断长度（超过则整块落盘，仅回显前 N 字符 + 保存路径）
CHUNK_STDOUT_PREVIEW_CHARS = 200
# chunk 全文另存文件的阈值：小于该长度直接内联到 stdout（浪费的 token 有限）
CHUNK_INLINE_THRESHOLD_CHARS = 400

# 本地"最近任务"登记表：滚动保留最近 30 条 messageId，供 --list-recent 秒读。
# 提交时写入一条 (status=submitted)，终态时更新同 messageId 的记录。
# 与 output 目录同级（.linkfox-os/recent-tasks.json），语义上是"skill 级注册表"，
# 不是某次任务的产物。
RECENT_TASKS_FILE = os.path.join(os.path.dirname(OUTPUT_ROOT), "recent-tasks.json")
RECENT_TASKS_MAX = 30


def get_api_key() -> str:
    """Get API key from environment. Reads LINKFOXAGENT_API_KEY only."""
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "Error: LINKFOXAGENT_API_KEY environment variable not set.\n"
            "Get your API key from: https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb\n"
            "Then set it:\n"
            "  export LINKFOXAGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def api_request(endpoint: str, payload: dict) -> dict:
    """Make a POST request to the linkfox-os API."""
    api_key = get_api_key()
    # rstrip/lstrip 兼容环境变量值带或不带末尾斜杠
    url = f"{LINKFOXAGENT_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    data = json.dumps(payload).encode("utf-8")

    req = Request(
        url,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "linkfox-os-skill/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

    # swoosh 统一响应：成功 errcode=200（或 0/缺省）；其他值（如 401）为业务错误
    if isinstance(result, dict):
        errcode = result.get("errcode")
        if errcode is not None and errcode not in (200, 0, "200", "0"):
            errmsg = result.get("errmsg") or result.get("message") or "未知错误"
            return {"error": f"业务错误 errcode={errcode}: {errmsg}", "details": result}
    return result


def submit_task(prompt: str, model_id: str = DEFAULT_MODEL_ID) -> dict:
    """Submit a task to AgentStudio. Returns response; task id is under `id`."""
    return api_request(SUBMIT_ENDPOINT, {"prompt": prompt, "modelId": model_id})


def cancel_task(message_id: str) -> dict:
    """Cancel a running task by messageId."""
    return api_request(CANCEL_ENDPOINT, {"messageId": message_id})


# ---------- Per-task output directory bookkeeping ---------------------------
#
# Each task gets its own folder under $PWD/.linkfox-os/output/{YYYYMMDDHHmm}/
# （或 LINKFOX_OS_OUTPUT_DIR env 指定的绝对目录），the moment the task is submitted
# (NOT when results arrive). The folder always contains a result.json describing
# the task — `messageId` (from the create response `id`), original `prompt` text,
# `submittedAt`, `status`, and once the task ends, `stopReason` and `completedAt`.
#
# Why submit-time creation: the default background mode returns immediately
# after submitting, so the messageId would otherwise live only on stdout.
# By dropping a result.json at submit time, the user (or agent) can later
# `ls -t .linkfox-os/output/` to find the most recent task and recover its
# messageId without having captured the original stdout.

def _meta_path(task_dir: str) -> str:
    return os.path.join(task_dir, META_FILENAME)


def find_task_dir(message_id: str):
    """Return the existing output dir for a messageId, or None.

    Cheap: each task has its own dir and we only read tiny JSON files.
    """
    if not message_id or not os.path.isdir(OUTPUT_ROOT):
        return None
    for name in sorted(os.listdir(OUTPUT_ROOT), reverse=True):
        d = os.path.join(OUTPUT_ROOT, name)
        meta_file = _meta_path(d)
        if not os.path.isfile(meta_file):
            continue
        try:
            with open(meta_file, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and data.get("messageId") == message_id:
            return d
    return None


def ensure_task_dir(message_id: str, prompt: str = "") -> str:
    """Get the dir for messageId, creating a new timestamped folder if missing.

    On first creation, writes an initial result.json with
    {messageId, prompt, status='submitted', submittedAt, stopReason=''}.
    Re-runs (poll/status of an already-tracked task) reuse the same folder.
    """
    existing = find_task_dir(message_id)
    if existing:
        return existing

    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    base = datetime.now().strftime("%Y%m%d%H%M")
    task_dir = os.path.join(OUTPUT_ROOT, base)
    # Two tasks in the same minute → suffix to keep them separate
    suffix = 0
    while os.path.isdir(task_dir):
        suffix += 1
        task_dir = os.path.join(OUTPUT_ROOT, f"{base}_{suffix}")
    os.makedirs(task_dir, exist_ok=True)

    meta = {
        "messageId": message_id,
        "prompt": prompt or "",
        "status": "submitted",
        "submittedAt": datetime.now().isoformat(timespec="seconds"),
        "stopReason": "",
    }
    try:
        with open(_meta_path(task_dir), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Warning: failed to write initial meta for {message_id}: {e}", file=sys.stderr)
    return task_dir


def update_meta(task_dir: str, **fields) -> None:
    """Merge `fields` into the dir's result.json. Skips empty/None values
    so we never blank out a value that an earlier write already set
    (e.g. preserving original `prompt` when --poll has no prompt text)."""
    meta_path = _meta_path(task_dir)
    data: dict = {}
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, encoding="utf-8") as f:
                data = json.load(f) or {}
        except (json.JSONDecodeError, OSError):
            data = {}
    for k, v in fields.items():
        if v in (None, ""):
            continue
        data[k] = v
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Warning: failed to update meta at {meta_path}: {e}", file=sys.stderr)


# ---------- 本地最近任务登记（recent-tasks.json 滚动 30 条）--------------------

def _load_recent_tasks() -> list:
    if not os.path.isfile(RECENT_TASKS_FILE):
        return []
    try:
        with open(RECENT_TASKS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def _save_recent_tasks(tasks: list) -> None:
    try:
        os.makedirs(os.path.dirname(RECENT_TASKS_FILE), exist_ok=True)
        tmp = RECENT_TASKS_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(tasks[:RECENT_TASKS_MAX], f, indent=2, ensure_ascii=False)
        os.replace(tmp, RECENT_TASKS_FILE)
    except OSError as e:
        print(f"Warning: failed to write recent-tasks.json: {e}", file=sys.stderr)


def record_task_submit(message_id: str, prompt: str, model_id: str, task_dir: str) -> None:
    """任务提交成功后追加一条到 recent-tasks.json；同 messageId 覆盖，超 30 条丢尾。"""
    if not message_id:
        return
    tasks = [t for t in _load_recent_tasks() if t.get("messageId") != message_id]
    tasks.insert(0, {
        "messageId": message_id,
        "modelId": model_id or DEFAULT_MODEL_ID,
        "prompt": (prompt or "")[:200],
        "status": "submitted",
        "stopReason": "",
        "submittedAt": datetime.now().isoformat(timespec="seconds"),
        "taskDir": task_dir or "",
    })
    _save_recent_tasks(tasks)


def record_task_terminal(message_id: str, stop_reason: str) -> None:
    """任务终态时更新对应记录的 status / stopReason / completedAt；不存在则忽略。"""
    if not message_id:
        return
    tasks = _load_recent_tasks()
    is_success = stop_reason in SUCCESS_STOP_REASONS
    changed = False
    for t in tasks:
        if t.get("messageId") == message_id:
            t["status"] = "finished" if is_success else "error"
            t["stopReason"] = stop_reason or ""
            t["completedAt"] = datetime.now().isoformat(timespec="seconds")
            changed = True
            break
    if changed:
        _save_recent_tasks(tasks)


# -----------------------------------------------------------------------------


def extract_progress(result: dict) -> str:
    """从轮询响应中提取进度信息（任务进行中时 eventList 非空）。

    后端 eventList[] 每项是 AcpEventItemVo：sessionUpdate 为类型标记字符串（非 dict），
    真实内容在 content（thought/message chunk 的 text）或 tool_call 平级字段
    (title / rawInput.args)。故取最后一个事件的可读标签，而非从 sessionUpdate 取 key。
    返回单行进度文本（可能为空）。
    """
    if not isinstance(result, dict):
        return ""
    events = result.get("eventList") or []
    if not events:
        return ""
    last = events[-1]
    return _event_label(last) if isinstance(last, dict) else ""


# ---------- Structured progress for agent clients (plan / commentary / final) --
#
# 把 get 响应解析成通用结构化进度 JSON，供各 agent 客户端（Claude Code / Cursor /
# Codex / Copilot）映射到各自的原语：steps[] → todo/plan；progress_pct+message →
# 进度文字（commentary）；status+result/error → 终态分支（final）。eventList 的
# sessionUpdate 字段由 AgentStudio 透传、结构不固定，故采用通用键名提取 + 原样
# 透传(raw)兜底；待真机确认 sessionUpdate 字段后可收紧提取逻辑。

import re as _re

_PCT_RE = _re.compile(r"(\d+)\s*%")
_FRAC_RE = _re.compile(r"(\d+)\s*/\s*(\d+)")


def _extract_readable(obj, max_len: int = 160) -> str:
    """从任意对象通用提取可读文本：优先常见键，再递归找首个非空字符串。"""
    if isinstance(obj, str):
        return obj.strip()[:max_len]
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, dict):
        for key in ("text", "title", "label", "name", "message", "thought",
                    "step", "currentStep", "description", "summary", "content"):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()[:max_len]
            if isinstance(v, dict):
                r = _extract_readable(v, max_len)
                if r:
                    return r
        for v in obj.values():
            if isinstance(v, str) and v.strip():
                return v.strip()[:max_len]
            if isinstance(v, dict):
                r = _extract_readable(v, max_len)
                if r:
                    return r
    return ""


def _event_string_values(ev) -> list:
    """平铺单个 AcpEventItemVo 里所有字符串值，用于百分比等格式兜底查找。"""
    out = []

    def walk(o):
        if isinstance(o, str):
            out.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    if isinstance(ev, dict):
        for v in ev.values():
            walk(v)
    return out


def _format_tool_call(ev: dict, max_text: int = 200) -> str:
    """把 tool_call 事件格式化成 UI 风格的一行摘要，按 meta.agentStudio.toolName
    的类型选参数字段——避免 [Tool] tool 这种没信息量的行。

    映射（对齐 OS 前端 UI 的展示）：
      Bash / Terminal / Shell   → rawInput.command
      Read / Write / Edit / …   → rawInput.file_path
      Agent / Task / kind=think → rawInput.description
      rawInput.skill 存在       → [Skill] <skill> (<args>)
      其它                      → 拿到 command/file_path/description/args 任一，都出
    """
    raw_input = ev.get("rawInput") if isinstance(ev.get("rawInput"), dict) else {}
    meta = ev.get("meta") or ev.get("_meta") or {}
    meta_tool = ""
    if isinstance(meta, dict):
        as_obj = meta.get("agentStudio")
        if isinstance(as_obj, dict):
            meta_tool = as_obj.get("toolName") or ""
    title = ev.get("title") or ""
    tool_name = meta_tool or title
    skill = raw_input.get("skill") or ""
    command = raw_input.get("command") or ""
    file_path = raw_input.get("file_path") or ""
    description = raw_input.get("description") or ""
    args = raw_input.get("args") or ""

    def _cap(s: str, n: int = max_text) -> str:
        if not s:
            return ""
        s = _re.sub(r"\s+", " ", str(s)).strip()
        return s[:n].rstrip() + "…" if len(s) > n else s

    # 1) skill 调用（linkfox-aigc-imagegen 等）优先
    if skill:
        extra = f" ({_cap(args, 80)})" if isinstance(args, str) and args.strip() else ""
        return f"[Skill] {skill}{extra}"
    # 2) Bash / Terminal → 命令原文
    if tool_name in ("Bash", "Terminal", "Shell"):
        body = command or description
        return f"[Bash] {_cap(body)}" if body else "[Bash]"
    # 3) Read / Write / Edit → 文件路径
    if tool_name in ("Read", "Write", "Edit", "NotebookEdit", "MultiEdit"):
        body = file_path or description
        return f"[{tool_name}] {_cap(body)}" if body else f"[{tool_name}]"
    # 4) 子 agent / think kind → 任务描述
    if tool_name in ("Agent", "Task", "TaskCreate", "TaskUpdate") or ev.get("kind") == "think":
        label = tool_name or "Agent"
        return f"[{label}] {_cap(description)}" if description else f"[{label}]"
    # 5) 兜底：能拿到什么参数用什么，避免 [工具] tool
    fallback = command or file_path or description or args
    if tool_name and fallback:
        return f"[{tool_name}] {_cap(fallback)}"
    if tool_name:
        return f"[{tool_name}]"
    if fallback:
        return f"[Tool] {_cap(fallback)}"
    return ""


def _event_label(ev) -> str:
    """从单个 AcpEventItemVo 提取可读文本标签（供进度展示）。

    - tool_call：走 _format_tool_call（按 toolName 分类展示，[Bash]/[Read]/[Skill]/…）
    - thought/message chunk：读 content.text / content.value
    - 其余：通用提取兜底，最后回退到类型标记字符串
    """
    if not isinstance(ev, dict):
        return ""
    su = ev.get("sessionUpdate")
    content = ev.get("content")

    if su == "tool_call":
        return _format_tool_call(ev)

    # thought / message chunk：读 content.text / content.value
    if isinstance(content, dict):
        for key in ("text", "value"):
            val = content.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        if content:
            return json.dumps(content, ensure_ascii=False)
    if isinstance(content, str) and content.strip():
        return content.strip()

    # 通用兜底
    r = _extract_readable(content)
    if r:
        return r
    return su if isinstance(su, str) and su else ""


def _format_acp_event_line(ev, idx: int = -1, max_text: int = 200) -> str:
    """格式化单个 acpEvent（eventList 项）为可读的过程行，供 --wait/--poll 在
    任务进行中流式输出到 stderr。参照 OS 前端 UI 的展示语义，按工具类型出不同的摘要：

      [思考] The user wants to search for "cat" on Amazon US using SellerSprite…
      [Bash] sed -n '375,410p' /root/.linkfox/.ce/skills/linkfox-aigc-imagegen/scripts/aigc_imagegen.py
      [Read] /root/.linkfox/.ce/skills/linkfox-aigc-imagegen/SKILL.md
      [Write] /tmp/imagegen_params.json
      [Skill] linkfox-aigc-imagegen (args)
      [Agent] Upload laptop image to OSS
      [消息] Launching skill: linkfox-aigc-imagegen

    工具名从 `meta.agentStudio.toolName` 取（Bash / Read / Write / Edit / Agent / Task / …），
    参数按不同工具从 rawInput 里挑最能"人话"表达当前动作的字段：
      - Bash / Terminal   → rawInput.command（跑的命令）
      - Read              → rawInput.file_path（读哪个文件）
      - Write / Edit      → rawInput.file_path
      - Agent(subagent)   → rawInput.description（子 agent 任务描述）
      - Task              → rawInput.description
      - rawInput.skill 存在 → 视为 skill 调用（linkfox-aigc-imagegen 等）
      - 其它 / 拿不到     → 只出工具名，避免 [工具] tool 这种没信息的行

    **流式容错**：agentStudio 的 acpEvent 会分片后填充，本函数遇到不完整或
    结构异常的事件（缺字段 / 类型错乱 / 编码异常）一律降级为空串而不抛异常，
    由外层的"内容变化即重发"逻辑等下一次 poll 拿到补齐后的完整事件。
    """
    try:
        if not isinstance(ev, dict):
            return f"[event {idx}] {ev}" if idx >= 0 else str(ev)
        su = ev.get("sessionUpdate")
        content = ev.get("content")

        # tool_call：走统一格式化（与 parse_progress / _event_label 用同一份 [Bash]/[Read]/[Skill]/… 语义）
        if su == "tool_call":
            return _format_tool_call(ev, max_text=max_text)

        # thought / message chunk：读 content.text / content.value
        text = ""
        if isinstance(content, dict):
            for key in ("text", "value"):
                val = content.get(key)
                if isinstance(val, str) and val.strip():
                    text = val.strip()
                    break
        elif isinstance(content, str) and content.strip():
            text = content.strip()
        if not text:
            try:
                text = _extract_readable(content)
            except Exception:
                text = ""

        if su == "agent_thought_chunk":
            prefix = "[思考]"
        elif su == "agent_message_chunk":
            prefix = "[消息]"
        elif not su:
            prefix = "[消息]"
        else:
            prefix = f"[{su}]"

        # 折叠内部换行/多余空白，保证一个 acpEvent 输出为一行（终端流式更易扫读）
        if text:
            try:
                text = _re.sub(r"\s+", " ", text).strip()
            except Exception:
                # 极端流式截断可能产生非 str/含非法编码的内容，兜底忽略
                text = str(text)
        if len(text) > max_text:
            text = text[:max_text].rstrip() + "…"
        return f"{prefix} {text}" if text else ""
    except Exception:
        # 单个事件格式化失败绝不影响其余事件的解析与后续 poll
        return ""


def _parse_pct(text: str):
    """从文本提取百分比：'3/10' → 30，'45%' → 45；无法解析返回 None。"""
    if not text:
        return None
    m = _PCT_RE.search(text)
    if m:
        return min(100, int(m.group(1)))
    m = _FRAC_RE.search(text)
    if m:
        n, d = int(m.group(1)), int(m.group(2))
        return min(100, int(n * 100 / d)) if d > 0 else None
    return None


def _extract_result_text(message: dict) -> str:
    """从 agentMessageChunks 提取最终结果文本（终态用）。"""
    parts = []
    for chunk in message.get("agentMessageChunks") or []:
        if isinstance(chunk, dict):
            text = _extract_chunk_text(chunk.get("content"))
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def parse_progress(result: dict, prompt_text: str = "") -> dict:
    """解析 get 响应为通用结构化进度（跨客户端可消费）。

    返回字段：
      status        : running | finished | error
      progress_pct  : 0-100 整数或 null（无法推断时）
      message       : 当前在做什么的短文本（映射 commentary）
      steps         : [{label, status: completed|in_progress}]（映射 plan/todo）
      stop_reason   : 原始 stopReason（终态时）
      result        : 最终结果文本（finished 时，从 agentMessageChunks 提取）
      error         : 错误信息（error 时）
      message_id    : 任务 id
      raw           : 原始 eventList + 计数（高级解析兜底，sessionUpdate 字段未确认时用）
    """
    if not isinstance(result, dict):
        return {"status": "error", "error": "invalid response", "raw": result}
    if "error" in result:
        return {"status": "error", "error": result["error"], "raw": result}

    message = result.get("message") or {}
    if not isinstance(message, dict):
        message = {}
    stop_reason = message.get("stopReason") or ""
    event_list = result.get("eventList") or []
    msg_id = message.get("id") or result.get("id") or ""

    if stop_reason:
        status = "finished" if stop_reason in SUCCESS_STOP_REASONS else "error"
    else:
        status = "running"

    steps, progress_pct, cur_message = [], None, ""
    _seen_rl_uris: set = set()  # 去重：同一 uri 只下载一次
    for idx, ev in enumerate(event_list):
        if not isinstance(ev, dict):
            continue
        # label 从 content（thought/message 的 text）或 tool_call 的 title/rawInput 取，
        # 而非 sessionUpdate（后者只是类型标记字符串）。见 _event_label。
        label = _event_label(ev) or f"step {idx + 1}"
        is_last = (idx == len(event_list) - 1)
        steps.append({"label": label, "status": "in_progress" if is_last else "completed"})
        # 事件中的 resource_link 单独作为 step 输出，让调用方 agent 能看到数据文件 URL
        # file:// 是服务器内部路径，对调用方无意义，跳过；同 uri 只处理一次
        for item in (ev.get("contentList") or []):
            if isinstance(item, dict) and item.get("type") == "resource_link":
                uri = item.get("uri") or item.get("url") or ""
                name = item.get("name") or item.get("title") or "data"
                if uri and not uri.startswith("file://") and uri not in _seen_rl_uris:
                    _seen_rl_uris.add(uri)
                    task_dir = ensure_task_dir(msg_id)
                    local = _download_resource_link(uri, name, task_dir)
                    label_rl = f"[文件] [{name}] {uri}"
                    if local:
                        label_rl += f" → 已下载: [{os.path.basename(local)}]({local})"
                    steps.append({"label": label_rl, "status": "completed"})
        ev_content = ev.get("content")
        if isinstance(ev_content, dict) and ev_content.get("type") == "resource_link":
            uri = ev_content.get("uri") or ev_content.get("url") or ""
            name = ev_content.get("name") or ev_content.get("title") or "data"
            if uri and not uri.startswith("file://") and uri not in _seen_rl_uris:
                _seen_rl_uris.add(uri)
                task_dir = ensure_task_dir(msg_id)
                local = _download_resource_link(uri, name, task_dir)
                label_rl = f"[文件] [{name}] {uri}"
                if local:
                    label_rl += f" → 已下载: [{os.path.basename(local)}]({local})"
                steps.append({"label": label_rl, "status": "completed"})
        # 百分比：先从 label 找 n/m 或 N%，再遍历事件所有字符串值兜底
        pct = _parse_pct(label)
        if pct is None:
            for v in _event_string_values(ev):
                pct = _parse_pct(v)
                if pct is not None:
                    break
        if pct is not None:
            progress_pct = pct
        if is_last:
            cur_message = label

    # eventList 为空时（部分环境 fetchInProgressEvents 不返回中间事件），用计数兜底，
    # 让进行中状态至少有可读的 commentary 文本（终态不需要 message，用 result/error）
    if not cur_message and status == "running":
        ec = message.get("eventCount") or 0
        tc = message.get("toolCount") or 0
        if ec or tc:
            cur_message = f"任务执行中（已产生 {ec} 个事件、{tc} 次工具调用）"
        else:
            cur_message = "任务执行中…"

    out = {
        "status": status,
        "progress_pct": progress_pct,
        "message": cur_message,
        "steps": steps,
        "stop_reason": stop_reason or None,
        "message_id": msg_id,
    }
    if status in ("finished", "error"):
        result_text = _extract_result_text(message)
        if result_text:
            # 终态结果全文落盘，返回 truncated 预览 + 文件路径，避免调用方把整段 result
            # 塞到自己的 context（几千字符白烧 token）。真正要看完整内容用 Read 读 result_saved_to。
            n = len(result_text)
            try:
                task_dir = ensure_task_dir(msg_id or "unknown")
                result_path = os.path.join(task_dir, "result.md")
                with open(result_path, "w", encoding="utf-8") as rf:
                    rf.write(result_text)
                out["result_saved_to"] = result_path
                out["result_chars"] = n
                if n <= CHUNK_INLINE_THRESHOLD_CHARS:
                    out["result"] = result_text
                else:
                    out["result"] = result_text[:CHUNK_STDOUT_PREVIEW_CHARS].rstrip() + "…"
                    out["result_truncated"] = True
            except OSError:
                # 落盘失败退化为直接返回全文
                out["result"] = result_text
        if status == "error" and not result_text:
            out["error"] = stop_reason or "task ended abnormally"
    # raw.eventList 只在 running 时保留（供高级解析兜底）；终态丢弃，避免上百条
    # 事件累计上万 token——终态请通过 --poll 读 message.json 拿完整数据。
    if status == "running":
        out["raw"] = {
            "eventList": event_list,
            "eventCount": message.get("eventCount"),
            "toolCount": message.get("toolCount"),
        }
    else:
        out["raw"] = {
            "eventCount": message.get("eventCount"),
            "toolCount": message.get("toolCount"),
        }
    return out


def poll_result(message_id: str, max_wait: int = 300, interval: int = 15,
                stream_events: bool = True) -> dict:
    """Poll 任务直到终态（stopReason 非空）或超时。

    协议：每轮请求带 fromIndex，服务端只回 eventList 中该下标之后的增量切片，
    响应体的 eventTotal 是切片前的累计事件总数。stream_events=True 时按事件绝对
    下标去重，新增或内容变化的事件即时 emit 到 stderr（[思考]/[工具]/[消息] 前缀）。

    acpEvent 内容可能后填充（tool_call 的 title 由占位 "Skill" 后补真实技能名、
    thought/message chunk 的 content.text 分片追加），故下一轮 fromIndex 从
    max(0, eventTotal - TAIL_OVERLAP) 起，让末尾几条重新回读一次去覆盖旧内容。
    """
    TAIL_OVERLAP = 5
    elapsed = 0
    last_progress = ""
    last_result: dict = {}
    # 事件绝对下标 → 上次 emit 的格式化文本；resource_link 用 rl_{idx}_{uri} 键共用
    emitted_lines: dict = {}
    next_from_index = 0
    saw_running = False    # 是否见过 running 态；避免对"首次即终态"的任务回放历史
    while elapsed < max_wait:
        result = api_request(POLL_ENDPOINT, {
            "messageId": message_id,
            "fromIndex": next_from_index,
        })
        if isinstance(result, dict):
            last_result = result

        if "error" in result:
            return result

        message = result.get("message") or {}
        stop_reason = message.get("stopReason") or ""
        running = not stop_reason

        # 流式展示 acpEvent：仅在任务至少有一次处于 running 时输出，"首次即终态"
        # 的任务不回放历史；进行中任务把新增/内容更新的事件实时打出来，终态那次
        # 也补齐后填充的内容。
        events_slice = result.get("eventList") or []
        event_total = result.get("eventTotal")
        if event_total is None:
            # 兼容旧后端（无 eventTotal 字段）：回退为全量下标计算
            event_total = next_from_index + len(events_slice)
        slice_start = max(0, event_total - len(events_slice))
        if stream_events and (running or saw_running):
            for i, ev in enumerate(events_slice):
                abs_idx = slice_start + i
                line = _format_acp_event_line(ev, abs_idx)
                if line and line != emitted_lines.get(abs_idx):
                    print(line, file=sys.stderr, flush=True)
                    emitted_lines[abs_idx] = line
                # 输出事件中的 resource_link URL，让调用方 agent 实时感知数据文件
                # file:// 是服务器内部路径，无法访问，跳过
                if isinstance(ev, dict):
                    for item in (ev.get("contentList") or []):
                        if isinstance(item, dict) and item.get("type") == "resource_link":
                            uri = item.get("uri") or item.get("url") or ""
                            name = item.get("name") or item.get("title") or "data"
                            if uri and not uri.startswith("file://"):
                                rl_key = f"rl_{abs_idx}_{uri}"
                                if rl_key not in emitted_lines:
                                    rl_line = f"[文件] [{name}] {uri}"
                                    print(rl_line, file=sys.stderr, flush=True)
                                    emitted_lines[rl_key] = rl_line
                    ev_content = ev.get("content")
                    if isinstance(ev_content, dict) and ev_content.get("type") == "resource_link":
                        uri = ev_content.get("uri") or ev_content.get("url") or ""
                        name = ev_content.get("name") or ev_content.get("title") or "data"
                        if uri and not uri.startswith("file://"):
                            rl_key = f"rl_{abs_idx}_{uri}"
                            if rl_key not in emitted_lines:
                                rl_line = f"[文件] [{name}] {uri}"
                                print(rl_line, file=sys.stderr, flush=True)
                                emitted_lines[rl_key] = rl_line
            if events_slice:
                last_progress = emitted_lines.get(event_total - 1, "")

        if not running:
            # 终态：stopReason 非空
            return result

        saw_running = True
        # 下一轮从 total - TAIL_OVERLAP 起拉，末尾几条留重叠避免漏掉后填充的事件
        next_from_index = max(0, event_total - TAIL_OVERLAP)

        time.sleep(interval)
        elapsed += interval

        if elapsed % 30 == 0:
            heartbeat = f"... still working ({elapsed}s elapsed)"
            if last_progress:
                heartbeat += f" — {last_progress}"
            print(heartbeat, file=sys.stderr)

    return {
        "error": (
            f"Timeout after {max_wait}s. messageId: {message_id}. "
            f"Use --status {message_id} to check current progress, "
            f"or --poll {message_id} to keep waiting."
        ),
        "lastProgress": last_progress if last_progress else None,
    }


def _extract_chunk_text(content) -> str:
    """从单个 chunk 的 content 提取可读文本。

    content 可能是 dict 或 str。对 dict 按 type 分支：
      - text / output_text: 取 text / value / 字符串化
      - resource_link: 取 uri
      - tool_call / tool_use: [Tool: name]
      - 其他: 一行 JSON 兜底
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, dict):
        return json.dumps(content, ensure_ascii=False)

    ctype = content.get("type")

    # 文本类：多个可能字段
    if ctype in ("text", "output_text", "thinking"):
        for key in ("text", "value", "content"):
            val = content.get(key)
            if isinstance(val, str) and val.strip():
                return val
        # 兜底：content 里没有 text，直接字符串化
        return json.dumps(content, ensure_ascii=False)

    # 资源链接
    if ctype == "resource_link":
        uri = content.get("uri") or content.get("url") or ""
        title = content.get("title") or content.get("name") or "resource"
        return f"Resource [{title}]: {uri}".strip()

    # 工具调用
    if ctype in ("tool_call", "tool_use", "tool_result"):
        name = content.get("name") or content.get("toolName") or "unknown"
        return f"[Tool: {name}]"

    # 其他未知类型：一行 JSON 摘要
    return json.dumps(content, ensure_ascii=False)


def _download_resource_link(uri: str, name: str, output_dir: str) -> str:
    """将 resource_link 的 HTTPS URL 下载到 output_dir，返回本地路径。

    若 uri 是 file:// 协议则跳过（无法远程下载）。失败时打印警告并返回空字符串。
    """
    if not uri or uri.startswith("file://"):
        return ""
    try:
        # 用 name 作为文件名兜底，从 URL 末尾取原始文件名
        url_filename = uri.rstrip("/").split("/")[-1].split("?")[0]
        filename = url_filename or (name.replace(" ", "_") + ".bin")
        local_path = os.path.join(output_dir, filename)
        urlretrieve(uri, local_path)
        return local_path
    except Exception as e:
        print(f"Warning: 下载文件失败 [{name}] {uri}: {e}", file=sys.stderr)
        return ""


def _collect_resource_links(result: dict) -> list:
    """从 get 响应中收集所有 resource_link，涵盖 eventList 和 agentMessageChunks。

    返回 list of (name, uri)，uri 可能是 HTTPS（后端已转换）或 file://（未转换）。
    去重（同 uri 只出现一次）。
    """
    seen = set()
    links = []

    def _add(name, uri):
        # file:// 是服务器内部路径，无法下载且对用户无意义，直接跳过
        if uri and not uri.startswith("file://") and uri not in seen:
            seen.add(uri)
            links.append((name or "data", uri))

    # eventList：contentList 和 content 两个位置
    for ev in (result.get("eventList") or []):
        if not isinstance(ev, dict):
            continue
        for item in (ev.get("contentList") or []):
            if isinstance(item, dict) and item.get("type") == "resource_link":
                _add(item.get("name") or item.get("title"), item.get("uri") or item.get("url") or "")
        ev_content = ev.get("content")
        if isinstance(ev_content, dict) and ev_content.get("type") == "resource_link":
            _add(ev_content.get("name") or ev_content.get("title"), ev_content.get("uri") or ev_content.get("url") or "")

    # agentMessageChunks：终态结果里也可能有 resource_link
    message = result.get("message") or {}
    for chunk in (message.get("agentMessageChunks") or []):
        if not isinstance(chunk, dict):
            continue
        content = chunk.get("content")
        if isinstance(content, dict) and content.get("type") == "resource_link":
            _add(content.get("name") or content.get("title"), content.get("uri") or content.get("url") or "")

    return links


def fetch_share_url(message_id: str) -> dict:
    """任务终态后调用 /agent-studio/task/getShareUrl 换取工作台公开分享链接。

    仅在 stopReason 非空后调用；后端会二次校验（任务归属 + 终态），失败时返回
    带 error 字段的 dict，调用方按需展示或忽略。
    """
    if not message_id:
        return {"error": "missing messageId"}
    return api_request(SHARE_URL_ENDPOINT, {"messageId": message_id})


def format_result(result: dict, message_id: str = "", prompt_text: str = "") -> str:
    """Format a poll result as human-readable text.

    结果从 message.agentMessageChunks[].content 提取，按 chunk type 转纯文本。
    同时把完整 message JSON 落盘到任务目录，便于事后追溯。
    """
    if "error" in result:
        return f"Error: {result['error']}"

    lines = []

    # 复用提交时创建的目录（或为从未见过的任务新建一个）
    output_dir = ensure_task_dir(message_id or "unknown", prompt=prompt_text)

    message = result.get("message") or {}
    if not isinstance(message, dict):
        message = {}

    stop_reason = message.get("stopReason") or ""
    is_success = stop_reason in SUCCESS_STOP_REASONS
    if stop_reason:
        status = "finished" if is_success else "error"
    else:
        status = "unknown"
    lines.append(f"Status: {status}")
    if stop_reason:
        lines.append(f"StopReason: {stop_reason}")

    # 落盘完整 message JSON（事后追溯用）
    message_path = os.path.join(output_dir, "message.json")
    try:
        with open(message_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Warning: failed to write message.json: {e}", file=sys.stderr)

    tool_count = message.get("toolCount")
    event_count = message.get("eventCount")
    extras = []
    if tool_count is not None:
        extras.append(f"toolCount={tool_count}")
    if event_count is not None:
        extras.append(f"eventCount={event_count}")
    if extras:
        lines.append(" | ".join(extras))

    chunks = message.get("agentMessageChunks") or []
    if chunks:
        lines.append("")
        lines.append(f"--- Result ({len(chunks)} chunk(s)) ---")
        any_saved = False
        for i, chunk in enumerate(chunks, 1):
            if not isinstance(chunk, dict):
                lines.append(f"[chunk {i}] {chunk}")
                continue
            content = chunk.get("content")
            text = _extract_chunk_text(content) or ""
            n = len(text)
            # 短 chunk 直接内联；长 chunk 落盘 + 短预览，避免调用方 agent 白烧 token
            if n <= CHUNK_INLINE_THRESHOLD_CHARS:
                lines.append(f"[chunk {i}] {text}")
                continue
            chunk_filename = f"chunk_{i}.md"
            chunk_path = os.path.join(output_dir, chunk_filename)
            try:
                with open(chunk_path, "w", encoding="utf-8") as cf:
                    cf.write(text)
            except OSError as e:
                print(f"Warning: failed to write {chunk_filename}: {e}", file=sys.stderr)
                # 落盘失败仍然把内容打出去，别丢内容
                lines.append(f"[chunk {i}] {text}")
                continue
            any_saved = True
            preview = text[:CHUNK_STDOUT_PREVIEW_CHARS].rstrip()
            if len(text) > CHUNK_STDOUT_PREVIEW_CHARS:
                preview += "…"
            preview_flat = " ".join(preview.split())
            lines.append(f"[chunk {i}] length={n} chars → saved: {chunk_path}")
            lines.append(f"  preview: {preview_flat}")
        if any_saved:
            lines.append("")
            lines.append("（完整内容请用 Read 工具读上面的 chunk_*.md 路径，仅需要的段落再展示给用户，避免 stdout 全量占 token）")
    else:
        lines.append("")
        lines.append("(no agentMessageChunks — task may still be running or returned no content)")

    # 收集所有 resource_link（eventList + agentMessageChunks），下载并输出
    all_resource_links = _collect_resource_links(result)
    if all_resource_links:
        lines.append("")
        lines.append("--- 数据文件 ---")
        for rl_name, rl_uri in all_resource_links:
            lines.append(f"[{rl_name}] {rl_uri}")
            local_path = _download_resource_link(rl_uri, rl_name, output_dir)
            if local_path:
                lines.append(f"  已下载到本地: [{os.path.basename(local_path)}]({local_path})")
            else:
                lines.append(f"  (跳过下载，uri={rl_uri})")

    # 任务已终态：尝试拉工作台公开分享链接（后端会二次校验归属+终态），有则显示
    share_url = ""
    share_id = ""
    if stop_reason and message_id:
        share_resp = fetch_share_url(message_id)
        if isinstance(share_resp, dict) and "error" not in share_resp:
            share_url = share_resp.get("shareUrl") or ""
            share_id = share_resp.get("shareId") or ""
        if share_url:
            lines.append("")
            lines.append("--- 分享链接 ---")
            lines.append(f"ShareUrl: {share_url}")
            if share_id:
                lines.append(f"ShareId: {share_id}")
        elif isinstance(share_resp, dict) and share_resp.get("error"):
            lines.append("")
            lines.append(f"(获取分享链接失败: {share_resp.get('error')})")

    # 更新 result.json（保留 submittedAt 等初始字段）
    meta_extra = {}
    if share_url:
        meta_extra["shareUrl"] = share_url
    if share_id:
        meta_extra["shareId"] = share_id
    update_meta(
        output_dir,
        status=status,
        stopReason=stop_reason,
        messageId=message_id,
        prompt=prompt_text,
        completedAt=datetime.now().isoformat(timespec="seconds"),
        **meta_extra,
    )
    # 同步更新本地 recent-tasks.json 里对应 messageId 的记录（终态标记）
    if stop_reason and message_id:
        record_task_terminal(message_id, stop_reason)
    lines.append(f"\nResult meta saved to: {os.path.join(output_dir, META_FILENAME)}")
    lines.append(f"Full message JSON saved to: {message_path}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="linkfox-os - AgentStudio async task CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("task", nargs="?", help="Prompt / task description to submit")
    parser.add_argument(
        "--stdin", action="store_true",
        help="Read task from stdin instead of positional argument (safe against shell injection)",
    )
    parser.add_argument(
        "--model", dest="model_id", default=DEFAULT_MODEL_ID,
        help=f"Model ID (default: {DEFAULT_MODEL_ID})",
    )
    parser.add_argument(
        "--wait", action="store_true",
        help="Block until task completes and return the result (default: background, return messageId immediately)",
    )
    parser.add_argument(
        "--poll", dest="poll_id", metavar="MESSAGE_ID",
        help="Poll result for an existing messageId until terminal or timeout",
    )
    parser.add_argument(
        "--watch", dest="watch_id", metavar="MESSAGE_ID",
        help="Poll and emit one structured progress JSON per change (JSONL) until terminal; "
             "for agent clients to map to plan/commentary/final primitives",
    )
    parser.add_argument(
        "--status", dest="status_id", metavar="MESSAGE_ID",
        help="One-shot check of current status & progress for a messageId (no polling)",
    )
    parser.add_argument(
        "--cancel", dest="cancel_id", metavar="MESSAGE_ID",
        help="Cancel a running task by messageId",
    )
    parser.add_argument(
        "--list-recent", dest="list_recent", type=int, nargs="?", const=RECENT_TASKS_MAX, metavar="N",
        help=f"List the most recent N tasks (default {RECENT_TASKS_MAX}, capped at {RECENT_TASKS_MAX}) from $OUTPUT_ROOT/recent-tasks.json (滚动登记表：提交时追加、终态时更新)",
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Max wait time in seconds (default: 300)",
    )
    parser.add_argument(
        "--interval", type=int, default=15,
        help="Poll interval in seconds (default: 15)",
    )
    parser.add_argument(
        "--format", "-f", choices=["json", "text", "progress"], default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--no-stream-events", dest="stream_events", action="store_false",
        help="Do not stream per-acpEvent progress ([思考] thought / [工具] tool_call / [消息] message) "
             "to stderr while waiting. Default: stream them so the live process is visible "
             "(used by the Codex direct-run path).",
    )

    args = parser.parse_args()

    # Mode: list recent tasks from local recent-tasks.json — pure local, no API call.
    # 数据源是 $OUTPUT_ROOT/recent-tasks.json（提交时追加、终态时更新），滚动 30 条。
    if args.list_recent is not None:
        n = max(1, min(args.list_recent, RECENT_TASKS_MAX))
        rows = _load_recent_tasks()[:n]
        if args.format == "json":
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        else:
            if not rows:
                print(f"(no local tasks recorded yet — file: {RECENT_TASKS_FILE})")
                return
            for r in rows:
                submitted = r.get("submittedAt", "")
                status = (r.get("status") or "submitted")[:10]
                mid = r.get("messageId", "")
                model = r.get("modelId", "")
                prompt = (r.get("prompt") or "")[:80]
                print(f"{submitted}  {status:<10}  {mid}  [{model}]  {prompt}")
        return

    # Mode: cancel a running task
    if args.cancel_id:
        result = cancel_task(args.cancel_id)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
                sys.exit(1)
            else:
                print(f"Task {args.cancel_id} cancelled successfully.")
                task_dir = find_task_dir(args.cancel_id)
                if task_dir:
                    update_meta(task_dir, status="cancelled",
                                completedAt=datetime.now().isoformat(timespec="seconds"))
                record_task_terminal(args.cancel_id, "cancelled")
        return

    # Mode: one-shot status — single API call, no polling, returns immediately.
    if args.status_id:
        # --status 是 one-shot 快照，无本地状态需要维护，总是拉全量：fromIndex=0
        result = api_request(POLL_ENDPOINT, {"messageId": args.status_id, "fromIndex": 0})
        if args.format == "progress":
            print(json.dumps(parse_progress(result), ensure_ascii=False))
            return
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                message = result.get("message") or {}
                stop_reason = message.get("stopReason") or ""
                if stop_reason:
                    status = "finished" if stop_reason in SUCCESS_STOP_REASONS else "error"
                    print(f"Status: {status}")
                    print(f"StopReason: {stop_reason}")
                    print("(task ended; use --poll to fetch full result)")
                else:
                    print("Status: working")
                    progress = extract_progress(result)
                    if progress:
                        print(f"Progress: {progress}")
                    else:
                        print("Progress: (no progress info yet)")
        return

    # Mode: poll existing messageId
    if args.poll_id:
        result = poll_result(args.poll_id, max_wait=args.timeout, interval=args.interval,
                             stream_events=args.stream_events)
        if args.format == "progress":
            print(json.dumps(parse_progress(result), ensure_ascii=False))
        elif args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_result(result, message_id=args.poll_id))
        return

    # Mode: watch — emit structured progress JSONL until terminal (for agent clients).
    # 每次进度变化（status/progress_pct/message/steps 数）输出一行 JSON；终态退出。
    if args.watch_id:
        elapsed = 0
        last_sig = None
        while elapsed <= args.timeout:
            # --watch 无状态循环，每次拉全量事件用于计算 progress 签名；fromIndex=0
            result = api_request(POLL_ENDPOINT, {"messageId": args.watch_id, "fromIndex": 0})
            if "error" in result:
                print(json.dumps(parse_progress(result), ensure_ascii=False), flush=True)
                break
            prog = parse_progress(result)
            sig = (prog.get("status"), prog.get("progress_pct"),
                   prog.get("message"), len(prog.get("steps") or []))
            if sig != last_sig:
                print(json.dumps(prog, ensure_ascii=False), flush=True)
                last_sig = sig
            if prog.get("status") in ("finished", "error"):
                break
            time.sleep(args.interval)
            elapsed += args.interval
        return

    # Require task for submit modes
    if args.stdin:
        task_text = sys.stdin.read().strip()
        if not task_text:
            parser.error("stdin was empty")
    elif args.task:
        task_text = args.task
    else:
        parser.error("task is required (or use --stdin, --status MESSAGE_ID, or --poll MESSAGE_ID)")

    response = submit_task(task_text, model_id=args.model_id)
    if "error" in response:
        error_msg = response["error"]
        print(f"Error: {error_msg}", file=sys.stderr)
        if response.get("details"):
            print(f"Details: {response['details']}", file=sys.stderr)
        # HTTP 401/403 almost always means a bad or missing API key
        if "401" in error_msg or "403" in error_msg or "Unauthorized" in error_msg or "Forbidden" in error_msg:
            key_val = os.environ.get("LINKFOXAGENT_API_KEY") or ""
            masked = key_val[:4] + "****" + key_val[-4:] if len(key_val) > 8 else ("(未设置)" if not key_val else "****")
            print(
                "\nHint: 任务发起失败，请检查 LINKFOXAGENT_API_KEY 是否正确。\n"
                f"  当前值: {masked}\n"
                "  获取 API Key: https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb",
                file=sys.stderr,
            )
        sys.exit(1)

    # 注意：create 返回的任务 ID 字段是 "id"（不是 "messageId"）
    message_id = response.get("id") or ""
    if not message_id:
        key_val = os.environ.get("LINKFOXAGENT_API_KEY") or ""
        masked = key_val[:4] + "****" + key_val[-4:] if len(key_val) > 8 else ("(未设置)" if not key_val else "****")
        print(
            "Error: 任务发起失败，服务器未返回 id。\n"
            "请检查 LINKFOXAGENT_API_KEY 是否正确。\n"
            f"  当前值: {masked}\n"
            "  获取 API Key: https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb\n"
            f"  服务器原始响应: {response}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 提交成功立即落盘 result.json，便于事后用 --list-recent 恢复 messageId
    task_dir = ""
    try:
        task_dir = ensure_task_dir(message_id, prompt=task_text)
    except Exception as e:
        print(f"Warning: 无法落盘 messageId 元数据: {e}", file=sys.stderr)
    # 同时登记到本地 recent-tasks.json（滚动 30 条），--list-recent 秒读
    record_task_submit(message_id, task_text, args.model_id, task_dir)

    # Mode: background (default) — return messageId immediately so the caller can continue
    if not args.wait:
        out = {"messageId": message_id}
        if task_dir:
            out["taskDir"] = task_dir
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # Mode: --wait — block until task completes
    print(f"Task submitted. messageId: {message_id}", file=sys.stderr)
    print("Waiting for result...", file=sys.stderr)

    result = poll_result(message_id, max_wait=args.timeout, interval=args.interval,
                         stream_events=args.stream_events)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_result(result, message_id=message_id, prompt_text=task_text))

    # stopReason 非空且不在 SUCCESS_STOP_REASONS 视为异常退出
    message = result.get("message") or {}
    stop_reason = message.get("stopReason") or ""
    if stop_reason and stop_reason not in SUCCESS_STOP_REASONS:
        sys.exit(1)


if __name__ == "__main__":
    main()
