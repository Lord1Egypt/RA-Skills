# Playbooks — pet-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Pet Hotel

**Trigger:** "pet-friendly hotel", "可以带狗"

```bash
flyai search-hotel --dest-name "{city}" --key-words "宠物友好" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels accepting pets.

---

## Playbook B: Pet + Park Nearby

**Trigger:** "带宠物住有公园"

```bash
flyai search-hotel --dest-name "{city}" --key-words "宠物" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Pet-friendly with nearby green space.

---

## Playbook C: Budget Pet Stay

**Trigger:** "便宜的宠物酒店"

```bash
flyai search-hotel --dest-name "{city}" --key-words "宠物友好" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Affordable pet-friendly options.

---

