# Playbooks — photo-spots

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Landmarks

**Trigger:** "photo spots"

```bash
flyai search-poi --city-name "{city}" --category "地标建筑"
```

**Output emphasis:** Iconic landmarks and viewpoints.

---

## Playbook B: City Walks

**Trigger:** "instagrammable places"

```bash
flyai search-poi --city-name "{city}" --category "城市观光"
```

**Output emphasis:** City observation and walking spots.

---

## Playbook C: Art Districts

**Trigger:** "art district photos"

```bash
flyai search-poi --city-name "{city}" --category "文创街区"
```

**Output emphasis:** Creative and art districts.

---

