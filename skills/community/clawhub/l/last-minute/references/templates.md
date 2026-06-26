# Templates — last-minute

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞到哪里？" (Priority 2)
Both missing → "您从哪个城市出发，飞到哪里？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Default: today. Tell user: "默认查今天的临期航班"
Missing dep-hour-start → Default: current hour + 1
Missing sort-type → Default: 6 (earliest departure)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about departure time — last-minute implies ASAP
- ✅ Always emphasize urgency in confirmation: "正在搜索X小时内起飞的航班..."

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "last-minute",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "today",
    "dep_hour_start": "now+1",
    "sort_type": "6"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Last Minute Flights: {origin} → {destination}

**Soonest: {airline} departs {dep_time} (in {hours_away}h) — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | ⏰ Status | 📎 Book |
|---|--------|---------|---------|----------|----------|-----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {X}h away | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {X}h away | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {X}h away | [Book]({detailUrl}) |

⚠️ **Last-minute inventory changes fast — book now before seats sell out.**

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Last Minute Flights: {origin} → {destination}

No flights found for today.

**Tried:**
- ✅ Searched same-day with hour filter → 0 results
- ✅ Expanded to tomorrow → {count} flights available

**Suggestions:**
1. Try tomorrow morning (6:00-12:00)
2. Check nearby airports
3. Expand to 3-day window
```

### 3.3 CLI Failed

```markdown
## ✈️ Last Minute Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 6`

Real-time data requires a working flyai-cli.
```
