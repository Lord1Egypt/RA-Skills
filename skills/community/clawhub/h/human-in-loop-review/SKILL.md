---
name: human-in-loop-review
description: |-
  给自主智能体/自动化流水线加一层「人类在环审核」：把中高危、不可逆、外发隐私、提权、支付等
  有副作用的动作路由到人工审核队列，阻止无人值守 agent 越权执行。内置审核分级（needs_review）、
  审核队列（add/pending/approve/reject/summary）、完整审计（提议者/风险/审核人/结论/理由/时间戳）。
  与 safety-guardrails 互补：护栏做 ALLOW/CONFIRM/DENY 决策，本技能把 CONFIRM 类动作转人工队列。
  触发词：人类在环、人工审核、审核队列、审批流、human-in-the-loop、操作确认、越权拦截、agent 审核。
agent_created: true
version: 1.0.0
display_name: "人类在环审核"
display_name_en: "Human-in-the-Loop Review"
description_zh: "把中高危动作路由到人工审核队列，阻止自主 agent 越权"
description_en: "Route risky actions to a human review queue"
visibility: "public"
---

# 人类在环审核（human-in-loop-review）

## 什么时候用
- 自主 agent / 每小时触发的元进化 / 定时任务要执行「有副作用」动作，但没有真人在环兜底。
- 任何删除、写库、外发、提权、安装依赖、上线发布、资金转移、关机重启前的最后一道闸。

## 核心机制
1. **审核分级** `needs_review(action, context)`：对 medium/high/critical 及「不可逆/外发/
   提权/支付」类动作返回 True；已 `user_approved` 的直接放行。
2. **审核队列** `ReviewQueue`：
   - `add(action, proposed_by)` → 返回 review_id，状态 `pending`
   - `pending()` 列出等待项；`get(id)` 查详情
   - `approve(id, reviewer, note)` / `reject(id, reviewer, note)` 落结论
   - 重复审核同一项会被 `ValueError` 拦截（防双签）
3. **完整审计**：每条含 提议者 / 动作 / 风险 / 审核人 / 结论 / 理由 / 时间戳。
4. **摘要** `summary()`：总量 + 按状态/风险分布。

## 用法
```bash
python scripts/human_review.py --selftest

# 提议一个动作入队
python scripts/human_review.py --add '{"action":"delete /var/log/app","proposed_by":"agent-7"}'
# => {"review_id": "a1b2c3d4", "status": "pending"}

python scripts/human_review.py --pending
python scripts/human_review.py --approve a1b2c3d4 --reviewer alice --note "已备份可删"
python scripts/human_review.py --reject <id> --reviewer bob --note "先走 PR"
python scripts/human_review.py --summary
```

## 与生态集成
- 配合 `safety-guardrails`：CONFIRM 决策 → 转本队列，agent 挂起等待结果再继续。
- 配合 `behavior-observability`：审核结论与理由落盘行为日志，用于事后归因与策略调优。
- 配合 `super-agent-loop`：作为「人工闸」节点插入执行 DAG，高风险节点门控后才放行下游。
---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
