# Bootstrap

Three ways in. Default to **Quick Start** — a profile that exists is worth more
than a perfect profile the user abandoned halfway through.

| Mode | When | Cost |
|---|---|---|
| **Quick Start** | S1 (no file), `/jd-triage quickstart` | 5 questions |
| **Derive from examples** | `/jd-triage learn`, or offered when a profile is thin | Paste a few JDs |
| **Full** | S5 (`update` / `reset`), or user asks | All fields |

Write to `~/.openclaw/workspace/jd_criteria.md` using `assets/criteria-template.yaml`.
Field keys English; values in the user's language.

## Using presets

`assets/presets/*.yaml` are **menus, never defaults**. Pick the preset matching
the user's `role_family`, show the suggested traits and red-line starters as a
numbered list, and write only the lines the user selects — reworded however they
like. Never silently write a preset value. `axis_weights` are the one exception:
they are a starting distribution, applied unless the user changes them, and
mentioned once so the user knows they exist.

---

## Quick Start — 5 questions

Ask one at a time. Accept "skip" on any of them.

**1. Context.** "What kind of role, what market, and which languages can you work
in?" → `context.role_family`, `context.market`, `context.languages`.
From the market, infer `context.comp_convention` and **state the inference for
confirmation** ("I'll assume comp is quoted as an all-in annual number — correct?").

**2. Target.** "What titles are you looking for, and what should the organization
actually do?" → `soft_axes.target_title_keywords`, `soft_axes.target_domains`.

**3. Floors.** "What's the lowest offer you'd accept — and is that base or
all-in? Where can you work, and is remote acceptable?" → `hard_gates.comp_floor`
(amount, currency, period, basis), `hard_gates.locations`, `hard_gates.remote_ok`.

**4. Automatic no's.** "Anything that makes a role an instant no — and why?"
→ `hard_gates.red_lines`. Push for the *why* on each one; it is what makes
matching work across languages and rewordings. "None" is a valid answer.

**5. Anchors.** Use the preset's `vibe_prompt`. Ask for 1–3 organizations, teams,
or products the user admires, **each with one line on why**.
→ `soft_axes.vibe_anchors_positive`.

Then write the file and say plainly what is not yet filled:

> Saved. Org fit and Candidacy will show *info insufficient* until you add org
> traits and your skills — I'll ask for those the first time they matter.

### Just-in-time capture

Do not front-load the rest. Ask for a field the first time an evaluation
actually needs it, once, inline:

- **Skills** — before scoring Candidacy for the first time: "To score whether you
  can get this, I need your skills. List what you could be interviewed on today,
  and separately what you're actively learning." → `skills.mastered`,
  `skills.learning`. Write them to the file so this is asked only once.
- **Org traits** — the first time a JD's org type looks decision-relevant.
- **Negative anchors** — the first time a JD trips something the user reacts badly
  to: "Want me to save that as a negative anchor?"
- **Intensity tier** — the first time a JD carries strong intensity signals.

Each capture writes to the file and bumps `criteria_version`.

---

## Derive from examples (`/jd-triage learn`)

The highest-quality path, and the repair path for a thin or lazy profile. People
are bad at stating preferences in the abstract and good at reacting to concrete
postings.

1. Ask for **2–4 postings the user would apply to** and **2–4 they turned down or
   scrolled past**. Past rejections work; so do screenshots pasted as text.
2. Read all of them and extract:
   - Recurring title and scope patterns → `target_title_keywords`
   - What the organizations do → `target_domains`
   - Traits shared by the liked set / by the rejected set → `org_traits`
   - Phrases that plausibly explain each rejection → candidate `red_lines`
   - Tone and values language distinguishing the two sets → candidate anchors
3. **Propose, never write.** Output a numbered list of drafted entries, each with
   the evidence it came from and a drafted `why`:

   ```
   3. Red line: "individual revenue target"
      From: Posting B, "own a quarterly booking number" — you skipped this one.
      Why (draft): a quota changes what the job optimizes for.
      Keep / edit / drop?
   ```
