# 使用指南 - Image Recognition Skill

## 场景示例

### 1. OCR 文字提取

```bash
python3 recognize.py screenshot.png "提取图片中的所有文字"
```

### 2. 识别截图内容

```bash
python3 recognize.py chat_screenshot.jpg "这是什么应用的截图？显示什么内容？"
```

### 3. 识别花朵/植物

```bash
python3 recognize.py flower.jpg "这是什么花？有什么特点？"
```

### 4. 识别文档

```bash
python3 recognize.py document.jpg "提取文档的标题和主要内容"
```

### 5. 识别二维码/条形码

```bash
python3 recognize.py qr_code.png "这是什么二维码？内容是什么？"
```

## 在 OpenClaw 会话中使用

### 示例代码

```python
import base64
import requests

def recognize_image_in_session(image_path):
    """在 OpenClaw 会话中识别图片"""
    
    # 读取图片
    with open(image_path, 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()
    
    # 调用 API
    api_key = "sk-sp-e20dc070c4724e909f4b0be4d1d386e0"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen3.5-plus",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}},
                    {"type": "text", "text": "请识别这张图片中的内容"}
                ]
            }
        ]
    }
    
    response = requests.post(
        "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=90
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}"

# 使用
result = recognize_image_in_session("/path/to/image.jpg")
print(result)
```

## 批量处理

```bash
#!/bin/bash
# 批量识别文件夹中的所有图片

for img in /path/to/images/*.jpg; do
    echo "=== $img ==="
    python3 recognize.py "$img"
    echo ""
done
```

## 输出到文件

```bash
python3 recognize.py image.jpg > result.txt
```

## 与其他工具结合

### 配合截图工具

```bash
# 截图并识别
scrot /tmp/screenshot.png && python3 recognize.py /tmp/screenshot.png
```

### 配合文件管理器

创建桌面快捷方式或脚本，右键菜单调用。

## 性能优化

### 1. 图片压缩

```python
from PIL import Image

def compress_image(image_path, max_size=1024):
    img = Image.open(image_path)
    img.thumbnail((max_size, max_size))
    img.save(image_path, quality=85)
```

### 2. 并发处理

```python
from concurrent.futures import ThreadPoolExecutor

def batch_recognize(image_paths):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(recognize_image, image_paths))
    return results
```

## 常见问题

### Q: 如何获取 API Key？

A: 访问 https://help.aliyun.com/zh/model-studio/ 注册并创建 API Key

### Q: 费用如何计算？

A: 按 token 计费，图片按分辨率折算 token。具体参考官方定价。

### Q: 支持视频吗？

A: 当前版本只支持静态图片。视频需要逐帧提取后识别。

### Q: 支持手写文字吗？

A: 支持，但准确率取决于字迹清晰度。

## 更新日志

- 2026-04-01: 初始版本
