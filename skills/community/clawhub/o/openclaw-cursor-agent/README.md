# OpenClaw Cursor Agent Skill

让 OpenClaw 把长时间编码任务交给 Cursor CLI 在 tmux 里持久运行。

## 架构

```text
用户（飞书/聊天） → OpenClaw Agent → 插件 → WSL → tmux → Cursor CLI Agent
```

## 组件

| 组件 | 路径 | 说明 |
|------|------|------|
| **插件** | `extensions/openclaw-cursor-agent/` | OpenClaw 插件，注册工具和命令 |
| **工具脚本** | `cursor-agent-system/scripts/` | 5 个 Bash 脚本管理 tmux 会话 |
| **Cursor Skill** | `.cursor/skills/openclaw-cursor-agent-system/` | 教 Cursor IDE 如何维护工具脚本 |
| **安装脚本** | `install-openclaw-cursor-agent.ps1` | Windows PowerShell 一键安装 |

## 插件工具

| 工具 | 说明 |
|------|------|
| `cursor_agent_spawn_task` | 启动后台 Cursor 编码任务 |
| `cursor_agent_list_tasks` | 列出所有任务 |
| `cursor_agent_check_status` | 查询任务状态和进度 |
| `cursor_agent_send_command` | 向任务发送补充指令 |
| `cursor_agent_kill_session` | 结束任务 |
| `cursor_agent_doctor` | 诊断环境和依赖 |

## 环境要求

- Windows 10+ 且已启用 WSL
- WSL 内安装 Debian（或其他发行版）
- WSL 内需要：`bash`、`tmux`、`python3`、Cursor CLI（`agent`）
- OpenClaw 已安装并运行

## 安装

```powershell
.\install-openclaw-cursor-agent.ps1 -DefaultProjectPath "D:\project\your-project" -WslDistro "Debian"
```

安装后验证：

```
openclaw cursor-agent-doctor
```

## 使用

直接用自然语言对 OpenClaw 说：

- **启动任务**：帮我用 Cursor 在后台做一个任务：实现用户登录接口
- **查看进度**：看看刚才那个 Cursor 任务做到哪了
- **补充要求**：告诉刚才那个任务：JWT 改成 RS256
- **结束任务**：把刚才那个 Cursor 任务停掉

## 项目结构

```text
openclaw/
├── extensions/openclaw-cursor-agent/   # OpenClaw 插件
│   ├── index.js                        # 插件入口
│   ├── openclaw.plugin.json            # 插件清单
│   ├── skill/                          # 插件 Skill（给 OpenClaw 用）
│   └── examples/                       # 配置示例
├── cursor-agent-system/                # 工具脚本
│   ├── scripts/                        # spawn / check-status / send / kill / attach
│   ├── templates/                      # 任务提示模板
│   ├── status/                         # 运行时状态 JSON
│   ├── tasks/                          # 运行时任务文件
│   └── logs/                           # 运行时日志
├── .cursor/skills/                     # Cursor IDE Skill（开发维护用）
├── docs/                               # 文档
│   ├── usage-guide.md                  # 使用指南
│   ├── archive/                        # 历史文档归档
│   └── LOCAL_SETUP_GUIDE.md            # OpenClaw 本地部署指南
├── install-openclaw-cursor-agent.ps1   # 安装脚本
├── .gitattributes                      # 强制 LF 换行
└── .gitignore
```

## 文档

- [使用指南](docs/usage-guide.md) — 自然语言操作说明
- [插件 README](extensions/openclaw-cursor-agent/README.md) — 插件详细说明
- [工具脚本 README](cursor-agent-system/README.md) — 脚本详细说明

## License

MIT
