# Playbooks — infant-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| dep-hour-start | `--dep-hour-start` | Default: **6** |
| dep-hour-end | `--dep-hour-end` | Default: **20** |
| sort-type | `--sort-type` | Default: **4** (shortest duration) |
| journey-type | `--journey-type` | Optional: 1=direct (strongly preferred) |

---

## Playbook A: Shortest Infant-Friendly Flight

**Trigger:** User says "infant flights", "婴儿机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 20 --sort-type 4
```

**Output:** Shortest duration flights within comfortable hours.

---

## Playbook B: Direct-Only Infant Flight

**Trigger:** User says "direct flight with baby", "带宝宝直飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 20 --journey-type 1 --sort-type 8
```

**Output:** Direct flights only — no transfers with infant.

---

## Playbook C: Cheapest Infant Flight

**Trigger:** User says "cheapest baby ticket", "最便宜婴儿票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Cheapest fares (no hour filter for maximum options).

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} infant flights"
```

**Output:** Broader search + keyword fallback.
