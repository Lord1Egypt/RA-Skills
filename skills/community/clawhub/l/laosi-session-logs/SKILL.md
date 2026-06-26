---
name: session-logs
description: 会话日志分析 - 搜索和分析历史会话日志，查找之前的对话内容和结果。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [session, logs, history, search, analysis]
version: 1.0.0
author: laosi
source: adapted
---

# Session Logs - 会话日志分析

> 激活词: 会话日志 / 搜索历史 / 历史记录

## 功能

- 搜索历史会话
- 分析会话模式
- 提取关键信息
- 按时间过滤

## Python实现

```python
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class SessionLogs:
    def __init__(self, log_dir: str = "~/.openclaw/logs"):
        self.log_dir = Path(log_dir).expanduser()
    
    def list_sessions(self, days: int = 7) -> list:
        sessions = []
        cutoff = datetime.now() - timedelta(days=days)
        
        for file in self.log_dir.glob("*.log"):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime > cutoff:
                sessions.append({
                    'file': file.name,
                    'modified': mtime,
                    'size': file.stat().st_size
                })
        
        return sorted(sessions, key=lambda x: x['modified'], reverse=True)
    
    def search_logs(self, keyword: str, days: int = 7) -> list:
        results = []
        for file in self.log_dir.glob("*.log"):
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if keyword.lower() in line.lower():
                            results.append({
                                'file': file.name,
                                'line': i,
                                'content': line.strip()[:200]
                            })
            except:
                pass
        return results
    
    def extract_commands(self, log_file: str) -> list:
        commands = []
        with open(self.log_dir / log_file, 'r') as f:
            for line in f:
                if 'command:' in line.lower() or 'user:' in line.lower():
                    commands.append(line.strip())
        return commands
```

## 使用示例

```python
logs = SessionLogs()

# 列出最近7天会话
recent = logs.list_sessions(7)
for s in recent:
    print(f"{s['modified']}: {s['file']}")

# 搜索关键词
results = logs.search_logs("Python", days=30)
for r in results:
    print(f"{r['file']}:{r['line']}: {r['content']}")
```

## 输出格式

```markdown
## 会话日志

### 最近会话
| 日期 | 文件 | 大小 |
|------|------|------|
| 2026-04-28 | 2026-04-28.log | 1.2MB |
| 2026-04-27 | 2026-04-27.log | 2.3MB |

### 搜索结果 "Python"
- 2026-04-28.log:142: "用Python写个脚本..."
- 2026-04-27.log:89: "Python怎么导入模块"
```