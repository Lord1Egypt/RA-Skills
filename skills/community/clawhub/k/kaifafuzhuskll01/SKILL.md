---
name: ppt-generator
description: |
  生成类PPT的HTML演示文稿。自包含单文件、1280×720固定画布、键盘翻页。
  触发条件：
  (1) 用户说"做个PPT"、"生成演示"、"做几页幻灯片"、"presentation"
  (2) KAIFA## PPT <主题>
  三种模式：简易(10min/7-10页/无目录)、标准(25min/20-25页/有目录+章节封面)、详尽(50min/40-50页/有目录+章节封面)
  用户只需说主题+模式+章节数，其余自动。
---

# PPT Generator — HTML 演示文稿生成器

## 触发

| 方式 | 示例 |
|------|------|
| 自然语言 | "做个PPT"、"生成一个演示"、"做几页幻灯片"、"presentation about X" |
| 显式 | `KAIFA## PPT <主题>` |

## 三种预设模式

| 参数 | 简易 | 标准 | 详尽 |
|------|------|------|------|
| 时长 | ~10 min | ~25 min | ~50 min |
| 总页数 | 7-10 | 20-25 | 40-50 |
| 目录页 | 无 | 有 | 有 |
| 章节封面 | 无 | 有（每章1页） | 有（每章1页） |
| 结构页 | Cover+Ending=2 | Cover+TOC+章封面+Ending | 同标准 |

### 页数公式

```
简易: total = 2 + Σ每章内容页
标准: total = 2 + 1(TOC) + 章节数 + Σ每章内容页
详尽: total = 2 + 1(TOC) + 章节数 + Σ每章内容页
```

---

## 核心流程

```
PHASE 0: DISCOVERY  → 模式确认 → 大纲打磨 → 锁定
PHASE 1: PLAN       → 分配布局 → 内容要点
     ⛔ APPROVAL
PHASE 2: IMPLEMENT   → 并发生成 slide 片段 → 拼接
PHASE 3: REVIEW      → 一致性检查
PHASE 4: REPORT      → canvas 预览 → 输出文件
```

---

## PHASE 0: DISCOVERY（交互式大纲打磨）

### 步骤

1. **确认模式**：用户说了模式→直接用。没说→追问 "简易/标准/详尽？"
2. **确认章节数**：用户没说→追问 "几个章节/部分？"
3. **计算页数**：套公式，结构页固定扣除，内容页按章节重要性动态分配
4. **出大纲草案**：显示每页标题+布局类型，区分结构页和内容页
5. **用户调整**：展开/压缩/合并 → 修订 → 再确认 → 锁定

### 大纲输出格式

```
📊 大纲草案 — 标准模式
总页数: 22页 (结构7 + 内容15)

结构页:
  p1   封面                                    [cover]
  p2   目录                                    [toc]

第1章 项目概况
  p3   章节封面                                [chapter-cover]
  p4   背景与目标                              [ca-bullets]
  p5   项目范围                                [ca-bullets]

第2章 关键进展 ← 核心
  p6   章节封面                                [chapter-cover]
  p7   三大成果                                [ca-cards-3]
  p8   对比分析                                [ca-bullets-2col]
  ...

  pN   结束页                                  [ending]

需要展开/压缩/调整哪里？
```

### 内容分配规则

- 用户指定的"核心"章节 → 多分配 1-3 页
- 有数据/对比 → 自动插入 chart 页
- "简要提到"的章节 → 1页（不含章节封面）
- 每页内容要点在 Phase 1 细化

---

## PHASE 1: PLAN

基于锁定的大纲，产出两个结构化数据文件：

### 产出物

1. **`master_config.json`** — 母版配置
2. **`slides_data.json`** — 每页的数据定义

### master_config.json 结构

```json
{
  "theme_color": "#004D8C",
  "theme_accent": "#009688",
  "header_title": "数据安全合规培训",
  "show_footer": true,
  "footer_text": "内部资料，请勿外传",
  "bg_style": "gradient"
}
```

### slides_data.json 结构

每页定义：`page`, `type`（content_area 或 special 或 chart）, `layout`（布局模板名）, `data`（模板变量）。

```json
[
  { "page": 1, "type": "special", "layout": "cover", "data": { "title": "...", "subtitle": "..." } },
  { "page": 2, "type": "content_area", "layout": "ca-bullets", "data": { "title": "...", "points": [...] } },
  { "page": 3, "type": "special", "layout": "chapter-cover", "data": { "number": 1, "title": "...", "desc": "..." } },
  { "page": 4, "type": "content_area", "layout": "ca-cards-3", "data": { "title": "...", "cards": [...] } },
  { "page": N, "type": "special", "layout": "ending", "data": { "thanks": "...", "contact": "..." } }
]
```

