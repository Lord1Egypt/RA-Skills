# 网关管理参考

## 基本操作
```bash
openclaw gateway status [--deep] [--json] [--no-probe]  # 状态
openclaw gateway start [--json]                          # 启动
openclaw gateway stop [--json]                           # 停止
openclaw gateway restart [--json]                        # 重启
openclaw gateway install [--port N] [--force]            # 安装服务
openclaw gateway uninstall                               # 卸载服务
openclaw gateway --port 18789 --verbose                  # 手动运行(调试)
openclaw gateway --force                                 # 强制启动(杀占用端口)
openclaw gateway call <method> --params '{}'             # RPC调用
openclaw logs --follow                                   # 实时日志
```

## 端口与绑定
- 默认端口: 18789
- 优先级: `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > 18789
- 派生端口: 浏览器=基础+2, Canvas=基础+4
- 绑定地址: `gateway.bind` (loopback|lan|tailnet|custom)
- 非loopback绑定需要认证: `gateway.auth.token`

## 认证
```json5
{
  gateway: {
    auth: {
      token: "your-token",     // 或 ${OPENCLAW_GATEWAY_TOKEN}
      password: "your-pass"    // 备选
    }
  }
}
```

## 配置热重载
- 监视 `~/.openclaw/openclaw.json` 变更
- 默认: `gateway.reload.mode="hybrid"` (安全变更热应用，关键变更重启)
- SIGUSR1 触发进程内重启
- 禁用: `gateway.reload.mode="off"`

## 远程访问
```bash
# SSH隧道
ssh -N -L 18789:127.0.0.1:18789 user@host
# Tailscale (推荐)
gateway.tailscale.enabled: true
gateway.tailscale.hostname: "openclaw"
```

## macOS 服务管理
- LaunchAgent: `~/Library/LaunchAgents/bot.molt.gateway.plist`
- 配置文件模式: `bot.molt.<profile>.plist`
- 安装: `openclaw gateway install`
- 停止: `openclaw gateway stop` 或 `launchctl bootout gui/$UID/bot.molt.gateway`
- 重启: `openclaw gateway restart` 或 `launchctl kickstart -k gui/$UID/bot.molt.gateway`

## Linux 服务管理 (systemd)
- 用户单元: `~/.config/systemd/user/openclaw-gateway[-<profile>].service`
- 需要 lingering: `sudo loginctl enable-linger youruser`
- 启用: `systemctl --user enable --now openclaw-gateway.service`
- 系统单元(多用户): `/etc/systemd/system/openclaw-gateway.service`

## Dev 配置文件 (--dev)
```bash
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
```
- 状态目录: `~/.openclaw-dev`
- 默认端口: 19001
- 工作区: `~/.openclaw/workspace-dev`

## 多Gateway (同一主机)
通常不需要。需要时确保:
- 唯一 `gateway.port`
- 唯一 `OPENCLAW_CONFIG_PATH`
- 唯一 `OPENCLAW_STATE_DIR`
- 唯一 `agents.defaults.workspace`
```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

## 日志
| 类型 | 位置 |
|------|------|
| 文件日志(结构化) | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| macOS服务日志 | `~/.openclaw/logs/gateway.log` + `gateway.err.log` |
| Linux服务日志 | `journalctl --user -u openclaw-gateway.service -n 200` |
| 会话文件 | `~/.openclaw/agents/<agentId>/sessions/` |
| 凭证 | `~/.openclaw/credentials/` |

### 日志级别配置
```json5
logging: {
  level: "info",           // 文件日志级别(debug/info/warn/error/trace)
  consoleLevel: "warn",    // 控制台级别
  consoleStyle: "pretty",  // pretty|json
  redactSensitive: "tools" // off|tools|all
}
```

## 健康检查
```bash
openclaw gateway status          # 服务+探测
openclaw gateway status --deep   # 含系统扫描
openclaw health --json           # 网关健康
openclaw doctor                  # 诊断修复
openclaw doctor --fix            # 自动修复
lsof -nP -iTCP:18789 -sTCP:LISTEN  # 端口占用检查
```

## HTTP API 端点 (同端口)
- `/v1/chat/completions` — OpenAI 兼容 Chat API
- `/v1/responses` — OpenResponses API
- `/tools/invoke` — 工具调用 API
- Canvas: `http://<host>:18793/__openclaw__/canvas/`

## 协议要点
- WebSocket 连接，首帧必须是 `connect`
- 认证: `connect.params.auth.token`
- 事件: agent(流式输出), presence(状态), tick(保活), shutdown(关闭)
- 错误码: NOT_LINKED, AGENT_TIMEOUT, INVALID_REQUEST, UNAVAILABLE
