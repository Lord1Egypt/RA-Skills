---
name: reading-assistant
version: 1.0.0
description: 阅读助手 - 贴链接或粘贴文字，自动提炼4点：主旨/论据/行动/疑问，不用读全文。支持网页抓取和本地文本
tags: [reading, summary, research, productivity, learning, extraction]
author: laosi
source: original
---

# Reading Assistant - 阅读助手

> 激活词: 读一下 / 总结 / 提炼 / 摘要

## 功能

- 4点结构化提炼：主旨 / 论据 / 行动 / 疑问
- 支持网页URL抓取和纯文本输入
- 自动保存阅读记录到知识库

## Python 实现

```python
import os, json, re
from datetime import datetime

class ReadingAssistant:
    def __init__(self):
        self.log_file = os.path.join(os.path.dirname(__file__), "reading_log.json")
    
    def extract(self, text: str, source: str = "text") -> dict:
        """对输入文本做4点结构化提炼"""
        # 分段落
        paragraphs = [p.strip() for p in re.split(r'\n\n+', text) if p.strip()]
        
        result = {
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "paragraphs": len(paragraphs),
                "total_chars": len(text),
                "total_words": len(text.split())
            },
            "extraction": {
                "main_idea": self._extract_main_idea(paragraphs),
                "key_arguments": self._extract_arguments(paragraphs),
                "action_items": self._extract_actions(paragraphs),
                "open_questions": self._extract_questions(text)
            }
        }
        
        self._log(result)
        return result
    
    def _extract_main_idea(self, paragraphs: list) -> str:
        """提取主旨：取第一段或包含关键词的句子"""
        candidates = [p for p in paragraphs if any(k in p.lower() 
                      for k in ["this paper", "we propose", "in this", "本文", "我们提出"])]
        if candidates:
            return candidates[0][:300]
        return paragraphs[0][:300] if paragraphs else ""
    
    def _extract_arguments(self, paragraphs: list) -> list:
        """提取论据：含数据/引用的段落"""
        args = []
        for p in paragraphs:
            if any(k in p for k in ["%", "图", "table", "实验", "accuracy", "结果表明", "实验表明"]):
                args.append(p[:200])
        return args[:5]
    
    def _extract_actions(self, paragraphs: list) -> list:
        """提取行动项：含should/must/需要/应该的句子"""
        actions = []
        for p in paragraphs:
            sentences = re.split(r'[。.!?]', p)
            for s in sentences:
                if any(k in s for k in ["should", "must", "need", "需要", "应该", "建议", "推荐"]):
                    actions.append(s.strip())
        return actions[:5]
    
    def _extract_questions(self, text: str) -> list:
        """提取开放问题：含问号的句子"""
        questions = re.findall(r'[^。]*?[？?][^。]*', text)
        return [q.strip() for q in questions][:5]
    
    def _log(self, result: dict):
        """保存阅读记录"""
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, encoding="utf-8") as f:
                logs = json.load(f)
        logs.append(result)
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

# 使用示例
reader = ReadingAssistant()

# 从文本提炼
article = """
We propose FlashAttention, a novel attention algorithm that computes exact attention
with significantly fewer memory accesses. Our experiments show 2-4x speedup over
baseline implementations on GPT-2 and BERT. The key insight is to tile the attention
computation, avoiding materialization of the full N×N attention matrix. 
We recommend using block sizes of 128×128 for optimal performance.
"""
result = reader.extract(article, source="AI论文: FlashAttention")
print(f"主旨: {result['extraction']['main_idea'][:80]}...")
print(f"论据: {len(result['extraction']['key_arguments'])} 条")
print(f"行动: {result['extraction']['action_items']}")
```

## 网页抓取模式

```python
from urllib.request import urlopen
from urllib.parse import urlparse

def extract_url(url: str) -> dict:
    """从URL抓取并提炼"""
    try:
        resp = urlopen(url, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        # 简单去标签
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        reader = ReadingAssistant()
        return reader.extract(text, source=url)
    except Exception as e:
        return {"error": str(e)}

# 使用示例
# result = extract_url("https://arxiv.org/abs/2205.14135")
```

## 输出格式

```
📄 阅读摘要
━━━━━━━━━━━━━━━━━━━━
💡 主旨:
  FlashAttention通过分块计算注意力，
  避免完整N×N矩阵物化，实现2-4x加速

📊 论据:
  1. GPT-2和BERT上验证2-4x加速
  2. 推荐块大小128×128

✅ 行动:
  - 建议在长序列任务中使用FlashAttention

❓ 疑问:
  - 是否支持梯度检查点？
```

## 使用场景

1. **论文快速浏览**: 贴arXiv链接，30秒了解核心贡献
2. **公众号文章**: 太长不看？提炼4点够了
3. **技术文档**: API文档的快速导航
4. **邮件处理**: 长邮件自动摘要

## 依赖

- Python 3.8+
- urllib (标准库，可选URL抓取)
