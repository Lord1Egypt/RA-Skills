#!/usr/bin/env python3
"""从 data/ 目录生成 llms-full.txt"""
import os
import re

DATA_DIR = os.path.expanduser("~/.claude/skills/java-design-patterns/data")
OUTPUT = os.path.expanduser("~/.claude/skills/java-design-patterns/llms-full.txt")

# 分类顺序
CATEGORY_ORDER = [
    ("creational", "Creational 创建型模式"),
    ("structural", "Structural 结构型模式"),
    ("behavioral", "Behavioral 行为型模式"),
    ("architectural", "Architectural 架构模式"),
    ("concurrency", "Concurrency 并发模式"),
    ("data-access", "Data Access 数据访问模式"),
    ("functional", "Functional 函数式模式"),
    ("integration", "Integration 集成模式"),
    ("resilience", "Resilience 弹性模式"),
    ("testing", "Testing 测试模式"),
    ("messaging", "Messaging 消息模式"),
    ("performance-optimization", "Performance Optimization 性能优化模式"),
    ("resource-management", "Resource Management 资源管理模式"),
    ("idiom", "Idiom 惯用法模式"),
    ("service-discovery", "Service Discovery 服务发现模式"),
]

# 读取分类映射
mapping = {}
with open(os.path.join(DATA_DIR, "category-mapping.txt")) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        cat, slug = line.split("|", 1)
        mapping[slug] = cat

# 中文名映射（从 SKILL.md 提取的关键模式）
ZH_NAMES = {
    "abstract-factory": "抽象工厂", "builder": "建造者", "factory-method": "工厂方法",
    "prototype": "原型", "singleton": "单例", "adapter": "适配器", "bridge": "桥接",
    "composite": "组合", "decorator": "装饰器", "facade": "外观", "flyweight": "享元",
    "proxy": "代理", "chain-of-responsibility": "责任链", "command": "命令",
    "interpreter": "解释器", "iterator": "迭代器", "mediator": "中介者",
    "memento": "备忘录", "observer": "观察者", "state": "状态", "strategy": "策略",
    "template-method": "模板方法", "visitor": "访问者", "mvc": "MVC", "mvp": "MVP",
    "mvvm": "MVVM", "factory": "工厂", "dependency-injection": "依赖注入",
    "object-pool": "对象池", "value-object": "值对象", "null-object": "空对象",
}

def clean_markdown(content, slug, url):
    """清理和格式化 markdown 内容"""
    lines = content.split('\n')
    cleaned = []

    # 跳过 "Skip to main content" 行
    skip_main = True
    for line in lines:
        if skip_main and ('Skip to main content' in line or line.strip().startswith('[Skip')):
            skip_main = False
            continue
        skip_main = False
        # 清理 URL 中的转义反斜杠
        line = line.replace('\\#', '#')
        cleaned.append(line)

    result = '\n'.join(cleaned).strip()

    # 添加模式标题头
    title_match = re.search(r'^# (.+?) Pattern in Java', result, re.MULTILINE)
    display_name = title_match.group(1) if title_match else slug.replace('-', ' ').title()

    zh_name = ZH_NAMES.get(slug, '')
    zh_suffix = f" {zh_name}" if zh_name else ""

    header = f"## [{mapping.get(slug, 'unknown')}/{slug}] {display_name}{zh_suffix}\n"
    header += f"> 官方文档: {url}\n\n"

    # 移除原页面 h1 标题（因为我们已经添加了 ## header）
    result = re.sub(r'^# .+?\n\n', '', result, count=1)

    return header + result

# 生成 llms-full.txt
with open(OUTPUT, 'w', encoding='utf-8') as out:
    out.write("# Java 设计模式完整参考文档\n\n")
    out.write("> 来源: https://java-design-patterns.com/\n")
    out.write("> 生成日期: 2026-06-25\n")
    out.write(f"> 总模式数: {len(mapping)}\n")
    out.write("> 语言: 英文原文 + 简体中文标注\n\n")
    out.write("---\n\n")

    total = 0
    for cat_dir, cat_name in CATEGORY_ORDER:
        # 找出该分类下的所有 slug
        slugs = sorted([s for s, c in mapping.items() if c == cat_dir])
        if not slugs:
            continue

        out.write(f"<!-- ============================================ -->\n")
        out.write(f"<!-- {cat_name} ({len(slugs)} 个) -->\n")
        out.write(f"<!-- ============================================ -->\n\n")

        for slug in slugs:
            filepath = os.path.join(DATA_DIR, f"{slug}.md")
            if not os.path.exists(filepath):
                print(f"  WARN: missing {slug}.md")
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            url = f"https://java-design-patterns.com/patterns/{slug}/"
            formatted = clean_markdown(content, slug, url)
            out.write(formatted)
            out.write("\n\n---\n\n")
            total += 1

print(f"Generated: {OUTPUT}")
print(f"Patterns: {total}")
print(f"Lines: {sum(1 for _ in open(OUTPUT)):,}")
