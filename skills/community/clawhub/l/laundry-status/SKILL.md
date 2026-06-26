---
name: laundry-status
description: Use when the user wants to check washing machine or dryer status, laundry room availability, or which machines are free at Shanghai Jiao Tong University Minhang campus.
version: 1.0.0
metadata:
  openclaw:
    emoji: "👕"
    triggers:
      - 洗衣机
      - 洗衣房
      - washer
      - dryer
      - laundry
      - 空闲机器
      - 有没有空的
      - 洗衣机状态
      - 楼下洗衣机
    tags:
      - iot
      - smart-home
      - laundry
      - haier
      - sjtu
---

# laundry-status

## Overview

Query real-time status of Haier IoT washing machines and dryers at SJTU Minhang campus.

## When to Use

Invoke this skill when the user asks about:
- Washing machine or dryer availability
- Whether any machines are free
- Laundry room status for a specific building
- When machines will finish (estimated completion time)

## How to Use

**Default building (西21楼):**

```
python3 {skill_dir}/laundry_status.py
```

**Specific building:**

```
python3 {skill_dir}/laundry_status.py --building 西16楼
```

**All buildings:**

```
python3 {skill_dir}/laundry_status.py --all
```

## Output Interpretation

Each machine is grouped by status label:

| Status | Meaning |
|--------|---------|
| 空闲 (Idle) | Machine is available — tell the user to go use it now |
| 使用中 (In Use) | Machine is running; an estimated finish time may be shown as `[预计HH:MM结束]` |
| 故障 (Fault) | Machine is broken and cannot be used |
| 离线 (Offline) | Machine is unreachable or powered off |

Machines are listed in priority order: 空闲 first, then 使用中 (with finish times), then 故障 and 离线.

## Available Buildings

| Building Name | ID |
|---------------|----|
| 西21楼 | 27131 |
| 西16楼 | 27136 |

Use the building name (e.g. `--building 西16楼`) or ID (e.g. `--building 27136`). If the user does not specify a building, default to **西21楼**.

## Error Handling

- **Network timeout or failure**: The script exits with a message to stderr. Tell the user the request timed out and to check their network connection.
- **Unknown building**: The script reports the invalid name and lists valid buildings. Tell the user the building was not found and offer the available options.
- **API error**: The script reports the API error message. Tell the user the service returned an error and to try again later.
