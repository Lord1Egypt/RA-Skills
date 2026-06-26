# Templates — island-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞往哪个海岛？" (Priority 2)
Both missing → "请告诉我出发城市和目的地海岛？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "哪天出发？"
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: 1 (direct — prefer non-stop to islands)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest popular island destinations: "热门海岛：三亚、厦门、普吉岛、巴厘岛"
- ✅ Note transfer requirements: "部分海岛需中转，或到达后乘船前往"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "island-flight",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "journey_type": "1",
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
## ✈️ Island Flights: {origin} → {destination}

**Best island route: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | Type | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | Direct | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | Connect | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | Direct | ¥{price} | [Book]({detailUrl}) |

🏝️ **Island Tip:** {island_transfer_note}

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Island Flights: {origin} → {destination}

No flights found for this island route.

**Suggestions:**
1. Try connecting flights via nearest major hub
2. Check nearby airports on the mainland
3. Consider ferry + flight combination
```

### 3.3 CLI Failed

```markdown
## ✈️ Island Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
