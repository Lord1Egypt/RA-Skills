---
version: "1.0.0"
name: "project-cookbook-latex"
description: "Creates source-level 80k+ word project CookBooks as LaTeX, PDF, and EPUB. Invoke for websites/docs/repos requiring deep technical books."
---
> **Bilingual note**: This English edition mirrors `SKILL.zh-CN.md`. For the authoritative Chinese version, see `SKILL.zh-CN.md`.


# Project CookBook LaTeX Generator

本 Skill 用于根据用户提供的网站、在线文档、仓库源码、本地文档、API 说明、论文或其他项目资料，生成一套关于该项目的深度 CookBook。目标产物包括：**章节化 LaTeX 工程、编译后的 PDF、从 LaTeX/结构化源生成的 EPUB、图表源文件、图表图片、非空封面图、参考资料清单、字数统计与构建验证报告**。

> 核心原则：本 Skill 的最终排版源应优先是 **LaTeX**，而不是 Markdown。Markdown 只能作为临时大纲、笔记或内容暂存；不得把 Markdown 表格、代码围栏或原始 Markdown 片段直接塞进 LaTeX/PDF 正文。



## ⚠️ Security & Side-Effects Disclosure

| Behaviour | Default | Rationale |
|---|---|---|
| Network access | OFF | Only fetch remote resources when user explicitly approves. |
| Host toolchain install | OFF / fail-closed | Never auto-run `pip install`, `npm install -g`, `apt install`, etc. Report missing deps and wait for manual confirmation. |
| LaTeX `-shell-escape` | OFF | Disabled by default; only enabled when user consents AND environment is sandboxed AND content is trusted. |

**Core principles:**

1. Offline by default — all side-effects require explicit user consent.
2. Fail closed on missing dependencies — never auto-install packages.
3. Never enable `-shell-escape` on untrusted input.
4. Pin remote fetches to release tags (never master/main) — require user approval before network access.

## ⚠️ 安全与副作用声明

| 行为 | 默认值 | 说明 |
|---|---|---|
| 网络访问 | 关闭 | 仅在用户明确同意后访问网络资源。 |
| 主机工具链安装 | 关闭 / 失败即止 | 不会自动运行 `pip install`、`npm install -g`、`apt install` 等。缺失依赖时报告给用户并等待手动确认。 |
| LaTeX `-shell-escape` | 关闭 | 默认不启用 `-shell-escape`；仅在用户明确同意、沙箱/容器化环境、受信内容三者同时满足时才可开启。 |

**核心原则：**

1. 默认离线，所有副作用需用户明确同意。
2. 缺失依赖时**失败即止**，不自动安装任何包。
3. 对不受信内容禁用 `-shell-escape`。
4. 远程获取资源时**固定版本/标签**，不追踪 master/main，并需用户批准。

## 灵活输入支持

本技能接受多种输入格式：

| 输入类型 | 说明 |
|---|---|
| Markdown / TXT 文件 | 最常见输入，直接处理。 |
| JSON 结构化数据 | 包含 `title`、`chapters[]`、`content` 字段时作为结构化大纲处理。 |
| 直接 LLM 上下文 | 当用户以对话方式提供内容时，自动从上下文提取大纲与正文。 |
| URL / 仓库地址 | 仅在用户明确同意后抓取远程内容。 |

## Trigger Conditions

当用户提出以下任一需求时，应调用本 Skill：

- 根据某个项目的网站、文档、源码或仓库生成详细 CookBook、教程、架构手册、源码解析书籍。
- 要求内容覆盖项目调用方式、API 使用方式、实现架构、源码级实现细节。
- 要求使用 `elegantbook-latex` 生成 LaTeX 项目、PDF 或书籍排版。
- 要求输出 PDF、EPUB、LaTeX 工程等多格式交付物。
- 要求生成架构图、调用图、类图、时序图、流程图等工程图表。
- 要求长篇技术书籍，尤其是 **8 万字以上** 的项目 CookBook。
- 用户反馈已有 CookBook 存在如下问题时，也应调用本 Skill 进行修复：Markdown 表格源码出现在 PDF、表格太挤、代码块被切分、封面为空白、内容体量不足、EPUB 样式差或 LaTeX 工程不可复现。

