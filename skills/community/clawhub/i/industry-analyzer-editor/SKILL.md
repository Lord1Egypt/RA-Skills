---
name: industry-analysis-editor
description: "Aggregate the 4 dimension outputs (top-enterprise, ecosystem, digital-solutions, opportunity) into one comprehensive industry analysis report. Read 4 markdown files + session.json, write the main report. Use when user invokes the 行业分析 pipeline 成章官 step, or wants to re-synthesize after partial updates. Part of the industry-analyzer plugin (6-Skill 流水线第 5 环)."
---

# 行业分析成章官 (Industry Analysis Editor)

Aggregate the 4 dimension outputs into one comprehensive industry analysis report. The editor's job is **integration + cross-dimension insight**, not regurgitation.

## When to Use

- 行业分析流水线第 5 环：在 4 个分析 Skill 跑完后，整合为一份主稿
- 用户说"整合 4 份 md" / "重跑成章官" / "更新主稿"
- session.json 中 `status.top-enterprise/ecosystem/solutions/opportunity` 全部为 `done` 时触发

## Input

- **必填**：
  - `output/{industry-slug}/session.json`
  - `output/{industry-slug}/01-top-enterprise.md`
  - `output/{industry-slug}/02-ecosystem.md`
  - `output/{industry-slug}/03-digital-solutions.md`
  - `output/{industry-slug}/04-opportunity.md`
- **可选**：用户可指定主稿的"重点章节"或"目标读者"

## Output

- **文件**：`output/{industry-slug}/industry-analysis-report.md`
- **格式**：Markdown，5 块齐全（执行摘要 + 4 章主体 + 跨维度洞察 + 行动建议）

### 必含 5 块

| # | 块 | 内容 | 字数 |
|---|---|---|---|
| 1 | **执行摘要** | 核心数字 + 关键洞察，读者 1 分钟看完 | 200-400 字 |
| 2 | **头部企业** | 从 `01-top-enterprise.md` 整合（去重 + 补充上下文） | 全文保留 |
| 3 | **生态图谱** | 从 `02-ecosystem.md` 整合 + 简化 Mermaid | 全文保留 |
| 4 | **数字化方案** | 从 `03-digital-solutions.md` 整合 | 全文保留 |
| 5 | **行业机会** | 从 `04-opportunity.md` 整合 | 全文保留 |
| 6 | **跨维度洞察** | 4 章之间的关联（如"头部企业 X 在 数字化方案 中是 4 大厂合作伙伴"） | 300-500 字 |
| 7 | **行动建议** | 按 `audience` 给具体建议 | 200-400 字 |

> 注：执行摘要在前，跨维度洞察和行动建议在底部，4 章主体居中。

## Workflow

1. **读 session.json**：确认 industry / audience / language
2. **读 4 份 md**：完整读入
3. **提炼执行摘要**：
   - 提取每章最关键 1-2 个数字 / 事实
   - 浓缩为 200-400 字
   - 包含：行业范围 + 头部代表 + 生态特征 + 数字化格局 + 关键机会
4. **整合 4 章节**：
   - 保留原文核心内容
   - 去重（避免跨章节重复）
   - 补充章节间衔接句（1-2 句）
   - 引用标注："数据来自：01-top-enterprise.md"（每章末尾）
5. **生成跨维度洞察**（300-500 字）：
   - 头部企业 × 生态图谱：哪些头部企业占据关键生态位
   - 头部企业 × 数字化方案：哪些头部企业是 4 大厂方案的标杆客户
   - 数字化方案 × 行业机会：哪些政策红利对应到 4 大厂的布局
   - 生态图谱 × 行业机会：哪些痛点 / 政策 / 未来趋势对应到具体生态位
6. **生成行动建议**（按 audience）：
   - internal（内部）：投资方向 / 战略卡位 / 风险提示
   - client（客户）：方案选型建议 / 合作建议
   - investor（投资）：标的筛选 / 估值锚点 / 时间窗
7. **写 `industry-analysis-report.md`**
8. **更新 session.json**：`status.report` = `done`

### 主稿整合模板

参见 `references/synthesis-template.md`

## stop_condition

- `industry-analysis-report.md` 存在
- 5 块齐全
- 执行摘要 200-400 字
- 跨维度洞察有意义（不是空洞泛泛）
- 行动建议按 audience 调整
- session.json `status.report` = `done`

## style

- 整合者视角，不重复上游（避免把 4 份 md 整段粘贴）
- 衔接自然（1-2 句话把 4 章"缝"在一起）
- 不确定 → 标"未找到，参考线索：..."（继承上游标注）
- 跨维度洞察是这份主稿的"主菜"——必须比单维度更深

## 更新 session.json

- 改 `status.report` = `done` / `failed`
- 改 `updated_at`

## 重跑规则

- 任一上游 md 更新后都可重跑本 Skill
- 重跑只覆盖 `industry-analysis-report.md`，不动上游
- session.json 中 `status.report` 重置为 `in_progress` → `done`

## 错误处理

- 某份 md 缺失 → 提示"上游 Skill 未完成：{md 文件名}，请先跑 {对应 Skill}"
- 4 份 md 内容互相矛盾 → 在跨维度洞察中标注"数据口径不一致，已注明"
- 找不到跨维度关联 → 退而求其次，提炼"行业最值得关注 X 个点"

## 参考

- 行业分析器总 spec：`~/Downloads/周报生成器/行业分析器/docs/superpowers/specs/2026-06-07-industry-analyzer-design.md` §5.5
- 整合模板：`references/synthesis-template.md`
