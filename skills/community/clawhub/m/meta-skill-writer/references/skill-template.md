# SKILL.md 模板（含注释）

```markdown
---
name: my-skill                    # kebab-case，与目录名一致
version: "1.0.0"                  # 语义化版本
description: "一句话描述。以'当用户...'开头，包含触发关键词，不讲步骤。"
homepage: https://...              # 可选：项目主页
metadata:                         # 可选：OpenClaw 元数据
  {
    "openclaw":
      {
        "emoji": "🔧",            # 显示用 emoji
        "requires": { "bins": ["curl"] },  # 必需的二进制依赖
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl (brew)",
            },
          ],
      },
  }
---

# Skill 名称 — 一句话用途

（可选：1-2 句补充说明，不重复 description）

## 首次设置（如果没有就删掉这节）

### 1. 获取 XX
### 2. 配置环境变量
### 3. 检查依赖

## 工作流

### Step 1：读什么、拿什么
### Step 2：做什么
### Step 3：输出什么

### 边界情况

- 输入为空时：...
- API 返回错误时：...
- 依赖缺失时：...

## 输出格式

（写明输出的结构，方便 Agent 和用户预期对齐）

## 注意事项

- 安全相关：什么不能做
- 性能相关：什么很慢
- 合规相关：什么需要用户确认
```

## 脚本模板（Python）

```python
#!/usr/bin/env python3
"""脚本用途说明"""

import sys
import json

def main():
    # 1. 读取输入
    # 2. 执行核心逻辑
    # 3. 输出结果
    pass

if __name__ == "__main__":
    sys.exit(main())
```

## 脚本模板（Bash）

```bash
#!/bin/bash
# 脚本用途说明

INPUT="$1"
if [ -z "$INPUT" ]; then
    echo "用法: $0 <input>"
    exit 1
fi

# 核心逻辑
# 输出结果
```