## Required Linked Skills

本 Skill 是编排型 Skill。执行时应按需调用以下 Skills：

1. `research-guide`
   - 用于网络资料检索、官方文档优先级判断、交叉验证、引用规范。
   - 当需要从网站、文档、博客、论文、GitHub 等来源收集项目信息时调用。

2. `drawio`
   - 用于生成架构图、模块关系图、部署图、数据流图、调用链图等可视化图表。
   - 适合复杂系统结构图、分层架构图、组件关系图。

3. `plantuml`
   - 用于生成类图、时序图、活动图、组件图、状态机图、用例图等源码级工程图。
   - 适合从源码结构、类关系、调用流程中抽象图表。

4. `elegantbook-latex`
   - 用于生成或优化 ElegantBook LaTeX 工程。
   - 用于优化 LaTeX 书籍样式、章节结构、封面、目录、代码块、中文字体、表格与整体排版。

5. `epub-reader-optimizer`
   - 用于优化 EPUB 阅读体验，修复 CSS、字体、深色模式、表格、代码块等问题。
   - 当从 LaTeX/HTML 生成 EPUB 后需要进一步美化时调用。

6. `pdf`
   - 当需要检查、合并、压缩、提取或验证 PDF 时调用。

7. `md-image-to-tos`
   - 仅当用户明确要求 Markdown/EPUB 图片上传图床，或 EPUB 必须使用远程图片链接时调用。

## Overall Goals

生成一套面向开发者、架构师和高级使用者的项目 CookBook，要求：

- **内容长度目标为 8 万字以上**，除非用户明确要求更短。不得用“字符数”“token 数”“LaTeX 源码字节数”冒充字数。
- 不只介绍使用方法，还要解释实现原理、架构设计、源码组织、关键模块和调用链。
- 精确到源代码具体实现方式，包括关键文件、核心类/函数、调用关系、配置项、扩展点、异常处理与性能设计。
- 使用图表提高可读性，包括但不限于：
  - 项目整体架构图
  - 模块分层图
  - 运行时调用链图
  - 核心类图
  - API 请求时序图
  - 数据流图
  - 生命周期图
  - 插件/扩展机制图
  - 部署拓扑图
  - 错误处理流程图
- **必须有非空封面图片**。封面图优先从官方品牌资源、项目官网、仓库资源、Wikimedia Commons、Unsplash、Pexels 等来源搜索和选择；若许可证不明确，必须记录“许可证未知，不声明可商用”。
- 所有外部图片必须记录来源 URL、作者或页面信息（如果可得）、许可证信息（如果可得）。
- 最终交付至少包含：
  - LaTeX 工程目录
  - 编译后的 PDF
  - 优化后的 EPUB
  - 图表源文件（PlantUML / draw.io）
  - 图表图片文件（PNG/SVG/PDF）
  - 封面图片及来源说明
  - 参考资料或 sources 文件
  - 字数统计文件 `metadata/word-count.txt`
  - 构建脚本或构建说明
  - 验证报告 `dist/validation-result.md`

## Mandatory Quality Gates

生成完成前必须通过以下检查；不通过则继续修复，不得直接交付：

