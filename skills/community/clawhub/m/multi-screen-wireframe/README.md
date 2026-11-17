# Multi-Screen Wireframe

**语言 / Language:** [中文](README.md) | [English](README.en.md)

**Skill 版本：`2.1.0`**（见 `VERSION`）

**交付格式：`vue-global@2`**

**作者：** [reaidea](https://reaidea.com/)

从产品需求或视觉参考，生成**可双击打开**、可继续由 AI 编辑的多屏线框原型。

打开原型后怎么用画板、演示、修改、注释、导出等功能，见 **[使用说明](docs/使用说明.md)**（[English](docs/user-guide.md)）。

v2 交付物自带业务源码、Vue 3 Global Build、画板与导出能力。无需构建、Node.js、包管理器、网络、本地服务器或目录授权；修改业务 `.js` / CSS 后刷新 `index.html` 即可。

## 能做什么

- **多屏页面流**：画布总览 + 演示模式跳转（`links` / `to`）
- **桌面 / 移动**：SideNav、TabBar、表格、表单、弹层等线框组件
- **灰阶线框**：几何占位图标；有参考图时按测量还原布局
- **导出**：单页 PNG / 多页 ZIP
- **修改 Prompt**：单选 / 多选 DOM 节点添加意见，以黄色编号标记并浮动查看，生成可继续编辑和复制给 AI 的 Prompt
- **页面 / 模块注释**：蓝色注释标记，本机自动保存；可编辑、删除、导入 / 导出 JSON，并批量同步到原型源码
- **帮助与快捷操作**：键盘切换画板、演示、交互锁、修改、沉浸、全屏与热区；按 `?` 查看完整清单
- **界面语言**：画板 chrome 支持简体中文 / 繁体中文 / 英文；默认跟随浏览器，可在设置中切换
- **可配置索引**：画板索引可拖拽、关闭，并按项目记住显示开关
- **无需构建、可继续改**：业务源码按 screen 拆成普通 `.js`；保存后刷新浏览器
- **屏级错误隔离**：单个 screen 编译或运行失败时显示错误卡，其他页面继续工作

### 功能示意

多屏画板总览（桌面 demo）：

![多屏画板总览](docs/screenshots/01-api-client-board.png)

演示模式跳转：

![演示模式](docs/screenshots/04-api-client-demo.png)

修改模式：点选节点、整理修改清单并生成 Prompt：

![修改模式](docs/screenshots/02-api-client-modify.png)

帮助 / 快捷键 / 设置与画板索引：

![帮助与设置](docs/screenshots/03-api-client-help.png)

移动端多屏画板：

![移动端画板](docs/screenshots/05-travel-app-board.png)

移动端演示：

![移动端演示](docs/screenshots/06-travel-app-demo.png)

## 不适合

- 高保真视觉稿 / 设计系统落地
- 真实后端联调、鉴权、路由框架
- 需要 SFC、TypeScript、Vite 或 npm 组件生态的正式 Vue 应用
- 只要单页静态说明、不要多屏画板

## v1 / v2 兼容边界

| 交付物 | 识别方式 | 编辑方式 | framework 升级 |
| --- | --- | --- | --- |
| v1 React/JSX | `.jsx`、`src/app.jsx`、build 脚本或 `framework/tools/esbuild-*` | 读取交付物自己的 `AGENTS.md` / `EDITING.md`，修改后重新构建 | 只使用 v1 framework |
| v2 Vue Global | `project.formatVersion === 2` 且 `framework/FORMAT_VERSION` 为 `vue-global@2` | 修改普通 `.js` / CSS，刷新浏览器 | 只使用 `vue-global@2` framework |

更新 Skill 不会自动改动已经生成的 v1 原型。不要给 v1 项目覆盖 v2 framework，也不要把 v1 项目顺手改写为 Vue。需要迁移时必须明确提出，并在新目录中转换，保留原目录作为回退。

v1 React/JSX 最终版保存在 Git tag `v1.8.0`。v2 从 `v2.0.0` 起作为主线维护，不提供旧组件 API 的运行时兼容层。完整 breaking changes 见 [`CHANGELOG.md`](CHANGELOG.md)。

## 目录说明

| 路径 | 作用 |
| --- | --- |
| `starter/` | 唯一复制源：生成原型时整目录复制到目标路径 |
| `demo/` | 覆盖示例（后台 / 移动），不是复制源 |
| `docs/使用说明.md` | 面向产品/设计的画板功能使用说明（[English](docs/user-guide.md)） |
| `SKILL.md` | 给 AI Agent 的生成、修改、格式识别与迁移约束 |
| `reference.md` | Project、Vue factory、组件和注释协议 |
| `AGENTS.md` | 仓库维护边界与技术约束 |
| `framework-source/` | Board 的 React/JSX 维护源，不进入交付物；编译产物写入 `starter/framework/runtime/board.js` |
| `scripts/` | 创建与检查单个交付物 |
| `tools/check.mjs` | 检查整个 Skill、starter 与 demos |
| `CHANGELOG.md` | major 版本和 breaking changes |

## 安装

本仓库本身就是一个 Agent Skill（根目录有 `SKILL.md`）。任选一种方式接入支持 Skills 的 AI Agent（Cursor、Claude Code、Codex、OpenCode 等）。

### 1. 用 Skills CLI 安装（推荐）

需要本机有 Node.js / npm：

```sh
# 当前项目安装（可随仓库提交，团队共享）
npx skills add ginuim/multi-screen-wireframe

# 全局安装（本机所有项目可用）
npx skills add ginuim/multi-screen-wireframe -g

# 跳过确认；也可指定 Agent，例如 cursor / claude-code / codex
npx skills add ginuim/multi-screen-wireframe -g -y
npx skills add ginuim/multi-screen-wireframe -a cursor -g -y
```

也可用完整仓库地址：

```sh
npx skills add https://github.com/ginuim/multi-screen-wireframe
```

安装后可用 `npx skills check` / `npx skills update` 检查与更新。更多用法见 [skills CLI](https://github.com/vercel-labs/skills) 与 [skills.sh](https://skills.sh/)。

### 2. 把链接直接交给 AI Agent

在对话里贴上仓库地址，让 Agent 按 Skill 执行即可，例如：

> 请按这个 skill 生成多屏线框：https://github.com/ginuim/multi-screen-wireframe
> 先读 `SKILL.md`，再按流程复制 `starter/` 并只改业务 `src/`。

多数支持 Skills / 可读取 GitHub 的 Agent 会据此拉取约定并生成原型。

### 3. 手动克隆到 skills 目录

```sh
git clone https://github.com/ginuim/multi-screen-wireframe.git
```

把克隆目录放到你所用工具的 skills 路径（例如 Cursor / Claude / Codex 各自的 `skills` 目录），或在项目里用符号链接指向该目录。

安装 v1 时使用 `v1.8.0` tag 对应的仓库快照；不要从 v2 主线复制 framework 到 v1 交付物。

## 生成新原型

确认输出路径 → 整目录复制 `starter/` → 只改业务 `src/` → 双击或刷新 `index.html`。

有 Node.js 的 AI 或维护环境可以使用安全复制与静态检查脚本：

```sh
node scripts/create-project.mjs /absolute/path/to/new-prototype
node scripts/check-project.mjs /absolute/path/to/new-prototype
```

这些脚本不是交付物运行依赖；没有 Node.js 时完整复制 `starter/` 并直接用 `file://` 回归即可。

## 修改交付物

进入交付目录后先读：

- `AGENTS.md`：格式、允许修改范围和验证步骤
- `EDITING.md`：Vue Global screen 的完整写法
- `COMPONENTS.md`：Wf 组件 props、事件、插槽和组合方式的权威契约
- `src/screens/_template.js`：页面模板

业务修改只放在 `src/`；页面 title 或新增业务 CSS link 时可改 `index.html`。不要修改 `framework/` 来绕过业务错误。业务 Vue template 节点保留语义 class，关键节点保留全局唯一 id，重复数据节点保留 `data-wf-key`，这样修改 Prompt 和注释中的 DOM 选择器才能稳定映射回源码。

升级 framework 前必须确认 `src/project.js` 的 `format` / `formatVersion` 与 `framework/FORMAT_VERSION` 都属于 `vue-global@2`。只在同一格式和 major 内整夹覆盖 `framework/`，不要覆盖 `src/`。

## 修改并生成 Prompt

传统原型工具直接维护元素的内容、样式和位置；本工具的界面由 AI 生成的业务源码驱动，无法从画面反推该改哪段代码。因此修改模式的作用是：精确定位 DOM 节点，生成带稳定选择器的 Prompt，交给 AI 改 `src/`。

打开原型后点击工具栏「修改」：点选屏内节点；第一次常点到最内层，用层级面包屑切换到父组件。开启「多选」或按住 Shift / Command / Ctrl 点击，可把多个节点绑到同一条意见（例如选两个元素做顺序对调）。每条意见会在所有目标旁显示同一个半透明黄色编号；点击编号浮动查看意见。按住空格可临时拖动画布，松开后继续修改。修改清单会生成 Prompt；Prompt 可继续手动编辑，再一键复制给 AI。

修改记录只保留在当前页面会话中，不会直接改业务源码，也不会生成额外状态文件。AI 应按 Prompt 中的 id / class / `data-wf-key` 搜索 `src/screens/*.js` 中的 Vue template；修改源码后刷新 `index.html`。

## 添加与同步注释

点击工具栏「注释」，可直接选择页面，或点选屏内模块后添加说明、问题和设计决策。注释以蓝色编号标记，可编辑或删除，不承载 Todo / 评审状态。

注释先以操作日志自动保存在当前浏览器，并显示“待同步”数量。点击「复制同步 Prompt」交给 AI，会把操作按稳定 id 幂等合并到 `src/annotations.js`；刷新后注释随原型和 Git 一起保存。浏览器本地存储不可用时应立即导出注释 JSON。

「导出注释 JSON」生成 `<project-id>.wireframe-annotations.json`，可从其他设备或浏览器的注释面板导入并合并。同一项目 id 才允许导入，避免把注释误写到其他原型。JSON 是跨设备交换和备份方式，不是日常必经步骤。

## 快捷键与画板设置

macOS 使用 `Ctrl+1` / `Ctrl+2` 切换画板与演示，`Ctrl+I` 切换交互锁，`Ctrl+M` 切换修改模式；Windows/Linux 使用 `Alt+1` / `Alt+2`、`Alt+I`、`Alt+M`。浏览器全屏使用当前平台修饰键加 `Shift+F`，沉浸模式使用当前平台修饰键加 `3`；缩放使用 `Ctrl+滚轮`。按住 `Space` 临时拖动画布，按 `Esc` 关闭当前面板或退出模式，按 `?` 打开“帮助 / 快捷键”面板。输入框和可编辑内容不会响应普通快捷键；沉浸工具栏同样提供帮助和设置入口。

画板底部索引可通过独立把手拖动，也可直接关闭。工具栏“帮助 / 快捷键 / 设置”面板中的“显示画板索引”可重新开启索引；“默认显示注释标记”可控制普通浏览状态是否展示 Marker，关闭后进入注释模式仍会临时显示。显示状态按项目保存在浏览器本地，拖拽位置只在当前页面会话中保留。同一面板可切换界面语言（简体中文 / 繁体中文 / English）；语言偏好全局保存在本机，与项目设置分开。

## 运行

直接双击交付目录中的 `index.html`。页面通过 `file://` 加载本地 Vue compiler、Wf UI、预编译 Board 与多文件业务源码；不需要执行构建命令。

## Demo

打开（需能解析到共享的 `starter/`）：

- `demo/api-client/index.html` — 桌面 API Client（6 屏，SideNav、DataTable、Tabs、表单）；见上方画板 / 演示 / 修改截图
- `demo/travel-app/index.html` — 移动旅行助手（10 屏，长页面、地图、TabBar、完整表单、弹层与反馈）；见上方移动端截图

demo 只用于覆盖测试，`../../starter/framework/` 是仓库内测试路径。生成用户原型时必须复制完整 `starter/`，不能复制 demo 的 `index.html`。

维护者检查整个 v2 Skill：

```sh
node scripts/check-project.mjs starter
node tools/check.mjs
```

## 给 AI Agent

按 `SKILL.md` 执行：先识别交付格式 → 确认输出目录 → 复制 `starter/` → 只改业务 `src/` → 用 `index.html` 验证画板、演示、视口、导航、修改和注释。组件与 project schema 见 `reference.md`，交付物内组件 API 以 `COMPONENTS.md` 为准。

## 平台与版本

交付物使用 Vue 3 Global Build、React / ReactDOM Board 和本地导出库，版本与许可证位于 `starter/framework/vendor/`。运行不含 esbuild、WASM、Node runtime 或平台相关二进制，适用于支持本地 `file://` 脚本的现代桌面浏览器。

## 作者

由 [reaidea](https://reaidea.com/) 维护，更多作品与文章见 [reaidea Studio](https://reaidea.com/)。
