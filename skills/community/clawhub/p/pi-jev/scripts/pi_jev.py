# -*- coding: utf-8 -*-
"""
pi-jev 决策层：自动选技能（skill-picker）+ 模型档位路由（model-router）+ 使用学习（usage learning）
借鉴开源 Pi 编码智能体 + Jev 决策层思路，纯 Python 标准库实现，无需 API 密钥。

用法：
  python pi_jev.py "我要给客户写跟进私信"                 # 决策卡：推荐技能+脚本+档位+历史经验
  python pi_jev.py "审核这篇稿子" --note "结果：通过"      # 决策 + 记录结果
  python pi_jev.py --review                              # 每周复盘：使用频率 + 固化建议
"""
import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACK_DIR = os.path.join(SCRIPT_DIR, "..")
MEMORY_DIR = os.path.join(SCRIPT_DIR, "..", "memory")
USAGE_FILE = os.path.join(MEMORY_DIR, "usage-log.md")
USAGE_HEADER = """# 使用记录（pi-jev 决策层自动记录）

每次调用决策层记一行；--review 每周复盘，把高频技能与经验固化。

| 日期 | 任务 | 选中技能 | 模型档位 | 备注 |
|---|---|---|---|---|
"""

SKILLS = [
    {
        "name": "ip-peipao-9clients",
        "title": "客户陪跑与转化",
        "script": "python ip-peipao-9clients/scripts/followup.py --weekly",
        "keywords": ["客户", "跟进", "私信", "陪跑", "转化", "成交", "漏斗", "9.9", "600", "企业版",
                     "话术", "学员", "付费", "待定", "卡点"],
        "tier": "标准",
    },
    {
        "name": "yihaiyoudao",
        "title": "内容审核与原创改造",
        "script": "python yihaiyoudao/scripts/audit.py 文章.txt",
        "keywords": ["审核", "原创", "洗稿", "限流", "敏感词", "风险", "改写", "观点", "文案",
                     "公众号", "小红书", "抖音", "标题", "风格"],
        "tier": "标准",
    },
    {
        "name": "qingchuang-shizhan",
        "title": "内容创业与轻创业实操",
        "script": "python qingchuang-shizhan/scripts/topic_bank.py --positioning \"定位\" --audience \"人群\" --calendar",
        "keywords": ["选题", "内容", "创业", "副业", "账号", "定位", "自媒体", "私域", "变现",
                     "图文", "短视频", "涨粉", "更新", "平台"],
        "tier": "标准",
    },
    {
        "name": "zhanlue-peipao",
        "title": "战略陪跑教练",
        "script": "python zhanlue-peipao/scripts/roadmap.py --income 年收入 --hours 每周小时 --target 档位",
        "keywords": ["战略", "规划", "目标", "10万", "100万", "1000万", "档位", "里程碑",
                     "路线图", "年入", "诊断", "升档", "复盘", "长期"],
        "tier": "深度",
    },
]

DEEP_WORDS = ["战略", "规划", "诊断", "复盘", "深度", "商业模式", "100万", "1000万", "长期", "里程碑"]
FAST_WORDS = ["快速", "简单", "草稿", "初稿", "一句话", "立刻", "马上", "随便"]


def ensure_usage_file():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w", encoding="utf-8") as f:
            f.write(USAGE_HEADER)


