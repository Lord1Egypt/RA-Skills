# 新闻摘要生成方法详解

## 概述

本文档详细介绍新闻摘要生成的两种主要方法:提取式摘要和生成式摘要,包括技术原理、实现代码和适用场景。

## 1. 提取式摘要 (Extractive Summarization)

### 原理

提取式摘要从原文中提取最重要的句子或段落,组合成摘要。核心思想是:
1. 将原文分割成句子
2. 计算每个句子的重要性得分
3. 选择得分最高的 N 个句子作为摘要

### 优点
- 实现简单,计算效率高
- 摘要完全基于原文,不会产生虚假信息
- 不需要训练模型

### 缺点
- 摘要可能不够连贯
- 可能包含冗余信息
- 摘要长度受原文句子长度限制

### 实现方法

#### 方法 1: 基于 TextRank 算法

TextRank 是基于图排序算法的文本摘要方法。

```python
import jieba
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

def textrank_summarize(text, num_sentences=3):
    """
    使用 TextRank 算法生成提取式摘要

    Args:
        text: 原文文本
        num_sentences: 摘要句子数

    Returns:
        摘要文本
    """
    # 分句
    sentences = [s.strip() for s in text.split('。') if s.strip()]

    # 分词
    words_list = []
    for sent in sentences:
        words = jieba.lcut(sent)
        words_list.append(' '.join(words))

    # TF-IDF 向量化
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(words_list)

    # 构建相似度矩阵
    similarity_matrix = tfidf_matrix * tfidf_matrix.T

    # 构建 PageRank 图
    nx_graph = nx.from_scipy_sparse_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)

    # 选择得分最高的句子
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    summary = '。'.join([s for score, s in ranked_sentences[:num_sentences]]) + '。'
    return summary
```

#### 方法 2: 基于关键词提取

```python
import jieba.analyse
import re

def keyword_based_summarize(text, num_sentences=3):
    """
    基于关键词提取生成摘要

    Args:
        text: 原文文本
        num_sentences: 摘要句子数

    Returns:
        摘要文本
    """
    # 提取关键词
    keywords = jieba.analyse.extract_tags(text, topK=10, withWeight=True)

    # 分句
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 计算每个句子的得分
    sentence_scores = []
    keyword_set = set([kw[0] for kw in keywords])

    for sentence in sentences:
        score = 0
        # 包含关键词的句子得分更高
        for keyword, weight in keywords:
            if keyword in sentence:
                score += weight * 10
        # 句子长度适中得分更高
        if 20 <= len(sentence) <= 100:
            score += 5
        sentence_scores.append((sentence, score))

    # 按得分排序
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    selected_sentences = [s[0] for s in sentence_scores[:num_sentences]]

    return '。'.join(selected_sentences) + '。'
```

### 适用场景
- 快速浏览大量新闻
- 实时监控系统
- 资源受限的环境
- 需要准确性的场景

## 2. 生成式摘要 (Abstractive Summarization)

### 原理

生成式摘要使用深度学习模型,理解原文内容并生成新的句子作为摘要。核心思想是:
1. 将原文编码为向量表示
2. 使用解码器生成摘要
3. 摘要是新生成的句子,不一定在原文中出现

### 优点
- 摘要更连贯、更自然
- 可以压缩信息,去除冗余
- 可以生成比原文更短的摘要

### 缺点
- 计算资源需求高
- 可能产生虚假信息(幻觉)
- 需要训练好的模型

### 实现方法

#### 方法 1: 使用 HuggingFace Transformers 库

```python
from transformers import pipeline

def abstractive_summarize(text, model="google/mt5-small-chinese", max_length=150):
    """
    使用预训练模型生成生成式摘要

    Args:
        text: 原文文本
        model: 模型名称
        max_length: 摘要最大长度

    Returns:
        摘要文本
    """
    # 初始化摘要管道
    summarizer = pipeline("summarization", model=model, device=-1)

    # 生成摘要
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=30,
        do_sample=False
    )

    return summary[0]['summary_text']
```

#### 推荐的中文摘要模型

1. **google/mt5-small-chinese**
   - 基于 mT5 模型
   - 支持中文摘要
   - 轻量级,推理速度快

