---
name: clipboard-history
version: 1.0.0
description: 剪贴板历史 - 自动保存复制内容，最多50条历史，可搜索可恢复。再也不丢复制过的东西
tags: [clipboard, history, utility, windows, productivity]
author: laosi
source: original
---

# Clipboard History - 剪贴板历史

> 激活词: 剪贴板 / 复制历史 / clipboard

## 有什么用

复制-粘贴是最高频的操作之一。但 Windows 的剪贴板只能存一个。这个技能自动保存每次复制的内容，可以随时找回。

## Python 实现

```python
import os
import json
import time
from datetime import datetime

CLIPBOARD_FILE = os.path.join(os.path.dirname(__file__), "clipboard_history.json")

class ClipboardHistory:
    MAX_ITEMS = 50
    
    def __init__(self):
        os.makedirs(os.path.dirname(CLIPBOARD_FILE), exist_ok=True)
        self.history = self._load()
    
    def _load(self):
        if os.path.exists(CLIPBOARD_FILE):
            try:
                with open(CLIPBOARD_FILE, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                return []
        return []
    
    def _save(self):
        with open(CLIPBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def save(self, text: str) -> dict:
        """保存一条剪贴板记录（去重）"""
        if not text or not text.strip():
            return {"saved": False, "reason": "empty"}
        
        # 去重：不保存和上一条相同的
        if self.history and self.history[0]["text"] == text.strip()[:200]:
            return {"saved": False, "reason": "duplicate"}
        
        entry = {
            "text": text.strip()[:200],
            "length": len(text.strip()),
            "time": datetime.now().isoformat(),
            "timestamp": time.time()
        }
        self.history.insert(0, entry)
        if len(self.history) > self.MAX_ITEMS:
            self.history = self.history[:self.MAX_ITEMS]
        self._save()
        return {"saved": True, "index": 0, "count": len(self.history)}
    
    def get(self, index: int = 0) -> str:
        """取指定位置的剪贴板历史"""
        if 0 <= index < len(self.history):
            return self.history[index]["text"]
        return ""
    
    def search(self, keyword: str) -> list:
        """搜索历史中的内容"""
        results = []
        for i, entry in enumerate(self.history):
            if keyword.lower() in entry["text"].lower():
                results.append({"index": i, "text": entry["text"], "time": entry["time"]})
        return results
    
    def clear(self):
        """清空历史"""
        self.history = []
        self._save()
    
    def stats(self) -> dict:
        """统计信息"""
        if not self.history:
            return {"total": 0}
        return {
            "total": len(self.history),
            "oldest": self.history[-1]["time"],
            "newest": self.history[0]["time"],
            "total_chars": sum(e["length"] for e in self.history)
        }

# 使用示例
ch = ClipboardHistory()

# 模拟复制操作
ch.save("Python 3.12 新增了类型参数语法")
ch.save("FlashAttention 实现了2-4x加速")
ch.save("https://github.com/anomalyco/opencode")

# 搜索
results = ch.search("python")
for r in results:
    print(f"[{r['index']}] {r['text']}")

# 取最新一条
latest = ch.get(0)
print(f"最新: {latest}")

# 统计
print(f"共 {ch.stats()['total']} 条历史")
```

## 监控模式（自动保存）

```python
import pyperclip
import time

def auto_watch(interval: float = 1.0):
    """轮询剪贴板，自动保存新内容"""
    ch = ClipboardHistory()
    last = ""
    print("剪贴板监控已启动（按 Ctrl+C 停止）")
    try:
        while True:
            try:
                current = pyperclip.paste()
                if current and current != last:
                    result = ch.save(current)
                    if result["saved"]:
                        print(f"  保存: {current[:40]}...")
                    last = current
            except Exception:
                pass
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n监控已停止")

# 启动监控
# auto_watch()
```

## 数据格式

```json
[
  {
    "text": "FlashAttention 实现了2-4x加速",
    "length": 20,
    "time": "2026-05-28T10:30:00",
    "timestamp": 1748392200.0
  }
]
```

## 使用场景

1. **编程**: 复制了一段代码忘了存，回来还能找回
2. **写作**: 不同段落之间切换，之前复制的引用还在
3. **研究**: 搜集资料时多次切换复制源，不丢失
4. **办公**: 不同文档间复制粘贴，随时回溯

## 依赖

- Python 3.8+
- pyperclip (可选，用于自动监控模式)
