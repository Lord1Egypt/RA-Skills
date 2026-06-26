---
name: multi-model-router
description: 多模型路由器 - 原创技能。根据任务特征自动选择最优AI模型，优化成本和性能。适用于大型项目、混合任务、成本优化等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [multi-model, routing, optimization, cost-saving, model-selection]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 模型选择逻辑完整
- [x] 成本优化策略明确
- [x] 任务分类清晰
- [x] 无语法错误

---

# Multi-Model Router - 多模型路由器

> 原创技能 | 激活词: 选择模型 / 路由模型 / 成本优化

## 核心概念

不同任务需要不同模型：
- 简单任务用小模型，省成本
- 复杂任务用大模型，保质量
- 特定任务用专用模型，提效率

## 模型能力矩阵

### 主流模型对比

| 模型 | 推理 | 编程 | 创意 | 成本 | 速度 |
|------|------|------|------|------|------|
| GPT-4o | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 高 | 中 |
| Claude 3.5 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 高 | 中 |
| GPT-4o-mini | ⭐⭐ | ⭐⭐ | ⭐⭐ | 低 | 快 |
| Claude 3-haiku | ⭐⭐ | ⭐⭐ | ⭐⭐ | 最低 | 最快 |
| DeepSeek-V3 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 中 | 快 |

### 擅长领域

```python
MODEL_STRENGTHS = {
    'claude-opus': {
        'best': ['复杂推理', '长文本分析', '代码审查'],
        'good': ['创意写作', '技术文档'],
        'avoid': ['简单问答', '批量处理'],
    },
    'claude-sonnet': {
        'best': ['编程', '数据分析', '快速迭代'],
        'good': ['日常对话', '文档生成'],
        'avoid': ['超长上下文'],
    },
    'gpt-4o': {
        'best': ['多模态', '实时信息', 'API集成'],
        'good': ['通用对话', '代码生成'],
        'avoid': ['超长输出'],
    },
    'deepseek': {
        'best': ['代码优化', '数学', '中文'],
        'good': ['低成本批量处理'],
        'avoid': ['英文创意写作'],
    },
}
```

## 任务分类

### 类型1: 简单任务 (Simple)

```markdown
特征:
- 单一问题
- 答案明确
- 不需要推理

示例:
- "现在几点了"
- "把这段文字翻译成英文"
- "计算 2+2"

推荐模型: Claude-haiku / GPT-mini
```

### 类型2: 常规任务 (Normal)

```markdown
特征:
- 需要一定推理
- 有明确答案
- 标准流程

示例:
- "写一个用户登录函数"
- "解释什么是闭包"
- "帮我总结这段文章"

推荐模型: Claude-sonnet / GPT-4o-mini
```

### 类型3: 复杂任务 (Complex)

```markdown
特征:
- 多步推理
- 需要深度分析
- 可能有歧义

示例:
- "设计一个微服务架构"
- "分析并优化这段代码性能"
- "制定产品上线计划"

推荐模型: Claude-opus / GPT-4o
```

### 类型4: 专业任务 (Specialized)

```markdown
特征:
- 需要专业知识
- 领域特定
- 高准���性要求

示例:
- "法律文件审查"
- "数学证明"
- "代码安全审计"

推荐模型: 专用模型 / Claude-opus
```

## 路由算法

### 主路由逻辑

```python
def route_task(task: Task) -> Model:
    # 1. 分析任务特征
    complexity = analyze_complexity(task)
    domain = analyze_domain(task)
    urgency = analyze_urgency(task)
    
    # 2. 成本预算
    budget = get_budget()
    
    # 3. 选择模型
    if complexity == 'simple':
        if budget == 'low':
            return 'claude-haiku'
        else:
            return 'gpt-mini'
    
    elif complexity == 'normal':
        if domain == 'code' and urgency == 'high':
            return 'claude-sonnet'  # 编程优先
        else:
            return 'deepseek'  # 性价比
    
    elif complexity == 'complex':
        if domain == 'reasoning':
            return 'claude-opus'
        elif domain == 'creative':
            return 'gpt-4o'
        else:
            return 'claude-sonnet-max'
    
    else:  # specialized
        return 'claude-opus'
```

### 成本优化

```python
def optimize_cost(task: Task, model: Model) -> Model:
    # 检查是否可以用更便宜的模型
    if can_use_cheaper(task):
        cheaper = find_cheaper_alternative(model)
        if test_quality(task, cheaper) >= 0.9:
            return cheaper
    
    return model
```

## 路由决策输出

```markdown
## 路由决策

### 任务分析
- **复杂度**: Complex (多步推理)
- **领域**: Code (编程任务)
- **紧迫度**: Normal
- **预算**: 标准

### 模型选择
- **推荐**: claude-opus
- **备选**: gpt-4o
- **降级**: claude-sonnet

### 理由
1. 任务复杂度高，需要强推理能力
2. 编程任务，Claude编码能力强
3. 有足够预算

### 预估成本
- claude-opus: $0.015/1K tokens
- 预计消耗: 约 $0.05
```

## 模型切换策略

### 串行路由

```python
def serial_route(task: Task) -> Response:
    # 用小模型先试
    response = call_model('haiku', task)
    
    if not satisfied(response):
        # 升级到大模型
        response = call_model('opus', task)
    
    return response
```

### 并行路由

```python
async def parallel_route(task: Task) -> Response:
    # 并行调用多个模型
    results = await asyncio.gather(
        call_model('haiku', task),
        call_model('sonnet', task),
        call_model('opus', task),
    )
    
    # 选择最佳结果
    return select_best(results)
```

## 性能监控

### 监控指标

```python
MONITOR = {
    'response_time': [],
    'quality_score': [],
    'cost_per_task': [],
    'model_usage': {},
}
```

### 路由优化

```python
def optimize_routing():
    # 分析历史数据
    # 找出成本和质量最佳平衡点
    # 调整路由规则
    pass
```

## 集成建议

| 配合技能 | 效果 |
|---------|------|
| intent-classifier | 先识别意图再路由 |
| hallucination-detector | 验证模型输出质量 |
| context-optimizer | 优化各模型的上下文 |

## 原创性声明

本技能为原创，融合了：
- 模型能力评估
- 任务复杂度分析
- 成本效益优化
- 动态路由算法

---

**作者**: laosi
**创建日期**: 2026-04-28