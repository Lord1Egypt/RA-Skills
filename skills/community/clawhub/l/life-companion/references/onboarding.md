# Onboarding — first run

Goal: collect the **minimum** to be useful *for what they actually asked*, warmly
and with consent — not a 20-question intake. Onboarding is **tiered and lazy**:
gather Tier 0 once, then only the tier the current request needs. It's resumable
(`onboarding_complete` / explicit `null`s mean "not asked yet", so nothing gets
re-asked). **Never** run onboarding during a crisis — help first (see safety.md).

**Preferred method: the HTML form.** Run `scripts/form_server.py --form onboarding`
(see `references/forms.md`) — it collects Tier 0 + the consent-gated birth block in
one clean page and writes it for you. The tiered chat flow below is a **fully supported
equal**, not a fallback: use it when a browser is awkward or they would rather just talk.
Either way the tiers and consent rules are the same.

When you do use chat: give **selectable options** wherever there's a choice — this
person strongly prefers picking over typing. Use `AskUserQuestion` if your harness has
it; otherwise a short **numbered list** they answer with numbers. Keep free text for
names and dates only.

## Tier 0 — identity (~4 quick things, after the first answer)
Offer these once, **after** you have answered what they came for, as one short list of
options. Don't hold the answer back for them: read the language from the message they
wrote, keep the default tone until they pick one, and ask where they are when it matters
(daily timing; the crisis table, where an unknown location means findahelpline.com):
- **What to call you** (free text).
- **Language** → sets `identity.locale` (offer 中文 / English / 双语). Ask in the
  language they wrote to you in.
- **Where you are** (city/country or timezone) → `identity.timezone`. Needed for
  correct daily timing *and* for localizing crisis helplines — you can say that.
  Take their own words and resolve them offline:
  `companion.py resolve-tz "柏林"` → `Europe/Berlin`. One clear candidate: store it.
  Several: ask which. **None: ask for a nearby major city — never guess a zone**, since
  it decides which country's crisis line they'd be given. Keep the raw words in
  `identity.location` too.
- **Tone** you want (options: 温暖直接 / 轻松俏皮 / 简洁克制) → `preferences.tone`.

Write with `companion.py set-profile --merge-json '{"identity":{…},"preferences":{…}}'`.

## Tier 1 — birth block (only for destiny / daily-fortune)
Before anything is **stored**, ask consent, as options — birth data is sensitive, and it stays
on this machine. If they already gave the details in their message, compute and answer first,
then ask:
**存到本机** · **这次算一下，不存** · **不提供**.
- 存到本机 → `companion.py consent --set birth=yes`, then collect the fields below.
- 这次算一下，不存 → take the details from the conversation and compute directly
  (destiny.md §1): no `set-profile` and no cache, which refuses without consent anyway.
  Say plainly that nothing was kept and that a daily card will need the details again.
- 不提供 → skip these modules gracefully.
Then collect:
- **Birth date** — required for BaZi. Ask which calendar they know it in, as options
  (公历 / 农历). Many people, and most parents, only know the lunar date. For 农历 run
  `companion.py lunar-to-solar YEAR MONTH DAY [--leap]` and store the solar result as
  `birth.date`, with what they said in `birth.date_input`
  (`{"calendar": "lunar", "lunar": "YYYY-MM-DD", "leap": false}`). **Never convert by
  hand**: leap months and 29-day months are where that goes wrong, and the command refuses
  a date that doesn't exist (e.g. a 闰月 in a year without one) instead of rolling it over.
  If they aren't sure whether it was a 闰月, ask; don't pick one.
- **Birth time** (HH:MM) — offer "know it exactly / roughly / don't know". If
  unknown, that's fine: BaZi still works; Western rising/houses won't. Store
  `time_known` explicitly so it's never re-asked, and store the answer as
  `birth.time_accuracy` (`exact` / `approx` / `unknown`). For "roughly", ask how rough as
  options (±30 min / ±1 h / ±2 h) into `birth.time_window_min`: a rough 09:00 stored as an
  exact one makes every pillar computed from it look certain.
- **Birthplace** (city) — store the name in `birth.place`, **and immediately derive
  and store `birth.lat`, `birth.lon`, and `birth.tz_at_birth`** from it. A city's
  coordinates and its timezone are stable public reference facts (not fabrication, not
  prediction — this is a lookup, like knowing Beijing is ~39.9°N/116.4°E in
  Asia/Shanghai), so fill them rather than leaving them null.
  **Store `tz_at_birth` as an IANA zone NAME** (`Asia/Shanghai`, `Europe/Amsterdam`),
  not as a number of hours. Pass that name straight to `astro.py --tz` and it resolves
  the offset actually in force at that birth moment — historical DST and zone changes
  included. Do **not** work the offset out yourself; that turns a lookup into a guess,
  and a summer European birth is the case people get wrong. (A plain offset like `8`
  or `-5` still works if a zone name genuinely isn't determinable.)
  Without these three, **the full Western natal chart can never compute the
  Ascendant/houses and BaZi can't offer True Solar Time** — so this is the step that
  makes those features actually work.
- **Chart convention** (the field is `birth.gender`) — BaZi's 大运 runs forward or
  backward by the rule 阳男阴女顺行 / 阴男阳女逆行, so the calculation needs one of two
  values and the tradition offers no third. **Ask for it as what it is: a setting the
  chart needs, not a statement about who they are.** 「起大运的方向在传统规则里只有两种
  取法，我按哪一种给你算？」 If they are non-binary, say plainly that the tradition has
  no convention for it, let them pick which one to use, and note that the choice is
  theirs and reversible. Their actual identity belongs in `identity.pronouns`, which is
  never inferred from this field. Do not let a chart setting become a label.

Write to `birth:` via `set-profile`. Then hand to `modules/destiny.md`.

## Tier 2 — career (only when they use the career module)
Don't front-load. The career module runs its own short assessment (interest items
first). See `modules/career.md`.

## Tier 3 — relationships (only when they bring it up)
Consent first (`relationships=yes`). Mostly accrues from journaling — no intake
quiz. See `modules/relationships.md`.

## Finishing
When Tier 0 (+ whatever tier the request needed) is in, mark onboarding done —
`companion.py set-profile --merge-json '{"onboarding_complete": true}'`. A good first run
starts and ends with the thing they came for (their chart, their first logged day, their
career read); the profile questions ride along at the end, never in front of it.

## Example (first message = "帮我看看八字，1993-04-12 07:35，男，北京")
1. `brief` → not initialized. They gave everything the chart needs, so compute it now
   (`modules/destiny.md`) and deliver their 命盘: one disclaimer note at the top (from
   disclaimers.md), then the reading. Nothing is stored yet.
2. At the end, one list of options: keep the birth details on this machine / only this
   time / don't keep them, plus what to call them, language and tone.
3. If they choose to keep them: `init` → `consent --set birth=yes` → `set-profile` with the
   birth block (resolve `tz_at_birth` and the coordinates) and whatever Tier 0 they
   answered → `onboarding_complete: true`.

If the first message is only "帮我看看八字", the birth details are what the chart needs: ask
for them, with the three consent options, before computing.
