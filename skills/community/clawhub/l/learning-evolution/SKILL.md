---
name: learning-evolution
version: 1.0.3
description: Create evidence-based learning reviews for skills — analyze usage patterns, track effectiveness, and plan evolutions. Use when planning skill improvements from real usage data, user feedback, and observed outcomes. Generates local Markdown templates with data integrity guardrails.
---

# Learning Evolution

## 🚀 First-Success Path (30秒上手)

**分析一个 skill 的使用情况：**
```bash
./scripts/analyze-usage.sh --skill my-skill --period 30d
```

**评估效果：**
```bash
./scripts/track-effectiveness.sh --skill my-skill --since 2024-01-01
```

三步即用：运行分析 → 填入验证数据 → 生成改进提案。

## Sample Prompts（输入→输出示例）

### Sample 1: 分析 Skill 使用模式

**用户输入：**
```
帮我分析一下 insight-tracker 过去30天的使用情况
```

**Expected Output：**
> 📊 使用分析报告：insight-tracker (过去30天)
> ---------
> ⏱ **分析周期：** 2026-05-17 ~ 2026-06-16
>
> **总使用次数：** [待填写 - 从使用日志获取]
> **完成率：** [待填写 - 从用户反馈或日志获取]
>
> **主要使用场景：**
> 1. 记录洞察（约占总使用60%）
> 2. 搜索已有洞察（约25%）
> 3. 归档/清理（约15%）
>
> **可能的 drop-off 点：**
> - [待确认] 用户在"添加标签"步骤可能停滞
> - [待确认] 搜索功能使用率低于预期
>
> ⚠️ 以上数据字段为模板占位符，请在填入验证数据后再用于决策。

### Sample 2: 评估 Skill 有效性

**用户输入：**
```
评估 health-checkup-report 从发布以来的效果
```

**Expected Output：**
> 📈 效果评估报告：health-checkup-report
> ---------
> **评估周期：** 2026-01-01 ~ 2026-06-16
>
> **成功信号（来自用户反馈或日志）：**
> - [待填写] 用户完成解读率
> - [待填写] 用户"有用"反馈占比
>
> **错误分析：**
> - [待填写] 解读中的常见错误类型
> - [待填写] 用户修正请求频率
>
> **用户反馈摘要：**
> - [待填写 - 从直接用户反馈获取]
>
> **整体判断：** [待填写 - 需要足够证据支持]
>
> ⚠️ 所有指标需有可验证来源，避免基于猜测做修改决策。

### Sample 3: 提出改进建议

**用户输入：**
```
基于最近的使用数据，insight-tracker 可以做哪些改进？
```

**Expected Output：**
> 💡 改进提案：insight-tracker
> ---------
> **数据依据：** [待填写 - 需要有验证数据或反馈支撑]
>
> | 候选改进 | 预期收益 | 实现成本 | 证据置信度 |
> |---------|---------|---------|-----------|
> | [待评估] 增加批量导入 | 降低记录门槛 | 中 | [待填写] |
> | [待评估] 改进搜索算法 | 提高检索效率 | 高 | [待填写] |
> | [待评估] 标签自动建议 | 提升标签一致性 | 低 | [待填写] |
>
> **推荐的下一步：** [待填写 - 需人工确认后再执行]
>
> ⚠️ 候选改进仅为初步建议，所有改动需经过人工审核后才能实施。

### Sample 4: 版本对比分析

**用户输入：**
```
对比 freshippo v1.0 和 v2.0 的使用差异
```

**Expected Output：**
> 📊 版本对比分析：freshippo v1.0 → v2.0
> ---------
> **主要变化：** 增加了浏览器自动化支持
>
> **指标对比（需要验证数据）：**
> | 指标 | v1.0 | v2.0 | 变化 |
> |------|------|------|------|
> | 月使用次数 | [待填] | [待填] | - |
> | 用户保留率 | [待填] | [待填] | - |
> | 任务完成率 | [待填] | [待填] | - |
>
> **用户反馈对比：**
> - [待填写]
>
> **结论：** [待填写]

### Sample 5: 发现使用模式

**用户输入：**
```
看看 learning-evolution 自己的使用数据，有没有有意思的模式
```

**Expected Output：**
> 🔍 元分析：learning-evolution 使用模式
> ---------
> **使用频率：** [待填写]
> **最常用命令：** [待填写]
> **闲置率：** [待填写]（脚本生成模板后用户是否实际填写）
>
> **值得关注的模式：**
> - [待确认] 生成模板后很少有人填写验证数据
> - [待确认] analyze-usage 使用率高于 track-effectiveness
>
> **建议行动：**
> 1. [待确认] 是否需要简化数据填写流程
> 2. [待确认] 脚本输出是否应该包含更多引导性问题

## Overview

