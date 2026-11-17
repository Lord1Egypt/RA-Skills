---
name: jev-code-review
description: |
  Jev 模拟代码评审。用 LLM 模拟 TypeSafe Jev 的三种原语（Choice/Score/Noul），
  对代码变更进行结构化评审，输出概率化判断。
  触发词：评审代码、code review、jev review、代码审查。
---

# Jev Code Review (LLM 模拟版)

用 LLM 模拟 Jev 的决策模型，对代码变更进行**结构化评审**。

## 核心原理

Jev 不是生成文本，而是回答**原子问题**。本 skill 用 LLM 模拟三种原语：

| 原语 | 用途 | 输出格式 |
|------|------|---------|
| **Noul** | 是/否判断 | `{"answer": 0.85}` (0-1 概率) |
| **Score** | 1-5 分打分 | `{"answer": 4, "confidence": 0.72}` |
| **Choice** | 多选一 | `{"answer": "B", "probabilities": {"A": 0.1, "B": 0.7, "C": 0.2}}` |

## 代码评审问题集

对每段代码变更，并行提问 5 个原子问题：

### 1. 安全性 (Noul)
```
问题：这段代码是否引入了安全风险？
- 检查：SQL注入、XSS、硬编码密钥、路径遍历、命令注入
- 输出：概率 0-1（>0.7 = 有风险）
```

### 2. 正确性 (Noul)
```
问题：这段代码是否可能引入 bug？
- 检查：空指针、边界条件、资源泄漏、并发问题、逻辑错误
- 输出：概率 0-1（>0.6 = 可能有问题）
```

### 3. 可维护性 (Score 1-5)
```
问题：代码质量如何？
1 = 难以维护，5 = 优秀
- 检查：命名清晰、函数长度、注释、复杂度
- 输出：分数 + 置信度
```

### 4. 性能 (Score 1-5)
```
问题：是否有性能隐患？
1 = 严重性能问题，5 = 无隐患
- 检查：N+1查询、循环内IO、大数据量处理、内存泄漏
- 输出：分数 + 置信度
```

### 5. 需要人工审查 (Noul)
```
问题：是否需要人工介入审查？
- 触发条件：安全>0.7 或 正确性>0.6 或 可维护性<3
- 输出：概率 0-1
```

## 使用方式

### 命令行
```bash
# 评审单个文件
python3 scripts/jev_review.py --file app.py

# 评审 diff
python3 scripts/jev_review.py --diff changes.diff

# 评审 Git 提交
python3 scripts/jev_review.py --commit HEAD~1

# 输出 JSON（便于集成）
python3 scripts/jev_review.py --file app.py --json
```

### 作为 Skill 调用
用户说"评审这段代码"时：
1. 获取代码变更（文件/diff/commit）
2. 并行调用 5 个原子问题
3. 汇总结果，标记需要人工审查的部分

## 输出示例

```json
{
  "file": "app.py",
  "timestamp": "2026-09-19T21:10:00",
  "review": {
    "security": {
      "type": "noul",
      "question": "这段代码是否引入了安全风险？",
      "answer": 0.15,
      "threshold": 0.7,
      "flagged": false
    },
    "correctness": {
      "type": "noul",
      "question": "这段代码是否可能引入 bug？",
      "answer": 0.45,
      "threshold": 0.6,
      "flagged": false
    },
    "maintainability": {
      "type": "score",
      "question": "代码质量如何？",
      "answer": 3,
      "confidence": 0.68,
      "threshold": 3,
      "flagged": false
    },
    "performance": {
      "type": "score",
      "question": "是否有性能隐患？",
      "answer": 4,
      "confidence": 0.75,
      "threshold": 3,
      "flagged": false
    },
    "needs_human": {
      "type": "noul",
      "question": "是否需要人工介入审查？",
      "answer": 0.12,
      "threshold": 0.5,
      "flagged": false
    }
  },
  "summary": {
    "flagged_count": 0,
    "max_risk": "correctness (0.45)",
    "recommendation": "PASS"
  }
}
```

## 阈值规则

| 指标 | 阈值 | 动作 |
|------|------|------|
| security | >0.7 | 🔴 阻断，必须修复 |
| correctness | >0.6 | 🟡 警告，建议修复 |
| maintainability | <3 | 🟡 警告，建议改进 |
| performance | <3 | 🟡 警告，建议优化 |
| needs_human | >0.5 | 👀 需要人工审查 |

## 与真实 Jev 的对比

| 特性 | LLM 模拟 | 真实 Jev |
|------|---------|---------|
| 延迟 | 2-5秒 | 70-500ms |
| 成本 | ~$0.002/次 | ~$0.0001/次 |
| 校准性 | 中等（依赖 prompt） | 高（RLCD 训练） |
| 确定性 | 低（温度影响） | 高（温度=0） |
| 可用性 | ✅ 现在就能用 | ⏳ 等 API key |

## 后续：切换到真实 Jev

拿到 API key 后：
1. 安装 `pip install typesafe-sdk`
2. 修改 `scripts/jev_review.py` 中的 `call_llm()` 为 `call_jev()`
3. 问题结构完全兼容，无需改动

## 文件结构

```
jev-code-review/
├── SKILL.md              # 本文件
├── scripts/
│   ├── jev_review.py     # 主评审脚本
│   ├── primitives.py     # Noul/Score/Choice 模拟实现
│   └── thresholds.json   # 阈值配置
└── references/
    └── jev_api.md        # 真实 Jev API 文档（待接入）
```