1. **PDF 中不得出现 Markdown 表格源码**：不得出现大段 `| --- | --- |`、未转义 Markdown 管道表格、Markdown 代码围栏 ```、`![alt](url)` 形式图片引用。
2. **表格必须是 LaTeX 表格环境**：普通表格使用 `booktabs`，宽表格使用 `tabularx` 或 `xltabular`，跨页表格使用 `longtable` 或 `xltabular`，必要时使用横向页面。
3. **代码块必须是 LaTeX 代码环境**：优先使用 `tcolorbox + listings` 或 `listings`，不得将代码作为普通段落输出。
4. **代码块和表格尽量不被切分**：短代码/短表格使用 `samepage`、`minipage`、`tcolorbox[breakable=false]` 或 `needspace` 保护；长代码和长表格允许跨页，但必须使用可读的跨页样式。
5. **表格不得过挤**：表格必须设置合理列宽、行距、字号与自动换行。不得为了塞进页面盲目使用过小字号或全表强制缩放。
6. **封面图片不得空白**：必须检查封面图片文件存在、大小合理，并能在 PDF 中显示。若网络图片下载失败，必须改用可生成的 SVG/PNG 封面或其他可访问图片源。
7. **必须满足 8 万字目标**：若用户没有明确要求更短，必须统计正文中文词/字、英文词和总估算字数，生成 `metadata/word-count.txt`。若不足 8 万字，继续扩写源码解析、Recipe、配置项速查、API 速查、测试与部署章节。
8. **PDF 与 EPUB 均可打开**：PDF 用可用工具检查页数；EPUB 检查 zip 结构，`mimetype` 必须为第一个条目且未压缩。
9. **LaTeX 可复现编译**：必须提供 `build.ps1` 或等价构建说明，并记录编译命令和结果。
10. **引用可追踪**：关键事实、外部图片、官方文档和源码路径必须出现在 sources 或 references 中。

## Workflow

### 1. Input Confirmation & Scope Definition

先识别用户提供的信息类型：

- 官方网站 URL
- 在线文档 URL
- GitHub/GitLab/代码仓库 URL
- 本地源码目录
- 本地文档、PDF、Markdown、Word、网页导出文件
- API 文档或 OpenAPI/Swagger 文件
- 项目名称但未提供资料

如果缺少关键输入，应简洁询问：

- 项目名称或项目资料来源是什么？
- 是否需要覆盖源码级实现？如果是，源码仓库或本地目录在哪里？
- 目标读者是谁：初学者、业务开发者、框架贡献者、架构师？
- 期望输出语言是什么？默认与用户语言一致。

若用户已提供足够信息，不要过度询问，直接开始。

### 2. Research & Data Collection

资料优先级：

1. 官方文档、官方仓库、官方 API reference。
2. 源码、示例项目、测试用例、变更日志、RFC、设计文档。
3. 作者博客、维护者演讲、issue/PR 讨论。
4. 高质量技术博客、论文、课程、社区实践。
5. 其他二手资料。

执行要求：

- 对官方文档和源码进行优先分析。
- 网络资料必须交叉验证，不能只依赖单一博客。
- 对关键事实保留来源链接。
- 若遇到受限网页无法抓取，不得绕过限制；应说明无法访问并改用可访问来源。
- 对源码仓库应识别语言、构建系统、目录结构、入口文件、核心模块、测试与示例。

### 3. Source-Level Analysis

如果有源码，必须分析：

- 项目结构与目录职责。
- 构建系统与依赖管理。
- 核心入口点。
- 主要 API 暴露方式。
- 核心类、函数、模块、接口。
- 配置加载流程。
- 插件/扩展机制。
- 请求/任务/事件/数据处理主链路。
- 错误处理与日志机制。
- 并发、缓存、队列、异步、生命周期管理。
- 测试体系与典型测试用例。
- 性能优化与安全边界。

源码引用要求：

- 章节中应明确写出关键文件路径。
- 对重要函数/类给出职责说明、输入输出、调用者与被调用者。
- 示例代码应尽量来自项目真实 API；如为伪代码，必须标注。
- 不要大段复制源码。应摘取关键片段并解释。

### 4. CookBook Structure Design

推荐 8 万字以上 CookBook 章节结构如下，可按项目类型调整：

```text
00 前言与阅读指南
01 项目概览与问题域
02 快速开始与最小可运行示例
03 安装、环境与构建系统
04 项目调用方式总览
05 API 设计与用户侧编程模型
06 项目整体架构
07 源码目录结构深度导览
08 启动流程与入口点解析
09 核心模块一：职责、接口与实现
10 核心模块二：职责、接口与实现
11 核心模块三：职责、接口与实现
12 关键调用链源码解析
13 配置系统与扩展机制
14 数据模型、状态管理与持久化
15 并发、异步、队列或调度机制
16 错误处理、日志与可观测性
17 性能设计与优化实践
18 安全模型与边界条件
19 测试体系与调试方法
20 部署、集成与生产实践
21 常见任务 CookBook Recipes
22 二次开发与贡献指南
23 与同类项目对比
24 版本演进、路线图与生态
25 总结
附录 A API 速查表
附录 B 配置项速查表
附录 C 核心源码索引
附录 D 图表索引
附录 E 参考资料
```

每章应有明确功能：

- 概念章：解释项目解决的问题。
- 使用章：提供可运行示例。
- 架构章：用图表解释系统边界和模块关系。
- 源码章：按文件、类、函数、调用链展开。
- Recipe 章：提供任务导向的实践方案。
- 附录：提供查表式资料。

### 5. Diagram Planning

必须先建立图表清单，推荐至少包含：

| 图表 | 工具 | 说明 |
|---|---|---|
| 项目整体架构图 | drawio | 展示用户、API、核心模块、外部依赖 |
| 源码目录分层图 | drawio | 展示目录与模块职责 |
| API 调用时序图 | plantuml | 展示用户代码到内部执行路径 |
| 核心类图 | plantuml | 展示核心类、接口、继承/组合关系 |
| 生命周期图 | plantuml | 展示对象、任务、请求或插件生命周期 |
| 数据流图 | drawio 或 plantuml | 展示数据进入、转换、输出过程 |
| 部署拓扑图 | drawio | 展示运行时环境、依赖服务、网络关系 |
| 错误处理流程图 | plantuml | 展示异常捕获、重试、降级、日志 |

图表要求：

- 每张图必须有编号、标题、说明文字。
- 图表必须在正文中被引用，而不是孤立存在。
- 图表源文件和导出图片都应保存。
- PlantUML 图表建议保存为 `.puml` 并导出为 `.svg` 或 `.png`。
- draw.io 图表建议保存为 `.drawio` 并导出为 `.png` 或 `.svg`。

### 6. Images & Cover

封面是强制交付物，不得留空，并且必须遵守 ElegantBook 模板的封面图尺寸规则。

#### 6.1 图源选择规则

1. **优先使用免费可引用图源**：Pixabay、Pexels，或项目官方可公开使用的品牌/文档图片。
2. 若使用 ElegantBook 模板默认示例，应采用 Pixabay 示例图：`https://pixabay.com/en/tea-time-poetry-coffee-reading-3240766/`。
3. 使用 Pixabay/Pexels 图片时，必须记录图片页面 URL、作者/平台、许可证说明与访问日期。
4. 不得使用 iStock、广告位、未知来源、搜索结果缩略图或许可证不可确认的图片作为最终封面。
5. 若项目官方 logo 只适合作为视觉元素，不应直接把 logo 拉伸为整张封面；应叠加在符合尺寸的封面背景图或生成设计图上。

