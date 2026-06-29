#!/usr/bin/env python3
"""处理设计原则页面，生成 reference 文件并更新 llms-full.txt"""
import os
import re

DATA_DIR = os.path.expanduser("~/.claude/skills/java-design-patterns/data")
REFS_DIR = os.path.expanduser("~/.claude/skills/java-design-patterns/references/principles")
LLMS_FULL = os.path.expanduser("~/.claude/skills/java-design-patterns/llms-full.txt")
os.makedirs(REFS_DIR, exist_ok=True)

# 原则定义: slug, display_name, zh_name, 关键词匹配
PRINCIPLES = [
    ("kiss", "KISS", "保持简单", "## [KISS]"),
    ("yagni", "YAGNI", "你不会需要它", "## [YAGNI]"),
    ("do-the-simplest-thing", "Do The Simplest Thing That Could Possibly Work", "做最简单可行的事", "## [Do The Simplest Thing]"),
    ("separation-of-concerns", "Separation of Concerns", "关注点分离", "## [Separation of Concerns]"),
    ("dry", "DRY (Don't Repeat Yourself)", "不要重复自己", "## [Keep things DRY]"),
    ("code-for-the-maintainer", "Code For The Maintainer", "为维护者编码", "## [Code For The Maintainer]"),
    ("avoid-premature-optimization", "Avoid Premature Optimization", "避免过早优化", "## [Avoid Premature Optimization]"),
    ("minimise-coupling", "Minimise Coupling", "最小化耦合", "## [Minimise Coupling]"),
    ("law-of-demeter", "Law of Demeter", "迪米特法则", "## [Law of Demeter]"),
    ("composition-over-inheritance", "Composition Over Inheritance", "组合优于继承", "## [Composition Over Inheritance]"),
    ("orthogonality", "Orthogonality", "正交性", "## [Orthogonality]"),
    ("robustness-principle", "Robustness Principle", "健壮性原则", "## [Robustness Principle]"),
    ("inversion-of-control", "Inversion of Control", "控制反转", "## [Inversion of Control]"),
    ("maximise-cohesion", "Maximise Cohesion", "最大化内聚", "## [Maximise Cohesion]"),
    ("liskov-substitution-principle", "Liskov Substitution Principle (LSP)", "里氏替换原则", "## [Liskov Substitution Principle]"),
    ("open-closed-principle", "Open/Closed Principle (OCP)", "开闭原则", "## [Open/Closed Principle]"),
    ("single-responsibility-principle", "Single Responsibility Principle (SRP)", "单一职责原则", "## [Single Responsibility Principle]"),
    ("hide-implementation-details", "Hide Implementation Details", "隐藏实现细节", "## [Hide Implementation Details]"),
    ("curlys-law", "Curly's Law", "科里定律", "## [Curly's Law]"),
    ("encapsulate-what-changes", "Encapsulate What Changes", "封装变化", "## [Encapsulate What Changes]"),
    ("interface-segregation-principle", "Interface Segregation Principle (ISP)", "接口隔离原则", "## [Interface Segregation Principle]"),
    ("boy-scout-rule", "Boy-Scout Rule", "童子军规则", "## [Boy-Scout Rule]"),
    ("command-query-separation", "Command Query Separation (CQS)", "命令查询分离", "## [Command Query Separation]"),
    ("murphys-law", "Murphy's Law", "墨菲定律", "## [Murphy's Law]"),
    ("brooks-law", "Brooks's Law", "布鲁克斯定律", "## [Brooks's Law]"),
    ("linus-law", "Linus's Law", "林纳斯定律", "## [Linus's Law]"),
]

# 读取原始 principles 数据
src_file = os.path.join(DATA_DIR, "principles.md")
if not os.path.exists(src_file):
    print(f"ERROR: {src_file} not found. Save the principles page first.")
    print("Use: opencli web read --url https://java-design-patterns.com/principles/ --stdout > data/principles.md")
    exit(1)

with open(src_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 清理 Skip to main content
content = re.sub(r'\[Skip to main content\]\([^)]+\)\n\n', '', content)

# 提取标题后的内容
intro_match = re.match(r'^# .+?\n\n(.+?)\n\n## ', content, re.DOTALL)
intro = intro_match.group(1).strip() if intro_match else ""

# 为每个原则提取内容
principle_contents = {}
for i, (slug, display_name, zh_name, marker) in enumerate(PRINCIPLES):
    # 找到该原则的起始位置
    start_pattern = re.escape(marker)
    start_match = re.search(start_pattern, content)
    if not start_match:
        print(f"  WARN: not found {slug}")
        continue

    start_pos = start_match.start()

    # 找到下一个原则的起始位置
    next_pos = len(content)
    for _, _, _, next_marker in PRINCIPLES[i+1:]:
        nm = re.search(re.escape(next_marker), content)
        if nm and nm.start() > start_pos:
            next_pos = nm.start()
            break

    section = content[start_pos:next_pos].strip()
    principle_contents[slug] = (display_name, zh_name, section)

print(f"Extracted {len(principle_contents)} principles")

# 生成 reference 文件
for slug, (display_name, zh_name, section) in principle_contents.items():
    # 清理内容
    cleaned = section.replace('\\#', '#')

    # 提取描述
    desc_match = re.search(r'## \[.+?\]\([^)]+\)\n\n(.+?)(?:\n\n|$)', cleaned, re.DOTALL)
    desc = desc_match.group(1).strip()[:200] if desc_match else f"{display_name} 设计原则"

    frontmatter = f"""---
name: "{slug}"
description: "{display_name} {zh_name} -- 软件设计原则。{desc}"
url: "https://java-design-patterns.com/principles/#{slug.replace('-', '')}"
category: "principles"
tags: [design-principle]
---

# {display_name} {zh_name}原则

> 官方文档: https://java-design-patterns.com/principles/
> 分类: 设计原则 (Principles)

{cleaned}
"""

    ref_path = os.path.join(REFS_DIR, f"{slug}.md")
    with open(ref_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

print(f"Generated {len(principle_contents)} reference files in references/principles/")

# 更新 llms-full.txt - 追加设计原则部分
principles_section = """
---

<!-- ============================================ -->
<!-- 设计原则 (Design Principles) — """ + f"{len(principle_contents)} 个" + """ -->
<!-- ============================================ -->

"""

for slug, (display_name, zh_name, section) in principle_contents.items():
    cleaned = section.replace('\\#', '#')
    # 移除原来的 ## [...] anchor 标题
    cleaned = re.sub(r'^## \[.+?\]\([^)]+\)\n\n', '', cleaned, count=1)
    principles_section += f"## [principles/{slug}] {display_name} {zh_name}\n"
    principles_section += f"> 官方文档: https://java-design-patterns.com/principles/\n\n"
    principles_section += cleaned + "\n\n---\n\n"

with open(LLMS_FULL, 'a', encoding='utf-8') as f:
    f.write(principles_section)

print(f"Appended principles to llms-full.txt")

# 统计
total_lines = sum(1 for _ in open(LLMS_FULL))
print(f"llms-full.txt total: {total_lines:,} lines")
print(f"reference files: {len(os.listdir(REFS_DIR))} in references/principles/")
