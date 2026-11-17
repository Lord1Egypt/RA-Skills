#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conversation.py — office-token-booster 对话编排层（方向 B）

把三个既有外壳（qa 追问 / report_engine 报告 / ledger_agent 写回）串成
单一对话流：用户说一句，本层理解意图、调用对应的内核能力，必要时建议记账。

设计原则（与三层解耦一致）：
- 只消费既有模块，**绝不改 qa / report_engine / ledger_agent 一行**。本层完全是新增的
  "粘合层"，复用它们暴露的纯函数（answer_followup / generate_* / propose_* / run_long_chain）。
- 纯标准库、无第三方依赖、无网络、无硬编码密钥。
- 状态用普通 dict 传递（state["pending"] 保存待确认条目），便于上层 Skill / 对话 UI 集成。
- 安全默认：记账必须显式「确认」才写回账本（ledger_agent 内部仍是默认 dry-run + 备份）。
- 类型字典 type_registry.json 消除自然语言里任务类型的歧义（如『周报』→『周报生成』），
  让记账类型始终落到标准名，不再依赖脆弱的子串猜测。

用法：
  python conversation.py <ledger.json>          # 进入交互式对话
  或在 Python 中：
  from conversation import handle
  state = {}
  print(handle("ledger.json", "记一笔 周报生成 花了1800 token 5分钟", state))
  print(handle("ledger.json", "确认", state))
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# 允许从任意目录运行（与 qa / report_engine / ledger_agent 保持一致的 sibling import）。
sys.path.insert(0, str(Path(__file__).resolve().parent))

from diagnose import load_ledger, diagnose, format_number          # noqa: E402
from qa import answer_followup                                      # noqa: E402
from ledger_agent import (                                         # noqa: E402
    propose_entry, propose_automation_targets, run_long_chain)
from report_engine import (                                        # noqa: E402
    generate_markdown_summary, generate_markdown_report)
from type_registry import load_registry                            # noqa: E402  # 类型字典单一事实源（与 executor 共用）
from executor import (  # noqa: E402  # execute 意图路由复用执行引擎
    resolve_exec_type as _resolve_exec_type,
    EXECUTORS as _EXECUTORS,
    execute_render as _exec_render,
)


# ─────────────────────────────────────────────────────────────
# 类型字典：标准类型名 ↔ 别名/关键词
# ─────────────────────────────────────────────────────────────

def _load_registry():
    """读取类型字典；文件缺失/损坏时降级为空字典（退化为无字典的行为）。

    实际读取委托给 `type_registry.load_registry`——字典的加载与容错规则只留一处，
    对话层（本模块 `_detect_type`）与执行层（`executor.resolve_exec_type`）共用同一事实源。
    """
    return load_registry()


# 模块加载时读取一次类型字典（供 _detect_type 全局复用）
_REGISTRY = _load_registry()


# ─────────────────────────────────────────────────────────────
# 自然语言解析
# ─────────────────────────────────────────────────────────────

# 中文数量单位 → 乘数（万/千/k 常见）。
_UNIT_MULT = {"万": 10 ** 4, "千": 10 ** 3, "k": 10 ** 3, "w": 10 ** 4}

# ── S6：热路径正则预编译（classify/parse 高频调用，避免每次重新拼接+编译）──
# 数字前缀（与单位/关键词解耦）：抽取「数字+可选单位」。
_NUM_PREFIX_RE = re.compile(r"(\d[\d,]*\.?\d*)\s*(万|千|k|w)?")
# 关键词正则：数字须紧邻其后的关键词才命中（保留原语义，杜绝遥远处误命中）。
_TOKEN_KW_RE = re.compile(r"\s*(?:个\s*)?(?:token|tokens|Token|TOKEN)", re.I)
_MIN_KW_RE = re.compile(r"\s*(?:分钟|分|min|mins)", re.I)
# 类型抽取（短语抓取）：预编译单行正则，消除 classify 每次重建。
_TYPE_EXTRACT_RE = re.compile(
    r"(?:记一笔|记录|记账|记一下|记上|登记|添加任务|新增任务|记下来|写进账本|"
    r"生成了|做了|完成了|写好?了|做好?了|产出|整理|搞完?了)\s*"
    r"([一-龥A-Za-z0-9]{1,12}?)"
    r"(?=\s*(?:花了|用了|耗时|花费|消耗|占|，|,|。|\.|$))"
)


