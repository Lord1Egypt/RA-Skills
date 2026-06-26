---
name: ppt-reader
description: |
  Use when user sends a PPT/PPTX file or asks to read PowerPoint content.
  适用于：读取PPT文件、解析演示文稿内容、提取幻灯片文本。
---

# PPT Reader

## Overview

读取和解析 PowerPoint 文件（.pptx），提取幻灯片文本内容。

## When to Use

- 用户发送了 .pptx 文件
- 需要提取PPT中的文字内容
- 需要了解PPT的结构和页数

## Quick Reference

| 操作 | 命令 |
|------|------|
| 查看PPT页数 | `unzip -l file.pptx \| grep "slide[0-9]*\.xml" \| wc -l` |
| 提取所有文本 | `unzip -p file.pptx "ppt/slides/slide*.xml" \| sed 's/<[^>]*>//g'` |
| 逐页提取 | 见下方脚本 |

## Implementation

### 方法1：快速提取所有文本

```bash
unzip -p "file.pptx" "ppt/slides/slide*.xml" 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n'
```

### 方法2：逐页提取（推荐）

```bash
cd /path/to/ppt/
for i in {1..N}; do 
  echo "=== Slide $i ===" 
  unzip -p "file.pptx" "ppt/slides/slide$i.xml" 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n'
  echo ""
done
```

### 方法3：获取PPT基本信息

```bash
# 页数
unzip -l "file.pptx" | grep -c "slide[0-9]*\.xml"

# 文件结构
unzip -l "file.pptx" | grep -E "slide[0-9]+\.xml"
```

## Workflow

1. **确认文件路径** - 从 `/root/.openclaw/media/inbound/` 获取文件
2. **获取页数** - 确定有多少张幻灯片
3. **逐页提取** - 循环提取每页内容
4. **整理输出** - 汇总成结构化摘要

## Common Patterns

### 处理飞书发送的PPT

飞书发送的文件通常保存在：
```
/root/.openclaw/media/inbound/
```

文件名格式：
```
原始文件名-uuid.pptx
```

### 提取特定幻灯片

```bash
# 只提取第1页
unzip -p "file.pptx" "ppt/slides/slide1.xml" | sed 's/<[^>]*>//g'

# 提取第1-5页
for i in {1..5}; do unzip -p "file.pptx" "ppt/slides/slide$i.xml" | sed 's/<[^>]*>//g'; done
```

## Limitations

- 只能提取文本内容，无法提取图片、图表
- 无法获取格式信息（字体、颜色、布局）
- 复杂表格可能提取不完整
- 仅支持 .pptx 格式（不支持旧版 .ppt）

## Real-World Example

```bash
# 完整提取流程
PPT_FILE="/root/.openclaw/media/inbound/智能体-概述-20260116-xxx.pptx"

# 1. 获取页数
PAGE_COUNT=$(unzip -l "$PPT_FILE" | grep -c "slide[0-9]*\.xml")
echo "Total slides: $PAGE_COUNT"

# 2. 逐页提取
for i in $(seq 1 $PAGE_COUNT); do
  echo "=== Slide $i ==="
  unzip -p "$PPT_FILE" "ppt/slides/slide$i.xml" 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n'
  echo ""
done
```
