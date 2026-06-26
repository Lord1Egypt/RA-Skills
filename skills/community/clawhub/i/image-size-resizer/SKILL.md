---
name: image-resizer
description: 图片分辨率调整工具。Use when user needs to resize images to specific dimensions. Supports custom size, batch resize, aspect ratio preservation. 图片缩放、分辨率调整、图片裁剪。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📐", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install pillow"
---

# 图片分辨率调整工具

根据用户要求调整图片分辨率，支持自定义尺寸和批量处理。

## 功能特点

- 📐 **自定义尺寸**：任意宽度×高度
- 🔄 **保持比例**：可选保持原始比例
- 📦 **批量处理**：一次调整多个图片
- 🎯 **预设尺寸**：常用尺寸快速选择
- ⚡ **高质量缩放**：LANCZOS算法

## 预设尺寸

| 用途 | 尺寸 | 说明 |
|------|------|------|
| 微信头像 | 640×640 | 方形 |
| 微博头像 | 200×200 | 方形 |
| 淘宝主图 | 800×800 | 方形 |
| 抖音封面 | 1080×1920 | 竖版 |
| 朋友圈 | 1080×1080 | 方形 |
| 小红书 | 1080×1440 | 竖版 |
| A4文档 | 2480×3508 | A4 300dpi |

## 使用方式

```
User: "把这张图片调整为640×640"
Agent: 调整图片尺寸

User: "帮我把这些图片都改成1080宽度，保持比例"
Agent: 批量调整宽度

User: "生成微信头像尺寸"
Agent: 调整为640×640
```

## Python代码

```python
from PIL import Image
import os

class ImageResizer:
    def __init__(self):
        self.presets = {
            'wechat_avatar': (640, 640),
            'weibo_avatar': (200, 200),
            'taobao_main': (800, 800),
            'douyin_cover': (1080, 1920),
            'friends_circle': (1080, 1080),
            'xiaohongshu': (1080, 1440),
            'a4_300dpi': (2480, 3508),
        }
    
    def resize(self, input_path, output_path, width=None, height=None, 
               keep_ratio=True, preset=None):
        """调整图片尺寸"""
        
        img = Image.open(input_path)
        
        # 使用预设尺寸
        if preset and preset in self.presets:
            width, height = self.presets[preset]
        
        # 计算尺寸
        if width and height:
            if keep_ratio:
                # 保持比例
                ratio = min(width / img.width, height / img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
            else:
                new_width = width
                new_height = height
        elif width:
            ratio = width / img.width
            new_width = width
            new_height = int(img.height * ratio)
        elif height:
            ratio = height / img.height
            new_width = int(img.width * ratio)
            new_height = height
        else:
            new_width = img.width
            new_height = img.height
        
        # 高质量缩放
        resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # 保存
        ext = os.path.splitext(output_path)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            if resized.mode == 'RGBA':
                resized = resized.convert('RGB')
            resized.save(output_path, 'JPEG', quality=95)
        else:
            resized.save(output_path)
        
        return output_path
    
    def batch_resize(self, input_dir, output_dir, width=None, height=None, 
                     keep_ratio=True, preset=None):
        """批量调整尺寸"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                try:
                    self.resize(input_path, output_path, width, height, keep_ratio, preset)
                    results.append({'file': filename, 'status': 'success'})
                except Exception as e:
                    results.append({'file': filename, 'status': 'error', 'error': str(e)})
        
        return results

# 使用示例
resizer = ImageResizer()

# 自定义尺寸
resizer.resize('input.jpg', 'output.jpg', width=640, height=640)

# 保持比例
resizer.resize('input.jpg', 'output.jpg', width=1080, keep_ratio=True)

# 使用预设
resizer.resize('input.jpg', 'output.jpg', preset='wechat_avatar')
```

## Notes

- 使用LANCZOS算法，高质量缩放
- 支持批量处理
- 保持比例避免变形
- 本地处理，无需网络
