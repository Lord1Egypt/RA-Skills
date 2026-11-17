# Demo 维护约定

本目录只用于覆盖测试，不是生成项目的复制源。

- demo 的 `index.html` 使用 `../../starter/framework/`，这是仓库内共享 runtime 的测试路径，只在当前位置有效。
- AI 参考 demo 时只读取 `src/` 中的业务状态、template 和样式写法；禁止把 demo `index.html` 或它的 framework 路径复制到交付物。
- 新项目必须通过根目录 `scripts/create-project.mjs` 完整复制 `starter/`；交付物路径固定为 `framework/...`。
- Wf 组件 API 以 `starter/COMPONENTS.md` 为准，不以 demo 用法反推完整契约。
