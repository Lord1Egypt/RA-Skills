---
name: multi-screen-wireframe
description: Create or revise complete offline multi-screen wireframes and page-flow prototypes with Vue 3 Global Build, multi-file JavaScript screens, no build step, no Node dependency in the deliverable, and direct file:// opening. Use for mobile apps, mini-program flows, desktop admin tools, interactive product demos, or visual-reference reconstruction when the output must remain AI-editable without JSX, esbuild, WASM, npm, a local server, or directory-selection permissions.
---

# Multi-Screen Wireframe

生成可直接双击、可继续由 AI 编辑、无需构建的多屏线框交付物。

## 先识别交付格式

修改已有原型时，先读取目标目录自己的 `AGENTS.md` 和 `EDITING.md`，再检查源码格式：

- 若存在 `src/app.jsx`、`src/screens/*.jsx`、`build.command`、`build.cmd` 或 `framework/tools/esbuild-*`，这是 v1 React/JSX 交付物。继续遵守交付物内的 v1 编辑与构建说明；不得复制 v2 `starter/`，不得覆盖其 `framework/`，不得把 `.jsx` 顺手改写成 Vue。
- 若 `src/project.js` 声明 `format: 'vue-global'`、`formatVersion: 2`，且 `framework/FORMAT_VERSION` 为 `vue-global@2`，这是当前 v2 交付物，按本 Skill 修改。
- 若标识缺失或互相冲突，停止框架升级；只做安全的业务源码检查，并向用户报告格式不明确。

v1 与 v2 不提供运行时或组件 API 兼容层。用户明确要求迁移时，必须复制到新的目标目录后转换，保留旧目录作为回退；不得原地迁移或顺带迁移。

## 生成流程

1. 确认用户指定的输出目录；未指定时先询问，不覆盖现有目录。
2. 完整复制 `starter/` 到目标目录。有可用 Node.js 时可从本 Skill 根目录运行 `node scripts/create-project.mjs <目标目录>`；当前环境不能运行 Node.js / `.mjs` 时，使用可用的文件工具复制整个目录，不要求最终用户安装 Node.js。
3. 先定义 `src/project.js`：viewport、screen id、入口、页面说明和唯一页面流边 `links`。
4. 只修改目标副本的 `src/`；必要时修改 `index.html` 的 title 和业务 CSS link。
5. 为每个 screen 创建 `src/screens/<id>.js`，并用同 id 调用 `WireframeVue.defineScreen()`。
6. 共享布局或业务组件放入 `src/layouts/` 或 `src/components/`，用 `Wf` 前缀注册，并按依赖顺序写入 `project.components`。
7. 当前 AI 或维护环境能运行 Node.js / `.mjs` 时，运行 `node <Skill根>/scripts/check-project.mjs <目标目录>`；环境不支持时允许跳过这项脚本校验，继续按第 8 步直接打开 `index.html` 回归，不得为了校验要求产品经理安装 Node.js。
8. 通过 `file://` 打开目标 `index.html`，回归画板、演示、导航、交互、修改、注释和错误隔离。
9. 用户要求导出时，实际验证一张 PNG；多屏导出实际验证 ZIP。

详细业务 schema、状态写法和注释格式见 [reference.md](reference.md)；Wf 组件 props、默认值、事件、slots 和组合示例以复制后的 `COMPONENTS.md` 为权威契约。生成业务代码前先读该文件，不要为查询组件用法扫描 framework 源码。

## 交付边界

复制源永远是整个 `starter/`。生成任务中：

- 只修改目标副本，不修改本 Skill 的 `starter/` 或 `demo/`。
- 只修改目标副本的 `src/`；不得修改 `framework/` 来绕过业务错误。
- 不生成 `dist/`，不加入 build 脚本、esbuild、WASM、npm 依赖或服务器。
- 不要求最终用户选择目录或授权 File System Access API。
- 框架升级只允许在 `project.format`、`project.formatVersion` 与 `framework/FORMAT_VERSION` 均匹配时进行；确认同为 `vue-global@2` 后才可整夹覆盖 `framework/`，并保留 `src/`。

目标交付物保持以下结构：

```text
index.html
framework/                 # 稳定 runtime、Board、样式和离线 vendor
src/
  project.js               # 页面与页面流
  annotations.js           # 固化注释
  screens/<id>.js          # 一屏一文件
  layouts/*.js             # 可选共享布局
  components/*.js          # 可选共享业务组件
  styles/app.css           # 业务样式
AGENTS.md
EDITING.md
README.md
COMPONENTS.md              # Wf 组件权威公开 API
```

## Vue 源码约束