2. **csebuetnlp/mT5_multilingual_XLSum**
   - 多语言摘要模型
   - 支持中文
   - 在 XLSum 数据集上训练

3. **Helsinki-NLP/opus-mt-zh-en**
   - 中英翻译模型
   - 可用于跨语言摘要

#### 使用示例

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_summarizer(model_name):
    """
    加载摘要模型和分词器

    Args:
        model_name: 模型名称或路径

    Returns:
        tokenizer, model
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def generate_summary(tokenizer, model, text, max_length=150):
    """
    生成摘要

    Args:
        tokenizer: 分词器
        model: 模型
        text: 原文文本
        max_length: 摘要最大长度

    Returns:
        摘要文本
    """
    # 分词
    inputs = tokenizer(text, max_length=512, truncation=True, return_tensors="pt")

    # 生成摘要
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # 解码
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# 使用示例
tokenizer, model = load_summarizer("google/mt5-small-chinese")
text = "这是一段长新闻文本..."
summary = generate_summary(tokenizer, model, text)
print(summary)
```

### 适用场景
- 生成高质量的新闻摘要
- 需要自然语言的场景
- 深度分析报告
- 用户界面展示

## 3. 混合方法 (Hybrid Summarization)

结合提取式和生成式摘要的优点:

```python
def hybrid_summarize(text):
    """
    混合摘要方法:先用提取式筛选重要句子,再用生成式改写

    Args:
        text: 原文文本

    Returns:
        摘要文本
    """
    # 第一步:提取式摘要获取关键句子
    key_sentences = keyword_based_summarize(text, num_sentences=5)

    # 第二步:生成式摘要改写
    summary = abstractive_summarize(key_sentences, max_length=150)

    return summary
```

## 4. 评估方法

### ROUGE 指标

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) 是常用的摘要评估指标。

```python
from rouge import Rouge

def evaluate_summary(generated_summary, reference_summary):
    """
    使用 ROUGE 指标评估摘要质量

    Args:
        generated_summary: 生成的摘要
        reference_summary: 参考摘要

    Returns:
        ROUGE 分数
    """
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summary)
    return scores
```

### 人工评估
- 信息完整性
- 准确性
- 可读性
- 连贯性

## 5. 性能优化

### 批量处理

```python
def batch_summarize(texts, batch_size=8):
    """
    批量生成摘要

    Args:
        texts: 文本列表
        batch_size: 批次大小

    Returns:
        摘要列表
    """
    summaries = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # 使用 GPU 加速
        batch_summaries = [summarize(text) for text in batch]
        summaries.extend(batch_summaries)
    return summaries
```

### 缓存机制

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_summarize(text):
    """
    带缓存的摘要生成

    Args:
        text: 原文文本

    Returns:
        摘要文本
    """
    return abstractive_summarize(text)
```

## 6. 实际应用建议

### 选择依据

| 场景 | 推荐方法 | 原因 |
|------|---------|------|
| 实时监控 | 提取式 | 速度快,资源消耗低 |
| 深度分析 | 生成式 | 质量高,连贯性好 |
| 大规模处理 | 提取式 | 效率高,可批量处理 |
| 用户展示 | 生成式 | 自然度高,体验好 |
| 准确性优先 | 提取式 | 基于原文,无幻觉 |

### 参数调优

1. **摘要长度**
   - 新闻摘要: 100-150 字
   - 快速浏览: 50-80 字
   - 深度分析: 200-300 字

2. **模型选择**
   - 轻量级: mT5-small
   - 高质量: mT5-base, BART
   - 特定领域: 微调模型

3. **后处理**
   - 去除重复句子
   - 修正语法错误
   - 调整句子顺序

## 7. 常见问题

### Q: 提取式摘要不够连贯怎么办?
A: 可以使用句子重排序或使用生成式摘要改写提取的句子。

### Q: 生成式摘要产生虚假信息怎么办?
A: 可以:
- 使用事实一致性检查
- 限制摘要长度
- 添加源文档作为输入
- 使用校验模型

### Q: 如何提高摘要质量?
A: 可以:
- 使用更大的模型
- 在特定领域数据上微调
- 结合提取式和生成式
- 优化超参数

### Q: 如何处理长文档?
A: 可以:
- 分段摘要
- 层次化摘要
- 先提取关键段落再摘要
