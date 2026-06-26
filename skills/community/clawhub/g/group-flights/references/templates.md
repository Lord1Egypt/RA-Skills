# Templates — group-flights

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
Missing dep-date → Default: next week. Tell user: "默认查下周的团队航班"
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: direct preferred for groups
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about passenger count — CLI does not support it; count is handled at booking
- ✅ Mention group booking tip: "建议尽早预订同一航班，热门航线座位有限"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "group-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "sort_type": "2"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Group Flights: {origin} → {destination}

**Recommended: ¥{price}/person on {airline} ({aircraft_type})**

| # | Flight | Departs | Arrives | Duration | 💰 Price/person | Aircraft | 📎 Book |
|---|--------|---------|---------|----------|----------------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {aircraft} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {aircraft} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {aircraft} | [Book]({detailUrl}) |

💡 **Group Tip:** Wide-body aircraft (A330/B777/B787) have more seats per flight — ideal for 10+ passengers.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Group Flights: {origin} → {destination}

No flights found for {date}.

**Tried:**
- ✅ Searched with sort-type=recommended → 0 results
- ✅ Removed sort filter → {count} flights available

**Suggestions:**
1. Try flexible dates (±3 days)
2. Consider connecting flights
3. Split group across nearby departure times
```

### 3.3 CLI Failed

```markdown
## ✈️ Group Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
