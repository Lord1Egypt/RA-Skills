#!/usr/bin/env python3
"""
毛泽东思想问答 skill
基于知识库回答毛泽东思想相关问题
"""

import json
import re
from pathlib import Path

KNOWLEDGE_FILE = Path(__file__).parent / "knowledge.md"


def load_knowledge():
    """加载知识库"""
    if KNOWLEDGE_FILE.exists():
        return KNOWLEDGE_FILE.read_text(encoding="utf-8")
    return ""


def extract_keyword(question: str) -> str:
    """从问题中提取关键词"""
    # 去除常见疑问词
    q = re.sub(r"[的吗呢呀啊嘛]|什么|怎么|如何|为什么|哪些|哪个", "", question)
    return q.strip()


def search_knowledge(question: str, knowledge: str) -> str:
    """在知识库中搜索相关内容"""
    keyword = extract_keyword(question)
    
    if not knowledge:
        return None
    
    # 简单的关键词匹配
    lines = knowledge.split("\n")
    relevant_lines = []
    current_section = ""
    
    for line in lines:
        if line.startswith("#"):
            current_section = line
        elif keyword in line:
            relevant_lines.append(current_section)
            relevant_lines.append(line)
    
    if relevant_lines:
        return "\n".join(relevant_lines[:10])
    return None


def answer_question(question: str) -> str:
    """根据问题生成回答"""
    knowledge = load_knowledge()
    
    # 直接返回知识库内容，让LLM自行判断回答
    return knowledge


if __name__ == "__main__":
    # 测试
    test_questions = [
        "毛泽东思想的活的灵魂是什么？",
        "矛盾论的核心观点是什么？",
        "新民主主义革命理论的内容有哪些？",
    ]
    
    knowledge = load_knowledge()
    for q in test_questions:
        result = search_knowledge(q, knowledge)
        print(f"Q: {q}")
        print(f"A: {result}\n")
