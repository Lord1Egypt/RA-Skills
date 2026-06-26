# Playbooks — island-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| journey-type | `--journey-type` | Default: **1** (direct) |
| sort-type | `--sort-type` | Default: **2** (recommended) |

---

## Playbook A: Recommended Island Route

**Trigger:** User says "fly to island", "海岛航班", "海岛机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights to island destinations.

---

## Playbook B: Budget Island Getaway

**Trigger:** User says "cheap island flight", "便宜海岛机票", "特价海岛".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Output:** Cheapest flights to island within date range.

---

## Playbook C: Connecting Island Route

**Trigger:** User says "connecting flight to island", "中转海岛", "转机海岛".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --sort-type 2
```

**Output:** Connecting flights for islands without direct service.

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} island flights"
```

**Output:** Broader search + keyword fallback.
