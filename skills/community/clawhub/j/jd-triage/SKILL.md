---
name: jd-triage
description: "Career decision system for job seekers. Scores a job description on two independent dimensions — how much you want it (5 weighted axes against your stored criteria) and how likely you are to get it (your skills vs the JD's stated requirements) — then returns one concrete action. Use when (1) the user pastes a job description or recruiter message, (2) the user invokes /jd-triage or asks 'should I apply for this role', (3) the user asks to list, compare, or analyze previously evaluated roles, (4) the user asks what to learn next for a target role, (5) the user asks to set up, update, or reset their career criteria. Market-, language-, and profession-neutral; bootstraps a criteria profile on first run."
---

# jd-triage · v1.1.1

A JD is evaluated on **two independent dimensions**, never collapsed into one number:

- **Desirability** — do you want this? Five weighted axes scored against the user's stored criteria.
- **Candidacy** — can you get this? The JD's stated must-have requirements vs the user's skills inventory.

A role you want but can't get is a *stretch*, not a *skip*. A role you can get but don't want is a *backup*, not an *apply*. Collapsing both into one star rating destroys that distinction — which is the whole decision.

Responsibilities:

1. **Bootstrap & maintain** a criteria profile at `~/.openclaw/workspace/jd_criteria.md`.
2. **Evaluate** a JD → two-dimension verdict + one action.
3. **Log** every evaluation to `~/.openclaw/workspace/jd_history.md`.
4. **Analyze / Plan** over accumulated history (see `references/analysis-commands.md`).

## Language

**Default to English.** If the user writes in another language, respond entirely in that language for the rest of the session.

| Surface | Language |
|---|---|
| All conversational output — bootstrap Q&A, verdicts, tables, **and the verdict tier as displayed** | User's language (English by default) |
| `jd_criteria.md` field keys, `jd_history.md` structural labels, verdict tier names **in storage** | **Always English** — grep-friendly, stable across language switches |
| Stored free-text values (org names, summaries, red-line rationales, JD quotes) | The language the user wrote them in, at write time |

**Never auto-translate stored content.** When listing or comparing entries written in different languages, render structural labels in the current language and show stored free text verbatim. Quotes pulled from a JD keep the JD's original language even when the surrounding output is translated — a translated quote is no longer evidence.

## State machine

On every invocation, read `~/.openclaw/workspace/jd_criteria.md` and branch:

| State | Condition | Action |
|---|---|---|
| **S1: Missing** | File does not exist | **Quick Start** (5 questions) → proceed to the requested command |
| **S2: Schema gap** | File exists, `schema_version` < 3 | Migrate silently where possible, ask only for fields that cannot be inferred (see `references/bootstrap.md § Migration`) |
| **S3: Fresh** | Complete, `last_updated` ≤ 30 days ago | Proceed directly. Note "Using criteria from `<date>`" in one line |
| **S4: Stale** | Complete, `last_updated` > 30 days ago | Ask once: "Anything changed — comp, location, red lines, what you're learning? (y/n)". `n` → refresh timestamp only. `y` → user names the fields, patch those |
| **S5: Explicit update** | "update criteria" / `/jd-triage update` / `/jd-triage reset` | Full bootstrap, current values pre-filled |

`criteria_version` increments on every S1 / S2 / S5 write. S4 "nothing changed" bumps `last_updated` only.

If the invocation included a JD, continue to Evaluation after the criteria are settled. Otherwise execute the requested command and stop.

## Commands

| Input | Action |
|---|---|
| A pasted JD, or `/jd-triage` | Evaluate |
| `/jd-triage update` \| `reset` | S5 bootstrap |
| `/jd-triage quickstart` | Force the 5-question Quick Start |
| `/jd-triage learn` | Derive criteria from example JDs (`references/bootstrap.md § Derive from examples`) |
| `/jd-triage history` | Last 10 entries, one line each |
| `/jd-triage compare <id1> [<id2>]` | Side-by-side table |
| `/jd-triage analyze` | Market signals across history → `references/analysis-commands.md` |
| `/jd-triage plan` | Skill-gap plan per target role → `references/analysis-commands.md` |

