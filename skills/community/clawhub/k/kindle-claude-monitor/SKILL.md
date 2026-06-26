---
name: kindle-claude-monitor
description: 把闲置 Kindle / 旧手机 / 任意空闲屏幕变成 Claude Code 的状态监视屏。用户说「把 Kindle 变成 Claude Code 状态屏」/「Claude Code 状态监视屏 / monitor / 仪表盘」/「让 Claude 等确认时通知我」/「多 session 监控」/`/kindle-claude-monitor` 时触发。本机 Python HTTP server 接收 hooks 事件，渲染 e-ink 友好的纯黑白仪表盘——「思考中 / 执行中 / 请确认 / 已完成」一眼可见。多 session 下 waiting 状态有粘性锁。
metadata:
  type: skill
  scope: global
---

# Kindle Claude Monitor

把吃灰的 Kindle 变成 Claude Code 的状态屏。

灵感来自字节笔记本 2026-05 的「把盖泡面的 Kindle 变成 Claude Code 的监视屏」一文，独立实现 + 工程化。

## 触发方式

- 用户说「把 Kindle 变成 Claude Code 状态屏」
- 用户说「Claude Code 状态监视屏 / monitor / 仪表盘」
- 用户说「让 Claude 等确认时通知我」
- 用户说「多 session 监控」
- `/kindle-claude-monitor`

## 它解决什么

Claude Code 在长任务里会停下来等用户确认（PermissionRequest / Notification），如果不盯终端容易卡很久没人管。这个 skill 把所有 hook 事件转发到本地 HTTP server，渲染成大字号 HTML，让任何带浏览器的二屏（Kindle / 旧手机 / iPad / 桌面副屏）都能远远扫一眼看到状态。

## 架构

```
Claude Code (Mac)
   ├─ hook (PreToolUse / PostToolUse / Notification / Stop / ...)
   │      ↓
   ├─ ~/.claude/kindle-monitor/notify.sh   (透传 stdin + 后台 POST)
   │      ↓
   ├─ Python HTTP server (port 8787, launchd 守护)
   │      ↓
   └─ HTML (meta refresh 每 3s)  ← Kindle 浏览器
```

## 5 个状态

| 状态 | 触发事件 | 视觉 |
|---|---|---|
| 就绪 | SessionStart / SessionEnd | 白底大字 |
| 思考中 | UserPromptSubmit / PostToolUse | 白底大字 |
| 执行中 | PreToolUse | 白底大字 + 工具名 + 输入摘要 |
| **请 确 认** | Notification | **反白震动** + 项目名 + 消息框 |
| 已完成 | Stop | 白底大字 |

## 关键设计点（和"随便撸一个"的区别在哪）

### 1. waiting 是粘性锁
单 session 监控容易被多 session 干扰：A 在等确认时，B 跑了一个 PreToolUse 直接把 banner 冲掉。本 skill 引入 `waiting_session` 字段——一旦某 session 进入 waiting，**其他 session 的事件只追加到事件流（带 `~` 前缀）但不抢 banner**。

### 2. 三层兜底防止锁死
- 5 分钟超时自动解锁（避免虚拟 session / 异常关闭导致永久卡死）
- 每次浏览器刷新都查超时
- `/reset` 端点手动重置

### 3. e-ink 友好的视觉
- 纯黑白配色（waiting 反白震动）
- 大字号 + 单一 sans-serif，无渐变阴影圆角
- meta refresh，不用 WebSocket（Kindle 实验浏览器不支持现代 JS）

### 4. hook 透传不阻塞
notify.sh 用 `printf '%s' "$INPUT"` 把 stdin 原样吐到 stdout，POST 走后台 + curl 1s 超时——hook 失败永远不会拖慢 Claude Code。

### 5. macOS launchd 守护
配 KeepAlive=true，进程崩了自动重启；开机自启。

## 安装

```bash
# 1. 克隆
git clone https://github.com/heavenchenggong/kindle-claude-monitor.git \
  ~/.claude/skills/kindle-claude-monitor

# 2. 跑安装脚本
bash ~/.claude/skills/kindle-claude-monitor/install.sh
```

`install.sh` 会做这些事：
- 把 `server.py` / `notify.sh` 拷到 `~/.claude/kindle-monitor/`
- 把 launchd plist 写到 `~/Library/LaunchAgents/` 并启动
- 在 `~/.claude/settings.json` 的 hooks 里 append 7 个 kindle 钩子（不动既有 hooks）
- 处理 macOS 防火墙隐身模式（如有需要会提示用户用 sudo 关闭）
- 报告 Mac 局域网 IP，告诉你 Kindle 上输入什么 URL

## Kindle 端配置

1. Kindle 接同一 WiFi
2. Menu → Experimental Browser → 输入 `http://<Mac-IP>:8787/`
3. Menu → Bookmark this page

## 端点

| 路径 | 用途 |
|---|---|
| `/` | 仪表盘（meta refresh 3s） |
| `/raw.json` | 原始 state JSON（debug） |
| `/healthz` | 健康检查 |
| `/reset` | 紧急清空所有状态（包括卡死的 waiting 锁） |
| `/event` (POST) | hook 调用入口 |

## 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `KINDLE_MONITOR_PORT` | 8787 | HTTP server 端口 |
| `KINDLE_MONITOR_REFRESH` | 3 | meta refresh 秒数 |
| `KINDLE_MONITOR_WAITING_TIMEOUT` | 300 | waiting 锁超时秒数 |

改了之后改 plist 里的 EnvironmentVariables 块，然后 `launchctl unload && launchctl load` 一次。

## 卸载

```bash
bash ~/.claude/skills/kindle-claude-monitor/uninstall.sh
```

会停 launchd、删 LaunchAgents plist、从 settings.json 移除 7 个 kindle 钩子（保留其他不动）。

## 故障排查

| 现象 | 原因 | 修法 |
|---|---|---|
| Kindle 转圈连不上 | macOS stealth mode 把 LAN 包丢了 | `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode off` |
| 浏览器都连不上 | server 没起来 | `launchctl list \| grep kindle-monitor` 看是否 running，看 `~/.claude/kindle-monitor/launchd.err.log` |
| Mac 端能开 localhost 但 Kindle 连不上 | Mac IP 变了 | `ipconfig getifaddr en0` 拿新 IP，路由器后台给 Mac 设静态 DHCP 租约一劳永逸 |
| 显示一直停在「请确认」但没在等 | 虚拟 session 锁死 | 浏览器开 `http://<Mac-IP>:8787/reset`，或等 5 分钟 |
| 事件流里看到 `~PreToolUse` | 来自其他 session 的事件被锁住时只追加不抢 banner | 这是设计行为，不是 bug |

## 致谢 / Inspiration

字节笔记本《把盖泡面的 Kindle 变成 Claude Code 的监视屏》（公众号 2026-05-26）—— 提供了核心 idea。本实现独立完成，加了多 session 粘性锁、超时兜底、reset 端点、launchd 守护这些工程化细节。
