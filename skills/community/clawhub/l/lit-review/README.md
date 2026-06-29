# 📚 文献智能检索与综述生成器

自动检索学术文献（Semantic Scholar / arXiv / CrossRef），进行相关性筛选、主题聚类分析，并生成结构化综述草稿。

## ✨ 功能特点

- **多源检索**: 支持 Semantic Scholar、arXiv、CrossRef 三大数据库
- **智能筛选**: 基于TF-IDF相似度 + 引用数加权筛选
- **主题聚类**: 自动识别研究热点方向（支持BERTopic深度聚类）
- **趋势分析**: 年度发文量、热门期刊统计
- **零API费用**: 本地处理模式，无需大模型API
- **结构化输出**: 自动生成标准综述格式

## 🚀 快速开始

### 命令行使用

```bash
# 基础用法
python lit_review.py "联邦学习在工业视觉中的应用"

# 指定时间范围和文献数
python lit_review.py "大模型微调技术" --years 3 --max-papers 30

# 保存到文件
python lit_review.py "柔性机器人" --output review.md
```

### 代码调用

```python
from lit_review import LiteratureReviewer

reviewer = LiteratureReviewer({
    "default_years": 3,
    "max_papers": 50,
    "output_format": "markdown"
})

review = reviewer.run("深度学习在图像识别中的应用", "output.md")
print(review)
```

## 📋 配置说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `default_years` | 5 | 检索最近多少年的文献 |
| `max_papers` | 50 | 最终保留的文献数量 |
| `use_llm_for_writing` | false | 是否使用大模型润色 |
| `llm_model` | deepseek-chat | 大模型名称 |
| `human_review_papers` | false | 是否需要人工确认文献列表 |

## 🔧 安装依赖

```bash
# 基础依赖（必需）
pip install requests

# 进阶功能（可选）
pip install scikit-learn numpy
pip install sentence-transformers bertopic  # 深度主题聚类
pip install python-docx  # DOCX格式输出
```

## 📝 输出示例

生成的综述包含以下部分：
1. **摘要** - 研究领域概况
2. **主要研究方向** - 按主题分类的论文列表
3. **研究趋势与挑战** - 年度趋势、热门期刊、未来方向
4. **参考文献** - 完整的引用列表

## ⚡ 触发关键词

在OpenClaw中使用以下关键词触发此技能：
- "文献综述"
- "检索文献"
- "写一篇综述"
- "研究热点"
- "论文检索"

## 📊 示例输出

```markdown
# 联邦学习在工业视觉中的应用 研究文献综述

生成时间: 2026-04-27 14:30:00
检索范围: 近5年文献（2021-2026）
文献数量: 42篇

## 1. 摘要
本文基于42篇学术文献，对"联邦学习在工业视觉中的应用"领域的
研究进展进行了系统性综述。通过文献计量分析，共识别出6个主要
研究方向...
```