A past role referred to by org name resolves to an ID by grepping `jd_history.md`.

## Evaluation

### 1. Parse

Extract: title, org name, responsibilities, **must-have requirements**, **preferred requirements** (keep these separate — the split drives Candidacy), comp, location and remote policy, intensity signals, reporting line, team size.

If the input has a title but no responsibilities or requirements, **stop and ask for the full posting.** Do not evaluate a title.

### 2. Hard gates

Failures produce **❌ OUT** and stop — except red lines, which are weighted (below).

- `comp_floor` — compare like for like: the JD's basis (base / total / hourly) against the floor's basis, in the same currency and period. If the bases differ or the currency is different, convert only if the user supplied a rate; otherwise mark **unknown** and raise an open question. If the JD states no comp at all, mark unknown and continue — **never auto-fail on missing comp.**
- `locations` / `remote_ok` — JD location must be in the list, or the JD must be remote-eligible under the user's `remote_ok` setting.
- `intensity_tier` — the JD's implied tier must not exceed the user's. Signal patterns are per-language in `references/intensity-signals.md`. When the JD gives no signal either way, assume the user's own tier (no penalty) and say so.
- `red_lines` — match **semantically**, not by substring. A red line is `{pattern, why}`; use the `why` to decide whether a phrase in a different language or different wording is the same thing. Then weight by position:

  | Where the matched responsibility sits | Verdict |
  |---|---|
  | In the title, in the first 1–2 responsibility bullets, or plausibly >30% of the role | **❌ OUT** — core |
  | Only in tail bullets, framed as support/assist/partner-with | **⚠️ CONDITIONAL** — score normally, flag it, raise an open question |
  | Only in the requirements/preferred section, not in the duties | Note as an open question, do not gate |

  Always cite the matched phrase **and its location** ("bullet 6 of 7, framed as 'support'"). A bare keyword is not a citation — the user needs the framing to judge.

  Semantic matching cuts both ways: it must not fire on incidental use. A red line of "growth" does not match "growth mindset" in a values paragraph. State what you matched and let the user correct you.

### 3. Desirability — 5 weighted axes

Score each 1–5 per `references/scoring.md`. Weights come from `axis_weights` in the criteria file (defaults there too).

| Axis | Scored against | Default weight |
|---|---|---|
| **Role fit** | `target_title_keywords`, seniority and scope of the role | 25% |
| **Domain fit** | `target_domains` — what the org actually does | 20% |
| **Org fit** | `org_traits` — user-described traits with their own weights | 15% |
| **Vibe fit** | `vibe_anchors_positive` / `_negative`, each carrying a `why` | 25% |
| **Comp fit** | `comp_floor` and `profile.current_comp` | 15% |

**Never pad.** If the JD lacks the information for an axis, output `(info insufficient)` and **exclude that axis from the weighted average**, renormalizing the remaining weights. A 3★ placeholder is a fabricated data point that silently moves the verdict.

**Vibe must cite.** Every vibe score names at least one anchor and quotes the JD phrase that triggered it, and reasons from the anchor's `why` — not from what the model happens to know about that organization. Anchors may be small or local; if the model has no knowledge of the named org, the `why` is the *only* valid basis. Adjective-only judgments ("feels corporate") are forbidden.

### 4. Candidacy — can you get it?

If `skills` is empty — the normal state after Quick Start — ask for it once,
inline, before scoring: *"To score whether you can get this, I need your skills:
what could you be interviewed on today, and what are you actively learning?"*
Save the answer so this is never asked twice.

Compare the JD's **must-have** requirements against `skills` and `profile`:

