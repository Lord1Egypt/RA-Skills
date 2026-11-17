# -*- coding: utf-8 -*-
"""
ip-peipao-9clients 自动化脚本：每日跟进计划 + 私信草稿 + 每周漏斗周报
用法：
  python followup.py                # 今日跟进计划（自动读同目录 clients.json）
  python followup.py --weekly       # 每周漏斗周报
  python followup.py --clients 我的客户.json --weekly
  python followup.py --date 2026-10-15
规则：每天最多挑 3 个客户；优先"该动没动"的人；L1 观望层不追单。
"""
import argparse
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CLIENTS = [
    {"id": "客户A", "tier": "L1", "paid_status": "未付款", "days_since_action": 12,
     "blocker": "无行动", "direction": "决策顾问类", "next_action": "交3个目标客户名单"},
    {"id": "客户B", "tier": "L2", "paid_status": "399元已付", "days_since_action": 4,
     "blocker": "没方向，虚假安全感", "direction": "幕后军师类", "next_action": "本周发1条方向主题内容"},
    {"id": "客户C", "tier": "L3", "paid_status": "2999元待定", "days_since_action": 6,
     "blocker": "观望未付", "direction": "企业陪跑", "next_action": "约20分钟诊断通话"},
    {"id": "客户D", "tier": "L2", "paid_status": "517元已付", "days_since_action": 2,
     "blocker": "输出易断，流量不稳", "direction": "个人IP内容", "next_action": "确认固定发布日，排下周选题"},
    {"id": "客户E", "tier": "L2", "paid_status": "388元已付", "days_since_action": 9,
     "blocker": "找方向与内耗", "direction": "细分人群决策陪跑", "next_action": "交整理10个案例"},
    {"id": "客户F", "tier": "L2", "paid_status": "598元已付", "days_since_action": 5,
     "blocker": "需要落地", "direction": "创始人IP升级", "next_action": "本周做1个案例诊断"},
    {"id": "客户G", "tier": "L2", "paid_status": "600元已付", "days_since_action": 8,
     "blocker": "缺差异化", "direction": "避坑指南内容+引流变现", "next_action": "交10个坑点清单"},
    {"id": "客户H", "tier": "L2", "paid_status": "700元已付", "days_since_action": 3,
     "blocker": "案例进度慢", "direction": "案例标准化", "next_action": "本周再跑3个案例+1次同行拆解"},
    {"id": "客户I", "tier": "L2", "paid_status": "388元已付", "days_since_action": 7,
     "blocker": "卡在判断逻辑梳理", "direction": "Agent判断标准", "next_action": "交出判断标准初稿"},
]

TIER_BASE = {"L1": 10, "L2": 20, "L3": 30}
TIER_NAME = {"L1": "L1 观望", "L2": "L2 执行", "L3": "L3 企业版"}

LOG_DIR = os.path.join(SCRIPT_DIR, "..", "memory")
LOG_FILE = os.path.join(LOG_DIR, "learning-log.md")
LOG_HEADER = """# 学习日志（自迭代用）

每次使用后把新经验记一行；每周复盘，把出现 2 次以上的经验固化到 SKILL.md 或词库。

| 日期 | 任务类型 | 经验/记录 |
|---|---|---|
"""


def log_learn(date, note):
    """把一条跟进经验追加到学习日志（自迭代闭环的输入）。"""
    if not note:
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(LOG_HEADER)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"| {date} | 跟进记录 | {note.replace('|', '／')} |\n")
    print(f"[学习] 已记录到学习日志：{LOG_FILE}")


