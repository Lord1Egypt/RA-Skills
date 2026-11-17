#!/usr/bin/env python3
"""
LinkFox 定时任务管理 - LinkFox Skill
统一调用定时任务的五个接口：create / update / update-status / delete / list。

Usage:
  python task_scheduler.py <action> '<JSON parameters>'           # 自动：小结果全量；大结果写文件+摘要
  python task_scheduler.py <action> '<JSON parameters>' --inline  # 强制全量打印到 stdout
  python task_scheduler.py <action> '<JSON parameters>' --allow-recurring-text  # 跳过 promptContent 周期词校验（仅在确认误报时使用）

  <action> ∈ create | update | update-status | delete | list

输出策略（脚本默认行为）：
  - **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-task-scheduler-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）
  - 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
  - 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
  - 加 `--inline` 强制全量打印到 stdout（同样落盘）
  - `delete` 接口后端无返回体，脚本会输出操作成功提示

环境变量：
  - LINKFOX_AGENT_API_KEY  : 必填，作为 Authorization 头
  - LINKFOX_TOOL_GATEWAY  : 可选，覆盖默认 base url（默认 https://tool-gateway.linkfox.com）
  - LINKFOX_TIMER_TASK    : 由定时任务调度器在触发任务时注入，**仅值为 "1" 时生效**。命中时，
                            所有写操作（create / remind / update / update-status / delete）
                            一律直接失败退出——定时任务内部不允许再操作定时任务，
                            否则任务会自我复制、指数增长。list 仍可用（只读）。
"""

import json
import os
import re
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


SLUG = "linkfox-task-scheduler"

# action -> 端点路径
ACTIONS = {
    "create": "/task/add4api",
    "update": "/task/update4api",
    "update-status": "/task/updateStatus4api",
    "delete": "/task/delete4api",
    "list": "/task/list4api",
}

# 客户端合成 action（不直接对应 API 端点，需预处理后转为 ACTIONS 中的操作）
SYNTHETIC_ACTIONS = {"remind"}

# 响应小于等于该字节数时，直接全量输出，不落文件
SMALL_THRESHOLD = 8000


def base_url():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from linkfox_paths import get_api_base
    return get_api_base()