#### 6.2 严格裁剪尺寸

ElegantBook 封面图片最终文件必须严格为：

```text
1280 × 1024
```

更换图片时必须按 5:4 比例裁剪，不得仅依赖 LaTeX 自动缩放。推荐流程：

1. 下载高分辨率原图，保存为 `latex/figures/cover-original.*` 或 `latex/figures/cover-pixabay-original.jpg`。
2. 按 5:4 比例进行中心裁剪或人工裁剪，避免主体被切掉。
3. 将裁剪结果缩放/保存为 `latex/figures/cover.png`，实际像素必须是 `1280×1024`。
4. 可另存 `latex/figures/cover.jpg` 作为备用，但 `main.tex` 中主封面应使用 `\cover{figures/cover.png}`。
5. 在 `metadata/image-sources.md` 中记录裁剪方式：例如“中心裁剪为 5:4，再缩放到 1280×1024”。

#### 6.3 验证规则

编译前后必须检查：

- `latex/figures/cover.png` 存在；
- 图片实际尺寸等于 `1280×1024`；
- `main.tex` 中存在 `\cover{figures/cover.png}`；
- `metadata/image-sources.md` 记录来源 URL、作者/平台、许可证、访问日期、裁剪方式；
- PDF 首页封面非空；
- `dist/validation-result.md` 写明封面来源和实际尺寸。

