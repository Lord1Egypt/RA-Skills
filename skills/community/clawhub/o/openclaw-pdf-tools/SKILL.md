---
name: pdf-toolkit
description: "PDF工具箱 - 合并、拆分、压缩、转换PDF文件。支持批量处理，无需联网，本地执行。"
version: 1.0.0
author: OpenClaw
license: MIT
tags: [pdf, document, tool, utility]
---

# 📄 PDF工具箱

一个强大的本地PDF处理技能，无需联网，保护隐私安全。

## 功能特性

- ✅ **PDF合并** - 多个PDF合并为一个
- ✅ **PDF拆分** - 按页码拆分PDF
- ✅ **PDF压缩** - 减小PDF文件大小
- ✅ **PDF转图片** - 将PDF页面转为图片
- ✅ **图片转PDF** - 将图片合并为PDF
- ✅ **PDF提取文字** - 提取PDF中的文本内容
- ✅ **PDF添加水印** - 为PDF添加文字水印
- ✅ **PDF加密/解密** - 设置或移除PDF密码

## 安装

```bash
npx clawhub@latest install pdf-toolkit
```

## 依赖

需要安装以下系统依赖：

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils ghostscript imagemagick

# macOS
brew install poppler ghostscript imagemagick

# Windows (使用 scoop 或 chocolatey)
scoop install poppler ghostscript imagemagick
# 或
choco install poppler ghostscript imagemagick
```

## 使用方法

### 1. PDF合并

```bash
node scripts/merge.js file1.pdf file2.pdf output.pdf
```

### 2. PDF拆分

```bash
# 拆分为单页
node scripts/split.js input.pdf output_dir/

# 按页码范围拆分
node scripts/split.js input.pdf output.pdf 1-5
```

### 3. PDF压缩

```bash
node scripts/compress.js input.pdf output.pdf
```

### 4. PDF转图片

```bash
# 转换所有页面
node scripts/pdf2img.js input.pdf output_dir/

# 指定分辨率 (dpi)
node scripts/pdf2img.js input.pdf output_dir/ --dpi 150
```

### 5. 图片转PDF

```bash
node scripts/img2pdf.js image1.png image2.jpg output.pdf
```

### 6. 提取文字

```bash
node scripts/extract-text.js input.pdf output.txt
```

### 7. 添加水印

```bash
node scripts/watermark.js input.pdf "机密文件" output.pdf
```

### 8. 加密/解密

```bash
# 加密
node scripts/encrypt.js input.pdf output.pdf password123

# 解密
node scripts/decrypt.js input.pdf output.pdf password123
```

## API示例

也可以在代码中直接调用：

```javascript
const { merge, split, compress, pdf2img, img2pdf } = require('pdf-toolkit');

// 合并PDF
await merge(['file1.pdf', 'file2.pdf'], 'merged.pdf');

// 拆分PDF
await split('input.pdf', 'output_dir/');

// 压缩PDF
await compress('input.pdf', 'compressed.pdf');

// PDF转图片
await pdf2img('input.pdf', 'output_dir/', { dpi: 150 });

// 图片转PDF
await img2pdf(['img1.png', 'img2.jpg'], 'output.pdf');
```

## 注意事项

1. 处理大文件时可能需要较长时间
2. 加密的PDF需要先解密才能进行其他操作
3. ImageMagick默认限制了PDF转换，可能需要修改配置：
   ```bash
   # 编辑 /etc/ImageMagick-6/policy.xml
   # 将 <policy domain="coder" rights="none" pattern="PDF" />
   # 改为 <policy domain="coder" rights="read|write" pattern="PDF" />
   ```

## 常见问题

### Q: 为什么PDF转图片失败？
A: 检查ImageMagick的安全策略配置，详见上方注意事项。

### Q: 压缩效果不明显？
A: 压缩效果取决于PDF内容类型。图片较多的PDF压缩效果更明显。

### Q: 支持中文文件名吗？
A: 支持，但建议使用英文路径避免编码问题。

## 更新日志

### v1.0.0 (2026-03-23)
- 初始版本
- 支持基础PDF操作

## 许可证

MIT License