# Playbooks — museum-guide

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Museums

**Trigger:** "museums near me"

```bash
flyai search-poi --city-name "{city}" --category "博物馆"
```

**Output emphasis:** All museums.

---

## Playbook B: Art Galleries

**Trigger:** "art gallery"

```bash
flyai search-poi --city-name "{city}" --category "展览馆"
```

**Output emphasis:** Exhibition halls and galleries.

---

## Playbook C: Memorial Halls

**Trigger:** "memorial"

```bash
flyai search-poi --city-name "{city}" --category "纪念馆"
```

**Output emphasis:** Memorial halls and monuments.

---

