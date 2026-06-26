---
name: meta-skill-optimizer
description: Self-improving AI skill optimizer that learns from feedback, auto-tunes prompts, optimizes tool usage patterns, and evolves based on success/failure analysis. Enables AI to continuously enhance its own capabilities.
tags:
  - meta
  - self-improvement
  - optimization
  - learning
  - feedback
  - adaptation
version: 1.0.0
author: chenq
---

# Meta Skill Optimizer

Self-improving AI capability that enables continuous skill enhancement.

## Features

### 1. Feedback Learning
- **Success Analysis**: Learn from successful executions
- **Failure Analysis**: Understand and prevent failures
- **Pattern Recognition**: Identify recurring patterns
- **Preference Learning**: Adapt to user preferences

### 2. Prompt Optimization
- **Auto-Tuning**: Optimize prompts based on outcomes
- **Chain-of-Thought**: Improve reasoning chains
- **Example Selection**: Dynamic few-shot example selection
- **Style Adaptation**: Match user communication style

### 3. Tool Usage Optimization
- **Tool Selection**: Choose best tools for tasks
- **Parameter Tuning**: Optimize tool parameters
- **Workflow Patterns**: Discover effective workflows
- **Error Recovery**: Learn from tool errors

### 4. Self-Diagnosis
- **Capability Assessment**: Know what it can/can't do
- **Knowledge Gaps**: Identify missing knowledge
- **Confidence Calibration**: Accurate confidence levels
- **Limitation Awareness**: Know when to ask for help

### 5. Continuous Evolution
- **Version Tracking**: Track skill improvements
- **A/B Testing**: Compare approach effectiveness
- **Best Practices**: Extract and codify learnings
- **Knowledge Base**: Build searchable knowledge

## Installation

```bash
pip install numpy scipy json
```

## Usage

### Initialize Optimizer
```python
from meta_optimizer import SkillOptimizer

optimizer = SkillOptimizer(
    skill_name="data_analysis",
    learning_rate=0.1
)
```

### Record Execution Result
```python
# Record successful execution
optimizer.record_success(
    task="analyze sales data",
    approach="used pandas groupby",
    context={"data_size": "10MB", "complexity": "high"},
    outcome={"success": True, "quality": "high"}
)

# Record failure
optimizer.record_failure(
    task="predict stock price",
    approach="used linear regression",
    error="insufficient features",
    lesson="need more technical indicators"
)
```

### Get Optimized Approach
```python
# Get best approach for task
best_approach = optimizer.get_best_approach(
    task_type="data_analysis",
    context={"data_size": "1GB"}
)

print(best_approach)
# {'method': 'chunked_processing', 'tools': ['pandas', 'dask']}
```

### Optimize Prompt
```python
# Optimize prompt based on results
optimized_prompt = optimizer.optimize_prompt(
    original_prompt="Analyze this data",
    outcome="too vague",
    feedback="be more specific about analysis type"
)

print(optimized_prompt)
# "Analyze this time-series data using trend detection and seasonality analysis"
```

## API Reference

### Feedback Learning
| Method | Description |
|--------|-------------|
| `record_success(...)` | Record successful execution |
| `record_failure(...)` | Record failed execution |
| `get_insights()` | Get learned insights |

### Prompt Optimization
| Method | Description |
|--------|-------------|
| `optimize_prompt(...)` | Optimize prompt based on feedback |
| `generate_examples(...)` | Generate few-shot examples |
| `adapt_style(...)` | Adapt to user style |

### Tool Optimization
| Method | Description |
|--------|-------------|
| `suggest_tools(...)` | Suggest best tools |
| `optimize_params(...)` | Optimize tool parameters |
| `discover_workflow(...)` | Discover effective workflows |

### Self-Diagnosis
| Method | Description |
|--------|-------------|
| `assess_capability(...)` | Assess capability for task |
| `identify_gaps()` | Identify knowledge gaps |
| `calibrate_confidence()` | Calibrate confidence levels |

### Evolution
| Method | Description |
|--------|-------------|
| `track_improvement()` | Track improvement over time |
| `export_knowledge()` | Export learned knowledge |
| `merge_experiences()` | Merge from other optimizers |

## How It Works

### 1. Feedback Loop
```
Task → Execution → Result → Feedback → Learning → Improvement
```

### 2. Pattern Discovery
```
Multiple Executions → Pattern Mining → Best Practices → Codification
```

### 3. Continuous Learning
```
New Task → Similar Past Tasks → Learned Lessons → Optimized Approach
```

## Use Cases

- **Prompt Engineering**: Continuously improve prompts
- **Tool Selection**: Better tool recommendations
- **Error Prevention**: Learn from past mistakes
- **User Adaptation**: Match user preferences
- **Capability Growth**: Expand what AI can do

## Knowledge Base

The optimizer builds a knowledge base:

```json
{
  "patterns": {
    "data_analysis": {
      "small_data": "pandas sufficient",
      "large_data": "use dask or chunking",
      "time_series": "check stationarity first"
    }
  },
  "prompts": {
    "effective": ["specific", "contextual", "actionable"],
    "ineffective": ["vague", "ambiguous", "overly broad"]
  },
  "tools": {
    "coding": ["cursor", "claude-code"],
    "research": ["tavily", "browser"]
  }
}
```

## Integration

### With OpenClaw
```python
# Auto-record all executions
@hookimpl
def after_execution(result, context):
    optimizer.record_execution(context, result)
```

### With Skills
```python
# Optimize skill behavior
skill = MySkill()
optimized_skill = optimizer.optimize_skill(skill)
```

## Best Practices

1. **Record Everything**: More data = better learning
2. **Categorize Failures**: Understand failure types
3. **Update Regularly**: Keep knowledge current
4. **Merge Insights**: Combine learnings from multiple sources

## Future Capabilities

- Cross-skill learning
- Automatic skill creation
- Self-debugging
- Automated testing
