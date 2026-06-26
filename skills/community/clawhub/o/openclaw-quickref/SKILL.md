---
name: openclaw-quickref
description: 快速查询 OpenClaw CLI 命令、配置语法和常用模式。当用户问"怎么配置"、"命令是什么"、"配置格式"时触发。
license: MIT
metadata:
  author: OpenClaw Expert
  version: 1.0.0
---

# OpenClaw 快速参考

快速查询 OpenClaw 常用命令、配置语法和最佳实践。

## 触发条件

- 用户询问 CLI 命令用法
- 用户询问配置文件格式
- 用户询问"怎么配置 X"
- 用户询问"命令是什么"
- 用户需要快速参考某个功能

## CLI 命令速查

### Gateway 管理

```bash
openclaw gateway status    # 查看状态
openclaw gateway start     # 启动服务
openclaw gateway stop      # 停止服务
openclaw gateway restart   # 重启服务
```

### 插件管理

```bash
openclaw plugin list              # 列出已安装插件
openclaw plugin install <pkg>     # 安装插件
openclaw plugin remove <id>       # 移除插件
```

### 配置管理

```bash
openclaw config show              # 显示当前配置
openclaw config set <path> <val>  # 设置配置项
openclaw config get <path>        # 获取配置项
```

## 配置文件结构

### openclaw.json 主配置

```json
{
  "providers": {
    "openai": {
      "apiKey": "${OPENAI_API_KEY}",
      "models": ["gpt-4", "gpt-3.5-turbo"]
    }
  },
  "agents": {
    "default": {
      "model": "gpt-4",
      "systemPrompt": "You are a helpful assistant."
    }
  },
  "skills": {
    "paths": ["./skills", "~/.agents/skills"]
  }
}
```

### 环境变量

```bash
OPENCLAW_API_KEY         # Gateway API 密钥
OPENAI_API_KEY            # OpenAI API 密钥
ANTHROPIC_API_KEY        # Anthropic API 密钥
```

## 常用模式

### 配置提供商

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "${ANTHROPIC_API_KEY}",
      "baseUrl": "https://api.anthropic.com"
    }
  }
}
```

### 配置 Agent

```json
{
  "agents": {
    "my-agent": {
      "model": "claude-3-opus",
      "provider": "anthropic",
      "systemPrompt": "Custom system prompt..."
    }
  }
}
```

### 配置 Channel

```json
{
  "channels": {
    "discord": {
      "token": "${DISCORD_TOKEN}",
      "clientId": "123456789"
    }
  }
}
```

## 详细参考

更多详细信息请参阅：
- CLI 命令详解：`./references/cli-reference.md`
- 配置详解：`./references/config-reference.md`

## 最佳实践

1. **环境变量优先** - 敏感信息用 `${VAR_NAME}` 引用
2. **分层配置** - 全局配置 + 工作空间配置
3. **技能路径** - 使用相对路径或 `~` 扩展
4. **模型别名** - 为常用模型创建别名简化配置