---
name: multimodal-image-understanding
description: 通过调用多模态模型来理解图片内容。触发场景：(1) 用户要求分析/描述/提取/OCR 图片信息，且当前模型不支持图像输入（如 deepseek-v4、glm 5.1 等纯文本模型），(2) 用户明确要求"用我的视觉模型"或"调用多模态 API"来看图，(3) 用户显式调用本 skill（/multimodal-image-understanding）。
---

# 多模态图片理解

## 前置判断

**在调用本 skill 之前**，先确认当前模型是否已支持视觉：
- 如果当前模型（如 Claude Opus/Sonnet/Haiku、GPT-4o）本身已能看图 → 直接使用内置 `understand_image` 工具或原生图片输入，不需要本 skill。
- 如果当前模型是纯文本模型（如 `deepseek-v4`、`glm 5.1`），或用户明确要求用其 BYOK 配置中指定的模型来看图 → 使用本 skill。

## 工作流程

1. 读取 BYOK 配置（默认路径：`~/.config/multimodal-image-understanding/config.json`，可通过 `--config` 覆盖）。
2. 根据 `config.protocol` 自动识别协议（`anthropic` 或 `openai`）。
3. 调用 `scripts/multimodal_understand.py`，传入图片和 prompt。
4. 脚本调用上游 API，并将模型回复打印到 stdout。

## 快速开始

```bash
# 1. 创建配置文件（一次性）
mkdir -p ~/.config/multimodal-image-understanding
cp assets/config.example.json ~/.config/multimodal-image-understanding/config.json
# 编辑 config.json：填入 api_key、model、endpoint

# 2. 用图片和 prompt 运行脚本
python3 scripts/multimodal_understand.py \
  --image /path/to/photo.jpg \
  --prompt "请详细描述这张图片。"
```

脚本将模型对图片的理解输出到 stdout。请将输出作为对用户图片问题的最终回答。

## 配置文件格式

完整 schema 见 `references/config-schema.md`。最简示例：

```json
{
  "protocol": "openai",
  "endpoint": "https://api.openai.com/v1",
  "model": "gpt-4o",
  "api_key": "sk-...",
  "max_tokens": 1024,
  "temperature": 0.2
}
```

Anthropic 协议端点（Anthropic 官方、Bedrock，或任何兼容 Anthropic 协议的网关）：

```json
{
  "protocol": "anthropic",
  "endpoint": "https://api.anthropic.com",
  "model": "claude-opus-4-6",
  "api_key": "sk-ant-...",
  "max_tokens": 1024
}
```

支持在 `api_key`、`endpoint` 等字符串值中用 `${ENV_VAR_NAME}` 引用环境变量，脚本会自动从 `os.environ` 展开。**推荐使用这种方式**，避免密钥落盘。

## CLI 参数

```
multimodal_understand.py
  --image PATH|URL        图片的本地路径或 HTTP(S) URL（必填）
  --prompt TEXT           关于图片的 prompt/问题（必填）
  --config PATH           BYOK 配置文件路径（默认：~/.config/multimodal-image-understanding/config.json）
  --protocol {anthropic,openai}  覆盖配置文件中的 protocol
  --model MODEL           覆盖配置文件中的 model
  --max-tokens N          覆盖 max_tokens
  --timeout SECONDS       请求超时时间（默认：120）
  --quiet                 关闭 stderr 上的进度日志，只输出模型回复到 stdout
```

## 图片输入规则

- **本地文件**：通过 `--image /path/to/file.png` 传入，脚本读取后做 base64 编码再上传 API。
- **URL**：通过 `--image https://...` 传入；多数 provider 直接接受图片 URL。若 provider 不支持，在配置中设置 `"image_mode": "base64"`，脚本会先下载再编码。
- 支持格式：JPEG、PNG、WebP、GIF（静态）。

## 输出处理

- 脚本将**模型回复文本**打印到 stdout（使用 `--quiet` 时只输出回复；不带 `--quiet` 时进度日志走 stderr，回复仍走 stdout）。
- 回复内容就是给用户图片理解问题的最终答案。
- 出错时，脚本返回非零退出码，错误信息以 JSON 形式输出到 stderr。

## 安全建议

- 配置文件中的 API key 直接存储在磁盘，请设置文件权限 `chmod 600`。
- 推荐在配置文件中使用 `${ENV_VAR}` 引用环境变量，避免密钥落盘。
- 不要将配置内容回显给用户。

## 资源

- `scripts/multimodal_understand.py` — 主脚本；运行无需加载到 context 中。
- `references/config-schema.md` — 完整配置 schema、环境变量展开规则、协议注意事项。
- `assets/config.example.json` — 可直接复制的配置模板。
