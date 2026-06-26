# Playbooks — group-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | Optional: 1=direct (preferred for groups) |
| seat-class-name | `--seat-class-name` | Optional: economy/business/first |
| max-price | `--max-price` | Optional: per-ticket budget cap |

---

## Playbook A: Recommended Group Flight

**Trigger:** User says "group flights", "团队机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Best recommended flights for group travel.

---

## Playbook B: Cheapest Group Flight

**Trigger:** User says "cheapest group tickets", "最便宜的团队票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Flights sorted by lowest per-ticket price.

---

## Playbook C: Direct Group Flight

**Trigger:** User says "direct group flight", "直飞团队机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 8
```

**Output:** Direct flights only — reduces coordination risk for large groups.

---

## Playbook D: Broad Search (no suitable flights)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} group flights discount"
```

**Output:** Broader search + keyword fallback.
