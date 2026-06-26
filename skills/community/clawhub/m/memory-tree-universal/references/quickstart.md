# Memory Tree 快速上手

## 步骤 1：初始化

```python
from memory_tree import MemoryTreeHotPath

hotpath = MemoryTreeHotPath(db_path='memory.db')
```

## 步骤 2：摄入数据

```python
import time
messages = [
    {'role': 'user', 'content': '记住：项目预算 5 万', 'timestamp': time.time()},
    {'role': 'assistant', 'content': '已记住', 'timestamp': time.time()},
]
chunks = hotpath.ingest('session-001', messages, source='chat')
```

## 步骤 3：检索

```python
results = hotpath.search('预算', limit=5)
for r in results:
    print(f"[{r['score']:.2f}] {r['content'][:100]}")
```

## 步骤 4：清理（可选）

```python
hotpath.close()
```
