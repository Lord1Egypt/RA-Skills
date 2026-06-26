---
name: junyi-client-followup
description: 儿童成长规划月度跟进工具（客户版）。定时发送复盘问卷、收集家长反馈、格式化整理后转发给规划师。不做评估、不做策略调整、不改报告。覆盖 0-8 岁。触发词：月度跟进、成长复盘、followup、跟进一下孩子、复盘一下、发问卷。不处理：出规划、评估进展、修改报告、医学诊断。
---

# junyi-client-followup

月度跟进问卷收集器。定时提醒家长填写复盘问卷，收集反馈后整理转发给规划师（君一）。

## Core Rules

1. **只收集，不评估。** 不对家长反馈做任何分析、评分、策略调整。
2. **不碰报告。** 不读取、不修改规划报告文档内容。
3. **幂等设计。** 按 plan_id + 年月去重，同月不重复发送问卷。
4. 隐私规则：不在群聊中展示孩子信息，memory/ 只写匿名 ID + 状态。
5. 语气温暖友好，不制造焦虑。

### memory/ 写入白名单

只允许写入：child_uid、plan_id、status、state、followup_count、最近跟进日期。
禁止写入：孩子姓名、家长原话、评估细节。

## Exit Conditions

- 找不到 plan_meta 或 status ≠ active → 告知用户需先联系规划师生成规划
- followup_count ≥ 12 → 提醒：规划已跟进满一年，建议联系规划师评估续期
- 连续 3 月未回复 → 通知规划师
- 孩子超龄（0-3 岁超 36 月龄 / 3-8 岁超 8 岁）→ 提醒联系规划师评估新阶段

## 高风险红线

家长反馈中出现以下情况时，不做常规整理，立即通知规划师：
- 明显退行（已有能力消失）
- 极端情绪问题（持续暴怒、自伤倾向）
- 校园安全事件
- 家庭重大变故

处理方式：state → flagged，立即发消息给规划师，附上家长原文。

## 配置

安装时需在 openclaw.json 中配置：

```json
{
  "skills": {
    "entries": {
      "junyi-client-followup": {
        "env": {
          "PLANNER_CONTACT": "规划师联系方式（飞书 open_id 或其他）"
        }
      }
    }
  }
}
```

## Workflow

### Mode: send-checkin

触发：cron 每月 1 号 / 手动说"发跟进问卷"
前置：state 必须为 idle

1. 读取规划文档末尾的 plan_meta
2. 检查 Exit Conditions
3. 根据 age 判断年龄段：
   - age_months 存在 → 0-3 岁问卷
   - age_years 存在 → 3-8 岁问卷
4. 读取 `references/client-questionnaire.md` 获取对应问卷模板
5. 填充变量（孩子姓名、月份、年龄）
6. 发送问卷给家长
7. 更新 plan_meta：state → sent，current_cycle += 1

### Mode: collect-reply

触发：收到家长回复 / 手动说"处理跟进回复"
前置：state 必须为 sent 或 reminded

1. 读取家长回复原文
2. 高风险红线检测（读取 `references/client-rules.md`）
   - 命中红线 → state → flagged，立即通知规划师，附原文
   - 未命中 → 继续
3. 格式化整理（不分析、不评价）：
   ```
   📋 {孩子姓名} {YYYY年M月} 月度反馈
   ──────────────────
   孩子年龄：{X岁Y个月}
   plan_id：{plan_id}
   跟进次数：第 {N} 次
   ──────────────────
   【家长反馈原文】
   {整理后的反馈，保持原意，分条列出}
   ──────────────────
   ⏰ 请规划师评估后更新规划文档
   ```
4. 将整理好的反馈发送给规划师（PLANNER_CONTACT）
5. 更新 plan_meta：state → idle，last_followup → 当前年月，followup_count += 1
6. 回复家长："收到你的反馈，已转给规划师，评估后会给你更新建议 ☺️"

## 未回复处理

- 发送后 7 天未回复 → 发一次温和提醒，state → reminded
- 提醒后仍未回复 → state → skipped，通知规划师"{孩子} 本月未回复"

## Read References When Needed

- 问卷模板：`references/client-questionnaire.md`
- 跟进规则：`references/client-rules.md`
