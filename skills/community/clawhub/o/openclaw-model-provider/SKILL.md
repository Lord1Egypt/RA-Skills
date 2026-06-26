---
name: openclaw-model-provider
description: Help users add custom model providers to OpenClaw. Use when the user wants to add a new AI model provider (like custom OpenAI-compatible APIs, local LLMs, or third-party services) to their OpenClaw configuration. Handles configuration of models.providers, agents.defaults.model, environment variables, and validation.
---

# OpenClaw 自定义模型提供商配置

帮助用户在 OpenClaw 中添加和配置自定义模型提供商。

## 快速开始

判断用户的配置类型：

### 类型 A：内置提供商（只需一处配置）
OpenClaw 已内置支持，只需设置 API Key 和默认模型：
- `openai`, `anthropic`, `moonshot`, `zai`, `google`, `deepseek`
- 配置位置：`agents.defaults.model.primary`
- API Key：通过环境变量或 `env` 字段设置

### 类型 B：自定义提供商（需要两处配置）
文档未内置支持的模型或自建代理：
- 配置位置 1：`models.providers` - 定义提供商信息
- 配置位置 2：`agents.defaults.model` - 设置默认使用

## 配置流程

### 步骤 1：收集必要信息

询问用户提供：
1. **提供商名称**（如 `my-openai-proxy`）
2. **API 基础地址**（如 `https://api.xxx.com/v1`）
3. **API 密钥**
4. **模型 ID**（如 `gpt-4`, `kimi-k2.5`）
5. **接口类型**：
   - `openai-completions` - OpenAI 兼容接口（大多数情况）
   - `anthropic-messages` - Anthropic 兼容接口

### 步骤 2：生成配置

根据用户提供的信息，生成完整的配置片段。

**自定义提供商完整配置示例：**

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "提供商名称/模型ID"
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "提供商名称": {
        "baseUrl": "https://api.xxx.com/v1",
        "apiKey": "${ENV_VAR_NAME}",
        "api": "openai-completions",
        "models": [
          {
            "id": "模型ID",
            "name": "显示名称",
            "contextWindow": 128000,
            "maxTokens": 4096,
            "reasoning": false,
            "input": ["text", "image"]
          }
        ]
      }
    }
  }
}
```

### 步骤 3：应用配置

指导用户将配置合并到 `~/.openclaw/openclaw.json`：

```bash
# 1. 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 2. 编辑配置
openclaw config edit
# 或直接修改文件
nano ~/.openclaw/openclaw.json
```

### 步骤 4：验证配置

```bash
# 检查配置格式
openclaw config validate

# 查看可用模型列表
openclaw models list

# 测试模型
openclaw models test 提供商名称/模型ID
```

## 环境变量设置

推荐将 API Key 放在环境变量中，而非硬编码到配置文件：

**方式 1：shell 配置文件**
```bash
# ~/.bashrc 或 ~/.zshrc
export PROVIDER_API_KEY="sk-xxxxx"
```

**方式 2：OpenClaw 配置中的 env 字段**
```json
{
  "env": {
    "PROVIDER_API_KEY": "sk-xxxxx"
  }
}
```

**方式 3：.env 文件（如果 OpenClaw 支持）**

## 常见提供商模板

### OpenAI 兼容代理

```json
{
  "models": {
    "providers": {
      "custom-openai": {
        "baseUrl": "https://api.openai-proxy.com/v1",
        "apiKey": "${OPENAI_PROXY_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "gpt-4",
            "name": "GPT-4",
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "custom-openai/gpt-4"
      }
    }
  }
}
```

### 本地 Ollama

```json
{
  "models": {
    "providers": {
      "ollama-local": {
        "baseUrl": "http://localhost:11434/v1",
        "apiKey": "ollama",
        "api": "openai-completions",
        "models": [
          {
            "id": "llama3.3",
            "name": "Llama 3.3",
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

### Moonshot AI (Kimi)

```json
{
  "models": {
    "providers": {
      "moonshot": {
        "baseUrl": "https://api.moonshot.ai/v1",
        "apiKey": "${MOONSHOT_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5",
            "contextWindow": 256000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

## 故障排查

### 配置验证失败

```bash
# 检查 JSON 语法
openclaw config validate

# 查看详细错误
openclaw config validate --verbose
```

### 模型不可用

```bash
# 确认模型列表中包含目标模型
openclaw models list | grep 提供商名称

# 测试连接
openclaw models test 提供商名称/模型ID --verbose
```

### API Key 无效

- 检查环境变量是否正确设置：`echo $PROVIDER_API_KEY`
- 确认 OpenClaw 能读取环境变量
- 检查 API Key 是否有调用权限和余额

## 高级配置

### 多密钥轮换

支持配置多个 API Key 实现自动故障转移：

```json
{
  "env": {
    "PROVIDER_API_KEY_1": "sk-xxx1",
    "PROVIDER_API_KEY_2": "sk-xxx2",
    "PROVIDER_API_KEY_3": "sk-xxx3"
  }
}
```

或在 shell 中：
```bash
export PROVIDER_API_KEYS="sk-xxx1,sk-xxx2,sk-xxx3"
```

### 模型参数覆盖

为特定模型设置默认参数：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "提供商名称/模型ID": {
          "params": {
            "temperature": 0.7,
            "maxTokens": 2048,
            "fastMode": true
          }
        }
      }
    }
  }
}
```

## 参考资源

- [OpenClaw 官方文档 - 模型提供商](https://docs.openclaw.ai/zh-CN/concepts/model-providers)
- [OpenClaw 配置参考](references/openclaw-config-reference.md)

## 使用示例

**用户说**："我想添加硅基流动的 DeepSeek-R1"

**执行流程**：
1. 确认是自定义提供商（非内置）
2. 收集信息：
   - 名称：`siliconflow`
   - 地址：`https://api.siliconflow.cn/v1`
   - API Key：用户提供的 key
   - 模型：`deepseek-ai/DeepSeek-R1`
3. 生成配置并指导用户应用
4. 验证配置
