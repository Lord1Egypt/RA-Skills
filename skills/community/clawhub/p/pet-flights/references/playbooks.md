# Playbooks — pet-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | Optional: 1=direct (preferred for pets) |
| dep-hour-start | `--dep-hour-start` | Optional: morning flights preferred |
| dep-hour-end | `--dep-hour-end` | Optional: avoid late-night for pets |

---

## Playbook A: Recommended Pet-Friendly Flight

**Trigger:** User says "pet flights", "宠物航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended flights (direct preferred for pet travel).

---

## Playbook B: Shortest Pet Flight

**Trigger:** User says "shortest flight for pet", "宠物最短航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 4
```

**Output:** Flights sorted by shortest duration — minimizes pet travel time.

---

## Playbook C: Direct-Only Pet Flight

**Trigger:** User says "direct flight with pet", "带宠物直飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 8
```

**Output:** Direct flights only — no transfers, less stress for pets.

---

## Playbook D: Broad Search (no pet-friendly flights)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} pet friendly flights"
```

**Output:** Broader search + keyword fallback.
