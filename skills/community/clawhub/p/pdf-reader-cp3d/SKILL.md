---
name: pdf-reader-cp3d
version: 1.0.0
description: PDF 阅读助手 - PDF 转 Markdown、智能摘要、重点提取
---

# 📄 PDF Reader - PDF 阅读助手

## 触发规则

**关键词：**
- 读 PDF、PDF 转 markdown、PDF 摘要
- 提取重点、总结 PDF
- 这个 PDF 讲了什么
- 转换 PDF、解析 PDF

**场景：**
- 用户上传 PDF 文件
- 用户需要 PDF 内容摘要
- 用户想提取 PDF 重点
- 用户需要 PDF 转其他格式

## 功能描述

### 核心功能

1. **PDF 内容提取**
   - 提取纯文本
   - 保留标题结构
   - 提取表格
   - 提取图片（可选）

2. **PDF 转 Markdown**
   - 自动识别标题层级
   - 转换列表、代码块
   - 转换表格为 markdown 表格
   - 保留引用格式

3. **智能摘要**
   - 提取核心观点
   - 生成内容大纲
   - 提取关键数据
   - 生成一句话总结

4. **重点提取**
   - 高亮关键句子
   - 提取定义/概念
   - 提取结论/建议
   - 提取数据/图表说明

5. **问答功能**
   - 基于 PDF 内容问答
   - "这篇论文的主要贡献是什么？"
   - "第三章讲了什么？"
   - "作者的观点是什么？"

### 支持的 PDF 类型

- 📄 学术论文（arXiv、期刊）
- 📚 电子书
- 📊 报告/白皮书
- 📝 文档/手册
- 📋 表格/表单

### 输出格式

- Markdown (.md)
- 纯文本 (.txt)
- HTML (.html)
- JSON (结构化数据)

## 权限需求

- [x] 文件读写（PDF 处理）
- [x] 网络访问（可选：在线 API）
- [ ] 外部 API（可选：PDF 解析服务）

## 技术实现

### 方案 1：本地处理（推荐）

```python
# Python 库
- PyMuPDF (fitz) - 快速提取
- pdfplumber - 表格提取
- pymupdf4llm - PDF 转 Markdown
```

### 方案 2：在线 API

- Adobe PDF Extract API
- Amazon Textract
- Google Document AI

## 示例对话

```
用户：[上传文件：research_paper.pdf]
助手：收到 PDF 文件！📄
- 文件名：research_paper.pdf
- 页数：12 页
- 大小：2.3 MB

需要我帮你做什么？
1. 提取全文
2. 生成摘要
3. 转 Markdown
4. 提取重点
5. 基于内容问答

用户：生成摘要
助手：【PDF 摘要】research_paper.pdf

📌 标题：Attention Is All You Need

👥 作者：Ashish Vaswani et al. (Google Brain)

📅 日期：2017

🎯 核心贡献：
1. 提出 Transformer 架构，完全基于注意力机制
2. 摒弃 RNN/CNN 的序列处理，实现并行化
3. 在翻译任务上达到 SOTA

📋 主要方法：
- Self-Attention 机制
- Multi-Head Attention
- Positional Encoding

📊 实验结果：
- WMT 2014 英德翻译：28.4 BLEU
- WMT 2014 英法翻译：41.0 BLEU
- 训练成本降低

💡 结论：
Transformer 为 NLP 领域带来革命性突破，
后续 BERT、GPT 等均基于此架构。

用户：转 Markdown
助手：✅ 已转换并保存：
📁 D:\OneDrive\Desktop\公众号文章\research_paper.md

用户：这篇论文的主要创新点是什么？
助手：基于 PDF 内容，主要创新点：

1. **完全摒弃 RNN/CNN**
   传统序列模型需要按顺序处理，Transformer 实现完全并行

2. **Self-Attention 机制**
   让模型直接关注序列中任意位置的信息

3. **Multi-Head Attention**
   多个注意力头同时工作，捕捉不同维度的关系

4. **Positional Encoding**
   用位置编码替代序列顺序，保留位置信息

5. **训练效率提升**
   相比 RNN 训练速度提升数倍
```

## 数据存储

```json
// ~/.openclaw/workspace/pdf-reader/history.json
{
  "processed_files": [
    {
      "filename": "research_paper.pdf",
      "processed_date": "2026-03-16",
      "pages": 12,
      "output_md": "D:\\...\\research_paper.md",
      "summary": "Attention Is All You Need..."
    }
  ]
}
```

## 待办事项

- [ ] 实现 PDF 文本提取
- [ ] 实现 PDF 转 Markdown
- [ ] 实现智能摘要
- [ ] 实现问答功能
- [ ] 添加批量处理

---

**版本：** 1.0.0
**创建日期：** 2026-03-16
**作者：** 小鬼 👻