如果网络图片不可访问，才允许生成 SVG/PNG 兜底封面；兜底封面同样必须输出为 `1280×1024`，并记录“本地生成”。

### 7. LaTeX 优先写作流程

推荐流程是 **先生成结构化 LaTeX 正文，再从 LaTeX 或同源结构化内容生成 EPUB**：

```text
project-cookbook/
  latex/
    main.tex
    chapters/
      00-preface.tex
      01-overview.tex
      ...
    figures/
    diagrams/
    metadata/
      sources.md
      image-sources.md
      word-count.txt
      build-notes.md
  dist/
    Project-CookBook.pdf
    Project-CookBook.epub
    Project-CookBook-LaTeX.zip
```

Markdown 只允许用于：

- 资料笔记；
- 大纲草案；
- EPUB 的临时中间文件；
- sources 记录。

禁止事项：

- 禁止把 Markdown 表格原文直接写入 `.tex`。
- 禁止把 Markdown 代码围栏直接写入 `.tex`。
- 禁止把 Markdown 图片语法直接写入 `.tex`。
- 禁止以“已经有 Markdown，所以 PDF 就用 Markdown 源码展示”的方式偷工减料。

### 8. LaTeX 工程组织

使用 `elegantbook-latex` 生成或优化 LaTeX 工程。推荐结构：

```text
<ProjectName>-CookBook/
  latex/
    main.tex
    elegantbook.cls
    reference.bib
    build.ps1
    chapters/
      00-preface.tex
      01-overview.tex
      02-quickstart.tex
      ...
      appendix-a-api-reference.tex
      appendix-b-config-reference.tex
      appendix-c-source-index.tex
    figures/
      cover.jpg
      architecture-overview.png
      api-sequence.svg
      core-class-diagram.svg
    diagrams/
      architecture-overview.drawio
      api-sequence.puml
      core-class-diagram.puml
    metadata/
      sources.md
      image-sources.md
      word-count.txt
      build-notes.md
  dist/
    <ProjectName>-CookBook.pdf
    <ProjectName>-CookBook.epub
    <ProjectName>-CookBook-LaTeX.zip
    validation-result.md
```

LaTeX 要求：

- `main.tex` 只负责全局配置和 `\input{chapters/...}`。
- 每章一个 `.tex` 文件，按编号命名。
- 长章节可拆分为 `chapters/chapter-xx/section-yy.tex`，但主章节入口仍保持清晰。
- 中文技术书籍优先使用清晰的章节标题和交叉引用。
- 图表统一放在 `figures/`，图表源文件放在 `diagrams/`。
- 参考文献统一在 `reference.bib` 或 `metadata/sources.md` 中维护。

### 9. LaTeX 表格规范

表格必须手工或程序化转换成真正的 LaTeX 表格环境。不得以 Markdown 原文显示。

#### 9.1 推荐宏包

在 `main.tex` 中至少准备：