def get_api_key():
    key = os.environ.get("LINKFOX_AGENT_API_KEY")
    if not key:
        print(
            "API Key not configured. Please complete authorization first:\n"
            "1. Visit https://skill.linkfox.com/linkfoxskills/guide.htm to obtain your Key\n"
            "2. Set the environment variable: export LINKFOX_AGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# 定时任务上下文守卫（LINKFOX_TIMER_TASK）
#
# 调度器触发一个定时任务时，会向执行环境注入 LINKFOX_TIMER_TASK=1。
# 此时 Agent 正在"执行某个定时任务"，绝不能再创建 / 修改 / 删除定时任务：
#   - 再创建 → 任务自我复制，每次触发都多一个，指数增长（线上已出现单账号 1100+ 副本）
#   - 再修改 / 删除 → 定时任务改动用户的其它任务，用户无从感知，且可能改掉自己
# 因此在这里做能力隔离：带该标记时，写操作一律直接失败，只保留只读的 list。
# 这是硬性拦截，不提供绕过开关——需要排任务请在交互会话里做。
# ---------------------------------------------------------------------------

# 写操作：在定时任务上下文中一律禁止
WRITE_ACTIONS = {"create", "update", "update-status", "delete", "remind"}


def in_timer_task():
    """当前是否运行在定时任务的执行上下文中。

    只认 LINKFOX_TIMER_TASK=1（去空白后严格等于 "1"）。其它任何值——包括
    "true" / "yes" / "0" / 空 / 未设置——都视为普通交互会话，不拦截。
    """
    return os.environ.get("LINKFOX_TIMER_TASK", "").strip() == "1"


def guard_timer_task(action):
    """定时任务上下文中禁止一切定时任务写操作。"""
    if action not in WRITE_ACTIONS or not in_timer_task():
        return

    if action in ("create", "remind"):
        headline = "失败：定时任务内部无法再次创建定时任务。"
    else:
        headline = f"失败：定时任务内部无法{'修改' if action.startswith('update') else '删除'}定时任务。"

    print(
        headline + "\n"
        "\n"
        f"当前进程带有 LINKFOX_TIMER_TASK={os.environ.get('LINKFOX_TIMER_TASK')}，"
        "说明本次执行是由定时任务调度器触发的。"
        f"在这个上下文中 `{action}` 等写操作（create / remind / update / "
        "update-status / delete）一律被拒绝，仅允许只读的 `list`。\n"
        "\n"
        "原因：定时任务在执行时再创建定时任务，会让任务每次触发都多出一个副本，"
        "自我复制、指数增长（线上已出现单账号 1100+ 副本的事故）；"
        "修改 / 删除同理会让定时任务擅自改动用户的其它任务。\n"
        "\n"
        "正确做法：\n"
        "  - 本次执行只完成任务内容本身（出数据、出报告、发通知），不要碰任务调度。\n"
        "  - 周期由任务自身的 execType / execPoint / execTime 决定，"
        "已经会按周期自动再次触发，不需要、也不应该由任务自己去续期或重排。\n"
        "  - 需要新增 / 调整定时任务，请在与用户的交互会话中进行。\n"
        "\n"
        "本拦截没有绕过开关。请把这条结果如实告知用户，不要改写参数重试。",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# promptContent 周期性文案校验
#
# 周期**只能**由 execType / execPoint / execTime 表达。若把"每天…""定时任务"
# 之类的周期性 / 元指令文案写进 promptContent，任务每次触发时 Agent 会把它再当成
# 一次"创建定时任务"的请求，导致定时任务自我复制、指数增长。
# 因此在 create / update / remind 落库前直接拦下，不做静默改写。
# ---------------------------------------------------------------------------

# 元指令：出现即意味着 promptContent 在指挥 Agent 去"排任务"，一律拦截
META_PATTERNS = [
    r"定时任务", r"定时执行", r"定期执行", r"周期性执行", r"周期执行",
    r"循环执行", r"重复执行", r"自动重复", r"新增任务", r"创建任务",
    r"schedule\s+(?:a\s+)?task", r"scheduled\s+task", r"\bcron\b",
    r"recurring\s+task",
]

# 周期副词：说明周期被写进了任务内容里
PERIOD_PATTERNS = [
    r"每天", r"每日", r"每周", r"每月", r"每年", r"每季度",
    r"每小时", r"每分钟", r"每隔", r"每个工作日", r"每工作日",
    r"\bdaily\b", r"\bweekly\b", r"\bmonthly\b", r"\bhourly\b",
    r"every\s+(?:day|week|month|year|hour|minute)",
]


def _scan_recurring_text(text):
    """返回命中的周期性 / 元指令片段列表。"""
    hits = []
    for pat in META_PATTERNS + PERIOD_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            hits.append(m.group(0))
    return hits


def validate_prompt_content(params, allow_recurring_text=False):
    """校验 promptContent：必须是"执行一次"的指令，不得含周期性 / 元指令表述。"""
    content = params.get("promptContent")
    if not isinstance(content, str) or not content.strip():
        return

    hits = _scan_recurring_text(content)
    if not hits or allow_recurring_text:
        return

    print(
        "promptContent 含周期性 / 定时元指令，已拒绝提交：" + "、".join(sorted(set(hits))) + "\n"
        "\n"
        "原因：promptContent 是每次触发时交给 Agent 执行的指令，必须写成"
        "「执行一次」的任务本身。写成周期性表述会让 Agent 每次执行时又去创建"
        "一个新的定时任务，任务会自我复制、指数增长。\n"
        "\n"
        "正确做法：周期只由 execType / execPoint / execTime 表达。\n"
        "  ✗ promptContent: \"每天自动执行亚马逊美国站潜力新品选品任务\"\n"
        "  ✓ promptContent: \"执行亚马逊美国站潜力新品选品，输出 Top 20 潜力新品及入选理由\"\n"
        "    execType: 1, execTime: \"09:00\"\n"
        "\n"
        "确认为误报（如\"统计每天的销量\"这类描述性用词）时，可加 --allow-recurring-text 跳过本校验。",
        file=sys.stderr,
    )
    sys.exit(1)


def preprocess_remind(params):
    """把 remind 参数转成 create 参数，在客户端计算目标时刻。"""
    from datetime import datetime, timedelta

    delay_minutes = float(params.get("delayMinutes", 0))
    delay_hours = float(params.get("delayHours", 0))
    total_minutes = delay_minutes + delay_hours * 60

    if total_minutes <= 0:
        print(
            "remind action requires delayMinutes > 0 or delayHours > 0",
            file=sys.stderr,
        )
        sys.exit(1)

    message = params.get("message", "提醒时间到！")
    title = params.get("title", "定时提醒")
    feishu_webhook = params.get("feishuWebhook") or params.get("webhookUrl")

    now = datetime.now()
    target = now + timedelta(minutes=total_minutes)
    exec_point = target.strftime("%Y-%m-%d")
    exec_time = target.strftime("%H:%M")

    create_params = {
        "title": title,
        "promptContent": message,
        "taskStatus": True,
        "execType": 4,
        "execPoint": exec_point,
        "execTime": exec_time,
    }

    if not feishu_webhook:
        print(
            "remind action requires feishuWebhook or webhookUrl "
            "(noticeList is required; provide a Feishu bot webhook address)",
            file=sys.stderr,
        )
        sys.exit(1)

    create_params["noticeList"] = [
        {"noticeType": 3, "address": feishu_webhook, "sign": ""}
    ]

    return "create", create_params


def call_api(action, params):
    api_key = get_api_key()
    url = base_url() + ACTIONS[action]
    data = json.dumps(params).encode("utf-8")
    req = Request(
        url,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/2.0",
            "SESSION_ID": os.environ.get("SESSION_ID", ""),
        "MESSAGE_ID": os.environ.get("MESSAGE_ID", ""),
            "MODE_ID": os.environ.get("MODE_ID", ""),
        "APP_NAME": os.environ.get("APP_NAME", ""),
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=150) as response:
            body = response.read().decode("utf-8")
            if not body.strip():
                # delete 等接口可能无返回体
                return {"_empty": True}
            return json.loads(body)
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        try:
            return json.loads(body) if body else {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception:
            return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def _find_main_list(obj):
    """递归找到元素数最多的 list 字段。不写死字段名，适配任何结构。"""
    best = (None, None, -1)

    def walk(node, path):
        nonlocal best
        if isinstance(node, list):
            if len(node) > best[2]:
                best = (path, node, len(node))
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k)

    walk(obj, "")
    return best[0], best[1]


def summarize(result):
    """打印紧凑摘要。"""
    if not isinstance(result, dict):
        print(f"Response type: {type(result).__name__}")
        print(json.dumps(result, ensure_ascii=False)[:500])
        return

    print(f"Top-level keys: {list(result.keys())}")

    for k in ("errcode", "errorCode", "code", "errmsg", "errorMsg", "msg",
              "total", "totalCount", "count", "pageNum", "currentPage",
              "pageSize", "perPage", "pages", "costToken", "costTime", "success"):
        if k in result:
            v = result[k]
            if isinstance(v, (int, float, bool, str)):
                print(f"  {k}: {v}")

    list_path, main_list = _find_main_list(result)
    if list_path is not None and main_list:
        print(f"\nMain list field: `{list_path}` (length={len(main_list)})")
        sample = main_list[:3]
        print(f"Sample (first {len(sample)} of {len(main_list)}):")
        print(json.dumps(sample, indent=2, ensure_ascii=False))


def _resolve_output_path(ts):
    """落到 <cwd>/linkfox/<日期>/<session>/data/<slug>-<ts>.json，按 SESSION_ID 聚合到同一会话。"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from linkfox_paths import resolve_data_path
    return resolve_data_path(SLUG, ts)


def main():
    argv = sys.argv[1:]
    inline = False
    if "--inline" in argv:
        inline = True
        argv = [a for a in argv if a != "--inline"]

    allow_recurring_text = False
    if "--allow-recurring-text" in argv:
        allow_recurring_text = True
        argv = [a for a in argv if a != "--allow-recurring-text"]

    if len(argv) < 2:
        print(
            "Usage: task_scheduler.py <action> '<JSON parameters>' "
            "[--inline] [--allow-recurring-text]\n"
            f"  <action> ∈ {' | '.join(ACTIONS)}",
            file=sys.stderr,
        )
        sys.exit(1)

    action = argv[0].strip().lower()
    all_valid = set(ACTIONS) | SYNTHETIC_ACTIONS
    if action not in all_valid:
        print(
            f"Unknown action '{action}'. Valid: {', '.join(sorted(all_valid))}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 定时任务上下文中禁止写操作（防自我复制），在解析参数前就拦掉
    guard_timer_task(action)

    try:
        params = json.loads(argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid parameter format: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(params, dict):
        print("Parameters must be a JSON object.", file=sys.stderr)
        sys.exit(1)

    # memberId 由后端从 token 注入，调用方传了也会被覆盖；这里主动剔除避免误导。
    params.pop("memberId", None)

    # 合成 action 预处理：转换为底层 API action + 参数
    if action == "remind":
        action, params = preprocess_remind(params)

    # templateId 是 add4api 的非必填来源追溯字段，调用方不需要传入
    if action == "create":
        params.pop("templateId", None)

    # 周期只能由 execType/execPoint/execTime 表达，promptContent 里不得有周期性表述
    if action in ("create", "update"):
        validate_prompt_content(params, allow_recurring_text)

    result = call_api(action, params)

    # delete 等无返回体的成功响应
    if isinstance(result, dict) and result.get("_empty"):
        print(f"OK: {action} succeeded (no response body).")
        return

    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    ts = int(time.time())
    out_path = _resolve_output_path(ts)
    try:
        with open(out_path, "w") as f:
            f.write(serialized)
        print(f"Saved full response: {out_path} ({len(serialized)} bytes)")
    except OSError as e:
        print(f"Failed to save to {out_path}: {e}", file=sys.stderr)

    if inline or len(serialized.encode("utf-8")) <= SMALL_THRESHOLD:
        print(serialized)
    else:
        summarize(result)


if __name__ == "__main__":
    main()
