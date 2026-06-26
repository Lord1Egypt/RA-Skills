# Playbooks — graduation

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| seat-class-name | `--seat-class-name` | Default: **economy** |
| sort-type | `--sort-type` | Default: **3** (cheapest) |

---

## Playbook A: Grad Season Budget Trip

**Trigger:** User says "graduation flight", "毕业航班", "毕业旅行".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {jun_start} --dep-date-end {aug_end} --seat-class-name economy --sort-type 3
```

---

## Playbook B: Class Trip Group Search

**Trigger:** User says "class trip", "同学旅行", "班级出游".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --sort-type 2
```

---

## Playbook C: Flexible Date Grad Trip

**Trigger:** User says "flexible grad trip", "毕业旅行随便哪天".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} graduation flights"
```
