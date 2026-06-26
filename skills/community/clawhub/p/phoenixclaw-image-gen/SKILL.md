---
name: image-generation
description: 图像生成辅助。支持通过 OpenRouter 直接调用各种生图模型（如 Seedream），为 OpenClaw 优化，支持提示词、尺寸等参数配置。目前仅限 OpenRouter provider。
license: MIT
compatibility: OpenClaw, Claude Code, OpenCode, Antigravity
metadata:
  version: "0.2.1"
  openclaw:
    emoji: "🎨"
    requires:
      env: ["OPENROUTER_API_KEY"]
      optional: ["IMAGE_GEN_TEXT_TO_IMAGE_MODEL", "IMAGE_GEN_IMAGE_TO_IMAGE_MODEL"]
    primaryEnv: "OPENROUTER_API_KEY"
---

# 图像生成辅助

为 OpenClaw 提供原生的图像生成能力，通过文字描述词快速生成高质量图像。

## 工作流程

```
用户提示词 (Prompt)
    ↓
┌─────────────────────────────────────┐
│  识别参数：模型、尺寸、比例、路径   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  调用 OpenRouter 接口 (OpenClaw)    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  默认模型：seedream-4.5 (Text-to-Image) & Gemini 2.5 (Image-to-Image) │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  原子化写入本地存储 (Safety First)  │
└─────────────────────────────────────┘
    ↓
返回结构化 JSON (Success Payload)
```

## 安装与配置

### 1. 获取 API Key

本技能需要 **OpenRouter API Key** 才能调用图像生成服务。

