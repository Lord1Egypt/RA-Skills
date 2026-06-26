# Playbooks — pool-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Pool Hotel

**Trigger:** "hotel with pool", "有泳池"

```bash
flyai search-hotel --dest-name "{city}" --key-words "泳池" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels with swimming pools.

---

## Playbook B: Infinity Pool

**Trigger:** "infinity pool"

```bash
flyai search-hotel --dest-name "{city}" --key-words "无边泳池" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Resorts with infinity pools.

---

## Playbook C: Indoor Pool

**Trigger:** "indoor pool", "室内泳池"

```bash
flyai search-hotel --dest-name "{city}" --key-words "室内泳池" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Year-round swimming options.

---

