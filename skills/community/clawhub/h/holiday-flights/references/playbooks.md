# Playbooks — holiday-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Spring Festival

**Trigger:** "春节回家", "CNY flight"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {cny_start} --sort-type 3
flyai search-flight --origin "{d}" --destination "{o}" --dep-date {cny_end} --sort-type 3
```

**Output emphasis:** Warn: prices 50-200% higher. Book 1-2 months ahead.

---

## Playbook B: Golden Week

**Trigger:** "国庆出游"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start 2026-09-28 --dep-date-end 2026-10-03 --sort-type 3
```

**Output emphasis:** Suggest departing 1-2 days early to save 30-50%.

---

## Playbook C: Labor Day / Dragon Boat

**Trigger:** "五一/端午"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {holiday_start} --back-date {holiday_end} --sort-type 3
```

**Output emphasis:** 3-day mini-holidays. Book 2-3 weeks ahead.

---

## Playbook D: Anti-Peak Strategy

**Trigger:** "避开高峰"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {holiday_start+2} --sort-type 3
```

**Output emphasis:** Search offset dates — depart 2 days after holiday starts for 40-60% savings.

---

