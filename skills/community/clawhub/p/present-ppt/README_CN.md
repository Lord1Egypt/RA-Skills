# present-ppt

> **present-ppt** Fork 并增强自 [html-slide-to-pptx](https://github.com/mucsbr/ppt-agent-workflow-san/tree/main/html-slide-to-pptx)。
>
> 这是 [mk-present](https://github.com/textboy/mk-present) 项目中的一个 skill。

将结构化的 HTML 幻灯片转换为可编辑的 PowerPoint (.pptx) 幻灯片，包含原生文本框、形状、标签、箭头和面板。

这是一个**预设驱动的转换器**，不是通用的浏览器渲染器。

- 如果 HTML 匹配现有预设，直接转换。
- 如果 HTML 属于新的幻灯片家族，先添加新预设，再转换。

## 本技能擅长

- 分析师风格的固定布局幻灯片
- 架构页面
- AI 运行时 / 流程页面
- 小型 deck 或单页 HTML 设计（可编辑性比任意 CSS 保真度更重要）

## 本技能不是

- 通用的 HTML/CSS 转 PPT 引擎
- 截图导出器
- 响应式网页转换器

## 当前预设支持

### `v9-architecture`

用于接近以下结构的页面：
- 头部标签栏 + 品牌标识
- 标题
- 核心摘要框
- 左侧驱动面板
- 中间分层架构堆栈
- 右侧判断链面板

### `ai-runtime-page`

用于接近以下结构的页面：
- 头部标签栏 + 品牌标识
- 标题 + 引导框
- 输入标签行
- 主运行时框（5 个模块）
- 支撑层卡片
- 输出标签行
- 基础层 + 要点

## 环境要求

- 已安装 Node.js
- 可用的 npm
- 从 `package.json` 安装本地依赖

推荐：Node.js 18+

本技能的核心转换流程**不**需要 Python、Chrome、Playwright 或 LibreOffice。

## 在新机器或新 agent 上安装

```bash
cd <skill-dir>
npm ci
npm run check-env
```

如果 `npm ci` 不可用或因 lockfile 缺失/过时而失败：

```bash
npm install
npm run check-env
```

详细安装说明：见 `references/setup.md`。

## 快速开始

### 1) 验证环境

```bash
npm run check-env
```

### 2) 将 HTML 转换为 PPTX

```bash
node scripts/html_to_pptx.js input.html output.pptx --preset=v9-architecture --dump-model model.json
```

或：

```bash
node scripts/html_to_pptx.js input.html output.pptx --preset=ai-runtime-page --dump-model model.json
```

### 3) 运行 QA / 预检

```bash
node scripts/preflight_qa.js model.json --preset=v9-architecture --report qa.json
```

## 标准工作流

1. 识别幻灯片家族。
2. 阅读 `references/preset-decision-rules.md`，决定是复用、扩展还是替换预设。
3. 如果没有匹配的预设，添加新预设而非硬转换任意 HTML。
4. 将 HTML 转换为 PPTX，可选导出中间模型。
5. 运行 QA / 预检检查。
6. 打开 PPTX 目视检查间距、溢出和箭头方向。
7. 必要时迭代预设映射。

## 如何扩展到新的幻灯片家族

当输入的 HTML 不匹配现有预设时，按三个层次添加支持：

1. **DOM 提取规则**
   - 从 HTML 中提取语义内容到小型模型。
2. **布局 / 渲染映射**
   - 将模型映射为原生 PowerPoint 对象。
3. **QA 规则**
   - 添加预设特定的溢出和间距检查。

参考文件：
- `references/preset-decision-rules.md`
- `references/presets.md`
- `references/preset-template.md`
- `references/qa-heuristics.md`
- `references/roadmap.md`
- `references/usage-principles.md`

## 主要文件

- `SKILL.md` — 面向 AI agent 的指令和触发描述
- `scripts/html_to_pptx.js` — 主要转换入口
- `scripts/preflight_qa.js` — 预检 QA 运行器
- `scripts/check_env.js` — 环境自检
- `scripts/html_to_pptx_v9.js` — v9 预设渲染器
- `scripts/ai_runtime_preset.js` — AI 运行时预设提取器/渲染器

## 故障排查

### `Cannot find module 'cheerio'` 或 `Cannot find module 'pptxgenjs'`

运行：

```bash
npm ci
```

或：

```bash
npm install
```

### 转换在一台机器上正常，在另一台机器上失败

- 在目标机器上重新安装依赖。
- 不要假设复制的 `node_modules/` 在不同环境间可移植。
- 再次运行 `npm run check-env`。

### HTML 结构与现有预设差异较大

不要强行套用旧预设。添加新预设。

## 可移植性说明

另一个 agent 通常可以理解并使用本技能，**前提是**：
- 技能文件夹安装在可见的技能目录中，
- `SKILL.md` 存在，
- 依赖已安装，
- 并且 agent 遵循预设驱动的工作流。

为获得最佳可移植性，分发整个技能文件夹，包括：
- `SKILL.md`
- `package.json`
- `package-lock.json`
- `scripts/`
- `references/`

`node_modules/` 可能有助于本地复用，但不应该作为唯一的安装方式。
