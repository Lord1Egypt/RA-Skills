# 配置文件 Schema 参考

BYOK 配置文件是一个 JSON 对象，路径默认为 `~/.config/multimodal-image-understanding/config.json`，可通过 `--config` 覆盖。

## 完整字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `protocol` | string | 是 | 协议类型，取值 `"anthropic"` 或 `"openai"`。 |
| `endpoint` | string | 是 | 上游 API 的 base URL（不含路径）。脚本会自行追加 `/v1/messages` 或 `/chat/completions`。 |
| `model` | string | 是 | 上游模型名，例如 `"gpt-4o"`、`"claude-opus-4-6"`、`"MiniMax-M3"`。 |
| `api_key` | string | 视情况 | API 密钥。推荐使用 `${ENV_VAR}` 形式从环境变量读取，避免落盘。 |
| `auth_header` | string | 否 | 自定义鉴权 header 名称。Anthropic 默认使用 `x-api-key`，OpenAI 默认使用 `Authorization: Bearer ...`。 |
| `max_tokens` | int | 否 | 最大输出 token 数。默认 1024。 |
| `temperature` | float | 否 | 采样温度，例如 `0.2`。不设置则由上游决定。 |
| `system` | string | 否 | （仅 Anthropic 协议）system prompt。 |
| `image_mode` | string | 否 | 图片传输模式：`"auto"` / `"url"` / `"base64"`，默认 `"auto"`。详见下表。 |

## `image_mode` 取值

| 取值 | 行为 |
|------|------|
| `auto` | `--image` 是 URL 时直接传 URL；是本地路径时读文件并 base64 编码。 |
| `url` | 始终传 URL；若传入的是本地路径会报错。适合上游只接受 URL 链接的场景。 |
| `base64` | 始终先下载（URL）或读取（本地）再 base64 编码。适合上游不支持 image URL 的场景。 |

## 环境变量展开

任何字符串字段都支持 `${VAR_NAME}` 形式的引用，脚本会从 `os.environ` 展开。例如：

```json
{
  "api_key": "${ANTHROPIC_AUTH_TOKEN}",
  "endpoint": "${MY_LLM_BASE_URL}"
}
```

如果引用的环境变量未设置，脚本会直接报错退出。

## Anthropic 协议配置示例

Anthropic 官方：

```json
{
  "protocol": "anthropic",
  "endpoint": "https://api.anthropic.com",
  "model": "claude-opus-4-6",
  "api_key": "${ANTHROPIC_API_KEY}",
  "max_tokens": 1024,
  "system": "你是一个严谨的图像分析助手。"
}
```

Anthropic 协议兼容代理（如 minimaxi）：

```json
{
  "protocol": "anthropic",
  "endpoint": "https://api.minimaxi.com/anthropic",
  "model": "MiniMax-M3",
  "api_key": "${ANTHROPIC_AUTH_TOKEN}",
  "image_mode": "base64"
}
```

## OpenAI ChatCompletion 协议配置示例

OpenAI 官方：

```json
{
  "protocol": "openai",
  "endpoint": "https://api.openai.com/v1",
  "model": "gpt-4o",
  "api_key": "${OPENAI_API_KEY}"
}
```

Azure OpenAI：

```json
{
  "protocol": "openai",
  "endpoint": "https://{your-resource}.openai.azure.com/openai/deployments/{your-deployment}",
  "model": "gpt-4o",
  "auth_header": "api-key",
  "api_key": "${AZURE_OPENAI_API_KEY}"
}
```

## 常见网关限制：上游无法主动抓取外网 URL

部分 Anthropic 协议兼容网关（如 minimaxi）**不会**主动去 fetch 用户传入的图片 URL，会报 `invalid param: fetch url failed: dial tcp ... i/o timeout`。

**解决办法**：在配置中设置 `"image_mode": "base64"`，脚本会先在本地下载图片、base64 编码后再上传。这种方式兼容性最好，推荐作为默认配置。

```json
{
  "protocol": "anthropic",
  "endpoint": "https://api.minimaxi.com/anthropic",
  "image_mode": "base64"
}
```



| 行为 | Anthropic | OpenAI ChatCompletion |
|------|-----------|------------------------|
| 端点路径 | `/v1/messages` | `/chat/completions` |
| 图片块 | `{"type":"image","source":{...}}` | `{"type":"image_url","image_url":{"url":...}}` |
| base64 表示 | `data` + `media_type` | 直接放在 `image_url.url`，前缀 `data:<mime>;base64,` |
| system prompt | 顶层 `system` 字段 | 只能作为 `role: "system"` 消息（脚本未启用，预留扩展） |

## 调试技巧

- 加 `--quiet` 关闭 stderr 进度日志，方便管道处理。
- 用 `--model` 临时覆盖模型名，不必改配置文件。
- 想看原始响应时，把 `image_mode` 临时设成 `"url"`，并传一个公开可访问的图片 URL，最小化数据处理。
