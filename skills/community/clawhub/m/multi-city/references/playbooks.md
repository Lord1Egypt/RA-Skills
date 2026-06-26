# Playbooks — multi-city

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** per leg |
| transfer-city  journey-type | `--journey-type` | Optional: 1=direct per leg |

---

## Playbook A: Standard Multi-City (3 cities)

**Trigger:** User says "multi-city flights", "多程航班" with 3 cities.

```bash
flyai search-flight --origin "{city_a}" --destination "{city_b}" --dep-date {date1} --sort-type 2
flyai search-flight --origin "{city_b}" --destination "{city_c}" --dep-date {date2} --sort-type 2
flyai search-flight --origin "{city_c}" --destination "{city_a}" --dep-date {date3} --sort-type 2
```

---

## Playbook B: Open-Jaw (fly A→B, return C→A)

**Trigger:** User says "open-jaw flight", "开口航班".

```bash
flyai search-flight --origin "{city_a}" --destination "{city_b}" --dep-date {date1} --sort-type 2
flyai search-flight --origin "{city_c}" --destination "{city_a}" --dep-date {date2} --sort-type 2
```

---

## Playbook C: Stopover City

**Trigger:** User says "flight with stopover in X", "X中转停留".

```bash
flyai search-flight --origin "{city_a}" --destination "{city_c}" --dep-date {date} --sort-type 2
```

---

## Playbook D: Keyword Fallback

**Trigger:** Complex route not directly supported.

```bash
flyai keyword-search --query "{city_a} to {city_b} to {city_c} multi-city flights"
```
