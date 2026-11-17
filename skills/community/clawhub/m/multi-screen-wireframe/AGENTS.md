# AGENTS.md — multi-screen-wireframe

本目录是 `multi-screen-wireframe` v2 主线。生成流程见 `SKILL.md`，业务协议见 `reference.md`，当前版本见 `VERSION`。v1 React/JSX 最终版冻结在 Git tag `v1.8.0`。

## 代际边界

- v2 交付格式固定为 `vue-global@2`。`src/project.js` 的 `format` / `formatVersion` 与 `framework/FORMAT_VERSION` 必须一致。
- v1 的 `.jsx`、build 脚本、esbuild 工具和 framework 不进入 v2 starter；不提供旧组件 API 兼容层。
- framework 只允许在相同格式和 major 内整夹更新。禁止 v1 / v2 互相覆盖 framework。
- 迁移 v1 交付物必须由用户明确要求，并在新目录中转换；不得原地覆盖旧项目。

## 维护边界

- 交付复制源永远是整个 `starter/`。
- 生成项目时优先使用 `scripts/create-project.mjs`；环境没有 Node.js 时可完整复制 `starter/`，随后只修改目标副本的 `src/`。
- 不得用 `demo/` 作为复制源；demo 只覆盖复杂交互和长内容。
- demo 共享 `starter/framework/`，其中 `../../starter/framework/` 只是仓库测试路径，不能复制进交付物。
- 仓库根目录不保留可运行的 `framework/`、`src/` 或 `index.html` 镜像；交付内容只以 `starter/` 为准。
- `framework-source/` 只保存 Board 的 React/JSX 维护源码，不进入 starter；入口为 `framework-source/bridge-entry.jsx`。
- 修改 Board 维护源码后重新生成 `starter/framework/runtime/board.js`；其他 runtime、styles、vendor 和 `FORMAT_VERSION` 直接在 `starter/framework/` 维护，再验证 starter 与两个 demo。
- 交付物不加入 esbuild、WASM、Node runtime、包管理器或服务器。

## 组件契约维护

- `starter/COMPONENTS.md` 是 Wf 公共组件的权威 API 文档；生成业务代码前先读它，不扫描 framework 猜测组件用法。
- 任何组件改动都必须在同一次修改中同步更新 `starter/COMPONENTS.md` 及其实现指纹。
- `starter/framework/runtime/ui.js` 的组件增删/改名，以及 props、默认值、事件、插槽、属性透传、DOM/ARIA、导航和布局行为变化，必须同步更新 `starter/COMPONENTS.md`。
- 影响组件公开布局或交互行为的 CSS 修改也必须同步更新组件文档。
- 组件实现变更后更新 `ui-contract-sha256` 并运行 `node tools/check.mjs`；只改指纹、不审阅正文不算完成。

## 版本

- `VERSION`、`package.json`、screen/layout 的 `@wireframe-skill` 和“修改基于”必须同步。
- major 格式变更必须同步 `project.formatVersion`、`starter/framework/FORMAT_VERSION`、README 兼容矩阵和 CHANGELOG。
- starter 和两个 demo 都使用当前版本注释；不得新增根目录业务源码镜像。

## 验证

1. `node scripts/check-project.mjs starter`
2. `node tools/check.mjs`
3. 通过 `file://` 回归 `starter/index.html`、`demo/api-client/index.html`、`demo/travel-app/index.html`
4. 验证控制台、错误隔离、主路径导航、弹层、TabBar、修改、注释和导出

## 文件修改

- 使用 `apply_patch` 编辑文本文件；机械版本替换和目录提升可使用批处理命令。
- 保留与当前任务无关的未跟踪文件和用户修改。
