# Templates — graduation

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "毕业旅行想去哪？" (Priority 2)
Both missing → "请告诉我出发城市和毕业旅行目的地？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Default: Jun-Aug (grad season)
Missing sort-type → Default: 3 (cheapest)
Missing seat-class-name → Default: economy
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest popular grad destinations: "热门毕业旅行：丽江、成都、厦门、重庆"
- ✅ Note: "毕业季机票紧俏，建议尽早预订"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "graduation",
  "params": { "origin": "", "destination": "", "dep_date": "", "sort_type": "3", "seat_class_name": "economy" },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Graduation Trip Flights: {origin} → {destination}

**Cheapest: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

🎓 **Grad Tip:** 毕业季热门目的地，建议尽早预订！

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Graduation Trip Flights: {origin} → {destination}

No flights found for selected dates.

**Suggestions:**
1. Try flexible dates in Jun-Aug
2. Consider connecting flights
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Graduation Trip Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3`
```
