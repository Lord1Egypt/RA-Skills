# Playbooks — one-way

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **3** (cheapest) |
| journey-type | `--journey-type` | Optional: 1=direct |
| max-price | `--max-price` | Optional: budget cap |
| dep-date-start | `--dep-date-start` | Optional: flexible dates |
| dep-date-end | `--dep-date-end` | Optional: flexible dates |

---

## Playbook A: Cheapest One-Way

**Trigger:** User says "one-way flights", "单程机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

---

## Playbook B: Flexible Date One-Way

**Trigger:** User says "cheapest one-way any day", "单程哪天最便宜".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3
```

---

## Playbook C: Direct One-Way

**Trigger:** User says "direct one-way flight", "单程直飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 8
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} one-way flights"
```
