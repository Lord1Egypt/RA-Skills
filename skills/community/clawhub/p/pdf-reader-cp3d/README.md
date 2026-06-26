# 📄 PDF Reader - PDF 阅读助手

## 📖 功能说明

PDF 转 Markdown、摘要生成、重点提取、基于内容问答。

## 🚀 使用方法

### 在 OpenClaw 中使用

```
D:/docs/paper.pdf
处理这个 PDF
提取重点
这篇论文讲了什么？
```

### Python 脚本调用

```python
from pdf_reader import process_pdf

# 处理 PDF
result = process_pdf("D:/docs/paper.pdf")
print(result["summary"])
print(result["key_points"])
```

## 📁 文件结构

```
pdf-reader/
├── SKILL.md              # 技能描述
├── pdf_reader.py         # 主程序
└── history.json          # 处理历史（自动生成）
```

## 🔧 依赖安装

```bash
# 安装 PDF 解析库
pip install PyMuPDF pdfplumber pymupdf4llm
```

## 📊 示例输出

```
✅ PDF 处理完成！

📄 文件名：attention_is_all_you_need.pdf
📁 输出：D:/OneDrive/Desktop/公众号文章/attention_is_all_you_need.md
📊 字数：8500

📌 **摘要**：
# Attention Is All You Need

## Abstract
The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...

🔑 **关键点**：
1. We present the Transformer, the first sequence transduction model based entirely on attention.
2. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task.
3. The Transformer allows for significantly more parallelization.
```

## 🛠️ 开发计划

- [x] PDF 文本提取
- [x] Markdown 转换
- [x] 摘要生成
- [ ] 真实 PDF 解析（PyMuPDF）
- [ ] 表格提取
- [ ] RAG 问答

## 📝 更新日志

### v1.0.0 (2026-03-16)
- 🎉 初始版本

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