- Each requirement scores `1.0` if it matches `skills.mastered`, `0.5` if it matches `skills.learning`, `0` otherwise.
- Years-of-experience counts as one requirement; met if `profile.years_of_experience` is within one year of the stated minimum.
- **Preferred / nice-to-have requirements are excluded from the denominator** and reported separately.
- Hit rate → tier: **Likely** ≥75%, **Plausible** 40–74%, **Stretch** <40%.
- Fewer than 3 stated must-haves → **Unknown**; do not guess, raise an open question instead.

Do not invent requirements the JD does not state. Do not map seniority labels across markets (an L5 and a P7 and a 主管 are not comparable) — count stated requirements only.

Report gaps honestly in both directions: no inflation ("you basically have this"), no catastrophizing. A gap is a fact plus how it is usually probed in an interview, not a disqualification. Items in `skills.learning` are real partial credit — say so.

### 5. Decide

Apply in this order. **The first rule that fires wins; stop there.**

1. Hard gate failed → **❌ OUT**
2. Red line in a non-core responsibility, **or** an unknown that could flip the verdict (comp, location, or scope) → **⚠️ CONDITIONAL**

   Test whether the unknown can actually flip anything before invoking this. An
   unknown that is already bounded on the deciding side is an **open question, not
   a conditional**: a posting quoting €95,000 base against a €90,000 *total* floor
   leaves comp unscoreable, but the gate is settled — base alone cannot make the
   total fall below the floor. Say so and carry on to the matrix. Reserve
   CONDITIONAL for unknowns whose resolution genuinely changes the answer.
3. Otherwise → look up the matrix

Desirability tier from the weighted average — checked top to bottom, **first
match wins**, so a high average with one collapsed axis falls through rather than
qualifying:

- **Strong** — ≥ 4.0 and no axis ≤ 2
- **Good** — ≥ 3.2 and no axis = 1
- **Weak** — ≥ 2.4
- **Poor** — < 2.4

One override: **vibe ≤ 2★ caps desirability at Weak**, whatever the average says. Vibe is the axis people rationalize away and regret.

| | Likely | Plausible | Stretch |
|---|---|---|---|
| **Strong** | 🔥 Apply now | 🔥 Apply now | 🎯 Stretch apply |
| **Good** | ✅ Apply | ✅ Apply | 🎯 Stretch apply |
| **Weak** | 🗄️ Backup | 🗄️ Backup | ❌ Skip |
| **Poor** | ❌ Skip | ❌ Skip | ❌ Skip |

Candidacy **Unknown** → read the **Plausible** column, mark the result provisional
(`✅ Apply (provisional)`), and put a question about the actual requirements first
under Open questions. Never silently drop to a one-dimensional verdict.

Desirability **too thin to score** (three or more axes insufficient, per
`references/scoring.md`) → the verdict is **⚠️ CONDITIONAL**, written as
`Desirability: (too thin to score)`. There is no tier to report and no matrix to
read; what the posting is missing goes under Open questions.

### 6. Log

Append to `~/.openclaw/workspace/jd_history.md` — format and ID scheme in `references/history.md`. Create the file if missing.

**The evaluation is not complete until this write succeeds.** Confirm it on the last line of the output (`Logged: JD-…`). If the write fails, say so explicitly — never let it fail silently.

### 7. Output

Two surfaces, two rules. Do not let the second one leak into the first.

**On screen — the user's language.** Everything in the template below is a
*label*, not a literal: the section headings, the axis names, and the tier itself
are all translated into the language of the conversation. Keep the **shape** —
line order, star glyphs, arrows, emoji, the `<k>/<n>` figures. An evaluation
written for a Chinese speaker reads in Chinese throughout; the only fragments
that stay in another language are quotes lifted from the posting, which are
evidence and are never translated.

**In `jd_history.md` — always English.** The stored `Action` field carries the
tier token exactly as spelled here, in this casing, because `history` and
`compare` parse it:

`Apply now` · `Apply` · `Stretch apply` · `Backup` · `Skip` · `OUT` · `CONDITIONAL`

