# Release Notes - v0.7.7

## ✨ 功能与体验改进 / Features & Improvements

- **自定义 Gateway URL 支持 / Custom Gateway URL Support**  
  通过新增 `gatewayBaseUrl` 配置项，支持将请求发送到自定义的 Gateway 地址，例如通过 Nginx 反向代理到启用 TLS/HTTPS 的 Gateway。  
  With the new `gatewayBaseUrl` option, requests can be sent to a custom Gateway URL, such as an Nginx reverse proxy in front of a TLS/HTTPS-enabled Gateway.

- **钉钉「思考中」表情反馈 / DingTalk “Thinking” Emotion Feedback**  
  在处理用户消息期间，Connector 会在原消息上贴上「🤔思考中」表情，处理结束后自动撤回，以更直观地展示处理进度。  
  While processing a user message, the connector attaches a “🤔 Thinking” emotion to the original message and automatically recalls it after completion to clearly indicate processing progress.

- **测试基础设施完善 / Testing Infrastructure Enhancement**  
  引入 Vitest 测试框架与多种测试脚本（单次运行、watch、覆盖率、UI、集成测试），为后续质量保障和回归测试打下基础。  
  Introduced the Vitest testing framework and multiple test scripts (run, watch, coverage, UI, integration) to improve quality assurance and regression testing.

- **文档与示例优化 / Documentation & Examples Improvements**  
  更新 README，补充了 OpenClaw 官方连接器定位、Gateway TLS/HTTPS 配置示例、钉钉机器人创建引导图、以及在 OpenClaw 中配置 MCP 触发规则的截图说明。  
  Updated README with official connector positioning, Gateway TLS/HTTPS configuration example, DingTalk bot creation walkthrough images, and screenshots for configuring MCP trigger rules in OpenClaw.

## 🐛 修复 / Fixes

- **媒体元数据与缩略图提取健壮性提升 / More Robust Media Metadata & Thumbnail Extraction**  
  当 ffprobe 或缩略图生成失败（例如环境缺少依赖、视频流缺失）时，不再抛出异常中断主流程，而是安全返回默认元数据或空缩略图，确保消息处理不中断。  
  When ffprobe or thumbnail generation fails (e.g., missing dependencies or video stream), the connector no longer throws and aborts the main flow, but safely returns default metadata or a null thumbnail so message handling continues.

- **音频时长提取兼容性改进 / Audio Duration Extraction Compatibility**  
  使用动态 `import('child_process')` 替代 `require('child_process')`，提升在不同打包/运行环境下的兼容性。  
  Switched from `require('child_process')` to dynamic `import('child_process')` to improve compatibility across different bundling and runtime environments.

- **主动消息用户列表校验 / Proactive Message User List Validation**  
  在向多个用户发送主动消息时，对 `userIds` 列表进行空值过滤，避免因无效用户 ID 导致的请求失败。  
  Filters out empty values from the `userIds` list when sending proactive messages to multiple users, preventing request failures caused by invalid user IDs.

## 📋 技术细节 / Technical Details

### Gateway URL 配置 / Gateway URL Configuration

- `GatewayOptions` 接口新增 `gatewayBaseUrl?: string` 字段，用于指定自定义 Gateway URL（例如 `http://127.0.0.1:18788`）。  
- `streamFromGateway` 中优先使用 `gatewayBaseUrl` 构造请求地址，否则回退到本地端口逻辑：  
  `gatewayBaseUrl ? \`\${gatewayBaseUrl}/v1/chat/completions\` : \`http://127.0.0.1:\${port}/v1/chat/completions\``。  
- 插件配置新增 `gatewayBaseUrl` 字段说明，帮助用户在 TLS/HTTPS 或 Nginx 代理场景下正确配置。

### 钉钉表情反馈逻辑 / DingTalk Emotion Feedback Logic

- 新增 `addEmotionReply`：在处理用户消息前，为该消息贴上「🤔思考中」表情，使用机器人凭证调用 `robot/emotion/reply` 接口。  
- 新增 `recallEmotionReply`：在消息处理完成后的 `finally` 块内调用，撤回之前贴上的表情，通过 `robot/emotion/recall` 接口实现。  
- 以上调用均带有完善的错误日志，失败不会中断主消息处理流程，仅记录警告日志。

