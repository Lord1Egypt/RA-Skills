# Scoring

Two dimensions, computed separately, never averaged together. Decision tiers and
the action matrix live in `SKILL.md § Decide` — this file defines how each number
is produced.

## Rules that apply to every axis

- **1–5 only. No 3★ placeholders.** If the JD does not contain the information an
  axis needs, output `(info insufficient)` and drop the axis from the average.
- **Cite the JD.** Every score below 4★ or above 4★ names the phrase that drove
  it. Quote the JD in its original language even when the surrounding output is
  translated — a translated quote is no longer evidence.
- **The criteria file is the only source of preference.** Never score against what
  you happen to know about an industry, a city, or an employer's reputation.

---

## Desirability axes

### Role fit — `target_title_keywords`, plus scope and seniority in the body

| ★ | Meaning |
|---|---|
| 5 | Title matches a keyword, and the responsibilities match what the user means by that title |
| 4 | Title clearly aligns, or matches with a different label but the same substance |
| 3 | Adjacent — same family, different specialty, or a level off |
| 2 | Related only through a shared word; the actual work is something else |
| 1 | No match |

Read the bullets, not just the header. The same title means different work at
different organizations — a title match with mismatched responsibilities is a
3★, not a 5★, and the one-liner should say so.

### Domain fit — `target_domains`

| ★ | Meaning |
|---|---|
| 5 | The organization's main business is in the user's list |
| 4 | In the list, but this role sits on an adjacent product or team |
| 3 | One step removed — the domain is applied to a field the user did not ask for |
| 2 | Tangential |
| 1 | Not in the list |

**Match by meaning, not by label.** The user wrote their domains in their own
words; a posting will use different ones. "Forecasting and settlement software for
regional grid operators" *is* climate tech, and "cohort-building tools for hospital
research teams" *is* health data, even though neither phrase appears in the list.
Name which listed domain you matched it to and why, so a wrong reading is visible
and correctable. Reserve 1★ for a genuine miss, not a vocabulary mismatch.

### Org fit — `org_traits`

Identify which of the user's traits this organization plausibly has, from the JD
and its self-description only. Traits you cannot assess are simply not matched —
do not assume.

| Situation | Score |
|---|---|
| One or more traits present | Weighted mean of the **present** traits' weights |
| Traits were assessable, none of them present | **3★** — neutral |
| Nothing about the organization can be assessed | `(info insufficient)` |

**The absence of a preferred trait is not the presence of a rejected one.** An
employer that is merely *not* remote-first and *not* a research lab scores 3★, not
1★. A low score requires a trait the user weighted 1–2 to actually be there — a
posting that says "a Thornbury Capital portfolio company" against a stored
`private-equity owned: 1` earns the 1★; a posting that simply never mentions
ownership does not.

An unknown employer with no self-description is the normal case, not a failure.

### Vibe fit — `vibe_anchors_positive` / `vibe_anchors_negative`

The axis people rationalize away and then regret. Compare the JD's language,
values statements, and product description against the anchors — **reasoning from
each anchor's `why`, not from the anchor's reputation.**

| ★ | Meaning |
|---|---|
| 5 | Multiple signals matching a positive anchor's `why`; nothing matching a negative one |
| 4 | Clear positive-anchor alignment, no negative signals |
| 3 | Genuinely neutral — the JD is written in standard corporate register and reveals little |
| 2 | Some language matching a negative anchor's `why` |
| 1 | Strong, repeated match to a negative anchor's `why` |

**Mandatory citation format:**

```
Vibe ★★☆☆☆  negative anchor "<name>" — its why: "<the user's stated reason>"
            triggered by: "<exact JD phrase>", "<exact JD phrase>"
```

An adjective without a quote is not a rating. "Feels corporate", "seems
growth-y", "no product taste" are all invalid on their own.

**Unknown organizations.** If you have no reliable knowledge of an anchor, that
changes nothing: the `why` is the comparison basis, and it always was. Never
substitute a reputation for the user's stated reason — that is how the axis drifts
away from the person it is supposed to represent. Equally, never refuse to score
because an anchor is obscure.

