#!/usr/bin/env python3
"""
技能评估系统 - 自动评估和改进 skills
参考 Hermes Agent 的技能自我改进机制
"""

import os
import json
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path.home() / "self-improving" / "skills"
EVAL_LOG = SKILLS_DIR / "evaluation_log.json"

def load_evaluation_log():
    """加载评估日志"""
    if EVAL_LOG.exists():
        with open(EVAL_LOG) as f:
            return json.load(f)
    return {"evaluations": [], "improvements": []}

def save_evaluation_log(log):
    """保存评估日志"""
    with open(EVAL_LOG, "w") as f:
        json.dump(log, f, indent=2)

def evaluate_skill(skill_name, rating, feedback=None):
    """评估 skill"""
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        return {"error": f"Skill {skill_name} not found"}
    
    # 读取 meta
    meta_file = skill_dir / "_meta.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
    else:
        meta = {"name": skill_name}
    
    # 更新评估
    if "evaluations" not in meta:
        meta["evaluations"] = []
    
    evaluation = {
        "rating": rating,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    meta["evaluations"].append(evaluation)
    
    # 计算平均分
    ratings = [e["rating"] for e in meta["evaluations"]]
    meta["avg_rating"] = sum(ratings) / len(ratings)
    meta["usage_count"] = len(ratings)
    
    # 保存 meta
    with open(meta_file, "w") as f:
        json.dump(meta, f, indent=2)
    
    # 记录到日志
    log = load_evaluation_log()
    log["evaluations"].append({
        "skill": skill_name,
        "rating": rating,
        "timestamp": evaluation["timestamp"]
    })
    
    # 检查是否需要改进
    needs_improvement = rating < 3 or meta["avg_rating"] < 3.5
    
    result = {
        "skill": skill_name,
        "rating": rating,
        "avg_rating": meta["avg_rating"],
        "needs_improvement": needs_improvement,
        "usage_count": meta["usage_count"]
    }
    
    if needs_improvement:
        result["suggestion"] = f"考虑改进 {skill_name}，当前评分 {meta['avg_rating']:.1f}"
    
    save_evaluation_log(log)
    return result

def auto_improve_skill(skill_name, improvement_notes):
    """自动改进 skill"""
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_file.exists():
        return {"error": f"Skill file not found"}
    
    # 读取现有内容
    with open(skill_file) as f:
        content = f.read()
    
    # 添加改进记录
    timestamp = datetime.now().strftime("%Y-%m-%d")
    improvement_entry = f"""
## 改进记录
- {timestamp}: {improvement_notes}
"""
    
    # 添加到文件末尾
    new_content = content + improvement_entry
    
    # 保存
    with open(skill_file, "w") as f:
        f.write(new_content)
    
    # 更新 meta
    meta_file = SKILLS_DIR / skill_name / "_meta.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
    else:
        meta = {"name": skill_name}
    
    if "improvements" not in meta:
        meta["improvements"] = []
    meta["improvements"].append({
        "timestamp": timestamp,
        "notes": improvement_notes
    })
    
    with open(meta_file, "w") as f:
        json.dump(meta, f, indent=2)
    
    # 记录到日志
    log = load_evaluation_log()
    log["improvements"].append({
        "skill": skill_name,
        "notes": improvement_notes,
        "timestamp": timestamp
    })
    save_evaluation_log(log)
    
    return {"status": "improved", "skill": skill_name}

def get_skill_stats():
    """获取所有 skills 的统计"""
    if not SKILLS_DIR.exists():
        return {}
    
    stats = {}
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        
        meta_file = skill_dir / "_meta.json"
        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
            stats[skill_dir.name] = {
                "usage_count": meta.get("usage_count", 0),
                "avg_rating": meta.get("avg_rating"),
                "needs_improvement": meta.get("needs_improvement", False),
                "improvements_count": len(meta.get("improvements", []))
            }
        else:
            stats[skill_dir.name] = {"usage_count": 0}
    
    return stats

def suggest_improvements(skill_name):
    """基于评估历史建议改进"""
    meta_file = SKILLS_DIR / skill_name / "_meta.json"
    if not meta_file.exists():
        return {"error": "Skill not found"}
    
    with open(meta_file) as f:
        meta = json.load(f)
    
    evaluations = meta.get("evaluations", [])
    if not evaluations:
        return {"message": "暂无评估数据"}
    
    # 分析低分评价
    low_ratings = [e for e in evaluations if e["rating"] < 3]
    if not low_ratings:
        return {"message": "评分良好，无需改进"}
    
    # 生成建议
    suggestions = []
    for eval in low_ratings:
        if eval.get("feedback"):
            suggestions.append(eval["feedback"])
    
    return {
        "skill": skill_name,
        "low_rating_count": len(low_ratings),
        "suggestions": suggestions[:3]
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="技能评估系统")
    parser.add_argument("--evaluate", type=str, help="评估 skill: name,rating")
    parser.add_argument("--improve", type=str, help="改进 skill: name,notes")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--suggest", type=str, help="建议改进")
    
    args = parser.parse_args()
    
    if args.evaluate:
        parts = args.evaluate.split(",")
        name, rating = parts[0], int(parts[1])
        feedback = parts[2] if len(parts) > 2 else None
        result = evaluate_skill(name, rating, feedback)
        print(json.dumps(result, indent=2))
    
    elif args.improve:
        parts = args.improve.split(",", 1)
        name, notes = parts[0], parts[1]
        result = auto_improve_skill(name, notes)
        print(json.dumps(result, indent=2))
    
    elif args.stats:
        stats = get_skill_stats()
        print(json.dumps(stats, indent=2))
    
    elif args.suggest:
        result = suggest_improvements(args.suggest)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
