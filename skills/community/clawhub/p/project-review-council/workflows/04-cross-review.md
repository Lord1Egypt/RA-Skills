# Phase 4 — 交叉审计（Adversarial Verification）

> **模式**：Adversarial Verification。角色互相反驳，Independent Auditor 裁决。

## 输入

P3 角色报告集 + [config/settings.yaml](../config/settings.yaml) 的 `cross_review.min_groups`(默认 3)。

## 处理

### Step 1 — 生成对立组

按 `cross_review.random_selection` 随机选取 ≥3 组角色对（优先选取 P3 中评分分歧 ≥4 的对）。

典型对立组：
- CEO vs Devil's Advocate（战略乐观 vs 死亡论证）
- CTO vs Future Analyst（当下可行 vs 未来过时）
- Growth vs Competitor（增长路径 vs 攻击弱点）
- VC vs Sales（投资价值 vs 销售难度）

### Step 2 — 互相反驳

每组成员必须：
1. 指出对方的错误、遗漏、逻辑漏洞
2. 指出对方隐含假设
3. 指出对方证据不足处

**不能客气。** 允许激烈对立。

### Step 3 — Auditor 裁决

加载 [roles/independent-auditor.md](../roles/independent-auditor.md)。
Auditor 只看对立双方的论据（不看 P3 推理过程），按其 verdict schema 裁决：
- 成立 / 猜测 / 需实验验证

## 输出

反驳记录集 + Auditor 裁决集。

## Exit Gate

- ≥ `min_groups`(3) 组完成交叉
- 每组双方都给出反驳
- Auditor 对每条关键对立给出裁决

## Decision Gate

| 情况 | 动作 |
|------|------|
| 发现新证据缺口 | 回退 P2 补证据 |
| 对立未覆盖核心争议 | 增加交叉组 |
| 达标 | 进入 P5 |

## Retry / Rollback

- **Retry**：某组反驳不充分 → 重跑该组
- **Rollback**：交叉暴露 P3 角色报告根本性错误 → 回退 P3