1. 访问 [OpenRouter 控制台](https://openrouter.ai/keys) 创建 API Key
2. 请根据下方指引手动配置环境变量

### 2. 配置到环境变量

根据 OpenClaw 官方最佳实践，请通过 `~/.openclaw/openclaw.json` 配置环境变量：

```json5
{
  skills: {
    entries: {
      "image-generation": {
        enabled: true,
        env: {
          OPENROUTER_API_KEY: "sk-or-v1-xxxxxxxx..."
        }
      }
    }
  }
}
```

或使用 `primaryEnv` 快捷配置：

```json5
{
  skills: {
    entries: {
      "image-generation": {
        enabled: true,
        apiKey: "sk-or-v1-xxxxxxxx..."
      }
    }
  }
}
```

配置完成后无需重启，新配置会在下次运行 OpenClaw 时自动生效。


### 3. 选择默认模型（可选）

本技能默认使用 `bytedance-seed/seedream-4.5` 作为文本生图模型，`google/gemini-2.5-flash-image` 作为图生图模型。你可以通过以下方式更改：

**方式一：环境变量配置**
在 `~/.openclaw/openclaw.json` 中添加：
```json5
{
  skills: {
    entries: {
      "image-generation": {
        enabled: true,
        env: {
          OPENROUTER_API_KEY: "sk-or-v1-xxx",
          IMAGE_GEN_TEXT_TO_IMAGE_MODEL: "bytedance-seed/seedream-4.5",
          IMAGE_GEN_IMAGE_TO_IMAGE_MODEL: "google/gemini-2.5-flash-image"
        }
      }
    }
  }
}
```


本技能默认使用 `bytedance-seed/seedream-4.5` 模型，你可以通过以下方式更改：

**方式一：环境变量配置**
在 `~/.openclaw/openclaw.json` 中添加：
```json5
{
  skills: {
    entries: {
      "image-generation": {
        enabled: true,
        env: {
          OPENROUTER_API_KEY: "sk-or-v1-xxx",
          IMAGE_GEN_IMAGE_TO_IMAGE_MODEL: "google/gemini-2.5-flash-image",
          IMAGE_GEN_TEXT_TO_IMAGE_MODEL: "bytedance-seed/seedream-4.5"
      }
    }
  }
}
```

**方式二：查看可用模型**
```bash
node skills/image-generation/scripts/cli/openrouter.js --list-models
```

**方式三：生成时指定模型**
```bash
node skills/image-generation/scripts/generate.js \
  --prompt "a futuristic city" \
  --model "bytedance-seed/seedream-4.5" \
  --i2i-model "google/gemini-2.5-flash-image"
```

```bash
node skills/image-generation/scripts/generate.js \
  --prompt "a futuristic city" \
  --image "bytedance-seed/seedream-4.5" \
  --model "google/gemini-2.5-flash-image"
```

**推荐模型**：
- `bytedance-seed/seedream-4.5` - 默认，高质量图像生成
- `anthropic/claude-3.5-sonnet-image` - Claude 图像生成
- `openai/dall-e-3` - DALL-E 3

### 4. 验证配置

```bash
node skills/image-generation/scripts/cli/openrouter.js --test
```

预期输出：
```json
{
  "success": true,
  "message": "OpenRouter API key is configured. Test passed."
}
```

## 核心配置

### 仅限 OpenRouter (v1)

本技能在 v1 版本中**仅支持**通过 OpenRouter 提供商进行图像生成。目前不原生支持 Anthropic、Replicate 或 Stability AI 等直接接口。所有生图请求均通过 OpenRouter 统一中转。

### 默认模型

- **文本生图模型 (Text-to-Image)**: `bytedance-seed/seedream-4.5`
- **图生图模型 (Image-to-Image)**: `google/gemini-2.5-flash-image`
- **获取地址**: [OpenRouter | bytedance-seed/seedream-4.5](https://openrouter.ai/bytedance-seed/seedream-4.5)

## OpenClaw 调用方式

### 命令调用

OpenClaw 会通过以下 CLI 方式触发图像生成：

```bash
# 基础生成
node skills/image-generation/scripts/generate.js \
  --prompt "a futuristic city at sunset" \
  --output "outputs/city.png"

# 指定模型、尺寸与比例 (OpenRouter 默认)
node skills/image-generation/scripts/generate.js \
  --prompt "cyberpunk landscape" \
  --model "bytedance-seed/seedream-4.5" \
  --i2i-model "google/gemini-2.5-flash-image" \
  --size "2K" \
  --aspect "16:9"

node skills/image-generation/scripts/generate.js \
  --prompt "cyberpunk landscape" \
  --image "bytedance-seed/seedream-4.5" \
  --model "google/gemini-2.5-flash-image" \
  --size "2K" \
  --aspect "16:9"

# 通过 OpenClaw 包装器调用
node skills/image-generation/scripts/cli/openrouter.js \
  --prompt "abstract oil painting" \
  --size "1K"

### 预检测 (Connectivity Check)

OpenClaw 在启动时可运行以下脚本检查 API 连通性：

```bash
node skills/image-generation/scripts/cli/openrouter.js --test
```

## 参数详解

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `--prompt` | 图像描述词 | 是 | - |
| `--model` | 文本生图模型 ID | 否 | `bytedance-seed/seedream-4.5` |
| `--i2i-model` | 图生图模型 ID | 否 | `google/gemini-2.5-flash-image` |
| `--input-image`| 图生图输入图片路径 | 否 | - |
| `--list-models` | 列出所有可用模型 | 否 | - |
| `--size` | 分辨率等级 (`1K`\|`2K`\|`4K`) | 否 | 模型默认 |
| `--aspect` | 宽高比 (如 1:1, 16:9) | 否 | `1:1` |
| `--output` | 输出文件路径 | 否 | `.sisyphus/generated/image_<ts>.png` |

|------|------|------|--------|
| `--prompt` | 图像描述词 | 是 | - |
|| `--model` | 图生图模型 ID | 否 | `google/gemini-2.5-flash-image` |
|| `--image` | 文本生图模型 ID | 否 | `bytedance-seed/seedream-4.5` |
| `--list-models` | 列出所有可用模型 | 否 | - |
| `--size` | 分辨率等级 (`1K`\|`2K`\|`4K`) | 否 | 模型默认 |
| `--aspect` | 宽高比 (如 1:1, 16:9) | 否 | `1:1` |
| `--output` | 输出文件路径 | 否 | `.sisyphus/generated/image_<ts>.png` |
| `--output` | 输出文件路径 | 否 | `.sisyphus/generated/image_<ts>.png` |

### 分辨率与尺寸说明

**`--size` 参数格式**：
- 只接受三个字符串值：`"1K"`、`"2K"`、`"4K"`
- **不要** 使用像素格式如 `"1024x1024"` 或 `"3840x2160"`（OpenRouter API 不接受）

**实际输出像素尺寸**（由 `size` 和 `aspect` 共同决定）：

| size | aspect | 实际像素 | 说明 |
|------|--------|----------|------|
| `1K` | `1:1` | 1024×1024 | 默认，约 1MP |
| `1K` | `16:9` | ~1280×720 | 约 0.9MP |
| `2K` | `1:1` | 2048×2048 | 约 4MP |
| `2K` | `16:9` | ~2560×1440 | 约 3.7MP |
| `4K` | `1:1` | 4096×4096 | 约 16MP |
| `4K` | `16:9` | 3840×2160 | 标准 4K UHD |

**重要限制**：
1. **并非所有模型都支持 4K**，部分模型最高只支持到 2K
2. **4K 生成成本更高**（约 2 倍于 1K/2K）
3. **推荐**：日常使用 `2K`（与 1K 同价，质量显著提升）

**支持的宽高比**：`1:1`（默认）、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`

## 退出码说明 (Exit Codes)

符合 `cli-contract.md` 规范：

| 代码 | 标签 | 描述 |
|------|-------|-------------|
| `0` | `SUCCESS` | 生成成功并已保存到本地 |
| `1` | `CONFIG_ERROR` | 参数缺失、格式错误或鉴权失败 |
| `2` | `API_ERROR` | OpenRouter API 调用失败（限流、超时等） |
| `3` | `FS_ERROR` | 本地文件系统错误（目录权限、磁盘空间等） |

## 验证与证据 (Verification)

在交付前，请确保通过以下冒烟测试：

1. **环境检查**: `node skills/image-generation/scripts/cli/openrouter.js --test` (返回 success: true)
2. **基础生成**: `node skills/image-generation/scripts/generate.js --prompt "test" --output "test.png"`
3. **路径安全**: 确保生成的图片位于 `.sisyphus/generated/` 或指定的安全路径下。

---

## 资源维护

- **扩展新 Provider**: 参考 `references/extension-guide.md`
- **配置详情**: 参考 `references/configuration.md`
- **CLI 规范**: 参考 `references/cli-contract.md`
