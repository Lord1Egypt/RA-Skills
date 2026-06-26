#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 PDF Reader - PDF 阅读助手
功能：PDF 转 Markdown、摘要生成、重点提取、问答
"""

import json
import re
from pathlib import Path
from datetime import datetime

# 数据文件路径
DATA_DIR = Path(__file__).parent
HISTORY_FILE = DATA_DIR / "history.json"
OUTPUT_DIR = Path("D:/OneDrive/Desktop/公众号文章")  # 根据用户偏好设置

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"processed_files": []}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_text_from_pdf(pdf_path):
    """
    从 PDF 提取文本
    实际实现可用 PyMuPDF 或 pdfplumber
    这里用示例文本模拟
    """
    # TODO: 实现真实 PDF 解析
    # import fitz  # PyMuPDF
    # doc = fitz.open(pdf_path)
    # text = ""
    # for page in doc:
    #     text += page.get_text()
    
    # 示例文本（模拟）
    sample_text = """
# Attention Is All You Need

## Abstract

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...

## 1 Introduction

Recurrent neural networks, long short-term memory and gated recurrent neural networks have been firmly established as state of the art approaches in sequence modeling...

## 2 Background

The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU...

## 3 Model Architecture

Most competitive neural sequence transduction models have an encoder-decoder structure...

### 3.1 Encoder and Decoder Stacks

**Encoder**: The encoder is composed of a stack of N = 6 identical layers...

**Decoder**: The decoder is also composed of a stack of N = 6 identical layers...

### 3.2 Attention

An attention function can be described as mapping a query and a set of key-value pairs to an output...

**Scaled Dot-Product Attention**: We call our particular attention "Scaled Dot-Product Attention"...

**Multi-Head Attention**: Instead of performing a single attention function...

## 4 Why Self-Attention

In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers...

## 5 Training

This section describes the training regime for our models...

## 6 Results

We evaluated Transformer on the WMT 2014 English-German translation task...

## 7 Conclusion

In this work, we presented the Transformer, the first sequence transduction model based entirely on attention...
"""
    return sample_text.strip()


def pdf_to_markdown(text):
    """
    将 PDF 文本转换为 Markdown
    简单实现，可优化
    """
    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 识别标题（假设#开头的是标题）
    lines = text.split('\n')
    markdown_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            markdown_lines.append('')
            continue
        
        # 检测标题层级
        if line.startswith('#'):
            markdown_lines.append(line)
        elif line.startswith('##'):
            markdown_lines.append(line)
        elif len(line) < 100 and line[0].isupper() and line.endswith(':'):
            # 可能是小标题
            markdown_lines.append(f'### {line[:-1]}')
        else:
            markdown_lines.append(line)
    
    return '\n'.join(markdown_lines)


def generate_summary(text):
    """
    生成摘要
    简单提取前几段和关键句
    """
    paragraphs = text.split('\n\n')
    
    if len(paragraphs) < 3:
        return text[:500] + "..."
    
    # 提取标题
    title = paragraphs[0].strip()
    
    # 提取摘要（前 3 段）
    summary_parts = [title]
    for p in paragraphs[1:4]:
        if p.strip():
            summary_parts.append(p.strip())
    
    return '\n\n'.join(summary_parts)


def extract_key_points(text):
    """
    提取关键点
    简单实现：提取包含特定关键词的句子
    """
    key_phrases = [
        "we present", "we propose", "our model", "our contribution",
        "the main", "the key", "important", "significant",
        "conclusion", "result", "experiment", "achieve"
    ]
    
    sentences = re.split(r'[.!?]', text)
    key_points = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20 or len(sentence) > 300:
            continue
        
        for phrase in key_phrases:
            if phrase.lower() in sentence.lower():
                key_points.append(sentence + ".")
                break
    
    return key_points[:10]  # 最多 10 个关键点


def answer_question(text, question):
    """
    基于文本问答
    简单关键词匹配，实际可用 RAG
    """
    question_lower = question.lower()
    
    # 简单关键词匹配
    paragraphs = text.split('\n\n')
    relevant = []
    
    for p in paragraphs:
        score = 0
        p_lower = p.lower()
        
        # 统计问题词在段落中出现次数
        for word in question_lower.split():
            if len(word) > 3 and word in p_lower:
                score += 1
        
        if score > 0:
            relevant.append((score, p))
    
    # 按相关性排序
    relevant.sort(reverse=True, key=lambda x: x[0])
    
    if relevant:
        return f"""基于文档内容，关于"{question}"的回答：

{relevant[0][1][:500]}..."""
    
    return "抱歉，文档中没有找到相关信息。"


def process_pdf(pdf_path):
    """处理 PDF 文件"""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        return {"error": f"文件不存在：{pdf_path}"}
    
    # 提取文本
    text = extract_text_from_pdf(pdf_path)
    
    # 转换为 Markdown
    markdown = pdf_to_markdown(text)
    
    # 生成输出文件名
    output_md = OUTPUT_DIR / f"{pdf_path.stem}.md"
    
    # 保存 Markdown
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    # 生成摘要
    summary = generate_summary(text)
    
    # 提取关键点
    key_points = extract_key_points(text)
    
    # 记录历史
    history = load_json(HISTORY_FILE)
    history["processed_files"].append({
        "filename": pdf_path.name,
        "processed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pages": text.count('\n\n'),  # 估算页数
        "output_md": str(output_md),
        "word_count": len(text.split())
    })
    save_json(HISTORY_FILE, history)
    
    return {
        "success": True,
        "filename": pdf_path.name,
        "output_md": str(output_md),
        "summary": summary,
        "key_points": key_points,
        "full_text": markdown
    }


def main(query):
    """主函数"""
    query = query.strip()
    
    # 检测是否是文件路径
    if query.endswith('.pdf') or query.startswith('D:') or query.startswith('C:'):
        result = process_pdf(query)
        
        if result.get("error"):
            return f"❌ {result['error']}"
        
        response = f"""✅ PDF 处理完成！

📄 文件名：{result['filename']}
📁 输出：{result['output_md']}
📊 字数：{result['word_count']}

📌 **摘要**：
{result['summary'][:500]}...

🔑 **关键点**：
"""
        for i, point in enumerate(result['key_points'][:5], 1):
            response += f"{i}. {point}\n"
        
        response += """
💡 你可以继续问我：
- "提取全文"
- "生成摘要"
- "提取重点"
- "XXX 讲了什么？"（问答）"""
        
        return response
    
    # 问答
    if "什么" in query or "为什么" in query or "如何" in query:
        # 假设已有处理的文本（实际应从历史加载）
        return f"""🔍 基于最近处理的文档：

{query} 的答案是...

（需要实际 PDF 内容才能准确回答）"""
    
    # 默认回复
    return """📄 PDF 阅读助手

**使用方法**：
1. 直接发送 PDF 文件路径
2. 或上传文件后说"处理这个 PDF"

**功能**：
- 📝 PDF 转 Markdown
- 📌 自动生成摘要
- 🔑 提取关键点
- ❓ 基于内容问答

**示例**：
- "D:/docs/paper.pdf"
- "处理这个 PDF"
- "这篇论文讲了什么？"
- "提取重点"

发送 PDF 文件路径开始！👻"""


if __name__ == "__main__":
    # 测试
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("D:/test.pdf"))
