---
name: homework-grader
description: 老师作业批改助手，用于自动批改数学作业、统计错题、生成Excel统计表和PDF报告。当老师需要：(1) 上传正确答案并让AI识别 (2) 批量上传学生作业照片进行批改 (3) 统计全班错误率并生成错题分析报告 (4) 生成重点错题PDF供讲解使用时，触发此skill。
---

# Homework Grader - 作业批改助手

## Overview

帮助老师自动批改数学作业，统计错题信息，生成 Excel 统计表和 PDF 分析报告。

## 依赖安装

运行此 skill 前需要安装以下依赖：

### Python 包
```bash
pip install -r scripts/requirements.txt
```

### 系统依赖（必须安装）
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract

# Windows
# 下载安装：https://github.com/UB-Mannheim/tesseract/wiki
```

## Workflow

### 完整工作流程

```
Step 1: 上传正确答案 → AI OCR 识别
    ↓
Step 2: 循环上传学生作业 → AI 批改 → 记录结果
    ↓
Step 3: 统计错误率 → 生成 Excel 统计表
    ↓
Step 4: 生成 PDF 报告（含重点标记）
```

---

## Step 1: 上传正确答案

老师上传包含正确答案的图片（可以是纸质答案照片或电子版截图）。

**AI 行为：**
1. 使用 OCR 识别图片中的答案
2. 解析答案内容，按题目编号存储
3. 向老师确认识别结果是否正确
4. 如需修改，允许老师手动调整

---

## Step 2: 上传学生作业

循环上传学生作业照片。

**交互流程：**
1. 询问老师"请上传学生作业照片"
2. 提供学生姓名输入框（可选填写）
3. 如果不填姓名，使用序号标识（如：学生1、学生2）
4. 重复步骤1-3，直到老师说"上传完成"

**AI 行为：**
1. OCR 识别学生作业内容
2. 与正确答案比对
3. 标记正确/错误
4. 记录错误类型

---

## Step 3: 生成 Excel 统计表

当老师说"生成统计表"或"上传完成"时：

**输出 Excel 包含：**
- 学生姓名/序号
- 各题对错情况
- 正确题数、错误题数
- 错误率百分比

---

## Step 4: 生成 PDF 报告

当老师说"生成 PDF"或"生成报告"时：

**PDF 内容：**
1. 班级概况 - 总人数、提交人数、平均正确率
2. 错题统计表 - 每道题的错题人数、错误率
3. 重点错题 - 错误率 ≥ 配置阈值的题目（默认40%）
4. 讲解建议 - AI 针对重点错题提供的解题思路和讲解要点

---

## 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| threshold | 重点错题错误率阈值 | 40% |

**修改阈值：** 老师可以说"设置阈值为 30%"来调整

---

## Resources

### scripts/requirements.txt
Python 依赖包列表

### scripts/
- `ocr_helper.py` - OCR 识别辅助工具
- `generate_excel.py` - 生成 Excel 统计表
- `generate_pdf.py` - 生成 PDF 分析报告

### references/
- `answer_format.md` - 答案格式规范
- `output_format.md` - 输出格式说明

### assets/
- `report_template.html` - PDF 报告 HTML 模板