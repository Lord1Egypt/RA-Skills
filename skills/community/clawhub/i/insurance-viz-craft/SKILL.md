---
name: insurance-viz-craft
version: 1.0.0
description: 保险条款转交互式知识图谱HTML，含保障责任/免责/理赔等7种视图
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

保险条款的阅读体验是出了名的差——长达数十页的合同文本、密集的专业术语、保障责任和免责条款分散在不同章节、理赔条件流程不清晰。客户买完保险往往不知道自己保了什么、什么情况不赔、出险了该怎么操作。代理人的口头讲解也不够系统，容易产生理解偏差。

本 Skill 将复杂的保险条款转化为可视化的交互式知识图谱，包含保障责任图谱、免责条款网络、理赔流程图、产品对比、场景模拟、术语词典、保单时间轴 7 种模式。通过纯 SVG 绘制节点和连线，点击节点查看详情、路径追踪、场景模拟，让晦涩的合同条款变得一目了然。

---

# Insurance Viz Craft — 保险条款可视化图谱 Skill

> 将复杂的保险条款转化为可视化的交互式知识图谱，帮助理解保障范围、责任免除、理赔流程等。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **粘贴保险条款**：粘贴保险合同、条款说明的原文文本
2. **选择可视化类型**：从映射表中选择适合的可视化方式
3. **选择配色方案**：选择保险行业配色主题
4. **生成图谱**：输出交互式单文件 HTML

### 输入格式建议

- 粘贴完整的保险条款文本（可分批粘贴）
- 标明条款名称、保险公司名称
- 指明是否需要多产品对比

## 场景-模式映射表

| 保险业务场景 | 推荐模式 | 特点 |
|------------|---------|------|
| 了解保障范围 | coverage-map（保障责任图谱） | 中心辐射图，展示保障项目及条件 |
| 了解免责范围 | exclusion-web（免责条款网络） | 网络图展示所有免责情形及关联 |
| 出险理赔 | claim-flow（理赔流程图） | 流程图展示报案→审核→赔付全流程 |
| 选购产品 | product-compare（产品对比） | 多产品并排对比保障项、价格、免责 |
| 假设验证 | scenario-sim（场景模拟） | 用户输入场景，AI 判断理赔可能性 |
| 理解术语 | term-glossary（术语词典） | 术语列表 + 关联图谱，点击查看解释 |
| 保单管理 | policy-timeline（保单时间轴） | 缴费、等待期、保障期、续费等时间节点 |

## 配色方案库

### 保险行业配色

- **信任蓝**（主体/保障）：`#1a73e8`
- **保障绿**（确定性/已覆盖）：`#22c55e`
- **警示橙**（等待/注意）：`#f59e0b`
- **免责红**（风险/不覆盖）：`#ef4444`

### 节点颜色说明
- **保障责任**：绿色系 `#22c55e` → `#16a34a` → `#15803d`
- **免责条款**：红色系 `#ef4444` → `#dc2626` → `#b91c1c`
- **理赔流程**：蓝色系 `#3b82f6` → `#2563eb` → `#1d4ed8`
- **条件/限制**：橙色系 `#f59e0b` → `#d97706` → `#b45309`
- **术语/定义**：紫色系 `#8b5cf6` → `#7c3aed` → `#6d28d9`

### 4 套主题配色

#### 1. 保险蓝
```
--bg: #f0f7ff
--text: #1e293b
--card-bg: #ffffff
--card-border: #bfdbfe
--link-line: #93c5fd
--node-coverage: #22c55e
--node-exclusion: #ef4444
--node-process: #3b82f6
```

#### 2. 稳重大气
```
--bg: #f8fafc
--text: #0f172a
--card-bg: #ffffff
--card-border: #e2e8f0
--link-line: #94a3b8
--node-coverage: #16a34a
--node-exclusion: #dc2626
--node-process: #2563eb
```

#### 3. 深色监管
```
--bg: #0f172a
--text: #e2e8f0
--card-bg: #1e293b
--card-border: #334155
--link-line: #475569
--node-coverage: #22c55e
--node-exclusion: #f87171
--node-process: #60a5fa
```

#### 4. 纸质文档
```
--bg: #fefcf6
--text: #3a3a3a
--card-bg: #ffffff
--card-border: #d4d4d4
--link-line: #a3a3a3
--node-coverage: #16a34a
--node-exclusion: #dc2626
--node-process: #2563eb
```

## 交互增强包列表

### 基础交互
- 节点点击展开详情（弹出卡片显示条款原文）
- 路径高亮（从保障 → 条件 → 例外 → 理赔的完整路径）
- 图例筛选（按类型显示/隐藏节点）
- 缩放和平移（适用于大型图谱）

### 高级交互
- 场景模拟（输入"小病住院"，查看是否赔、赔多少）
- 条款原文定位（点击节点跳转到条款原文位置）
- 对比模式切换（多产品切换对比）
- 打印摘要（仅保留核心结构，打印友好）
- 问答模式（图谱 + 文字回答结合）

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **知识图谱**：使用纯 SVG + CSS 绘制节点和连线
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：支持画布缩放，移动端可手势操作

## 命令定义

### `/insurance-viz`
主入口命令。输入保险条款文本，选择可视化类型后生成交互式知识图谱 HTML。

### `/insurance-compare`
多产品对比分析。支持同时分析 2-4 款保险产品，生成对比图谱和差异列表。

## 文件结构

```
skills/insurance-viz-craft/
├── SKILL.md
├── patterns/
│   ├── coverage-map.json    # 保障责任图谱
│   ├── exclusion-web.json   # 免责条款网络
│   ├── claim-flow.json      # 理赔流程图
│   ├── product-compare.json # 产品对比视图
│   ├── scenario-sim.json    # 场景模拟器
│   ├── term-glossary.json   # 术语词典
│   └── policy-timeline.json # 保单时间轴
└── templates/
    ├── base.html
    ├── coverage-map.html
    ├── exclusion-web.html
    ├── claim-flow.html
    ├── product-compare.html
    ├── scenario-sim.html
    ├── term-glossary.html
    └── policy-timeline.html
```
