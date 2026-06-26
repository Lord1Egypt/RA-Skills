# Playbooks — military-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | Optional: 1=direct |
| max-price | `--max-price` | Optional: budget cap |

---

## Playbook A: Recommended Military Flight

**Trigger:** User says "military flights", "军人机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

---

## Playbook B: Cheapest Military Fare

**Trigger:** User says "cheapest military fare", "最便宜军人票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

---

## Playbook C: Direct Military Flight

**Trigger:** User says "direct military flight", "军人直飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 8
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} military discount flights"
```
