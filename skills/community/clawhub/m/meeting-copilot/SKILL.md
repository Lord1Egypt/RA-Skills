---
name: meeting-copilot
description: 会议运营 Copilot — 支持会前 briefing 生成、会中结构化纪要整理、会后待办追踪与 follow-up 草稿。面向需要系统性管理会议全生命周期的职场人士。提供 boss mode（向上汇报视角）和 executor mode（向下追踪视角）两种输出格式。⚠️ 不提供实时语音转录、日历集成或自动提醒。
---

# Meeting Ops Copilot

会议全生命周期辅助，覆盖：会前 briefing → 会中纪要结构化整理 → 会后待办追踪与 follow-up 草稿。支持 boss / executor 两种模式输出。

## Overview

本 skill 帮助用户系统性管理会议全生命周期：

- **会前**：基于议程和背景生成 briefing 材料，供主持或主讲人快速进入状态
- **会中**：将散乱的讨论内容整理为结构化纪要（讨论要点 / 决议 / 待办含负责人）
- **会后**：从纪要中提取待办清单和 follow-up 草稿邮件/消息

**⚠️ 免责声明**：本工具不提供实时语音转录、不接入日历、不发送通知。其输出依赖用户输入的原始信息，质量受限于输入完整性。

## When to Use This Skill

- 需要在会议前快速准备 briefing
- 会议中或会议后需要整理出结构化纪要
- 需要从纪要中生成待办追踪列表
- 需要向老板（boss mode）或下属（executor mode）发送 follow-up 邮件/消息草稿

## Workflow

### Mode 1: boss mode（向上汇报视角）

输出重点：结论先行、决策清晰、风险可见。

```
输入：会议主题 + 议程 + 背景要点（或原始讨论文本）
↓ 识别关键决议、支撑理由、潜在风险
↓ 输出：Boss-friendly Briefing（结论 + 要点 + 风险 + 建议行动）
```

### Mode 2: executor mode（向下追踪视角）

输出重点：任务明确、责任到人、时间清楚。

```
输入：会议纪要 / 讨论要点 / 决议
↓ 提取待办事项（含负责人 / 截止 / 优先级）
↓ 输出：结构化待办列表 + follow-up 草稿
```

## Input

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task` | string | ✅ | 任务类型：`briefing` / `minutes` / `followup` |
| `meeting_topic` | string | ✅ | 会议主题 |
| `meeting_date` | string | ✅ | 会议日期 YYYY-MM-DD |
| `mode` | string | ✅ | `boss` 或 `executor` |
| `agenda` | string | 条件必填 | 议程要点，多条用 `\|` 分隔（briefing 必填） |
| `raw_text` | string | 条件必填 | 原始讨论文本（minutes 必填） |
| `decisions` | string | 可选 | 已决事项，多条用 `\|` 分隔 |
| `participants` | string | 可选 | 参与者列表，多人用 `\|` 分隔 |

## Output

### briefing（boss mode）

```json
{
  "status": "success",
  "task": "briefing",
  "mode": "boss",
  "meeting_topic": "...",
  "meeting_date": "...",
  "sections": {
    "conclusion": "一句话结论",
    "key_points": ["要点1", "要点2"],
    "decisions_needed": ["待决策事项"],
    "risks": ["风险1", "风险2"],
    "suggested_actions": ["建议行动1"]
  },
  "briefing_text": "格式化 briefing 文本"
}
```

### minutes（executor mode）

```json
{
  "status": "success",
  "task": "minutes",
  "mode": "executor",
  "meeting_topic": "...",
  "meeting_date": "...",
  "minutes": {
    "discussion_points": ["讨论点1", "讨论点2"],
    "decisions": ["决议1"],
    "action_items": [
      {"task": "任务描述", "owner": "负责人", "deadline": "YYYY-MM-DD", "priority": "high|medium|low"}
    ]
  },
  "minutes_text": "格式化纪要文本"
}
```

### followup

```json
{
  "status": "success",
  "task": "followup",
  "mode": "boss|executor",
  "meeting_topic": "...",
  "followup_items": [...],
  "draft_email": "邮件草稿文本",
  "draft_message": "简短消息草稿"
}
```

## Safety & Disclaimer

- ⚠️ 本 skill 不接入日历系统，不发送通知，不进行实时语音转录
- ⚠️ 输出的完整性和准确性依赖用户输入的原始信息，不做信息真实性担保
- ⚠️ 本工具是辅助参考，不替代专业会议记录人员或法律/合规审查
- 如涉及重大决策，请结合实际情况自行判断或咨询专业人士

## Constraints

- ❌ 不提供实时语音转录
- ❌ 不接入日历（Google Calendar、钉钉日历等）
- ❌ 不自动发送通知或邮件（仅生成草稿）
- ❌ 不做会议录音存储

## Examples

### 会前 Briefing（boss mode）

**输入**：
```
task: briefing
meeting_topic: Q2 产品规划评审
meeting_date: 2026-04-05
mode: boss
agenda: Q2目标对齐|技术方案选型|资源评估
participants: 产品经理|研发负责人|设计负责人
```

**输出**：Boss-friendly briefing，包含结论先行的核心要点 + 风险 + 建议行动。

### 会中纪要整理（executor mode）

**输入**：
```
task: minutes
meeting_topic: 周例会
meeting_date: 2026-03-31
mode: executor
raw_text: 讨论了A功能延期的风险；决定启用备选方案；张三分头对接供应商；李四负责测试
decisions: 启用备选方案
participants: 张三|李四|王五
```

**输出**：结构化纪要 + 提取的待办（含负责人）。

### 会后 Follow-up（executor mode）

**输入**：
```
task: followup
meeting_topic: 周例会
mode: executor
decisions: 启用备选方案
（action_items from minutes output）
```

**输出**：待办追踪列表 + 邮件/消息草稿。

## Acceptance Criteria

- [ ] 支持 `briefing` / `minutes` / `followup` 三种 task
- [ ] 支持 `boss` / `executor` 两种 mode
- [ ] briefing 输出包含 conclusion / key_points / risks / suggested_actions
- [ ] minutes 输出包含 discussion_points / decisions / action_items（含 owner/deadline/priority）
- [ ] followup 输出包含结构化待办列表 + 邮件草稿 + 消息草稿
- [ ] handler.py 带 `if __name__ == "__main__":` 自测分支，直接 `python3 handler.py` 可跑
- [ ] skill.json / .claw/identity.json / tests/test_handler.py 齐全
- [ ] 免责声明完整呈现于输出和文档中
