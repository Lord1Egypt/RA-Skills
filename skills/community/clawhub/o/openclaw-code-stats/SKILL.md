---
name: code-stats
description: 分析代码仓库的统计信息（行数、文件数，语言分布）。用于了解项目规模和复杂度。当需要了解项目有多大、有多少代码时使用。
---

# Code Stats

分析当前工作区的代码统计信息。

## 使用方法

```bash
node skills/code-stats/index.js
```

或者在 OpenClaw 中作为技能使用。

## 功能特性

- **总文件数统计** - 统计项目中的所有代码文件
- **总行数统计** - 统计代码总行数
- **语言分布** - 按编程语言分类统计
- **百分比计算** - 计算各语言占比

## 支持的语言

- JavaScript / TypeScript
- Python
- JSON / YAML
- Markdown
- Shell / Bash
- HTML / CSS

## 示例输出

```
📊 Code Stats for /home/duan/.openclaw/workspace
========================================
Total Files: 408
Total Lines: 68,095

By Language:
  JavaScript: 176 files, 36,983 lines (54.3%)
  Markdown: 100 files, 16,365 lines (24.0%)
  TypeScript: 17 files, 2,359 lines (3.5%)
  Python: 3 files, 1,195 lines (1.8%)
```

## 使用场景

1. 了解项目规模
2. 评估代码复杂度
3. 统计各语言占比
4. 定期跟踪代码量变化
