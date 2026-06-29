# Phase 10 — 红蓝对抗

> **模式**：Adversarial Verification（终局）。`enable_phase_10: true` 时执行。

## 输入

P9 委员会决议 + [config/settings.yaml](../config/settings.yaml) 的 `red_blue` 设置。

## 处理

### Step 1 — 组队

- **Blue Team**：必须证明这个项目一定会成功（≥ `arguments_per_side`(20) 条论据）
- **Red Team**：必须证明这个项目一定会失败（≥ `arguments_per_side`(20) 条论据）

### Step 2 — 交锋

- 每条论据**必须被对方回应**（`require_response: true`）
- 论据**不可重复**（`allow_repeat: false`）
- 逐条对攻

### Step 3 — Auditor 最终裁决

加载 [roles/independent-auditor.md](../roles/independent-auditor.md)。
对红蓝双方的论据逐条裁决：
- 真正成立的观点
- 只是猜测
- 需要实验验证

## 输出：按 [templates/decision-memo.md](../templates/decision-memo.md) 模板

Final Decision Memo 包含：
- Blue Team 成立论据清单
- Red Team 成立论据清单
- 需实验验证项清单
- 最终裁决（修正 P9 决议）

## Exit Gate

- 双方各 ≥ `arguments_per_side`(20) 条论据
- 每条已被对方回应
- Auditor 对每条给出裁决
- 最终裁决明确（支持/修正/推翻 P9 决议）

## Decision Gate

| 情况 | 动作 |
|------|------|
| 论据不足 20 条 | 追加（允许 Blue/Red 各补） |
| 论据重复 | 删除并补新论据 |
| Auditor 发现 P9 致命疏漏 | 回退 P9 修正决议 |
| 达标 | 输出 Final Memo，结束全流程 |

## Retry / Rollback

- **Retry**：论据质量低 → 追问深化
- **Rollback**：终局暴露 P9 根本性错误 → 回退 P9 甚至 P5 重做
