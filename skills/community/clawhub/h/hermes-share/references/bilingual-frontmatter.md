# Bilingual Skill Frontmatter Convention

Established 2026-05-11 during `hermes-share` v1.1.0 development.

---

## The Convention

Every SKILL.md **may** include an `ar_description` field in its YAML frontmatter alongside the standard `description`:

```yaml
---
name: my-skill
description: End-to-end Python data analysis pipeline for survey data — cleaning, EDA, visualization, statistical testing.
ar_description: خط أنابيب تحليل بيانات بايثون متكامل لبيانات الاستبيانات — تنظيف، تحليل استكشافي، رسوم بيانية، اختبارات إحصائية.
version: 1.0.0
---
```

---

## Rules

| Rule | Detail |
|------|--------|
| **English always** | `description` must exist and be in English — this is what ClawHub and skill_search use |
| **Arabic optional** | `ar_description` is optional. If absent, tools show a placeholder message |
| **Length** | Arabic: 2-4 lines (30-60 words). English: whatever's needed for clarity |
| **Content** | Answer: what does this skill do, when to use it, top capability |
| **Not auto-translated** | Arabic is human/AI-written, not machine-translated from English |

---

## Consumers

### `pack_skills.py` (hermes-share)

The script reads both fields:

```python
frontmatter = parse_yaml_frontmatter(skill_md)
info["description_en"] = frontmatter.get("description", "")
info["description_ar"] = frontmatter.get("ar_description", "")
```

If `ar_description` is missing, the generated `SKILLS_README.txt` shows:
```
(لم يتم توفير شرح بالعربية بعد — يمكن طلبه من المُرسِل)
Arabic description not yet provided — you can request it from the sender.
```

### Hermes Share Agent Workflow

When sharing a skill, the agent should:
1. Read the skill's SKILL.md
2. If `ar_description` is missing → generate one (2-4 Arabic lines)
3. Write it into the generated `SKILLS_README.txt` before sending
4. Optionally: patch the skill's own SKILL.md to add `ar_description` permanently

---

## Adoption Status

| Skill | Has `ar_description`? |
|-------|----------------------|
| `hermes-share` (v1.1.0) | ✅ Yes |
| All 224 other skills | ❌ Not yet |

Adding `ar_description` to skills is a background task — do it opportunistically when a skill is loaded or shared, not as a bulk operation.