# Templates — one-way

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
Missing dep-date → Default: tomorrow. Tell user: "默认查明天的单程航班"
Missing sort-type → Default: 3 (cheapest first)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about return date — one-way means no return
- ✅ If user mentions return needs → redirect to round-trip skill

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "one-way",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "sort_type": "3"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ One-Way Flights: {origin} → {destination}

**Cheapest: ¥{price} on {airline}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | Type | 📎 Book |
|---|--------|---------|---------|----------|----------|------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {type} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {type} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {type} | [Book]({detailUrl}) |

📌 **One-way only** — no return ticket included.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ One-Way Flights: {origin} → {destination}

No one-way flights found for {date}.

**Suggestions:**
1. Try flexible dates (±3 days)
2. Check nearby airports
3. Consider connecting flights
```

### 3.3 CLI Failed

```markdown
## ✈️ One-Way Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3`

Real-time data requires a working flyai-cli.
```
