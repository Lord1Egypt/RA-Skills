---
name: industry-opportunity-analyzer
description: "Analyze the opportunity landscape of a given industry — demand scenarios, customer pain points, industry policy opportunities, and potential future developments. Use when user asks for '行业机会', '行业痛点', '行业政策', '行业未来', '市场机会', 'industry opportunities', 'policy trends'. Outputs 4-section markdown (场景/痛点/政策/未来). Part of the industry-analyzer plugin (6-Skill 流水线第 4 环)."
---

# 行业机会分析器 (Industry Opportunity Analyzer)

Analyze the opportunity landscape of a given industry across 4 dimensions: demand scenarios, customer pain points, industry policy opportunities, and potential future developments.

## When to Use

- 用户明确要求"分析 {行业} 机会 / 痛点 / 政策 / 未来"
- 行业分析流水线第 4 环（由 行业分析成章官 调度）
- 独立召唤

## Input

- **必填**：`output/{industry-slug}/session.json`

## Output

- **文件**：`output/{industry-slug}/04-opportunity.md`
- **格式**：Markdown，4 大节齐全

### 4 大节（标准结构）

#### ① 需求场景（3-5 个典型场景）

每个场景：
- **场景名**：典型应用 / 业务场景
- **目标客户**：谁在用
- **痛点**：现在的难点
- **现有方案缺口**：现有方案没解决什么

#### ② 需求痛点（3-7 个，按客户分层）

按客户分层（如：终端用户 / 厂商 / 渠道商 / 监管）：
- **痛点描述**：具体问题
- **影响范围**：多少人 / 多少规模受影响
- **量化（如有）**：占比 / 增长率 / 损失

#### ③ 政策机会（3-5 项）

每项：
- **政策名**：政策 / 规划 / 文件全名
- **发布时间**：YYYY-MM
- **发布部门**：国务院 / 部委 / 地方政府
- **资金 / 规模**：如有
- **影响**：对行业 / 厂商 / 客户的影响

#### ④ 潜在未来发展（3-5 个趋势）

每个趋势：
- **趋势名**：未来 1-3 年的关键变化
- **时间窗**：短期 / 中期 / 长期
- **驱动因素**：什么在推动
- **潜在赢家**：哪些公司 / 玩家可能受益

## Workflow

1. **读 session.json**
2. **需求场景搜索**：
   - `"{行业} 典型应用场景"`
   - `"{行业} 用户需求"`
   - `"{行业} 痛点 调研报告"`
3. **痛点搜索**：
   - `"{行业} 行业痛点"`
   - `"{行业} 客户痛点 报告"`
   - `"{行业} 现有方案 不足"`
4. **政策搜索**：
   - `"{行业} 国家政策 2024 2025 2026"`
   - `"{行业} 国务院 规划"`
   - `"{行业} 部委 文件"`
   - `"{行业} 十四五 规划"`
   - `"{行业} 地方政府 补贴"`
5. **未来趋势**：web 搜索行业研究报告（艾瑞/IDC/Gartner/赛迪/McKinsey）+ AI 推演
6. **写 `04-opportunity.md`**
7. **更新 session.json**

### 4 维度机会框架

参见 `references/opportunity-dimensions.md`

## stop_condition

- `04-opportunity.md` 存在
- 4 大节齐全
- 需求场景 3-5 个
- 痛点 3-7 个
- 政策 3-5 项（含发布时间 / 部门）
- 未来趋势 3-5 个
- session.json `status.opportunity` = `done`

## style

- 前瞻、有数据、有时间窗
- 不用"赋能""引领"等空话
- 政策必须有发布时间和部门（找不到 → 标"未找到具体政策文件"）
- 未来趋势要有"驱动因素"——不能凭空预测

## 更新 session.json

- 改 `status.opportunity` = `done` / `failed`
- 改 `updated_at`
- 在 `data_sources` 追加

## Standalone Mode

同 Skill 1，未提供 session.json 时自动生成最小版本。

## 错误处理

- 政策文件找不到 → 标"未找到具体政策，参考线索：..."
- 行业报告稀缺 → 用 AI 通用知识 + 显式标"基于行业普遍认知，缺少具体报告支撑"
- 痛点 / 场景数据不足 → 至少 3 个，标"信息有限"

## 参考

- 行业分析器总 spec：`~/Downloads/周报生成器/行业分析器/docs/superpowers/specs/2026-06-07-industry-analyzer-design.md` §5.4
- 4 维度框架：`references/opportunity-dimensions.md`
