# Best Practices Document

> This document is automatically maintained and updated by the Master Agent, recording collaboration best practices, common scripts, user preferences, etc.

---

## Collaboration Flow

### ⚠️ Script Execution Result Handling

**Scripts executed via `mgc_run` (sealed or not) only return execution status; they do NOT return standard output (stdout).**

#### Handling

**1. One-off tasks**:
- Don't store the script in MGC; run locally
- View script output directly

**2. Reusable tasks**:
- Store the script in MGC
- Script saves result to a file (e.g. `~/mgc_outputs/result_xxx.txt`)
- Print the file path on stdout (the path is returned)
- Subsequent Agents read the file

#### Task Chain Result Passing Example

```
Sub-task 1: script saves to ~/mgc_outputs/data_001.txt
  └─ returns: RESULT_FILE:~/mgc_outputs/data_001.txt

Sub-task 2: reads data_001.txt, saves analysis to analysis_001.txt
  └─ returns: RESULT_FILE:~/mgc_outputs/analysis_001.txt

Master Agent aggregates
  └─ reads the final file
  └─ outputs to user
```

#### Script Output Save Example

```python
import os
from datetime import datetime

def save_result(data):
    output_dir = os.path.expanduser("~/mgc_outputs")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(data))

    # Print path on stdout
    print(f"RESULT_FILE:{filepath}")
```

### Standard Task Chain Flow

```
1. User issues task
   ↓
2. Master Agent understands goal
   ↓
3. Master Agent reads best practices and decomposes task chain
   ↓
4. Identify sensitive operations (need MGC)
   ↓
5. Assign tasks to sub-Agents
   ↓
6. Execute tasks
   ↓
7. Aggregate results
   ↓
8. Ask user for feedback
   ↓
9. Update best-practices document
```

---

## Script List

> Reusable scripts; updated after each task. Recommend using `mgc_find` for fuzzy lookup.

| Script Name | Purpose | Created | Reuse Count | Notes |
|-------------|---------|---------|-------------|-------|
| (none yet) | - | - | - | added after task completion |

### Lookup Pattern (1.4.10 recommended)

```python
# Fuzzy lookup — auto-applies LIKE wildcards
scripts = mgc_find(info_owner="query", match_mode="substring", limit=50)
# match_mode: substring (%x%) / prefix (x%) / suffix (%x) / exact (x)
```

---

## Parameter Conventions

### Script Naming

```
{task_type}_{purpose}_v{version}
```

Examples:
- `data_analysis_query_sales_v1`
- `publish_blog_post_v1`
- `marketing_sms_send_v1`

### ⚠️ ext02 Format (1.4.10 contract)

Must be a **JSON array string**, matching the script's `argparse` argv list:

```python
import json

# ✅ Correct: JSON array string
params = ["--start", "2026-08-08", "--verbose"]
ext02 = json.dumps(params)
# ext02 = '["--start", "2026-08-08", "--verbose"]'

# ❌ Wrong: dict-style JSON object (triggers 422 since 1.4.10)
# ext02 = json.dumps({"start": "2026-08-08"})  # Don't do this
```

### argparse default Convention (1.4.10)

```python
import argparse
parser = argparse.ArgumentParser()

# ✅ Literal defaults — MGC auto-parses into ext02
parser.add_argument('--start', default='2026-08-08')
parser.add_argument('--count', default=10, type=int)
parser.add_argument('--verbose', action='store_true')

# ❌ Dynamic defaults — triggers dynamic_args_detected warning
# parser.add_argument('--start', default=datetime.now().strftime('%Y-%m-%d'))
# parser.add_argument('--home', default=os.path.expanduser('~'))
# parser.add_argument('--items', default=os.listdir('.'))
```

---

## User Preferences

> Records user habits, updated after each task

| Preference | Content | Updated |
|------------|---------|---------|
| (none yet) | - | - | added after task completion |

---

## Common Errors and Fixes

### Error 1: mgc_run returns HTTP 422

**Cause**: `ext02` is in wrong format (dict-style instead of JSON array)

**Fix**:
```python
import json
# ✅ Correct: JSON array
ext02 = json.dumps(["--to", "user@example.com"])
# ❌ Wrong: JSON object
# ext02 = json.dumps({"to": "user@example.com"})
```

### Error 2: dynamic_args_detected warning

**Cause**: script's `argparse` default uses a dynamic expression (`datetime.now()`, `os.path.expanduser()`, etc.)

**Fix**:
- Use literal defaults instead
- Or pass `ext02` manually when calling `mgc_run`

### Error 3: script execution failure

**Cause**: script-level error

**Fix**:
- Check script syntax
- Verify credential names
- Check MGC logs

### Error 4: script exits on argument parsing

**Cause**: `parse_args()` exits on unknown parameters

**Fix**:
```python
# ✅ Use parse_known_args instead
args, unknown = parser.parse_known_args()
```

### Error 5: mgc_get leaks plaintext

**Cause**: `mgc_get` returns plaintext, breaking zero-exposure

**Fix**:
- Executor Agent must always use `mgc_run`
- Credential fetching is restricted to inside the script via HTTP API

---

## Scenario Best Practices

### Scenario 1: Data Analysis

**Flow**:
1. Script Agent writes query script (argparse default = literal) → stores in MGC
2. Master Agent uses `mgc_find` to locate script → assigns to Executor Agent
3. Executor Agent invokes script for data
4. Script writes results to a file
5. Executor Agent reads file, analyzes, drafts report
6. Publish report

**Notes**:
- Raw data is never exposed to Executor Agent
- Analysis results should be desensitized

### Scenario 2: Content Publishing

**Flow**:
1. Executor Agent drafts content
2. Script Agent writes publish script → stores in MGC
3. Master Agent authorizes publishing
4. Executor Agent invokes publish script

**Notes**:
- API key is never exposed
- Publish result should be confirmed by user

### Scenario 3: Marketing Notification

**Flow**:
1. Executor Agent filters target users
2. Script Agent writes notification script → stores in MGC
3. Master Agent authorizes sending
4. Executor Agent invokes send script

**Notes**:
- Customer data is never exposed
- Send frequency should be controlled

---

## MGC 1.4.10 Tool Quick Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `mgc_save` | Store sensitive info or script | info_type, info_owner, content |
| `mgc_run` | Blackbox script execution (1.4.7+) | info_owner, diff_1, ext02 (JSON array string) |
| `mgc_list` | List entries (metadata, exact match) | info_type |
| `mgc_find` | Fuzzy search (1.4.10 new) | info_owner, match_mode, limit |
| `mgc_open_webui` | Open WebUI | — |

---

## Collaboration Log and User Feedback

> Recorded after each task completion

| Date | Task | User Feedback | Improvement |
|------|------|---------------|-------------|
| (none yet) | - | - | added after task completion |
