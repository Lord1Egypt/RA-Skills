---
name: nlp-text-analyzer
description: NLP文本分析器 - 支持分词、情感分析、关键词提取、文本分类等自然语言处理功能 | NLP Text Analyzer - Tokenization, sentiment analysis, keyword extraction, text classification
homepage: https://github.com/kaiyuelv/nlp-text-analyzer
category: nlp
tags:
  - nlp
  - text-analysis
  - sentiment
  - tokenization
  - chinese
  - jieba
  - textblob
version: 1.0.0
---

# NLP文本分析器

强大的自然语言处理工具，支持中文和英文文本分析，包含分词、情感分析、关键词提取等功能。

## 概述

本Skill提供完整的NLP文本分析能力：
- 中文分词（Jieba分词）
- 情感分析（SnowNLP / TextBlob）
- 关键词提取
- 文本摘要生成
- 词频统计
- 命名实体识别
- 文本分类基础
- 相似度计算
- 中英双语支持

## 依赖

- Python >= 3.8
- jieba >= 0.42.1
- snownlp >= 0.12.3
- textblob >= 0.17.1

## 文件结构

```
nlp-text-analyzer/
├── SKILL.md                  # 本文件
├── README.md                 # 使用文档
├── requirements.txt          # 依赖声明
├── scripts/
│   └── text_analyzer.py      # 文本分析脚本
├── examples/
│   └── basic_usage.py        # 使用示例
└── tests/
    └── test_nlp.py           # 单元测试
```

## 快速开始

```python
from scripts.text_analyzer import TextAnalyzer

# 初始化分析器
analyzer = TextAnalyzer()

# 中文分词
text = "自然语言处理是人工智能的重要分支"
tokens = analyzer.segment(text)
print(tokens)
# ['自然语言', '处理', '是', '人工智能', '的', '重要', '分支']

# 情感分析
sentiment = analyzer.analyze_sentiment("这个产品真的很棒！")
print(sentiment)
# {'polarity': 0.95, 'subjectivity': 0.8}

# 关键词提取
keywords = analyzer.extract_keywords(text, top_k=5)
print(keywords)
# [('人工智能', 1.5), ('自然语言', 1.2), ...]
```

## 许可证

MIT

---

# NLP Text Analyzer

Powerful NLP tool supporting Chinese and English text analysis, including tokenization, sentiment analysis, keyword extraction.

## Overview

This Skill provides complete NLP text analysis capabilities:
- Chinese tokenization (Jieba)
- Sentiment analysis (SnowNLP / TextBlob)
- Keyword extraction
- Text summarization
- Word frequency statistics
- Named entity recognition
- Text classification basics
- Similarity calculation
- Chinese/English bilingual support

## Dependencies

- Python >= 3.8
- jieba >= 0.42.1
- snownlp >= 0.12.3
- textblob >= 0.17.1

## File Structure

```
nlp-text-analyzer/
├── SKILL.md                  # This file
├── README.md                 # Usage documentation
├── requirements.txt          # Dependencies
├── scripts/
│   └── text_analyzer.py      # Text analysis script
├── examples/
│   └── basic_usage.py        # Usage examples
└── tests/
    └── test_nlp.py           # Unit tests
```

## Quick Start

```python
from scripts.text_analyzer import TextAnalyzer

# Initialize analyzer
analyzer = TextAnalyzer()

# Chinese tokenization
text = "Natural language processing is an important AI branch"
tokens = analyzer.segment(text)
print(tokens)

# Sentiment analysis
sentiment = analyzer.analyze_sentiment("This product is really amazing!")
print(sentiment)
# {'polarity': 0.95, 'subjectivity': 0.8}

# Keyword extraction
keywords = analyzer.extract_keywords(text, top_k=5)
print(keywords)
```

## License

MIT
