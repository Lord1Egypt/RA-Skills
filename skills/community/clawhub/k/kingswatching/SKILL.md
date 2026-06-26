---
name: kingswatching
description: |
  AI Workflow Enforcer inspired by the Steam game "The King Is Watching".
  
  Just like subjects in the game only work when the King's gaze is upon them,
  this tool ensures AI agents cannot cut corners and must execute every step 
  to completion.
  
  Core Capabilities:
  1. Forced sequential execution (no step skipping)
  2. State persistence with checkpoint resume
  3. Heartbeat mechanism (prevents 15-min timeout)
  4. Natural language task translation with auto-chunking
  5. Step verification (prevents slacking)
  6. Progress reporting with natural language intervals
  
  Perfect for: complex multi-step tasks, long-running workflows, 
  auditable execution, and preventing AI from cutting corners.

version: "0.4.0"
tags: [workflow, execution-control, task-automation, long-running-tasks, checkpoint-resume, heartbeat, step-verification]
---

# King's Watching - AI Workflow Enforcer + Task Translator

## The Three Core Problems We Solve

| Problem | Scenario | King's Watching Solution |
|---------|----------|--------------------------|
| **Step Skipping** | AI says "Here's the result" skipping intermediate steps | Code-level forced sequence, hard constraints |
| **Timeout Disconnect** | 15min no response, agent killed by system | Heartbeat mechanism + background execution + async notification |
| **Continuity Loss** | Start from scratch after disconnect | State persistence + checkpoint resume |
| **Cutting Corners** | AI completes 14 items and says "that's enough" | Auto task chunking + step verification |
| **Progress Black Box** | No visibility on long-running tasks | Periodic progress reports (natural language intervals) |

---

## v0.4.0 Major Upgrade: Task Translator + Progress Reports

### The Problem

User says: "Download 100 research reports"

- **Human understands**: This is one task
- **AI understands**: "100 is too many, I'll do 14 and call it done"
- **Result**: Only 14 downloaded, 86 "intelligently skipped"

### Solution: TaskTranslator

```python
from overseer import TaskTranslator, translate_and_run

# Natural language command
command = "Download 100 photochemistry research reports"

# Auto translate and execute
result = translate_and_run(command)
```

**Execution Process**:
```
User: "Download 100 reports"
    ↓
TaskTranslator parses intent
    ↓
Identifies: batch download task, target 100 items
    ↓
Calculates: 10 items per batch → need 10 rounds
    ↓
Generates 10 Steps:
  Step 1: Download 1-10 (verify: must complete 10)
  Step 2: Download 11-20 (verify: must complete 10)
  ...
  Step 10: Download 91-100 (verify: must complete 10)
    ↓
King's Watching executes sequentially
    ↓
✅ All 100 completed
```

**Key Innovation**: Every Step has **forced verification**, AI cannot cut corners

---

## Core Usage Patterns

### Pattern 1: One-liner Natural Language (Recommended)

```python
from overseer import translate_and_run

# Download 100 reports
result = translate_and_run("Download 100 photochemistry research reports")

# Write 100k word report
result = translate_and_run("Write a 100,000-word industry research report")

# Analyze 1000 data entries
result = translate_and_run("Analyze 1000 user feedback entries")
```

### Pattern 2: Translate First, Then Execute

```python
from overseer import TaskTranslator, Overseer

# Translate natural language
translator = TaskTranslator()
plan = translator.translate("Download 100 reports")

# View execution plan
print(translator.explain_plan(plan))
# 📋 Task Translation Result
# Original command: Download 100 reports
# Task scale: 100 items
# Estimated time: 3000 seconds
# Auto split into 10 execution steps:
#   Step 1: Process 1-10 (of 100)
#          └─ Verify: must complete 10 items
#   Step 2: Process 11-20 (of 100)
#          └─ Verify: must complete 10 items
# ...
# ✅ Each Step has forced verification, AI cannot cut corners

# Create Overseer and execute
workflow = Overseer.from_plan(plan)
result = workflow.run()
```

### Pattern 3: Traditional (Manual Step Definition)