```latex
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xltabular}
\usepackage{longtable}
\usepackage{array}
\usepackage{makecell}
\usepackage{multirow}
\usepackage{threeparttable}
\usepackage{pdflscape}
\usepackage{needspace}
\renewcommand{\arraystretch}{1.25}
\setlength{\tabcolsep}{5pt}
```

#### 9.2 表格选择规则

- 3 列以内、行数较少：使用 `table + tabularx + booktabs`。
- 列很多或说明很长：使用 `tabularx`，长文本列使用 `X` 或 `p{}`，不要用 `l l l l l` 硬挤。
- 行数很多可能跨页：使用 `xltabular` 或 `longtable`，设置重复表头。
- 横向宽表：使用 `pdflscape` 的 `landscape` 环境，而不是把字号缩到不可读。
- 表格前使用 `\Needspace{8\baselineskip}`，减少表格标题与表格主体分离。

#### 9.3 表格样式要求

- 使用 `\toprule`、`\midrule`、`\bottomrule`，避免竖线。
- 文本列必须自动换行。
- 数字列可右对齐，文本列左对齐。
- 表格字号通常用 `\small`，最多用到 `\footnotesize`；不得全书滥用 `\scriptsize`。
- 表格过宽时优先改列宽、拆表、横向页面，不要简单 `\resizebox{\textwidth}{!}{...}`。
- 每个表格必须有 `\caption{}` 和稳定 `\label{tab:...}`。
- 表格后应有解释段落，不得让表格孤立。

#### 9.4 Markdown 表格转换检查

生成或修复 LaTeX 后必须搜索：

```text
|---
---|
| --- |
```

如果 `.tex` 正文中仍有 Markdown 表格痕迹，必须立即转换为 LaTeX 表格。

### 10. LaTeX 代码块规范

代码块必须使用专业代码环境，避免作为普通文本或 Markdown 源码出现。

#### 10.1 推荐宏包与样式

优先使用 `tcolorbox + listings`，因为它可以控制分页、边框、背景、标题和断行：

```latex
\usepackage{listings}
\usepackage[most]{tcolorbox}
\lstdefinestyle{cookbookcode}{
  basicstyle=\ttfamily\small,
  breaklines=true,
  breakatwhitespace=true,
  columns=fullflexible,
  keepspaces=true,
  showstringspaces=false,
  frame=none,
  tabsize=2
}
\newtcblisting{codeblock}[2][]{
  listing only,
  listing style=cookbookcode,
  title={#2},
  breakable,
  enhanced,
  colback=gray!3,
  colframe=gray!45,
  boxrule=0.4pt,
  arc=2mm,
  left=1.5mm,
  right=1.5mm,
  top=1mm,
  bottom=1mm,
  fonttitle=\bfseries\small,
  #1
}
```

#### 10.2 分页规则

- 短代码块（约 40 行以内）尽量不要切分：使用 `\Needspace{12\baselineskip}`，或 `tcolorbox` 设置 `breakable=false`。
- 长代码块可以切分，但必须保持标题、边框、背景和行断开可读。
- 不要使用 `verbatim` 作为默认代码样式，因为它难以美化和控制分页。
- 长路径、长 URL、长命令必须允许断行，避免 overfull box。

#### 10.3 代码内容规则

- 代码示例应短而聚焦，避免复制大段源码。
- 源码级解析应更多解释调用链，而不是堆砌源码。
- 若代码来自真实项目，应标注文件路径和符号名。

### 11. PDF 生成

PDF 生成要求：

- 使用 XeLaTeX 或 LuaLaTeX 编译，以保证中文支持。
- 至少执行两遍编译以生成目录和交叉引用。
- 检查 PDF 是否包含封面、目录、章节、图表、参考资料。
- 若出现 LaTeX 编译错误，应优先修复：
  - 特殊字符转义问题。
  - 图片路径问题。
  - 中文字体问题。
  - 表格过宽或 Markdown 表格未转换问题。
  - 代码块过宽或代码环境错误问题。
  - 引用或标签缺失问题。
