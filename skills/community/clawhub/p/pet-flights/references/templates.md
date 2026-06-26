# Templates — pet-flights

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
Missing dep-date → Default: next week. Tell user: "默认查下周的航班"
Missing journey-type → Default: direct preferred for pet travel
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Mention pet policy tip: "建议出发前确认航空公司的宠物托运/随身政策"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "pet-flights",
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
## ✈️ Pet-Friendly Flights: {origin} → {destination}

**Recommended: ¥{price} on {airline} — {duration}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | Type | 📎 Book |
|---|--------|---------|---------|----------|----------|------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | Direct | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | Direct | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | 1-stop | [Book]({detailUrl}) |

🐾 **Pet Tip:** Confirm airline pet policy (cargo/cabin) before booking. Direct flights reduce transfer stress.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Pet-Friendly Flights: {origin} → {destination}

No flights found for {date}.

**Tried:**
- ✅ Searched with sort-type=recommended → 0 results
- ✅ Removed filters → {count} flights available

**Suggestions:**
1. Try flexible dates (±3 days)
2. Consider connecting flights
3. Check nearby departure airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Pet-Friendly Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
