---
name: minimax-usage-cn
description: Monitor Minimax Coding Plan usage to stay within API limits. Fetches current usage stats and provides status alerts. Use when checking API quota, monitoring usage, or before running large AI tasks. Shows 5-hour sliding window status.
homepage: https://www.minimaxi.com
metadata:
  openclaw:
    emoji: "📊"
    category: "AI工具"
    requires:
      env:
        - MINIMAX_API_KEY
      bins:
        - curl
    primaryEnv: MINIMAX_API_KEY
---

# Minimax Usage (国内版)

Monitor Minimax Coding Plan usage to stay within API limits.

---

## 目录结构

```
~/.openclaw/workspace/skills/minimax-usage-cn/
├── SKILL.md
└── scripts/
    └── minimax-usage.sh   # Main script
```

---

## 功能

- Check current usage quota
- Monitor 5-hour sliding window
- Get usage alerts before hitting limits

---

## When to Use This Skill

Use this skill whenever:

- User asks to check Minimax usage
- Before running large AI tasks
- When approaching limit warnings

---

## API Specification

**Endpoint:** `GET https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains`

**Headers:**
```
Authorization: Bearer <MINIMAX_API_KEY>
Content-Type: application/json
```

**注意：** 此接口仅适用于国内版 `www.minimaxi.com`。

---

## Response Fields

| 字段 | 含义 | 示例 |
|------|------|------|
| `remains_time` | 订阅周期剩余时间 (秒)，和5小时窗口无关 | 8277752 |
| `current_interval_total_count` | 周期总配额 (固定1500) | 1500 |
| `current_interval_usage_count` | **当前窗口剩余可用次数** | 1263 |
| `model_name` | 模型名称 | MiniMax-M2.5 |
| `start_time` / `end_time | 当前5小时滑动窗口起止时间 (毫秒时间戳) | 1773558000000 |

### 计算公式（重要！）

```python
# ❌ 错误理解
已用 = current_interval_usage_count  # 误以为这是"已用量"

# ✅ 正确理解
剩余 = current_interval_usage_count  # 这是"剩余可用次数"
已用 = current_interval_total_count - current_interval_usage_count
使用率 = (current_interval_total_count - current_interval_usage_count) / current_interval_total_count * 100%
```

**示例**：API 返回 `current_interval_total_count=1500`, `current_interval_usage_count=1263`
- 剩余 = 1263 次
- 已用 = 1500 - 1263 = **237 次**
- 使用率 = 237 / 1500 = **15.8%**

### 状态阈值

| 剩余量 | 使用率 | 状态 |
|--------|--------|------|
| >600 | <60% | 💚 GREEN |
| 375-600 | 60-75% | ⚠️ CAUTION |
| 150-375 | 75-90% | ⚠️ WARNING |
| <150 | >90% | 🚨 CRITICAL |

---

## Output Format

```
🔍 Checking Minimax Coding Plan usage...
✅ Usage retrieved successfully:

📊 Coding Plan Status (MiniMax-M2.5):
   Used:      102 / 1500 prompts (6%)
   Remaining: 1398 prompts
   Window:    20:00 - 00:00 (UTC+8)
   Resets in: 约 1h 13m

💚 GREEN: 6% used. Plenty of buffer.
```

### JSON Output Mode

For programmatic use, add `--json` or `-j` flag:

```bash
./minimax-usage.sh --json
```

Output:
```json
{
  "status": "GREEN",
  "used": 102,
  "total": 1500,
  "remaining": 1398,
  "percent": 6,
  "model": "MiniMax-M2.5",
  "window_start": "20:00",
  "window_end": "00:00",
  "resets_in_seconds": 4380
}
```

### Cron 定时检查

添加到 crontab 每小时检查一次：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每小时检查并记录）
0 * * * * cd /home/rocfly/.openclaw/workspace/skills/minimax-usage-cn/scripts && ./minimax-usage.sh >> /home/rocfly/.openclaw/workspace/logs/minimax-usage.log 2>&1

# 或者带通知（需要配置邮件或 webhook）
0 * * * * cd /home/rocfly/.openclaw/workspace/skills/minimax-usage-cn/scripts && ./minimax-usage.sh --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data['percent'] > 75:
    print(f'⚠️ ALERT: {data[\"percent\"]}% used!')
    # 在此添加 webhook 通知
"
```

### 常见使用场景

| 场景 | 命令 |
|------|------|
| 手动检查用量 | `./minimax-usage.sh` |
| 静默检查（无输出） | `./minimax-usage.sh -q` |
| JSON 格式输出 | `./minimax-usage.sh --json` |
| 配合 cron 记录 | `./minimax-usage.sh >> usage.log` |

---

## Status Thresholds

| 使用率 | 状态 | 提示 |
|--------|------|------|
| 0-60% | 💚 GREEN | Plenty of buffer |
| 60-75% | ⚠️ CAUTION | Target is 60% |
| 75-90% | ⚠️ WARNING | Approaching limit |
| >90% | 🚨 CRITICAL | Stop all AI work |

---

## Notes

- 需要使用 Coding Plan API Key, 专用于 Coding Plan 套餐
- Coding Plan 用量每5小时重置
- 一个 prompt 约等于 15 次模型调用
- `current_interval_usage_count` 是**剩余用量**，不是已用量！
- 窗口时间为 UTC+8 时区

---

## Error Handling

| 错误码 | 含义 | 解决方法 |
|--------|------|----------|
| 2013 | 参数错误 | 请检查请求参数 |
| 1004 | 未授权/Token 不匹配 | 请检查 API Key |
| 2049 | 无效的 API Key | 请检查 API Key |
| 1002 | 请求频率超限 | 请稍后再试 |
| 2056 | 超出 Coding Plan 资源限制 | 请等待下一个时间段资源释放后，再次尝试 |
| 1000/1024/1033 | 系统错误/内部错误 | 请稍后再试 |