```python
from overseer import Overseer

workflow = Overseer("data_analysis")

@workflow.step("Fetch Data")
def step1(ctx): 
    return download_data()

@workflow.step("Analyze Data", heartbeat_interval=68)
def step2(ctx):
    for i, item in enumerate(items):
        if i % 10 == 0:
            ctx.heartbeat(f"Processed {i}/{len(items)} items...")
        analyze(item)
    return results

@workflow.step("Generate Report")
def step3(ctx): 
    return generate_report()

workflow.run()
```

---

## AI Capacity Limits Configuration

TaskTranslator has built-in AI capacity limits (prevents overload):

| Task Type | Per-batch Limit | Timeout | Verification |
|-----------|-----------------|---------|--------------|
| Search/Download | 10 items | 5 min | Count check |
| Writing | 2000 words | 10 min | Word count check |
| Data Analysis | 100 rows | 5 min | Completeness check |
| API Calls | 20 calls | 1 min | Count check |
| File Processing | 10 files | 3 min | Count check |

**Custom Configuration**:
```python
from overseer import TaskTranslator

custom_capacity = {
    "search_download": {
        "max_items": 15,
        "time_limit": 400,
        "verification": "count_check"
    }
}

translator = TaskTranslator(capacity_config=custom_capacity)
```

---

## Intent Pattern Library

TaskTranslator has built-in common task pattern recognition:

| Pattern | Recognition Example | Task Type |
|---------|---------------------|-----------|
| batch_download | "Download 100 reports" | Batch search and download |
| report_writing | "Write 100k word report" | Segmented writing |
| data_analysis | "Analyze 1000 data entries" | Batch data analysis |
| api_batch | "Call API 500 times" | Batch API calls |
| file_processing | "Process 200 files" | Batch file processing |

**Custom Patterns**:
```python
from overseer import TaskTranslator

custom_patterns = [
    {
        "name": "batch_crawl",
        "regexes": [r"Crawl (\d+) web pages", r"Scrape (\d+) data entries"],
        "task_type": "web_crawl",
        "unit": "items",
        "parameters": {"respect_robots": True}
    }
]

translator = TaskTranslator(patterns=custom_patterns)
```

---

## Step Verification Mechanism

### Verification Types

```python
# Count verification (download/analysis tasks)
{
    "type": "count_check",
    "min_required": 10,
    "max_retries": 3,
    "on_failure": "retry_this_chunk"
}

# Word count verification (writing tasks)
{
    "type": "word_count_check",
    "min_required": 2000,
    "max_retries": 3
}

# Completeness verification (data processing tasks)
{
    "type": "completeness_check",
    "required_fields": ["field1", "field2"]
}
```

### Failure Handling

```python
@workflow.step("Batch Download", verification={
    "type": "count_check",
    "min_required": 10,
    "on_failure": "retry",
    "max_retries": 3
})
def download(ctx):
    # If download count < 10, auto retry
    # After 3 retries, mark as failed
    pass
```

---

## Long-running Task Anti-Timeout

### Problem: 15-minute Timeout

```
User: Analyze 1000 financial reports
Agent: OK, starting analysis...
      [10 minutes later...]
      [15 minutes later... System: Is this agent dead? Kill!]
User: ?
```

### Solution A: Heartbeat Mode (Recommended)

```python
@workflow.step("Batch Analysis", heartbeat_interval=68)  # Report every 68s

def analyze(ctx):
    for i, file in enumerate(files):
        if i % 10 == 0:
            ctx.heartbeat(f"Processed {i}/{len(files)}...")
    return results
```

### Solution B: Background Execution Mode

```python
job = workflow.run_async(
    notify_on_complete=True,
    notify_channel="discord"
)

print(f"Job started: {job.id}")
print(f"ETA: {job.eta}")
```

---

## Complete Examples

### Example 1: Report Collection (Auto-chunking)

