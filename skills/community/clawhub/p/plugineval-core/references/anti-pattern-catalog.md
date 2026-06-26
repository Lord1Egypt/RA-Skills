# Anti-Pattern Catalog

## Overview

Anti-patterns reduce skill quality and user trust. Each has a penalty applied to the final score.

---

## OVER_CONSTRAINED

**Penalty:** 10%

**Description:** Skill has too many MUST/ALWAYS/NEVER directives, limiting flexibility.

**Detection:** Count directives: MUST, ALWAYS, NEVER, REQUIRED, MANDATORY

**Threshold:** >15 directives

**Auto-fixable:** ❌ No (needs manual review)

**Fix:** Review directives, keep only critical ones, use SHOULD/RECOMMENDED instead.

---

## EMPTY_DESCRIPTION

**Penalty:** 10-50%

**Description:** Description is too short or missing.

**Detection:** Check frontmatter description length

**Thresholds:**
- Missing: 50% penalty
- <20 chars: 30% penalty
- <50 chars: 10% penalty

**Auto-fixable:** ✅ Yes

**Fix:** Generate description from skill content (first paragraph).

---

## MISSING_TRIGGER

**Penalty:** 15%

**Description:** No trigger phrase ("Use when...") to tell users when to invoke the skill.

**Detection:** Check for "Use when", "Trigger", "Call when"

**Auto-fixable:** ✅ Yes

**Fix:** Add "Use when" section with trigger conditions.

---

## BLOATED_SKILL

**Penalty:** 10%

**Description:** Skill is too large without using references/ folder.

**Detection:** Count lines in SKILL.md

**Threshold:** >800 lines without references/

**Auto-fixable:** ❌ No (needs restructuring)

**Fix:** Move details to references/, keep SKILL.md concise.

---

## ORPHAN_REFERENCE

**Penalty:** 5%

**Description:** Reference files exist but are empty or unused.

**Detection:** Check files in references/

**Auto-fixable:** ✅ Yes

**Fix:** Remove empty reference files.

---

## DEAD_CROSS_REF

**Penalty:** 5%

**Description:** References to non-existent skills or files.

**Detection:** Check markdown links

**Auto-fixable:** ❌ No (needs verification)

**Fix:** Verify and fix broken links.

---

## Summary Table

| Pattern | Penalty | Auto-fix | Priority |
|---------|---------|----------|----------|
| OVER_CONSTRAINED | 10% | ❌ | High |
| EMPTY_DESCRIPTION | 10-50% | ✅ | Critical |
| MISSING_TRIGGER | 15% | ✅ | High |
| BLOATED_SKILL | 10% | ❌ | Medium |
| ORPHAN_REFERENCE | 5% | ✅ | Low |
| DEAD_CROSS_REF | 5% | ❌ | Low |
