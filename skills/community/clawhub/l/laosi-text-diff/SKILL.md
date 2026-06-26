---
name: text-diff
version: 1.0.0
description: 文本对比 - 对比两段文本差异，逐行diff，高亮变更，支持side-by-side和unified格式输出
tags: [diff, text, compare, development, code-review]
author: laosi
source: original
---

# Text Diff - 文本对比工具

> 激活词: 对比 / diff / 比较文本 / 找不同

## 功能

- 逐行文本对比 (unified diff)
- 高亮新增/删除/修改行
- Side-by-side视图
- 文件对比
- 统计变更信息
- 忽略空白差异

## Python 实现

```python
import difflib, json, os
from datetime import datetime
from typing import List, Tuple, Dict

class TextDiff:
    def __init__(self):
        self.results: list = []
    
    def diff(self, old_text: str, new_text: str, context: int = 3) -> dict:
        """对比两段文本"""
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)
        
        # Unified diff
        unified = list(difflib.unified_diff(
            old_lines, new_lines,
            fromfile="old", tofile="new",
            lineterm="", n=context
        ))
        
        # 计算统计
        added = [l[1:].rstrip() for l in unified if l.startswith("+") and not l.startswith("+++")]
        removed = [l[1:].rstrip() for l in unified if l.startswith("-") and not l.startswith("---")]
        
        # Side-by-side
        sbs = list(difflib.ndiff(old_lines, new_lines))
        left = [l[2:].rstrip() for l in sbs if l.startswith("- ") or l.startswith("  ")]
        right = [l[2:].rstrip() for l in sbs if l.startswith("+ ") or l.startswith("  ")]
        
        result = {
            "unified": "".join(unified),
            "side_by_side": {"old": left, "new": right},
            "stats": {
                "old_lines": len(old_lines),
                "new_lines": len(new_lines),
                "added": len(added),
                "removed": len(removed),
                "changed": max(len(added), len(removed)),
                "similarity": self._similarity(old_lines, new_lines),
            },
            "added_lines": added,
            "removed_lines": removed,
            "timestamp": datetime.now().isoformat(),
        }
        self.results.append(result)
        return result
    
    def diff_files(self, old_path: str, new_path: str) -> dict:
        """对比两个文件"""
        with open(old_path, encoding="utf-8") as f:
            old = f.read()
        with open(new_path, encoding="utf-8") as f:
            new = f.read()
        
        result = self.diff(old, new)
        result["old_file"] = old_path
        result["new_file"] = new_path
        return result
    
    def _similarity(self, old: list, new: list) -> float:
        """计算相似度百分比"""
        sm = difflib.SequenceMatcher(None, old, new)
        return round(sm.ratio() * 100, 1)
    
    def ignore_whitespace(self, old_text: str, new_text: str) -> dict:
        """忽略空白差异的对比"""
        import re
        def normalize(text):
            return re.sub(r'\s+', ' ', text).strip()
        old_norm = "\n".join(normalize(l) for l in old_text.splitlines())
        new_norm = "\n".join(normalize(l) for l in new_text.splitlines())
        return self.diff(old_norm, new_norm)
    
    def print_side_by_side(self, old_text: str, new_text: str, width: int = 80):
        """并排显示差异"""
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()
        sm = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        half = width // 2 - 2
        print(f"{'OLD':^{half}} | {'NEW':^{half}}")
        print("-" * width)
        
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for line in old_lines[i1:i2]:
                    print(f"{line[:half]:>{half}} | {line[:half]:<{half}}")
            elif tag == "replace":
                for old, new in zip(old_lines[i1:i2], new_lines[j1:j2]):
                    print(f"{old[:half]:>{half}} | {new[:half]:<{half}}")
            elif tag == "delete":
                for line in old_lines[i1:i2]:
                    print(f"{line[:half]:>{half}} | {'':{half}}")
            elif tag == "insert":
                for line in new_lines[j1:j2]:
                    print(f"{'':{half}} | {line[:half]:<{half}}")

# 使用示例
differ = TextDiff()

# 简单对比
old = """def hello():
    print("Hello, World!")
    return True"""

new = """def hello(name: str):
    print(f"Hello, {name}!")
    return True
    # Added comment"""

result = differ.diff(old, new)
print(f"统计: +{result['stats']['added']} -{result['stats']['removed']} (相似度: {result['stats']['similarity']}%)")
print(f"\nUnified Diff:")
print(result["unified"])

# 并排显示
print("\nSide-by-Side:")
differ.print_side_by_side(old, new, width=60)

# 文件对比
# result = differ.diff_files("v1.py", "v2.py")
```

## 输出格式

```
统计: +3 -2 (相似度: 85.7%)

--- old
+++ new
@@ -1,3 +1,4 @@
 def hello():
-    print("Hello, World!")
+    print(f"Hello, {name}!")
     return True
+    # Added comment
```

## 使用场景

1. **代码审查**: 比较PR前后代码差异
2. **配置管理**: 检查配置文件变更
3. **文档更新**: 对比文档修订内容
4. **调试**: 找出程序输出的差异

## 依赖

- Python 3.8+
- 标准库（difflib）
