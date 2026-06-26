# King's Watching User Guide

> 📦 Version: v0.4.0  
> 💡 One-liner: Make AI complete large batch tasks honestly, no slacking, no skipping, with visible progress

---

## What Can You Do With It?

Imagine these scenarios:

| Scenario | Traditional AI Problem | King's Watching Solution |
|----------|------------------------|--------------------------|
| "Download 100 research reports" | Only downloads 14, says "that's enough" | **Forces 10 rounds, 10 reports each, must complete all** |
| "Write a 100k word report" | Writes 20k and submits | **Splits into 50 segments, 2000 words each, complete one by one** |
| "Analyze 1000 data entries" | Disconnects midway, restart from scratch | **Checkpoint resume, continue from disconnect point** |
| "Develop 10 feature modules" | Does 3, says "finished" | **Accepts one by one, none can be skipped** |
| Long tasks | Timeout after 15 minutes | **Heartbeat keepalive + background execution** |
| Don't know progress | Black box execution, just wait | **Progress report every 5 minutes** |

---

## Three Usage Patterns (Simple to Advanced)

### 🟢 Pattern 1: One-liner (Recommended)

Simplest, suitable for most scenarios:

```python
from overseer import translate_and_run

# Download 100 reports, report every 5 minutes
result = translate_and_run(
    "Download 100 new energy industry research reports",
    report_interval="Every 5 minutes"
)
```

**What happens?**
1. King's Watching auto-understands your intent
2. Splits 100 into 10 Steps (10 reports each)
3. Every 5 minutes tells you: "50 done, 50 remaining, ETA 25 minutes"
4. Each Step has forced verification, AI cannot cut corners
5. Returns complete result

---

### 🟡 Pattern 2: Preview Execution Plan

Want to confirm plan before execution?

```python
from overseer import TaskTranslator, Overseer

# Step 1: Translate your command
translator = TaskTranslator()
plan = translator.translate("Download 100 new energy industry research reports")

# Step 2: View execution plan
print(translator.explain_plan(plan))

# Output:
# 📋 Task Translation Result
# Original command: Download 100 new energy industry research reports
# Task scale: 100 items
# Estimated time: 3000 seconds
# Auto split into 10 execution steps:
#   Step 1: Process 1-10 (of 100)
#   Step 2: Process 11-20 (of 100)
#   ...
# ✅ Each Step has forced verification, AI cannot cut corners

# Step 3: Execute after confirmation
workflow = Overseer.from_plan(plan)
result = workflow.run()
```

---

### 🟠 Pattern 3: Custom Steps

Need fine-grained control over each step? Define yourself:

```python
from overseer import Overseer

# Create workflow
workflow = Overseer(
    "My Data Analysis Task",
    report_interval="Every 10 minutes"
)

# Define Step 1: Fetch data
@workflow.step("Fetch Data")
def step1(ctx):
    data = download_files()
    return {"files": data}

# Define Step 2: Analyze data (with heartbeat)
@workflow.step("Analyze Data", heartbeat_interval=68)
def step2(ctx):
    for i, file in enumerate(files):
        # Report progress every 10 files
        if i % 10 == 0:
            ctx.heartbeat(f"Processed {i}/{len(files)} files...")
        analyze(file)
    return {"analyzed": len(files)}

# Define Step 3: Generate report
@workflow.step("Generate Report")
def step3(ctx):
    report = generate_report()
    return {"report": report}

# Execute
workflow.run()
```

---

## Supported Report Intervals

Describe in natural language, King's Watching auto-understands:

| You say | Actual interval |
|---------|-----------------|
| "Report every 30 seconds" | 30 seconds |
| "Every 5 minutes" | 5 minutes |
| "Every 10 minutes" | 10 minutes |
| "Quarterly" | 15 minutes |
| "Half hour" | 30 minutes |
| "Every 1 hour" | 1 hour |

**Default**: If not specified, reports every 15 minutes

---

## What Will You See?

### Start Execution

```
📋 Workflow: auto_batch_xxx
   Auto-generated: Download 100 new energy industry research reports
   Total 10 steps
```

### Periodic Report (Every 5 minutes)

```
============================================================
📊 [14:30:00] Progress Report #3
============================================================
Task: auto_batch_xxx
Overall: 5/10 (50.0%)
Elapsed: 25 minutes
ETA: 25 minutes
Current: download_batch_5
Steps: 5 done / 10 total
============================================================
```

### Step Complete

```
⏳ Step 5/10: download_batch_5...
✅ Step 5/10 Complete: 10 reports downloaded
```

### All Complete

```
🎉 All Complete!
```

---

## Task Splitting Examples

