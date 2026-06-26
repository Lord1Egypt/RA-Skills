# Scoring rubric

Each soft axis is scored 1–5. Never default to 3★ to fill space. If the JD lacks the information needed for an axis, output `★★★☆☆ (info insufficient)` explicitly so the user can ask the recruiter.

Hard gates use the same JD signals but are pass/fail.

---

## Hard gate signal extraction

### `lifestyle_tier` — JD intensity signals

Scan the JD for these patterns and map to a tier. If the JD's implied tier is **higher** than the user's tier, the gate fails.

| Tier | JD signals (any of) |
|---|---|
| `strict_9to5` | "9-to-5", "no overtime", "work-life balance" explicit, "flex hours, no weekends" |
| `standard` | "occasional crunch around launches", "some weekends during release", "fast-paced but sustainable" |
| `crunch` | "高强度", "fast-paced", "long hours", "10/12 hour days", "996", "wear many hats" without balance counterweight, startup with no balance language |
| `always_on` | "on-call rotation", "24/7", "global team across timezones with night meetings", "大小周", "7×12" |

Default when ambiguous: assume `standard` for established companies, `crunch` for early-stage startups under 50 people. Note the assumption explicitly in output.

### `hard_red_lines` — substring matching + responsibility weight

Case-insensitive substring/keyword match against the full JD text (title + responsibilities + requirements + company description). On a hit, **do not auto-OUT**. Apply the responsibility-weight rule from `SKILL.md § Hard gates`:

- Keyword in title / first 1–2 bullets / >30% of role → **❌ OUT** (core)
- Keyword only in tail bullets, framed as "支持/协助/辅助/support/assist", main duties fit user → **⚠️ CONDITIONAL** (proceed to scoring, list as open question)
- Keyword only in qualifications/preferred section → note as open question, do not gate

Always cite the matched substring AND its location (which bullet, what wording). A bare keyword citation is insufficient — the user needs to see the framing to judge.

Examples:
- "负责增长策略制定" in bullet 1 → core, OUT
- "支持AI产品的商业化工作（定价、合作伙伴对接、Demo）" in last bullet, when bullets 1-4 are Agent/RAG/Prompt → CONDITIONAL, ask HR about scope split

---

## Soft axis rubrics

### Title fit (`target_title_keywords`)

| Stars | Meaning |
|---|---|
| ★★★★★ | JD title exactly matches a keyword (e.g. user has "Agent PM" → JD title "Agent PM, Foundation Models") |
| ★★★★☆ | JD title strongly aligns (e.g. "AI Product Manager" matches user's "Agent PM") |
| ★★★☆☆ | JD title is adjacent (e.g. "Product Manager, AI" — generic AI PM, not specifically agent/dev tools) |
| ★★☆☆☆ | JD title is vaguely related (e.g. "Senior PM" with AI mentioned only in responsibilities) |
| ★☆☆☆☆ | JD title doesn't match any keyword |

### Industry/track fit (`target_industries`)

| Stars | Meaning |
|---|---|
| ★★★★★ | JD's industry/product area is in user's list AND is the company's main focus |
| ★★★★☆ | In user's list but adjacent product area at the same company |
| ★★★☆☆ | One step removed (e.g. user wants "AI", JD is "AI in fintech" with heavy fintech weight) |
| ★★☆☆☆ | Tangentially related |
| ★☆☆☆☆ | Not in user's list |

### Company type fit (`company_type_preferences`)

Direct lookup. Identify the company type from JD/company info, return the user's stored 1–5 rating for that type. If company type is genuinely unclear (e.g. unknown startup, no public info), output `★★★☆☆ (info insufficient)`.

### Company size fit (`company_size_preferences`)

Direct lookup. If company size is mentioned in JD, use it; otherwise mark info insufficient. Don't guess from training data.

### Vibe fit (`vibe_anchors_positive` / `vibe_anchors_negative`)

This is the load-bearing axis. Compare the JD's tone, product description, company description, and stated values against the user's two anchor lists.

| Stars | Meaning |
|---|---|
| ★★★★★ | JD/company reads strongly like one of the positive anchors — same product philosophy, same restraint, same craftsmanship signals |
| ★★★★☆ | Solid alignment with positive anchors, no negative-anchor signals |
| ★★★☆☆ | Neutral — neither group's signals strongly present |
| ★★☆☆☆ | Mild signals matching negative anchors (e.g. heavy growth/conversion language, KPI-heavy framing) |
| ★☆☆☆☆ | Strong match to negative anchors — anxiety-driven, conversion-funnel language, dark patterns, retention-at-all-costs |

**Mandatory citation rule.** Every vibe rating must name at least one specific anchor (positive or negative) AND quote the JD phrase that triggered the comparison. Adjective-only judgments ("零产品美感", "看着很增长") are insufficient — they hide whether the model is actually using the user's anchor list or making things up.

Required format:
```
Vibe ★☆☆☆☆ — closer to negative anchor "<anchor name>" than positive anchor "<anchor name>";
  triggered by: "<exact JD phrase 1>", "<exact JD phrase 2>"
```

A 1★ on vibe alone is enough to drop the overall verdict to ⚠️ Caution.

### Salary match (`salary_floor`, `current_salary`)

| Stars | Meaning |
|---|---|
| ★★★★★ | JD comp ≥ 130% of `current_salary` (significant uplift) |
| ★★★★☆ | JD comp 110–130% of `current_salary` (meaningful uplift) |
| ★★★☆☆ | JD comp 100–110% of `current_salary` (lateral) |
| ★★☆☆☆ | JD comp ≥ `salary_floor` but below current — caution |
| ★☆☆☆☆ | JD comp < `salary_floor` — should already be caught by hard gate |

If JD has no comp info, output `★★★☆☆ (info insufficient — ask recruiter)`.

---

## Verdict aggregation

```
Strong Apply (✅)   — all axes ≥ 4★, no axis below 3★, no near-miss hard gates
Apply (🎯)          — average ≥ 3.5★, no axis below 2★, vibe ≥ 3★
Conditional (⚠️)   — red-line keyword in non-core responsibility, OR critical unknowns that could flip the verdict; proceed to soft scoring + list open questions
Caution (⚠️)        — average ≥ 2.5★, OR vibe = 1-2★ (vibe drag)
Skip (❌)           — average < 2.5★, OR any high-weight axis = 1★
OUT (❌)            — hard gate failed: core-responsibility red line, salary below floor, city mismatch, lifestyle exceeds tier
```

Vibe is non-negotiable: a 1★ on vibe drops verdict at least one tier below what averages would suggest.

OUT verdicts must still output a `Strengths matched` section listing axes/aspects of the JD that aligned with the user (e.g. company type, language environment, partial responsibility match) — even when skipping, this builds signal for future similar JDs.
