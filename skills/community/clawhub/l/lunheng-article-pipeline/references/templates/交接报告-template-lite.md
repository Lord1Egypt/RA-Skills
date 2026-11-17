> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

> 🏁 **收尾硬规则（v2.12.56 P-4，硬约束；与 P-1 同源）**：本交接报告的**正文/摘要必须随最终消息一起结束回合**（该消息即 completion event 送达主控）；**不得**塞进 `acknowledgment` 字段（该字段不从子代理回合发出，实际不送达——实测导致主控「完成事件 + 摘要」双丢）。**禁用** `sessions_yield` / `agents_wait` / `next_check` / `subagents` / `sessions_list` / `sessions_history`（worker 自行 `sessions_yield` = 被拒或挂起 run，均不产生完成事件）。详见 [`../_shared/真源/dispatch-header.md`](../_shared/真源/dispatch-header.md) §收尾协议。

# 交接报告模板（精简版）

> **精简版**：只保留骨架 + 必填字段，详细说明见 [`交接报告-template.md`](交接报告-template.md)

```markdown
# 交接报告

> **位置**: `run/<项目名>/交接报告/<角色>-<阶段>.md`
> **使用**: 每个角色交付时必填

## 1. 做了什么
（一句话）

## 2. 产物在哪
- `path/to/file1`
- `path/to/file2`

## 3. 怎么验证
- 检查项 1
- 检查项 2

## 4. 已知问题
- 问题 A
- 问题 B

## 5. 下一步
- 阶段 X 的预期任务

## 6. 状态机更新（status.md 对应行）
（由主控代写）

## 7. AI 使用披露（T5 写手 + T8 主控必填）
- 本文由论衡 AI 写作流水线生成
- 核心论点：主人原创洞察（任务简报第 X 行）
- 检索证据：全部真实（[Lxx]/[Dxx]/[Cxx] 编号可追溯）
```

---

**精简版结束**

> **token 消耗不属子代理回报段**：由**主控**在收到本子代理 completion event 时，从事件末尾 Stats line 提取 `Token usage`（input/output/total）记录（`sessions_spawn` 返回值无 stats 字段）。

> 完整版（含文末附录四节完整性自检）见 [`交接报告-template.md`](交接报告-template.md)