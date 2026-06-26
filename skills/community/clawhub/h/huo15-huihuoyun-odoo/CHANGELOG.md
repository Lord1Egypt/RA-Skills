# Changelog

## 1.23.2 — 2026-05-11(manifest runtimeExtensions — 让 OpenClaw 2026.5.x 找到 dist/)

### 触发

OpenClaw 2026.5.x gateway / `openclaw doctor` 启动报：

```
plugins.entries.odoo: plugin odoo: installed plugin package requires
  compiled runtime output for TypeScript entry index.ts: expected
  ./dist/index.js, ./dist/index.mjs, ./dist/index.cjs, ...
```

### 根因

OpenClaw 2026.5.x `dist/discovery-CVL9-KJt.js` 在加载 npm 安装的插件时,对 `package.json.openclaw.extensions` 里 `.ts` 入口要求显式声明编译产物路径(`runtimeExtensions[]`)。

### 改动

`package.json` 加 `openclaw.runtimeExtensions: ["./dist/index.js"]`,显式告诉 OpenClaw ts entry 编译后的 JS 在哪。dist/index.js 已经由 prepublishOnly 自动生成。

### 不影响

代码逻辑不变,只动 manifest。

