# Templates — multi-city

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Collect route segments
```
Missing cities → "请告诉我您的行程路线，例如：北京→上海→成都→北京"
Missing dates → "每段行程的出发日期分别是？"
```

### Round 2: Confirm route
```
→ "确认行程：{city_a}→{city_b} ({date1})，{city_b}→{city_c} ({date2})，搜索中..."
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Must collect ≥2 legs before searching
- ✅ Warn about minimum connection time: "建议两段之间预留至少3小时"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "multi-city",
  "params": {
    "legs": [
      {"origin": "", "destination": "", "dep_date": ""},
      {"origin": "", "destination": "", "dep_date": ""}
    ],
    "sort_type": "2"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result (multi-leg itinerary)

```markdown
## ✈️ Multi-City Itinerary

### Leg 1: {city_a} → {city_b} ({date1})
| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

### Leg 2: {city_b} → {city_c} ({date2})
| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

### Leg 3: {city_c} → {city_a} ({date3})
| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

**Total: {N} flights · Est. ¥{total}+**

📌 **Note:** Each leg is booked separately. Allow ≥3h between connections.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results (one leg)

```markdown
## ✈️ Multi-City Itinerary — Leg {N} Issue

No flights found for {city_x} → {city_y} on {date}.

**Suggestions:**
1. Try ±3 days for this leg
2. Consider nearby airports
3. Try connecting flights for this leg
```

### 3.3 CLI Failed

```markdown
## ✈️ Multi-City Itinerary

⚠️ Could not retrieve data for Leg {N}: {error}

**Next steps:**
- Retry the failed leg
- Check network: `flyai --version`

Real-time data requires a working flyai-cli.
```