### 🔴 内容设计（强制，不可跳过）

**布局分配完成后、进入实现之前，必须逐页写出完整文字内容。**

这是整个流程中最关键的一步。不能只写"标题+1-2句要点"就进入渲染——渲染阶段不增不减文字，只做排版。

#### 内容密度约束

| 页面类型 | 字数要求 | 说明 |
|----------|---------|------|
| cover / chapter-cover / ending | 10-30字 | 极简导航 |
| toc | 30-120字 | 章节标题+简述 |
| ca-bullets / ca-cards / ca-image / ca-timeline / ca-architecture | 100-500字 | 展开阐述 |

**每个 bullet point 可以多句展开，不是每条只能10个字。** 参考PPT的平均展开型页面有300-400字。

#### 输出要求

将完整文字内容写入 `slides_data.json`，每条文字必须是可逐字渲染的最终版本。

> ⚠️ 前端渲染 = 排版。后端内容 = 定稿。两者的职责不可混淆。

### 布局选择指南

| 页面意图 | 推荐 layout |
|----------|-----------|
| 法规/要点罗列 | ca-bullets |
| 对比/并列 | ca-bullets-2col |
| 3 个方案/类型 | ca-cards-3 |
| 4 个方案/类型 | ca-cards-4 |
| 架构图/流程 | ca-architecture |
| 数据展示 | ca-table |
| 案例/截图说明 | ca-image-left / ca-image-right |
| 步骤/时间 | ca-timeline |

输出 Plan 摘要 + 审批闸门。

---

## ⛔ APPROVAL GATE

一次性审批，通过后进入 Implement。

---

## PHASE 2: IMPLEMENT（母版渲染 + 内容区布局注入）

### 渲染管线

```
master_config.json ──→ PM renders base-template.html
                          → 母版HTML（header + footer + {{content-area}} 占位符）

slides_data.json ──→ For each slide:
  1. 根据 type 选择分支:
     - type=special → 读取 references/specials/{{layout}}.html
     - type=content_area → 读取 references/content-areas/{{layout}}.html
     - type=chart → 读取 references/content-areas/{{layout}}.html
  2. 展开模板中的 {{#each}} {{#if}} {{variable}} → 纯HTML
  3. content_area 类型: 注入到母版的 content-area 占位区，包裹 <section class="slide">
     special 类型: template 已自带 <section class="slide">，直接使用
  4. 按 page 排序 → 拼接所有 <section>

拼接所有 <section> → 注入 {{slides}} 占位 → 完整HTML
```

### 并发模型

```
审批通过后，并发 spawn N 个子 agent：

  ┌─ developer-slide-1  (cover, p1)
  ├─ developer-slide-2  (toc, p2)
  ├─ developer-slide-3  (chapter-cover, p3)
  ├─ developer-slide-4  (ca-bullets, p4)
  ├─ developer-slide-5  (ca-cards-3, p5)
  ├─ developer-slide-6  (ca-architecture, p6)
  └─ developer-slide-N  (ending, pN)
         │
    全部返回 → PM 拼接为完整 HTML
```

### 每个子 agent 的 task

```
基于以下信息生成一页 slide 的 HTML 片段：

页面类型: [special | content_area]
布局模板: [从 references/content-areas/xxx.html 或 references/specials/xxx.html 读取]
母版片段: [master-header + master-footer HTML]
内容数据: { title, points, icon, highlight, cards... }
页码: N

要求：
1. 输出 ONLY <section class="slide" data-page="N">...</section>
2. 展开所有 {{#each}} {{#if}} {{variable}} 为纯HTML
3. content_area 类型：模板只输出 .content-area 内部，需自行构造完整 .ppt-slide 结构（master-header + content + master-footer）
4. special 类型：模板已自带完整结构，直接展开变量
5. 严格使用 CSS 变量，不硬编码颜色
6. 内容精确匹配 data，不删减不压缩，不自行发挥
```

### 拼接

PM 收齐所有 slide 片段后：
1. 读取 `assets/base-template.html`
2. 将 slide 片段按页码顺序注入 `{{slides}}` 占位符
3. 注入 icons.svg 内容到 `{{icons}}` 占位符
4. 写入 `output/<slug>-presentation.html`

---

## PHASE 2.5: PPTX EXPORT（可选）

