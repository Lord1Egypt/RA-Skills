# Provider 切换 / `/model` 命令陷阱

## `/model` 和 `hermes model` 是同一个

CLI 里 `/model` slash 命令、命令行 `hermes model` 子命令,都进 `hermes_cli/model_switch.py`。流程:

1. 列出已配置的 provider 和 model
2. 用户选择 → 写 `config.yaml` 的 `model.provider`、`model.default`、(可能)`model.api_key`、`model.base_url`
3. 重置 `model.api_mode`(早期版本不重置 → issue #3685)
4. 运行时下次发起请求时 reload provider

## issue #3685:`/model` 切换后 api_mode 残留

**症状**:从 provider A(用 `chat_completions` mode)切到 B(用 Anthropic-compatible mode)后,所有请求 404。

**根因**:`config.yaml` 的 `model.api_mode` 字段没被切换逻辑清掉,继续用 A 的 path。

**修复**:已在 hermes-agent 主分支修了 — 升级即可:
```bash
hermes update              # 或对应安装方式
```

或临时手工修:
```bash
HOME_DIR="$(hermes dump --redact 2>&1 | awk -F': ' '/HERMES_HOME/{print $2; exit}')"
cp "$HOME_DIR/config.yaml" "$HOME_DIR/config.yaml.broken-$(date +%Y%m%d-%H%M%S)"
# 编辑 config.yaml,删掉 model.api_mode 那一行(或注释掉)
# 重启 hermes
```

参考:https://github.com/NousResearch/hermes-agent/issues/3685

## active_profile vs root model.*

`config.yaml`:
```yaml
model:
  active_profile: <name>   # 非空时,profile 字段覆盖 root
  provider: deepseek       # active_profile 为空时这个生效
  base_url: ...
  api_key: ...
  default: ...

model_profiles:
  <name>:
    provider: ...
    base_url: ...
    api_key: ...           # 实际生效的 key
    default: ...
```

**坑 1**:active_profile 切换时,顶层 `model.provider/base_url/api_key/default` 可能不变,**但运行时 hermes 用 profile 的字段**。如果你只看顶层会以为还在 A 实际已经在 B。

**坑 2**:profile 的 api_key 没填时,fallback 到 root model.api_key,再没填 fallback 到 credential_pool,再没找到 → 占位符 `no-key-required`(参 auth-troubleshooting.md 类型 1)。

**调试**:`hermes dump --redact` 看 active provider 和 source。

## 切 provider 后必跑的验证

切完 `/model` 后立刻:
1. `hermes dump --redact` 看运行时配置
2. 发一句 `ping`(空对话),观察 token 计数 / 模型名是否对
3. 如果用了多 profile,检查 `model.active_profile` 字段
4. 看 `<HOME_DIR>/sessions/request_dump_*.json` 最新一条的 `request.url` 和 `request.headers.Authorization`

## 配置一个新 provider 的最小 config

如果 `hermes setup` 没覆盖你要的 provider(比如自建 OpenAI 兼容 endpoint):

```yaml
# config.yaml
model:
  provider: custom
  base_url: https://your-endpoint.example.com/v1
  default: your-model-id
  auth_mode: api_key
  api_key: sk-...
  auth_header: Authorization
  auth_scheme: Bearer
```

然后 `auth.json` 加一条 credential_pool.custom 同步(参 auth-troubleshooting.md)。两边都填,启动 hermes 验证。

## 把现有 profile 设为默认

```bash
hermes config set model.active_profile "<name>"
```

或编辑 `config.yaml` 改 `active_profile`。重启生效。

## 常见 provider base_url 速查

| Provider | base_url |
|---|---|
| deepseek | https://api.deepseek.com/v1 |
| anthropic | https://api.anthropic.com |
| gemini | https://generativelanguage.googleapis.com/v1beta/openai |
| openai | https://api.openai.com/v1 |
| openrouter | https://openrouter.ai/api/v1 |
| zai (GLM) | https://api.z.ai |
| kimi (Moonshot 国际) | https://api.moonshot.ai/v1 |
| kimi-cn | https://api.moonshot.cn/v1 |
| arcee | https://api.arcee.ai/v1 |
| dashscope (Alibaba) | https://dashscope-intl.aliyuncs.com/compatible-mode/v1 |
| dashscope-cn | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| xai | https://api.x.ai/v1 |
| nvidia | https://integrate.api.nvidia.com/v1 |
| copilot | https://api.githubcopilot.com |

如果不确定你装的版本支持哪些 provider,翻 `hermes_cli/auth.py` 里的 PROVIDER_REGISTRY 定义(典型在 95-260 行附近,具体行号随版本浮动)。