Use this skill to structure evidence-based learning reviews for OpenClaw skills. It creates local Markdown templates for usage analysis, effectiveness review, and evolution planning. The bundled scripts leave analytics, confidence scores, outcomes, and user feedback blank until you fill them from verified logs, direct feedback, or observed outcomes.

## When to Use

- Reviewing real usage patterns for a skill
- Turning user feedback into improvement candidates
- Tracking whether a published change improved outcomes
- Planning a skill update with an explicit human review gate
- Avoiding changes based only on guesses or anecdotal impressions

## Data Rules

- Do not treat blank template fields as measured facts.
- Do not invent usage, satisfaction, completion, or error metrics.
- Keep sensitive user feedback out of persisted reports unless retention is intentional.
- Verify the source of every metric before using it to change a published skill.
- Require human review before applying recommendations generated from reports.

## Churn Diagnosis Workflow

When a skill has usage but weak retention, diagnose before recommending delisting.

1. **Classify the failure mode**
   - Demand problem: few qualified users or unclear trigger.
   - Discovery problem: good skill, poor name/description/examples.
   - First-success problem: user cannot reach a useful output quickly.
   - Quality problem: useful category, but answers are vague, unsafe, or not workflow-shaped.
   - Trust/safety problem: unclear data, payment, account, or write boundaries.
2. **Collect evidence**
   - Usage/download/install deltas, direct feedback, maintainer reports, eval failures, and concrete session examples.
   - Mark every field as verified, inferred, or missing.
3. **Choose action**
   - Upgrade when demand exists and churn points to quality or first-success gaps.
   - Rename/reposition when trigger or description is the likely problem.
   - Delist only when demand is absent, unsafe behavior is intrinsic, or maintenance cost is unjustified.
4. **Validation plan**
   - Add 3-5 proxy eval prompts that represent the churn failure.
   - Define what a better answer must include and what it must avoid.
   - Recheck after publish using the same evidence fields.

Preferred output:

```text
Diagnosis: <demand | discovery | first-success | quality | trust/safety>
Evidence: <verified / inferred / missing>
Recommended action: <upgrade | rename | reposition | delist>
Upgrade target: <workflow, examples, safety boundary, eval>
Validation: <proxy cases + post-publish signal>
```

## Commands

### Analyze Usage Patterns

```bash
./scripts/analyze-usage.sh --skill <name> --period 30d
```

Creates `data/USAGE-<skill>-YYYYMMDD.md` with fields for verified usage counts, completion signals, drop-off points, and evidence-backed insights.

### Track Effectiveness

```bash
./scripts/track-effectiveness.sh --skill <name> --since 2024-01-01
```

Creates `data/EFFECTIVENESS-<skill>-YYYYMMDD.md` with fields for verified success metrics, error analysis, and review notes.

### Suggest Evolutions

```bash
./scripts/suggest-evolutions.sh --skill <name> --min-confidence 0.7
```

Creates `data/EVOLUTIONS-<skill>-YYYYMMDD.md` with an evidence checklist and candidate table. It does not assign confidence values automatically.

## Input

Use real evidence such as:

- Skill usage logs
- User feedback and ratings
- Reproducible error reports
- Success or failure outcomes
- Version comparison notes
- Manual review observations

## Output

The scripts create local Markdown templates under `data/` or `LEARNING_DATA_DIR`:

- Usage analysis template
- Effectiveness review template
- Evolution planning template

Each output includes a data policy reminder so agents and users do not confuse unfilled fields with measured analytics.

## Review Workflow

1. Run the relevant script to create a dated template.
2. Fill in only verified facts and cite the source of each metric.
3. Mark unknown values as `TODO` until evidence exists.
4. Decide whether the evidence supports an incremental fix, a larger evolution, a pivot, or no change.
5. Review the proposed change with a human before modifying or publishing another skill.

## Safety Notes

- Scripts validate `--skill` before using it in report filenames.
- Scripts write only local Markdown files.
- Scripts do not access the network, read credentials, or modify other skills.
- `LEARNING_DATA_DIR` can redirect report output; check it before running if you need a specific destination.

## 真实任务示例

| 场景 | 用户会说 | Skill 执行 |
|------|---------|-----------|
| 使用分析 | "这个skill最近用得怎么样" | 运行analyze-usage → 生成模板 → 引导填写验证数据 |
| 效果评估 | "发布的改进有效果吗" | 运行track-effectiveness → 对比前后数据 → 提供证据判断 |
| 改进规划 | "接下来该改什么" | 运行suggest-evolutions → 列出候选 → 要求人工审核 |
| 版本对比 | "新版本和老版本比怎么样" | 跨版本数据分析 → 对比关键指标 → 提出调整建议 |
| 元分析 | "自己的使用模式有什么问题" | 检查自身使用数据 → 发现改进空间 → 自引用改进建议 |
