# Playbooks — early-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: First Flight Out

**Trigger:** "earliest", "最早"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 5 --dep-hour-end 9 --sort-type 6
```

**Output emphasis:** Show 5-9 AM flights, earliest first.

---

## Playbook B: Early + Cheap

**Trigger:** "cheapest morning flight"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 5 --dep-hour-end 9 --sort-type 3
```

**Output emphasis:** Morning flights sorted by price.

---

## Playbook C: Before Meeting

**Trigger:** "arrive by 10am", "10点前到"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 5 --dep-hour-end 7 --sort-type 6
```

**Output emphasis:** Ultra-early to arrive before 10am for business.

---

