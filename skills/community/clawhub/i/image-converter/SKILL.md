---
name: image-converter
description: 图片格式转换工具。支持PNG、JPG、WEBP、SVG等格式互转。Use when user needs to convert image formats. 图片转换、格式转换、PNG转JPG、JPG转PNG。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install pillow cairosvg"
---

# 图片格式转换工具

支持PNG、JPG、WEBP、SVG等格式互转。

## 功能特点

- 🖼️ **多格式支持**：PNG/JPG/WEBP/SVG/GIF/BMP
- 🔄 **双向转换**：任意格式互转
- 📦 **批量转换**：一次转换多个文件
- 🎨 **质量可控**：自定义压缩质量
- ⚡ **快速转换**：本地处理，无需网络

## 支持格式

| 格式 | 输入 | 输出 | 说明 |
|------|------|------|------|
| PNG | ✅ | ✅ | 无损压缩 |
| JPG | ✅ | ✅ | 有损压缩 |
| WEBP | ✅ | ✅ | 现代格式 |
| SVG | ⚠️ | ✅ | 矢量图 |
| GIF | ✅ | ✅ | 动图 |
| BMP | ✅ | ✅ | 位图 |

## 使用方式

```
User: "把这张PNG转成JPG"
Agent: 转换图片格式

User: "把这些图片都转成WEBP"
Agent: 批量转换

User: "JPG转SVG"
Agent: 转换为矢量图
```

## Python代码

```python
from PIL import Image
import os

class ImageConverter:
    def __init__(self):
        self.formats = {
            'png': 'PNG',
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'webp': 'WEBP',
            'gif': 'GIF',
            'bmp': 'BMP'
        }
    
    def convert(self, input_path, output_path, quality=95):
        """转换图片格式"""
        img = Image.open(input_path)
        
        # 获取输出格式
        ext = os.path.splitext(output_path)[1].lower().replace('.', '')
        
        if ext in ['jpg', 'jpeg']:
            # JPG需要RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            img.save(output_path, 'JPEG', quality=quality)
        elif ext == 'png':
            img.save(output_path, 'PNG')
        elif ext == 'webp':
            img.save(output_path, 'WEBP', quality=quality)
        elif ext == 'gif':
            img.save(output_path, 'GIF')
        elif ext == 'bmp':
            img.save(output_path, 'BMP')
        else:
            img.save(output_path)
        
        return output_path
    
    def batch_convert(self, input_dir, output_dir, target_format='jpg', quality=95):
        """批量转换"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp')):
                input_path = os.path.join(input_dir, filename)
                output_filename = os.path.splitext(filename)[0] + f'.{target_format}'
                output_path = os.path.join(output_dir, output_filename)
                
                try:
                    self.convert(input_path, output_path, quality)
                    results.append({'file': filename, 'status': 'success'})
                except Exception as e:
                    results.append({'file': filename, 'status': 'error', 'error': str(e)})
        
        return results

# 使用示例
converter = ImageConverter()
converter.convert('input.png', 'output.jpg', quality=95)
```

## Notes

- 本地处理，无需网络
- 支持批量转换
- PNG转JPG会丢失透明度
- SVG输出需要cairosvg
