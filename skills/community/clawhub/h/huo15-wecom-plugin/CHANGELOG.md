# Changelog

## 2.9.5 — 2026-05-11(manifest contracts.tools — 适配 OpenClaw 2026.5.x loader 契约)

### 触发

OpenClaw 2026.5.x gateway 启动 log 大量 warning：

```
[gateway] [plugins] plugin must declare contracts.tools before registering agent tools
  (plugin=wecom, source=...dist/index.js)
```

3 个工具(wecom_calendar / wecom_doc / wecom_mcp)各刷一条。

### 根因

OpenClaw 2026.5.x loader(`dist/loader-B-GXgDrk.js`)在 `registerTool` 加了契约校验,要求 manifest 根级 `contracts.tools[]` 显式声明。

### 改动

`openclaw.plugin.json` 加根级 `contracts.tools` 数组：

```json
"contracts": {
  "tools": ["wecom_calendar", "wecom_doc", "wecom_mcp"]
}
```

### 不影响

- 没改任何代码逻辑,只动 manifest
- 工具注册 / 调用方式不变
- 兼容旧 OpenClaw

