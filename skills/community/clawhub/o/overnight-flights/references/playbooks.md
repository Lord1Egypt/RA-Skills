# Playbooks — overnight-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Pure Red-Eye

**Trigger:** "cheapest night flight"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --sort-type 3
```

**Output emphasis:** Night flights only, cheapest first.

---

## Playbook B: Day vs Night Compare

**Trigger:** "how much cheaper at night"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --sort-type 3
```

**Output emphasis:** Show savings: night vs day.

---

## Playbook C: Red-Eye + Direct

**Trigger:** "direct night flight"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --journey-type 1 --sort-type 3
```

**Output emphasis:** Direct red-eye flights only.

---

