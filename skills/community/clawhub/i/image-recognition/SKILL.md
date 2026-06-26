---
name: image-recognition
description: "图片识别 - 通用图片识别技能，支持 OCR 文字提取、物体识别、场景分析等。自动使用用户配置的视觉模型，适用于 Android/Termux 环境。"
homepage: https://clawhub.ai/skills/image-recognition
version: 1.0.0
author: 小 MIX
changelog: "Initial release: Android/Termux 图片识别技能，自动使用用户配置的视觉模型，绕过 sharp 模块限制"
metadata: { "openclaw": { "emoji": "👁️", "requires": { "python": ["requests", "Pillow"] } } }
---

# Image Recognition Skill (图片识别)

**适用于 Android/Termux 环境的图片识别技能**

## 何时使用

✅ **使用此技能：**

- "识别这张图片"
- "图片里有什么"
- "提取图片中的文字"
- OCR 文字识别
- 物体/场景识别
- 截图内容分析

❌ **不使用此技能：**

- 用户明确要求用其他 OCR 服务
- 图片文件不存在或损坏

## 技术原理

**核心方法：**
1. 读取图片文件为二进制
2. Base64 编码
3. 调用用户配置的视觉模型 API
4. 返回识别结果

**为什么不用 sharp：**
- `sharp` 模块在 Termux (Android arm64) 无法加载
- 直接使用 Python + requests 调用 API 更稳定

**支持的模型提供商：**
- ✅ Bailian (通义千问) - `qwen3.5-plus`, `qwen-vl-max`
- ✅ OpenRouter - 支持视觉的模型
- ✅ 其他 OpenAI 兼容接口 - 支持 `image_url` 格式的模型

## 配置

### 方式一：使用 OpenClaw 配置的模型（推荐）

脚本会自动读取 OpenClaw 的配置文件 `~/.openclaw/openclaw.json`，使用已配置的模型和 API Key。

**无需额外配置！** 只要你的 OpenClaw 配置了支持视觉的模型即可。

### 方式二：手动配置环境变量

```bash
# Bailian (通义千问)
export IMAGE_MODEL_PROVIDER="bailian"
export IMAGE_MODEL_API_KEY="sk-sp-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="qwen3.5-plus"
export IMAGE_MODEL_ENDPOINT="https://coding.dashscope.aliyuncs.com/v1/chat/completions"

# OpenRouter
export IMAGE_MODEL_PROVIDER="openrouter"
export IMAGE_MODEL_API_KEY="sk-or-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="qwen/qwen-2.5-vl-72b-instruct"
export IMAGE_MODEL_ENDPOINT="https://openrouter.ai/api/v1/chat/completions"
```

### Python 依赖

```bash
pip3 install requests Pillow
```

## 使用方法

### 方式一：自动检测（推荐）

脚本会自动读取 OpenClaw 配置文件，使用已配置的**支持视觉的模型**。

```bash
python3 ~/.openclaw/skills/image-recognition/recognize.py /path/to/image.jpg
```

**无需额外配置！** 只要你的 OpenClaw 配置了支持视觉的模型（如 `qwen3.5-plus`）即可。

### 方式二：手动指定环境变量

```bash
# Bailian (通义千问)
export IMAGE_MODEL_PROVIDER="bailian"
export IMAGE_MODEL_API_KEY="sk-sp-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="qwen3.5-plus"

# OpenRouter
export IMAGE_MODEL_PROVIDER="openrouter"
export IMAGE_MODEL_API_KEY="sk-or-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="qwen/qwen-2.5-vl-72b-instruct"

# 使用
python3 recognize.py /path/to/image.jpg
```

### 方式三：在 Python 代码中使用

```python
from recognize import recognize_image, get_model_config

# 自动检测配置
config = get_model_config()
print(f"使用模型：{config['provider']}/{config['model']}")

# 识别图片
result = recognize_image("/path/to/image.jpg", "提取图片中的文字")
print(result)

# 或手动指定配置
custom_config = {
    "provider": "bailian",
    "api_key": "sk-sp-xxx",
    "model": "qwen3.5-plus",
    "endpoint": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
    "headers": {"Authorization": f"Bearer sk-sp-xxx"}
}
result = recognize_image("/path/to/image.jpg", config=custom_config)
```

## API 配置（高级）

**大多数用户不需要手动配置**，脚本会自动使用 OpenClaw 的模型配置。

### 自动检测逻辑

1. **优先使用环境变量**（如果设置了）
2. **其次读取 OpenClaw 配置**（`~/.openclaw/openclaw.json`）
3. **最后使用默认配置**（Bailian qwen3.5-plus）

### 手动配置各提供商

#### Bailian (通义千问)

```bash
export IMAGE_MODEL_PROVIDER="bailian"
export IMAGE_MODEL_API_KEY="sk-sp-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="qwen3.5-plus"
# 端点自动设置为：https://coding.dashscope.aliyuncs.com/v1/chat/completions
```

#### OpenRouter

```bash
export IMAGE_MODEL_PROVIDER="openrouter"
export IMAGE_MODEL_API_KEY="sk-or-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="qwen/qwen-2.5-vl-72b-instruct"
# 端点自动设置为：https://openrouter.ai/api/v1/chat/completions
```

#### 其他 OpenAI 兼容接口

```bash
export IMAGE_MODEL_PROVIDER="openai"
export IMAGE_MODEL_API_KEY="sk-xxxxxxxxxxxxx"
export IMAGE_MODEL_NAME="gpt-4o"
export IMAGE_MODEL_ENDPOINT="https://api.openai.com/v1/chat/completions"
```

## 支持的平台

✅ **已测试：**
- Android (Termux) - arm64
- Linux - x86_64, arm64
- macOS - x86_64, arm64

✅ **支持的图片格式：**
- JPEG/JPG
- PNG
- GIF (静态)
- WebP
- BMP

## 常见问题

### Q: 为什么不用 sharp 模块？

A: `sharp` 依赖 libvips，在 Termux (Android) 上编译和安装非常困难。直接使用 Python + requests 调用 API 更简单稳定。

### Q: API Key 无效怎么办？

A: 检查：
1. API Key 是否正确（`sk-sp-` 开头）
2. 是否使用了正确的端点（`coding.dashscope.aliyuncs.com`）
3. API Key 是否已开通视觉模型权限

### Q: 识别速度慢怎么办？

A: 
- 图片太大 → 压缩到 2MB 以内
- 网络问题 → 检查网络连接
- 模型响应慢 → 尝试 `qwen-turbo`

### Q: 识别不准确怎么办？

A:
- 图片模糊 → 提供更清晰的图片
- 文字太小 → 放大或裁剪
- 特殊字体 → 尝试其他 OCR 服务

## 成本

- `qwen3.5-plus`：约 0.002 元/次（1000x1000 图片）
- 具体价格参考：https://help.aliyun.com/zh/model-studio/pricing

## 替代方案

如无 Bailian API，可使用：
- OpenRouter: `qwen/qwen-2.5-vl-72b-instruct`
- 本地 OCR: `tesseract`（需要安装）
- 其他云服务：百度 OCR、腾讯 OCR 等

## 更新日志

- **2026-04-01**: 初始版本，支持 Bailian API 图片识别
- 适用于 Android/Termux 环境，绕过 sharp 模块限制