def _parse_number(text, keyword_re):
    """从 text 抽取一个带可选单位（万/千/k）的数字，返回 int。

    keyword_re 必须是预编译的关键词正则（_TOKEN_KW_RE / _MIN_KW_RE），
    要求数字后紧邻该关键词（保留原语义，避免关键词遥远处误命中）。
    抽不到/解析失败返回 None，绝不抛异常（修复 H1）。

    _NUM_PREFIX_RE 在模块级预编译，仅在调用处做关键词邻接校验，
    消除每次解析都重新拼接+编译正则的开销（S6）。
    """
    for m in _NUM_PREFIX_RE.finditer(text or ""):
        rest = text[m.end():]
        if keyword_re.match(rest):
            raw = m.group(1).replace(",", "")
            if raw in ("", "."):
                continue
            try:
                val = float(raw)
            except ValueError:
                continue
            unit = (m.group(2) or "").lower()
            return int(val * _UNIT_MULT.get(unit, 1))
    return None


def _parse_numbers(text):
    """从自然语句里抽 token / 分钟数，抽不到返回 None（不崩溃）。"""
    tokens = _parse_number(text, _TOKEN_KW_RE)
    minutes = _parse_number(text, _MIN_KW_RE)
    return tokens, minutes


_BASE_HEAD_RE = re.compile(r"(基准|手搓|baseline|笨办法)", re.I)


def _parse_skill_and_baseline(text):
    """把确认话按首个 baseline 触发词切成两段，各自独立解析 token/分钟。

    触发词（基准/手搓/baseline/笨办法）之前的片段当作 skill 成本，
    之后的片段当作 baseline 成本。两段互不吞，解决「同时给 skill+baseline
    时 skill 被静默丢弃」的数据丢失问题（对抗式审查 C1）。

    返回 (skill_tokens, skill_minutes, baseline_tokens, baseline_minutes)，
    未解析到的维度为 None。
    """
    head = _BASE_HEAD_RE.search(text or "")
    skill_seg = text[:head.start()] if head else (text or "")
    base_seg = text[head.end():] if head else ""
    st = _parse_number(skill_seg, _TOKEN_KW_RE)
    sm = _parse_number(skill_seg, _MIN_KW_RE)
    bt = _parse_number(base_seg, _TOKEN_KW_RE)
    bm = _parse_number(base_seg, _MIN_KW_RE)
    return st, sm, bt, bm


def _detect_type(text, diag):
    """判断任务类型，返回 (type, is_new) 元组。

    匹配优先级：
      1. 账本里已记录的标准类型名精确出现 → 直接用
      2. 类型字典：标准名或别名/关键词出现在话里 → 映射到标准名
      3. 短语抓取（『生成了/做了…<词>』）→ 依次用账本类型、字典做模糊匹配
      4. 都无命中但抓到短语 → 作为「全新类型候选」返回，is_new=True（预览时让用户确认）

    is_new=True 表示账本与字典都没有这个类型，确认后会作为新类型写回，
    并提示用户在 type_registry.json 补别名以便以后识别。
    """
    known = [d["task_type"] for d in diag.by_type if d["task_type"]]

    # 1. 账本已知类型精确出现（按长度降序，优先返回最具体的标准名，
    #    修复 M1：避免『周报生成』被更短的『周报』先命中）
    for k in sorted(known, key=len, reverse=True):
        if k in text:
            return k, False

    # 2. 类型字典：标准名 + 别名/关键词
    for std, aliases in _REGISTRY.items():
        if std in text:
            return std, False
        for alias in (aliases or []):
            if alias and alias in text:
                return std, False

    # 3. 短语抓取：显式记账词（『记一笔 X』）或被动完成信号（『生成了周报』『做了个PPT』）
    #    用前瞻断言在成本词/标点前截断类型名，避免『记一笔』被拆成『笔』。
    #    正则已提到模块级 _TYPE_EXTRACT_RE（S6，不再每次重建）。
    m = _TYPE_EXTRACT_RE.search(text)
    cand = m.group(1).strip() if m else None
    if cand:
        # 3a. 账本已知类型模糊（如 cand='周报' 命中 '周报生成'）
        for k in known:
            if cand in k or k in cand:
                return k, False
        # 3b. 字典标准名/别名模糊
        for std, aliases in _REGISTRY.items():
            if cand in std or std in cand:
                return std, False
            for alias in (aliases or []):
                if alias and (cand in alias or alias in cand):
                    return std, False
        # 3c. 全新类型候选（账本与字典都没有）
        return cand, True

    return None, False


