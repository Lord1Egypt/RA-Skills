#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
learner.py — 通用自进化学习模块（任意 WorkBuddy 技能可调用）。

设计目标：让每个技能都能"越用越好用、越用越高效"。
它不依赖任何业务知识，完全技能无关，只负责：
  1. 记录每次使用（能力、成功/失败、错误类型、备注）
  2. 记录用户偏好
  3. 累计洞察（高频能力、反复出现的错误）
  4. 自动复盘（错误达阈值给改进建议，操作达阈值做优化分析）

用法（在技能的 scripts/ 目录下，或由任意目录调用并传入技能目录）:
  python learner.py init    <skill_dir>            # 初始化 learned_patterns.json
  python learner.py record  <skill_dir> --capability <能力名> [--fail] [--error <类型>] [--note <文本>]
  python learner.py prefer  <skill_dir> --key <键> --val <值>
  python learner.py insight <skill_dir>            # 打印累计洞察
  python learner.py reflect <skill_dir>            # 复盘并给出改进建议
"""
import os, sys, json, argparse, datetime

THRESHOLD_ERROR = 3    # 同一错误出现次数达到此值 -> 建议加预检/兜底
THRESHOLD_OPS   = 10   # 操作总数达到此值 -> 进入高频/低频优化分析

def resolve_skill_dir(arg):
    """支持传文件夹绝对路径，或技能名（在 ~/.workbuddy/skills 下）。"""
    if os.path.isdir(arg):
        return arg
    alt = os.path.join(os.path.expanduser("~/.workbuddy/skills"), arg)
    if os.path.isdir(alt):
        return alt
    return arg

def learn_path(skill_dir):
    return os.path.join(skill_dir, "learned_patterns.json")

def default_data(skill_name=""):
    return {
        "version": 1,
        "skill": skill_name,
        "totalOps": 0,
        "totalErrors": 0,
        "capabilityStats": {},   # 能力名 -> {count, success, fail}
        "errorPatterns": {},     # 错误类型 -> {count, lastNote, lastTime}
        "preferences": {},       # 用户偏好 key->value
        "recentOps": [],         # 最近 20 条操作
        "optimizations": {},     # 已采纳的优化
        "lastUpdated": ""
    }

def load_learning(skill_dir):
    p = learn_path(skill_dir)
    try:
        return json.loads(open(p, encoding="utf-8").read())
    except Exception:
        return default_data(os.path.basename(skill_dir))

def save_learning(skill_dir, data):
    data["lastUpdated"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    p = learn_path(skill_dir)
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))

def record_op(skill_dir, capability, success=True, error=None, note=None):
    data = load_learning(skill_dir)
    data["totalOps"] += 1
    cap = data["capabilityStats"].setdefault(capability, {"count": 0, "success": 0, "fail": 0})
    cap["count"] += 1
    if success:
        cap["success"] += 1
    else:
        cap["fail"] += 1
        data["totalErrors"] += 1
    if error:
        ep = data["errorPatterns"].setdefault(error, {"count": 0, "lastNote": "", "lastTime": ""})
        ep["count"] += 1
        ep["lastNote"] = note or ""
        ep["lastTime"] = data["lastUpdated"] or datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    rec = {"t": data["lastUpdated"], "cap": capability, "ok": success, "err": error, "note": note}
    data["recentOps"].append(rec)
    data["recentOps"] = data["recentOps"][-20:]
    save_learning(skill_dir, data)
    return data

def record_preference(skill_dir, key, value):
    data = load_learning(skill_dir)
    data["preferences"][key] = value
    save_learning(skill_dir, data)
    return data

def get_insights(skill_dir):
    data = load_learning(skill_dir)
    caps = sorted(data["capabilityStats"].items(), key=lambda kv: kv[1]["count"], reverse=True)
    errors = sorted(data["errorPatterns"].items(), key=lambda kv: kv[1]["count"], reverse=True)
    return {
        "totalOps": data["totalOps"],
        "topCapabilities": [(k, v["count"]) for k, v in caps[:5]],
        "recurringErrors": [(k, v["count"]) for k, v in errors[:5]],
        "preferences": data["preferences"],
    }

def self_reflect(skill_dir):
    data = load_learning(skill_dir)
    suggestions = []
    for err, info in data["errorPatterns"].items():
        if info["count"] >= THRESHOLD_ERROR:
            suggestions.append(
                f"⚠️ 错误「{err}」已出现 {info['count']} 次，建议增加预检/兜底步骤，"
                f"并将经验回写本技能 SKILL.md（lastNote: {info.get('lastNote','')}）"
            )
    if data["totalOps"] >= THRESHOLD_OPS:
        caps = data["capabilityStats"]
        top = max(caps.items(), key=lambda kv: kv[1]["count"]) if caps else None
        if top:
            suggestions.append(f"📈 最常用能力：「{top[0]}」({top[1]['count']} 次)，优先打磨其示例与输出质量")
        low = [k for k, v in caps.items() if v["count"] <= 1]
        if low:
            suggestions.append(f"🧹 低频能力：{', '.join(low)}，可评估是否精简或合并进高频能力")
    return suggestions

def main():
    ap = argparse.ArgumentParser(description="通用自进化学习模块")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init");   p_init.add_argument("skill_dir")
    p_rec  = sub.add_parser("record"); p_rec.add_argument("skill_dir")
    p_rec.add_argument("--capability", required=True); p_rec.add_argument("--fail", action="store_true")
    p_rec.add_argument("--error"); p_rec.add_argument("--note")
    p_pre  = sub.add_parser("prefer"); p_pre.add_argument("skill_dir")
    p_pre.add_argument("--key", required=True); p_pre.add_argument("--val", required=True)
    p_ins  = sub.add_parser("insight"); p_ins.add_argument("skill_dir")
    p_ref  = sub.add_parser("reflect"); p_ref.add_argument("skill_dir")

    args = ap.parse_args()
    sd = resolve_skill_dir(args.skill_dir)

    if args.cmd == "init":
        if os.path.exists(learn_path(sd)):
            print("已存在 learned_patterns.json，跳过")
            return
        save_learning(sd, default_data(os.path.basename(sd)))
        print("✅ 已初始化", learn_path(sd))
    elif args.cmd == "record":
        data = record_op(sd, args.capability, success=not args.fail, error=args.error, note=args.note)
        print(f"✅ 已记录 (totalOps={data['totalOps']}, errors={data['totalErrors']})")
    elif args.cmd == "prefer":
        record_preference(sd, args.key, args.val)
        print("✅ 已记录偏好")
    elif args.cmd == "insight":
        print(json.dumps(get_insights(sd), indent=2, ensure_ascii=False))
    elif args.cmd == "reflect":
        sgs = self_reflect(sd)
        print("\n".join(sgs) if sgs else "暂无明显改进点，继续积累数据。")

if __name__ == "__main__":
    main()
