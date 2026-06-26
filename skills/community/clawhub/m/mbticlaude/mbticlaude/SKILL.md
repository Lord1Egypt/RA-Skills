---
name: mbticlaude
description: 通过分析用户在多个 AI 工具（Claude Code、Codex、Gemini、OpenCode、OpenClaw ）的提示词来推测 MBTI 性格类型
version: 1.0.0
author: xmr
tags: [mbti, personality, analysis, prompts]
---

# MBTIClaude

通过分析用户在多个 AI 工具（Claude Code、Codex、Gemini、OpenCode、OpenClaw）中的提示词来推测 MBTI 性格类型。

## 功能

- 自动提取五种 AI 工具的用户提示词历史
- 分析沟通风格、信息处理方式、决策模式和生活方式
- 基于行为模式推测 MBTI 类型
- 提供详细的特征分析和建议

## 使用方法

```bash
/mbticlaude
```

## 分析维度

### 1. 沟通风格 (E vs I)
- 提示词长度和详细程度
- 社交性表达 vs 任务导向
- 背景说明的丰富程度

### 2. 信息处理 (S vs N)
- 关注具体细节 vs 抽象概念
- 实现导向 vs 概念导向
- 创造性思维的体现

### 3. 决策方式 (T vs F)
- 逻辑性 vs 情感性
- 任务导向 vs 人际关系考虑
- 技术语言 vs 情感表达

### 4. 生活方式 (J vs P)
- 计划性 vs 灵活性
- 结构化 vs 探索性
- 快速迭代 vs 系统规划

## 数据来源

- **Claude Code**: `~/.claude/history.jsonl`
- **Codex**: `~/.codex/history.jsonl`
- **Gemini**: `~/.gemini/tmp/*/chats/*.json`
- **OpenCode**: `~/.local/state/opencode/prompt-history.jsonl`
- **OpenClaw**: `~/.openclaw/agents/*/sessions/*.jsonl`

## 注意事项

⚠️ **重要提醒：**
1. 样本基于工作场景，可能不反映真实性格
2. MBTI 本身科学性存疑，仅供参考
3. 这是基于行为模式的推测，非专业心理测评
4. 需要足够的历史数据才能得出较准确的结论

## 安装

### 使用 npx skills add（推荐）

```bash
npx skills add xmanrui/mbtiClaude
```

### 从 GitHub 手动安装

```bash
curl -fsSL https://raw.githubusercontent.com/xmanrui/mbtiClaude/main/SKILL.md -o ~/.claude/skills/mbticlaude.md
```

## 项目地址

GitHub: https://github.com/xmanrui/mbtiClaude

## 示例输出

```
🔍 正在提取用户提示词...

📊 数据统计：
  Claude Code: 100 条
  Codex: 100 条
  Gemini: 62 条
  OpenCode: 2 条
  OpenClaw: 100 条
  总计: 364 条

🧠 正在分析 MBTI 维度...

==================================================
🎯 你的 MBTI 类型：INTP
==================================================

类型名称：逻辑学家

📋 维度分析：
  I - 内向：简洁高效沟通
  N - 直觉：抽象思维，系统化方案
  T - 思考：纯理性，关注效率
  P - 知觉：灵活探索，快速迭代

⚠️  重要提醒：
  1. 基于工作场景的行为推测，可能不反映真实性格
  2. MBTI 本身科学性存疑，仅供参考
  3. 这是基于行为模式的推测，非专业心理测评
```

## 许可证

MIT
