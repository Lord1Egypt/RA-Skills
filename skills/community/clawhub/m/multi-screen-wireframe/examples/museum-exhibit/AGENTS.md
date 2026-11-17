# Vue Global 多屏线框交付物约定

本目录是可直接双击运行的离线原型。日常生成与修改只写 `src/`，不要修改 `framework/`。

## 格式与升级边界

- 本交付物格式是 `vue-global@2`：`src/project.js` 必须声明 `format: 'vue-global'` 和 `formatVersion: 2`，`framework/FORMAT_VERSION` 必须为 `vue-global@2`。
- framework 只能从相同格式和 major 的 v2 starter 整夹更新；不得使用 React/JSX v1 framework，也不得把本 framework 覆盖到 v1 项目。
- 发现 `src/app.jsx`、`src/screens/*.jsx` 或 build 脚本时，目标是 v1 项目；停止本工作流并读取该项目自己的 `AGENTS.md` / `EDITING.md`。
- v1 → v2 迁移必须由用户明确提出，在新目录中完成，不原地转换。

## 组件文档优先

- 生成或修改业务代码前先读 `COMPONENTS.md`；它是 Wf 公共组件的权威 API 契约，优先级高于 demo 和零散示例。
- 普通业务任务禁止为了解 props、事件或插槽而扫描 `framework/runtime/ui.js`、Board、vendor 或维护源码，避免额外上下文和对内部实现产生依赖。
- 只有用户明确要求维护 framework，或 `COMPONENTS.md` 与运行行为不一致时，才读取组件实现；发现不一致必须报告，并在同一次组件改动中同步更新 `COMPONENTS.md`。
- 组件增删/改名，或 props、默认值、事件、插槽、DOM/ARIA、导航、布局和组件样式行为变化，都视为组件改动，必须同步更新 `COMPONENTS.md` 及其实现指纹。

## 源码完整性

- `project.screens` 每个 id 都有对应 `src/screens/<id>.js`。
- screen 文件调用同 id 的 `WireframeVue.defineScreen()`。
- 共享业务组件写入 `src/layouts/` 或 `src/components/`，以 `Wf` 前缀注册，并在 `project.components` 声明。
- 不使用 import/export、JSX、SFC、TypeScript、动态 import 或 npm 依赖。
- 保存后刷新 `index.html`，不执行构建。

## 修改边界

- 业务页面、状态、文案和样式只改 `src/`。
- 页面 title 或新增业务样式 link 时可以改 `index.html`。
- 不修改 `framework/` 来规避 screen 错误。
- 不添加 `dist/`、build 脚本、esbuild、WASM、服务器或目录选择流程。

## 稳定性

- 使用 Composition API；定时器和监听器在 `onUnmounted()` 清理。
- `v-html` 仅绑定源码内受控的静态 / 演示 HTML，或已经过可信清洗器处理的 HTML；不直接渲染用户输入、URL、本地存储或外部数据。
- 所有业务节点使用语义 class；关键节点使用唯一 id；重复节点使用稳定 `data-wf-key`。
- 页面流只写 `screens[].links`；导航使用 Wf 组件的 `to`。
- 移动端使用 `WfMobileShell`，让内容区内部滚动、TabBar 留在 screen 底部。
- 弹层只使用 Wf 反馈组件并相对当前 screen 定位。

完成后检查画板、演示、主路径、屏内状态、修改、注释、导出和错误隔离。
