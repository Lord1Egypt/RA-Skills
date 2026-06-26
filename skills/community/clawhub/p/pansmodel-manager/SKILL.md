---
name: PansModel-Manager
displayName: PansModel Manager
version: 1.0.1
description: |
  PanSclaw 模型管理器 - 管理自定义模型接入和切换。
  支持添加、删除、切换、列出模型配置。
  
  触发关键词: 模型管理, 切换模型, 添加模型, 删除模型, 模型列表, 
              配置模型, 更换模型, 接入模型, 模型设置
metadata: {"openclaw": {"emoji": "🤖"}}
---

# 模型管理器

## 功能

管理 PanSclaw 的模型配置，支持：
- 添加自定义模型提供商
- 切换默认模型
- 列出已配置模型
- 删除模型配置

## 使用方法

### 添加模型

```
/模型 添加 厂商=<name> 地址=<url> 密钥=<key> 模型=<model_id>
```

示例：
```
/模型 添加 厂商=deepseek 地址=https://api.deepseek.com/v1 密钥=sk-xxx 模型=deepseek-chat
```

### 切换模型

```
/模型 切换 <厂商>/<模型名>
```

示例：
```
/模型 切换 deepseek/deepseek-chat
```

### 列出模型

```
/模型 列表
```

### 删除模型

```
/模型 删除 <厂商>
```

## 支持的 API 类型

| 厂商 | API 适配器 |
|------|-----------|
| openai | openai-completions |
| anthropic | anthropic-messages |
| deepseek | openai-completions |
| moonshot | openai-completions |
| zhipu | openai-completions |
| qwen | openai-completions |
| ollama | ollama |

## 配置文件位置

`~/.openclaw-pansclaw/openclaw.json`

配置修改后需要重启 Gateway 生效。