# 确认意图识别（修复 H2 + P1 质量门禁）：
# - 仅接受强确认词，移除『好的/可以/行』等宽词，避免『好的，记一笔…』被误判为 confirm；
# - 否定/疑问语境（不…确定 / 可以吗 / 行不行 …）一律排除。
_CONFIRM_RE = re.compile(
    r"(确认|我同意|同意|记吧|写吧|没问题|就这样|确定)"
    r"|^\s*行[\s，。！,.!？?]*$",
    re.I,
)
_NEG_RE = re.compile(
    r"(不(确定|行|可以|要|想|用|写|记)|能不能|是否|可否|"
    r"吗\s*[?？]?$|行吗$|可以吗$|好吗$|行不行$|是否应该)",
    re.I,
)

# 任务「做完了」的完成动词（单一事实源，与 skill_bridge.is_completion_event 共享，
# 避免两套口径漂移——修复 L3）。conversation.classify 的被动完成信号与
# skill_bridge 的完成事件判定都引用此常量。
COMPLETION_VERBS = (
    "生成了|做好?了|做完了|写完?了|写好了|写完了|完成了|做完|产出|"
    "整理好?了|整理完|搞完?了|交付了|交付|搞定|提交了|提交|"
    "发布了|发布|产出了|做出来"
)
_COMPLETION_VERBS_RE = re.compile(COMPLETION_VERBS)


# 执行意图识别：用户说「帮我写周报 / 生成纪要 / 做PPT」等主动执行请求。
# 仅匹配具体任务域词（周报/纪要/数据/文档/PPT），不吞「报告/摘要」（走 report 意图）。
_EXEC_RE = re.compile(
    r"(帮我|请|麻烦|替我|给我|来个)?\s*"
    r"(写|做|生成|整理|分析|起草|产出|提炼|总结|拟|编|列|画)\s*"
    r"(一[份个篇]|份|个|篇|下)?\s*"
    r"(周报|周报生成|纪要|会议纪要|会议记录|数据|数据分析|报表|文档|材料|文章|要点|PPT|ppt|幻灯片|大纲|csv|excel|xlsx|表格)",
    re.I,
)

# execute 域词同义 → 执行引擎标准类型（csv/excel/表格 等归数据分析）
_EXEC_SYNONYMS = {
    "csv": "数据分析", "excel": "数据分析", "xlsx": "数据分析", "表格": "数据分析",
}


def _extract_exec_type(text):
    """从执行意图话里抽标准任务类型；抽不到返回 None。"""
    m = _EXEC_RE.search(text or "")
    if not m:
        return None
    dom = (m.group(4) or "").lower()
    return _EXEC_SYNONYMS.get(dom) or _resolve_exec_type(m.group(4) or "")


def _extract_exec_input(text):
    """从执行意图话里抽交付物内容：取首个冒号/换行后的部分；无分隔符则去掉执行动词短语。"""
    parts = re.split(r"[:：\n]", text or "", maxsplit=1)
    if len(parts) > 1 and parts[1].strip():
        return parts[1].strip()
    return _EXEC_RE.sub("", text or "").strip(" ：:，,。.、\n")


def classify(text):
    """把一句话归到意图：exit / cancel / confirm / record / report_summary /
    report_full / targets / followup。"""
    t = (text or "").strip()
    if not t:
        return "unknown"
    if re.search(r"(退出|exit|quit|再见|bye)", t, re.I):
        return "exit"
    if re.search(r"(取消|不算了|不要记|别记|false|撤销)", t, re.I):
        return "cancel"
    # 显式记账词优先于确认（P1 修复：『好的，记一笔…』必须归 record，不被确认词吞）
    if re.search(r"(记一笔|记录|记一下|记上|登记|添加任务|新增任务|记下来|写进账本)", t):
        return "record"
    # 被动完成信号：既说「完成了某任务」又给出成本数字 → 自动建议记账
    # 完成动词复用模块级 COMPLETION_VERBS（与 skill_bridge 同一事实源，修复 L3）
    if (re.search(r"(花了|用了|耗时|花费|消耗|占)\s*.{0,12}?\s*(token|分钟|分)", t, re.I)
            and _COMPLETION_VERBS_RE.search(t)):
        return "record"
    if re.search(r"(完整报告|详细报告|九段|生成报告|全部明细|看报告)", t):
        return "report_full"
    if re.search(r"(摘要|一页|总结一下|概览|看下概况|概括)", t):
        return "report_summary"
    if _EXEC_RE.search(t):
        return "execute"
    if re.search(r"(待自动化|哪些值得|自动化建议|该自动化|targets)", t, re.I):
        return "targets"
    # 确认意图：用强确认词 + 否定/疑问排除（P1 已收窄，移除宽词）
    if _CONFIRM_RE.search(t) and not _NEG_RE.search(t):
        return "confirm"
    return "followup"


