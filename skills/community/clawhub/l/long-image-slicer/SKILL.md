---
name: long-image-slicer
version: 1.0.0
description: 智能长截图切片工具。将超长图片（如聊天记录、长截图）按 9:16 比例智能切片，确保文字/拼音不被分割，输出 PDF/ZIP/切片图片。使用场景：用户发送长截图要求切片、分割、转 PDF 等。
author: 果光
license: MIT
tags: [image, pdf, screenshot, slice, long-image]
---

# Long Image Slicer - 长截图智能切片

## 触发条件

当用户提出以下需求时触发此技能：
- 长截图切片/分割
- 聊天记录转 PDF
- 超长图片处理
- 确保文字不被截断的切片

## 工作流程

### 1. 获取源图片

**方式 A：用户直接发送**
- 保存到临时目录

**方式 B：用户提供 URL**
```bash
curl -L "<图片 URL>" -o /tmp/source.jpg
```

**方式 C：用户指定本地路径**
- 直接使用用户提供的路径

### 2. 执行切片

```bash
cd ~/.openclaw/skills/long-image-slicer
python3 scripts/slice_processor.py <源图片路径> [输出目录]
```

脚本自动：
1. 分析图片内容密度（检测文字行）
2. 智能计算切分位置（确保文字/拼音完整）
3. 生成切片图片（slice_01.jpg ~ slice_48.jpg）
4. 保存到 `输出目录/slices_v7/`

### 3. 生成 PDF

```bash
python3 scripts/create_pdf.py <切片目录> [输出 PDF 路径]
```

PDF 规格：
- A4 大小 (21.0cm × 29.7cm)
- 按高度缩放，确保所有切片完整显示
- 左右边距自动计算（相等）
- 上下边距 1cm
- 每页一张切片，垂直居中
- 页码：右下角（距右边缘 1cm，距下边缘 0.5cm）

### 4. 交付结果

输出文件：
- `输出目录/slices_v7/` - 切片图片目录
- `输出目录/slices_v7.pdf` - A4 PDF 文档

## 脚本说明

### scripts/slice_processor.py

**核心算法 v7 - 精细平衡版**

- 目标切片高度：1388 像素（按 9:16 比例）
- 搜索范围：±250 像素
- 综合评分：间隙大小 (50 分) + 距离 (30 分) + 高度合理性 (20 分)
- 确保 81% 切片在 1300-1400 像素范围内

**依赖**：
```bash
pip3 install Pillow numpy python-docx
```

### scripts/create_pdf.py

**PDF 生成器 v5**

- 使用 reportlab 库
- 按高度缩放，确保所有切片完整显示
- 左右边距自动计算（相等）
- 右下角页码

**依赖**：
```bash
pip3 install reportlab
```

## 示例对话

**用户**：这张长截图帮我切片，文字不要截断

**助手**：收到，使用长截图切片工具：
1. 分析文字行位置
2. 智能切分（确保拼音完整）
3. 生成 48 个切片 + PDF

---

**用户**：把聊天记录转 PDF，A4 打印

**助手**：可以，生成长截图 PDF：
- A4 尺寸，所有切片完整显示
- 右下角页码

## 版本历史

- **v7**: 精细平衡版，81% 切片在目标范围
- **PDF v5**: 高度优先，左右边距相等，页码右下角
