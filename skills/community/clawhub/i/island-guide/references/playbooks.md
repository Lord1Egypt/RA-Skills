# Playbooks — beach-island-guide

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Beaches

**Trigger:** "best beaches"

```bash
flyai search-poi --city-name "{city}" --category "沙滩海岛"
```

**Output emphasis:** Beach and island attractions.

---

## Playbook B: Snorkeling Spots

**Trigger:** "snorkeling"

```bash
flyai search-poi --city-name "{city}" --keyword "浮潜"
```

**Output emphasis:** Snorkeling destinations.

---

## Playbook C: Family Beach

**Trigger:** "beach for kids"

```bash
flyai search-poi --city-name "{city}" --category "沙滩海岛" --poi-level 5
```

**Output emphasis:** Family-friendly beaches.

---