- Overfull box 警告若来自表格或代码，应尽量通过列宽、断行、横向页面或代码样式修复；不得忽略明显影响阅读的溢出。

### 12. EPUB 生成与优化

EPUB 推荐流程：

1. 以 LaTeX 工程为权威内容源。
2. 从 LaTeX 生成结构化中间 HTML/EPUB，或从与 LaTeX 同源的章节结构生成 EPUB。Markdown 仅可作为中间格式，不作为主要交付格式。
3. 保留章节目录结构、代码高亮、图片、表格和图注。
4. 使用 `epub-reader-optimizer` 优化 CSS、字体、颜色、代码块和表格。
5. 检查 EPUB zip 结构：`mimetype` 必须是第一个条目且未压缩；必须包含导航文件。
6. 检查 EPUB 在常见阅读器中的基本可读性。

注意：

- LaTeX/PDF 书籍样式优化应交给 `elegantbook-latex`。
- EPUB 阅读体验优化应优先交给 `epub-reader-optimizer`。
- 如果从 LaTeX 直接转 EPUB 效果差，可从同一份结构化章节数据生成 HTML/EPUB，但内容必须与 LaTeX 同步，不能缺章或删减关键内容。

### 13. 8 万字内容扩写策略

若生成内容不足 8 万字，应按以下优先级扩写，而不是填充空话：

1. **源码级逐模块解析**：每个核心目录、核心类、关键函数都包含职责、入口、调用者、被调用者、状态变化、异常路径、扩展点。
2. **调用链章节**：从 CLI/API 调用到内部引擎、调度器、下载器、解析器、输出管线的完整链路。
3. **配置项速查与场景解释**：每个重要配置项包含默认值、作用、源码使用位置、调优建议、常见误区。
4. **Recipes**：至少 20 个任务导向 Recipe，每个 Recipe 包含目标、适用场景、步骤、代码、原理、常见坑、扩展建议。
5. **测试与调试**：测试结构、典型测试用例、mock/stub、日志、性能诊断、内存排查。
6. **生产部署与运维**：配置分层、容器化、CI、监控、告警、限流、重试、数据质量。
7. **同类项目对比**：从架构、性能、扩展性、适用场景、生态等维度比较。
8. **附录**：API 速查表、配置项速查表、核心源码索引、图表索引、术语表。

字数统计要求：

- 生成 `metadata/word-count.txt`。
- 统计时应排除 LaTeX 命令、宏包声明、目录、构建脚本和重复样板。
- 同时输出：中文字符数、英文词数、估算总字数、章节数、Recipe 数、表格数、代码块数、图表数。
- 若最终低于 8 万字，必须在最终回复中明确说明“不满足 8 万字”及原因；默认情况下应继续补足。

### 14. 质量标准

最终内容必须满足：

- 不少于用户要求的目标体量。若技术或上下文不足以达到 8 万字，应明确说明缺口，并通过源码分析、Recipe、附录、API 表、配置表补足。
- 章节结构完整，逻辑从入门到源码深入再到实践。
- 每个关键结论有来源或源码依据。
- 每个核心模块至少包含：职责、入口、关键类型、关键函数、调用链、边界条件、扩展点。
- 每个 Recipe 至少包含：目标、适用场景、步骤、代码示例、实现原理、常见坑。
- 图表与正文互相引用。
- PDF 与 EPUB 均可打开。
- LaTeX 工程可复现编译。
- PDF 不得包含 Markdown 表格源码。
- 封面图片非空且来源可追踪。

### 15. 推荐执行清单

执行时可使用如下 Todo：

