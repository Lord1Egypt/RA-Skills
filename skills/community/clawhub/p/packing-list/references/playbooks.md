# Playbooks — packing-list

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: General Packing

**Trigger:** "what to pack"

```bash
flyai keyword-search --query "旅行清单 {dest}"
```

**Output emphasis:** General packing suggestions.

---

## Playbook B: Beach Packing

**Trigger:** "beach trip packing"

```bash
flyai keyword-search --query "海边旅行清单"
```

**Output emphasis:** Beach-specific packing list.

---

## Playbook C: Winter Packing

**Trigger:** "cold weather packing"

```bash
flyai keyword-search --query "冬季旅行清单"
```

**Output emphasis:** Cold weather essentials.

---

