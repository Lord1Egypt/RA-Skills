\# image-scanner



\## Description

扫描指定文件夹，识别图片格式、分析主色调和风格，自动分类整理摄影作品。



\## Triggers

\- 扫描图片文件夹

\- 分析照片类型

\- 整理摄影作品

\- 识别图片颜色风格

\- 批量处理图片文件



\## Capabilities

\- 扫描目录中的所有图片文件

\- 识别图片格式（JPG/PNG/RAW/HEIC/TIFF 等）

\- 分析图片主色调（冷色/暖色/黑白/鲜艳）

\- 按风格分类（人像/风景/静物/建筑等）

\- 生成分类报告

\- 可选：自动创建子文件夹并移动文件



\## Usage

```bash

openclaw skill image-scanner --path <目录路径> --action scan

openclaw skill image-scanner --path <目录路径> --action classify --output <输出目录>

