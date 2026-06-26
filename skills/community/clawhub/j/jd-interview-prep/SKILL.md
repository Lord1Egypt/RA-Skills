---
name: interview-prep
displayName: JD + 简历 → 面试题预测助手
version: 1.0.0
description: >
  上传岗位描述（JD）和个人简历，AI 自动预测面试题（必问/针对性/追问三类），
  给出 STAR 答题框架，分析简历与 JD 匹配度，导出备考手册。
author: antonia-sz
tags: [interview, resume, job, career, ai, productivity]
---

# JD + 简历 → 面试题预测助手 🎯

## 你能做什么

上传岗位描述（JD）和个人简历，我帮你：

1. **预测面试题** — 分三类共 15 道，覆盖必问、针对、追问
2. **给出答题框架** — 每题配 STAR 结构思路 + 关键词提示
3. **评估匹配度** — 你的简历和 JD 有多契合，哪里是弱点
4. **生成备考手册** — 一键导出 Markdown，随时温习

---

## 使用方式

### 基本用法

直接粘贴 JD 和简历文本：

```
JD：
[粘贴岗位描述]

简历：
[粘贴简历内容]
```

### 文件上传

```
请分析我的面试准备，JD 文件：/path/to/jd.txt，简历：/path/to/resume.pdf
```

支持格式：`.txt` / `.md` / `.pdf` / `.docx`

---

## 输出格式

### 一、匹配度分析

```
📊 简历与 JD 匹配度：78%

✅ 优势匹配项（重点展示）
  - Python 5年经验 ↔ JD要求：Python 3年以上 ✓
  - 带过5人团队 ↔ JD要求：有团队管理经验 ✓

⚠️ 待补强项（重点准备）
  - JD 要求 Kubernetes 经验 → 简历未提及
  - JD 强调客户沟通能力 → 简历案例较少
```

### 二、面试题预测（15题）

#### 📌 必问题（5题）
> 岗位通用高频题，几乎必问

1. **请简单介绍一下你自己**
   - 答题要点：30秒版本 + 2分钟版本各准备一个
   - STAR框架：背景→核心技能→最大成就→为何适合这个岗位

#### 🎯 针对性题（5题）
> 根据你简历 vs JD 的 gap 生成，面试官大概率会追问的薄弱点

...

#### 🔍 追问题（5题）
> 针对简历中的亮点/可疑点，深挖细节

...

### 三、备考手册（导出）

运行导出命令后生成 `interview_prep_YYYY-MM-DD.md`，包含所有题目+答题框架。

---

## 工具调用

```python
# 解析文件（PDF/DOCX → 文本）
exec: python3 SKILL_DIR/scripts/parse_file.py "/path/to/file.pdf"

# 生成面试题报告
exec: python3 SKILL_DIR/scripts/generate_questions.py \
  --jd "JD文本或文件路径" \
  --resume "简历文本或文件路径" \
  --output "/tmp/interview_prep.md"
```

---

## 注意事项

- JD 和简历都可以粘贴纯文本，不需要特定格式
- PDF 解析需要 `pdfplumber`：`pip install pdfplumber`
- DOCX 解析需要 `python-docx`：`pip install python-docx`
- 没有安装时自动 fallback 到纯文本输入
