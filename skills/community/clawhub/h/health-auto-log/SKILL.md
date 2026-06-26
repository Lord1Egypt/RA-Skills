---
name: health-auto-log
description: Automatically detect and log health data (weight, blood sugar, exercise) to AX3 system. Use when user sends health measurements via WhatsApp or other messaging channels, especially messages containing numbers with health-related keywords like "體重", "血糖", or plain numeric values that could be weight measurements.
---

# Health Auto Log

## Overview

Automatically detect health metrics from user messages and record them to AX3 Personal system. Supports weight, blood sugar, and exercise time tracking with flexible input formats.

## When to Use This Skill

Trigger this skill when user messages contain:
- Weight measurements (e.g., "體重69.8公斤", "69.8kg", "69.8")
- Blood sugar readings (e.g., "血糖120", "120 mg/dL")
- Exercise time (e.g., "跑步機30分", "跑步30")

## Quick Start

Use the `record_health_data.py` script to process any message:

```bash
python3 scripts/record_health_data.py "體重69.8公斤"
```

The script will:
1. Extract health metrics from the message
2. Validate the values are within reasonable ranges
3. Record to AX3 using mcporter
4. Return confirmation with record IDs

## Supported Metrics

### 1. Weight (體重)

**Habit ID:** 1  
**Unit:** kg  
**Range:** 40-200 kg

**Supported formats:**
- `體重69.8公斤`
- `69.8kg`
- `69.8` (plain number)

### 2. Blood Sugar (血糖)

**Habit ID:** 4  
**Unit:** mg/dL  
**Range:** 50-500 mg/dL

**Supported formats:**
- `血糖120`
- `120 mg/dL`

### 3. Running Time (跑步機)

**Habit ID:** 2  
**Unit:** minutes  

**Supported formats:**
- `跑步機30分`
- `跑步30`

## Workflow

### Automatic Detection Flow

1. **Receive message** from WhatsApp or other channel
2. **Run script** with message text: `python3 scripts/record_health_data.py "<message>"`
3. **Extract metrics** using regex patterns
4. **Validate** values are in reasonable ranges
5. **Record to AX3** via mcporter call to `ax3-personal.record_habit`
6. **Confirm** with user showing what was recorded

### Example Usage

```bash
# Single metric
python3 scripts/record_health_data.py "體重69.8公斤"
# Output: ✅ 體重 69.8 kg 已記錄

# Multiple metrics in one message
python3 scripts/record_health_data.py "體重69.8公斤 血糖120"
# Output: 
# ✅ 體重 69.8 kg 已記錄
# ✅ 血糖 120 mg/dL 已記錄
```

### Integration Pattern

When a user sends a health-related message:

1. Call the script with the message text
2. Parse the JSON output to check if data was detected
3. If detected, respond with confirmation (e.g., "收到！69.8 kg 已記錄 📝")
4. If not detected, reply normally without mentioning the skill

## Error Handling

The script includes validation:
- **Out of range values** are ignored (e.g., weight of 500kg won't be recorded)
- **Invalid formats** are silently skipped
- **mcporter failures** are captured and returned in the JSON output

## Resources

### scripts/record_health_data.py

Python script that handles:
- Pattern matching for various health data formats
- Value validation and range checking
- AX3 API calls via mcporter
- JSON output for programmatic integration

The script can be called directly or integrated into message handling workflows.
