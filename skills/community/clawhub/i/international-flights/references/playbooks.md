# Playbooks — international-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Flight + Visa

**Trigger:** "fly to Japan", "去日本"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{country} visa requirements"
```

**Output emphasis:** Show flights + visa info together.

---

## Playbook B: Cheapest Entry Point

**Trigger:** "cheapest way to Europe"

```bash
flyai search-flight --origin "{o}" --destination "London" --dep-date {date} --sort-type 3
flyai search-flight --origin "{o}" --destination "Paris" --dep-date {date} --sort-type 3
flyai search-flight --origin "{o}" --destination "Frankfurt" --dep-date {date} --sort-type 3
```

**Output emphasis:** Compare entry cities, recommend cheapest.

---

## Playbook C: Transit Visa Check

**Trigger:** "do I need transit visa"

```bash
flyai keyword-search --query "transit visa {country}"
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 8
```

**Output emphasis:** Check transit visa + show direct flights to avoid transit issues.

---

