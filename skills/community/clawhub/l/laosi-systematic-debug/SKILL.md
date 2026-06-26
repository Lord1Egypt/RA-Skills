---
name: systematic-debug
version: 1.0.0
description: 系统化调试 - 假设驱动调试：观察→假设→隔离→验证→修复。附带Binary Search调试树、Minimal Reproducer生成
tags: [debugging, troubleshooting, development, root-cause]
author: laosi
source: original
---

# Systematic Debug - 系统化调试

> 激活词: 调试 / debug / 排查问题

## Debug流水线

```
观察问题 → 形成假设 → 隔离范围 → 验证假设 → 修复并回归
   ↓          ↓          ↓          ↓          ↓
 收集日志    3+候选   二分查找    最小复现   修复+测试
```

核心原则：**永远不要不带着假设就去改代码。**

## Python 实现

```python
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from datetime import datetime

@dataclass
class Hypothesis:
    description: str
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)
    confidence: float = 0.0  # 0-1
    confirmed: Optional[bool] = None
    
    def evaluate(self):
        """根据正反证据更新置信度"""
        total = len(self.evidence_for) + len(self.evidence_against)
        if total == 0:
            self.confidence = 0.0
        else:
            self.confidence = len(self.evidence_for) / total
        return self.confidence

@dataclass
class DebugSession:
    title: str
    symptoms: List[str] = field(default_factory=list)
    hypotheses: List[Hypothesis] = field(default_factory=list)
    log: List[str] = field(default_factory=list)
    created: str = ""
    
    def __post_init__(self):
        if not self.created:
            self.created = datetime.now().isoformat()
    
    def add_symptom(self, symptom: str):
        self.symptoms.append(symptom)
        self.log.append(f"[OBSERVE] 症状: {symptom}")
    
    def add_hypothesis(self, desc: str) -> Hypothesis:
        h = Hypothesis(description=desc)
        self.hypotheses.append(h)
        self.log.append(f"[HYPOTHESIZE] 假设: {desc}")
        return h
    
    def add_evidence(self, hypothesis_index: int, evidence: str, supports: bool):
        h = self.hypotheses[hypothesis_index]
        if supports:
            h.evidence_for.append(evidence)
        else:
            h.evidence_against.append(evidence)
        tag = "FOR" if supports else "AGAINST"
        self.log.append(f"[EVIDENCE] {tag}: {evidence}")
        h.evaluate()
    
    def best_hypothesis(self) -> Optional[Hypothesis]:
        if not self.hypotheses:
            return None
        return max(self.hypotheses, key=lambda h: h.confidence)
    
    def report(self) -> str:
        lines = [f"# Debug Report: {self.title}", f"Created: {self.created}\n"]
        lines.append("## 症状")
        for s in self.symptoms:
            lines.append(f"- {s}")
        
        lines.append("\n## 假设 (按置信度排序)")
        sorted_h = sorted(self.hypotheses, key=lambda h: -h.confidence)
        for i, h in enumerate(sorted_h):
            status = "✅ 确认" if h.confirmed else "❌ 排除" if h.confirmed is False else "⏳ 待验证"
            lines.append(f"\n### {status} H{i}: {h.description} (置信度: {h.confidence:.0%})")
            if h.evidence_for:
                lines.append("支持证据:")
                for e in h.evidence_for:
                    lines.append(f"  ✅ {e}")
            if h.evidence_against:
                lines.append("反对证据:")
                for e in h.evidence_against:
                    lines.append(f"  ❌ {e}")
        
        lines.append(f"\n## 根因")
        best = self.best_hypothesis()
        if best and best.confirmed:
            lines.append(f"✅ {best.description}")
        else:
            lines.append("⏳ 尚未确认根因")
        
        lines.append("\n## 调试日志")
        for entry in self.log:
            lines.append(f"- {entry}")
        
        return "\n".join(lines)

# 二分查找定位Bug
def binary_search_isolation(items: list, test_fn: Callable[[list], bool]) -> int:
    """在列表中用二分法找到第一个触发错误的元素"""
    lo, hi = 0, len(items)
    steps = 0
    while lo < hi:
        mid = (lo + hi) // 2
        steps += 1
        if test_fn(items[lo:mid]):
            lo = mid + 1
        else:
            hi = mid
    print(f"二分查找: {steps} 步定位到 index {lo}")
    return lo

# 使用示例
session = DebugSession(title="API超时排查")

# 观察阶段
session.add_symptom("用户列表API响应时间>10s（正常应<200ms）")
session.add_symptom("只在数据量>10000条时出现")
session.add_symptom("CPU使用率正常，内存正常")

# 形成假设
h1 = session.add_hypothesis("数据库缺少索引导致全表扫描")
h2 = session.add_hypothesis("N+1查询问题：每次循环都发SQL")
h3 = session.add_hypothesis("ORM懒加载触发过多查询")

# 收集证据
session.add_evidence(0, "EXPLAIN显示全表扫描 type=ALL", True)
session.add_evidence(0, "查询数据量100万只返回10条", True)
session.add_evidence(1, "代码中for循环内调用了query()", True)
session.add_evidence(1, "使用select_related可减少查询数", True)
session.add_evidence(2, "DB总查询数=用户数+1", True)

# 确认根因
session.hypotheses[2].confirmed = True

print(session.report())

# 定位到具体代码行
code_lines = [
    "def get_users():",
    "    users = User.objects.all()",
    "    result = []",
    "    for u in users:           # ← 懒加载，这里才发SQL",
    "        result.append({",
    "            'name': u.name,",
    "            'posts': u.posts.count()  # ← 每次循环一条SQL",
    "        })",
    "    return result",
]

# 用二分法定位问题代码段
def test_has_nplus1(lines_slice):
    return not any("count()" in l for l in lines_slice)

idx = binary_search_isolation(code_lines, test_has_nplus1)
print(f"问题代码在第 {idx+1} 行: {code_lines[idx]}")
```

## 反模式（不要这样做）

| ❌ 坏做法 | ✅ 好做法 |
|----------|----------|
| 随便改一行看看 | 先形成假设再改 |
| 同时改多个地方 | 一次只改一个变量 |
| 跳过最小复现 | 先写最小复现再改 |
| 只修症状 | 修根因加回归测试 |
| 不复盘 | 记录根因和修复过程 |

## 使用场景

1. **线上故障**: 服务宕机时按流水线快速定位根因
2. **性能问题**: 慢查询/高延迟，二分法定位瓶颈
3. **回归Bug**: 之前能用的功能坏了，从最近的变更开始查
4. **偶发Bug**: 记录所有条件，找交集缩小范围

## 依赖

- Python 3.8+
- 无第三方依赖
