#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qa.py — 对话式诊断的「追问」外壳（office-token-booster / B 线）

消费诊断内核产出的 Diagnosis 对象，对用户的追问给出**基于账本数据**的应答，
避免大模型凭空编造数字（grounding）。这是「对话式诊断」骨架的追问层：
先 show 一页摘要 + 图表（report_engine），再在追问时调用本模块做数据接地。

用法：
  python qa.py <ledger.json> "哪个任务类型节省最多？"

  或在 Python 中：
  from diagnose import load_ledger, diagnose
  from qa import answer_followup
  diag = diagnose(load_ledger("ledger.json"))
  print(answer_followup(diag, "每周节省趋势如何？"))
"""

import argparse
import sys

from diagnose import load_ledger, diagnose, format_number


def _top_type(diag):
    return diag.by_type[0] if diag.by_type else None


def _hottest_type(diag):
    return max(diag.by_type, key=lambda x: x["baseline_tokens"]) if diag.by_type else None


def _lowest_type(diag):
    """节省 Token 最少的类型（提效最不明显的场景）。"""
    return min(diag.by_type, key=lambda x: x["saved_tokens"]) if diag.by_type else None


def _consume_most_type(diag):
    """Token 实际消耗最多的类型（本技能实耗 skill_tokens 最高）。

    与「节省最多」(_top_type) 严格区分：消耗 = 你为这类任务实际花掉的 Token，
    节省 = 基准 − 实耗的差额。追问里的「消耗最多」必须锚定 skill_tokens，
    不能落到 saved_tokens 分支（否则「最多」会错误路由到节省口径）。
    """
    return max(diag.by_type, key=lambda x: x["skill_tokens"]) if diag.by_type else None


def _match_type(diag, q):
    """若追问里出现某个已记录的任务类型名，返回该类型 dict，否则 None。"""
    for d in diag.by_type:
        if d["task_type"] and d["task_type"] in q:
            return d
    return None


# ─────────────────────────────────────────────────────────────
# 追问意图的关键词表：一种意图对应一组同义问法，集中在此便于增删口语说法。
# ─────────────────────────────────────────────────────────────
_KW_REPORT = ("完整报告", "完整", "九段", "明细", "看报告", "生成报告", "全部")
_KW_METHOD = ("怎么算", "怎么得出", "公式", "方法", "如何计算", "基准是什么", "基线是什么", "baseline")
_KW_TRUST = ("可信", "准确", "可靠", "异常", "偏差", "虚高", "真实", "水分", "护栏")
_KW_TASK_LIST = ("明细", "清单", "哪些任务", "做了什么", "任务列表", "记录", "列表")
_KW_WORST = ("最差", "最低", "不省", "最少", "拉胯", "最不划算")
_KW_TIME = ("耗时", "时间", "分钟", "花了多久", "效率")
_KW_COUNT = ("多少任务", "几条", "记录数", "个数", "多少条", "一共几条")
_KW_TOTAL = ("总共", "合计", "总节省", "一共", "总体", "概览", "总结一下")
_KW_RATIO = ("比例", "百分比", "省了", "省多少", "%", "多高")
_KW_CONSUME = ("消耗", "用量", "占用", "实耗", "花掉", "用了多少", "花了多少",
               "用掉", "用得最多", "最费", "费token", "费钱", "耗费最多")
_KW_SAVE_MOST = ("最多", "最高", "主力", "第一", "最大", "top", "Top",
                 "最省", "省最多", "省得最多", "最划算")
_KW_AUTOMATE = ("值得", "自动化", "优先", "场景", "推荐做", "哪些任务值得", "哪类")
_KW_PERIOD = ("本期", "上期", "比上周", "相比上周", "和上周比", "这周比", "环比")
_KW_WEEK = ("周", "趋势", "变化", "每周", "时间线", "走势")
_KW_ADVICE = ("建议", "怎么", "如何", "下一步", "优化", "改进", "该怎么做")
_KW_INSIGHT = ("洞察", "发现", "结论", "看出来", "总结", "亮点")

# 「消耗」命中但同时问「省」时，按「节省最多」处理
_KW_SAVING_EXCLUDE = ("省", "节省", "省下")


def _ask_report(diag, q):
    return ("请对我说「生成完整报告」，技能将调用 report_engine 输出完整明细报告"
            "（任务类型 / 周趋势 / 执行情况 / 产出物 / 洞察建议 / 可信度提示等）。")


def _ask_type(diag, q):
    hit = _match_type(diag, q)
    return (f"「{hit['task_type']}」：{hit['count']} 次，基准 {format_number(hit['baseline_tokens'])} "
            f"→ 本技能 {format_number(hit['skill_tokens'])} Token，"
            f"省 {format_number(hit['saved_tokens'])}（{hit['token_save_pct']:.1f}%）；"
            f"耗时省 {format_number(hit['saved_minutes'])} 分（{hit['time_save_pct']:.1f}%）。")


def _ask_method(diag, q):
    return (diag.methodology + "\n"
            "简言之：节省 = 你填的「基准估计」−「本技能实际消耗」。基准是你对"
            "「自己手搓 / 反复试错」成本的主观估计，不是平台实测扣费。")


def _ask_trust(diag, q):
    if diag.caveats:
        return "数据可信度提示（已识别以下可能拉高提效声称的项）：\n" + "\n".join(
            f"- ⚠️ {c}" for c in diag.caveats)
    return ("当前未发现明显异常。但请记住：节省值是你填的基准估计的参照值，不是平台实测扣费；"
            "其可信度完全取决于「基准」是否如实反映你手搓的真实成本。")


def _ask_task_list(diag, q):
    if not diag.tasks:
        return "暂无任务明细。"
    lines = [f"共 {len(diag.tasks)} 条任务："]
    for i, t in enumerate(diag.tasks, 1):
        bt = t.get("baseline_tokens", 0) or 0
        st = t.get("skill_tokens", 0) or 0
        note = t.get("note") or ""
        lines.append(f"{i}. {t.get('date','')} ｜ {t.get('type','')} ｜ 省 "
                     f"{format_number(bt - st)} Token {('｜ ' + note) if note else ''}")
    return "\n".join(lines)


def _ask_worst(diag, q):
    low = _lowest_type(diag)
    if low:
        return (f"提效最不明显的是「{low['task_type']}」：{low['count']} 次仅省 "
                f"{format_number(low['saved_tokens'])} Token（省 {low['token_save_pct']:.1f}%）。"
                f"可检查该类是否基线估计偏低，或本技能在该场景收益本就有限。")
    return "暂无可统计的任务类型。"


def _ask_time(diag, q):
    return (f"合计节省 {format_number(diag.saved_min)} 分钟（省 {diag.time_save_pct:.1f}%）；"
            f"基准 {format_number(diag.total_base_min)} 分 → 本技能 {format_number(diag.total_skill_min)} 分。")


def _ask_count(diag, q):
    return f"账本共 {diag.n} 条任务记录。"


def _ask_total(diag, q):
    return (
        f"共 {diag.n} 条任务，合计节省 {format_number(diag.saved_tok)} Token"
        f"（省 {diag.token_save_pct:.1f}%）、{format_number(diag.saved_min)} 分钟"
        f"（省 {diag.time_save_pct:.1f}%）。"
    )


def _ask_ratio(diag, q):
    return (f"Token 节省比例 {diag.token_save_pct:.1f}%，"
            f"时间节省比例 {diag.time_save_pct:.1f}%。")


def _ask_consume_most(diag, q):
    cons = _consume_most_type(diag)
    if cons:
        return (
            f"Token 实耗最多的任务类型是「{cons['task_type']}」：{cons['count']} 次共消耗 "
            f"{format_number(cons['skill_tokens'])} Token（本技能实耗）；"
            f"其手搓基准约 {format_number(cons['baseline_tokens'])} Token。"
        )
    return "暂无可统计的任务类型。"


def _ask_save_most(diag, q):
    top = _top_type(diag)
    if top:
        return (f"节省最多的任务类型是「{top['task_type']}」：{top['count']} 次共省 "
                f"{format_number(top['saved_tokens'])} Token（省 {top['token_save_pct']:.1f}%）。")
    return "暂无可统计的任务类型。"


def _ask_automate(diag, q):
    hot = _hottest_type(diag)
    if hot:
        return (f"基线成本最高、最值得自动化的是「{hot['task_type']}」：单次基线约 "
                f"{format_number(hot['baseline_tokens'] / max(hot['count'], 1))} Token，"
                f"自动化空间最大。")
    return "暂无可分析的任务类型。"


def _ask_period(diag, q):
    pc = diag.period_compare
    if not pc:
        return "账本中周数据不足（需要至少两周记录），暂无法做「本期 vs 上期」对比。请继续累积记账。"
    arrow = {"up": "▲ 上升", "down": "▼ 下降", "flat": "▬ 持平", "new": "✦ 新增"}.get(pc["direction"], "")
    pct = "—" if pc["saved_tokens_pct"] is None else f"{pc['saved_tokens_pct']:+.1f}%"
    cur, prev = pc["current"], pc["previous"]
    return (
        f"本期（{pc['current_week']}）对比上期（{pc['previous_week']}）：\n"
        f"- 节省 Token：{format_number(cur['saved_tokens'])}（{arrow}，{pct}）；上期 {format_number(prev['saved_tokens'])}\n"
        f"- 任务数：{cur['count']} 次（上期 {prev['count']} 次）\n"
        f"- 节省时间：{format_number(cur['saved_minutes'])} 分（上期 {format_number(prev['saved_minutes'])} 分）"
    )


def _ask_weekly(diag, q):
    if not diag.by_week:
        return "账本中没有可用的日期信息，无法按周分析。"
    lines = ["按周节省 Token："]
    for w in diag.by_week:
        lines.append(f"- {w['week']}：{w['count']} 次任务，省 "
                     f"{format_number(w['saved_tokens'])} Token（省 {w['token_save_pct']:.1f}%）")
    return "\n".join(lines)


def _ask_advice(diag, q):
    if not diag.recommendations:
        return "暂无建议。"
    return "建议：\n" + "\n".join(f"- {r}" for r in diag.recommendations)


def _ask_insight(diag, q):
    if not diag.insights:
        return "暂无洞察。"
    return "洞察：\n" + "\n".join(f"- {x}" for x in diag.insights)


def _fallback(diag, q):
    return (
        "我已为你生成「一页摘要」作为首屏。可继续追问，或说「生成完整报告」查看完整明细。常见问法：\n"
        "- 总共节省了多少？\n"
        "- 哪个任务类型节省最多 / 最不省？\n"
        "- 哪个场景最值得自动化？\n"
        "- 按周趋势如何？\n"
        "- 有哪些任务明细？\n"
        "- 这些数字怎么算出来的 / 可信吗？\n"
        "- 有什么建议 / 洞察？"
    )


def _keywords(keywords, exclude=()):
    """构造谓词：问句命中任一同义问法、且不含排除词时匹配。"""
    def match(diag, q):
        return any(k in q for k in keywords) and not any(k in q for k in exclude)
    return match


def _type_name(diag, q):
    """问句里出现某个已记录的任务类型名时匹配（如「会议纪要怎么样」）。"""
    return _match_type(diag, q) is not None


# 路由表**按序求值**，顺序本身是语义，不可随意重排：
# - 「消耗」必须早于「节省最多」：否则「消耗最多」会被「最多」抢进节省口径；
# - 类型名匹配紧跟报告路由：否则「周报怎么样」会先落到「报告」分支。
# 表驱动的价值是把「问法 → 应答」集中在一处可见，而不是消掉顺序敏感性。
_ROUTES = (
    (_keywords(_KW_REPORT), _ask_report),
    (_type_name, _ask_type),
    (_keywords(_KW_METHOD), _ask_method),
    (_keywords(_KW_TRUST), _ask_trust),
    (_keywords(_KW_TASK_LIST), _ask_task_list),
    (_keywords(_KW_WORST), _ask_worst),
    (_keywords(_KW_TIME), _ask_time),
    (_keywords(_KW_COUNT), _ask_count),
    (_keywords(_KW_TOTAL), _ask_total),
    (_keywords(_KW_RATIO), _ask_ratio),
    (_keywords(_KW_CONSUME, _KW_SAVING_EXCLUDE), _ask_consume_most),
    (_keywords(_KW_SAVE_MOST), _ask_save_most),
    (_keywords(_KW_AUTOMATE), _ask_automate),
    (_keywords(_KW_PERIOD), _ask_period),
    (_keywords(_KW_WEEK), _ask_weekly),
    (_keywords(_KW_ADVICE), _ask_advice),
    (_keywords(_KW_INSIGHT), _ask_insight),
)


def answer_followup(diag, question):
    """基于 Diagnosis 结构化数据应答常见追问。返回中文文本（已接地，不编造）。

    命中 _ROUTES 中的第一条匹配意图；未命中则给出常见问法兜底。
    """
    q = (question or "").strip()
    if not q:
        return "请提出一个关于账本的具体问题，例如：节省最多的任务类型是什么？"

    if diag.n == 0:
        return "账本为空，暂无可分析的数据。请先记录任务账本。"

    for match, handler in _ROUTES:
        if match(diag, q):
            return handler(diag, q)

    return _fallback(diag, q)


def main():
    parser = argparse.ArgumentParser(description="对话式诊断追问应答（office-token-booster）")
    parser.add_argument("ledger", help="账本 JSON 路径")
    parser.add_argument("question", help="追问内容")
    args = parser.parse_args()
    try:
        tasks = load_ledger(args.ledger)
    except (FileNotFoundError, ValueError) as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 2
    diag = diagnose(tasks)
    print(answer_followup(diag, args.question))
    return 0


if __name__ == "__main__":
    sys.exit(main())
