---
name: image-watermark
description: >
  图片批量加水印。输入图片文件+水印文字，自动在图片上添加水印并返回处理后的图片。
  触发词：加水印、图片水印、批量水印。
version: 1.0.0
author: Dick Dunkel
license: MIT-0
tags: [utility, image, watermark]
category: utility
created_by: agent
---

# 图片批量加水印

## 触发条件

用户发送图片并要求加水印时触发。

## 必需输入

| 输入项 | 必需 | 说明 |
|--------|------|------|
| 图片文件 | ✅ | 1张或多张图片（PNG/JPG） |
| 水印文字 | ✅ | 要添加的水印内容 |
| 水印位置 | 可选 | 居中/右下角/平铺（默认：平铺） |
| 透明度 | 可选 | 0-100%（默认：30%） |
| 字体大小 | 可选 | 自动/小/中/大（默认：自动根据图片尺寸） |

## 执行流程

### 脚本实现

```python
# 使用 Pillow 库
from PIL import Image, ImageDraw, ImageFont
import math

def add_watermark(input_path, output_path, text, opacity=0.3, mode='tile'):
    """
    mode: 'tile'(平铺) / 'center'(居中) / 'corner'(右下角)
    """
    img = Image.open(input_path).convert('RGBA')
    txt_layer = Image.new('RGBA', img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    
    # 自动计算字体大小（图片宽度的5%）
    font_size = max(int(img.width * 0.05), 20)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', font_size)
    except:
        font = ImageFont.load_default()
    
    alpha = int(255 * opacity)
    
    if mode == 'tile':
        # 平铺模式：45度角重复
        bbox = draw.textbbox((0,0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        for y in range(-img.height, img.height*2, int(th*3)):
            for x in range(-img.width, img.width*2, int(tw*2)):
                draw.text((x, y), text, fill=(128,128,128,alpha), font=font)
        txt_layer = txt_layer.rotate(45, expand=False, center=(img.width//2, img.height//2))
    elif mode == 'center':
        bbox = draw.textbbox((0,0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        x = (img.width - tw) // 2
        y = (img.height - th) // 2
        draw.text((x, y), text, fill=(128,128,128,alpha), font=font)
    elif mode == 'corner':
        bbox = draw.textbbox((0,0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        x = img.width - tw - 20
        y = img.height - th - 20
        draw.text((x, y), text, fill=(128,128,128,alpha), font=font)
    
    result = Image.alpha_composite(img, txt_layer)
    result = result.convert('RGB')
    result.save(output_path, quality=95)
```

### 依赖
- `Pillow` (pip3 install Pillow)
- 中文字体：`wqy-zenhei`（apt install fonts-wqy-zenhei）

## 输出规范

- 处理后的图片保存为 PNG/JPG
- 通过企微发送给用户
- 如多张图片，逐一处理后打包发送

## 质量标准

- ✅ 水印不遮挡主要内容（透明度合理）
- ✅ 支持中文水印
- ✅ 自动适配图片尺寸
- ❌ 不破坏原图质量
