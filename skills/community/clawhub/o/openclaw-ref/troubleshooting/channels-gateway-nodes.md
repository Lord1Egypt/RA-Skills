# 渠道排错

## Telegram
| 问题 | 解决 |
|------|------|
| 群组不响应非提及消息 | BotFather `/setprivacy` → Disable，移除重新添加机器人 |
| 完全看不到群组消息 | 群组必须在 `groups` 中列出或用 `"*"` |
| 命令不工作 | 确认用户ID已授权(配对或allowFrom) |
| IPv6导致静默失败 | `network.autoSelectFamily: false` 或 `/etc/hosts` 强制IPv4 |
| 分块流式不工作 | `blockStreamingDefault: "on"` + `streamMode: "off"` |
| `setMyCommands failed` | 出站HTTPS/DNS被阻止 |

## WhatsApp
| 问题 | 解决 |
|------|------|
| 未关联/断开 | `openclaw channels login` 重新扫描二维码 |
| 重连循环 | `openclaw doctor` 或重启网关 |
| 消息不触发 | 检查 `allowFrom` 中的号码格式(E.164) |
| Bun运行时不稳定 | 切换到Node运行时 |

## Discord
| 问题 | 解决 |
|------|------|
| "Used disallowed intents" | 开发者门户启用 Message Content Intent |
| 不回复服务器消息 | 检查权限+意图+allowlist+requireMention |
| `groupPolicy` 默认阻止 | 设为 `open` 或添加guild到配置 |
| `requireMention` 不生效 | 必须在 `guilds.<id>` 下，不是顶层 |

## Signal
| 问题 | 解决 |
|------|------|
| signal-cli启动慢 | 设置 `startupTimeoutMs` 或用外部守护进程模式 |
| 收不到消息 | 检查 `signal-cli` 守护进程是否运行 |
| 自己的消息被忽略 | 使用单独的bot号码 |

## 通用
| 问题 | 解决 |
|------|------|
| 消息未触发 | 1. 发送者在白名单? 2. 群聊需提及? 3. 查日志 |
| 渠道未启动 | `openclaw channels status` 检查 |
| 渠道日志 | `openclaw channels logs --channel <name>` |
| 多渠道冲突 | 检查端口和token配置 |

# 网关+节点排错

## 网关问题
| 问题 | 解决 |
|------|------|
| 配置无效无法启动 | `openclaw doctor --fix` |
| 端口被占用 | `lsof -nP -iTCP:18789 -sTCP:LISTEN` → `kill <PID>` |
| 服务已安装没运行 | `openclaw gateway status` → `openclaw logs --follow` |
| 卡在Starting | `openclaw gateway stop` → 检查端口 → 重启 |
| "set gateway.mode=local" | `openclaw config set gateway.mode local` |
| 高内存 | `session.historyLimit: 100` 或定期重启 |
| 配置热重载失败 | 检查JSON语法 → `openclaw doctor` |

## macOS特有
| 问题 | 解决 |
|------|------|
| 权限提示崩溃 | `tccutil reset All bot.molt.mac.debug` |
| LaunchAgent不启动 | `openclaw gateway install --force` |
| 端口冲突 | `launchctl bootout gui/$UID/bot.molt.gateway` |

## Linux特有
| 问题 | 解决 |
|------|------|
| systemd服务不启动 | `sudo loginctl enable-linger $USER` |
| 浏览器无法启动 | 安装Google Chrome，设置 `browser.executablePath` |
| 日志查看 | `journalctl --user -u openclaw-gateway.service -n 200` |

## 节点问题
| 问题 | 解决 |
|------|------|
| 节点未发现 | `openclaw nodes status` 检查配对状态 |
| 配对待批准 | `openclaw nodes pending` → `openclaw nodes approve <id>` |
| 节点离线 | 检查节点主机网络和服务状态 |
| Exec在节点失败 | 检查 `tools.exec.security` 和审批配置 |
