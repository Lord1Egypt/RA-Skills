# Playbooks — trip-planner

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Full Plan

**Trigger:** "plan my trip", "帮我规划行程"

```bash
flyai keyword-search --query "{dest} visa"
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {day1} --sort-type 3
flyai search-flight --origin "{d}" --destination "{o}" --dep-date {dayN} --sort-type 3
flyai search-hotel --dest-name "{city}" --check-in-date {day1} --check-out-date {dayN} --sort rate_desc
flyai search-poi --city-name "{city}" --poi-level 5
```

**Output emphasis:** Complete itinerary with all components.

---

## Playbook B: Quick Plan

**Trigger:** "plan a quick trip"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {day1} --sort-type 3
flyai search-hotel --dest-name "{city}" --sort rate_desc --check-in-date {day1} --check-out-date {dayN}
flyai search-poi --city-name "{city}" --poi-level 5
```

**Output emphasis:** Skip visa, focus on core booking.

---

## Playbook C: Budget Plan

**Trigger:** "plan cheap trip"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {day1} --sort-type 3
flyai search-hotel --dest-name "{city}" --sort price_asc --max-price 300 --check-in-date {day1} --check-out-date {dayN}
flyai search-poi --city-name "{city}" --poi-level 5
```

**Output emphasis:** All budget-oriented selections.

---