def load_clients(path):
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    local = os.path.join(SCRIPT_DIR, "clients.json")
    if os.path.exists(local):
        with open(local, "r", encoding="utf-8") as f:
            return json.load(f)
    example = os.path.join(SCRIPT_DIR, "clients.example.json")
    if os.path.exists(example):
        with open(example, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CLIENTS


def score(c):
    return TIER_BASE.get(c.get("tier", "L2"), 20) + min(int(c.get("days_since_action", 0)), 14) \
        + (10 if c.get("paid_status") and "待定" not in c.get("paid_status") and int(c.get("days_since_action", 0)) >= 7 else 0)


def message(c):
    tier = c.get("tier", "L2")
    days = int(c.get("days_since_action", 0))
    name = c["id"]
    if days >= 7 and tier in ("L1", "L2"):
        return f"{name}，你做好了再来找我。"  # 断联/不动，不追单
    if tier == "L1":
        return (f"{name}，这个方向要先验证。你把这3个（目标客户/案例）列给我，"
                f"我看看能不能做；列不出来就先放着。")
    if tier == "L3":
        return (f"{name}，你的问题不在{c.get('blocker', '流量')}，在结构。"
                f"我帮你拆一页利润结构，你约20分钟，拆完你再决定。")
    action = c.get("next_action", "把上次说好的任务做完")
    return f"{name}，你上次说确定做{c.get('direction', '这个方向')}，现在只差一件事：{action}。做完发我。"


def classify(c):
    days = int(c.get("days_since_action", 0))
    tier = c.get("tier", "L2")
    if tier == "L1":
        return "观察中（不主动追）"
    if days >= 7:
        return "立即行动（该动没动）"
    if days >= 3:
        return "需要推一把"
    return "已稳定（暂缓）"


def daily(clients, date):
    print(f"===== 每日跟进计划 · {date} =====")
    ranked = sorted(clients, key=score, reverse=True)
    # 观察中（L1 且 未欠任务）默认不占名额
    pool = [c for c in ranked if not (c["tier"] == "L1" and int(c.get("days_since_action", 0)) < 7)]
    if len(pool) < 3:
        pool = ranked
    picks = pool[:3]
    print("今日最多跟进 3 人（按优先级）：\n")
    for i, c in enumerate(picks, 1):
        print(f"[{i}] {c['id']} | {TIER_NAME.get(c['tier'], c['tier'])} | 分类：{classify(c)}"
              f" | 已{c.get('days_since_action', 0)}天没动 | {c.get('paid_status', '')}")
        print(f"    卡点：{c.get('blocker', '')}")
        print(f"    私信草稿：{message(c)}\n")
    rest = [c for c in ranked if c not in picks]
    if rest:
        print(f"其余 {len(rest)} 人今日不动：{', '.join(c['id'] for c in rest)}（不追第二遍）")


def weekly(clients):
    print("===== 每周漏斗周报 =====")
    tiers = {}
    for c in clients:
        tiers.setdefault(c["tier"], []).append(c)
    print("\n漏斗分布：")
    for t in ("L1", "L2", "L3"):
        group = tiers.get(t, [])
        print(f"  {TIER_NAME.get(t, t)}：{len(group)} 人"
              + (f"（{'、'.join(c['id'] for c in group)}）" if group else ""))
    unpaid = [c for c in clients if "已付" not in c.get("paid_status", "")]
    print(f"  未付款：{len(unpaid)} 人" + (f"（{'、'.join(c['id'] for c in unpaid)}）" if unpaid else ""))
    print("\n该动没动（本周主攻名单）：")
    hot = [c for c in clients if classify(c) == "立即行动（该动没动）"]
    if hot:
        for c in hot:
            print(f"  {c['id']}：{c.get('blocker', '')} → 下个动作：{c.get('next_action', '')}")
    else:
        print("  无。全员在动或已稳定。")
    print("\n周报建议：")
    print("  1) 逐层核对付费状态（防止混淆 600/9.9/补差价）。")
    print("  2) 每个客户输出：状态 + 下一个动作。")
    print("  3) 本周主攻名单为上面列出的该动没动者，每天最多挑 3 个跟进。")


def main():
    ap = argparse.ArgumentParser(description="ip-peipao-9clients 跟进自动化")
    ap.add_argument("--clients", help="客户 JSON 文件路径")
    ap.add_argument("--weekly", action="store_true", help="输出每周漏斗周报")
    ap.add_argument("--date", default="今日", help="日期（默认今日）")
    ap.add_argument("--note", help="把一条跟进经验/记录追加到学习日志（如回复情况、话术效果）")
    args = ap.parse_args()
    clients = load_clients(args.clients)
    if not clients:
        print("错误：没有客户数据。请提供 --clients 文件或确认 clients.json 存在。")
        sys.exit(1)
    if args.weekly:
        weekly(clients)
    else:
        daily(clients, args.date)
    log_learn(args.date, args.note)


if __name__ == "__main__":
    main()
