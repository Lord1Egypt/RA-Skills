---
title: "kai-report-creator 使用指南"
theme: corporate-blue
author: kai-report-creator
date: 2024-04-07
lang: zh
toc: true
abstract: "一行命令生成异步友好的 HTML 报告——决策者 30 秒抓住要点，下游 AI 可解析三层结构。"
---

## 为什么报告总是"一眼 AI"

决策者没时间读完所有材料。AI 能生成报告，但往往一眼就能看出是模板产物：

- 章节标题像填空（"概述"、"关键发现"、"下一步"）
- 主色泛滥在六种元素上（标题、KPI、图表、边框、按钮、链接）
- KPI 不管几个都是三列

**kai-report-creator 解决的核心问题：让报告能独立承受第一次阅读。**

## 五大设计原则

:::callout type=tip
这些原则对任何编写 AI 技能的人都有参考价值。
:::

### 渐进式披露

命令路由表确保每次只加载必要内容：

| 命令 | 加载内容 |
|------|----------|
| `--plan` | 只读 IR 规则，不接触 CSS |
| `--generate` | 只加载一个主题 CSS |
| `--themes` | 预构建 HTML，技能不解析内部 |

**效果：** `--plan` 调用从不接触 CSS，`--generate` 从不加载其他 5 套主题。

### 硅碳协作设计

:::callout type=note
输入端：IR 三层结构 → 人类自然书写  
输出端：HTML 三层结构 → 机器渐进解析
:::

IR 为碳基读者揭示结构，HTML 为硅基读者揭示数据。同一原则为双物种设计。

### 视觉节奏即认知节拍

禁止连续 3 个纯文字章节，每 4-5 章节必须有视觉锚点（KPI 网格/图表/流程图）。

**为什么：** 大段密集文字让读者疲惫，没有背景的数据让读者迷失。

### 异步决策支持

报告没有讲述者在场。读者扫开头、看标题、瞥数据，30 秒内决定是否继续。

**产品设计约束：** `--review` 是一次性自动优化，不是交互式确认。

### 设计质量基线

- **90/8/2 配色** — 90% 中性面，8% 结构色，2% 弹点
- **10:1 字号张力** — 标题有锚点感，不是标签感
- **KPI 网格规则** — 4 个 KPI 用 2×2，英雄指标用 2fr 1fr 1fr
- **内容气质色调** — 思辨用暖棕、技术用藏蓝、商业用深青绿

## 一行命令开始

**安装：**

```
# Claude Code：对 Claude 说
安装 https://github.com/kaisersong/report-creator

# OpenClaw
clawhub install kai-report-creator
```

**使用：**

```
/report --from meeting-notes.md
/report --from https://example.com/data --output market-analysis.html
/report --plan "Q3 总结" --from data.csv
```

## 核心工作流

### 一步生成

从文档或 URL 直接输出 HTML，零配置。

### 两阶段流程

复杂报告建议先生成 `.report.md` 大纲，编辑确认后再渲染：

```
/report --plan "Q3 销售" --from q3.csv
# 编辑生成的 .report.md
/report --generate q3-sales.report.md
```

### Review 自动优化

8 项检查点，一次性自动修复：

| 检查点 | 解决的问题 |
|--------|------------|
| BLUF 开场 | 开头没有结论，读者不知道为什么继续读 |
| 标题栈逻辑 | 标题都是名词短语，看不出论证脉络 |
| 去模板腔标题 | "概述""关键发现"等信息量为零 |
| 文字砖块拆解 | 段落超过 150 字，无法扫读 |
| 数据后 takeaway | 有数字没解读，读者自己猜含义 |
| 洞察优于数据 | 罗列数字，没有说"这意味着什么" |
| 扫读锚点覆盖 | 连续纯文字，没有视觉休息 |
| 条件触发指引 | 教程类没说"适合谁、需要什么" |

## 报告格式（IR）

**Frontmatter 声明文档身份：**

```yaml
---
title: Q3 销售报告
theme: corporate-blue
abstract: "Q3 营收同比增长12%"
---
```

**组件块传递结构化数据：**

```
:::kpi
items:
  - label: 营收
    value: ¥2,450万
    delta: ↑12%
  - label: 新客户
    value: 183
    delta: ↑8%
:::

:::timeline
- 2024-10-15: Q4 目标下发
- 2024-10-31: 新品发布
:::
```

## 6 套内置主题

| 主题 | 适合场景 |
|------|----------|
| corporate-blue | 高管汇报、商业报告 |
| minimal | 研究论文、分析报告 |
| dark-tech | 运维报告、技术文档 |
| dark-board | 架构图、指标看板 |
| data-story | 年度报告、增长故事 |
| newspaper | 行业分析、通讯 |

## 面向 AI 智能体

输出内嵌三层机器可读结构：

```
Layer 1 — <script id="report-summary">  文档级：标题、摘要、所有 KPI
Layer 2 — data-section data-summary     章节级：标题 + 一句话摘要
Layer 3 — data-component data-raw       组件级：原始数据
```

下游技能可直接提取：

```python
soup = BeautifulSoup(open("report.html"))
summary = json.loads(soup.find("script", {"id": "report-summary"}).string)
print(summary["kpis"])  # 所有 KPI 数据
```

---

**GitHub:** https://github.com/kaisersong/kai-report-creator
