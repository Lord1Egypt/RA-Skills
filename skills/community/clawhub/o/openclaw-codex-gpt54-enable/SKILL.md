---
name: openclaw-codex-gpt54-enable
description: Enable `openai-codex/gpt-5.4` in OpenClaw through a config-layer patch instead of rebuilding the app. Use when `openai/gpt-5.4` already works but Codex GPT-5.4 is blocked or missing, and you want a repeatable verification + rollback workflow.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧩",
        "homepage": "https://github.com/youxitianguo/openclaw-skill-openclaw-codex-gpt54-enable",
        "requires": { "bins": ["openclaw"], "env": [] }
      }
  }
---

# OpenClaw Codex GPT-5.4 Enable Skill

把 `openai-codex/gpt-5.4` 用“配置层补丁”方式接入 OpenClaw，避免直接改安装目录或整包重编译。

## 适用场景

当你遇到下面这种情况时使用：

- `openai/gpt-5.4` 已经在 OpenClaw 中可见
- 但 `openai-codex/gpt-5.4` 仍然显示 not allowed / missing
- 想快速验证 GPT-5.4 Codex 通道，而不是先改 Homebrew 安装产物
- 希望把 provider、模型、别名、fallback 一次补齐

## 核心思路

优先改 `~/.openclaw/openclaw.json`：

1. 在 `models.providers` 中新增 `openai-codex`
2. 设置：
   - `baseUrl: https://chatgpt.com/backend-api`
   - `api: openai-codex-responses`
3. 为该 provider 补上模型 `gpt-5.4`
4. 在 `agents.defaults.models` 和 `agents.defaults.model.fallbacks` 中补上 `openai-codex/gpt-5.4`
5. 给它加一个别名，例如 `GPT54Codex`
6. 用 `openclaw models list` 和 `session_status(model='openai-codex/gpt-5.4')` 验证

## 为什么优先走配置层

- 风险更低：不碰安装目录内打包 JS
- 回滚更简单：只需恢复一份 JSON 配置
- 更适合快速试验和迁移
- 对已经在跑的 OpenClaw 实例更友好

## 目标文件

```bash
~/.openclaw/openclaw.json
```

建议操作前先备份：

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
```

## 参考配置结构

> 字段名可能随 OpenClaw 版本略有变化，请以你当前 `openclaw.json` 结构为准，把下面内容合并进去。

```json
{
  "models": {
    "providers": {
      "openai-codex": {
        "apiKey": "$OPENAI_API_KEY",
        "baseUrl": "https://chatgpt.com/backend-api",
        "api": "openai-codex-responses",
        "models": {
          "gpt-5.4": {
            "label": "GPT-5.4 Codex",
            "contextTokens": 400000,
            "maxOutputTokens": 128000,
            "modalities": ["text", "image"],
            "supportsReasoning": true
          }
        }
      }
    }
  },
  "agents": {
    "defaults": {
      "models": {
        "GPT54Codex": "openai-codex/gpt-5.4"
      },
      "model": {
        "fallbacks": [
          "openai-codex/gpt-5.4"
        ]
      }
    }
  }
}
```

## 实战流程

### 1) 先确认当前支持面

```bash
openclaw models list --plain | grep 'gpt-5.4'
```

判断点：
- 如果 `openai/gpt-5.4` 已经存在，说明基础支持大概率已经在
- 如果只有 OpenAI 版本，没有 Codex 版本，就继续补配置

### 2) 备份配置

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
```

### 3) 编辑 provider

在 `models.providers` 里新增：
- provider id：`openai-codex`
- `baseUrl`: `https://chatgpt.com/backend-api`
- `api`: `openai-codex-responses`

### 4) 补模型定义

给 `openai-codex` provider 增加 `gpt-5.4` 模型定义，至少补：
- label
- context/max tokens
- text/image modality
- reasoning 支持

### 5) 补 agent 默认映射

在 `agents.defaults.models` 里补别名：

```json
{
  "GPT54Codex": "openai-codex/gpt-5.4"
}
```

在 `agents.defaults.model.fallbacks` 里补：

```json
[
  "openai-codex/gpt-5.4"
]
```

### 6) 验证模型注册

```bash
openclaw models list --plain | grep 'openai-codex/gpt-5.4'
```

### 7) 验证网关是否真正接受

用 OpenClaw 的状态能力做快速实测：

```bash
# 在 OpenClaw 会话内
session_status(model='openai-codex/gpt-5.4')
```

成功标准：
- 不再报 `not allowed`
- 模型可被选中
- provider 认证链路走 `openai-codex:default`（视环境展示而定）

## 经验结论

### 已验证有效的判断逻辑

1. 先看官方 PR / 改动方向，确认是不是“版本已支持、只是本地没放开”
2. 如果核心 provider 能力已在，优先尝试配置层补齐
3. 用 `session_status` 验证，比只看静态配置更靠谱
4. 改完后如果上下文上限没有立刻刷新，优先开新会话再测

### 这套方法特别适合

- 想快速上手新模型
- 不想改安装目录
- 想沉淀成可复用 SOP
- 多机器迁移 OpenClaw 配置

## 排障

### `not allowed`
- 检查 `agents.defaults.models` 是否已补别名
- 检查 `fallbacks` 是否已包含目标模型
- 检查 provider id 是否与模型前缀一致：`openai-codex/...`

### 模型存在但调用失败
- 检查 `baseUrl` 和 `api` 是否正确
- 检查对应认证是否已就绪
- 检查是否需要重启 OpenClaw Gateway / 新建会话

### 模型列表看不到
- 检查 JSON 是否写坏
- 检查 provider 是否放在正确层级
- 执行：

```bash
openclaw models list --plain | grep codex
```

## 回滚

```bash
cp ~/.openclaw/openclaw.json.bak.YYYYMMDD-HHMMSS ~/.openclaw/openclaw.json
```

然后重新启动或刷新相关服务。

## 推荐验证清单

- [ ] `openai/gpt-5.4` 已可见
- [ ] `openai-codex` provider 已加入
- [ ] `gpt-5.4` 模型定义已加入
- [ ] `GPT54Codex` 别名已加入
- [ ] `fallbacks` 已加入 `openai-codex/gpt-5.4`
- [ ] `openclaw models list` 能看到目标模型
- [ ] `session_status(model='openai-codex/gpt-5.4')` 成功
- [ ] 新会话验证通过

## 一句话版本

如果 `openai/gpt-5.4` 已经支持，而 `openai-codex/gpt-5.4` 还没放开，别急着重编译：先用 `~/.openclaw/openclaw.json` 做 provider + model + alias + fallback 的配置层补丁，再用 `session_status` 验证。"