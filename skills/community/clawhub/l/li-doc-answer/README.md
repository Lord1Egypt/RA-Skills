# Li_doc_answer 使用说明

## 简介

**Li_doc_answer** 是一款**通用 Word 文档处理工具**，支持任意 doc/docx 格式文档的批量处理、转换和 AI 答案生成。

> ⚠️ **注意：** 本技能不局限于特定主题或学科，可处理任何 Word 文档（教育题库、办公文档、报告等）

## 🎯 v3.0 核心功能：AI 智能答案生成

**输入：** 任意 doc/docx 文档（含题目）  
**处理：** 自动识别所有题目 + AI 生成参考答案  
**输出：** 带完整答案的文档

### 使用示例

```bash
# AI 自动答案生成
python3 scripts/ai_generate_answers.py 题库.doc

# 输出：题库_AI 答案版.docx
# 包含：所有题目 + 每道题的参考答案
```

### 支持的题型

| 题型 | 识别 | 答案模板 |
|------|------|----------|
| 判断题 | ✅ | 正确/错误 + 理由 |
| 单选题 | ✅ | 正确选项 + 解析 |
| 多选题 | ✅ | 正确选项 + 解析 |
| 简答题 | ✅ | 要点 1/2/3 + 说明 |
| 论述题 | ✅ | 引言/主体/结论 |
| 案例分析 | ✅ | 问题/理论/方案/总结 |
| 填空题 | ✅ | 正确答案 |
| 名词解释 | ✅ | 定义 + 特点 + 意义 |

## 适用场景

- 📚 教育/培训题库文档处理（任意学科）
- 📄 企业办公文档批量转换
- 📝 文档内容整理与归档
- 🔄 doc ↔ docx 格式统一化
- 📋 文档答案/备注批量添加

## 快速开始

### 1. 安装依赖

```bash
pip3 install python-docx mammoth
```

### 2. 安装技能

```bash
clawhub install li-doc-answer
```

### 3. 使用示例

#### AI 答案生成（v3.0 核心功能）

```bash
python3 scripts/ai_generate_answers.py /path/to/题库.doc
```

#### 处理单个文档

```bash
python3 scripts/generate_answers.py /path/to/document.doc
```

#### 批量处理目录

```bash
# 将待处理文件放入 data 目录
python3 scripts/generate_all_answers.py
```

#### 格式转换

```bash
python3 scripts/convert_md_to_docx.py input.md output.docx
```

#### 文档校验

```bash
python3 scripts/check_answers.py document.docx
```

## 支持的文档类型

| 类型 | 支持 | 说明 |
|------|------|------|
| .doc | ✅ | 旧版 Word 文档（需 antiword） |
| .docx | ✅ | 新版 Word 文档 |
| .md | ✅ | Markdown 转 Word |

## 支持的内容类型

本技能**不限制文档内容主题**，可处理：

- ✅ 任意学课题库（数学、英语、物理、化学、历史等）
- ✅ 单项选择题
- ✅ 判断题
- ✅ 简答题
- ✅ 案例分析题
- ✅ 论述题
- ✅ 任意办公文档

## 命令行参数

### ai_generate_answers.py（AI 核心功能）

```bash
python3 scripts/ai_generate_answers.py <输入文件> [输出文件]
```

- `输入文件` - 必填，待处理的 doc/docx 文件路径
- `输出文件` - 可选，默认输出为 `输入文件_AI 答案版.docx`

### generate_answers.py

```bash
python3 scripts/generate_answers.py <输入文件> [输出文件]
```

- `输入文件` - 必填，待处理的 doc/docx 文件路径
- `输出文件` - 可选，默认输出为 `输入文件_处理版.docx`

### generate_all_answers.py

```bash
python3 scripts/generate_all_answers.py [目录路径]
```

- `目录路径` - 可选，默认为 `data/` 目录

## 输出说明

处理后的文档将：

1. 保留原文档所有内容
2. 自动识别所有题目
3. 为每题生成参考答案
4. 统一格式排版
5. 保存为 .docx 格式

## 常见问题

**Q: 只能处理特定学科文档吗？**  
A: 不是！v3.0+ 是通用文档处理工具，可处理任意学科、任意主题的文档。

**Q: 支持 Mac/Windows 吗？**  
A: 支持，使用相对路径，可跨平台部署。

**Q: 会泄露我的文档内容吗？**  
A: 不会，所有操作均在本地完成，无网络请求。

**Q: AI 生成的答案准确吗？**  
A: AI 生成的答案仅供参考，请以教材和教师讲解为准。

## 作者

**北京老李**

## 版本

3.0.1 (2026 年 3 月)

## 许可证

MIT

## 其他语言

- [English](README_EN.md) - English version

---

## ⚠️ 重要说明

**AI 生成的答案仅供参考**，请以教材和教师讲解为准。

**参考答案来源：** 基于通用知识库生成，具体内容请根据相关教材完善。
