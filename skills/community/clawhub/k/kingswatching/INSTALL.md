# King's Watching v0.4.0 - Installation Guide

## Quick Install

```bash
# Method 1: Copy to OpenClaw skills directory
cp -r kingswatching ~/.openclaw/skills/

# Method 2: pip install (if supported)
cd kingswatching && pip install -e .

# Method 3: Temporary use (demo/testing)
export PYTHONPATH=/path/to/kingswatching:$PYTHONPATH
```

## Quick Start (3 Minutes)

```python
#!/usr/bin/env python3
from overseer import Overseer

# 1. Create workflow
workflow = Overseer(
    name="my_first_workflow",
    enable_heartbeat=True,
    heartbeat_interval=60
)

# 2. Define steps
@workflow.step("Fetch Data")
def step1(ctx):
    return {"items": [1, 2, 3, 4, 5]}

@workflow.step("Process Data")
def step2(ctx):
    items = ctx.get_step_result("Fetch Data")["items"]
    for i, item in enumerate(items):
        if i % 2 == 0:
            ctx.heartbeat(f"Progress {i}/{len(items)}")
    return {"processed": len(items)}

@workflow.step("Generate Report")
def step3(ctx):
    return {"report": "Complete"}

# 3. Execute
result = workflow.run()
print(f"Result: {result}")
```

## Directory Structure

```
kingswatching/
├── SKILL.md                    # Skill declaration
├── README.md                   # Quick start guide
├── setup.py                    # Python package config
├── overseer/                   # Core code
│   ├── __init__.py            # Overseer class + Context + Step
│   ├── translator.py          # TaskTranslator
│   └── reporter.py            # ProgressReporter
├── examples/                   # Usage examples
│   ├── demo_features.py       # Feature demo
│   ├── demo_translator.py     # Translator demo
│   └── demo_reporter.py       # Reporter demo
└── test_overseer.py           # Test suite

After installation:
from overseer import Overseer, translate_and_run
```

## Core API

### Overseer Configuration

```python
Overseer(
    name="workflow_name",           # Workflow name (required)
    description="Description",       # Description (optional)
    state_dir=".overseer",          # State storage directory
    enable_heartbeat=True,          # Enable heartbeat (anti-timeout)
    heartbeat_interval=60,          # Heartbeat interval (seconds)
    async_mode=False,               # Async execution
    notify_on_complete=False,       # Notify on completion
    allow_resume=True               # Allow checkpoint resume
)
```

### Step Decorator

```python
@workflow.step(
    name="Step Name",               # Required
    retry=3,                        # Retry count on failure
    retry_delay=5,                  # Retry delay (seconds)
    timeout=300,                    # Timeout (seconds)
    heartbeat_interval=60           # Step-specific heartbeat interval
)
def my_step(ctx):
    # ctx is OverseerContext object
    # Get input parameter
    param = ctx.get("param_name")
    
    # Get previous step result
    prev = ctx.get_step_result("Previous Step Name")
    
    # Send heartbeat (required for long steps)
    ctx.heartbeat("Progress report")
    
    # Save state (for chunked execution)
    ctx.set_state("cursor", 100)
    
    # Return result
    return {"key": "value"}
```

### Execution Methods

```python
# Synchronous execution (blocking, for short tasks)
result = workflow.run(param="value")

# Asynchronous execution (background, for long tasks)
job = workflow.run_async(param="value")
# job.id, job.status, job.eta

# Checkpoint resume
workflow.resume(run_id="xxx")
```

## Four Typical Usage Patterns

### Pattern 1: Short Tasks (< 10 minutes)

```python
workflow = Overseer(name="quick_task")

@workflow.step("Quick Process")
def quick(ctx):
    data = process_data()
    return data

workflow.run()
```

### Pattern 2: Long Tasks + Heartbeat (10-30 minutes)

```python
workflow = Overseer(
    name="long_task",
    enable_heartbeat=True,
    heartbeat_interval=60
)

@workflow.step("Long Process", heartbeat_interval=60)
def long_process(ctx):
    for i in range(1000):
        process_one()
        if i % 100 == 0:
            ctx.heartbeat(f"Progress {i}/1000")
    return "done"

workflow.run()
```

### Pattern 3: Very Long Tasks + Chunking (> 30 minutes)

```python
workflow = Overseer(name="huge_task")

@workflow.step("Chunked Process")
def chunked(ctx):
    cursor = ctx.get_state("cursor", 0)
    batch_size = 100
    
    # Process one batch
    for i in range(cursor, cursor + batch_size):
        process(i)
    
    # Save progress
    ctx.set_state("cursor", cursor + batch_size)
    
    return {"processed": cursor + batch_size}

# Call multiple times, process one batch each time
while True:
    result = workflow.run()
    if result["processed"] >= total:
        break
    time.sleep(60)  # Interval between runs
```

### Pattern 4: Async Execution + Notification

```python
workflow = Overseer(
    name="bg_task",
    async_mode=True,
    notify_on_complete=True,
    notify_channel="discord"
)

@workflow.step("Background Process")
def bg_process(ctx):
    time.sleep(300)  # 5 minutes
    return "done"

job = workflow.run_async()
print(f"Job started: {job.id}")
# Returns immediately, runs in background, sends notification when done
```

### Pattern 5: Natural Language One-liner (NEW v0.4.0)

```python
from overseer import translate_and_run

# One-liner starts complete workflow
result = translate_and_run("Download 100 photochemistry research reports")

# Auto splits into 10 steps, each verified
# No cutting corners possible
```

## Running Tests

```bash
cd kingswatching

# Run all quick tests
python3 test_overseer.py

# Run specific tests
python3 test_overseer.py --test order      # Forced sequence
python3 test_overseer.py --test heartbeat  # Heartbeat mechanism
python3 test_overseer.py --test resume     # Checkpoint resume
python3 test_overseer.py --test async      # Async execution
python3 test_overseer.py --test long       # 5-minute long test
```

## Troubleshooting

### Problem: Steps killed by system

**Cause**: Step execution time > system timeout threshold (usually 15 minutes)

**Solution**:
1. Add heartbeat: `ctx.heartbeat("progress")`
2. Reduce heartbeat_interval (default 60s, can set to 30s)
3. Split steps: break large steps into multiple smaller steps

### Problem: Duplicate execution after resume

**Cause**: Step completed but state not properly saved

**Solution**: Check if step returns normally, exceptions cause state not to be saved

### Problem: Async task not notifying

**Cause**: notify_channel not configured or background thread exception

**Solution**: Check notify_on_complete=True and notify_channel settings

## Core Design Principles

1. **Forced Sequence**: Hard-coded for loop, cannot skip steps
2. **Heartbeat Keepalive**: Long steps must periodically send heartbeats
3. **State Persistence**: Auto-saved after each step, supports checkpoint resume
4. **Async Optional**: Background execution, doesn't block user
5. **Anti-Corner-Cutting**: Step verification prevents AI from slacking

## Version Info

- **Version**: v0.4.0
- **Features**: Forced sequence, heartbeat, state persistence, checkpoint resume, async execution, task translation, step verification, progress reporting
- **Dependencies**: Pure Python, zero external dependencies
- **Python**: >=3.8

## Next Steps

King's Watching is ready. Try your use case!