def load_usage_counts():
    """统计每个技能在 usage-log.md 里被选中的次数（频率加权用）。"""
    counts = {}
    if not os.path.exists(USAGE_FILE):
        return counts
    with open(USAGE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("|") and "选中技能" not in line and "---" not in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[2]:
                    counts[cells[2]] = counts.get(cells[2], 0) + 1
    return counts


def load_learned_experiences(skill_name, limit=3):
    """从对应技能 memory/learning-log.md 召回最近经验（上下文精简）。"""
    path = os.path.join(PACK_DIR, skill_name, "memory", "learning-log.md")
    rows = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("|") and "经验" not in line and "---" not in line:
                    cells = [c.strip() for c in line.strip().strip("|").split("|")]
                    if len(cells) >= 3 and cells[2]:
                        rows.append(f"{cells[0]}｜{cells[2]}")
    return rows[-limit:]


def score_task(text):
    results = []
    for s in SKILLS:
        hits = sum(1 for k in s["keywords"] if k in text)
        results.append((s, hits))
    results.sort(key=lambda x: -x[1])
    return results


def route_tier(text, chosen):
    if any(w in text for w in DEEP_WORDS) or chosen["tier"] == "深度":
        return "深度（推理模型，慢但准）"
    if any(w in text for w in FAST_WORDS):
        return "快（轻量模型，省 token）"
    return "标准（均衡）"


def decision_card(text, note):
    results = score_task(text)
    top, top_hits = results[0]
    second, second_hits = results[1] if len(results) > 1 else (None, 0)
    usage = load_usage_counts()
    # 历史使用加权：并列时优先用过多的技能
    if top_hits == second_hits and usage.get(second["name"], 0) > usage.get(top["name"], 0):
        top, second, top_hits, second_hits = second, top, second_hits, top_hits
    tier = route_tier(text, top)
    out = []
    out.append("===== pi-jev 决策层 · 任务路由 =====")
    out.append(f"任务：{text}")
    out.append(f"→ 推荐技能：{top['name']}（{top['title']}）｜命中 {top_hits} 个关键词"
               + (f"｜历史使用 {usage.get(top['name'], 0)} 次" if usage.get(top['name']) else ""))
    out.append(f"→ 脚本命令：{top['script']}")
    out.append(f"→ 模型档位建议：{tier}")
    exps = load_learned_experiences(top["name"])
    if exps:
        out.append("→ 相关历史经验（已学过）：")
        for e in exps:
            out.append(f"    · {e}")
    else:
        out.append("→ 相关历史经验：暂无（这是第一次用，用 --note 记录结果，越用越准）")
    if top_hits == 0:
        out.append("→ 提示：任务没有命中关键词，建议先让用户用一句话说清目标，或直接走 zhanlue-peipao 定方向。")
    return "\n".join(out), top["name"], tier


def record_usage(task, skill, tier, note):
    ensure_usage_file()
    safe = lambda x: x.replace("|", "／").replace("\n", " ")
    with open(USAGE_FILE, "a", encoding="utf-8") as f:
        f.write(f"| 今日 | {safe(task)} | {safe(skill)} | {safe(tier)} | {safe(note or '')} |\n")
    print(f"[学习] 已记录到使用库：{USAGE_FILE}")


def review():
    ensure_usage_file()
    usage = load_usage_counts()
    out = []
    out.append("===== pi-jev 周复盘 =====")
    if not usage:
        out.append("使用记录为空：先跑几次 python pi_jev.py \"任务\" 再复盘。")
        return "\n".join(out)
    ranked = sorted(usage.items(), key=lambda x: -x[1])
    out.append("各技能使用频率：")
    for name, cnt in ranked:
        out.append(f"  {name}：{cnt} 次")
    top_name, top_cnt = ranked[0]
    out.append(f"\n固化建议：{top_name} 使用最多（{top_cnt} 次）。")
    out.append(f"  1) 回看 {top_name}/memory/learning-log.md，把出现 2 次以上的经验固化进它的 SKILL.md 或词库。")
    out.append("  2) 若某类任务经常路由不到对应技能，把关键词补充进本脚本 SKILLS 表。")
    out.append("  3) 决策卡里出现的「相关历史经验」就是已学到的沉淀，复盘时确认是否已固化。")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="pi-jev 决策层：自动选技能 + 档位路由 + 使用学习")
    ap.add_argument("task", nargs="?", help="一句话任务描述")
    ap.add_argument("--note", help="补充本次使用结果（记录到使用库）")
    ap.add_argument("--review", action="store_true", help="周复盘：使用频率 + 固化建议")
    args = ap.parse_args()

    if args.review:
        print(review())
        return

    if not args.task:
        print("错误：请输入任务描述。用法：python pi_jev.py \"我要给客户写跟进私信\"；或 --review 周复盘。")
        sys.exit(1)

    card, skill, tier = decision_card(args.task, args.note)
    print(card)
    record_usage(args.task, skill, tier, args.note)


if __name__ == "__main__":
    main()
