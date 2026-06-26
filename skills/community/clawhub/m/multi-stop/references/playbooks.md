# Playbooks — multi-stop

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Sequential Multi-City

**Trigger:** "A to B to C"

```bash
flyai search-flight --origin "{cityA}" --destination "{cityB}" --dep-date {day1} --sort-type 3
flyai search-flight --origin "{cityB}" --destination "{cityC}" --dep-date {day2} --sort-type 3
flyai search-flight --origin "{cityC}" --destination "{cityD}" --dep-date {day3} --sort-type 3
```

**Output emphasis:** Search each leg, show combined total cost.

---

## Playbook B: Open-Jaw

**Trigger:** "fly into A, out of C"

```bash
flyai search-flight --origin "{home}" --destination "{cityA}" --dep-date {day1} --sort-type 3
flyai search-flight --origin "{cityC}" --destination "{home}" --dep-date {dayN} --sort-type 3
```

**Output emphasis:** Outbound to first city, return from last city.

---

## Playbook C: Cheapest Hub

**Trigger:** "cheapest way to visit 3 cities"

```bash
# Search each permutation of city order
# Compare total cost across different sequences
```

**Output emphasis:** Optimize city visit order by total flight cost.

---

