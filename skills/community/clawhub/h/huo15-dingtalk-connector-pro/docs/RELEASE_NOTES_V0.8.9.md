# Release Notes - v0.8.9

## 🎉 新版本亮点 / Highlights

本次更新带来**引用消息完整解析**、**macOS LaunchAgent 兼容性修复**和**多项稳定性改进**。消息处理层新增对引用消息（reply）的递归解析，支持提取引用中的文本、媒体附件和链接；修复了 macOS LaunchAgent 环境下因无效文件描述符导致 WebSocket 连接失败的问题；同时修复了 AI Card 流式关闭的竞争条件、FormData CJS 互操作问题，并锁定 axios 版本以提升依赖稳定性。

This release introduces **quoted message parsing**, **macOS LaunchAgent compatibility**, and **multiple stability improvements**. The message handler now recursively parses quoted (reply) messages, extracting text, media attachments, and URLs. A fix for invalid file descriptors (EBADF) on macOS LaunchAgent environments prevents WebSocket connection failures. Additionally, the AI Card streaming close race condition is fixed, FormData CJS interop issues are resolved, and axios is pinned to v1.6.0 for dependency stability.

## ✨ 功能与体验改进 / Features & Improvements

- **引用消息完整解析 / Quoted message full parsing**  
  新增 `extractQuotedMsgText` 递归解析引用消息（最多 3 层嵌套），支持 text、richText、picture、video、audio、file、markdown、interactiveCard 等消息类型。引用消息中的媒体附件（图片/视频/音频/文件）会被自动提取并传递给下游处理。引用了含链接的文本消息时，链接会被提取用于 URL 路由（如 alidocs 文档链接）。  
  Added `extractQuotedMsgText` for recursive quoted message parsing (up to 3 levels), supporting text, richText, picture, video, audio, file, markdown, and interactiveCard message types. Media attachments in quoted messages are automatically extracted and passed downstream. URLs from quoted text messages are extracted for URL routing (e.g., alidocs document links).

- **新增配置项 / New configuration options**  
  `configSchema` 新增 `asyncMode`、`ackText`、`endpoint`、`debug` 四个配置字段，为异步消息处理和自定义端点提供灵活配置能力。  
  Added `asyncMode`, `ackText`, `endpoint`, `debug` to `configSchema`, enabling flexible configuration for async message processing and custom endpoints.

- **普通消息本地图片后处理 / Local image post-processing for normal messages**  
  `sendNormalToUser` 和 `sendNormalToGroup` 新增本地图片上传后处理，发送普通消息时自动将 Markdown 中的本地图片路径上传到钉钉并替换为 media_id，与 AI Card 消息行为保持一致。  
  Added local image upload post-processing to `sendNormalToUser` and `sendNormalToGroup`, automatically uploading local image paths in Markdown to DingTalk and replacing them with media_id, consistent with AI Card message behavior.

## 🐛 修复 / Fixes

- **macOS LaunchAgent 环境 WebSocket 连接失败 / WebSocket connection failure on macOS LaunchAgent**  
  修复 macOS LaunchAgent/daemon 环境下，进程启动时 stdin/stdout/stderr（fd 0/1/2）无效（EBADF），导致 Node.js 创建 TCP 连接时出现 EBADF 错误。启动前检测并将无效 fd 重定向到 `/dev/null`。  
  Fixed EBADF errors when creating TCP connections on macOS LaunchAgent/daemon environments where stdin/stdout/stderr (fd 0/1/2) are invalid at process startup. Invalid file descriptors are now detected and redirected to `/dev/null`.

- **AI Card 流式关闭竞争条件 / AI Card streaming close race condition**  
  修复 `closeStreaming` 可能被 `onIdle` 和 `onError` 同时触发时的竞争条件。现在在函数开头立即捕获并清空 `currentCardTarget`（snapshot 模式），防止并发调用导致 `finishAICard` 收到 null 参数而崩溃。  
  Fixed a race condition where `closeStreaming` could be triggered simultaneously by `onIdle` and `onError`. Now captures and clears `currentCardTarget` at function entry (snapshot pattern), preventing concurrent calls from passing null to `finishAICard`.