# ─────────────────────────────────────────────────────────────
# 路由
# ─────────────────────────────────────────────────────────────

def handle(ledger_path, text, state, intent=None):
    """对话主路由。state 是调用方维护的 dict（至少含可选 "pending"）。

    返回中文回复字符串。本函数不读 stdin、不写 stdout，方便上层直接调用。
    intent 可选：调用方（如 REPL）已算好的意图，避免重复 classify（S1）。
    """
    if intent is None:
        intent = classify(text)

    if intent == "exit":
        return "再见，账本已保留。"

    if intent == "cancel":
        if state.get("pending"):
            state["pending"] = None
            return "已取消，未写入账本。"
        return "当前没有待确认的记录。"

    tasks = load_ledger(ledger_path)
    diag = diagnose(tasks)

    if intent == "confirm":
        pending = state.get("pending")
        if not pending:
            # 没有待确认项：不返回错误式提示，降级为普通追问应答（修复 H2）
            return answer_followup(diag, text)
        # 确认时允许补充成本（execute 场景常在此补 baseline）；
        # 同时做成本完整性护栏，避免 execute 无成本时写入全 0 污染账本。
        # 分段解析：baseline 触发词之前=skill 段、之后=baseline 段，互不吞
        # （修复对抗式审查 C1：同句给 skill+baseline 时 skill 不再被静默丢弃）。
        st, sm, base_t, base_m = _parse_skill_and_baseline(text)
        if base_t is not None:
            pending["baseline_tokens"] = base_t
        if base_m is not None:
            pending["baseline_minutes"] = base_m
        if st is not None:
            pending["skill_tokens"] = st
        if sm is not None:
            pending["skill_minutes"] = sm
        _st = pending.get("skill_tokens")
        _bt = pending.get("baseline_tokens")
        if (_st in (None, 0)) and (_bt in (None, 0)):
            return ("⚠️ 还缺成本信息，未写入账本。请补充基准成本（笨办法手搓要多少），"
                    "例如：「确认 baseline 12000 token 25分钟」或「确认 花了1800 token 5分钟」。")
        res = run_long_chain(
            ledger_path, pending["type"], apply=True, date=pending.get("date"),
            skill_tokens=pending.get("skill_tokens"),
            skill_minutes=pending.get("skill_minutes"),
            baseline_tokens=pending.get("baseline_tokens"),
            baseline_minutes=pending.get("baseline_minutes"),
            note=pending.get("note"),
            quality_score=pending.get("quality_score"),
        )
        state["pending"] = None
        if res.get("blocked"):
            return ("⚠️ " + res["block_reason"] + " 这次未写入账本。你可以重新记账并带上基准成本，"
                    "例如：「记一笔 周报生成 花了1800 token 5分钟，手搓要12000 token 25分钟」。")
        new_d = res["new_diag"]
        msg = (f"[已记录] {pending['type']}。当前共 {new_d.n} 条任务，"
               f"累计节省 {format_number(new_d.saved_tok)} Token"
               f"（省 {new_d.token_save_pct:.1f}%）、"
               f"{format_number(new_d.saved_min)} 分钟"
               f"（省 {new_d.time_save_pct:.1f}%）。")
        tgs = propose_automation_targets(new_d)
        if tgs:
            msg += "\n待自动化建议：" + tgs[0]
        return msg

    if intent == "record":
        tokens, minutes = _parse_numbers(text)
        ttype, is_new = _detect_type(text, diag)
        if not ttype:
            return ('没认出任务类型。请这样告诉我：「记一笔 周报生成 花了1800 token 5分钟」，'
                    '或直接说类型名。')
        entry, meta = propose_entry(
            diag, ttype, skill_tokens=tokens, skill_minutes=minutes)
        # 存用户原始输入（未提供的字段留 None，让确认时按历史均值重估）
        state["pending"] = {
            "type": ttype,
            "date": entry["date"],
            "skill_tokens": tokens,
            "skill_minutes": minutes,
            "baseline_tokens": None,
            "baseline_minutes": None,
            "note": entry["note"],
        }
        lines = [
            f"建议记账：{ttype}",
            f"  本技能消耗：{format_number(entry['skill_tokens'])} Token / {entry['skill_minutes']} 分钟",
            f"  基准估计：{format_number(entry['baseline_tokens'])} Token / {entry['baseline_minutes']} 分钟（按历史均值预填）",
        ]
        if is_new:
            lines.append(
                f"  [新类型] 「{ttype}」在账本与类型字典里都没有，确认后将作为新类型记录；"
                f"可在 scripts/type_registry.json 补充别名便于以后识别。")
        if meta["estimated_fields"]:
            lines.append(f"  [提示] 以下为估算值，建议复核：{', '.join(meta['estimated_fields'])}")
        for w in meta["warnings"]:
            lines.append(f"  [注意] {w}")
        lines.append("确认写进账本吗？（回复「确认」即写回，或说「取消」）")
        return "\n".join(lines)

    if intent == "report_summary":
        return generate_markdown_summary(diag)

    if intent == "report_full":
        return generate_markdown_report(diag)

    if intent == "execute":
        return _do_execute(ledger_path, text, state, diag)

    if intent == "targets":
        out = propose_automation_targets(diag)
        if isinstance(out, list) and out and out[0].startswith("账本暂无"):
            return out[0]
        return "待自动化类型建议（按历史基线从高到低）：\n" + "\n".join(
            " - " + l for l in out)

    # 兜底：交给 qa 做数据接地的追问应答
    return answer_followup(diag, text)


