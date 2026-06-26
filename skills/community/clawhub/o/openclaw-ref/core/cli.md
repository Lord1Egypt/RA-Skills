# OpenClaw CLI 速查表

| 命令 | 子命令/参数 | 用途 |
|------|------------|------|
| `openclaw setup` | | 初始化配置+工作区 |
| `openclaw onboard` | | 交互式引导向导 |
| `openclaw configure` | | 交互式配置向导 |
| `openclaw config get <path>` | | 读取配置值（点路径） |
| `openclaw config set <path> <value>` | | 设置配置值（JSON5或字符串） |
| `openclaw config unset <path>` | | 删除配置值 |
| `openclaw doctor` | `[--deep] [--yes] [--fix]` | 健康检查+自动修复 |
| `openclaw reset` | `--scope full --yes` | 重置配置/状态 |
| `openclaw uninstall` | `--all --yes` | 卸载服务+数据 |
| `openclaw update` | `[--json]` | 更新 OpenClaw |
| `openclaw status` | `[--all] [--deep] [--usage]` | 会话健康+诊断 |
| `openclaw health` | `[--json]` | 网关健康状态 |
| `openclaw logs` | `--follow` | 跟踪网关日志 |
| `openclaw sessions` | `[--json]` | 列出会话 |
| `openclaw message send` | `--target <dest> --message "text"` | 出站消息 |
| `openclaw agent` | `--message "text" [--to <dest>]` | 运行单次智能体轮次 |
| `openclaw agents list` | `[--json] [--bindings]` | 列出隔离智能体 |
| `openclaw agents add` | `[name] [--workspace <dir>] [--model <id>]` | 添加智能体 |
| `openclaw agents delete` | `<id> [--force]` | 删除智能体 |
| `openclaw gateway status` | `[--deep] [--json] [--no-probe]` | 网关状态 |
| `openclaw gateway start` | `[--json]` | 启动网关 |
| `openclaw gateway stop` | `[--json]` | 停止网关 |
| `openclaw gateway restart` | `[--json]` | 重启网关 |
| `openclaw gateway install` | `[--port N] [--force]` | 安装网关服务 |
| `openclaw gateway uninstall` | | 卸载网关服务 |
| `openclaw gateway call <method>` | `--params '{}'` | RPC调用 |
| `openclaw system event` | `--text "text" [--mode now]` | 注入系统事件 |
| `openclaw system heartbeat` | `last|enable|disable` | 心跳管理 |
| `openclaw models status` | `[--json] [--probe]` | 模型状态 |
| `openclaw models list` | `[--all] [--provider <name>]` | 列出模型 |
| `openclaw models set` | `<provider/model>` | 设置主力模型 |
| `openclaw models set-image` | `<provider/model>` | 设置绘图模型 |
| `openclaw models aliases` | `list|add <alias> <model>|remove <alias>` | 管理别名 |
| `openclaw models fallbacks` | `list|add <model>|remove <model>|clear` | 管理故障转移 |
| `openclaw models scan` | `[--provider openrouter] [--max-candidates 5]` | 扫描免费模型 |
| `openclaw models auth` | `setup-token --provider anthropic` | 认证管理 |
| `openclaw memory status` | `|index|search "query"` | 记忆操作 |
| `openclaw channels list` | `[--json] [--no-usage]` | 列出渠道 |
| `openclaw channels status` | `[--probe]` | 渠道状态 |
| `openclaw channels logs` | `[--channel <name|all>] [--lines 200]` | 渠道日志 |
| `openclaw channels add` | `--channel telegram --account alerts --token $TOKEN` | 添加渠道 |
| `openclaw channels remove` | `--channel discord --account work` | 移除渠道 |
| `openclaw channels login` | `[--channel whatsapp]` | 登录渠道 |
| `openclaw channels logout` | `[--channel whatsapp]` | 登出渠道 |
| `openclaw skills list` | `[--eligible]` | Skills列表 |
| `openclaw plugins list` | `[--json]` | 插件列表 |
| `openclaw plugins install` | `<path|npm-spec>` | 安装插件 |
| `openclaw cron status` | `[--json]` | 定时任务状态 |
| `openclaw cron list` | `[--all] [--json]` | 列出定时任务 |
| `openclaw cron add` | `--name "任务" --cron "0 9 * * *" --message "执行..."` | 添加定时任务 |
| `openclaw cron edit` | `<id> --message "新提示"` | 编辑定时任务 |
| `openclaw cron rm` | `<id>` | 删除定时任务 |
| `openclaw cron enable` | `<id>` | 启用定时任务 |
| `openclaw cron disable` | `<id>` | 禁用定时任务 |
| `openclaw cron run` | `<id> [--force]` | 手动运行定时任务 |
| `openclaw nodes status` | `|list|describe` | 节点状态 |
| `openclaw nodes pending` | `|approve <id>|reject <id>` | 配对管理 |
| `openclaw nodes camera` | `list|snap [--facing front]|clip [--duration 10s]` | 摄像头操作 |
| `openclaw nodes canvas` | `snapshot|present <url>|hide` | Canvas操作 |
| `openclaw nodes screen` | `record [--duration 10s]` | 屏幕录制 |
| `openclaw nodes location` | `get` | 获取位置 |
| `openclaw node run` | `<command>` | 在节点上运行命令 |
| `openclaw browser status` | `|start|stop` | 浏览器控制 |
| `openclaw browser tabs` | `|open <url>|focus <id>|close <id>` | 标签页管理 |
| `openclaw browser screenshot` | `[--selector .class]` | 截图 |
| `openclaw browser snapshot` | `[--refs aria]` | UI快照 |
| `openclaw browser navigate` | `<url>` | 导航 |
| `openclaw sandbox list` | `|recreate --all|explain` | 沙箱管理 |
| `openclaw hooks list` | `[--eligible] [--verbose]` | Hooks列表 |
| `openclaw hooks enable` | `<name>` | 启用Hook |
| `openclaw hooks disable` | `<name>` | 禁用Hook |
| `openclaw webhooks gmail` | `setup|run` | Gmail Webhooks |
| `openclaw pairing list` | `|approve <code>` | 配对管理 |
| `openclaw security audit` | `[--deep] [--fix]` | 安全审计 |
| `openclaw dns setup` | `[--apply]` | DNS设置 |
| `openclaw docs` | `[query...]` | 文档搜索 |
| `openclaw tui` | `[--url <url>]` | 终端UI |

## 全局标志
- `--dev` - 隔离到 `~/.openclaw-dev`
- `--profile <name>` - 隔离到 `~/.openclaw-<name>`
- `--no-color` - 禁用ANSI颜色
- `-V/--version` - 打印版本

## 聊天斜杠命令
| 命令 | 用途 | 要求 |
|------|------|------|
| `/status` | 快速诊断 |  |
| `/config` | 持久化配置更改 | `commands.config: true` |
| `/debug` | 运行时覆盖 | `commands.debug: true` |
| `/model <alias>` | 切换模型 |  |
| `/reasoning on\|off\|stream\|high\|low` | 推理模式 |  |
| `/verbose on\|off\|full` | 详细模式 |  |
| `/elevated on\|off\|ask\|full` | 提升权限 |  |
| `/new` | 重置会话 |  |
| `/reset` | 重置会话 |  |
| `/tts off\|always\|inbound\|tagged` | TTS模式 |  |
| `! <cmd>` | 主机shell命令 | `commands.bash: true` |
