# Pillow Skill 使用示例

[English](EXAMPLES.md) | 简体中文

Pillow图像处理技能的全面使用示例。

## 示例1: 基础图像编辑

### 调整图像大小
```bash
# 调整到指定宽度（高度自动计算）
python scripts/image_editor.py portrait.jpg resized.jpg --width 600

# 调整到指定尺寸（忽略纵横比）
python scripts/image_editor.py photo.jpg stretched.jpg \
    --width 800 --height 600 --no-aspect
```

### 裁剪图像
```bash
# 从中心裁剪正方形
python scripts/image_editor.py photo.jpg cropped.jpg \
    --crop 200 200 800 800

# 提取特定区域
python scripts/image_editor.py screenshot.png section.png \
    --crop 0 0 1920 400
```

### 旋转和翻转
```bash
# 旋转90度
python scripts/image_editor.py photo.jpg rotated.jpg --rotate 90

# 水平翻转（镜像）
python scripts/image_editor.py selfie.jpg mirrored.jpg --flip horizontal

# 组合旋转和翻转
python scripts/image_editor.py input.jpg output.jpg \
    --rotate 45 --flip vertical
```

## 示例2: 颜色调整

### 亮度和对比度
```bash
# 提亮暗照片
python scripts/image_editor.py dark.jpg bright.jpg --brightness 1.5

# 增加对比度
python scripts/image_editor.py flat.jpg contrasted.jpg --contrast 1.3

# 降低亮度并增加对比度
python scripts/image_editor.py overexposed.jpg fixed.jpg \
    --brightness 0.8 --contrast 1.2
```

### 色彩饱和度
```bash
# 转换为灰度图
python scripts/image_editor.py color.jpg gray.jpg --color 0.0

# 增强色彩
python scripts/image_editor.py dull.jpg vivid.jpg --color 1.5

# 微妙降低饱和度
python scripts/image_editor.py saturated.jpg natural.jpg --color 0.9
```

### 锐度
```bash
# 锐化图像
python scripts/image_editor.py blurry.jpg sharp.jpg --sharpness 2.0

# 轻微锐化
python scripts/image_editor.py photo.jpg enhanced.jpg --sharpness 1.3
```

## 示例3: 滤镜

### 应用内置滤镜
```bash
# 模糊效果
python scripts/image_editor.py sharp.jpg blurred.jpg --filter blur

# 边缘检测
python scripts/image_editor.py photo.jpg edges.jpg --filter edge_enhance

# 艺术浮雕效果
python scripts/image_editor.py photo.jpg embossed.jpg --filter emboss

# 锐化滤镜
python scripts/image_editor.py soft.jpg sharpened.jpg --filter sharpen
```

## 示例4: 格式转换

### 格式间转换
```bash
# PNG转JPEG
python scripts/image_editor.py image.png image.jpg --format JPEG --quality 95

# JPEG转PNG（无损）
python scripts/image_editor.py photo.jpg photo.png --format PNG

# 转换为WebP（现代格式）
python scripts/image_editor.py image.jpg image.webp --format WEBP --quality 90
```

## 示例5: 批量处理

### 为画廊创建缩略图
```bash
# 为所有图像生成300x300缩略图
python scripts/batch_processor.py ./photos ./thumbnails \
    --thumbnail 300 300 \
    --workers 8
```

### 批量调整大小
```bash
# 将所有图像调整为1920x1080
python scripts/batch_processor.py ./originals ./resized \
    --resize 1920 1080

# 调整特定文件类型
python scripts/batch_processor.py ./images ./output \
    --pattern "*.jpg" \
    --resize 800 600
```

### 批量格式转换
```bash
# 将所有PNG转换为JPEG
python scripts/batch_processor.py ./pngs ./jpegs \
    --format JPEG \
    --quality 90

# 转换为灰度图
python scripts/batch_processor.py ./color ./bw \
    --grayscale
```

### 批量亮度调整
```bash
# 提亮目录中的所有图像
python scripts/batch_processor.py ./dark_photos ./brightened \
    --brightness 1.3
```

## 示例6: 水印

### 文字水印
```bash
# 简单版权文字
python scripts/watermark.py photo.jpg marked.jpg \
    --text "© 2026 张三" \
    --position bottom-right

# 居中水印
python scripts/watermark.py image.jpg output.jpg \
    --text "机密" \
    --position center \
    --font-size 72 \
    --opacity 100

# 自定义颜色和位置
python scripts/watermark.py photo.jpg branded.jpg \
    --text "我的品牌" \
    --position top-left \
    --color red \
    --font-size 48 \
    --margin 20
```

### Logo水印
```bash
# 角落公司logo
python scripts/watermark.py product.jpg branded.jpg \
    --image logo.png \
    --position bottom-right \
    --scale 0.15 \
    --opacity 180

# 大型居中水印
python scripts/watermark.py image.jpg watermarked.jpg \
    --image watermark.png \
    --position center \
    --scale 0.4 \
    --opacity 128

# 微妙的右上角logo
python scripts/watermark.py photo.jpg output.jpg \
    --image brand_icon.png \
    --position top-right \
    --scale 0.1 \
    --opacity 200 \
    --margin 15
```

