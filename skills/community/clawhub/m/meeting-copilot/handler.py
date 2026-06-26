#!/usr/bin/env python3
"""
Meeting Ops Copilot - handler.py
会议全生命周期辅助：会前 briefing / 会中纪要结构化整理 / 会后待办追踪与 follow-up 草稿
支持 boss mode（向上汇报视角）和 executor mode（向下追踪视角）
"""
import sys
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# ─── 常量 ────────────────────────────────────────────────────────────────────

DISCLAIMER = """
⚠️ **免责声明**
本工具的输出依赖用户输入的原始信息，不做信息真实性担保。
本 skill 不提供实时语音转录、不接入日历系统、不自动发送通知或邮件（仅生成草稿）。
涉及重大决策时，请结合实际情况自行判断或咨询专业人士。
"""

BOSS_BRIEFING_TEMPLATE = """
═══════════════════════════════════════════════════════
  📋 会议 Briefing（{meeting_topic}）
  📅 {meeting_date} | 视角：Boss（向上汇报）
═══════════════════════════════════════════════════════

🎯 一句话结论
───────────────────────────────────────────────────────
{conclusion}

📌 核心要点
───────────────────────────────────────────────────────
{key_points}

🔍 待决策事项
───────────────────────────────────────────────────────
{decisions_needed}

⚠️ 风险提示
───────────────────────────────────────────────────────
{risks}

✅ 建议行动
───────────────────────────────────────────────────────
{suggested_actions}

{DISCLAIMER}
"""

EXECUTOR_MINUTES_TEMPLATE = """
═══════════════════════════════════════════════════════
  📋 会议纪要（{meeting_topic}）
  📅 {meeting_date} | 视角：Executor（向下追踪）
═══════════════════════════════════════════════════════

💬 讨论要点
───────────────────────────────────────────────────────
{discussion_points}

✅ 决议事项
───────────────────────────────────────────────────────
{decisions}

📌 待办追踪
───────────────────────────────────────────────────────
{action_items}

{DISCLAIMER}
"""

EXECUTOR_FOLLOWUP_TEMPLATE = """
═══════════════════════════════════════════════════════
  📤 Meeting Follow-up（{meeting_topic}）
  📅 {meeting_date} | 视角：Executor（向下追踪）
═══════════════════════════════════════════════════════

📌 待办追踪列表
───────────────────────────────────────────────────────
{followup_items}

📧 邮件草稿
───────────────────────────────────────────────────────
{draft_email}

💬 简短消息草稿
───────────────────────────────────────────────────────
{draft_message}

{DISCLAIMER}
"""

BOSS_FOLLOWUP_TEMPLATE = """
═══════════════════════════════════════════════════════
  📤 Meeting Follow-up（{meeting_topic}）
  📅 {meeting_date} | 视角：Boss（向上汇报）
═══════════════════════════════════════════════════════

🎯 会议结论摘要
───────────────────────────────────────────────────────
{summary}

📌 待办追踪
───────────────────────────────────────────────────────
{followup_items}

📧 邮件草稿
───────────────────────────────────────────────────────
{draft_email}

💬 简短消息草稿
───────────────────────────────────────────────────────
{draft_message}

{DISCLAIMER}
"""


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def split_list(text: str, sep: str = "|") -> List[str]:
    """将分隔字符串拆分为列表，过滤空项"""
    return [s.strip() for s in text.split(sep) if s.strip()]


def parse_raw_text_to_points(raw_text: str) -> List[str]:
    """将原始讨论文本拆分为讨论要点列表"""
    raw_text = raw_text.strip()
    # 按常见分隔符拆分：句号/分号/换行
    points = re.split(r'[；;；\n]+', raw_text)
    result = []
    for p in points:
        p = p.strip()
        if p:
            # 去掉句末标点
            p = re.sub(r'[。.．,，]$', '', p)
            if p:
                result.append(p)
    return result


