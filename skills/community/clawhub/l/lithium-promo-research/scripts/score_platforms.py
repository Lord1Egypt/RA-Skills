#!/usr/bin/env python3
"""
锂电设备推广平台评分脚本
根据多维度规则对平台进行评分和分级
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def calculate_score(platform):
    """
    计算平台评分
    
    评分维度：
    - 行业知名度高: +2
    - 受众匹配度高: +2
    - 支持多语言/英语: +1
    - 有明确价格信息: +1
    - 支持中国厂商参展/入驻: +1
    - 有锂电/新能源专区: +2
    """
    score = 0
    reasons = []
    
    # 1. 行业知名度
    influence = platform.get("influence_score", 0)
    if influence >= 8:
        score += 2
        reasons.append("行业知名度高")
    elif influence >= 5:
        score += 1
        reasons.append("行业知名度中等")
    
    # 2. 受众匹配度
    audience = platform.get("audience_type", "")
    if any(kw in audience for kw in ["电池厂", "设备采购商", "制造商", "manufacturer", "buyer"]):
        score += 2
        reasons.append("受众匹配度高")
    
    # 3. 语言支持
    language = platform.get("language", "")
    if any(kw in language for kw in ["英语", "English", "多语言", "中英"]):
        score += 1
        reasons.append("支持英语/多语言")
    
    # 4. 价格信息
    price = platform.get("price_range", "")
    if price and price not in ["", "需询价", "unknown"]:
        score += 1
        reasons.append("有明确价格信息")
    
    # 5. 支持中国厂商
    notes = platform.get("notes", "")
    if any(kw in notes for kw in ["中国", "Chinese", "国际展商", "global"]):
        score += 1
        reasons.append("支持中国厂商")
    
    # 6. 锂电/新能源专区
    if any(kw in notes for kw in ["锂电", "新能源", "battery", "energy storage", "专区"]):
        score += 2
        reasons.append("有锂电/新能源专区")
    
    return score, reasons


def get_grade(score):
    """根据分数确定推荐等级"""
    if score >= 7:
        return "S"
    elif score >= 5:
        return "A"
    elif score >= 3:
        return "B"
    else:
        return "C"


def score_platforms(input_file, output_file=None):
    """对平台数据进行评分"""
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    platforms = data.get("platforms", [])
    
    scored_platforms = []
    for p in platforms:
        score, reasons = calculate_score(p)
        grade = get_grade(score)
        
        p["score"] = score
        p["grade"] = grade
        p["recommend_reason"] = "; ".join(reasons) if reasons else "基础推荐"
        
        scored_platforms.append(p)
    
    # 按分数排序
    scored_platforms.sort(key=lambda x: x["score"], reverse=True)
    
    # 保存
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_platforms": len(scored_platforms),
        "platforms": scored_platforms,
    }
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent.parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"platforms_scored_{timestamp}.json"
    else:
        output_file = Path(output_file)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"评分完成，已保存: {output_file}")
    print(f"共评分 {len(scored_platforms)} 个平台")
    
    # 统计
    grade_stats = {}
    for p in scored_platforms:
        grade = p["grade"]
        grade_stats[grade] = grade_stats.get(grade, 0) + 1
    
    print("\n推荐等级分布:")
    for grade in ["S", "A", "B", "C"]:
        count = grade_stats.get(grade, 0)
        print(f"  {grade}级: {count} 个")
    
    # Top 5
    print("\nTop 5 推荐平台:")
    for i, p in enumerate(scored_platforms[:5], 1):
        print(f"  {i}. [{p['grade']}] {p['platform_name']} ({p['country']}) - 得分: {p['score']}")
        print(f"     理由: {p['recommend_reason']}")
    
    return output_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="推广平台评分")
    parser.add_argument("input", help="输入JSON文件")
    parser.add_argument("--output", default=None, help="输出文件路径")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"错误: 输入文件不存在: {args.input}")
        return 1
    
    score_platforms(args.input, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
