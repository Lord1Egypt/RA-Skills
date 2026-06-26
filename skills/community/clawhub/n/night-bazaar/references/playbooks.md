# Playbooks — night-market

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Night Markets

**Trigger:** "night market"

```bash
flyai search-poi --city-name "{city}" --category "市集" --keyword "夜市"
```

**Output emphasis:** Night markets and food streets.

---

## Playbook B: Food Streets

**Trigger:** "food street"

```bash
flyai search-poi --city-name "{city}" --category "市集"
```

**Output emphasis:** Local food markets.

---

## Playbook C: Snack Street

**Trigger:** "street food"

```bash
flyai search-poi --city-name "{city}" --keyword "小吃街"
```

**Output emphasis:** Street food hotspots.

---

