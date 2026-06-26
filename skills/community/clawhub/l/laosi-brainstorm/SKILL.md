---
name: brainstorm
version: 1.0.0
description: 结构化头脑风暴 - 4视角拆解问题：约束/方案/边界/优先级，自动归档到知识库
tags: [thinking, ideation, creativity, planning, productivity]
author: laosi
source: original
---

# Brainstorm - 结构化头脑风暴

> 激活词: 头脑风暴 /  brainstorm / 想一下

## 为什么需要结构化

人的思维天然有偏见：确认偏误、锚定效应、可用性启发。固定4视角拆解能强迫大脑跳出惯性轨道。

## Python 实现

```python
import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class BrainstormSession:
    topic: str
    constraints: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
    edge_cases: List[str] = field(default_factory=list)
    priorities: List[str] = field(default_factory=list)
    created: str = ""
    
    def __post_init__(self):
        if not self.created:
            self.created = datetime.now().isoformat()
    
    def add_constraint(self, item: str):
        self.constraints.append(item)
    
    def add_alternative(self, item: str):
        self.alternatives.append(item)
    
    def add_edge_case(self, item: str):
        self.edge_cases.append(item)
    
    def add_priority(self, item: str):
        self.priorities.append(item)
    
    def summarize(self) -> dict:
        return {
            "topic": self.topic,
            "counts": {
                "constraints": len(self.constraints),
                "alternatives": len(self.alternatives),
                "edge_cases": len(self.edge_cases),
                "priorities": len(self.priorities),
            },
            "total_ideas": sum(len(v) for v in [
                self.constraints, self.alternatives,
                self.edge_cases, self.priorities
            ]),
            "created": self.created
        }
    
    def to_markdown(self) -> str:
        lines = [f"# 头脑风暴: {self.topic}\n"]
        lines.append("## 🚧 约束条件")
        for c in self.constraints:
            lines.append(f"- {c}")
        lines.append("\n## 💡 备选方案")
        for a in self.alternatives:
            lines.append(f"- {a}")
        lines.append("\n## ⚡ 边界情况")
        for e in self.edge_cases:
            lines.append(f"- {e}")
        lines.append("\n## 🎯 优先级")
        for p in self.priorities:
            lines.append(f"- {p}")
        return "\n".join(lines)

# 使用示例
s = BrainstormSession(topic="为个人博客添加AI搜索功能")
s.add_constraint("不能增加服务器成本")
s.add_constraint("搜索延迟必须<2秒")
s.add_constraint("必须支持中文分词")

s.add_alternative("使用Meilisearch自托管全文搜索")
s.add_alternative("调用OpenAI Embedding API + 向量数据库(Pinecone)")
s.add_alternative("纯前端TF-IDF + 倒排索引")
s.add_alternative("使用Cloudflare Workers + Workers AI")

s.add_edge_case("博客内容为空时搜索返回什么")
s.add_edge_case("用户输入特殊字符/正则注入")
s.add_edge_case("并发大量搜索请求时")
s.add_edge_case("索引更新延迟导致搜到旧内容")

s.add_priority("MVP: 纯前端TF-IDF搜索现有文章")
s.add_priority("Phase 2: 接入LLM做语义搜索")
s.add_priority("Phase 3: 中文纠错提示")

print(s.to_markdown())
print(f"\n总计 {s.summarize()['total_ideas']} 个想法")
```

## 4视角详解

```
┌─────────────┐     ┌─────────────┐
│   约束条件   │     │   备选方案   │
│  不可逾越    │     │  跳出惯性    │
├─────────────┤     ├─────────────┤
│ - 硬限制     │     │ - 3+方案     │
│ - 不能做的   │     │ - 反直觉的   │
└─────────────┘     └─────────────┘
        ↑                  ↑
        输入              发散
        ──────────────────→
        ←──────────────────
        收敛               选择
        ↓                  ↓
┌─────────────┐     ┌─────────────┐
│   边界情况   │     │   优先级     │
│   测试极限   │     │   MVP排序    │
├─────────────┤     ├─────────────┤
│ - 极端值     │     │ - 先做什么   │
│ - 静默失败   │     │ - 依赖关系   │
└─────────────┘     └─────────────┘
```

## 使用场景

1. **产品设计**: 新功能上线前跑一遍，避免遗漏边界情况
2. **技术选型**: 比较不同方案时，约束和优先级视角必用
3. **Bug修复**: 备选方案视角打开思路，不局限于一种解法
4. **OKR制定**: 约束（资源限制）+ 优先级（什么最重要）

## 命令行用法

```bash
python -c "
from brainstorm import BrainstormSession
s = BrainstormSession('test')
s.add_constraint('time limit: 2hrs')
s.add_alternative('approach A')
print(s.to_markdown())
"
```

## 依赖

- Python 3.8+
- 无第三方依赖