## 示例7: 图像信息

### 提取元数据
```bash
# 显示所有图像信息
python scripts/image_info.py photo.jpg

# 将信息保存为JSON
python scripts/image_info.py image.jpg -o info.json --format json

# 批量提取多张图像的信息
for img in *.jpg; do
    python scripts/image_info.py "$img" -o "${img%.jpg}_info.json" --format json
done
```

## 示例8: 组合工作流

### 完整照片增强
```bash
# 步骤1: 如需旋转
python scripts/image_editor.py raw.jpg rotated.jpg --rotate 90

# 步骤2: 裁剪去除边框
python scripts/image_editor.py rotated.jpg cropped.jpg \
    --crop 50 50 1850 1350

# 步骤3: 增强色彩和锐度
python scripts/image_editor.py cropped.jpg enhanced.jpg \
    --brightness 1.1 \
    --contrast 1.2 \
    --color 1.15 \
    --sharpness 1.3

# 步骤4: 添加水印
python scripts/watermark.py enhanced.jpg final.jpg \
    --text "© 2026 摄影工作室" \
    --position bottom-right \
    --opacity 150

# 步骤5: 优化用于网页
python scripts/image_editor.py final.jpg web_ready.jpg \
    --width 1200 \
    --quality 85
```

### 批量产品摄影工作流
```bash
# 1. 批量裁剪所有产品
python scripts/batch_processor.py ./raw_products ./cropped \
    --resize 2000 2000

# 2. 为所有添加水印
for img in ./cropped/*.jpg; do
    python scripts/watermark.py "$img" "./watermarked/$(basename $img)" \
        --image company_logo.png \
        --position bottom-right \
        --scale 0.12 \
        --opacity 180
done

# 3. 创建多种尺寸
python scripts/batch_processor.py ./watermarked ./large \
    --resize 1200 1200 \
    --quality 90

python scripts/batch_processor.py ./watermarked ./medium \
    --thumbnail 600 600 \
    --quality 85

python scripts/batch_processor.py ./watermarked ./small \
    --thumbnail 300 300 \
    --quality 80
```

### 社交媒体图像准备
```bash
# Instagram正方形格式(1080x1080)
python scripts/image_editor.py photo.jpg instagram.jpg \
    --crop 0 200 1080 1280 \
    --resize 1080 1080 \
    --brightness 1.1 \
    --color 1.2 \
    --sharpen 1.2 \
    --quality 95

# Facebook封面照片(820x312)
python scripts/image_editor.py wide.jpg fb_cover.jpg \
    --resize 820 312 --no-aspect \
    --quality 90

# Twitter头图(1500x500)
python scripts/image_editor.py banner.jpg twitter_header.jpg \
    --resize 1500 500 --no-aspect \
    --quality 92
```

## 示例9: 高级技巧

### HDR风格效果
```bash
# 创建伪HDR外观
python scripts/image_editor.py photo.jpg hdr_look.jpg \
    --contrast 1.4 \
    --color 1.3 \
    --sharpness 1.5 \
    --filter detail
```

### 复古效果
```bash
# 创建复古/褪色外观
python scripts/image_editor.py modern.jpg vintage.jpg \
    --color 0.7 \
    --contrast 0.9 \
    --brightness 1.1
```

### 创建缩略图网格
```bash
# 首先创建单独的缩略图
python scripts/batch_processor.py ./photos ./grid_thumbs \
    --thumbnail 200 200
```

## 技巧和最佳实践

### 1. 始终备份原始文件
```bash
# 处理前创建备份
cp -r ./originals ./originals_backup
```

### 2. 先在单张图像上测试
```bash
# 在单张图像上测试处理
python scripts/image_editor.py test.jpg test_output.jpg --brightness 1.3

# 如果满意，批量处理
python scripts/batch_processor.py ./images ./output --brightness 1.3
```

### 3. 使用适当的质量设置
- **网页照片**: quality 80-85
- **打印照片**: quality 95-100
- **缩略图**: quality 75-80

### 4. 选择正确格式
- **照片**: JPEG
- **图形/logo**: PNG
- **需要透明**: PNG或WebP
- **现代网页**: WebP配合JPEG后备

### 5. 保留EXIF数据
如需要，处理前提取信息：
```bash
python scripts/image_info.py original.jpg -o metadata.json --format json
```

## 故障排除

### 问题: 图像质量下降
```bash
# 使用更高质量设置
--quality 95

# 避免多次压缩（一次处理所有操作）
```

### 问题: 批量处理缓慢
```bash
# 增加工作线程
--workers 8
```

### 问题: 大图像内存错误
```bash
# 以较小批次处理图像
# 或先调整大小再进行其他操作
```

查看 [SKILL_CN.md](SKILL_CN.md) 获取完整文档，查看 [references/](references/) 获取详细的Pillow指南。
