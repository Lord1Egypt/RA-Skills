# Playbooks — hot-springs

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Hot Springs

**Trigger:** "hot springs near me"

```bash
flyai search-poi --city-name "{city}" --category "温泉"
```

**Output emphasis:** Hot spring attractions.

---

## Playbook B: Top Hot Springs

**Trigger:** "best onsen"

```bash
flyai search-poi --city-name "{city}" --category "温泉" --poi-level 5
```

**Output emphasis:** Top-rated hot springs.

---

## Playbook C: Natural Springs

**Trigger:** "natural hot spring"

```bash
flyai search-poi --city-name "{city}" --keyword "天然温泉"
```

**Output emphasis:** Natural thermal springs.

---

