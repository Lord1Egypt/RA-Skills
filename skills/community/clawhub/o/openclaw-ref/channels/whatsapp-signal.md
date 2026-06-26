# WhatsApp 配置参考

## 快速设置
1. 推荐使用单独手机号码(备用手机+eSIM)
2. 配置 `channels.whatsapp`
3. `openclaw channels login` 扫描二维码
4. 启动网关

### 最小配置
```json5
{ channels: { whatsapp: { dmPolicy: "allowlist", allowFrom: ["+15551234567"] } } }
```

## 两种模式

### 专用号码(推荐)
```json5
channels: { whatsapp: { dmPolicy: "allowlist", allowFrom: ["+15551234567"] } }
```

### 个人号码(备选)
```json5
channels: { whatsapp: { selfChatMode: true, dmPolicy: "allowlist", allowFrom: ["+15551234567"] } }
```
自聊天模式: 给自己发消息测试，不打扰联系人。

## 访问控制
- `dmPolicy`: `pairing`(默认) | `allowlist` | `open` | `disabled`
- `allowFrom`: E.164号码列表(如 `+15551234567`)
- `groupPolicy`: `open` | `allowlist`(默认) | `disabled`
- `groupAllowFrom`: 群组发送者白名单
- 配对: `openclaw pairing approve whatsapp <code>`

## 登录/凭证
```bash
openclaw channels login                    # 扫描二维码
openclaw channels login --account <id>     # 多账户
openclaw channels logout                   # 登出
```
凭证: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`

## 群组
- 会话键: `agent:<agentId>:whatsapp:group:<jid>`
- 激活模式: `mention`(默认需@提及) | `always`
- `/activation mention|always` 切换(仅所有者)
- 历史注入: 最近50条未处理消息作为上下文

## 确认表情
```json5
ackReaction: { emoji: "👀", direct: true, group: "mentions" }
// group: "always"|"mentions"|"never"
```

## 已读回执
```json5
channels: { whatsapp: { sendReadReceipts: false } }  // 全局禁用
```

## 限制
- `textChunkLimit`: 4000字符(默认)
- `mediaMaxMb`: 50MB入站(默认), 5MB出站(agents.defaults.mediaMaxMb)
- 图片自动优化为JPEG

## 重连
```json5
web: { reconnect: { initialMs: 1000, maxMs: 60000, factor: 2, maxAttempts: 10 } }
```

## 常见问题
- 未关联: `openclaw channels login` 重新扫描二维码
- 重连循环: `openclaw doctor` 或重启网关
- 不要用Bun运行时，WhatsApp在Bun上不可靠
- 避免Twilio(24h窗口限制+封锁风险)

# Signal 配置参考

## 快速设置
1. 安装 `signal-cli` (需要Java)
2. `signal-cli link -n "OpenClaw"` 扫描二维码
3. 配置并启动网关

### 最小配置
```json5
channels: {
  signal: {
    enabled: true,
    account: "+15551234567",
    cliPath: "signal-cli",
    dmPolicy: "pairing",
    allowFrom: ["+15557654321"]
  }
}
```

## 访问控制
- `dmPolicy`: `pairing`(默认) | `allowlist` | `open` | `disabled`
- `allowFrom`: E.164号码或 `uuid:<id>`
- `groupPolicy`: `open` | `allowlist`(默认) | `disabled`

## 外部守护进程模式
```json5
channels: { signal: { httpUrl: "http://127.0.0.1:8080", autoStart: false } }
```

## 投递目标
- 私信: `signal:+15551234567` 或纯E.164
- UUID: `uuid:<id>`
- 群组: `signal:group:<groupId>`

## 限制
- `textChunkLimit`: 4000字符
- `mediaMaxMb`: 8MB
- 支持输入指示器和已读回执
