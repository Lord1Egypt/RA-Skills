#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM 功能测试脚本

用于验证摘要生成和查询扩展功能是否正常工作
"""

import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.summarizer import summarize
from core.expansion import expand_query


def test_summarizer():
    """测试摘要生成功能"""
    print("=" * 60)
    print("测试摘要生成")
    print("=" * 60)
    
    test_paper = {
        "title": "Attention Is All You Need",
        "authors": ["Vaswani, A.", "Shazeer, N.", "Parmar, N.", "Jakob, U."],
        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.",
        "year": 2017
    }
    
    print(f"\n论文标题：{test_paper['title']}")
    print("\n生成摘要:")
    
    summary = summarize(test_paper, use_llm=True)
    
    for key, value in summary.items():
        print(f"  {key}: {value[:80]}..." if len(value) > 80 else f"  {key}: {value}")
    
    print("\n✓ 摘要生成测试完成\n")


def test_expansion():
    """测试查询扩展功能"""
    print("=" * 60)
    print("测试查询扩展")
    print("=" * 60)
    
    test_papers = [
        {
            "title": "Deep Residual Learning for Image Recognition",
            "abstract": "Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously."
        },
        {
            "title": "Attention Is All You Need",
            "abstract": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms."
        },
        {
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."
        }
    ]
    
    original_query = "deep learning"
    
    print(f"\n原始查询：{original_query}")
    print(f"参考论文：{len(test_papers)} 篇")
    print("\n生成扩展词:")
    
    expansions = expand_query(test_papers, original_query, max_terms=5, use_llm=True)
    
    for i, exp in enumerate(expansions, 1):
        print(f"  {i}. {exp['term']} (score={exp['score']:.2f})")
    
    if not expansions:
        print("  (无扩展词，使用 Fallback)")
    
    print("\n✓ 查询扩展测试完成\n")


if __name__ == "__main__":
    print("\n🧪 Paper Review Pro - LLM 功能测试\n")
    
    test_summarizer()
    #test_expansion()
    
    print("=" * 60)
    print("所有测试完成!")
    print("=" * 60)