- 使用 Vue 3 Composition API；状态写在 `setup()`，优先 `ref()` 和 `computed()`。
- screen 顶层只调用一次 `WireframeVue.defineScreen(id, factory)`，不声明可碰撞的全局变量。
- 从 factory 参数取得 `ref`、`computed`、生命周期和 screen 上下文；脚本中访问 ref 使用 `.value`，template 自动解包。
- template 必须是当前文件中的非空字符串，由 Vue Global compiler 编译。
- 禁止 import/export、`.vue` SFC、JSX、TypeScript、动态 import、裸 npm 包和本地 fetch。
- Vue Global full build 支持 `v-html`；仅用于当前业务源码内受控的静态 / 演示 HTML，或已经过可信清洗器处理的 HTML。禁止直接绑定用户输入、URL 参数、本地存储、外部 API / CMS 等不可信内容；来源不确定时使用文本插值或组件。
- 不加载在线资源、真实后端、emoji、Unicode 图标或业务语义 SVG。
- `v-for` 必须有稳定 `:key`；实际重复节点同时写稳定 `:data-wf-key`。
- 复杂派生逻辑放进 `computed()`；template 表达式保持简单且无副作用。
- 定时器、监听器和外部资源必须在 `onUnmounted()` 清理。

## Project 与页面流

- `project.format` 固定为 `'vue-global'`，`project.formatVersion` 固定为 `2`；不得删除或改写。
- `screens[].id` 唯一并匹配 `/^[a-z0-9-]+$/`。
- 每个 id 必须存在同名 `src/screens/<id>.js`，禁止只改 project 或只交运行产物。
- `defaultViewport` 必须存在；viewport 宽高必须是正数。
- 每个 screen 都写 `links` 数组；`links` 是页面流的唯一边数据。
- 至少一个 screen 写 `entry: true`。
- 导航用 Wf 组件的 `to="screen-id"`，不引入 Vue Router，不操作 location/hash。
- 共享组件名必须以 `Wf` 开头，避免与原生元素和内置组件冲突。
- `project.components` 的顺序就是加载顺序；依赖其他业务组件的模块必须排在依赖之后。

## DOM 定位协议

Board 的修改与注释能力依赖稳定 DOM：

- 所有业务节点使用英文语义 class，推荐 `<screen-or-module>__<role>`。
- 页面根、标题、主内容、关键卡片/表单/表格/操作/弹层使用以 screen id 开头的唯一 id。
- 重复业务节点使用稳定 `data-wf-key`，不使用数组下标代替业务 id。
- 共享 layout 不写会在多屏画布中重复的 id。
- 不把文字、`is-*` 状态 class、DOM 层级或 `nth-child` 当作定位协议。

每个新建或修改的 screen/layout 文件顶部写：

```js
/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.1.0
 * 修改基于 v2.1.0
 */
```

后续修改保留“创建基于”，只更新“修改基于”和 `@wireframe-skill`。

## 布局与反馈

- 默认灰阶；图标和图片使用圆形、方形、线框块等抽象几何占位。
- 移动端底栏优先使用 `WfMobileShell`；内容区滚动，TabBar 留在 screen 底部，禁止 `position: fixed`。
- 弹层使用 `WfModal`、`WfConfirmDialog`、`WfLoadingOverlay`、`WfToast`，相对单个 screen 定位。
- 业务样式只写 `src/styles/app.css` 或 template 内 `:style`，不修改 `framework/styles/prototype.css`。
- 有参考图时先测量 viewport、区域边界、尺寸、间距、对齐和圆角，再实现。

## 内容完整度

除非用户明确要求单屏、空态或少量样例：

- 覆盖完整主路径，例如列表 → 详情 → 编辑/确认 → 结果。
- 每屏写满关键内容和可演示交互，不交付空壳。
- 列表、表格、Cell 组至少提供 3 条有区分度的数据，并尽量超过一屏可滚。
- `WfEmptyState` 只用于真正无数据的状态，不与已有记录同时出现。

## 注释与修改回归

- 除非用户明确要求添加、固化或导入原型注释，否则不得自行生成页面注释或节点注释；保留 starter 中的空 `src/annotations.js` 即可。
- 正式注释写 `src/annotations.js`，通过 `WireframeVue.defineAnnotations()` 注册。
- 修改模式的 Prompt 只指向业务 `src/` 和 `.js` template，不指示修改 framework。
- 注释同步只修改 `src/annotations.js`；更新 `annotationsRevision`，按稳定 id 幂等合并。
- 回归至少覆盖：关键 id、普通业务 class、重复数据节点、多选修改、Prompt 生成与复制。
- 注释回归至少覆盖：页面注释、节点注释、刷新持久化、同步 Prompt、JSON 导入导出。

## 完成标准

- `project.format`、`project.formatVersion` 与 `framework/FORMAT_VERSION` 一致，未发生跨代 framework 覆盖。
- 有可用 Node.js / `.mjs` 运行环境时，`check-project.mjs` 通过，无缺屏、孤儿 screen、断链、重复 id 或不合规依赖；环境不能运行时可跳过脚本校验，不将 Node.js 作为交付或使用前提。
- `file://` 无目录授权即可启动，控制台无 Vue 编译/运行警告和错误卡。
- 画板与演示模式都能渲染；主路径导航和关键屏内状态可操作。
- 移动端长内容在 shell body 内滚动，TabBar 底边与 screen 底边对齐。
- 单屏故意失败时只显示该 screen 的错误卡，其他 screen 继续工作。

完整实现示例见 `demo/api-client` 和 `demo/travel-app`；demo 只用于覆盖测试。参考 demo 时只看其 `src/` 业务写法，不复制 `index.html` 或其中的 `../../starter/framework/` 仓库测试路径。
