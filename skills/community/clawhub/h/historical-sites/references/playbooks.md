# Playbooks — historical-sites

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Historical Sites

**Trigger:** "historical places"

```bash
flyai search-poi --city-name "{city}" --category "历史古迹"
```

**Output emphasis:** Historical landmarks.

---

## Playbook B: UNESCO Sites

**Trigger:** "world heritage"

```bash
flyai search-poi --city-name "{city}" --category "人文古迹"
```

**Output emphasis:** Heritage sites.

---

## Playbook C: Ancient Capitals

**Trigger:** "ancient capital history"

```bash
flyai search-poi --city-name "{city}" --category "历史古迹" --poi-level 5
```

**Output emphasis:** Top-rated historical sites.

---

