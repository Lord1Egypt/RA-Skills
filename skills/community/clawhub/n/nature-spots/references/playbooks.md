# Playbooks — nature-spots

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Nature Scenery

**Trigger:** "nature spots"

```bash
flyai search-poi --city-name "{city}" --category "自然风光"
```

**Output emphasis:** Natural scenic areas.

---

## Playbook B: Mountains

**Trigger:** "mountain hiking"

```bash
flyai search-poi --city-name "{city}" --category "山湖田园"
```

**Output emphasis:** Mountain and lake scenery.

---

## Playbook C: Top Nature

**Trigger:** "best nature in China"

```bash
flyai search-poi --city-name "{city}" --category "自然风光" --poi-level 5
```

**Output emphasis:** Top-rated natural sites.

---

