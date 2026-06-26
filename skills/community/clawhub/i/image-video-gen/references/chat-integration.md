# 在对话中直接返回图片的示例

## 示例 1: 使用 Markdown（最简单）

当用户请求生成图片时，直接返回：

```python
from scripts.generate_image import generate_image

result = generate_image(prompt="风景画")
if result and result["status"] == "SUCCESS":
    # 直接在回复中使用 Markdown 图片语法
    reply = f"生成成功！\n\n![风景画]({result['url']})"
```

## 示例 2: 使用 message 工具发送图片

如果需要使用 message 工具发送图片（支持更多平台）：

```python
from scripts.generate_image import generate_image
import base64

# 1. 生成并下载图片
result = generate_image(prompt="风景画", download=True)

if result and result["status"] == "SUCCESS":
    # 2. 读取图片数据
    with open(result["local_path"], "rb") as f:
        image_bytes = f.read()
    
    # 3. 转换为 base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # 4. 使用 message 工具发送
    # 注意：实际使用时通过 message 工具的 buffer 参数发送
```

## 示例 3: 直接在回复中包含图片

对于支持 Markdown 图片的平台（如 Discord、Telegram、WebChat）：

```
用户: 生成一张风景画

助手: 正在生成...

[生成完成后]

助手: 生成成功！🎨

![风景画](https://example.com/image.png)
```

## 平台兼容性

| 平台 | Markdown 图片 | 说明 |
|------|--------------|------|
| WebChat | ✅ 支持 | 直接显示 |
| Discord | ✅ 支持 | 直接显示 |
| Telegram | ✅ 支持 | 直接显示 |
| 飞书 | ⚠️ 部分支持 | 建议使用卡片消息 |
| WhatsApp | ❌ 不支持 | 需要下载后发送 |

## 最佳实践

1. **优先使用 Markdown**: 最简单，大多数平台支持
2. **同时提供链接**: 以防图片加载失败
3. **下载选项**: 对于不支持 Markdown 的平台，使用 `--download` 参数