Never store the action wording in place of the tier: a conditional evaluation
stores `CONDITIONAL`, not `Confirm before applying`. What the reader saw on
screen may match neither string — it was that tier, in their language.

If the criteria were reused rather than collected, put `Using criteria from <date>`
on its own line **above** the verdict line, never below or inside it — translated
like everything else on screen.

```
<emoji> <TIER>          Desirability: <tier>   Candidacy: <tier>

Want it
  Role fit     ★★★★☆
  Domain       ★★★★★
  Org          ★★★☆☆
  Vibe         ★★☆☆☆   anchor "<name>" — "<JD phrase>"
  Comp         ★★★★☆
  → weighted <n.n>/5

Can get it
  Meets <k>/<n> stated must-haves
  ✅ <met>            ⚠️ <partial — in progress>            ❌ <gap>

<one sentence: the actual judgment>

Open questions
- <only real unknowns; omit the section entirely if none>

Logged: JD-YYYYMMDD-NNN
```

**CONDITIONAL** — same shape, but the one-liner must carry the conditional explicitly: *"Fits if `<X>` is confirmed; OUT if `<X>` turns out to be core."* Action is always "Confirm before applying", and the deciding question goes first under Open questions.

**OUT** — short form, but never empty-handed:

```
❌ OUT
Triggered: <gate or red line, with location and exact phrase>
<one sentence: why>

Matched anyway
- <aligned dimensions worth remembering — omit if genuinely none>

Logged: JD-YYYYMMDD-NNN
```

The "Matched anyway" block exists so that rejections still accumulate signal about what to look for.

## Behavioral constraints

- **OUT means OUT.** Do not soften because the user is already emotionally invested in the role.
- **Never pad a score.** Missing information is `(info insufficient)` and drops out of the average — not 3★.
- **Never pre-fill from training data.** Criteria values come only from the user. Do not infer comp norms, city tiers, org reputations, or what a company is "known to be like".
- **Reason from the user's `why`, not from fame.** An anchor the model has never heard of must work exactly as well as a famous one.
- **Red lines are weighted, not literal**, and semantic, not substring.
- **The output template is a shape, not a script.** Its English wording stands in
  for the user's language — headings, axis names and the tier itself are all
  translated. Only two things resist translation: values stored in
  `jd_history.md`, and quotes taken from the posting.
- **Keep the two dimensions apart.** Never average desirability and candidacy together; never let "hard to get" lower the desirability score or vice versa.
- **Open questions are output, not internal state.** An unknown that could flip the verdict gets written down as a question to ask, phrased so it can be sent to a recruiter as-is.
- **One JD at a time.** Multiple pasted JDs are evaluated separately, then optionally compared.
- **No hollow encouragement.** No "good luck", no "hope this helps".
- **Trust hand edits.** If the user edited `jd_criteria.md`, parse what is there. If a field is malformed, quote the line and ask — never silently overwrite.
- **Analyze and plan need real data.** Below the thresholds in `references/analysis-commands.md`, say so and stop.

## Detection triggers

- A pasted block that reads like a job posting: a title-like line plus responsibilities or requirements. Length alone is not a trigger — do not claim any long paste.
- `/jd-triage` and its subcommands.
- "should I apply", "is this role worth it", "evaluate this JD", "what should I learn next", "what patterns do you see in the roles I've looked at", and their equivalents in the user's language.

## Files

| File | Loaded when |
|---|---|
| `assets/criteria-template.yaml` | Writing the criteria file |
| `assets/presets/*.yaml` | Quick Start, to pre-fill structure |
| `references/bootstrap.md` | S1 / S2 / S5, or `/jd-triage learn` |
| `references/scoring.md` | Every evaluation |
| `references/intensity-signals.md` | Intensity gate, when the JD is not in English |
| `references/history.md` | Logging, `history`, `compare` |
| `references/analysis-commands.md` | `analyze`, `plan` |

Load a reference only when its flow runs.
