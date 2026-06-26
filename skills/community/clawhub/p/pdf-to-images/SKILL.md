---
name: pdf-to-images
version: 1.0.1
description: 将 PDF 文件转换为图片（PNG/JPG），支持指定分辨率和页码范围
metadata:
  openclaw:
    emoji: 🖼️
    requires:
      bins:
        - node
    install:
      - kind: npm
        package: pdfjs-dist
---

# PDF to Images Skill

将 PDF 文件转换为图片（PNG 或 JPG 格式），支持指定分辨率和页码范围，本地处理。

## 使用方法

### 基本转换

```bash
node index.js input.pdf -o output.png
```

### 指定格式

```bash
node index.js input.pdf -o output.jpg --format jpg
```

### 指定分辨率

```bash
node index.js input.pdf -o output.png --scale 3.0
```

### 指定页码范围

```bash
node index.js input.pdf -o output/ --pages "1-3,5"
```

## 功能特点

- ✅ 本地处理，文件不上传
- ✅ 支持 PNG/JPG 格式
- ✅ 可指定分辨率（0.5-5.0）
- ✅ 支持页码范围选择
- ✅ 多页 PDF 自动分页输出
- ✅ 隐私安全

## 示例

### 转换单页 PDF

```bash
# 转换为 PNG
node index.js document.pdf -o page.png

# 转换为 JPG
node index.js document.pdf -o page.jpg --format jpg
```

### 转换多页 PDF

```bash
# 转换所有页面
node index.js book.pdf -o pages/

# 转换指定页面
node index.js book.pdf -o pages/ --pages "1-5"

# 高分辨率转换
node index.js book.pdf -o pages/ --scale 3.0
```

### 批量处理

```bash
# 转换当前目录所有 PDF
for f in *.pdf; do node index.js "$f" -o "${f%.pdf}.png"; done
```

## 许可证

MIT

## 作者

fly3094
