# Release Notes - v0.7.9

## ✨ 功能与体验改进 / Features & Improvements

- **钉钉 Stream 客户端心跳与重连机制优化 / DingTalk Stream Client Heartbeat & Reconnect**  
  关闭 DWClient SDK 内置的激进 keepAlive（避免 8 秒超时强制断连），启用应用层自定义心跳：基于 WebSocket ping/pong，30 秒间隔、90 秒超时，超时后主动断开并重连，重连失败时 5 秒后重试，提升长连稳定性。  
  Disabled the SDK's aggressive keepAlive (which could force disconnect after 8s), and added an application-layer heartbeat: WebSocket ping/pong with 30s interval and 90s timeout; on timeout the client disconnects and reconnects, with a 5s retry on failure, improving long-lived connection stability.

- **DWClient 配置调整 / DWClient Configuration**  
  启用 `autoReconnect: true` 以在连接断开时自动重连；设置 `keepAlive: false`，由应用层心跳替代 SDK 心跳，避免与钉钉服务端策略冲突。  
  Enabled `autoReconnect: true` for automatic reconnection on disconnect; set `keepAlive: false` and rely on application-layer heartbeat to avoid conflicts with DingTalk server behavior.

- **统一停止与清理逻辑 / Unified Stop & Cleanup**  
  停止 Stream 客户端时统一通过 `doStop` 清理心跳定时器并调用 `client.disconnect()`，确保资源释放与连接正确关闭。  
  When stopping the Stream client, a unified `doStop` now clears the heartbeat timer and calls `client.disconnect()` for consistent resource cleanup and connection closure.

## 🐛 修复 / Fixes

- **长连接被服务端或中间网络提前断开 / Long-lived Connection Premature Disconnect**  
  通过应用层心跳检测连接活性，超时后主动重连，减少因长时间无数据导致的静默断连且无法恢复的问题。  
  Application-layer heartbeat detects connection liveness and triggers reconnect on timeout, reducing silent disconnects when the link is idle.

## 📋 技术细节 / Technical Details

### 应用层心跳机制 / Application-Layer Heartbeat

- **参数**：心跳间隔 30 秒（`HEARTBEAT_INTERVAL`），超时 90 秒（`HEARTBEAT_TIMEOUT`），允许约 3 次 ping 无响应后再判定超时。  
- **流程**：定时器每 30 秒通过 `client.socket?.ping()` 发送 ping；监听 `socket.on('pong')` 更新 `lastPongTime`；若当前时间与 `lastPongTime` 差值超过 90 秒则触发重连。  
- **重连**：先 `await client.disconnect()`，再 `await client.connect()`，成功后重置 `lastPongTime`；若重连失败则 5 秒后再次尝试 `client.connect()`。  
- **停止**：`doStop(reason)` 中设置 `stopped = true`、清除心跳定时器、调用 `client.disconnect()`，并记录停止原因与活动。

### DWClient 配置说明 / DWClient Config

- `autoReconnect: true` — 连接断开时由 SDK 参与自动重连。  
- `keepAlive: false` — 关闭 SDK 内置的激进心跳，避免 8 秒无活动即强制断连，由应用层 30s/90s 心跳替代。

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

- **向下兼容 / Backward Compatible**：仅调整 Stream 客户端的心跳与重连策略，对现有配置与 API 无破坏性变更。  
- **长连场景建议**：若依赖钉钉 Stream 长连接，升级后将自动使用新的心跳与重连逻辑，无需额外配置。

## 🔗 相关链接 / Related Links

- [完整变更日志 / Full Changelog](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/CHANGELOG.md)
- [使用文档 / Documentation](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/README.md)
- [问题反馈 / Issue Feedback](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues)

---

**发布日期 / Release Date**：2026-03-13  
**版本号 / Version**：v0.7.9  
**兼容性 / Compatibility**：OpenClaw Gateway 0.4.0+
