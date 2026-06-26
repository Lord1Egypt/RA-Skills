# Playbooks — private-car

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Day Tour

**Trigger:** "private car tour"

```bash
flyai keyword-search --query "包车一日游 {city}"
```

**Output emphasis:** Full-day private car tour.

---

## Playbook B: Half Day

**Trigger:** "half day car"

```bash
flyai keyword-search --query "包车半日游 {city}"
```

**Output emphasis:** Half-day private car.

---

## Playbook C: Multi-Day

**Trigger:** "multi-day driver"

```bash
flyai keyword-search --query "包车多日游 {city}"
```

**Output emphasis:** Multi-day with driver.

---

