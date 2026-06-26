---
name: pexels-image-downloader
description: 使用Pexels API搜索和下载高质量免费图片，支持自动调整尺寸和格式验证
metadata: {"openclaw":{"emoji":"📸","stage":"production"}}
---

# Pexels图片下载技能

使用Pexels API搜索和下载高质量的免费图片，支持自动调整尺寸、格式验证和元数据管理。特别适合小红书、社交媒体等内容创作。

## 🎯 核心功能

- ✅ **高质量图片**：专业摄影师作品，非AI生成
- ✅ **免费商业使用**：Pexels免费许可，可商用
- ✅ **智能搜索**：多关键词搜索，自动选择最佳图片
- ✅ **尺寸调整**：自动调整到目标尺寸（如小红书1242x1660）
- ✅ **格式验证**：验证图片格式、尺寸、文件大小
- ✅ **元数据管理**：保存图片信息和许可条款

## 🔑 快速开始

### 1. 获取Pexels API密钥
1. 访问 [Pexels官网](https://www.pexels.com/api/)
2. 注册免费账号
3. 获取API密钥

### 2. 基本使用
```bash
# 设置API密钥
export PEXELS_API_KEY="your_api_key_here"

# 搜索并下载图片
python download_pexels.py --query "sculpture art" --size 1242x1660

# 批量下载
python download_pexels.py --query-file keywords.txt --count 5 --output-dir images/
```

## 📦 安装

```bash
# 安装依赖
pip install requests pillow

# 或使用requirements.txt
pip install -r requirements.txt
```

## 📁 项目结构

```
pexels-image-downloader/
├── SKILL.md                    # 本文档
├── download_pexels.py          # 主下载脚本
├── requirements.txt            # Python依赖
├── config/
│   ├── default_config.json     # 默认配置
│   └── image_sizes.json        # 平台尺寸配置
├── scripts/
│   ├── batch_download.sh       # 批量下载脚本
│   ├── resize_images.py        # 图片调整脚本
│   └── validate_images.py      # 图片验证脚本
├── examples/
│   ├── xiaohongshu_example.py  # 小红书示例
│   └── social_media_example.py # 社交媒体示例
└── docs/
    ├── api_reference.md        # API参考
    └── best_practices.md       # 最佳实践
```

## 🚀 核心功能详解

### 1. 智能图片搜索
```python
# 多关键词搜索，自动选择最佳图片
python download_pexels.py \
  --query "sculpture art;clay sculpture;art studio" \
  --orientation portrait \
  --size large \
  --color any
```

### 2. 平台专用尺寸
```bash
# 小红书尺寸
python download_pexels.py --query "art" --platform xiaohongshu

# 微信尺寸  
python download_pexels.py --query "food" --platform wechat

# 微博尺寸
python download_pexels.py --query "travel" --platform weibo

# 自定义尺寸
python download_pexels.py --query "nature" --width 1920 --height 1080
```

### 3. 批量处理
```bash
# 从文件读取关键词批量下载
python download_pexels.py \
  --query-file keywords.txt \
  --count 3 \
  --output-dir downloads/ \
  --platform xiaohongshu \
  --parallel 3
```

### 4. 高级筛选
```bash
# 按颜色筛选
python download_pexels.py --query "sunset" --color red

# 按方向筛选
python download_pexels.py --query "landscape" --orientation landscape

# 按尺寸筛选
python download_pexels.py --query "portrait" --size medium
```

## ⚙️ 配置说明

### 配置文件示例
```json
{
  "api_key": "YOUR_PEXELS_API_KEY",
  "default_settings": {
    "platform": "xiaohongshu",
    "output_dir": "./downloads",
    "max_results": 10,
    "image_quality": 95,
    "save_metadata": true
  },
  "platform_sizes": {
    "xiaohongshu": {"width": 1242, "height": 1660},
    "wechat": {"width": 900, "height": 500},
    "weibo": {"width": 1000, "height": 562},
    "instagram_square": {"width": 1080, "height": 1080},
    "instagram_portrait": {"width": 1080, "height": 1350}
  },
  "search_categories": {
    "art": ["sculpture", "painting", "drawing", "craft"],
    "food": ["cuisine", "restaurant", "cooking", "recipe"],
    "travel": ["landscape", "cityscape", "adventure", "nature"],
    "lifestyle": ["home", "decor", "fashion", "wellness"]
  }
}
```

### 环境变量
```bash
# 必需：Pexels API密钥
export PEXELS_API_KEY="your_api_key_here"

# 可选：默认设置
export PEXELS_DEFAULT_PLATFORM="xiaohongshu"
export PEXELS_OUTPUT_DIR="./images"
export PEXELS_MAX_DOWNLOADS=20
export PEXELS_IMAGE_QUALITY=95
```

## 🔧 使用示例

### 示例1：小红书内容创作
```python
#!/usr/bin/env python3
"""
小红书内容图片下载示例
"""

import os
from download_pexels import PexelsDownloader

# 初始化下载器
downloader = PexelsDownloader(
    api_key=os.getenv('PEXELS_API_KEY'),
    platform='xiaohongshu',
    output_dir='./xiaohongshu_images'
)

# 下载不同主题的图片
themes = [
    ('sculpture art', 3, '雕塑教程'),
    ('handcraft diy', 2, '手工制作'),
    ('art studio', 2, '艺术工作室'),
    ('creative design', 2, '创意设计')
]

for query, count, category in themes:
    print(f"下载 {category} 图片...")
    results = downloader.download(
        query=query,
        count=count,
        orientation='portrait',
        size='large'
    )
    
    print(f"✅ 下载完成: {len(results)} 张图片")
```

### 示例2：批量内容生产
```bash
#!/bin/bash
# batch_content_creation.sh

# 定义内容主题
THEMES=(
    "健康饮食|healthy food|营养早餐"
    "健身运动|fitness workout|居家锻炼"
    "护肤美妆|skincare makeup|日常护理"
    "旅行摄影|travel photography|风景打卡"
)

# 为每个主题下载图片
for theme in "${THEMES[@]}"; do
    IFS='|' read -r title query tags <<< "$theme"
    
    echo "处理主题: $title"
    
    # 下载图片
    python download_pexels.py \
      --query "$query" \
      --count 2 \
      --platform xiaohongshu \
      --output-dir "content/$title"
    
    # 生成内容文件
    echo "标题: $title" > "content/$title/content.md"
    echo "标签: $tags" >> "content/$title/content.md"
    echo "图片: " >> "content/$title/content.md"
    ls "content/$title/"*.jpg >> "content/$title/content.md"
    
    echo "✅ 完成: $title"
done
```

## 📊 图片验证

### 自动验证
```bash
# 验证图片是否符合平台要求
python validate_images.py \
  --dir ./downloads \
  --platform xiaohongshu \
  --check-size \
  --check-format \
  --check-quality
```

### 验证报告示例
```
📊 图片验证报告
================
总计: 15 张图片
✅ 通过: 12 张
❌ 失败: 3 张

失败原因:
1. image_001.jpg: 尺寸不符 (800x600 → 需要 1242x1660)
2. image_005.jpg: 文件过大 (8.2MB → 建议 <5MB)
3. image_012.jpg: 格式不支持 (.bmp → 需要 .jpg/.png)
```

## 🎯 最佳实践

### 1. 搜索策略
- **使用具体关键词**：避免过于宽泛的搜索
- **组合搜索**：使用多个相关关键词
- **利用分类**：使用预设的分类关键词
- **筛选条件**：使用颜色、方向、尺寸筛选

### 2. 图片管理
- **分类存储**：按主题/日期分类存储图片
- **保留元数据**：保存图片信息和许可条款
- **定期清理**：删除不符合要求的图片
- **备份重要图片**：重要图片多重备份

### 3. 合规使用
- **遵守许可**：Pexels图片可免费商用，但建议署名
- **避免侵权**：不要声称图片为自己拍摄
- **尊重版权**：如有疑问，查看具体图片许可
- **记录来源**：保存图片ID和摄影师信息

## 🔧 故障排除

### 常见问题
1. **API密钥无效**
   ```bash
   # 检查API密钥
   echo $PEXELS_API_KEY
   
   # 重新设置
   export PEXELS_API_KEY="new_api_key_here"
   ```

2. **下载失败**
   ```bash
   # 检查网络连接
   curl -I https://api.pexels.com
   
   # 检查API限制
   # 免费账户每月200次请求
   ```

3. **图片质量差**
   ```bash
   # 使用大尺寸图片
   python download_pexels.py --query "xxx" --size large
   
   # 提高下载质量
   python download_pexels.py --query "xxx" --quality 100
   ```

### 错误代码
- `ERR_API_KEY_INVALID`: API密钥无效
- `ERR_NETWORK`: 网络连接问题
- `ERR_NO_RESULTS`: 搜索无结果
- `ERR_DOWNLOAD_FAILED`: 下载失败
- `ERR_IMAGE_INVALID`: 图片格式无效

## 📈 高级功能

### 1. 图片后处理
```python
from PIL import Image, ImageFilter, ImageEnhance

# 图片增强
def enhance_image(image_path):
    img = Image.open(image_path)
    
    # 调整亮度
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    # 调整对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    
    # 轻微锐化
    img = img.filter(ImageFilter.SHARPEN)
    
    # 保存
    img.save(image_path, quality=95, optimize=True)
```

### 2. 智能裁剪
```python
# 人脸识别裁剪（如果图片含有人脸）
def smart_crop_for_faces(image_path, target_size):
    import face_recognition
    
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    
    if face_locations:
        # 以人脸为中心裁剪
        top, right, bottom, left = face_locations[0]
        face_center_x = (left + right) // 2
        face_center_y = (top + bottom) // 2
        
        # 计算裁剪区域
        # ... 裁剪逻辑
```

### 3. 批量重命名
```bash
# 按日期和主题重命名
python rename_images.py \
  --dir ./downloads \
  --pattern "{date}_{theme}_{index}.jpg" \
  --date-format "%Y%m%d" \
  --theme "sculpture"
```

## 📞 支持

### 资源链接
- [Pexels API文档](https://www.pexels.com/api/documentation/)
- [Pexels免费图片库](https://www.pexels.com)
- [Python PIL文档](https://pillow.readthedocs.io/)
- [图片处理最佳实践](https://developers.google.com/speed/docs/insights/OptimizeImages)

### 联系支持
- 问题反馈：创建GitHub Issue
- 功能请求：提交Feature Request
- 紧急问题：查看故障排除章节

---

**使用此技能，你可以轻松获取高质量、合法、免费的图片资源，大幅提升内容创作效率和质量！** 📸