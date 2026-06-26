---
name: nano-banana-pro-custom
description: Generate or edit images using OpenAI-compatible API. Supports multi-image input, fine-tuned models, and multiple configuration sources (env vars, openclaw.json, config.json). Use when generating images, editing images, or composing multiple images with OpenAI-style image APIs.
metadata:
  {
    "openclaw":
      {
        "emoji": "🍌",
        "requires": {
          "bins": ["uv"],
          "python": ">=3.10",
          "packages": ["openai>=1.0.0", "pillow>=10.0.0", "requests>=2.28.0"],
          "env": ["NANO_API_KEY", "NANO_BASE_URL", "NANO_MODEL"]
        },
        "primaryEnv": "NANO_API_KEY",
        "configPaths": ["~/.openclaw/openclaw.json", "{skillDir}/config.json"],
      },
  }
---

# Nano Banana Pro (OpenAI-Compatible Image Generation)

使用 OpenAI 兼容 API 生成或编辑图片，支持多图输入、微调模型和多源配置。

## 配置方式（优先级从高到低）

1. **命令行参数** `--base-url`, `--api-key`, `--model`
2. **环境变量** `NANO_BASE_URL`, `NANO_API_KEY`, `NANO_MODEL`
3. **openclaw.json** `~/.openclaw/openclaw.json` 中的 `skills.entries.nano-banana-pro-custom`
   - `apiKey` 字段用于配置 API Key
   - `env` 字段用于配置其他环境变量
4. **技能 config.json** `{baseDir}/config.json`

### 环境变量配置

```bash
export NANO_BASE_URL="https://api.openai.com/v1"
export NANO_API_KEY="your-api-key"
export NANO_MODEL="gpt-image-1"
```

### openclaw.json 配置

#### 使用命令行设置（推荐）

```bash
# 设置 API Key（特殊字段）
openclaw config set skills.entries.nano-banana-pro-custom.apiKey "sk-your-api-key"

# 设置 Base URL（env 字段）
openclaw config set skills.entries.nano-banana-pro-custom.env.NANO_BASE_URL "https://api.openai.com/v1"

# 设置模型（env 字段）
openclaw config set skills.entries.nano-banana-pro-custom.env.NANO_MODEL "gpt-image-1"
```

#### OpenRouter 示例

```bash
# OpenRouter 配置
openclaw config set skills.entries.nano-banana-pro-custom.env.NANO_BASE_URL "https://openrouter.ai/api/v1"
openclaw config set skills.entries.nano-banana-pro-custom.env.NANO_MODEL "google/gemini-3.1-flash-image-preview"
```

#### 手动编辑文件

也可以直接编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "nano-banana-pro-custom": {
        "apiKey": "sk-your-api-key",
        "env": {
          "NANO_BASE_URL": "https://openrouter.ai/api/v1",
          "NANO_MODEL": "google/gemini-3.1-flash-image-preview"
        }
      }
    }
  }
}
```

### 技能 config.json 配置

在技能目录下创建 `config.json` 文件：

```bash
# 创建配置文件
cat > {baseDir}/config.json << 'EOF'
{
  "baseUrl": "https://api.openai.com/v1",
  "apiKey": "your-api-key",
  "model": "gpt-image-1"
}
EOF
```

配置文件内容示例：

```json
{
  "baseUrl": "https://api.openai.com/v1",
  "apiKey": "your-api-key",
  "model": "gpt-image-1"
}
```

### 查看当前配置

```bash
uv run {baseDir}/scripts/generate_image.py --show-config
```

## 快速开始

### 生成新图片

```bash
uv run {baseDir}/scripts/generate_image.py \
    --prompt "一只宇航员猫在月球上" \
    --output "cat_astronaut.png"
```

### 编辑单张图片

```bash
uv run {baseDir}/scripts/generate_image.py \
    --prompt "给这只猫加上一顶帽子" \
    --input cat.png \
    --output "cat_with_hat.png"
```

### 多图合成

```bash
uv run {baseDir}/scripts/generate_image.py \
    --prompt "将这两张图片融合成一个场景" \
    --input img1.png \
    --input img2.png \
    --output "merged.png"
```

### 使用微调模型

```bash
uv run {baseDir}/scripts/generate_image.py \
    --prompt "以我训练的风格画一辆车" \
    --output "car_custom.png" \
    --model "ft:image-model:my-finetuned-model"
```

## 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--prompt, -p` | 图片描述/提示词 | ✓ | - |
| `--output, -o` | 输出文件名 | ✓ | - |
| `--input, -i` | 输入图片路径（可多次使用） | ✗ | - |
| `--base-url` | API 基础 URL | 配置优先 | - |
| `--api-key` | API 密钥 | 配置优先 | - |
| `--model` | 模型名称 | 配置优先 | gpt-image-1 |
| `--size, -s` | 输出尺寸 | ✗ | 1024x1024 |
| `--quality, -q` | 图片质量 | ✗ | auto |
| `--n` | 生成数量(1-10) | ✗ | 1 |
| `--response-format` | 响应格式(url/b64_json) | ✗ | b64_json |
| `--timeout` | 请求超时(秒) | ✗ | 120 |
| `--verbose, -v` | 详细输出 | ✗ | false |
| `--show-config` | 显示当前配置 | ✗ | false |

## 支持的尺寸

- `1024x1024` - 正方形（默认）
- `1792x1024` - 横向
- `1024x1792` - 纵向
- `1536x1024` - 横向（部分模型）
- `1024x1536` - 纵向（部分模型）
- `auto` - 自动选择

## 图片质量

- `low` - 快速生成，较低质量
- `medium` - 平衡速度和质量
- `high` - 最高质量
- `auto` - 自动选择（默认）

## 注意事项

- 输出文件会自动保存为 PNG 格式
- 生成的图片会自动添加 `MEDIA:` 标记以便 OpenClaw 自动附加到消息
- 多图输入功能取决于 API 提供商的支持程度
- 微调模型需先完成模型训练并获得模型 ID

## 示例服务商

此技能兼容任何 OpenAI 风格的图像 API：

- **OpenAI**: https://api.openai.com/v1
- **Azure OpenAI**: https://your-resource.openai.azure.com/openai/deployments/your-deployment
- **第三方兼容服务**: 任何兼容 OpenAI API 格式的服务商

## 故障排除

### 检查配置

```bash
# 查看当前配置来源
uv run {baseDir}/scripts/generate_image.py --show-config
```

### 常见问题

1. **No base_url provided**: 检查上述 4 种配置方式是否正确设置
2. **No api_key provided**: 同上，确保 API Key 已配置
3. **连接超时**: 使用 `--timeout` 增加超时时间