- **FormData CJS 互操作问题 / FormData CJS interop issue**  
  将 `form-data` 从动态 `import()` 改为静态 `import`，修复 jiti/ESM 环境下动态导入 CJS 模块时 `.default` 偶发为 `undefined` 导致 `Cannot read properties of undefined (reading 'registry')` 错误的问题。  
  Changed `form-data` from dynamic `import()` to static `import`, fixing intermittent `Cannot read properties of undefined (reading 'registry')` errors caused by `.default` being `undefined` when dynamically importing CJS modules in jiti/ESM environments.

- **纯文本图片路径误转换 / Bare image path false conversion**  
  禁用纯文本中本地图片路径的自动转换为图片语法的行为。此前纯文本中出现的本地路径（如 `/path/to/image.png`）会被自动包裹为 `![](mediaId)`，影响用户只想展示路径文本的场景。  
  Disabled automatic conversion of bare local image paths in plain text to image syntax. Previously, local paths like `/path/to/image.png` in plain text were automatically wrapped as `![](mediaId)`, which was undesirable when users intended to display the path as text.

## 🔧 内部改进 / Internal Improvements

- **Zod Schema 拆分兼容 Web UI / Zod Schema split for Web UI compatibility**  
  将 `DingtalkConfigSchema` 拆分为 `DingtalkConfigBaseSchema`（纯 ZodObject）和带 `superRefine` 的完整 Schema，解决 `superRefine` 将 Schema 转为 `ZodEffects` 后无法用于 `buildChannelConfigSchema` 生成 JSON Schema 的问题。  
  Split `DingtalkConfigSchema` into `DingtalkConfigBaseSchema` (pure ZodObject) and the full schema with `superRefine`, fixing incompatibility with `buildChannelConfigSchema` JSON Schema generation.

- **configSchema 类型简化 / configSchema type simplification**  
  将 `clientId`、`clientSecret`、`allowFrom`、`groupAllowFrom` 等字段的 JSON Schema 从 `oneOf` 联合类型简化为单一 `string` 类型，移除不再需要的 `secretInputJsonSchema`，降低配置复杂度。  
  Simplified JSON Schema for `clientId`, `clientSecret`, `allowFrom`, `groupAllowFrom` from `oneOf` union types to single `string` type, removing the no-longer-needed `secretInputJsonSchema`.

- **reply-dispatcher logger 统一 / reply-dispatcher logger unification**  
  将 `reply-dispatcher.ts` 中手动构建的 log 对象替换为 `createLoggerFromConfig`，与项目其他模块的日志规范保持一致。  
  Replaced manually constructed log object in `reply-dispatcher.ts` with `createLoggerFromConfig`, aligning with the project's logging conventions.

- **锁定 axios 版本 / Pin axios version**  
  将 `axios` 依赖从 `^1.6.0` 锁定为 `1.6.0`，避免自动升级引入不兼容变更。  
  Pinned `axios` dependency from `^1.6.0` to `1.6.0` to prevent automatic upgrades from introducing incompatible changes.

## 📥 安装升级 / Installation & Upgrade

```bash
# 通过 npm 安装最新版本 / Install latest version via npm
openclaw plugins install @dingtalk-real-ai/dingtalk-connector

# 或升级现有版本 / Or upgrade existing version
openclaw plugins update dingtalk-connector

# 通过 Git 安装 / Install via Git
openclaw plugins install https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector.git
```

## 🔗 相关链接 / Related Links

- [完整变更日志 / Full Changelog](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/CHANGELOG.md)
- [使用文档 / Documentation](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/README.md)

---

**发布日期 / Release Date**：2026-03-31  
**版本号 / Version**：v0.8.9  
**兼容性 / Compatibility**：OpenClaw Gateway 0.4.0+