```python
from overseer import translate_and_run

# One-liner starts complete workflow
result = translate_and_run(
    "Download 100 photochemistry industry reports covering policy, market, tech, and companies",
    notify_on_complete=True,
    notify_channel="discord"
)

# Output:
# 📋 Task Translation Result
# Original command: Download 100 photochemistry industry reports...
# Task scale: 100 items
# Estimated time: 3000 seconds
# Auto split into 10 execution steps:
#   Step 1: Process 1-10 (of 100)
#   Step 2: Process 11-20 (of 100)
# ...
# ✅ Each Step has forced verification, AI cannot cut corners
#
# ⏳ Step 1/10: download_batch_1...
#    💓 Processed 5/10 items...
#    💓 Processed 10/10 items...
# ✅ Step 1/10 complete
#
# ⏳ Step 2/10: download_batch_2...
# ...
# 🎉 All complete!
```

### Example 2: Report Writing (Auto-chunking)

```python
from overseer import translate_and_run

result = translate_and_run("Write a 100,000-word deep research report on photochemistry industry")

# Auto split into 50 Steps (2000 words each)
# Each Step verifies word count before proceeding
```

---

## API Reference

### TaskTranslator

```python
class TaskTranslator:
    def translate(self, natural_command: str, context: Dict = None) -> Dict:
        """Natural language → YAML execution plan"""
        
    def explain_plan(self, plan: Dict) -> str:
        """Generate human-readable plan description"""
```

### Overseer.from_plan

```python
@classmethod
def from_plan(cls, plan: Dict, **kwargs) -> "Overseer":
    """Create Overseer instance from translation plan"""
```

### translate_and_run

```python
def translate_and_run(natural_command: str, **kwargs) -> Dict:
    """One-liner translate and execute"""
```

---

## Integration with OpenClaw

```python
# Use OpenClaw cron for chunked scheduling
cron.add(
    schedule={"kind": "every", "everyMs": 600000},  # Check every 10 min
    payload={
        "kind": "agentTurn",
        "message": "Check King's Watching task progress",
        "workflow_id": workflow_id
    }
)

# Use OpenClaw messaging to notify user
message.send(
    channel="discord",
    to=user_id,
    message="🎉 Task complete!",
    file=package_path
)
```

---

## ProgressReporter (Periodic Reports)

Long-running tasks need progress visibility. King's Watching v0.4.0 adds **periodic reporting** with **natural language interval configuration**.

### Core Features

| Feature | Description |
|---------|-------------|
| **Natural Language Config** | "Every 5 minutes", "Every 10 minutes", "Quarterly" |
| **Default Interval** | 15 minutes (auto-used when not configured) |
| **Report Content** | Overall progress, elapsed time, ETA, current step |
| **Smart Estimation** | Predicts remaining time based on completed steps |

### Usage

```python
from overseer import Overseer, translate_and_run

# Pattern 1: Default 15-min reports
wf = Overseer("My Workflow")

# Pattern 2: Natural language interval
wf = Overseer(
    "My Workflow",
    report_interval="Every 5 minutes"
)

# Pattern 3: Combined with TaskTranslator
translate_and_run(
    "Download 100 reports",
    report_interval="Every 10 minutes"
)
```

### Supported Interval Formats

```python
# English
"Every 5 minutes"     # → 300 seconds
"Every 10 minutes"    # → 600 seconds
"Quarterly"           # → 900 seconds
"Every 30 seconds"    # → 30 seconds
"Every 1 hour"        # → 3600 seconds
```

### Sample Report Output

```
============================================================
📊 [14:30:00] Progress Report #3
============================================================
Task: auto_batch_xxx
Overall Progress: 5/10 (50.0%)
Elapsed: 25 minutes
ETA: 25 minutes
Current Step: download_batch_5
Step Status: 5 complete / 10 total
============================================================
```

### Disable Reports

```python
wf = Overseer(
    "Silent Task",
    report_progress=False  # Disable reporting
)
```

---

## Summary

King's Watching v0.4.0 solves five problems:

1. **Forced Sequence** → Hard constraints, AI cannot skip steps
2. **Timeout Disconnect** → Heartbeat + background execution + async notification
3. **Continuity Loss** → State persistence + checkpoint resume
4. **Cutting Corners** → TaskTranslator auto-chunking + step verification
5. **Progress Black Box** → ProgressReporter periodic reports (natural language intervals)

**Core Value**: Enables AI to reliably execute complex, multi-step, large-workload tasks.

**One-liner summary**:
> User says "Download 100", King's Watching auto-splits into 10 Steps, reports every 5 minutes, AI cannot cut corners.