4. Write only accepted items. Ask the user to fix any `why` that does not sound
   like them — the `why` is what the skill reasons from later.

Never infer a red line from a single posting without saying which one it came
from. One rejection can have many causes; the user picks the real one.

---

## Full bootstrap

Every field in `assets/criteria-template.yaml`, in four blocks, one block per
turn. Pre-fill current values on S5 so the user only changes what moved.

**Block 1 — Context & profile**
`context` (role_family, market, languages, comp_convention, fx_rates if the user
compares currencies) · `profile` (years_of_experience, current_title_org,
current_comp with basis and notes)

**Block 2 — Hard gates**
`comp_floor` (with basis) · `locations` · `remote_ok` · `intensity_tier` ·
`red_lines` (each with a `why`)

**Block 3 — Soft axes**
`target_title_keywords` · `target_domains` · `org_traits` (trait + weight 1–5) ·
`vibe_anchors_positive` and `vibe_anchors_negative` (each with a `why`) ·
`axis_weights` (offer the current distribution, ask only if they want to change it)

**Block 4 — Skills & targets**
`skills.mastered` / `.learning` / `.want_to_learn` · `target_roles`

State the half-credit rule when asking for skills: `learning` items score 0.5
against a requirement, so an honest split produces better advice than an
optimistic one.

### Summary and confirm

Show everything grouped as above, then:

```
Confirm and save?  (y / edit <field>)
```

`edit <field>` re-asks that field only, then re-shows the summary. On `y`, write
the file with today's ISO date and an incremented `criteria_version`.

---

## Migration

Triggered by S2 (`schema_version` < 3). Migrate everything inferable **without
asking**, then ask only for what cannot be derived. Show a summary of what
changed before writing.

| Old (v1 / v2) | New (v3) | How |
|---|---|---|
| `hard_gates.salary_floor` (string) | `hard_gates.comp_floor` (structured) | Parse amount / currency / period. **Basis cannot be inferred — ask.** Show the parse for confirmation |
| `profile.current_salary` (string) | `profile.current_comp` (structured) | Same; keep anything unparseable in `notes` verbatim |
| `lifestyle_tier` | `intensity_tier` | `strict_9to5`→`strict_hours`, `standard`→`standard`, `crunch`→`high`, `always_on`→`always_on` |
| `target_cities` | `hard_gates.locations` | Copy. If `Remote` was in the list, set `remote_ok: yes` and drop it from locations |
| `target_industries` | `soft_axes.target_domains` | Copy. Flag entries that describe an org *type* rather than a domain and offer to move them to `org_traits` |
| `company_type_preferences` + `company_size_preferences` | `soft_axes.org_traits` | Each entry rated ≠ 3 becomes `{trait, weight}`. **Entries rated 3 are dropped** — they never changed any outcome. Say how many were dropped |
| `hard_red_lines` (strings) | `hard_gates.red_lines` (`{pattern, why}`) | Pattern copies over; **`why` must be asked** — it is what enables semantic matching |
| `vibe_anchors_positive` / `_negative` (strings) | same keys, `{name, why}` | Names copy over; **`why` must be asked.** Without it the skill can only reason from what it happens to know about that organization, which is exactly the failure mode v3 fixes |
| `skills`, `target_roles`, `learning_velocity` (v2 only) | unchanged | Copy verbatim |
| — | `context` | **Ask** — nothing in v1/v2 implies market or comp convention |
| — | `axis_weights` | Apply defaults, mention once |

So a migration asks for, at most: comp basis, one `why` per red line and anchor,
and the `context` block. Batch them into a single turn.

If `red_lines` is empty after migration, say so directly — it means the
responsibility-weighting logic has never had anything to act on — and offer
`/jd-triage learn` to populate it from real postings.
