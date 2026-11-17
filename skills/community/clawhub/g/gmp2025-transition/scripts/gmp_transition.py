#!/usr/bin/env python3
"""gmp2025-transition: 中国《医疗器械生产质量管理规范》2025 版过渡时间线与自查清单.

依据：国家药监局 2025 年第 107 号公告 —— 新修订《医疗器械生产质量管理规范》
自 2026-11-01 起施行，替代 2014 年版（2014 年第 64 号公告）。

用法:
  python gmp_transition.py timeline [--as-of YYYY-MM-DD] [--json]
  python gmp_transition.py status   [--as-of YYYY-MM-DD] [--json]
  python gmp_transition.py checklist [--json]
  python gmp_transition.py sources

零第三方依赖，纯标准库。数据核定日：2026-09-21。MIT License.
"""
import argparse
import json
import sys
from datetime import date

DATA_AS_OF = "2026-09-21"

# 国家层面硬节点（已核验）
HARD_MILESTONES = [
    ("2026-11-01", "新修订《医疗器械生产质量管理规范》正式施行（同时替代 2014 年版）"),
]

# 省级实施口径示例（各地时限不同，必须按属地药监局方案执行）
PROVINCIAL_SAMPLES = [
    ("广西", "2026-04-30", "完成全区企业全覆盖宣贯培训"),
    ("广西", "2026-10-31", "企业对照《规范》完成自查改进并形成实施情况报告，报送属地市场监管局/检查分局"),
    ("广西", "2026-12-31", "各级监管部门开展实施情况督查评估"),
    ("广东（东莞口径）", "2026-05-31", "提交自查报告及整改计划书"),
    ("广东（东莞口径）", "2026-10-31", "提交整改报告"),
]

# 已核验的结构变化（来源：官方公告与权威报道，条款级差异须以官方原文为准）
VERIFIED_STRUCTURE = {
    "2014 版": "2014 年第 64 号公告",
    "2025 版": "2025 年第 107 号公告，共 15 章 132 条",
    "新增章节": ["质量保证", "验证与确认", "委托生产与外协加工"],
    "融合方向": ["全生命周期质量风险管理", "质量管理体系建设", "数智化监管与数字化转型", "关键岗位人员任职履职要求"],
}

# 过渡期自查行动清单（行动层面，非条款差异）
CHECKLIST = [
    ("差距识别", "获取 2025 年第 107 号公告原文与配套解读，逐条对照现行体系文件，形成差距清单（含不适用项及理由）"),
    ("体系文件", "按差距清单修订质量手册、程序文件、作业指导书与记录表单，完成换版与发放控制"),
    ("人员与培训", "组织全员培训，重点覆盖法定代表人/主要负责人/管理者代表/生产与质量管理负责人/产品放行审核人等关键岗位"),
    ("风险管理", "复核风险管理文件与产品放行逻辑，确保覆盖全生命周期质量风险（ISO 14971 / GB/T 42062 衔接）"),
    ("验证与确认", "梳理并补齐设计确认、过程确认、灭菌确认、软件确认等验证与确认证据链"),
    ("委托生产与外协加工", "复核委托生产质量协议、受托方审核记录与外协加工控制要求"),
    ("生产与过程控制", "复核厂房设施设备、洁净与环境监测、工艺用水/用气、批记录与追溯要求"),
    ("数据与数智化", "评估电子记录、数据可靠性与信息化系统的合规基线（电子签名/审计追踪如适用）"),
    ("内审与管理评审", "施行前完成一轮以内审；自查整改后开展管理评审，评估体系适宜性、充分性、有效性"),
    ("自查与报送", "按属地药监局要求完成自查/整改报告填报与报送（注意各地时限不同）"),
    ("注册与体系衔接", "排查在审注册与体系核查项目，确认技术文件与体系现状一致，避免核查期被开不符合项"),
    ("上市后活动", "确认不良事件监测、召回、变更控制与再评价流程在新规范下仍可运行"),
]


def parse_as_of(s):
    if not s:
        return date.today()
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def days_between(a, b):
    return (b - a).days


def phase_of(days_left):
    if days_left < 0:
        return "已施行", "按新规运行；关注属地监管的督查评估与不符合项整改"
    if days_left <= 90:
        return "冲刺期", "距施行不足 90 天：优先完成体系换版、内审与管理评审，并按时报送自查/整改报告"
    if days_left <= 180:
        return "自查整改期", "完成差距识别与整改闭环，安排内审与培训留痕"
    return "准备期", "启动差距识别、培训计划与体系文件修订排期"


