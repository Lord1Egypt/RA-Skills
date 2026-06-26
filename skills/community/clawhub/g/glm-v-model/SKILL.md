---
name: glm-v-model
description: |
  智谱 GLM-4V/4.6V 视觉模型调用技能。用于图像/视频理解、多模态对话、图表分析等任务。
  当用户提到：图片理解、图像识别、视觉模型、GLM-4V、GLM-4.6V、多模态分析、看图说话、图表分析、视频理解时使用此技能。
---

# GLM 视觉模型调用

本技能提供调用智谱 AI 的 GLM-4V 和 GLM-4.6V 视觉模型的能力，支持图像理解、视频分析、图表解读等功能。

## 支持的模型

| 模型 | 说明 | 特点 |
|------|------|------|
| glm-4v | GLM-4 视觉模型 | 基础视觉理解 |
| glm-4.6v | GLM-4.6V 视觉模型 | 更强的视觉理解能力，支持更长上下文 |

## 快速使用

### 基本图像理解

```python
from zai import ZhipuAiClient
import base64

client = ZhipuAiClient(api_key="YOUR_API_KEY")

# 读取本地图片并转为 base64
with open("image.jpg", "rb") as f:
    img_base = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base}"}},
            {"type": "text", "content": "描述这张图片"}
        ]
    }],
    thinking={"type": "enabled"}
)
print(response.choices[0].message.content)
```

### 使用图片URL

```python
response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
            {"type": "text", "content": "这张图片里有什么？"}
        ]
    }]
)
```

### 多图理解

```python
response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "图片1 base64 或 URL"}},
            {"type": "image_url", "image_url": {"url": "图片2 base64 或 URL"}},
            {"type": "text", "content": "比较这两张图片的异同"}
        ]
    }]
)
```

### 视频理解（GLM-4.6V）

```python
# 支持理解视频内容
response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "video_url", "video_url": {"url": "视频URL"}},
            {"type": "text", "content": "描述这个视频的内容"}
        ]
    }]
)
```

## 使用脚本

项目中已包含脚本 `script/infer_glmv.py`，可直接调用：

```python
import sys
sys.path.append('/Users/guobaokui/.openclaw/workspace_multmodal/skills/glm-v-model/script')
from infer_glmv import glm_v

# 使用方式
# glm_v(['image.jpg'], '描述图片', 'glm-4.6v')
```

## 常用场景

| 场景 | Prompt 示例 |
|------|-------------|
| 图片描述 | "详细描述这张图片的内容" |
| 图表分析 | "分析这张图表数据" |
| 文字识别(OCR) | "提取图片中的文字" |
| 物体识别 | "图片中有哪些物体" |
| 场景理解 | "这是什么地方" |
| 多图对比 | "比较这两张图片的异同" |
| 视频理解 | "总结这个视频的内容" |

## 注意事项

1. **API Key**: 需要智谱 AI 的 API Key，可从 https://open.bigmodel.cn 获取
2. **图片格式**: 支持 JPEG、PNG、WebP 等常见格式
3. **图片大小**: 单张图片建议不超过 10MB
4. **thinking**: 可启用深度思考模式 `thinking={"type": "enabled"}`
5. **计费**: 按 token 计费，图片会转换为 token 消耗