```text
1. 收集项目资料与源码入口
2. 建立资料索引与引用清单
3. 分析项目结构、调用方式和核心源码
4. 设计 8 万字 CookBook 章节大纲
5. 搜索/生成非空封面图片并记录来源
6. 规划图表清单
7. 直接生成 LaTeX 章节正文，而不是先生成最终 Markdown
8. 生成 draw.io 与 PlantUML 图表并导出图片
9. 将表格转换为 booktabs/tabularx/xltabular/longtable 环境
10. 将代码转换为 tcolorbox/listings 环境
11. 编译 PDF 并修复表格、代码、封面、字体和溢出问题
12. 从 LaTeX 或同源结构化内容生成 EPUB
13. 使用 epub-reader-optimizer 优化 EPUB
14. 统计字数并补足到 8 万字以上
15. 校验 PDF、EPUB、ZIP、封面、表格、代码、引用和最终交付物
```

### 16. 输出交付格式

最终回复用户时必须提供可打开的文件链接，至少包括：

- PDF 文件链接
- EPUB 文件链接
- LaTeX 工程压缩包或项目目录中的主文件链接
- Sources 文件链接
- 字数统计文件链接
- 验证报告链接

回复应简洁说明：

- 已生成哪些文件。
- 内容覆盖哪些核心部分。
- 是否达到 8 万字。
- 如果有未完成项或资料限制，应明确说明。

## 常见失败点与优化策略

### 失败点：PDF 中出现 Markdown 表格源码

优化：所有 `| A | B |`、`|---|---|` 必须转换为 LaTeX 表格。编译前 grep `.tex` 文件，发现 Markdown 表格立即修复。

### 失败点：表格太挤

优化：使用 `tabularx` / `xltabular` / `longtable`，长文本列设为 `X`，增加 `\arraystretch`，必要时拆表或横向页面。不要盲目缩放整表。

### 失败点：代码块被切得难以阅读

优化：短代码块使用 `Needspace` 或不可分页 `tcolorbox`；长代码块允许分页但使用 `breakable` 样式、清晰边框和自动断行。

### 失败点：封面图片空白

优化：必须验证图片存在并可显示。网络图片失败时改用其他可访问来源，或生成 SVG/PNG 封面兜底。记录图片来源。

### 失败点：内容过浅或不足 8 万字

优化：必须从源码文件、API 调用、执行链路、配置项、测试用例、Recipe、附录中补充细节，而不是只总结官网。生成字数统计并按缺口补写。

### 失败点：图表孤立

优化：图表必须在正文中被解释和引用，例如“如图 6-1 所示”。

### 失败点：LaTeX 工程混乱

优化：严格使用 `main.tex + chapters/ + figures/ + diagrams/ + metadata/ + dist/` 的结构。

### 失败点：EPUB 样式差

优化：使用 `epub-reader-optimizer` 修正 CSS、代码块、表格和字体。从 LaTeX 或同源结构化内容生成 EPUB，避免和 PDF 内容不一致。

### 失败点：图片版权不清

优化：记录来源，不确定许可证时仅作为参考素材，并在 sources 中标注许可证未知。

### 失败点：8 万字不可验证

优化：构建时统计 LaTeX 正文字数，并生成 `metadata/word-count.txt`。

### 失败点：源码引用不精确

优化：每个源码分析小节至少给出文件路径、符号名、职责和调用关系。

## 示例用户请求

```text
请基于 https://example.com/docs 和这个 GitHub 仓库生成一个 8 万字以上的项目 CookBook，要求输出 PDF、EPUB、LaTeX，并包含架构图和源码级解析。
```

应调用本 Skill，并联动 `research-guide`、`drawio`、`plantuml`、`elegantbook-latex`、`epub-reader-optimizer`、`pdf`。

## 示例最终产物目录

```text
ExampleProject-CookBook/
  latex/
    main.tex
    chapters/
    figures/
      cover.jpg
    diagrams/
    metadata/
      sources.md
      image-sources.md
      word-count.txt
      build-notes.md
  dist/
    ExampleProject-CookBook.pdf
    ExampleProject-CookBook.epub
    ExampleProject-CookBook-LaTeX.zip
    validation-result.md
```