### 媒体处理健壮性 / Media Handling Robustness

- `extractVideoMetadata`：  
  - 将 Promise 回调中的错误处理改为返回 `{ duration: 0, width: 0, height: 0 }`，而非直接 reject。  
  - 当未找到视频流时，同样返回默认元数据结构。  
  - 外层 `catch` 中也返回默认元数据，确保调用方不需要对 `null` 做额外分支判断。  
- `extractVideoThumbnail`：  
  - 截图失败时不再 reject，而是 resolve `null`，由上层逻辑决定是否展示缩略图。  
- `extractAudioDuration`：  
  - 使用 `await import('child_process')` 获取 `execFile`，提高 ESM/打包场景下的兼容性。

### 测试与依赖 / Testing & Dependencies

- 在 `package.json` 中：  
  - 将 `test` 脚本更新为 `vitest run`，并新增 `test:watch`、`test:coverage`、`test:ui`、`test:integration` 等脚本。  
  - 新增开发依赖：`@types/node`、`typescript`、`vitest`。  
- 这些变更为后续补充单元测试、集成测试以及 CI 集成提供基础设施支持。

### CI 工作流 / CI Workflow

- 新增 `.github/workflows/issue-to-AI-table.yml`：  
  - 监听 Issue 的创建、重开、关闭、编辑、打标签/去标签等事件。  
  - 将 Issue 的关键信息（编号、标题、内容、状态、链接等）以统一格式推送到配置的 Webhook（`ISSUE_WEBHOOK_URL`）。  
  - 可用于接入内部 AI 分析、需求盘点或看板同步等自动化流程。

## 📥 安装升级 / Installation & Upgrade

```bash
# 通过 npm 安装最新版本 / Install latest version via npm
openclaw plugins install @dingtalk-real-ai/dingtalk-connector

# 或升级现有版本 / Or upgrade existing version
openclaw plugins update dingtalk-connector

# 通过 Git 安装 / Install via Git
openclaw plugins install https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector.git
```

## ⚠️ 升级注意事项 / Upgrade Notes

### 兼容性说明 / Compatibility Notes

- **向下兼容 / Backward Compatible**：本次更新为小版本改进，保留了 v0.7.x 既有行为，对现有配置完全兼容。  
- **推荐使用 `gatewayBaseUrl` 配置 TLS 场景 / Recommended for TLS via `gatewayBaseUrl`**：  
  在通过 Nginx 或其他代理为 Gateway 启用 TLS/HTTPS 的场景下，建议配置 `gatewayBaseUrl`，以确保 Connector 能够直接访问代理层地址。  
- **媒体处理更安全 / Safer Media Handling**：即便视频/音频元数据提取失败，也不会影响消息主流程，仅在日志中记录错误。

### 验证步骤 / Verification Steps

升级到此版本后，建议进行以下验证：

1. **Gateway URL 验证 / Gateway URL Verification**  
   - 配置 `gatewayBaseUrl` 指向你的 Nginx/Gateway 代理地址。  
   - 发送一条消息，确认能够正常与 Gateway 通信。  
2. **钉钉表情反馈验证 / DingTalk Emotion Feedback Verification**  
   - 在钉钉中向机器人发送一条消息。  
   - 确认消息上出现「🤔思考中」表情。  
   - 等待 AI 回复结束后，确认该表情被自动撤回。  
3. **媒体消息兼容性验证 / Media Message Compatibility Verification**  
   - 发送包含视频或音频的消息，在缺少部分 ffmpeg 依赖的环境下确认不会导致整个会话失败，仅记录错误日志。

## 🔗 相关链接 / Related Links

- [完整变更日志 / Full Changelog](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/CHANGELOG.md)
- [使用文档 / Documentation](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/README.md)
- [问题反馈 / Issue Feedback](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues)

---

**发布日期 / Release Date**：2026-03-13  
**版本号 / Version**：v0.7.7  
**兼容性 / Compatibility**：OpenClaw Gateway 0.4.0+

