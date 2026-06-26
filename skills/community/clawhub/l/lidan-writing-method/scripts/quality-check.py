#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
李诞写作心法 - 质量检查清单
用于检验文章是否符合七步框架的质量标准
"""

import re
from typing import List, Dict, Tuple

# ============= 质量检查清单 =============

QUALITY_CHECKS = [
    {
        "id": 1,
        "question": "开场三句话，读者会不会继续往下读？",
        "check_type": "opening_hook",
        "description": "检查开场是否用具体场景而非抽象定义",
        "criteria": [
            "✓ 包含具体场景描述（时间、地点、人物）",
            "✓ 使用'你'称呼，制造代入感",
            "✓ 提出核心问题而非直接给答案",
            "✗ 避免'本文将探讨'等学术腔",
            "✗ 避免直接下定义"
        ]
    },
    {
        "id": 2,
        "question": "错误答案，读者会不会觉得'我之前也这么想'？",
        "check_type": "wrong_answers",
        "description": "检查是否列出 2-3 种常见误解并给出反例",
        "criteria": [
            "✓ 列出至少 2 种常见错误解释",
            "✓ 每种错误都有致死反例",
            "✓ 反例具体、有杀伤力",
            "✗ 避免温和的反驳",
            "✗ 避免'学术界有不同看法'等回避表述"
        ]
    },
    {
        "id": 3,
        "question": "正确答案，读者能不能给别人讲明白？",
        "check_type": "core_insight",
        "description": "检查本质洞察是否一句话能说清",
        "criteria": [
            "✓ 有一句话本质定义",
            "✓ 有具体例子支撑",
            "✓ 逻辑链条完整",
            "✗ 避免堆砌术语",
            "✗ 避免模糊表述"
        ]
    },
    {
        "id": 4,
        "question": "触类旁通，读者会不会觉得'原来这么多领域都相关'？",
        "check_type": "cross_domain",
        "description": "检查是否在 4-5 个不同领域验证观点",
        "criteria": [
            "✓ 覆盖 4-5 个不同领域",
            "✓ 每个领域有具体案例",
            "✓ 领域之间有差异性",
            "✓ 每个案例都有洞察总结",
            "✗ 避免领域过于相似",
            "✗ 避免只有观点没有例子"
        ]
    },
    {
        "id": 5,
        "question": "结尾，读者会不会有'值了'的感觉？",
        "check_type": "closing",
        "description": "检查是否回到开场场景并给出更深洞察",
        "criteria": [
            "✓ 回到开场场景，形成闭环",
            "✓ 给出更深层洞察",
            "✓ 有可执行的建议",
            "✓ 不说教，留有重量",
            "✗ 避免'所以我们应该'等说教",
            "✗ 避免简单总结重复"
        ]
    }
]

# ============= 结构检查 =============

STRUCTURE_CHECKS = {
    "paragraph_count": {
        "name": "段落数量",
        "target": "6-8 个主要段落",
        "description": "检查文章是否有清晰的段落划分"
    },
    "word_count": {
        "name": "总字数",
        "target": "4000-6000 字",
        "description": "检查文章长度是否适中"
    },
    "no_framework_titles": {
        "name": "无框架标题",
        "target": "不出现'开场故事'、'错误答案'等标题",
        "description": "检查是否隐藏了框架结构"
    },
    "data_points": {
        "name": "数据对比",
        "target": "至少 2-3 组数据对比",
        "description": "检查是否有数据作为转折点"
    },
    "book_recommendations": {
        "name": "延伸阅读",
        "target": "10 本书，分 3 级",
        "description": "检查是否有分级书单（入门 3/进阶 4/学术 3）"
    }
}

# ============= 文风检查 =============

STYLE_CHECKS = {
    "use_you": {
        "name": "用'你'称呼",
        "pattern": r"你",
        "min_count": 10,
        "description": "检查是否用'你'拉近与读者距离"
    },
    "no_academic_tone": {
        "name": "无学术腔",
        "forbidden": ["本文将探讨", "笔者认为", "综上所述", "由此可见"],
        "description": "检查是否避免学术腔调"
    },
    "no_jargon": {
        "name": "无术语堆砌",
        "forbidden": ["在 xx 现象学原理中", "从 xx 理论来看", "根据 xx 模型"],
        "description": "检查是否避免术语堆砌"
    },
    "story_elements": {
        "name": "故事元素",
        "pattern": r"场景 | 例子 | 案例 | 故事",
        "min_count": 5,
        "description": "检查是否有足够的故事和案例"
    }
}

# ============= 检查函数 =============

def check_opening_hook(text: str) -> Tuple[bool, str]:
    """检查开场是否有吸引力"""
    lines = text.strip().split('\n')
    if len(lines) < 3:
        return False, "开场太短，需要至少 3 句话"
    
    opening = '\n'.join(lines[:5])
    
    # 检查是否有具体场景
    scene_keywords = ["场景", "你", "有没有", "遇到", "坐在", "站在", "看着"]
    has_scene = any(kw in opening for kw in scene_keywords)
    
    # 检查是否避免学术腔
    academic_phrases = ["本文将", "本文探讨", "笔者", "综上所述"]
    has_academic = any(phrase in opening for phrase in academic_phrases)
    
    if not has_scene:
        return False, "开场缺少具体场景描述"
    if has_academic:
        return False, "开场有学术腔调"
    
    return True, "开场有吸引力"


def check_wrong_answers(text: str) -> Tuple[bool, str]:
    """检查是否有错误答案部分"""
    # 查找反驳/转折的表达
    counter_patterns = ["但", "但是", "然而", "其实不对", "问题是", "反例"]
    counter_count = sum(text.count(p) for p in counter_patterns)
    
    if counter_count < 3:
        return False, "缺少足够的反驳和反例（至少 3 处转折）"
    
    # 检查是否有常见误解的列举
    misconception_patterns = ["有人", "常见", "以为", "认为", "听起来"]
    has_misconception = any(p in text for p in misconception_patterns)
    
    if not has_misconception:
        return False, "没有列举常见误解"
    
    return True, f"错误答案部分完整（{counter_count}处转折）"


def check_core_insight(text: str) -> Tuple[bool, str]:
    """检查核心洞察是否清晰"""
    # 查找本质定义的表达
    insight_patterns = ["本质", "其实", "就是", "核心", "关键在于"]
    has_insight = any(p in text for p in insight_patterns)
    
    if not has_insight:
        return False, "缺少本质洞察的表达"
    
    # 检查是否有例子支撑
    example_patterns = ["比如", "例如", "举个例子", "就像"]
    example_count = sum(text.count(p) for p in example_patterns)
    
    if example_count < 2:
        return False, "核心洞察缺少例子支撑（至少 2 个例子）"
    
    return True, f"核心洞察清晰（{example_count}个例子支撑）"


def check_cross_domain(text: str) -> Tuple[bool, str]:
    """检查跨领域验证"""
    domains = ["商业", "职场", "历史", "文化", "艺术", "科技", "生活", "教育", "医疗"]
    found_domains = [d for d in domains if d in text]
    
    if len(found_domains) < 4:
        return False, f"跨领域不足（仅{len(found_domains)}个领域，需要 4-5 个）"
    
    return True, f"跨领域验证充分（{len(found_domains)}个领域：{', '.join(found_domains)}）"


def check_closing(text: str) -> Tuple[bool, str]:
    """检查结尾是否升华"""
    lines = text.strip().split('\n')
    closing = '\n'.join(lines[-10:])  # 最后 10 行
    
    # 检查是否回到开场
    closing_keywords = ["回到", "现在", "下次", "可以"]
    has_return = any(kw in closing for kw in closing_keywords)
    
    # 检查是否避免说教
    preachy_phrases = ["所以我们应该", "因此必须", "希望大家", "让我们"]
    is_preachy = any(phrase in closing for phrase in preachy_phrases)
    
    if not has_return:
        return False, "结尾没有回到开场场景或给出行动建议"
    if is_preachy:
        return False, "结尾有说教语气"
    
    return True, "结尾有升华且不说教"


def check_no_framework_titles(text: str) -> Tuple[bool, str]:
    """检查是否隐藏了框架标题"""
    forbidden_titles = [
        "开场故事", "错误答案", "正确答案", "触类旁通",
        "对比制造", "结尾升华", "延伸阅读", "七步", "框架"
    ]
    
    found_titles = [t for t in forbidden_titles if t in text]
    
    if found_titles:
        return False, f"出现框架标题：{', '.join(found_titles)}"
    
    return True, "框架标题已隐藏"


def check_data_points(text: str) -> Tuple[bool, str]:
    """检查数据对比"""
    # 查找数字和百分比
    import re
    numbers = re.findall(r'\d+[\.%]', text)
    
    if len(numbers) < 3:
        return False, f"数据点不足（仅{len(numbers)}个，需要至少 3 个）"
    
    return True, f"数据充分（{len(numbers)}个数据点）"


def check_book_recommendations(text: str) -> Tuple[bool, str]:
    """检查延伸阅读书单"""
    # 查找书名号
    import re
    books = re.findall(r'[《](.*?)[》]', text)
    
    if len(books) < 8:
        return False, f"推荐书籍不足（仅{len(books)}本，需要 8-10 本）"
    
    # 检查是否有分级
    level_keywords = ["入门", "进阶", "初级", "高级", "学术"]
    has_levels = any(kw in text for kw in level_keywords)
    
    if not has_levels:
        return False, "书籍推荐没有分级"
    
    return True, f"推荐{len(books)}本书，{'已' if has_levels else '未'}分级"


# ============= 主检查函数 =============

def run_quality_check(text: str) -> Dict:
    """运行完整的质量检查"""
    results = {
        "overall_pass": True,
        "checks": [],
        "suggestions": []
    }
    
    # 五大核心问题检查
    checks = [
        ("开场吸引力", check_opening_hook),
        ("错误答案", check_wrong_answers),
        ("核心洞察", check_core_insight),
        ("跨领域验证", check_cross_domain),
        ("结尾升华", check_closing),
        ("框架标题隐藏", check_no_framework_titles),
        ("数据对比", check_data_points),
        ("书籍推荐", check_book_recommendations),
    ]
    
    for name, check_func in checks:
        passed, message = check_func(text)
        results["checks"].append({
            "name": name,
            "passed": passed,
            "message": message
        })
        if not passed:
            results["overall_pass"] = False
            results["suggestions"].append(f"【{name}】{message}")
    
    # 字数统计
    word_count = len(text)
    results["word_count"] = word_count
    if word_count < 3000:
        results["suggestions"].append(f"【字数】{word_count}字，建议扩展到 4000-6000 字")
    elif word_count > 8000:
        results["suggestions"].append(f"【字数】{word_count}字，建议精简到 6000 字以内")
    
    return results


def print_check_report(results: Dict) -> str:
    """打印检查报告"""
    report = []
    report.append("=" * 60)
    report.append("📋 李诞写作心法 - 质量检查报告")
    report.append("=" * 60)
    report.append("")
    
    # 总体结果
    status = "✅ 通过" if results["overall_pass"] else "❌ 需改进"
    report.append(f"总体状态：{status}")
    report.append(f"文章字数：{results.get('word_count', 0)}字")
    report.append("")
    
    # 详细检查
    report.append("详细检查：")
    report.append("-" * 60)
    for check in results["checks"]:
        icon = "✅" if check["passed"] else "❌"
        report.append(f"{icon} {check['name']}: {check['message']}")
    
    # 改进建议
    if results["suggestions"]:
        report.append("")
        report.append("改进建议：")
        report.append("-" * 60)
        for i, suggestion in enumerate(results["suggestions"], 1):
            report.append(f"{i}. {suggestion}")
    
    report.append("")
    report.append("=" * 60)
    
    return '\n'.join(report)


# ============= CLI 入口 =============

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python quality-check.py <文章文件路径>")
        print("示例：python quality-check.py article.md")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        results = run_quality_check(text)
        report = print_check_report(results)
        print(report)
        
    except FileNotFoundError:
        print(f"错误：文件不存在 - {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)