def extract_action_items(raw_text: str, decisions: str, participants: str) -> List[Dict[str, str]]:
    """
    从原始文本中提取待办事项。
    策略：
    1. 切分为多个短句后识别 "X负责Y" / "X做Y" / "X跟进Y" 等模式
    2. 识别 "截止.../deadline..." 等时间线索
    3. 基于关键词判断优先级
    """
    # 纯空格字符串校验（DEF-001 修复）
    if not raw_text or not raw_text.strip():
        return []
    action_items = []
    person_names = split_list(participants, "|") if participants else []
    decision_list = split_list(decisions, "|") if decisions else []

    # 将原文和决议拼接后按句切分，减少跨句误匹配
    text_for_search = raw_text
    clauses = re.split(r'[；;\n\r]+', text_for_search)

    # 常见动作关键词（优先级顺序）
    action_patterns = [
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>负责)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>做)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>跟进)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>完成)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>提交)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>对接)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>协调)(?P<task>[^，。,;；\n\r]+)',
        r'(?P<owner>[\u4e00-\u9fff]{2,5})(?:分头)?(?P<verb>安排)(?P<task>[^，。,;；\n\r]+)',
    ]

    # 英文名兜底
    action_patterns.append(
        r'(?P<owner>[A-Za-z][A-Za-z0-9_\-]{1,20})(?:\s*\(?(?P<modifier>[^)）\s]{0,6})\)?)?(?P<verb>负责|做|跟进|完成|提交|对接|协调|安排)(?P<task>[^，。,;；\n\r]+)'
    )

    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue

        found_one = False
        for pattern in action_patterns:
            # 每个短句优先取第一条可用匹配，避免一个句子内重复匹配造成 owner 误切
            match = re.search(pattern, clause)
            if not match:
                continue

            owner = match.group("owner").strip()
            task = match.group("task").strip()

            # 去掉末尾标点
            task = re.sub(r'[。.．,，；;]+$', '', task)
            if len(task) < 2:
                continue

            # "分头" 可能被误入 owner 时去掉
            owner = owner.replace("分头", "")
            if not owner:
                continue

            # 与参与者名单对齐，增强名字可信度
            if person_names and owner not in person_names:
                # 有参与者信息但不匹配时，仍然保留，避免遗漏；给默认 TBD 标记
                if len(owner) > 2:
                    owner = owner
                else:
                    owner = "TBD"

            # 判断优先级
            priority = "medium"
            text_around = clause[max(0, match.start()-10):match.end()+20].lower()
            if any(kw in text_around for kw in ["紧急", "优先", "重要", "马上", "尽快"]):
                priority = "high"
            elif any(kw in text_around for kw in ["不急", "缓", "以后", "有空"]):
                priority = "low"

            # 判断截止时间
            deadline = ""
            deadline_patterns = [
                r'截止[：:：]?(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
                r'截止[：:：]?(\d{1,2}[-/月]\d{1,2}[日]?)',
                r'deadline[：:：]?(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
                r'最迟(\d{1,2}日)',
                r'下周|下个月|本周|本月|明天|今天|本周内',
            ]
            for dp in deadline_patterns:
                dm = re.search(dp, clause)
                if dm:
                    if dm.lastindex:
                        deadline = dm.group(1)
                    else:
                        deadline = dm.group(0)
                    break

            # 去掉 "X负责" 本身
            task_clean = re.sub(r'^(负责|做|完成|对接|协调|安排|提交|跟进)\s*', '', task)
            if task_clean:
                action_items.append({
                    "task": task_clean if len(task_clean) > 3 else task,
                    "owner": owner if owner not in ["负责", "做", "完成", "对接", "协调", "安排", "提交", "跟进", "TBD", ""] else "TBD",
                    "deadline": deadline,
                    "priority": priority
                })

            found_one = True
            break

        if not found_one:
            continue

    # 决议文本中若有明确人名 + 任务，补充一轮兜底匹配
    for clause in decision_list:
        clause = clause.strip()
        if not clause:
            continue
        for pattern in action_patterns[:8]:
            match = re.search(pattern, clause)
            if match:
                owner = match.group("owner").strip().replace("分头", "")
                task = re.sub(r'[。.．,，；;]+$', '', match.group("task").strip())
                if task and owner and len(task) >= 2:
                    action_items.append({
                        "task": re.sub(r'^(负责|做|完成|对接|协调|安排|提交|跟进)\s*', '', task),
                        "owner": owner,
                        "deadline": "",
                        "priority": "medium"
                    })
                    break

    # 去重：按 (task, owner) 去重
    seen = set()
    deduped = []
    for item in action_items:
        key = (item["task"], item["owner"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    return deduped


def format_action_items(action_items: List[Dict]) -> str:
    if not action_items:
        return "  （暂无明确待办）"
    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    lines = []
    for i, item in enumerate(action_items, 1):
        icon = priority_icon.get(item["priority"], "⚪")
        deadline_str = f" | 截止：{item['deadline']}" if item["deadline"] else ""
        lines.append(f"  {i}. {icon} [{item['priority'].upper()}] {item['task']}")
        lines.append(f"     负责人：{item['owner']}{deadline_str}")
    return "\n".join(lines)


def generate_followup_draft(meeting_topic: str, meeting_date: str,
                             action_items: List[Dict],
                             mode: str,
                             decisions: str = "") -> Dict[str, str]:
    """生成 follow-up 邮件草稿和消息草稿"""
    decisions_list = split_list(decisions, "|") if decisions else []
    summary_text = ""
    if decisions_list:
        summary_text = "；".join(decisions_list)
    elif action_items:
        summary_text = f"共 {len(action_items)} 项待办待落实"
    else:
        summary_text = "详见下文"

    # 邮件草稿
    if mode == "executor":
        action_lines = []
        for item in action_items:
            dl = f"（截止：{item['deadline']}）" if item["deadline"] else ""
            action_lines.append(f"- {item['task']} — {item['owner']} {dl} [优先级：{item['priority']}]")
        action_text = "\n".join(action_lines) if action_lines else "暂无明确待办"
        draft_email = f"""Subject: 【会议纪要】{meeting_topic} — 待办确认 ({meeting_date})

您好，

{meeting_topic} 会议已结束，以下为待办事项，请相关同事确认：

{action_text}

如有变化或疑问，请随时沟通。

谢谢！
"""
    else:  # boss mode
        draft_email = f"""Subject: 【会议汇报】{meeting_topic} — 结论与待办 ({meeting_date})

领导，

{meeting_topic} 已完成，核心结论：{summary_text}。

待办事项共 {len(action_items)} 项，主要负责人已确认，后续进展将定期汇报。

详细纪要见附件或后续整理版本。

谢谢！
"""

    # 消息草稿（简短）
    if mode == "executor":
        item_count = len(action_items)
        owners = ", ".join(dict.fromkeys(item["owner"] for item in action_items if item["owner"] != "TBD"))
        draft_message = f"""【{meeting_topic}】已整理纪要，共 {item_count} 项待办。负责人：{owners if owners else '待定'}。详情见邮件。"""
    else:
        draft_message = f"""【{meeting_topic}】会议已完成，核心结论：{summary_text}。共 {len(action_items)} 项待办推进中。"""

    return {
        "draft_email": draft_email.strip(),
        "draft_message": draft_message.strip()
    }


# ─── 核心处理函数 ─────────────────────────────────────────────────────────────

def build_briefing(meeting_topic: str, meeting_date: str,
                    agenda: str, participants: str) -> Dict[str, Any]:
    """
    生成 boss mode briefing。
    策略：基于议程结构化分析，提取核心结论要点、待决策项、风险和建议行动。
    """
    agenda_items = split_list(agenda, "|") if agenda else []
    participant_list = split_list(participants, "|") if participants else []

    # 从议程项推断可能的核心要点和决策需求
    key_points = []
    decisions_needed = []
    risks = []
    suggested_actions = []

    agenda_keywords_map = {
        "规划": ("制定明确目标和里程碑", "目标是否符合战略方向"),
        "评审": ("评审现有方案或进度", "方案是否通过评审"),
        "对齐": ("团队或部门间目标一致", "各方是否达成一致"),
        "选型": ("技术方案或产品选型决策", "选型标准是否清晰"),
        "资源": ("资源（人力/预算）分配评估", "资源是否满足需求"),
        "进度": ("项目或任务进展回顾", "进度是否正常"),
        "风险": ("风险识别和应对讨论", "风险是否在可控范围"),
        "决策": ("重大决策事项", "决策依据是否充分"),
        "复盘": ("项目或阶段复盘总结", "经验教训是否沉淀"),
        "预算": ("预算审核或调整", "预算分配是否合理"),
    }

    for item in agenda_items:
        item_stripped = item.strip()
        key_point = f"议题：{item_stripped}"
        key_points.append(key_point)

        for kw, (pt, dc) in agenda_keywords_map.items():
            if kw in item_stripped:
                decisions_needed.append(f"「{item_stripped}」相关：{dc}")
                suggested_actions.append(f"准备{item_stripped}的支撑数据和方案建议")
                break
        else:
            decisions_needed.append(f"「{item_stripped}」需要明确方向和结论")

    # 基于参与者推断行动建议
    if participant_list:
        suggested_actions.append(f"确认{participant_list[0]}的主持/主讲角色")

    # 通用风险
    risks.append("议程时间可能不足，部分议题需提前预判优先级")
    risks.append("决策所需数据或授权信息可能不完整")

    # 生成一句话结论
    conclusion = f"本次会议聚焦{meeting_topic}，共{len(agenda_items)}个议题，需形成明确结论并落实行动"
    if agenda_items:
        conclusion = f"围绕「{'」「'.join(agenda_items[:2])}」等议题，需对齐方向并落实{len(agenda_items)}项行动计划"

    # 格式化
    key_points_str = "\n".join(f"  • {kp}" for kp in key_points) if key_points else "  （议程为空）"
    decisions_str = "\n".join(f"  • {d}" for d in decisions_needed[:5]) if decisions_needed else "  （暂无）"
    risks_str = "\n".join(f"  • {r}" for r in risks[:3]) if risks else "  （暂无明显风险）"
    actions_str = "\n".join(f"  • {a}" for a in suggested_actions[:5]) if suggested_actions else "  （暂无）"

    briefing_text = BOSS_BRIEFING_TEMPLATE.format(
        meeting_topic=meeting_topic,
        meeting_date=meeting_date,
        conclusion=conclusion,
        key_points=key_points_str,
        decisions_needed=decisions_str,
        risks=risks_str,
        suggested_actions=actions_str,
        DISCLAIMER=disclaimer_block()
    )

    return {
        "status": "success",
        "task": "briefing",
        "mode": "boss",
        "meeting_topic": meeting_topic,
        "meeting_date": meeting_date,
        "participants": participant_list,
        "agenda_items": agenda_items,
        "sections": {
            "conclusion": conclusion,
            "key_points": key_points,
            "decisions_needed": decisions_needed[:5],
            "risks": risks[:3],
            "suggested_actions": suggested_actions[:5]
        },
        "briefing_text": briefing_text.strip()
    }


def build_minutes(meeting_topic: str, meeting_date: str,
                   raw_text: str, decisions: str,
                   participants: str, mode: str) -> Dict[str, Any]:
    """
    生成结构化会议纪要。
    支持 boss / executor 两种 mode（目前 executor 模式输出更详细的待办提取）。
    """
    # 纯空格 / 空字符串校验（DEF-001 修复）
    if not raw_text or not raw_text.strip():
        return {
            "status": "error",
            "message": "raw_text 不能为空或纯空格",
        }
    discussion_points = parse_raw_text_to_points(raw_text)
    decision_list = split_list(decisions, "|") if decisions else []
    participant_list = split_list(participants, "|") if participants else []

    # 提取待办事项
    action_items = extract_action_items(raw_text, decisions, participants)

    # 格式化讨论要点（boss mode 精简，executor mode 保留更多细节）
    if mode == "boss":
        dp_display = "\n".join(f"  • {p}" for p in discussion_points) if discussion_points else "  （无记录）"
    else:
        dp_display = "\n".join(f"  {i}. {p}" for i, p in enumerate(discussion_points, 1)) if discussion_points else "  （无记录）"

    decisions_display = "\n".join(f"  ✅ {d}" for d in decision_list) if decision_list else "  （暂无明确决议）"
    action_items_display = format_action_items(action_items)

    minutes_text = EXECUTOR_MINUTES_TEMPLATE.format(
        meeting_topic=meeting_topic,
        meeting_date=meeting_date,
        discussion_points=dp_display,
        decisions=decisions_display,
        action_items=action_items_display,
        DISCLAIMER=disclaimer_block()
    )

    return {
        "status": "success",
        "task": "minutes",
        "mode": mode,
        "meeting_topic": meeting_topic,
        "meeting_date": meeting_date,
        "participants": participant_list,
        "minutes": {
            "discussion_points": discussion_points,
            "decisions": decision_list,
            "action_items": action_items
        },
        "minutes_text": minutes_text.strip()
    }


def build_followup(meeting_topic: str, meeting_date: str,
                    decisions: str, action_items: List[Dict],
                    mode: str) -> Dict[str, Any]:
    """
    生成会后 follow-up 草稿（待办追踪 + 邮件草稿 + 消息草稿）。
    """
    decision_list = split_list(decisions, "|") if decisions else []
    followup_items_list = []

    for i, item in enumerate(action_items, 1):
        dl = f"截止：{item['deadline']}" if item.get("deadline") else "截止：待定"
        followup_items_list.append(f"  {i}. [{item['priority'].upper()}] {item['task']} — {item['owner']}（{dl}）")

    followup_items_str = "\n".join(followup_items_list) if followup_items_list else "  （暂无明确待办）"

    drafts = generate_followup_draft(meeting_topic, meeting_date, action_items, mode, decisions)

    if mode == "executor":
        followup_text = EXECUTOR_FOLLOWUP_TEMPLATE.format(
            meeting_topic=meeting_topic,
            meeting_date=meeting_date,
            followup_items=followup_items_str,
            draft_email=drafts["draft_email"],
            draft_message=drafts["draft_message"],
            DISCLAIMER=disclaimer_block()
        )
    else:
        summary = "；".join(decision_list) if decision_list else f"共 {len(action_items)} 项待办待落实"
        followup_text = BOSS_FOLLOWUP_TEMPLATE.format(
            meeting_topic=meeting_topic,
            meeting_date=meeting_date,
            summary=summary,
            followup_items=followup_items_str,
            draft_email=drafts["draft_email"],
            draft_message=drafts["draft_message"],
            DISCLAIMER=disclaimer_block()
        )

    return {
        "status": "success",
        "task": "followup",
        "mode": mode,
        "meeting_topic": meeting_topic,
        "meeting_date": meeting_date,
        "decisions": decision_list,
        "followup_items": action_items,
        "draft_email": drafts["draft_email"],
        "draft_message": drafts["draft_message"],
        "followup_text": followup_text.strip()
    }


def disclaimer_block() -> str:
    """提取免责声明纯文本部分"""
    return "\n".join(line.strip() for line in DISCLAIMER.strip().split("\n") if line.strip())


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def handle(topic: Optional[str], user_input: Optional[str],
           history: Optional[List] = None, args: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Meeting Ops Copilot 主处理函数。
    args 字典支持以下字段：
        task        : "briefing" | "minutes" | "followup"
        meeting_topic : string
        meeting_date  : string (YYYY-MM-DD)
        mode          : "boss" | "executor"
        agenda        : string (| 分隔，briefing 必填)
        raw_text      : string (minutes 必填)
        decisions     : string (| 分隔)
        participants  : string (| 分隔)
        action_items  : list (followup 必填，从 minutes 输出获取)
    """
    if args is None:
        args = {}

    # 兼容旧接口：topic 可能携带 JSON
    if topic and not args:
        try:
            args_candidate = json.loads(topic)
            if isinstance(args_candidate, dict):
                args = args_candidate
                topic = args.get("meeting_topic", "")
        except (json.JSONDecodeError, TypeError):
            # 尝试从 user_input 中解析
            if user_input:
                try:
                    args_candidate = json.loads(user_input)
                    if isinstance(args_candidate, dict):
                        args = args_candidate
                        user_input = ""
                except (json.JSONDecodeError, TypeError):
                    pass

    task = args.get("task", "")
    meeting_topic = args.get("meeting_topic", topic or "")
    meeting_date = args.get("meeting_date", datetime.now().strftime("%Y-%m-%d"))
    mode = args.get("mode", "executor")
    agenda = args.get("agenda", "")
    raw_text = args.get("raw_text", user_input or "")
    decisions = args.get("decisions", "")
    participants = args.get("participants", "")
    action_items = args.get("action_items", [])

    # 参数校验
    if task not in ("briefing", "minutes", "followup"):
        return {
            "status": "error",
            "message": "不支持的任务类型。请指定 task：briefing / minutes / followup",
            "disclaimer": DISCLAIMER
        }

    if not meeting_topic:
        return {
            "status": "error",
            "message": "缺少 meeting_topic（会议主题）",
            "disclaimer": DISCLAIMER
        }

    if task == "briefing" and not agenda:
        return {
            "status": "error",
            "message": "briefing 任务需要提供 agenda（议程，用 | 分隔多条）",
            "disclaimer": DISCLAIMER
        }

    if task == "minutes" and (not raw_text or not raw_text.strip()):
        return {
            "status": "error",
            "message": "minutes 任务需要提供 raw_text（原始讨论文本）",
            "disclaimer": DISCLAIMER
        }

    # 执行
    if task == "briefing":
        return build_briefing(meeting_topic, meeting_date, agenda, participants)
    elif task == "minutes":
        return build_minutes(meeting_topic, meeting_date, raw_text, decisions, participants, mode)
    elif task == "followup":
        if not action_items and not decisions:
            return {
                "status": "error",
                "message": "followup 任务需要提供 action_items（从 minutes 输出获取）或 decisions",
                "disclaimer": DISCLAIMER
            }
        return build_followup(meeting_topic, meeting_date, decisions, action_items, mode)


# ─── 自测分支 ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=" * 60)
    print("🧪 Meeting Ops Copilot — 自测")
    print("=" * 60)

    # ── Test 1: Briefing ─────────────────────────────────────────────
    print("\n📋 Test 1: Briefing（boss mode）")
    result1 = handle(
        topic="Q2 产品规划评审",
        user_input="",
        args={
            "task": "briefing",
            "meeting_topic": "Q2 产品规划评审",
            "meeting_date": "2026-04-05",
            "mode": "boss",
            "agenda": "Q2目标对齐|技术方案选型|资源评估",
            "participants": "产品经理|研发负责人|设计负责人"
        }
    )
    print(f"  status: {result1['status']}")
    print(f"  sections keys: {list(result1.get('sections', {}).keys())}")
    assert result1["status"] == "success", "briefing failed"
    assert "conclusion" in result1["sections"]
    assert "risks" in result1["sections"]
    print("  ✅ PASS")

    # ── Test 2: Minutes ──────────────────────────────────────────────
    print("\n📋 Test 2: Minutes（executor mode）")
    result2 = handle(
        topic="周例会",
        user_input="",
        args={
            "task": "minutes",
            "meeting_topic": "周例会",
            "meeting_date": "2026-03-31",
            "mode": "executor",
            "raw_text": "讨论了A功能延期的风险；决定启用备选方案；张三分头对接供应商；李四负责测试并提交报告；王五协调测试环境",
            "decisions": "启用备选方案",
            "participants": "张三|李四|王五"
        }
    )
    print(f"  status: {result2['status']}")
    assert result2["status"] == "success"
    assert len(result2["minutes"]["action_items"]) >= 3, f"Expected >=3 action items, got {len(result2['minutes']['action_items'])}"
    print(f"  action_items extracted: {len(result2['minutes']['action_items'])}")
    for item in result2["minutes"]["action_items"]:
        print(f"    - {item['task']} | owner={item['owner']} | priority={item['priority']}")
    print("  ✅ PASS")

    # ── Test 3: Follow-up ────────────────────────────────────────────
    print("\n📋 Test 3: Follow-up（executor mode）")
    result3 = handle(
        topic="周例会",
        user_input="",
        args={
            "task": "followup",
            "meeting_topic": "周例会",
            "meeting_date": "2026-03-31",
            "mode": "executor",
            "decisions": "启用备选方案",
            "action_items": result2["minutes"]["action_items"]
        }
    )
    print(f"  status: {result3['status']}")
    assert result3["status"] == "success"
    assert result3["draft_email"]
    assert result3["draft_message"]
    print(f"  draft_email length: {len(result3['draft_email'])}")
    print(f"  draft_message: {result3['draft_message']}")
    print("  ✅ PASS")

    # ── Test 4: Boss Mode Minutes ────────────────────────────────────
    print("\n📋 Test 4: Minutes（boss mode）")
    result4 = handle(
        topic="Q2规划评审",
        user_input="",
        args={
            "task": "minutes",
            "meeting_topic": "Q2规划评审",
            "meeting_date": "2026-04-05",
            "mode": "boss",
            "raw_text": "确认Q2目标为DAU增长30%；技术方案采用微服务架构；需要增编2人",
            "decisions": "Q2目标确认|采用微服务架构",
            "participants": "产品|研发|设计"
        }
    )
    print(f"  status: {result4['status']}")
    assert result4["status"] == "success"
    print("  ✅ PASS")

    # ── Test 5: Validation — missing params ──────────────────────────
    print("\n📋 Test 5: 参数校验（缺少 agenda）")
    result5 = handle(
        topic="测试会议",
        user_input="",
        args={
            "task": "briefing",
            "meeting_topic": "测试会议",
            "meeting_date": "2026-03-31",
            "mode": "boss",
            "agenda": ""  # 空
        }
    )
    assert result5["status"] == "error"
    print("  ✅ PASS（正确拒绝）")

    # ── Test 6: Follow-up from scratch ────────────────────────────────
    print("\n📋 Test 6: Follow-up 仅凭 decisions（无 action_items）")
    result6 = handle(
        topic="测试会议",
        user_input="",
        args={
            "task": "followup",
            "meeting_topic": "测试会议",
            "meeting_date": "2026-03-31",
            "mode": "boss",
            "decisions": "Q2目标确认为DAU+30%",
            "action_items": []
        }
    )
    print(f"  status: {result6['status']}")
    assert result6["status"] == "success"
    print("  ✅ PASS")

    print("\n" + "=" * 60)
    print("✅ 所有自测用例通过！")
    print("=" * 60)
    print("\n使用说明：")
    print("  python3 handler.py")
    print("  或通过 skill 框架调用 handle(topic, user_input, history, args)")
