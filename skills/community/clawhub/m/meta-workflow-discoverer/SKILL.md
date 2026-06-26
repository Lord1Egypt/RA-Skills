---
name: meta-workflow-discoverer
description: AI-powered workflow automation discoverer that observes user patterns, identifies repetitive tasks, and automatically generates executable automation workflows. Learns from history to create time-saving automations.
tags:
  - meta
  - workflow
  - automation
  - discovery
  - pattern-recognition
  - efficiency
version: 1.0.0
author: chenq
---

# Meta Workflow Discoverer

Automatically discover and create workflows from patterns.

## Features

### 1. Pattern Mining
- **Task Similarity**: Find similar recurring tasks
- **Sequence Patterns**: Identify common task sequences
- **Time Patterns**: Detect time-based patterns
- **Context Patterns**: Learn contextual triggers

### 2. Workflow Generation
- **Auto-Create**: Generate workflow from patterns
- **Step Optimization**: Optimize workflow steps
- **Error Handling**: Add robust error handling
- **Parallelization**: Identify parallelizable steps

### 3. Automation
- **Scheduled Triggers**: Time-based execution
- **Event Triggers**: Event-based execution
- **Conditional Logic**: Branching workflows
- **Looping**: Repeat workflows as needed

### 4. Learning
- **Success Tracking**: Monitor workflow success
- **Auto-Improve**: Refine based on results
- **User Feedback**: Incorporate user corrections
- **Cross-User Learning**: Share across users

## Installation

```bash
pip install numpy pandas scikit-learn
```

## Usage

### Initialize Discoverer
```python
from workflow_discoverer import WorkflowDiscoverer

discoverer = WorkflowDiscoverer(
    user_id="user123",
    min_occurrences=3
)
```

### Record Task History
```python
# Record task execution
discoverer.record_task(
    task="send daily report",
    steps=["fetch_data", "generate_chart", "send_email"],
    context={"time": "morning", "recipients": ["team"]},
    result="success"
)

# Record multiple similar tasks
for i in range(5):
    discoverer.record_task(
        task="weekly summary",
        steps=["collect_stats", "format_report", "post_to_slack"],
        context={"day": "friday"},
        result="success"
    )
```

### Discover Workflows
```python
# Discover potential workflows
workflows = discoverer.discover_workflows()

for wf in workflows:
    print(f"Workflow: {wf['name']}")
    print(f"Pattern: {wf['pattern']}")
    print(f"Confidence: {wf['confidence']:.0%}")
    print(f"Time saved: {wf['time_saved_minutes']} min")
```

### Create Automation
```python
# Create automated workflow
automation = discoverer.create_automation(
    workflow_id="weekly_summary",
    trigger={"type": "schedule", "time": "friday 09:00"},
    enabled=True
)

print(f"Automation created: {automation['id']}")
```

## API Reference

### Recording
| Method | Description |
|--------|-------------|
| `record_task(...)` | Record task execution |
| `record_sequence(...)` | Record task sequence |
| `import_history(...)` | Import from external source |

### Discovery
| Method | Description |
|--------|-------------|
| `discover_workflows()` | Find workflow patterns |
| `analyze_sequences()` | Analyze task sequences |
| `detect_triggers()` | Detect trigger patterns |

### Automation
| Method | Description |
|--------|-------------|
| `create_automation(...)` | Create automation |
| `enable_automation(id)` | Enable workflow |
| `disable_automation(id)` | Disable workflow |
| `run_automation(id)` | Run manually |

### Learning
| Method | Description |
|--------|-------------|
| `track_results()` | Track automation results |
| `improve_workflow()` | Improve based on results |
| `merge_patterns()` | Merge similar patterns |

## Workflow Templates

### Common Discovered Workflows

```python
# Data Analysis Workflow
{
    "name": "daily_data_review",
    "steps": [
        "fetch_yesterday_data",
        "run_analysis",
        "generate_report",
        "send_to_stakeholders"
    ],
    "trigger": "schedule: 09:00 daily",
    "time_saved": 30  # minutes
}

# Content Publishing Workflow
{
    "name": "cross_platform_post",
    "steps": [
        "create_content",
        "adapt_for_twitter",
        "adapt_for_linkedin",
        "schedule_posts"
    ],
    "trigger": "manual",
    "time_saved": 45
}

# Research Workflow
{
    "name": "topic_research",
    "steps": [
        "search_web",
        "filter_sources",
        "extract_key_info",
        "generate_summary"
    ],
    "trigger": "event: new_topic",
    "time_saved": 60
}
```

## Pattern Detection

### Task Similarity
```
Task: "send report to john"
Task: "send report to team"  
Similarity: 0.85
→ Potential workflow: "send_report"
```

### Sequence Patterns
```
[A, B, C] → D
[A, B, C] → D
[A, B, C] → D
Pattern: Auto-create [A,B,C] → D
```

### Time Patterns
```
Task: "morning standup" at 09:00 daily
Task: "morning standup" at 09:05 daily
→ Suggest: Scheduled automation at 09:00
```

## Example: Full Workflow

```python
# 1. Record user's recurring tasks
discoverer = WorkflowDiscoverer("user123")

# Over time, user does similar tasks
discoverer.record_task(
    task="analyze stock 600519",
    steps=["fetch_data", "compute_indicators", "generate_signal"],
    context={"stock": "600519", "type": "analysis"}
)

discoverer.record_task(
    task="analyze stock 000858",
    steps=["fetch_data", "compute_indicators", "generate_signal"],
    context={"stock": "000858", "type": "analysis"}
)

# 2. Discover patterns
workflows = discoverer.discover_workflows()

# 3. Create automation
if workflows:
    wf = workflows[0]
    
    automation = discoverer.create_automation(
        workflow_id=wf['id'],
        trigger={"type": "schedule", "cron": "0 9 * * 1-5"},
        params={"stocks": ["600519", "000858", "600036"]}
    )
    
    print(f"Created: {automation['name']}")
```

## Use Cases

- **Report Generation**: Auto-create scheduled reports
- **Data Processing**: Pipeline repetitive analysis
- **Communication**: Automate routine messages
- **Research**: Streamline information gathering
- **Trading**: Systematic trading routines

## Metrics

### Discovered Patterns
- Task frequency
- Sequence consistency
- Time regularity
- Context similarity

### Workflow Value
- Time saved per execution
- Error reduction
- Consistency improvement

## Integration

### With OpenClaw
```python
# Auto-discover from conversation
@hookimpl
def after_message(message, response):
    discoverer.record_task(
        task=extract_intent(message),
        steps=extract_tools_used(response),
        result="success"
    )
```

### With Skills
```python
# Learn from skill usage
for skill in used_skills:
    discoverer.record_task(
        task=skill.name,
        steps=skill.execution_steps,
        context=skill.context,
        result=skill.result
    )
```

## Best Practices

1. **More Data = Better Patterns**: Record more tasks for accuracy
2. **Verify Before Automating**: Review discovered workflows
3. **Start Simple**: Begin with 2-3 step workflows
4. **Monitor Results**: Track automation success
5. **Iterate**: Continuously improve workflows

## Future Capabilities

- Natural language workflow creation
- Cross-user pattern sharing
- AI-generated workflow optimization
- Self-healing workflows
