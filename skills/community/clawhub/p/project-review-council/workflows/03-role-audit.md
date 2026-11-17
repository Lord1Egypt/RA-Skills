# Phase 3 — 角色审计（Fan-out-and-Synthesize）

> **模式**：Fan-out-and-Synthesize。N 个角色并行独立审计，合并为角色报告集。

## 输入

P2 证据清单 + P1 项目画像 + [config/roles.yaml](../config/roles.yaml) 按 `depth` 启用的角色集。

## 处理（Dispatcher）

1. 读取 `roles.yaml` 的 `depth_presets[depth]` 得到启用角色列表
2. 为每个角色分配子任务（同一 role agent，输入区分）
3. 加载对应 [roles/*.md](../roles/) 人格文件
4. 按角色类别加载行业检查清单（📍 按需加载）：
   - 技术类（CTO/Chief Architect/Staff Engineer/QA/DevOps）→ [checklists/code.md](../checklists/code.md) + [checklists/architecture.md](../checklists/architecture.md)
   - 产品类（Product/UX）→ [checklists/product.md](../checklists/product.md)
   - 增长类（Growth/Marketing）→ [checklists/growth.md](../checklists/growth.md)
   - 安全类（Security/Compliance）→ [checklists/security.md](../checklists/security.md)
   - 战略类（CEO/VC）→ [checklists/business.md](../checklists/business.md)
5. 角色独立审计，**互不可见**

## 处理（Worker = 单角色）

每角色按 [templates/role-report.md](../templates/role-report.md) 的 7 字段契约输出：
观点 / 最大亮点 / 最大问题 / 最大风险 / 最容易失败的位置 / 第一件做什么 / 评分+解释

**特殊角色约束**：
- **Devil's Advocate** 必须给出失败论据，评分默认 ≤4
- **Competitor** 必须给出可执行的攻击方案
- **Independent Auditor** 不参与此阶段（仅在 P4/P10 触发）

## 处理（Synthesizer）

合并 N 份角色报告为角色报告集，按角色 `weight` 排序，标注评分分歧。

### 评分趋同检测（独立性门控）

合并后**必须**执行趋同检测，防止角色互相迎合导致独立性失效：

1. **计算评分分布** — 统计所有角色评分的极差（max − min）和标准差
2. **趋同判定**（查 [rubrics/scoring.md](../rubrics/scoring.md) 防 Gaming 规则 #3）：
   - 极差 < 2 → **趋同警报**：疑似互相迎合，独立性失效
   - 标准差 < 1.0 → **趋同警报**（即使极差 ≥2，分布过度集中也算）
3. **趋同处置**：
   - 触发警报 → 对趋同角色组执行**独立性重审**：要求每角色独立重写"观点"段（不看他人报告），重跑后再次检测
   - 重审后仍趋同 → 标记为"独立性存疑"并在 P9 Executive Summary 中显式声明，降权该组评分
4. 输出趋同检测记录（极差 / 标准差 / 是否触发 / 处置动作）写入角色报告集头部

## 输出

N 份角色报告（结构化），汇总为角色报告集。报告集头部含趋同检测记录。

## Exit Gate

- 每角色 7 字段齐全
- 每条论断标注证据等级
- Devil's Advocate 给出 ≥3 条失败论据
- Competitor 给出 ≥1 条可执行攻击方案
- **趋同检测已执行**（极差/标准差已计算，趋同警报已处理或确认无警报）

## Decision Gate

| 情况 | 动作 |
|------|------|
| 角色评分极差 ≥ `role_score_spread`(4) | 标记为分歧组，P4 强制交叉 |
| **评分极差 < 2 或 标准差 < 1.0** | **趋同警报：触发独立性重审，重审后仍趋同则降权** |
| 某角色报告缺字段 | 回退单角色重跑（非全局） |
| 证据标注缺失 | 驳回该角色补全 |

## Retry / Rollback

- **Retry**：单角色报告不合格 → 仅重跑该角色
- **Rollback**：证据系统性不足 → 回退 P2

## 用户检查点

展示启用角色集与评分概览，确认后进入 P4 交叉。
