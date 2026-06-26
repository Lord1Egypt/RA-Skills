# Templates — mountain-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞往哪个山区/高原城市？" (Priority 2)
Both missing → "请告诉我出发城市和目的地山区？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "哪天出发？"
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: none (show all)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest popular mountain destinations: "热门山区：丽江、九寨沟、拉萨、昆明"
- ✅ Warn about altitude: "高原目的地请注意高反风险，建议提前适应"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "mountain-flight",
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
## ✈️ Mountain Flights: {origin} → {destination}

**Best mountain route: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

🏔️ **Altitude Note:** {altitude_warning}

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Mountain Flights: {origin} → {destination}

No flights found for this mountain route.

**Suggestions:**
1. Try connecting flights via nearest major hub
2. Check nearby airports
3. Consider train + flight combination
```

### 3.3 CLI Failed

```markdown
## ✈️ Mountain Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
