# Playbooks — luxury-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: 5-Star Best Rated

**Trigger:** "best luxury hotel"

```bash
flyai search-hotel --dest-name "{city}" --hotel-stars 5 --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Top-rated 5-star hotels.

---

## Playbook B: Luxury Suite

**Trigger:** "presidential suite", "总统套房"

```bash
flyai search-hotel --dest-name "{city}" --hotel-stars 5 --key-words "套房" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Suite-level luxury.

---

## Playbook C: Luxury + Spa

**Trigger:** "spa hotel", "带SPA"

```bash
flyai search-hotel --dest-name "{city}" --hotel-stars 5 --key-words "SPA" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** 5-star with spa facilities.

---