def _do_execute(ledger_path, text, state, diag):
    """执行意图：调 executor 生成交付物，并自动 propose 一条记账（dry-run 预览）。

    与 record 意图的区别：record 是「我刚做完了、花了X」的被动记账；
    execute 是「帮我做X」的主动执行。两者最终都进同一套 run_long_chain 护栏，
    默认 dry-run，确认写回需补 baseline 基准成本（P0 护栏不破）。
    """
    etype = _extract_exec_type(text)
    if not etype:
        return ("没认出要执行的任务类型。支持：周报生成 / 会议纪要 / 数据分析 / "
                "文档整理 / PPT大纲。例如：「帮我写周报：这周完成了 A、B、C」")
    content = _extract_exec_input(text)
    ok, rendered, meta = _exec_render(etype, content)
    if not ok:
        return rendered

    # 自动 propose 记账（dry-run 预览，存 pending）。执行场景本地 CLI 不持有真实消耗，
    # skill 维度留 None，确认写回时由护栏要求补 baseline（P0 不破）。
    # 注意：此处无需调用 propose_entry —— 只取日期与空备注即可，避免为「历史均值估算」
    # 做无谓计算（其 meta 警告本就被丢弃）—— S2 修复：消除 _do_execute 的 propose_entry 浪费。
    # 质量分来自 execute 渲染后的确定性结构断言（不降质量护栏），跨轮经 pending 带入门。
    state["pending"] = {
        "type": etype,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "skill_tokens": None,
        "skill_minutes": None,
        "baseline_tokens": None,
        "baseline_minutes": None,
        "note": "",
        "quality_score": meta.get("quality_score"),
    }
    lines = [
        rendered,
        "",
        "---",
        f"已生成交付物（{etype}）。",
    ]
    # 不降质量护栏：当场给质量分，让用户在记账前就「看清」交付物结构完整度
    if meta.get("quality_score") is not None:
        checks = meta.get("quality_checks") or []
        mark_s = " ".join(f"{n}{'✓' if ok else '✗'}" for n, ok in checks)
        lines.append(f"质量分：{meta['quality_score']}/100（门槛 {meta.get('quality_credible') and '达标' or '偏低'}）｜ 检查：{mark_s}")
    lines += [
        "是否记入账本？",
        "回复「确认」即建议记账；写回账本需补 baseline 基准成本（笨办法手搓要多少），",
        "例如：「确认 baseline 12000 token 25分钟」。",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# CLI（交互式 REPL，薄包装）
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="办公室提效 · 对话式自动记账编排（office-token-booster）")
    parser.add_argument("ledger", nargs="?", help="账本 JSON 路径")
    parser.add_argument("--ledger", dest="ledger", help="账本 JSON 路径（同位置参数）")
    args = parser.parse_args()

    ledger = args.ledger
    if not ledger:
        print("[错误] 请提供账本路径：python conversation.py <ledger.json>",
              file=sys.stderr)
        return 2
    try:
        load_ledger(ledger)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 2

    state = {}
    print("=== 办公室提效对话（执行 + 自动记账）===")
    print('试试：我刚生成了周报，花了1800 token 5分钟 ｜ 哪个类型省最多？ '
          '｜ 生成摘要 ｜ 待自动化建议 ｜ 退出')
    running = True
    while running:
        try:
            line = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见，账本已保留。")
            running = False
            break
        if not line:
            continue
        intent = classify(line)                       # 仅算一次（S1：消除重复 classify）
        resp = handle(ledger, line, state, intent)
        if intent == "exit":
            print("助手> " + resp)
            running = False
            break
        print("助手> " + resp + "\n")


if __name__ == "__main__":
    sys.exit(main())
