---
name: obsidian-helper
description: Obsidian笔记助手 - 通过API创建/搜索/组织Obsidian笔记，支持双向链接、标签管理、图谱分析和每日笔记自动化
metadata: {"openclaw": {"requires": {"python": []}, "install": []}}
tags: [obsidian, notes, markdown, knowledge, vault, productivity, daily-notes, graph]
version: 1.0.0
author: laosi
source: adapted
---

# Obsidian Helper - Obsidian笔记助手

> 激活词: Obsidian / 笔记 / 知识库 / 双向链接

## 工作原理

通过操作Obsidian vault中的Markdown文件实现笔记管理。无需插件，直接读写`.md`文件。

## 功能

### 1. 创建笔记

```bash
# 在 vault 中创建新笔记
echo "---\ntags: [idea, project]\ncreated: $(date)\n---\n\n# 新笔记\n\n正文内容" > vault/ideas/新笔记.md
```

### 2. 每日笔记

```python
import os
from datetime import datetime

VAULT = r"D:\Obsidian\main-vault"
today = datetime.now().strftime("%Y-%m-%d")
path = os.path.join(VAULT, "Daily", f"{today}.md")

if not os.path.exists(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"""---
created: {today}
tags: [daily]
---

# {today}

## 今日待办

- [ ] 

## 笔记

## 反思
""")
    print(f"Created daily note: {path}")
```

### 3. 全文搜索

```python
import os, re

VAULT = r"D:\Obsidian\main-vault"

def search_notes(query: str, vault: str = VAULT):
    results = []
    for root, _, files in os.walk(vault):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                    if query.lower() in content.lower():
                        results.append((path, content.count(query)))
    results.sort(key=lambda x: -x[1])
    return results

matches = search_notes("机器学习")
for path, count in matches[:10]:
    print(f"{count} hits: {path}")
```

### 4. 标签管理

```python
import os, re

VAULT = r"D:\Obsidian\main-vault"

def get_all_tags(vault: str = VAULT):
    tags = {}
    for root, _, files in os.walk(vault):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    for m in re.finditer(r"#(\w[\w-]*)", fh.read()):
                        tag = m.group(1)
                        if tag not in ["obsidian"]:
                            tags[tag] = tags.get(tag, 0) + 1
    return sorted(tags.items(), key=lambda x: -x[1])

for tag, count in get_all_tags():
    print(f"#{tag}: {count} notes")
```

### 5. 双向链接检测

```python
import os, re

VAULT = r"D:\Obsidian\main-vault"

def find_backlinks(target: str, vault: str = VAULT):
    backlinks = []
    pattern = re.escape(f"[[{target}]]")
    for root, _, files in os.walk(vault):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    if re.search(pattern, fh.read()):
                        backlinks.append(path)
    return backlinks

links = find_backlinks("机器学习")
for l in links:
    print(f"  ← {l}")
```

### 6. 图谱数据导出

```python
import os, re, json

VAULT = r"D:\Obsidian\main-vault"

def export_graph(vault: str = VAULT, output: str = "graph.json"):
    nodes, edges = [], []
    notes = [f.replace(".md", "") for f in os.listdir(vault) if f.endswith(".md")]
    for note in notes:
        path = os.path.join(vault, f"{note}.md")
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            links = re.findall(r"\[\[([^\]]+)\]\]", content)
            for link in links:
                clean = link.split("|")[0].strip()
                if clean in notes:
                    edges.append({"source": note, "target": clean})
            nodes.append({"id": note, "group": 1})
    with open(output, "w") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False)
    print(f"Exported {len(nodes)} nodes, {len(edges)} edges to {output}")

export_graph()
```

## 使用场景

1. **知识管理**: Zettelkasten笔记法，原子笔记+双向链接
2. **每日笔记**: 自动创建模板化日记，记录待办和反思
3. **关系探索**: 导出图谱数据，发现知识间隐藏关联
4. **写作辅助**: 跨笔记引用，构建长篇内容大纲
5. **标签审计**: 清理冗余标签，统一标签体系

## 配置

```yaml
vault_path: "D:\\Obsidian\\main-vault"
daily_notes_dir: "Daily"
templates_dir: "Templates"
default_tags: [daily, auto]
```

## 依赖

- Python 3.8+
- 本地 Obsidian vault