### 📄 Download Tasks

```python
# 100 reports → 10 Steps, 10 each
translate_and_run("Download 100 photochemistry research reports")

# 50 materials → 5 Steps, 10 each  
translate_and_run("Collect 50 industry materials")
```

### ✍️ Writing Tasks

```python
# 100k word report → 50 Steps, 2000 words each
translate_and_run("Write 100k word industry deep dive report")

# 20k word whitepaper → 10 Steps, 2000 words each
translate_and_run("Write 20k word technical whitepaper")
```

### 📊 Data Analysis Tasks

```python
# 1000 entries → 10 Steps, 100 each
translate_and_run("Analyze 1000 user feedback entries")

# 500 records → 5 Steps, 100 each
translate_and_run("Process 500 sales records")
```

### 💻 Development Tasks

```python
# 10 feature modules → 4 Steps, 3 each
translate_and_run("Develop 10 user management modules")

# 20 APIs → 4 Steps, 5 each
translate_and_run("Implement 20 REST API endpoints")

# 50 tests → 5 Steps, 10 each
translate_and_run("Write 50 unit test cases")

# 12 file refactoring → 3 Steps, 4 each
translate_and_run("Refactor 12 legacy modules")
```

### 🔌 API Call Tasks

```python
# 500 API calls → 25 Steps, 20 each
translate_and_run("Call API 500 times to fetch company info")
```

### 📁 File Processing Tasks

```python
# 200 files → 20 Steps, 10 each
translate_and_run("Process 200 PDF files to extract info")
```

---

## Checkpoint Resume (Recover After Interruption)

If task disconnects midway (network issue, system restart), no need to restart from scratch:

```python
from overseer import Overseer

# Create workflow with same name
workflow = Overseer("Previous Task Name")

# Continue from checkpoint
result = workflow.resume()
```

King's Watching will auto-find where it left off and continue from that Step.

---

## Background Execution (Long Tasks)

If task takes hours and you don't want to wait:

```python
from overseer import Overseer

workflow = Overseer("Long Running Task")

# Background execution, notify when done
job = workflow.run_async(
    notify_on_complete=True,
    notify_channel="discord"  # Send Discord message when done
)

print(f"Job started: {job.id}")
print(f"ETA: {job.eta}")

# You can do other things, notification comes when done
```

---

## FAQ

### Q1: Can AI still cut corners?

**No.** Each Step has forced verification:
- Download tasks: Must complete specified count (e.g., 10 items)
- Writing tasks: Must reach specified word count (e.g., 2000 words)
- Development tasks: Must pass code review and tests

If not met, auto-retry up to 3 times. Only mark as failed after 3 failures.

### Q2: Can I cancel during execution?

Yes. Just stop the program. Next time use `resume()` to continue from checkpoint.

### Q3: Can I change report frequency mid-task?

Not currently, need to set at start. Suggestions based on total duration:
- Tasks under 30 minutes: Every 5 minutes
- 1-2 hour tasks: Every 10 minutes
- Half-day tasks: Every 15-30 minutes

### Q4: What if a step keeps failing?

Default retry 3 times, if all fail:
1. Workflow marks as failed
2. Saves current progress
3. You can view error, fix, and restart from that Step

### Q5: What task types are supported?

Currently built-in support for:
- Search download (reports, papers, materials)
- Report writing (various long-form content)
- Data analysis (records, feedback, logs)
- Batch API calls
- Batch file processing
- Program development (modules, APIs, tests, refactoring)

Other types get generic handling, or you can customize rules.

---

## Quick Start Checklist

```python
# 1. Install
pip install -e /path/to/kingswatching

# 2. Import
from overseer import translate_and_run

# 3. One-liner execution
translate_and_run(
    "Your task description (with quantity)",
    report_interval="Every 5 minutes"
)

# 4. Watch progress reports until complete
```

---

## Summary

King's Watching solves several pain points of using AI for large tasks:

| Pain Point | Solution |
|------------|----------|
| AI slacks, only does part | ✅ Forced splitting + segment acceptance |
| Disconnect midway, restart from scratch | ✅ Checkpoint resume |
| Don't know progress | ✅ Periodic progress reports |
| 15-minute timeout disconnect | ✅ Heartbeat keepalive + background execution |
| Don't know how to split complex tasks | ✅ Natural language auto-translation |

**Core Idea**: Split "big tasks" into "small Steps", complete and accept one by one, ensure no corner-cutting.

---

**Remember in one sentence**:
> Tell King's Watching "Download 100 items, report every 5 minutes", it auto-splits into 10 Steps, periodically tells you progress, until all 100 are complete.
