# Playbooks — mountain-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| dep-date-start/end | `--dep-date-start/end` | Ski season window |

---

## Playbook A: Recommended Mountain Route

**Trigger:** User says "fly to mountains", "山区航班", "山区机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended flights to mountain destinations.

---

## Playbook B: Ski Season Flight

**Trigger:** User says "ski resort flight", "滑雪航班", "雪场机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {ski_start} --dep-date-end {ski_end} --sort-type 3
```

**Output:** Cheapest flights during ski season window.

---

## Playbook C: Highland City Direct

**Trigger:** User says "direct flight to highland", "高原直飞", "高海拔直飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights to highland cities.

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} mountain flights"
```

**Output:** Broader search + keyword fallback.
