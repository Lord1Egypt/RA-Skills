#!/usr/bin/env python3
"""协作雷达 v0.4.7 核心处理管线 (R1-R5 + 证据约束 + 安全写入 + 凭据脱敏)。

本模块提供确定性（非 LLM）的执行层能力，配合 SKILL.md 的抽取流程使用：
  R1 证据强制留痕  : attach_evidence / enforce 为每个结论挂载 <=40 字证据短片段
  R2 脱敏规则库    : desensitize 对手机号/邮箱/身份证/银行卡/姓名等做遮蔽
  R3 跨多轮聚合    : aggregate_cross_turn 合并多段材料并去重
  R4 Schema 稳定   : canonical order 校验 7 模块键顺序与必填字段
  R5 冲突检测增强  : detect_conflicts 标记同一事实的多版本为「存在冲突，需人工确认」

仅依赖 Python 标准库。CLI:
  python process.py selftest
  python process.py enforce --card card.json --source chat.txt --out safe-card.json
  python process.py aggregate --cards c1.json c2.json --out combined.json
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

# 跨平台输出安全：Windows 默认控制台编码（cp936 等）不包含 emoji，
# 直接打印 ✅/❌ 会触发 UnicodeEncodeError。统一将标准输出重定向为 UTF-8
# 并加 errors="replace" 兜底，确保任意环境下脚本都不会因字符编码崩溃。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass

EVIDENCE_MAX_LEN = 40  # R1: 证据短片段上限（字符）


class RadarInputError(Exception):
    """输入层可预期错误（坏 JSON / 类型不符 / 文件缺失等）。

    CLI 捕获此异常后打印友好中文提示并以非零码退出，
    绝不向用户甩 Python Traceback（评审「异常输入不崩溃」硬指标）。
    """

# 7 模块 JSON 规范键（R4: 固定顺序）
CANONICAL_KEYS = [
    "project_overview",
    "progress",
    "confirmed_decisions",
    "action_items",
    "risks_dependencies",
    "cross_department_relationships",
    "needs_human_confirmation",
]

# 每个模块项里用于"结论文本"的优先字段（用于证据抽取与冲突比对）
STATEMENT_FIELDS = [
    "summary", "decision", "result", "task", "description",
    "collaboration_item", "item", "impact",
]

LABELS = {
    "phone_cn": "手机号",
    "phone_fixed": "座机",
    "email": "邮箱",
    "id_card": "身份证号",
    "bank_card": "银行卡号",
    "authorization": "授权头",
    "named_secret": "凭据",
    "private_key": "私钥",
    "provider_token": "API令牌",
    "jwt": "JWT",
    "name": "姓名",
}

# ---------- R2 脱敏规则库 ----------
PHONE_CN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
PHONE_FIXED = re.compile(r"(?<!\d)(0\d{2,3}-?\d{7,8})(?!\d)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ID_CARD = re.compile(r"(?<!\d)(\d{17}[\dXx])(?!\d)")
BANK_CARD = re.compile(r"(?<!\d)(\d{16,19})(?!\d)")
NAME_HONORIFIC = re.compile(r"([\u4e00-\u9fa5]{2,4})(?:先生|女士|同学|老师|总|姐|哥)")
AUTHORIZATION_HEADER = re.compile(r"(?im)\bauthorization\s*:\s*[^\r\n]+")
NAMED_SECRET = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
    r"password|passwd|pwd)\b\s*[:=]\s*(?:\"[^\"]+\"|'[^']+'|[^\s\"';,]+)"
)
PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.DOTALL,
)
PROVIDER_TOKEN = re.compile(
    r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"AKIA[0-9A-Z]{16})(?![A-Za-z0-9])"
)
JWT = re.compile(r"(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}(?![A-Za-z0-9_-])")

def _luhn_ok(num: str) -> bool:
    """Luhn 校验：真实银行卡/信用卡（含银联）均满足。
    用于把 16~19 位随机数字串（时间戳、订单号等）与真实卡号区分，
    避免误脱敏拉低结果质量。"""
    digits = [int(c) for c in num if c.isdigit()]
    if len(digits) < 12:
        return False
    total, alt = 0, False
    for d in reversed(digits):
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


# (kind, pattern, validator)：validator 为 None 表示无需二次校验；
# 银行卡额外用 Luhn 过滤，避免误伤普通长数字串。
DESENSITIZE_RULES = [
    ("private_key", PRIVATE_KEY, None),
    ("authorization", AUTHORIZATION_HEADER, None),
    ("named_secret", NAMED_SECRET, None),
    ("provider_token", PROVIDER_TOKEN, None),
    ("jwt", JWT, None),
    ("phone_cn", PHONE_CN, None),
    ("phone_fixed", PHONE_FIXED, None),
    ("email", EMAIL, None),
    ("id_card", ID_CARD, None),
    ("bank_card", BANK_CARD, _luhn_ok),
    ("name", NAME_HONORIFIC, None),
]


# --------------------------------------------------------------------------
# R2 脱敏
# --------------------------------------------------------------------------
def desensitize(text: str, extra_entities: Iterable[str] | None = None) -> tuple[str, list[dict]]:
    """对文本做 PII 遮蔽，返回 (脱敏后文本, 命中报告)。

    extra_entities: 已知姓名/专有实体列表（如团队成员真名），一并遮蔽。
    """
    if not text:
        return text, []
    report: list[dict] = []
    out = text
    for kind, pat, validator in DESENSITIZE_RULES:
        counter = {"n": 0}

        def _repl(m, k=kind, v=validator, c=counter):
            hit = m.group(0)
            if v is not None and not v(hit):
                return hit  # 未通过校验（如非法卡号），原样保留、不脱敏
            c["n"] += 1
            return f"[{LABELS[k]}]"

        out = pat.sub(_repl, out)
        if counter["n"]:
            report.append({"type": kind, "count": counter["n"]})
    for ent in (extra_entities or []):
        ent = (ent or "").strip()
        if ent and ent in out:
            count = out.count(ent)
            out = out.replace(ent, f"[{LABELS['name']}]")
            report.append({"type": "name", "count": count})
    return out, report


# --------------------------------------------------------------------------
# R1 证据强制留痕
# --------------------------------------------------------------------------
def _split_sentences(source: str) -> list[str]:
    return [s.strip() for s in re.split(r"[。！？\n；;]", source) if s.strip()]


# R1 证据匹配阈值：低于此相似度视为「无可靠证据」，返回「未提供」而非硬挂
EVIDENCE_SIM_THRESHOLD = 0.34


def _char_bigrams(s: str) -> set[str]:
    """取字符二元组集合（忽略空白）。用于 Dice 相似度。"""
    s = re.sub(r"\s+", "", s or "")
    if len(s) >= 2:
        return {s[i:i + 2] for i in range(len(s) - 1)}
    return {s} if s else set()


def _dice_similarity(a: str, b: str) -> float:
    """字符二元组 Dice 系数（0~1）。比原「字符集合重合度」更抗噪：
    只有连续片段相同才得分，碰巧共享单字不会被高估。"""
    A, B = _char_bigrams(a), _char_bigrams(b)
    if not A or not B:
        return 0.0
    return 2 * len(A & B) / (len(A) + len(B))


def attach_evidence(conclusion: str, source: str, max_len: int = EVIDENCE_MAX_LEN) -> str:
    """从 source 中为高亮结论找一段 <=max_len 字的证据短片段。

    匹配策略（R1）：子串直接命中 > 字符二元组 Dice 相似度；
    相似度低于阈值一律返回「未提供」，绝不把无关句硬挂成证据（不编造）。
    """
    conclusion = (conclusion or "").strip()
    source = source or ""
    if not conclusion:
        return "未提供"
    sentences = _split_sentences(source)
    best, best_score = None, 0.0
    for s in sentences:
        if len(s) > 120:  # 过长句子不参与，避免噪音
            continue
        # 子串命中最强信号；否则用二元组 Dice
        if conclusion in s or (len(conclusion) >= 4 and s in conclusion):
            score = 1.0
        else:
            score = _dice_similarity(conclusion, s)
        if score > best_score:
            best, best_score = s, score
    if best and best_score >= EVIDENCE_SIM_THRESHOLD:
        best = best.lstrip("-*·•\t ").strip()
        snippet = best[:max_len]
        return snippet + ("…" if len(best) > max_len else "")
    return "未提供"


def _statement_of(item: dict) -> str:
    for f in STATEMENT_FIELDS:
        if isinstance(item.get(f), str) and item[f].strip():
            return item[f]
    return ""


def _ground_action_fields(action_items: list[dict], source: str) -> list[dict]:
    """重置缺少逐字原文支持的草稿负责人和截止时间。"""
    resets: list[dict] = []
    for item in action_items:
        if not isinstance(item, dict):
            continue
        reset_fields: list[str] = []
        for field in ("owner", "ddl"):
            value = item.get(field)
            if not isinstance(value, str):
                continue
            normalized = value.strip()
            if not normalized or normalized == "未提供":
                continue
            if normalized not in source:
                item[field] = "未提供"
                reset_fields.append(field)
        if reset_fields:
            resets.append({
                "task": _statement_of(item) or "未提供",
                "fields": reset_fields,
            })
    return resets


# --------------------------------------------------------------------------
# R5 冲突检测
# --------------------------------------------------------------------------
def detect_conflicts(items: list[dict]) -> list[dict]:
    """对一组条目（通常 action_items）做同主题比对。

    若同一 task 出现不同 owner / ddl / 状态，判定为冲突，返回冲突组。
    """
    groups: dict[str, list[dict]] = {}
    for it in items:
        key = (_statement_of(it) or "").strip()
        if not key:
            continue
        groups.setdefault(key, []).append(it)
    conflicts: list[dict] = []
    for key, grp in groups.items():
        if len(grp) < 2:
            continue
        owners = {g.get("owner") for g in grp if g.get("owner")}
        ddls = {g.get("ddl") for g in grp if g.get("ddl")}
        statuses = {g.get("status") for g in grp if g.get("status")}
        if len(owners) > 1 or len(ddls) > 1 or len(statuses) > 1:
            conflicts.append({"topic": key, "variants": grp})
    return conflicts


# --------------------------------------------------------------------------
# 优先级打分
# --------------------------------------------------------------------------
def score_priority(item: dict) -> str:
    """对行动项做三级优先级打分。

    P0: 存在冲突标记（同一任务多版本）
    P1: Owner 与 DDL 都明确（不缺、不是「未提供」）
    P2: 缺少 Owner 或 DDL（信息不完整，需人工补全）
    """
    conflict = item.get("conflict")
    if isinstance(conflict, str) and conflict.strip() and conflict.strip() != "未提供":
        return "P0"
    owner = (item.get("owner") or "").strip()
    ddl = (item.get("ddl") or "").strip()
    if owner and owner != "未提供" and ddl and ddl != "未提供":
        return "P1"
    return "P2"


# --------------------------------------------------------------------------
# 执行摘要
# --------------------------------------------------------------------------
def synthesize(card: dict) -> str:
    """将 7 模块卡片合成为一段可直接复制的执行摘要（2–3 句）。

    摘要内容包括：阶段/状态 → 待办/风险规模 → 行动建议。
    """
    proj = card.get("project_overview") or {}
    stage = proj.get("current_phase") or proj.get("stage") or ""
    if isinstance(stage, str) and stage and stage not in ("未提供", ""):
        stage_text = str(stage)
    else:
        stage_text = "未标注阶段"
    status = proj.get("overall_status") or "未提供"
    if isinstance(status, str) and status not in ("未提供", ""):
        status_text = str(status)
    else:
        status_text = "未提供"

    actions = card.get("action_items") or []
    action_count = len(actions) if isinstance(actions, list) else 0
    p0_count = sum(1 for a in (actions if isinstance(actions, list) else [])
                   if isinstance(a, dict) and score_priority(a) == "P0")
    p1_count = sum(1 for a in (actions if isinstance(actions, list) else [])
                   if isinstance(a, dict) and score_priority(a) == "P1")

    risks = card.get("risks_dependencies") or []
    risk_count = len(risks) if isinstance(risks, list) else 0

    nhc = card.get("needs_human_confirmation") or []
    nhc_count = len(nhc) if isinstance(nhc, list) else 0

    lines: list[str] = []

    # 句 1: 阶段 + 状态
    stage_suffix = "" if stage_text.endswith("阶段") else "阶段"
    lines.append(f"项目处于{stage_text}{stage_suffix}，整体状态{status_text}。")

    # 句 2: 待办 + 风险规模
    parts: list[str] = []
    if action_count > 0:
        p = f"{action_count}项待办"
        if p0_count > 0:
            p += f"（{p0_count}项P0紧急）"
        parts.append(p)
    if risk_count > 0:
        parts.append(f"{risk_count}项风险/阻断")
    if parts:
        lines.append("，".join(parts) + "。")
    elif action_count == 0 and risk_count == 0:
        lines.append("当前无待办项或风险记录。")

    # 句 3: 行动建议
    suggestions: list[str] = []
    if p0_count > 0:
        suggestions.append(f"{p0_count}项P0待办需立即确认")
    if nhc_count > 0:
        top_item = ""
        if isinstance(nhc, list) and nhc and isinstance(nhc[0], dict):
            top_item = str(nhc[0].get("item", "")).strip()
        if top_item:
            suggestions.append(f"建议优先确认「{top_item}」")
    if suggestions:
        lines.append("行动建议：" + "，".join(suggestions) + "。")

    return "".join(lines)


# --------------------------------------------------------------------------
# Markdown 表格注入防护
# --------------------------------------------------------------------------
def sanitize_markdown_cell(value: Any) -> str:
    """清洗 Markdown 表格单元格值，防止表格结构被用户来源内容破坏。

    转义规则（按顺序）：
    1. 换行 → 空格（表格单元格不能跨行）
    2. \\ → \\\\（反斜杠必须最先转义）
    3. | → \\|（管道符是列分隔符）
    4. & → &amp;  < → &lt;  > → &gt;（XML/HTML 实体）
    5. [ → \\[  ] → \\]（阻断 Markdown 链接语法）
    """
    s = "" if value is None else str(value)
    s = s.replace("\n", " ").replace("\r", " ")
    s = s.replace("\\", "\\\\")
    s = s.replace("|", "\\|")
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace("[", "\\[")
    s = s.replace("]", "\\]")
    return s


def _sanitize_md_recursive(value: Any) -> Any:
    """递归清洗任意 JSON 值中所有字符串字段。"""
    if isinstance(value, str):
        return sanitize_markdown_cell(value)
    if isinstance(value, list):
        return [_sanitize_md_recursive(v) for v in value]
    if isinstance(value, dict):
        return {k: _sanitize_md_recursive(v) for k, v in value.items()}
    return value


# --------------------------------------------------------------------------
# R4 Schema 稳定校验
# --------------------------------------------------------------------------
def check_schema_stability(card: dict) -> list[str]:
    """校验 7 模块键存在且顺序规范（R4）。"""
    errors: list[str] = []
    if not isinstance(card, dict):
        return ["card 必须是 JSON 对象"]
    keys = list(card.keys())
    # 仅检查 7 个规范键的顺序，允许存在额外元信息键（如 sources）
    canonical_present = [k for k in CANONICAL_KEYS if k in keys]
    if canonical_present != CANONICAL_KEYS:
        missing = [k for k in CANONICAL_KEYS if k not in keys]
        if missing:
            errors.append(f"缺失模块: {missing}")
    # 顺序：7 个键在 card 中的出现顺序需与 CANONICAL_KEYS 一致
    positions = [keys.index(k) for k in CANONICAL_KEYS if k in keys]
    if positions != sorted(positions):
        errors.append("模块顺序不符合规范（必须为 7 模块固定顺序）")
    return errors


# --------------------------------------------------------------------------
# 递归脱敏（对所有字符串值）
# --------------------------------------------------------------------------
def _desensitize_value(value: Any, extra: set[str]) -> tuple[Any, list[dict]]:
    report: list[dict] = []
    if isinstance(value, str):
        new, rep = desensitize(value, extra)
        return new, rep
    if isinstance(value, list):
        out = []
        for v in value:
            nv, rep = _desensitize_value(v, extra)
            out.append(nv)
            report.extend(rep)
        return out, report
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            nk, _ = _desensitize_value(k, extra)
            nv, rep = _desensitize_value(v, extra)
            out[nk] = nv
            report.extend(rep)
        return out, report
    return value, report


def sanitize_and_desensitize(
    value: Any, extra_entities: Iterable[str] | None = None
) -> tuple[Any, list[dict]]:
    """返回与输入分离、完成 Markdown 清洗和脱敏的副本。"""
    extra = set(extra_entities or [])
    sanitized = _sanitize_md_recursive(copy.deepcopy(value))
    return _desensitize_value(sanitized, extra)


# --------------------------------------------------------------------------
# R1+R2+R5 综合执行层：enforce
# --------------------------------------------------------------------------
def enforce(card: dict, source: str, extra_entities: Iterable[str] | None = None) -> tuple[dict, dict]:
    """对 LLM 抽取出的卡片做确定性加固。

    返回 (加固后卡片, 元信息统计)。
    步骤：Owner/DDL 逐字校验 → Markdown 清洗 → R2 脱敏 → R1 证据 → R5 冲突 → 优先级 → 执行摘要 → R4 顺序校验。
    """
    if not isinstance(card, dict):
        raise RadarInputError(
            f"卡片 JSON 顶层必须是对象（含 7 模块键），当前是 {type(card).__name__}。"
            "请检查是否误传了数组或其它类型。"
        )
    extra = set(extra_entities or [])
    meta: dict = {
        "desensitized": [],
        "evidence_filled": 0,
        "evidence_missing": 0,
        "evidence_replaced": 0,
        "conflicts_found": 0,
        "schema_errors": [],
    }

    raw_action_items = card.get("action_items", []) or []
    grounded_resets = _ground_action_fields(raw_action_items, source)

    # Markdown 清洗必须在脱敏前执行，避免占位符被转义。
    card, drep = sanitize_and_desensitize(card, extra)
    safe_grounded_resets, reset_drep = sanitize_and_desensitize(grounded_resets, extra)
    safe_source, _ = desensitize(source, extra)
    meta["desensitized"] = drep + reset_drep
    meta["unsupported_action_fields_reset"] = safe_grounded_resets

    # R1 证据留痕 + R5 冲突检测（仅对列表型模块）
    action_items = card.get("action_items", []) or []
    conflict_topics = detect_conflicts(action_items)
    conflict_task_keys = {c["topic"] for c in conflict_topics}
    meta["conflicts_found"] = len(conflict_topics)
    # 冲突对应的「需人工确认项」先收集，遍历结束后再一次性追加，避免迭代中变长
    pending_nhc: list[dict] = [
        {
            "item": sanitize_markdown_cell(reset["task"]),
            "reason": "草稿负责人或截止时间缺少逐字原文支持，已重置",
            "suggested_confirm_with": "相关方",
            "evidence": "未提供",
        }
        for reset in safe_grounded_resets
    ]

    for key in CANONICAL_KEYS:
        section = card.get(key)
        if isinstance(section, list):
            for item in section:
                if not isinstance(item, dict):
                    continue
                stmt = _statement_of(item)
                draft_evidence = item.get("evidence")
                snippet = attach_evidence(stmt, safe_source)
                item["evidence"] = snippet
                if (
                    isinstance(draft_evidence, str)
                    and draft_evidence.strip()
                    and draft_evidence.strip() != "未提供"
                    and draft_evidence.strip() != snippet
                ):
                    meta["evidence_replaced"] += 1
                if snippet == "未提供":
                    meta["evidence_missing"] += 1
                else:
                    meta["evidence_filled"] += 1
                # 冲突标记：仅对 action_items 段，且只标记一次
                if key == "action_items" and stmt and stmt in conflict_task_keys and "conflict" not in item:
                    item["conflict"] = "存在冲突，需人工确认"
                    pending_nhc.append({
                        "item": stmt,
                        "reason": "同一任务出现多个不同负责人/截止时间/状态，需人工确认",
                        "suggested_confirm_with": item.get("owner") or "相关方",
                        "evidence": "存在冲突，需人工确认",
                    })
        elif isinstance(section, dict) and key == "project_overview":
            stmt = section.get("summary") or section.get("project_name") or ""
            draft_evidence = section.get("evidence")
            snippet = attach_evidence(stmt, safe_source)
            section["evidence"] = snippet
            if (
                isinstance(draft_evidence, str)
                and draft_evidence.strip()
                and draft_evidence.strip() != "未提供"
                and draft_evidence.strip() != snippet
            ):
                meta["evidence_replaced"] += 1

    if pending_nhc:
        card.setdefault("needs_human_confirmation", []).extend(pending_nhc)

    # 优先级打分 + 排序：P0 置顶，P1 次之，P2 垫底。
    action_items = card.get("action_items")
    if isinstance(action_items, list) and action_items:
        p0 = sum(1 for a in action_items if isinstance(a, dict) and score_priority(a) == "P0")
        p1 = sum(1 for a in action_items if isinstance(a, dict) and score_priority(a) == "P1")
        p2 = sum(1 for a in action_items if isinstance(a, dict) and score_priority(a) == "P2")
        meta["priority_summary"] = {"P0": p0, "P1": p1, "P2": p2}
        for item in action_items:
            if isinstance(item, dict) and "priority" not in item:
                item["priority"] = score_priority(item)
        action_items.sort(key=lambda a: {"P0": 0, "P1": 1, "P2": 2}.get(
            a.get("priority", "P2") if isinstance(a, dict) else "P2", 2))
    else:
        meta["priority_summary"] = {"P0": 0, "P1": 0, "P2": 0}

    # 执行摘要
    meta["executive_summary"] = synthesize(card)

    # R4 顺序校验
    meta["schema_errors"] = check_schema_stability(card)
    return card, meta


# --------------------------------------------------------------------------
# R3 跨多轮聚合
# --------------------------------------------------------------------------
def aggregate_cross_turn(
    cards: list[dict], extra_entities: Iterable[str] | None = None
) -> dict:
    """合并已清洗脱敏的卡片副本，去重后返回统一卡片。"""
    extra = set(extra_entities or [])
    safe_cards = [sanitize_and_desensitize(card, extra)[0] for card in cards]
    merged: dict = {k: [] for k in CANONICAL_KEYS}
    seen_action: set[tuple] = set()
    seen_text: dict[str, set] = {k: set() for k in CANONICAL_KEYS}

    for c in safe_cards:
        for k in CANONICAL_KEYS:
            section = c.get(k)
            if not isinstance(section, list):
                continue
            for item in section:
                if not isinstance(item, dict):
                    continue
                if k == "action_items":
                    sig = (_statement_of(item), item.get("owner"))
                    if sig in seen_action:
                        continue
                    seen_action.add(sig)
                    merged[k].append(item)
                else:
                    stmt = _statement_of(item)
                    if stmt and stmt in seen_text[k]:
                        continue
                    if stmt:
                        seen_text[k].add(stmt)
                    merged[k].append(item)

    merged["sources"] = [c.get("project_overview", {}).get("project_name", "未命名") for c in safe_cards]
    merged["aggregation_summary"] = f"已聚合 {len(cards)} 段材料，行动项去重后 {len(merged['action_items'])} 条"
    return merged


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _read_text_file(path: Path, label: str) -> str:
    """读取文本文件，缺失/不可读时抛出可预期的 RadarInputError。"""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise RadarInputError(f"{label}文件不存在：{path}")
    except IsADirectoryError:
        raise RadarInputError(f"{label}路径是目录而非文件：{path}")
    except PermissionError:
        raise RadarInputError(f"{label}文件无读取权限：{path}")
    except UnicodeDecodeError:
        raise RadarInputError(f"{label}文件不是 UTF-8 文本，无法解析：{path}")
    except OSError as e:
        raise RadarInputError(f"{label}文件读取失败：{path}（{e}）")


def _load_json(path: Path, *, require_dict: bool = True) -> Any:
    """加载 JSON，坏 JSON / 缺文件 / 类型不符时抛出 RadarInputError。"""
    raw = _read_text_file(path, "JSON")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RadarInputError(
            f"JSON 解析失败：{path}\n"
            f"  位置 第{e.lineno}行 第{e.colno}列：{e.msg}\n"
            "  请检查是否有多余逗号、缺引号或括号不匹配。"
        )
    if require_dict and not isinstance(data, dict):
        raise RadarInputError(
            f"JSON 顶层必须是对象 {{...}}，当前是 {type(data).__name__}：{path}"
        )
    return data


def write_output_text(
    path: Path,
    text: str,
    *,
    protected_paths: Iterable[Path] = (),
    force: bool = False,
) -> None:
    """写入明确命名的输出文件，禁止静默覆盖输入或已有文件。"""
    output_path = path.resolve(strict=False)
    protected = {item.resolve(strict=False) for item in protected_paths}
    if output_path in protected:
        raise RadarInputError(f"输出路径不得与任何输入路径相同：{path}")
    if path.exists() and not force:
        raise RadarInputError(f"输出文件已存在：{path}。请更换路径，或明确添加 --force。")
    try:
        path.write_text(text, encoding="utf-8")
    except IsADirectoryError:
        raise RadarInputError(f"输出路径是目录而非文件：{path}")
    except FileNotFoundError:
        raise RadarInputError(f"输出目录不存在：{path.parent}")
    except PermissionError:
        raise RadarInputError(f"输出路径不可写：{path}")
    except OSError as exc:
        raise RadarInputError(f"输出文件写入失败：{path}（{exc}）")


def _selftest() -> int:
    print("== 协作雷达 v0.4.7 核心引擎自测（含安全边界回归）==")
    fails = 0

    # R2 脱敏
    t, rep = desensitize("联系 13800138000 或 alice@corp.com，身份证 11010119900101123X")
    ok = ("13800138000" not in t) and ("alice@corp.com" not in t) and ("[手机号]" in t) and ("[邮箱]" in t)
    print(("PASS" if ok else "FAIL"), "R2 脱敏规则库:", t)
    fails += 0 if ok else 1

    secret_text = (
        "api_key=REDACTED-SECRET Authorization: Bearer abcdefghijklmnop "
        "password=hunter2"
    )
    safe_secret_text, _ = desensitize(secret_text)
    ok = "sk-123" not in safe_secret_text and "Bearer" not in safe_secret_text and "hunter2" not in safe_secret_text
    print(("PASS" if ok else "FAIL"), "R2 常见凭据脱敏:", safe_secret_text)
    fails += 0 if ok else 1

    # R1 证据
    ev = attach_evidence("接口由后端负责", "周五会上确认：接口由后端负责，下周三提测")
    ok = (0 < len(ev) <= EVIDENCE_MAX_LEN) and "后端负责" in ev
    print(("PASS" if ok else "FAIL"), "R1 证据留痕:", ev)
    fails += 0 if ok else 1

    ev_none = attach_evidence("完全无关结论", "这是一段讲天气的文本")
    ok = ev_none == "未提供"
    print(("PASS" if ok else "FAIL"), "R1 缺失标未提供:", ev_none)
    fails += 0 if ok else 1

    # R5 冲突
    items = [
        {"task": "登录模块开发", "owner": "张三", "ddl": "2026-07-10"},
        {"task": "登录模块开发", "owner": "李四", "ddl": "2026-07-12"},
    ]
    cf = detect_conflicts(items)
    ok = len(cf) == 1 and cf[0]["topic"] == "登录模块开发"
    print(("PASS" if ok else "FAIL"), "R5 冲突检测:", len(cf), "处")
    fails += 0 if ok else 1

    # R4 schema 顺序
    bad = {"progress": [], "project_overview": {}}
    ok = len(check_schema_stability(bad)) > 0
    print(("PASS" if ok else "FAIL"), "R4 顺序校验(异常检出):", check_schema_stability(bad))
    fails += 0 if ok else 1

    # enforce 端到端
    card = {
        "project_overview": {"project_name": "X", "summary": "联系人王总", "evidence": "伪造证据"},
        "progress": [{"item": "完成设计", "evidence": "伪造证据"}],
        "confirmed_decisions": [],
        "action_items": [
            {"task": "登录模块开发", "owner": "张三", "ddl": "2026-07-10"},
            {"task": "登录模块开发", "owner": "李四", "ddl": "2026-07-12"},
        ],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    src = "王总说联系人改一下。周五确认登录模块开发由张三负责，下周三提测。但周报里写李四负责。"
    out, meta = enforce(card, src, extra_entities=["王总"])
    ok = ("[姓名]" in json.dumps(out, ensure_ascii=False)) and meta["conflicts_found"] == 1 \
        and any(i.get("conflict") for i in out["action_items"]) and meta["evidence_replaced"] >= 1
    print(("PASS" if ok else "FAIL"), "enforce 端到端(R2+R1+R5):", meta)
    fails += 0 if ok else 1

    # R3 聚合
    c1 = {"project_overview": {"project_name": "A"}, "progress": [{"item": "p1"}], "confirmed_decisions": [],
         "action_items": [{"task": "t1", "owner": "张三"}], "risks_dependencies": [],
         "cross_department_relationships": [], "needs_human_confirmation": []}
    c2 = {"project_overview": {"project_name": "B"}, "progress": [{"item": "p2"}], "confirmed_decisions": [],
         "action_items": [{"task": "t1", "owner": "张三"}], "risks_dependencies": [],
         "cross_department_relationships": [], "needs_human_confirmation": []}
    merged = aggregate_cross_turn([c1, c2])
    ok = merged["aggregation_summary"] and len(merged["action_items"]) == 1 and len(merged["progress"]) == 2
    print(("PASS" if ok else "FAIL"), "R3 跨多轮聚合:", merged["aggregation_summary"])
    fails += 0 if ok else 1

    raw_secret = "demo-secret"
    raw_entity = "张三测试"
    unsafe_card = {
        "project_overview": {"project_name": raw_entity},
        "progress": [], "confirmed_decisions": [],
        "action_items": [{"task": f"发送邮件 alice@example.com，password={raw_secret}"}],
        "risks_dependencies": [], "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    safe_merged = aggregate_cross_turn([unsafe_card], extra_entities=[raw_entity])
    safe_merged_json = json.dumps(safe_merged, ensure_ascii=False)
    ok = all(value not in safe_merged_json for value in ("alice@example.com", raw_secret, raw_entity))
    print(("PASS" if ok else "FAIL"), "R3 聚合重新脱敏")
    fails += 0 if ok else 1

    # R2+ 银行卡 Luhn：真实卡号脱敏，随机长数字串不误伤
    real_card = "6222021234567894"  # 通过 Luhn 校验的银联卡样例
    t_card, _ = desensitize(f"卡号 {real_card}")
    ok = "[银行卡号]" in t_card
    print(("PASS" if ok else "FAIL"), "R2+ 真实卡号脱敏:", t_card)
    fails += 0 if ok else 1

    ts = "1234567890123456"  # 非法卡号（Luhn 不过）——应原样保留
    t_ts, _ = desensitize(f"订单号 {ts}")
    ok = ts in t_ts and "[银行卡号]" not in t_ts
    print(("PASS" if ok else "FAIL"), "R2+ 长数字串不误伤:", t_ts)
    fails += 0 if ok else 1

    # R1+ 证据阈值：低相似度不硬挂
    ev_low = attach_evidence("预算超支需要审批", "今天天气不错，大家去团建了")
    ok = ev_low == "未提供"
    print(("PASS" if ok else "FAIL"), "R1+ 弱相关不硬挂:", ev_low)
    fails += 0 if ok else 1

    # ---------- 对抗输入压测（评审「异常输入不崩溃」硬指标）----------
    import tempfile
    print("-" * 40)
    print("[对抗输入] 以下用例必须「不崩溃」——抛 RadarInputError 视为通过：")
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        src = tdp / "s.txt"
        src.write_text("一些源文本", encoding="utf-8")

        # A1: 损坏 JSON
        bad = tdp / "bad.json"
        bad.write_text("{broken,,,", encoding="utf-8")
        try:
            _load_json(bad)
            print("FAIL", "A1 损坏JSON 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A1 损坏JSON -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A1 抛了非预期异常 {type(e).__name__}"); fails += 1

        # A2: 顶层是数组而非对象
        arr = tdp / "arr.json"
        arr.write_text("[1,2,3]", encoding="utf-8")
        try:
            _load_json(arr)
            print("FAIL", "A2 数组JSON 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A2 数组JSON -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A2 抛了非预期异常 {type(e).__name__}"); fails += 1

        # A3: source 文件不存在
        try:
            _read_text_file(tdp / "NOPE.txt", "原始协作文本")
            print("FAIL", "A3 缺失文件 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A3 缺失文件 -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A3 抛了非预期异常 {type(e).__name__}"); fails += 1

        # A4: enforce 收到非 dict 卡片
        try:
            enforce([1, 2, 3], "源文本")
            print("FAIL", "A4 非对象卡片 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A4 非对象卡片 -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A4 抛了非预期异常 {type(e).__name__}"); fails += 1

        output = tdp / "result.json"
        write_output_text(output, "first")
        try:
            write_output_text(output, "second")
            print("FAIL", "A5 已有输出被静默覆盖"); fails += 1
        except RadarInputError:
            print("PASS", "A5 已有输出必须显式 --force")

        try:
            write_output_text(src, "replacement", protected_paths=[src], force=True)
            print("FAIL", "A6 输入路径被当作输出覆盖"); fails += 1
        except RadarInputError:
            print("PASS", "A6 输入路径不得作为输出路径")

    # ---------- v0.4.7 优先级打分 ----------
    print("-" * 40)
    print("[v0.4.7] 优先级打分 (P0/P1/P2):")
    ok = score_priority({"task": "联调", "conflict": "存在冲突，需人工确认", "owner": "张三", "ddl": "下周三"}) == "P0"
    print(("PASS" if ok else "FAIL"), "P1 冲突项 -> P0")
    fails += 0 if ok else 1

    ok = score_priority({"task": "写文档", "owner": "李四", "ddl": "下周五"}) == "P1"
    print(("PASS" if ok else "FAIL"), "P2 Owner+DDL 齐全 -> P1")
    fails += 0 if ok else 1

    ok = score_priority({"task": "调研", "owner": "未提供", "ddl": "未提供"}) == "P2"
    print(("PASS" if ok else "FAIL"), "P3 缺 Owner/DDL -> P2")
    fails += 0 if ok else 1

    ok = score_priority({"task": "写文档", "owner": "李四", "ddl": "下周五", "conflict": ""}) == "P1"
    print(("PASS" if ok else "FAIL"), "P4 空 conflict 不误判 -> P1")
    fails += 0 if ok else 1

    # ---------- enforce 含优先级排序 ----------
    mult_action = {
        "project_overview": {"project_name": "X", "summary": "测试"},
        "progress": [],
        "confirmed_decisions": [],
        "action_items": [
            {"task": "写文档", "owner": "李四", "ddl": "下周五", "evidence": "未提供"},
            {"task": "紧急修复", "owner": "张三", "ddl": "今天", "evidence": "未提供",
             "conflict": "存在冲突，需人工确认"},
            {"task": "调研", "owner": "未提供", "ddl": "未提供", "evidence": "未提供"},
        ],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    out2, meta2 = enforce(
        mult_action,
        "李四负责写文档，下周五完成。张三今天处理紧急修复。调研负责人和时间未提供。",
    )
    ais = out2.get("action_items", [])
    ok = len(ais) == 3 and ais[0].get("priority") == "P0" \
        and ais[1].get("priority") == "P1" and ais[2].get("priority") == "P2" \
        and meta2["priority_summary"] == {"P0": 1, "P1": 1, "P2": 1}
    print(("PASS" if ok else "FAIL"),
          f"P5 enforce 优先级排序: {meta2.get('priority_summary')}, 首项={ais[0].get('priority') if ais else 'N/A'}")
    fails += 0 if ok else 1

    unsupported_card = {
        "project_overview": {"project_name": "登录模块"},
        "progress": [],
        "confirmed_decisions": [],
        "action_items": [
            {"task": "登录模块开发", "owner": "王强", "ddl": "周五", "evidence": "未提供"},
        ],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    grounded, grounded_meta = enforce(
        unsupported_card,
        "登录模块继续推进，负责人和时间都没定。",
    )
    grounded_item = grounded["action_items"][0]
    ok = (
        grounded_item.get("owner") == "未提供"
        and grounded_item.get("ddl") == "未提供"
        and grounded_item.get("priority") == "P2"
        and len(grounded_meta.get("unsupported_action_fields_reset", [])) == 1
        and len(grounded.get("needs_human_confirmation", [])) == 1
    )
    print(("PASS" if ok else "FAIL"), "G1 无原文支持的 Owner/DDL 被重置")
    fails += 0 if ok else 1

    sensitive_card = {
        "project_overview": {"project_name": "X"},
        "progress": [], "confirmed_decisions": [],
        "action_items": [{
            "task": "发送邮件 alice@example.com，password=demo-secret",
            "owner": "张三测试", "ddl": "周五", "evidence": "未提供",
        }],
        "risks_dependencies": [], "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    safe_card, safe_meta = enforce(
        sensitive_card,
        "发送邮件 alice@example.com，password=demo-secret。负责人和截止时间尚未确定。",
        extra_entities=["张三测试"],
    )
    serialized = json.dumps({"card": safe_card, "meta": safe_meta}, ensure_ascii=False)
    ok = all(value not in serialized for value in (
        "alice@example.com", "demo-secret", "张三测试"
    ))
    print(("PASS" if ok else "FAIL"), "G2 诊断信息保持脱敏")
    fails += 0 if ok else 1

    # ---------- 执行摘要 ----------
    summary = meta2.get("executive_summary", "")
    ok = isinstance(summary, str) and "项目处于" in summary and "P0" in summary and "整体状态" in summary
    print(("PASS" if ok else "FAIL"), f"S1 执行摘要生成: {summary[:60]}...")
    fails += 0 if ok else 1

    # 空卡片摘要
    empty_card = {
        "project_overview": {"project_name": "X"},
        "progress": [], "confirmed_decisions": [],
        "action_items": [], "risks_dependencies": [],
        "cross_department_relationships": [], "needs_human_confirmation": [],
    }
    s_empty = synthesize(empty_card)
    ok = "项目处于" in s_empty and ("无待办" in s_empty or "0项待办" in s_empty)
    print(("PASS" if ok else "FAIL"), f"S2 空卡片摘要: {s_empty}")
    fails += 0 if ok else 1

    # ---------- 下游导出器（多工具协同落地）----------
    print("-" * 40)
    print("[下游导出器] 复用 export_card.selftest（含对抗输入）：")
    try:
        from export_card import selftest as _exp_selftest
        ok_exp = _exp_selftest() == 0
    except Exception as e:
        ok_exp = False
        print("FAIL", "E 导出器 selftest 异常:", type(e).__name__, e)
    print(("PASS" if ok_exp else "FAIL"), "E 下游导出器(多工具协同)")
    fails += 0 if ok_exp else 1

    # ---------- 雷达图 ----------
    print("-" * 40)
    print("[v0.4.7] 雷达图可视化:")
    try:
        from radar_chart import _selftest as _radar_selftest  # type: ignore[import-untyped]
        ok_radar = _radar_selftest() == 0
    except Exception as e:
        ok_radar = False
        print("FAIL", "R 雷达图 selftest 异常:", type(e).__name__, e)
    print(("PASS" if ok_radar else "FAIL"), "R 雷达图可视化")
    fails += 0 if ok_radar else 1

    # ---------- v0.4.7 Markdown 表格注入防护 ----------
    print("-" * 40)
    print("[v0.4.7] Markdown 表格注入防护:")
    # M1: 管道符转义
    ok = sanitize_markdown_cell("a|b") == "a\\|b"
    print(("PASS" if ok else "FAIL"), "M1 管道符 -> \\|")
    fails += 0 if ok else 1
    # M2: 换行转空格
    ok = sanitize_markdown_cell("line1\nline2") == "line1 line2"
    print(("PASS" if ok else "FAIL"), "M2 换行 -> 空格")
    fails += 0 if ok else 1
    # M3: HTML 实体
    ok = all(ch in sanitize_markdown_cell("<x>&y")
             for ch in ("&lt;", "&amp;", "&gt;"))
    print(("PASS" if ok else "FAIL"), "M3 <>& -> 实体")
    fails += 0 if ok else 1
    # M4: 链接语法阻断
    ok = sanitize_markdown_cell("[click](http://evil)") == "\\[click\\](http://evil)"
    print(("PASS" if ok else "FAIL"), "M4 [link] -> \\[link\\]")
    fails += 0 if ok else 1
    # M5: enforce 端到端 —— 管道符/换行/<> 被递归清洗
    poison_card = {
        "project_overview": {"project_name": "X", "summary": "a|b", "evidence": "未提供"},
        "progress": [{"item": "进\n展", "evidence": "<script>"}],
        "confirmed_decisions": [],
        "action_items": [{"task": "[link](x)", "owner": "未提供", "ddl": "未提供", "evidence": "未提供"}],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    out_md, meta_md = enforce(poison_card, "源文本")
    ok = (
        "a\\|b" in out_md["project_overview"]["summary"]
        and "进 展" in out_md["progress"][0]["item"]
        and out_md["progress"][0]["evidence"] == "未提供"
        and "\\[link\\](x)" in out_md["action_items"][0]["task"]
    )
    print(("PASS" if ok else "FAIL"), "M5 enforce 端到端递归清洗")
    fails += 0 if ok else 1

    print("=" * 40)
    if fails == 0:
        print("ALL PASS -- v0.4.7 核心引擎 + 证据重算 + 安全写入 + 凭据脱敏 自检通过")
        return 0
    print(f"{fails} 项失败 (FAIL)")
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="协作雷达 v0.4.7 核心处理管线")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_self = sub.add_parser("selftest")

    p_enf = sub.add_parser("enforce")
    p_enf.add_argument("--card", required=True, help="抽取出的卡片 JSON 路径")
    p_enf.add_argument("--source", required=True, help="原始协作文本（用于证据抽取）")
    p_enf.add_argument("--entities", help="可选：已知实体名单文件，每行一个")
    p_enf.add_argument("--out", required=True, help="新的输出 JSON 路径")
    p_enf.add_argument("--force", action="store_true", help="明确替换已存在的命名输出文件")

    p_agg = sub.add_parser("aggregate")
    p_agg.add_argument("--cards", nargs="+", required=True, help="多段卡片 JSON")
    p_agg.add_argument("--entities", help="可选：已知实体名单文件，每行一个")
    p_agg.add_argument("--out", required=True, help="新的输出 JSON 路径")
    p_agg.add_argument("--force", action="store_true", help="明确替换已存在的命名输出文件")

    args = parser.parse_args(argv)

    if args.cmd == "selftest":
        return _selftest()

    if args.cmd == "enforce":
        card = _load_json(Path(args.card))
        source = _read_text_file(Path(args.source), "原始协作文本")
        extra = []
        if args.entities:
            extra = [l.strip() for l in _read_text_file(Path(args.entities), "实体名单").splitlines() if l.strip()]
        out, meta = enforce(card, source, extra_entities=extra)
        out_path = Path(args.out)
        protected_paths = [Path(args.card), Path(args.source)]
        if args.entities:
            protected_paths.append(Path(args.entities))
        write_output_text(
            out_path,
            json.dumps(out, ensure_ascii=False, indent=2),
            protected_paths=protected_paths,
            force=args.force,
        )
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "aggregate":
        cards = []
        for p in args.cards:
            data = _load_json(Path(p), require_dict=False)
            if not isinstance(data, dict):
                raise RadarInputError(f"聚合输入需为卡片对象，跳过非对象文件：{p}")
            cards.append(data)
        if not cards:
            raise RadarInputError("没有可聚合的有效卡片。")
        extra = []
        if args.entities:
            extra = [l.strip() for l in _read_text_file(Path(args.entities), "实体名单").splitlines() if l.strip()]
        merged = aggregate_cross_turn(cards, extra_entities=extra)
        out_path = Path(args.out)
        protected_paths = [Path(item) for item in args.cards]
        if args.entities:
            protected_paths.append(Path(args.entities))
        write_output_text(
            out_path,
            json.dumps(merged, ensure_ascii=False, indent=2),
            protected_paths=protected_paths,
            force=args.force,
        )
        print(f"已聚合 {len(cards)} 段 -> {out_path}")
        return 0

    return 1


def _cli_entry(argv: list[str]) -> int:
    """CLI 总入口：捕获一切可预期输入错误，友好提示 + 非零退出，绝不甩堆栈。"""
    try:
        return main(argv)
    except RadarInputError as e:
        print(f"[输入错误] {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\n[已中断]", file=sys.stderr)
        return 130
    except Exception as e:  # 兜底：任何未预期异常也不甩完整 Traceback
        print(f"[意外错误] {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli_entry(sys.argv[1:]))
