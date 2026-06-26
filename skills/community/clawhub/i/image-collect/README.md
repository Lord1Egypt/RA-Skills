# Image Collect Skill

从图片中提取知识并保存到本地的 OpenClaw Skill。支持 URL、Base64、本地文件三种图片输入方式。

## 功能特性

- 支持 URL 下载、Base64 解码、本地文件复制
- 使用 Sharp 进行图像预处理（灰度化、归一化）
- 使用 Tesseract.js 进行中文 OCR 识别
- 自动提取摘要和关键词
- 知识记录存储为 JSON 文件

## 使用

```bash
# 从 URL 提取
pnpm start "https://example.com/image.png"

# 从 Base64 提取
pnpm start "data:image/png;base64,xxxx"

# 从本地文件提取
pnpm start "/tmp/image.png"
```

## 数据存储

- 图片保存在 `~/image-knowledge/images/`
- 知识记录保存在 `~/image-knowledge/data.json`

## 依赖

- axios - HTTP 请求，用于下载远程图片
- sharp - 图像预处理
- tesseract.js - OCR 文字识别
