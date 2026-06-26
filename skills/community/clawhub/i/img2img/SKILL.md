# img2img - 图生图能力

## 触发条件
当用户提到"图生图"、"AI 画图"、"生成图片"、"画一个"等时激活。

## 功能
使用 DALL-E 根据文字描述生成图片。

## 使用方式
用户发送描述文字，我调用 DALL-E 生成图片并发送。

## 技术实现
使用 OpenAI DALL-E 3 API 生成图片：

```python
import openai
import base64
import os

api_key = os.environ.get("API_KEY")

client = openai.OpenAI(api_key=api_key)

response = client.images.generate(
  model="dall-e-3",
  prompt="描述文字",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
```

## 限制
- 英文描述效果更好
- 避免生成真实人脸
- 遵守 DALL-E 使用政策