基于 PHASE 2 Plan 产出的结构化内容数据，生成可编辑的 .pptx 文件。

### 执行方式

```bash
python3 scripts/export_pptx.py \
  --input content_data.json \
  --output output/<slug>-presentation.pptx
```

### 与 HTML 管线的区别

| 维度 | HTML | PPTX |
|------|------|------|
| 视觉精度 | 高（像素级控制） | 中（PPTX 排版模型不同） |
| 可编辑性 | 低（需改源码） | 高（原生 PPTX） |
| 图表支持 | Chart.js 交互 | 表格替代（v1，v2 支持原生图表） |
| 生成速度 | 并行子 agent | 单进程顺序 |
| 适用场景 | 演示预览 | 交付/分享/修改 |

### 字体说明

PPTX 不支持 Google Fonts CDN，会使用系统已安装字体。
推荐安装 Noto Sans SC，否则自动回退到 Microsoft YaHei。

### 子 agent 失败处理

- 单个 slide 子 agent 出错 → 重试 1 次（共 2 次尝试）
- 2 次均失败 → 标记该页为占位页（显示"此页生成失败"），继续拼接其余页
- 失败 ≥ 总页数 30% → 停止，标记用户决策
- PM 在拼接前验证所有片段格式（是否以 `<section class="slide"` 开头）

---

## PHASE 3: REVIEW

| # | 检查项 |
|---|--------|
| 1 | 页数与 Plan 一致？ |
| 2 | 结构页出现顺序正确（封面→目录→章封面→内容→结束）？ |
| 3 | 每页布局匹配 Plan？ |
| 4 | 配色/字体统一（CSS 变量）？ |
| 5 | 翻页 JS 正常？ |
| 6 | 内容准确无误？ |

---

## PHASE 4: REPORT

- canvas 预览 HTML
- 输出文件路径
- 列出遗留问题（如有）

---

## 设计系统

详见 `references/design-system.md`。核心固化：

- 主色 `#004D8C` + 透明度层级
- 字体 Noto Sans SC，单字体全层级
- 容器 1280×720，Header 85px
- 卡片 rounded-xl + 2px 半透明边框
- 标签 rounded-full pill 样式

## 模板管理

| 操作 | 路径 |
|------|------|
| 加新 content-area 布局 | 直接创建 `references/content-areas/xxx.html` |
| 加新 special 页面 | 直接创建 `references/specials/xxx.html` |
| 改单个布局 | 直接编辑对应文件 |
| 改配色/设计系统 | 走 KAIFA##（影响所有模板） |
| 改流程 | 走 KAIFA##（编辑 SKILL.md） |

### 文件结构

```
ppt-generator/
├── SKILL.md
├── assets/
│   ├── base-template.html          # 母版系统（v3: Master + content-area 占位）
│   └── icons.svg
├── references/
│   ├── content-rules.md
│   ├── design-system.md            # 设计令牌 + 布局选择指南
│   ├── content-areas/              # [v3 新增] 内容区布局模板（9个）
│   │   ├── ca-bullets.html         # 单列要点
│   │   ├── ca-bullets-2col.html    # 双列要点
│   │   ├── ca-cards-3.html         # 三列卡片
│   │   ├── ca-cards-4.html         # 四列卡片
│   │   ├── ca-image-left.html      # 左图右文
│   │   ├── ca-image-right.html     # 左文右图
│   │   ├── ca-architecture.html    # 架构/流程图
│   │   ├── ca-table.html           # 数据表格
│   │   └── ca-timeline.html        # 时间线
│   └── specials/                   # [v3 新增] 特殊页面模板（3个）
│       ├── cover.html              # 深蓝全屏封面
│       ├── chapter-cover.html      # 章节标题页
│       └── ending.html             # 结束页
├── scripts/
│   └── export_pptx.py
├── tests/
│   └── test_export_pptx.py
└── requirements.txt
```

## 约束

1. **零外部 CSS 依赖**：不引用 Tailwind CDN
2. **唯一外部依赖**：Google Fonts (Noto Sans SC)
3. **图标内嵌**：使用 assets/icons.svg 内联引用
4. **一个风格**：配色/字体写死在 design-system.md，不支持换肤
5. **双轨输出**：HTML 预览 + PPTX 可编辑文件
6. **内容灵活性**：布局驱动密度（精简/标准/展开），废除全局字数上限
7. **v3 母版系统**：content-area 模板不含 header/footer，由母版统一提供
8. **内容先行**：Plan 阶段产出完整文字内容到 slides_data.json，渲染时不删减