def cmd_timeline(as_of, as_json):
    eff = date(2026, 11, 1)
    rows = []
    for d, name in HARD_MILESTONES:
        dd = date(*[int(x) for x in d.split("-")])
        rows.append({"date": d, "event": name, "scope": "国家", "days_from_as_of": days_between(as_of, dd)})
    for prov, d, name in PROVINCIAL_SAMPLES:
        dd = date(*[int(x) for x in d.split("-")])
        rows.append({"date": d, "event": name, "scope": prov, "days_from_as_of": days_between(as_of, dd)})
    rows.sort(key=lambda r: r["date"])
    if as_json:
        return json.dumps({"as_of": as_of.isoformat(), "data_as_of": DATA_AS_OF, "milestones": rows},
                          ensure_ascii=False, indent=2)
    out = [f"GMP 2025 过渡时间线（截至 {as_of.isoformat()}，数据核定 {DATA_AS_OF}）", ""]
    for r in rows:
        tag = "已过" if r["days_from_as_of"] < 0 else f"还有 {r['days_from_as_of']} 天"
        out.append(f"  {r['date']}  [{r['scope']}]  {r['event']}   （{tag}）")
    out += ["", "  ⚠️ 省级时限为示例（广西/广东口径），务必以属地药监局方案为准。"]
    return "\n".join(out)


def cmd_status(as_of, as_json):
    eff = date(2026, 11, 1)
    left = days_between(as_of, eff)
    phase, advice = phase_of(left)
    if as_json:
        return json.dumps({"as_of": as_of.isoformat(), "data_as_of": DATA_AS_OF,
                           "effective_date": "2026-11-01", "days_left": left,
                           "phase": phase, "advice": advice,
                           "source": "国家药监局 2025 年第 107 号公告"},
                          ensure_ascii=False, indent=2)
    return "\n".join([
        f"当前日期        : {as_of.isoformat()}",
        f"施行日          : 2026-11-01（国家药监局 2025 年第 107 号公告）",
        f"距施行          : {left} 天" + ("（已施行）" if left < 0 else ""),
        f"所处阶段        : {phase}",
        f"建议动作        : {advice}",
        f"替代关系        : 2025 版施行后替代 2014 年版（2014 年第 64 号公告）",
        "",
        "⚠️ 本工具只做时间与行动提示，不判定企业是否符合规范；条款级差异以官方原文为准。",
    ])


def cmd_checklist(as_json):
    if as_json:
        return json.dumps({"data_as_of": DATA_AS_OF,
                           "items": [{"group": g, "action": a} for g, a in CHECKLIST],
                           "verified_structure": VERIFIED_STRUCTURE}, ensure_ascii=False, indent=2)
    out = [f"GMP 2025 过渡自查清单（{len(CHECKLIST)} 项，数据核定 {DATA_AS_OF}）", ""]
    for i, (g, a) in enumerate(CHECKLIST, 1):
        out.append(f"  {i:>2}. [{g}] {a}")
    out += ["", "已核验的结构变化：",
            f"  · 2014 版：{VERIFIED_STRUCTURE['2014 版']}",
            f"  · 2025 版：{VERIFIED_STRUCTURE['2025 版']}",
            f"  · 新增章节：{'、'.join(VERIFIED_STRUCTURE['新增章节'])}",
            f"  · 融合方向：{'、'.join(VERIFIED_STRUCTURE['融合方向'])}",
            "", "⚠️ 条款级差异（逐条对照表）须以官方原文为准，本清单只到行动层。"]
    return "\n".join(out)


def cmd_sources():
    return "\n".join([
        "数据来源（2026-09-21 核定，多源交叉）",
        "  · 国家药监局 2025 年第 107 号公告：新修订《医疗器械生产质量管理规范》2026-11-01 施行",
        "  · 人民网广西频道 2026-04-24：自治区药监局部署实施工作（宣贯培训 / 企业自查改进 / 全面实施 / 督查评估）",
        "  · 甘肃省药监局 2026-01-14：贯彻实施工作方案",
        "  · 江西省药监局 2026-01-13：新修订实施方案",
        "  · 东莞市市场监管局 2026-04-16：自查及整改报告报送通知（自查 5/31、整改 10/31）",
        "  · 南方+ 报道：新版共 15 章 132 条，新增质量保证、验证与确认、委托生产与外协加工三章",
        "",
        "引用前请以官方最新原文与属地药监局方案复核。",
    ])


def main():
    ap = argparse.ArgumentParser(description="GMP 2025 过渡时间线与自查清单")
    ap.add_argument("mode", choices=["timeline", "status", "checklist", "sources"])
    ap.add_argument("--as-of", dest="as_of", default="", help="基准日期 YYYY-MM-DD（默认今天）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d = parse_as_of(a.as_of)
    if a.mode == "timeline":
        print(cmd_timeline(d, a.json))
    elif a.mode == "status":
        print(cmd_status(d, a.json))
    elif a.mode == "checklist":
        print(cmd_checklist(a.json))
    else:
        print(cmd_sources())
    return 0


if __name__ == "__main__":
    sys.exit(main())
