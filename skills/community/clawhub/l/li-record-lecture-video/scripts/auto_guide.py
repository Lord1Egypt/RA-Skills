# -*- coding: utf-8 -*-
"""
可复用学习指引生成器 v2.0.2
支持课程主题 profile，Agent 只需定义关键词匹配规则，无需每次重写脚本。
"""

# ═══════════════════════════════════════════════════════════
# 通用框架
# ═══════════════════════════════════════════════════════════

def build_guide_map(videos, rules, fallback=None):
    """
    根据规则列表为所有视频生成学习指引映射。
    
    参数:
      videos    — [(title, mins), ...]
      rules     — [(pattern_fn, (goal, verify, content)), ...]
                  pattern_fn(title) 返回 True/False
      fallback  — 兜底三元组，默认通用指引
    
    返回: {title: (goal, verify, content)}
    """
    if fallback is None:
        fallback = ('掌握本节核心知识点', '能复述关键概念', '视频讲解内容')

    guide = {}
    for title, _ in videos:
        matched = False
        for pattern_fn, triple in rules:
            if pattern_fn(str(title)):
                guide[title] = triple
                matched = True
                break
        if not matched:
            guide[title] = fallback

    # 覆盖率报告
    matched = sum(1 for v in guide.values() if v != fallback)
    missing = sum(1 for v in guide.values() if v == fallback)
    if missing > 0:
        print(f"[GUIDE] 匹配: {matched}/{len(videos)}, 兜底: {missing}")
    else:
        print(f"[GUIDE] 全部匹配: {matched}/{len(videos)}")

    return guide


# ═══════════════════════════════════════════════════════════
# 内置课程主题 Profile（示例，Agent 可在对话中动态扩展）
# ═══════════════════════════════════════════════════════════

def make_simple_rule(keyword, goal, verify, content):
    """快捷创建单关键词规则"""
    def fn(title):
        return keyword.lower() in str(title).lower()
    return (fn, (goal, verify, content))


def make_multi_rule(keywords, goal, verify, content):
    """创建多关键词规则（全部匹配）"""
    def fn(title):
        t = str(title).lower()
        return all(k.lower() in t for k in keywords)
    return (fn, (goal, verify, content))


def make_any_rule(keywords, goal, verify, content):
    """创建多关键词规则（任一匹配）"""
    def fn(title):
        t = str(title).lower()
        return any(k.lower() in t for k in keywords)
    return (fn, (goal, verify, content))


# 常用规则模板（Agent 可直接使用）
COMMON_RULES = {
    'course_intro': make_multi_rule(
        ['课程', '介绍'],
        '了解课程体系、讲师背景和学习目标',
        '明确课程整体框架和学习路径',
        '课程大纲介绍、学习资料说明、考试要求'
    ),
    'course_summary': make_any_rule(
        ['总结', '回顾', '复习'],
        '回顾全课程核心内容与知识体系',
        '能绘制课程知识框架图',
        '课程总结、重点回顾、考试提示'
    ),
    'exercise': make_any_rule(
        ['练习', '思考题', '习题'],
        '通过练习巩固所学知识',
        '正确率达标（建议≥80%）',
        '章节练习题、常见考点总结'
    ),
}

# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════

def validate_coverage(guide, videos):
    """验证覆盖率，返回缺失列表"""
    missing = []
    for title, _ in videos:
        if title not in guide or guide[title][0].startswith('掌握本节核心'):
            missing.append(title)
    return missing


def print_coverage_report(guide, videos):
    """打印覆盖率报告"""
    total = len(videos)
    missing = validate_coverage(guide, videos)
    matched = total - len(missing)
    print(f"学习指引覆盖率: {matched}/{total} ({matched*100//total if total else 0}%)")
    if missing:
        print(f"  以下 {len(missing)} 个视频使用兜底指引:")
        for t in missing[:5]:
            print(f"    - {t}")
        if len(missing) > 5:
            print(f"    ... 还有 {len(missing)-5} 个")
    else:
        print("  ✅ 全部视频都有专属学习指引")
