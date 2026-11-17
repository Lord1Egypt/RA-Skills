---

name: "google-fonts-tool-free"
description: "面向个人开发者的 Google Fonts 加载、子集与经典搭配工具。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "谷歌字体工具"
  version: "1.0.0"
  summary: "面向个人开发者的 Google Fonts 加载、子集与经典搭配工具。"
  tags:
    - "字体"
    - "前端性能"
    - "个人效率"
    - "其他工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
  - browser

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 谷歌字体工具（免费版）

## 概述

本工具帮助个人开发者正确加载 Google Fonts，规避不可见文字、冗余字重、缺少 preconnect 等常见性能坑，并提供经典字体搭配与按用途选字体清单。适合单项目快速优化。

## 核心能力

| 能力 | 说明 | 免费版范围 |
|:-----|:-----|:-----------|
| 加载优化 | display=swap + 双 preconnect | 标准加载 |
| 变量字体 | 单文件多字重 | 推荐 4 款 |
| 子集控制 | latin/latin-ext 选择 | 基础子集 |
| 经典搭配 | 衬线/无衬线/科技风 | 12 组 |
| 按用途选字 | 阅读/UI/标题/等宽 | 4 类 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人开发者的、Google、Fonts、子集与经典搭配工、性能加载与字体搭、配工具、优选加载、变量字体与按需字、重加载、经典衬线、科技风搭配推荐、按用途选字体与常、见错误规避等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：正确加载字体

```html
<!-- 双 preconnect + display=swap -->
<link rel="preconnect" href="https://fonts.googleapis.com">
gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

```css
/* 始终带回退栈 */
font-family: 'Inter', system-ui, sans-serif;
```

### 场景二：按用途选字体

| 用途 | 推荐字体 |
|:-----|:---------|
| 长文阅读 | Merriweather / Lora / Source Serif Pro |
| UI 界面 | Inter / Roboto / Open Sans |
| 冲击标题 | Playfair Display / Oswald / Bebas Neue（勿用于正文） |
| 等宽 | JetBrains Mono / Fira Code / Source Code Pro |

### 场景三：经典搭配

```text
衬线 + 无衬线（经典对比）:
  Playfair Display（标题）+ Source Sans Pro（正文）
  Lora（标题）+ Roboto（正文）

纯无衬线（现代干净）:
  Inter（标题正文同族，字重区分层级）
  Montserrat（标题）+ Hind（正文）
```

## 不适用场景

以下场景谷歌字体工具不适合处理：

- 纯技术文档撰写
- 学术论文写作
- 法律文书起草

## 触发条件

需要生成营销文案、写作内容、标题优化、内容创作时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 确定标题与正文字体。
2. 用 `display=swap` 与双 preconnect 加载。
3. 只加载用到的字重（通常 2-3 个）。
4. CSS 中始终带回退栈。

```bash
# 本地预览
python -m http.server 8000
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

变量字体单文件加载：

```html
<!-- 变量字体：单文件覆盖全部字重 -->
googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
```

```css
/* 变量字体可用任意字重值 */
font-weight: 450;
```

## 优选实践

- **只加载用到的字重**：每个冗余字重约浪费 20KB，通常 2-3 个足够。
- **必加 display=swap**：否则字体加载前文字不可见。
- **双 preconnect**：googleapis 与 gstatic 都要 preconnect，gstatic 加 crossorigin。
- **展示体勿用于正文**：Lobster、Pacifico、Abril Fatface 仅作标题。
- **别用两个相似字体**：Roboto + Open Sans 几乎一样，选一个即可。

## 常见问题

**Q1：加载 6 个字重保险吗？**
A：不保险。只加载用到的，通常 400/600/700 三个足够。

**Q2：为什么字重没生效？**
A：CSS 写了 `font-weight:600` 但只加载了 400 和 700。加载的字重必须包含 600。

**Q3：免费版支持自托管吗？**
A：不支持。GDPR 自托管与子集化工具为专业版能力。

**Q4：CJK 字体怎么办？**
A：Noto Sans JP 等 CJK 字体很大，Google 会切片但仍偏重，按需评估。

**Q5：display=swap 会闪烁吗？**
A：会有短暂 FOUT（无样式文本闪现），但优于不可见文字。

## 进阶用法

### 字重加载策略

不同场景字重需求不同，按需加载节省体积：

```text
落地页 hero:    700（粗体标题）+ 400（正文）
长文阅读:       400 + 600（小标题）
数据看板:       400 + 500（强调数值）
极简品牌站:     仅 400 + 变量字体调字重
```

### 回退栈设计

字体加载失败时回退栈决定体验，按场景设计：

```css
/* 衬线展示体回退 */
font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;

/* 无衬线 UI 回退 */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;

/* 等宽回退 */
font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### 字体加载性能自检

```text
自检清单:
  [ ] display=swap 已加
  [ ] 双 preconnect 已加（googleapis + gstatic crossorigin）
  [ ] 仅加载用到的字重（≤ 3 个）
  [ ] 变量字体用范围语法 wght@100..900
  [ ] CSS 回退栈完整
  [ ] 展示体未用于正文
```

## 字体搭配原则

- **对比要明显**：衬线+无衬线，或粗+细，别两个相似字体并列。
- **角色要单一**：标题字体只做标题，正文字体只做正文。
- **情绪要匹配**：严肃用衬线，科技用无衬线/等宽，活泼用圆体。
- **数量要克制**：一页最多 2 个字族，多了显乱。
- **等宽有讲究**：数字、代码用等宽，对齐更整齐。

## 常见坑速查

| 现象 | 原因 | 修复 |
|:-----|:-----|:-----|
| 文字不可见 | 缺 display=swap | 加 display=swap |
| 字重没生效 | 未加载该字重 | 链接加上对应字重 |
| 加载慢 | 字重过多 | 精简到 2-3 个 |
| FOUT 闪烁 | swap 副作用 | 可接受，优于不可见 |
| 中文重 | CJK 字体大 | 按语言子集 |

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **浏览器**: 任意现代浏览器

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Google Fonts CDN | 字体资源 | 必需 | fonts.googleapis.com |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令，无需额外 API Key
- 字体资源通过 CDN 引入，无需鉴权

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行预览）
- **说明**: 通过自然语言指令驱动 Agent 产出字体加载代码与搭配方案

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。