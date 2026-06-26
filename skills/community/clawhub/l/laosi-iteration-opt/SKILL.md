---
name: iteration-optimizer
description: 迭代优化器 - 原创技能。自动评估和改进AI生成的代码，通过多轮迭代达到最优结果。适用于代码优化、性能调优、质量提升等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [iteration, optimization, code-quality, improvement, feedback]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 迭代流程完整
- [x] 评估指标明确
- [x] 收敛条件清晰
- [x] 无语法错误

---

# Iteration Optimizer - 迭代优化器

> 原创技能 | 激活词: 迭代优化 / 改进代码 / 自动调优

## 核心概念

AI生成的代码通常需要多轮迭代优化：
- 第一版往往不是最优
- 需要持续的反馈和调整
- 迭代是达成高质量的关键

## 迭代流程

```
原始代码
    ↓
第1轮评估 → 问题1 + 建议1
    ↓
应用改进
    ↓
第2轮评估 → 问题2 + 建议2
    ↓
...
    ↓
收敛 (达到目标标准)
```

## 评估维度

### 1. 正确性 (Correctness)

```python
CORRECTNESS_METRICS = {
    'compilation': '能否编译通过',
    'test_pass': '测试是否通过',
    'edge_cases': '边界情况处理',
    'error_handling': '错误处理',
}
```

### 2. 性能 (Performance)

```python
PERFORMANCE_METRICS = {
    'time_complexity': '时间复杂度',
    'space_complexity': '空间复杂度',
    'response_time': '响应时间',
    'resource_usage': '资源消耗',
}
```

### 3. 可读性 (Readability)

```python
READABILITY_METRICS = {
    'naming': '命名是否清晰',
    'comments': '注释是否充分',
    'structure': '结构是否合理',
    'formatting': '格式是否规范',
}
```

### 4. 可维护性 (Maintainability)

```python
MAINTAINABILITY_METRICS = {
    'coupling': '耦合度',
    'cohesion': '内聚度',
    'duplication': '重复代码',
    'dependencies': '依赖关系',
}
```

## 评分系统

```python
def evaluate_code(code: str, metrics: dict) -> Score:
    scores = {}
    
    for metric_name, metric_func in metrics.items():
        scores[metric_name] = metric_func(code)
    
    # 加权平均
    weights = {
        'correctness': 0.4,
        'performance': 0.3,
        'readability': 0.2,
        'maintainability': 0.1,
    }
    
    final_score = sum(scores[k] * weights[k] for k in weights)
    
    return Score(
        overall=final_score,
        breakdown=scores,
        grade=get_grade(final_score),
    )

def get_grade(score: float) -> str:
    if score >= 0.9: return 'A'
    elif score >= 0.8: return 'B'
    elif score >= 0.7: return 'C'
    elif score >= 0.6: return 'D'
    else: return 'F'
```

## 改进建议生成

```python
def generate_improvements(code: str, score: Score) -> list[Improvement]:
    improvements = []
    
    if score.correctness < 0.8:
        improvements.append(Improvement(
            priority='high',
            category='correctness',
            issue='测试未全部通过',
            suggestion='添加边界条件测试',
        ))
    
    if score.performance < 0.7:
        improvements.append(Improvement(
            priority='high',
            category='performance',
            issue='循环嵌套过多',
            suggestion='考虑使用缓存或优化算法',
        ))
    
    if score.readability < 0.6:
        improvements.append(Improvement(
            priority='medium',
            category='readability',
            issue='变量命名不清晰',
            suggestion='使用描述性命名',
        ))
    
    return improvements
```

## 迭代控制

### 最大迭代次数

```python
MAX_ITERATIONS = 5  # 防止无限循环
```

### 收敛条件

```python
CONVERGENCE = {
    'score_threshold': 0.9,      # 达到90%就停止
    'improvement_threshold': 0.02,  # 提升小于2%停止
    'max_iterations': 5,         # 最多5轮
    'time_limit': 60,            # 最多60秒
}
```

### 终止条件

```python
def should_stop(iterations: int, score: Score, prev_score: Score) -> bool:
    # 达到目标分数
    if score.overall >= 0.9:
        return True
    
    # 提升太小
    improvement = score.overall - prev_score.overall
    if improvement < 0.02 and iterations > 2:
        return True
    
    # 达到最大次数
    if iterations >= 5:
        return True
    
    return False
```

## 输出格式

```markdown
## 迭代优化报告

### 第 3 轮迭代

### 当前评分
- **总分**: 0.85 (B)
- 正确性: 0.90
- 性能: 0.78
- 可读性: 0.82
- 可维护性: 0.85

### 本轮改进
✅ 修复了空指针异常
✅ 优化了循环结构

### 剩余问题
⚠️ [中等] 注释不足
⚠️ [中等] 可以使用更高效的算法

### 建议改进
1. 添加函数文档注释
2. 考虑用字典查找替代线性搜索

### 收敛状态
进度: 3/5 轮
提升: +0.08 (相比第2轮)
状态: 🔄 继续迭代
```

## 实际应用示例

### 场景: 优化排序算法

```markdown
用户: "帮我优化这个排序函数"

第1轮:
- 评分: 0.65 (D)
- 问题: O(n²) 复杂度太高
- 建议: 使用快速排序

第2轮:
- 评分: 0.78 (C+)
- 问题: 递归栈溢出风险
- 建议: 改用迭代实现

第3轮:
- 评分: 0.88 (B+)
- 问题: 基准选择不合理
- 建议: 使用三数取中法

第4轮:
- 评分: 0.93 (A)
- 状态: ✅ 收敛完成
```

## 集成建议

| 配合技能 | 效果 |
|---------|------|
| workflow-verifier | 验证每次迭代结果 |
| hallucination-detector | 检测迭代中的幻觉 |
| karpathy-principles | 保持代码简洁 |

## 原创性声明

本技能为原创，融合了：
- 代码质量评估模型
- 迭代优化算法
- 收敛判断逻辑
- 多维度评分系统

---

**作者**: laosi
**创建日期**: 2026-04-28