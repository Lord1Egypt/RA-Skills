---
name: quick-note
version: 1.0.0
description: 快速笔记 - 想到就记，自动带标签归档(idea/todo/readlater)，本地JSON持久化，支持搜索回溯
tags: [notes, quick-capture, productivity, organization, journal]
author: laosi
source: original
---

# Quick Note - 快速笔记

> 激活词: 记一下 / 笔记 / 记个事

## 功能

- 语音/文字快速记录
- 自动标签分类（idea / todo / readlater）
- 本地 JSON 持久化，私密可靠
- 按标签筛选检索

## Python 实现

```python
import os, json
from datetime import datetime

NOTES_FILE = os.path.join(os.path.dirname(__file__), "quick_notes.json")

class QuickNote:
    def __init__(self):
        os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
        self.notes = self._load()
    
    def _load(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save(self):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
    
    def add(self, text: str, tags: list = None):
        """保存一条笔记"""
        if tags is None:
            # 自动标签：根据内容关键词判断
            tags = []
            if "?" in text or "为什么" in text:
                tags.append("readlater")
            if "todo" in text.lower() or "需要" in text or "要去做" in text:
                tags.append("todo")
            if not tags:
                tags.append("idea")
        
        note = {
            "id": len(self.notes) + 1,
            "text": text,
            "tags": tags,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        self.notes.append(note)
        self._save()
        return note
    
    def search(self, keyword: str = "", tags: list = None):
        """搜索笔记"""
        results = self.notes
        if keyword:
            results = [n for n in results if keyword.lower() in n["text"].lower()]
        if tags:
            results = [n for n in results if any(t in n["tags"] for t in tags)]
        return results
    
    def delete(self, note_id: int):
        self.notes = [n for n in self.notes if n["id"] != note_id]
        self._save()

# 使用示例
note = QuickNote()
note.add("学习Transformer的FlashAttention机制，据说能加速3x", tags=["readlater"])
note.add("需要买牛奶和鸡蛋", tags=["todo"])
note.add("用Python写一个CLI工具来自动化部署", tags=["idea"])

# 搜索
for n in note.search(tags=["idea"]):
    print(f"[{n['id']}] {n['text']}")
```

## 命令行用法

```bash
# 添加笔记（直接传参）
python -c "from quick_note import QuickNote; QuickNote().add('读一下RAG论文', tags=['readlater'])"

# 列出所有 idea 标签
python -c "from quick_note import QuickNote; [print(n['text']) for n in QuickNote().search(tags=['idea'])]"
```

## 数据格式

```json
[
  {
    "id": 1,
    "text": "学习FlashAttention机制",
    "tags": ["readlater"],
    "created": "2026-05-28T10:30:00",
    "updated": "2026-05-28T10:30:00"
  }
]
```

## 使用场景

1. **灵感捕捉**: 正在洗澡突然想到好点子，说出来自动存
2. **阅读清单**: 看到有趣的文章先标记 readlater，回头再读
3. **快速待办**: 「记一下，记得买牛奶」自动归类为 todo
4. **知识碎片**: 碎片化知识汇总，周末统一整理

## 依赖

- Python 3.8+
- 无第三方依赖
