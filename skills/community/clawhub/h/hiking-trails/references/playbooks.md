# Playbooks — hiking-trails

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Hiking Trails

**Trigger:** "hiking near me"

```bash
flyai search-poi --city-name "{city}" --category "山湖田园" --keyword "徒步"
```

**Output emphasis:** Hiking trails.

---

## Playbook B: Mountain Treks

**Trigger:** "mountain climbing"

```bash
flyai search-poi --city-name "{city}" --category "山湖田园" --poi-level 5
```

**Output emphasis:** Top mountain trails.

---

## Playbook C: Easy Walks

**Trigger:** "easy hike"

```bash
flyai search-poi --city-name "{city}" --category "森林丛林"
```

**Output emphasis:** Gentle nature walks.

---

