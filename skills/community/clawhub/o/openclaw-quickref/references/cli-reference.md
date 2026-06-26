# OpenClaw CLI 命令参考

## Gateway 命令

### 基础操作

| 命令 | 说明 |
|------|------|
| `openclaw gateway status` | 查看 Gateway 运行状态 |
| `openclaw gateway start` | 启动 Gateway 服务 |
| `openclaw gateway stop` | 停止 Gateway 服务 |
| `openclaw gateway restart` | 重启 Gateway 服务 |

### 启动选项

```bash
openclaw gateway start --help

Options:
  --config <path>    指定配置文件路径
  --port <port>      指定端口（默认自动选择）
  --daemon           以守护进程模式运行
  --log-level <level> 日志级别 (debug/info/warn/error)
```

## Session 命令

### 会话管理

| 命令 | 说明 |
|------|------|
| `openclaw session list` | 列出所有会话 |
| `openclaw session show <id>` | 显示会话详情 |
| `openclaw session delete <id>` | 删除会话 |

## Plugin 命令

### 插件管理

| 命令 | 说明 |
|------|------|
| `openclaw plugin list` | 列出已安装插件 |
| `openclaw plugin install <package>` | 安装插件 |
| `openclaw plugin remove <id>` | 移除插件 |
| `openclaw plugin update <id>` | 更新插件 |

### 安装来源

```bash
# 从 npm 安装
openclaw plugin install @openclaw/plugin-discord

# 从本地路径安装
openclaw plugin install ./my-plugin

# 从 Git 仓库安装
openclaw plugin install github:user/repo
```

## Config 命令

### 配置管理

| 命令 | 说明 |
|------|------|
| `openclaw config show` | 显示当前配置 |
| `openclaw config get <path>` | 获取配置项 |
| `openclaw config set <path> <value>` | 设置配置项 |
| `openclaw config unset <path>` | 删除配置项 |

### 配置路径示例

```bash
# 获取默认模型
openclaw config get agents.default.model

# 设置提供商 API Key
openclaw config set providers.openai.apiKey "sk-xxx"

# 设置技能路径
openclaw config set skills.paths '["./skills", "~/.agents/skills"]'
```

## Node 命令

### 节点管理

| 命令 | 说明 |
|------|------|
| `openclaw node list` | 列出已配对节点 |
| `openclaw node pair` | 生成配对码 |
| `openclaw node unpair <id>` | 解除配对 |

## 工具命令

### 开发调试

| 命令 | 说明 |
|------|------|
| `openclaw version` | 显示版本信息 |
| `openclaw help` | 显示帮助 |
| `openclaw <cmd> --help` | 显示命令帮助 |

---

最后更新：2026-03-13