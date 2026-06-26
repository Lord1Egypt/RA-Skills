# 🔄 Background Running Support for PhD Research Companion

## Overview

本技能的主要 Python 脚本**本身不是持续运行的服务**,而是**一次性任务工具**。但某些特定场景可以/应该后台运行以提高效率。

---

## Which Tasks Should Run in Background?（哪些适合后台）

### ✅ **推荐后台运行** (Long-running tasks)

| Task | Script | Duration | Why Background |
|------|--------|----------|----------------|
| Literature download & analysis | `multi_source_search.py` + `paper_analyzer.py` | 5-20 min | Downloads PDFs from multiple APIs, parses documents |
| Batch paper deep analysis | `paper_analyzer.py --mode deep` on 50+ files | 10-30 min | Complex extraction and comparison logic |
| Experiment execution tracking | External experiment runs referenced by design YAML | Hours | GPU training jobs monitored by logging scripts |

### ⛔ **不适合后台运行** (Interactive/quick tasks)

| Task | Script | Duration | Why Not Background |
|------|--------|----------|-------------------|
| Project initialization | `init_research_project.py` | 5-10 sec | Instant file creation, user should see structure immediately |
| LaTeX template generation | `generate_latex_template.py` | 2-5 sec | Quick output, needs confirmation of success |
| Compliance checking | `check_compliance.py` | 5-15 sec | User needs immediate feedback on submission readiness |
| Revision tracking | `revision_tracker.py` | 2-3 sec | Interactive entry process |

---

## How to Run in Background (OpenClaw Native Methods)

### Method 1: OpenClaw exec with background mode
```bash
# In OpenClaw, use the exec tool with background=true
python /home/user/workspace/skills/phd-research-companion/scripts/multi_source_search.py \
    -q "machine unlearning" \
    -l 30 \
    --output ./results-2024-03-10
    
# Then check progress later:
# OpenClaw automatically manages background process IDs
```

### Method 2: Unix-style background with nohup
```bash
cd /home/user/workspace/skills/phd-research-companion/scripts

nohup python multi_source_search.py \
    -q "research topic" \
    -s arxiv,semanticscholar \
    --limit 50 \
    > search-output.log 2>&1 &

# Check if running: ps aux | grep multi_source_search
# View progress: tail -f search-output.log
```

### Method 3: Using Python subprocess (for integrated automation)
```python
import subprocess
from pathlib import Path

def run_background(task_type, args_str):
    script_map = {
        "litterature_survey": "multi_source_search.py",
        "paper_analysis": "paper_analyzer.py"
    }
    
    script_path = Path(__file__).parent / "scripts" / script_map[task_type]
    
    process = subprocess.Popen(
        ["python3", str(script_path), *args_str.split()],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(Path(__file__).parent.parent)
    )
    return process.pid

# Usage:
pid = run_background("literature_survey", "-q \"federated learning\" -l 20")
print(f"Background task started with PID: {pid}")
```

---

## Enhanced Script Version for Background Monitoring（改进版后台支持）

### Progress Tracking Feature Addition

建议为长耗时任务添加以下特性：

#### 方式 A: Write progress to file (simple method)
```python
# Add to multi_source_search.py at the beginning
from pathlib import Path
progress_file = Path("search-progress.json")

def update_progress(percentage, message):
    status = {"progress": percentage, "stage": message, "timestamp": datetime.now().isoformat()}
    progress_file.write_text(json.dumps(status, indent=2))

# In main loop:
update_progress(10, f"Started search for query: {args.query}")
for i, source in enumerate(sources):
    update_progress(30 + (30 * i / len(sources)), f"Querying {source}...")

update_progress(90, "Processing results and generating citations...")  
update_progress(100, "Completed successfully!")
```

#### 方式 B: Check progress from another terminal
```bash
# Monitor ongoing task (while it runs in background)
watch -n 5 'cat search-progress.json'

# After completion:
cat search-progress.json
ls -lh ./results-*.bibtex
```

---

## Cron Job Integration（定期自动化任务）

### Use Case：Daily Literature Updates（每日自动更新文献）

If you regularly want to monitor new publications in your research domain, set up a cron job:

```bash
# Edit crontab
crontab -e

# Add daily morning run at 8:00 AM
0 8 * * * cd /home/user/workspace/skills/phd-research-companion/scripts && \
    python multi_source_search.py -q "machine unlearning" -l 5 -s arxiv > /tmp/literature-update.log 2>&1

# Output goes to /tmp or redirect to project folder:
# 0 8 * * * YOUR_COMMAND >> ~/research-project/01-literature-survey/daily-updates.log 2>&1
```

---

## OpenClaw-Specific Background Integration（OpenClaw 专用后台集成）

### Using sub-agent pattern for long tasks:

1. Spawn a new agent instance dedicated to the background task
2. Main agent waits or continues other work
3. Background agent reports completion when done

示例配置可以在 `openclaw-config.yaml` 中添加：

```yaml
background_task_config:
  enabled: true
  max_duration_hours: 4
  notification_on_complete: true
  
long_running_scripts:
  multi_source_search.py:
    duration_estimate_minutes: "5-20"
    requires_background: true
    
  paper_analyzer.py--mode deep:
    duration_estimate_minutes: "10-30"  
    requires_background: true
```

---

## Quick Recommendations（最佳实践建议）

### For Single Research Session（单人工作场景）
```bash
# Just run normally - most tasks are quick anyway
python init_research_project.py ...
python generate_latex_template.py ...

# Only background the slow ones:
nohup python multi_source_search.py ... &
watch -n 10 'ps aux | grep multi_source_search'
```

### For Automated Pipelines（自动化流水线）
```bash
# Script automation wrapper with progress tracking
#!/bin/bash
cd /home/user/workspace/skills/phd-research-companion/scripts

START_TIME=$(date +%s)

echo "Starting PhD research workflow automation..."

# Step 1: Literature (background)  
nohup python multi_source_search.py -q "$TOPIC" -l 20 > step1.log 2>&1 &
LITERATURE_PID=$!

# Wait and monitor  
while kill -0 $LITERATURE_PID 2>/dev/null; do
    sleep 30
    echo "Literature search still running..."
done

# Step 2: Analysis (wait for step 1)
python paper_analyzer.py --input results/*.md --mode deep

END_TIME=$(date +%s)
echo "Completed in $((END_TIME - START_TIME)) seconds"
```

---

## Summary（总结）

| Feature | Supported? | Implementation Method |
|---------|-----------|----------------------|
| Background execution | ✅ Yes | Use `nohup ... &` or OpenClaw `exec background=true` |
| Progress monitoring | ⚠️ Partially (needs enhancement) | Add progress JSON writing to long scripts |
| Cron scheduling | ✅ Yes | Standard Unix cron jobs |
| Parallel task execution | ✅ Yes | Multiple `&` in parallel |
| Agent sub-task pattern | 🟡 OpenClaw specific | Use sub-agent spawning API if available |

**Recommendation**: 为长时间任务（文献搜索、批量 PDF 分析）添加后台运行选项，快速任务保持前景执行以获得即时交互反馈。

---
*Updated: March 2026 - PhD Research Companion Background Run Guide*