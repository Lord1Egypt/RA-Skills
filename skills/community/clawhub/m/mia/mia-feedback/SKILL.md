# MIA Feedback Skill

## 概述

MIA Feedback 是一个轻量级的反馈收集器，用于收集用户对答案质量的反馈。

## 职责

- 收集用户反馈（good/bad）
- 存储反馈记录
- 支持反馈查询
- **仅针对全新问题收集反馈**

## 使用方式

### 命令行调用

```bash
# 存储反馈
node mia-feedback.mjs store "问题" "答案" "good"

# 列出反馈
node mia-feedback.mjs list [数量]
```

### 环境变量

- `MIA_FEEDBACK_FILE`: 反馈文件路径（默认：./feedback.jsonl）

### 输出格式

```json
{
  "success": true,
  "record": {
    "timestamp": "2026-03-15T...",
    "question": "...",
    "result": "...",
    "label": "good"
  }
}
```

## 架构位置

```
[OpenClaw 执行者生成答案]
    ↓
判断：全新问题？
    ├─ 是 → [MIA Feedback] ← 收集反馈
    └─ 否 → 跳过（不打扰用户）
    ↓
[反馈文件]
```

## 注意事项

- 本 Skill **不生成 Plan，不执行搜索，不管理记忆**
- 只负责收集和存储用户反馈
- **智能判断：仅对全新问题收集反馈**
- 所有配置通过环境变量传入，无硬编码
