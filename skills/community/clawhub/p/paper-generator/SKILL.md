# paper-generator

version: 0.1.0

一个用于自动生成学术论文的 OpenClaw Skill，支持从实验代码生成完整的学术论文（中英文），包括摘要、引言、方法、实验、讨论和结论等章节。

## 功能

- 自动生成完整学术论文结构
- 支持中英文论文生成
- 自动转换为 PDF 格式
- 支持多种 LaTeX 模板

## 用法

```bash
# 生成英文论文
paper-gen --template=icml --output=paper.md

# 生成中文论文
paper-gen --template=icml --lang=zh --output=paper_cn.md

# 转换为 PDF
paper-to-pdf paper.md paper.pdf
```

## 安装

```bash
clawhub install paper-generator
```
