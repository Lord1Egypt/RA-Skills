---
name: industry-analysis-html-renderer
description: "Render an industry analysis report (4 dimension markdown + main report) into a single-page scrollable visual HTML page. Uses the visual-page skill for charts/SVG/comparison tables/timeline. Use when user wants to convert industry-analysis-report.md to a shareable visual HTML, or as the final step of the 行业分析 pipeline. Part of the industry-analyzer plugin (6-Skill 流水线第 6 环)."
---

# 行业分析 HTML 渲染官 (HTML Renderer)

Render an industry analysis report (4 dimension markdown + main report) into a single-page scrollable visual HTML page.

## When to Use

- 行业分析流水线第 6 环（最后一步）：在主稿完成后，渲染为可视化 HTML
- 用户单独召唤："把 4 份 md + 主稿渲成 HTML"
- 重跑：主稿更新后，重新渲染

## Input

- **必填**：
  - `output/{industry-slug}/session.json`
  - `output/{industry-slug}/01-top-enterprise.md`
  - `output/{industry-slug}/02-ecosystem.md`
  - `output/{industry-slug}/03-digital-solutions.md`
  - `output/{industry-slug}/04-opportunity.md`
  - `output/{industry-slug}/industry-analysis-report.md`

## Output

- **文件**：`output/{industry-slug}/industry-analysis-report.html`
- **格式**：单页可滚 HTML，4 大节均有可视化元素

### 4 大节可视化要求

| 节 | 来源 | 必备可视化元素 |
|---|---|---|
| **头部企业** | `01-top-enterprise.md` | Top 10 排序表（可滚动 / 高亮 Top 3） |
| **生态图谱** | `02-ecosystem.md` | 1 个 SVG 生态图（替代 Mermaid，更精致） |
| **数字化方案** | `03-digital-solutions.md` | 4 大厂 + 垂直厂商对比表（卡片式或表格式） |
| **行业机会** | `04-opportunity.md` | 政策 timeline + 趋势 cards |

### 页面结构

```
┌──────────────────────────────────┐
│ 顶部 Hero 区                      │
│ - 行业名 / 时间窗 / 摘要           │
│ - 数据来源 / 生成时间              │
├──────────────────────────────────┤
│ 1. 头部企业 Top 10                │
│   - 概览表 + 重点 3 家卡片         │
├──────────────────────────────────┤
│ 2. 生态图谱                       │
│   - SVG 图 + 4 生态位说明         │
├──────────────────────────────────┤
│ 3. 数字化方案对比                  │
│   - 4 大厂对比表 / 卡片            │
│   - 垂直厂商列表                   │
├──────────────────────────────────┤
│ 4. 行业机会                       │
│   - 政策 timeline                  │
│   - 需求场景 / 痛点 / 趋势 cards   │
├──────────────────────────────────┤
│ 5. 跨维度洞察 + 行动建议           │
│   - 简化文字版                     │
├──────────────────────────────────┤
│ 底部：源文件清单 + 数据缺口        │
└──────────────────────────────────┘
```

## Workflow

1. **读 5 个输入文件**（session.json + 4 md + 主稿）
2. **解析 4 维度数据**：
   - 头部企业 → 排序表数据
   - 生态图 → 节点 + 关系数据
   - 数字化方案 → 厂商 × 4 要素表
   - 行业机会 → 政策 timeline + 趋势 cards
3. **加载 visual-page skill**（这个 skill 是 mavis 自带的，擅长图表/SVG/对比/timeline）
4. **传入数据 + 视觉偏好**给 visual-page skill
5. **生成单页 HTML**
6. **保存到 `industry-analysis-report.html`**
7. **更新 session.json**

### 图表建议参考

参见 `references/chart-suggestions.md`

## stop_condition

- `industry-analysis-report.html` 存在
- 4 大节都有可视化元素
- 页面在浏览器中可滚 / 可读
- session.json `status.html` = `done`

## style

- 单页可滚（不要分页）
- 配色专业（参考 McKinsey / BCG 报告风）
- 数据可视化优先，少用纯文字墙
- 移动端可读（响应式）

## 调 visual-page skill 的方式

```text
调用 visual-page skill 时传入：
- 标题：{行业} 行业分析报告
- 4 大节数据（头部 / 生态 / 方案 / 机会）
- 主稿的执行摘要 + 跨维度洞察
- 视觉偏好：单页可滚 / McKinsey 风 / 中文

visual-page skill 会基于这些数据生成 HTML。
```

## 更新 session.json

- 改 `status.html` = `done` / `failed`
- 改 `updated_at`

## 重跑规则

- 主稿更新后，单独重跑本 Skill 即可
- 不动上游 4 份 md

## 错误处理

- 上游 md 缺失 → 提示"上游 Skill 未完成，无法渲染"
- visual-page skill 失败 → 保留 .md 主稿，标"`*.html` 渲染失败，可手动重试"
- HTML 体积过大（>5MB）→ 提示"数据量大，可考虑拆分"

## 参考

- 行业分析器总 spec：`~/Downloads/周报生成器/行业分析器/docs/superpowers/specs/2026-06-07-industry-analyzer-design.md` §5.6
- 视觉渲染工具：visual-page skill（mavis 自带）
- 图表建议：`references/chart-suggestions.md`
