# Kindle Claude Monitor

> 把吃灰的 Kindle 变成 Claude Code 的状态监视屏。

![status](https://img.shields.io/badge/status-stable-brightgreen) ![platform](https://img.shields.io/badge/platform-macOS-lightgrey) ![license](https://img.shields.io/badge/license-MIT-blue)

Claude Code 在长任务里会停下来等你确认权限。如果你不盯终端，常常卡 5 分钟没人管。

这个 skill 把所有 Claude Code hook 事件转发到本地 HTTP server，渲染成大字号黑白 HTML——Kindle / 旧手机 / iPad / 桌面副屏，任何带浏览器的二屏一眼可见 Claude 在做什么、要不要你确认。

## 灵感

字节笔记本 2026-05-26 的《把盖泡面的 Kindle 变成 Claude Code 的监视屏》—— idea 来自他，独立实现 + 工程化（多 session 粘性锁、tool stall 推断、超时兜底、reset 端点、launchd 守护）。

## 长这样

| 状态 | 视觉 |
|---|---|
| 就绪 / 思考中 / 执行中 | 白底大字 + 工具名 |
| **请 确 认** | 反白震动 + 项目名 + 提示框 |
| 已完成 | 白底大字 |

## 安装

```bash
git clone https://github.com/heavenchenggong/kindle-claude-monitor.git \
  ~/.claude/skills/kindle-claude-monitor

bash ~/.claude/skills/kindle-claude-monitor/install.sh
```

`install.sh` 做这几件事：

1. 拷 `server.py` / `notify.sh` 到 `~/.claude/kindle-monitor/`
2. 渲染并装 launchd plist 到 `~/Library/LaunchAgents/com.user.kindle-monitor.plist`
3. 启动 server（绑定 0.0.0.0:8787）
4. 在 `~/.claude/settings.json` 的 `hooks` 里 append 7 个 kindle 钩子（不动既有 hooks）
5. 检测 macOS 防火墙隐身模式，提示用户手动关
6. 报告 Mac 局域网 IP，告诉你 Kindle 上输入哪个 URL

## Kindle 配置

1. 接同一 WiFi
2. 实验性浏览器 → 输入 `http://<Mac-IP>:8787/`
3. 加书签

如果 Kindle 显示"无法连接"，多半是 macOS 防火墙隐身模式：

```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode off
```

## 工作原理

```
Claude Code (Mac)
   ├─ hook (PreToolUse / Notification / Stop / ...)
   │      ↓
   ├─ ~/.claude/kindle-monitor/notify.sh   (透传 stdin + 后台 POST)
   │      ↓
   ├─ Python HTTP server (port 8787, launchd 守护)
   │      ↓
   └─ HTML (meta refresh 每 3s)  ← Kindle 浏览器
```

## 关键设计点

### 1. waiting 是粘性锁（多 session 不打架）
A session 等确认时，B session 跑工具不会冲掉 banner。其他 session 的事件用 `~` 前缀加在事件流里。

### 2. tool stall 推断
**Claude Code 不一定为每次权限确认都触发 Notification hook**——这是 hook 系统实际行为。本 skill 改用补充逻辑：
- PreToolUse 后 20 秒还没等到 PostToolUse → 自动判定为"等待确认"
- PostToolUse 一来立刻还原（误判自动恢复）

### 3. 三层兜底防止锁死
- 5 分钟超时自动解锁
- 每次浏览器刷新都查超时
- `/reset` 端点手动重置

### 4. e-ink 友好
纯黑白配色（waiting 反白震动）、大字号 + sans-serif、meta refresh（不用 WebSocket，Kindle 实验浏览器不支持）。

### 5. hook 透传不阻塞
`notify.sh` 先把 stdin 原样吐到 stdout，POST 走后台 + 1s 超时——hook 失败永远不会拖慢 Claude Code。

## 端点

| 路径 | 用途 |
|---|---|
| `/` | 仪表盘（meta refresh 3s） |
| `/raw.json` | 原始 state JSON（debug） |
| `/healthz` | 健康检查 |
| `/reset` | 紧急清空所有状态 |
| `/event` (POST) | hook 入口 |

## 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `KINDLE_MONITOR_PORT` | 8787 | HTTP server 端口 |
| `KINDLE_MONITOR_REFRESH` | 3 | meta refresh 秒数 |
| `KINDLE_MONITOR_TOOL_STALL` | 20 | PreToolUse 后 N 秒未 PostToolUse 推断为 waiting |
| `KINDLE_MONITOR_WAITING_TIMEOUT` | 300 | waiting 锁超时秒数（5 分钟兜底） |

改值后改 `~/Library/LaunchAgents/com.user.kindle-monitor.plist` 的 `EnvironmentVariables` 块，再 `launchctl unload && load` 一次。

## 卸载

```bash
bash ~/.claude/skills/kindle-claude-monitor/uninstall.sh
```

会停 launchd、删 plist、从 settings.json 移除 7 个钩子（不动其他）。历史日志 `events.jsonl` 默认保留。

## 故障排查

| 现象 | 修法 |
|---|---|
| Kindle 转圈连不上 | macOS stealth mode 把 LAN 包丢了 → `sudo socketfilterfw --setstealthmode off` |
| 浏览器都连不上 | server 没起 → `launchctl list \| grep kindle-monitor`；看 `~/.claude/kindle-monitor/launchd.err.log` |
| Mac 端能开 localhost 但 Kindle 连不上 | Mac IP 变了 → `ipconfig getifaddr en0` 拿新 IP；路由器后台给 Mac 设静态 DHCP 一劳永逸 |
| 一直卡在「请确认」但实际没在等 | 浏览器开 `/reset`，或等 5 分钟超时 |
| 短命令偶发误判为 waiting | 调大 `KINDLE_MONITOR_TOOL_STALL`（默认 20s） |
| 事件流里看到 `~PreToolUse` | 来自其他 session 的事件被锁住时只追加不抢 banner（这是设计行为） |

## 兼容性

- macOS（launchd 必需）
- 理论上 Linux 也能跑（去掉 launchd 用 systemd 重写一下），但未测试
- Kindle Paperwhite / Oasis / Basic 的实验性浏览器都能跑
- 也可以用旧 iPhone / iPad / Android 平板代替 Kindle

## License

MIT