### Comp fit — `comp_floor`, `profile.current_comp`

Compare **like for like** first. Normalize period (year / month / hour) and check
`basis`:

- JD quotes base, floor is `total` → not comparable. Mark `(info insufficient)`
  and raise an open question asking for the full package.
- Different currencies → convert only with a rate from `context.fx_rates`.
  Without one, mark `(info insufficient)`. **Never invent an exchange rate.**
- `context.comp_convention: n_month` → annualize using the stated multiplier
  before comparing, and show the arithmetic.

| ★ | Meaning |
|---|---|
| 5 | ≥ 130% of current comp |
| 4 | 110–129% |
| 3 | 100–109% — lateral |
| 2 | Below current but at or above the floor |
| 1 | Below the floor — the hard gate should already have caught this |

No comp stated in the JD → `(info insufficient)` plus an open question. This is
the most common case in many markets; it must not silently become a 3★.

---

## Combining the desirability axes

Weighted mean using `axis_weights`. Axes marked `(info insufficient)` are removed
and the remaining weights renormalized.

Worked example — Org fit and Comp fit both unavailable:

```
Role fit  4  weight 25
Domain    5  weight 20
Org       —  (info insufficient, dropped)
Vibe      2  weight 25
Comp      —  (info insufficient, dropped)

Remaining weight = 25 + 20 + 25 = 70
Weighted = (4×25 + 5×20 + 2×25) / 70 = (100 + 100 + 50) / 70 = 3.57
Desirability tier: Good  →  capped at Weak by the vibe ≤ 2★ rule
```

Show the renormalized denominator whenever an axis was dropped, so the user can
see the verdict rests on three axes rather than five.

If **three or more** axes are insufficient, do not report a tier. Say the posting
is too thin to score and list what to ask for.

---

## Candidacy

### Extract the requirements

Split the JD's requirements into **must-have** and **preferred**. Markers vary by
language and market; treat anything hedged — preferred, nice to have, a plus,
bonus, ideally, 优先, wünschenswert, 尚可 — as preferred.

Ambiguous section with no split marker → treat everything as must-have and note
the assumption.

### Score

| Requirement matches | Credit |
|---|---|
| an item in `skills.mastered` | 1.0 |
| an item in `skills.learning` | 0.5 |
| nothing | 0 |

Years of experience is one requirement, met if `profile.years_of_experience` is
within one year of the stated minimum. A stated maximum is not a requirement.

`hit_rate = credit_earned / count(must_have)`

| Tier | Hit rate |
|---|---|
| **Likely** | ≥ 75% |
| **Plausible** | 40–74% |
| **Stretch** | < 40% |
| **Unknown** | fewer than 3 stated must-haves |

Worked example:

```
Must-haves (5):
  5+ years in the field          → profile says 6         1.0
  SQL                            → mastered               1.0
  Experiment design              → mastered               1.0
  Kubernetes                     → learning               0.5
  Managed a team of 3+           → no match               0

credit 3.5 / 5 = 70%  →  Plausible
Preferred (not counted): German at C1, healthcare experience
```

### Reporting rules

- **Count only what the JD states.** Never add a requirement the posting does not
  contain, however standard it seems for the role.
- **Never map seniority across markets.** L5, P7, Senior II, 主管, and Grade 6 are
  not comparable. Count stated requirements; ignore the level label.
- **Report gaps as facts plus context**, e.g. *"No team-management evidence — this
  is usually probed with 'tell me about a time you gave difficult feedback', so
  it is answerable from mentoring experience if you have any."* Not a verdict on
  the person.
- **No inflation.** Do not round `learning` up to `mastered` because the user
  seems close. The half-credit exists so the honest answer is the useful one.
- **No catastrophizing.** A Stretch is a real option with a named gap, not a
  rejection. Say which one or two items would move it to Plausible.
- Preferred requirements the user *does* meet are worth mentioning — they are
  interview material even though they do not affect the tier.
