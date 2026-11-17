# Profile & journal schemas

Canonical shapes for the files under `COMPANION_HOME`. **Don't hand-edit these** —
go through `companion.py` so writes stay atomic and consent-gated. `schema_version`
gates future migrations. Rule: an unknown/declined field is an explicit `null`
with a sibling `*_known:false` where relevant, so it is never re-asked.

## `profile.yaml` — slow-changing identity + preferences
```yaml
schema_version: 1
onboarding_complete: true
created: 2026-07-17
updated: 2026-07-17          # bumps on every write
identity:
  name: 小明                  # example persona (not a real user)
  pronouns: null             # optional; ask, don't infer
  timezone: Asia/Shanghai    # IANA zone. Drives daily timing + crisis-helpline locale.
                             # Resolve from their own words: `companion.py resolve-tz 柏林`.
                             # Never guess one — a wrong zone means the wrong country's
                             # helpline. No match → ask; leaving it null is the honest state.
  location: "São Paulo"      # the words THEY used for where they are (optional).
                             # Kept because a city names a country more reliably than a
                             # zone does, which matters for localizing crisis help.
  locale: zh                 # output language: zh | en | bilingual
birth:                       # sensitive — gated by consent.birth
  date: 1993-04-12           # ISO solar/公历; null if declined
  date_input:                # what they actually gave, when it wasn't a solar date
    calendar: lunar          # lunar | solar
    lunar: "1993-03-21"      # converted by `companion.py lunar-to-solar`, never by hand
    leap: false
  time: "07:35"              # local clock time; null if unknown
  time_known: true           # explicit false ⇒ never re-ask
  time_accuracy: exact       # exact | approx | unknown — "大概九点" is approx, not exact
  time_window_min: null      # approx only: ± minutes; pass to bazi.py --time-window
  gender: male               # male|female — needed for BaZi 大运 direction (阳男阴女…)
  place: "Beijing, CN"
  lat: 39.9042
  lon: 116.4074
  tz_at_birth: "Asia/Shanghai"   # IANA zone NAME (not an hour offset).
                             # Pass to BOTH astro.py --tz and bazi.py --tz. Without it
                             # bazi resolves 節氣 on a Beijing clock and a non-UTC+8
                             # birth can get the wrong year/month pillar.
  conventions:               # frozen so charts regenerate identically
    true_solar_time: false   # default civil time; TST is an offered toggle
    zishi_rule: late         # 早/晚子时 for 23:00–24:00 births
preferences:
  tone: warm-direct
  advice_style: options      # offer selectable options, not free-text questions
  skepticism: high           # keep "reflective, not predictive" explicit
  checkin_cadence: daily
context:                     # free-form, model-maintained, sensitive
  career: "在读研究生;在想毕业后的方向"
  values: ["honesty", "craft"]
modules_enabled: [journal, destiny]
```

## `consent.yaml` — per-category, revocable
```yaml
birth:         {granted: true,  date: 2026-07-17}
relationships: {granted: null,  date: null}     # null = not yet asked
mood:          {granted: true,  date: 2026-07-17}
```

## `journal/YYYY-MM.md` — human-readable (one file per month)
```markdown
## 2026-07-17  (Thu) · mood 6/10 · energy: low
tags: career, interview-anxiety

这周有点累。散步之后好一些。明天有场面试，有点紧张。

> companion: Second time this month movement reset your afternoon. Front-load it?
```
The `> companion:` line records the reflection you gave, so continuity is
auditable and you don't repeat yourself.

## `journal/index.jsonl` — machine mirror (written atomically with the prose)
```json
{"date":"2026-07-17","mood":6,"energy":"low","tags":["career"],"themes":["rejection","recovery-via-movement"],"module_touch":["career"],"people":[],"crisis_flag":false,"file":"journal/2026-07.md","offset":142}
```
`mood` is an integer **0–10** (out of range is rejected, not stored — it would poison
every `trend` average, which is presented as a computed fact). It is `null` for
text-only entries, and `add-entry` returns a `dropped` list when `consent.mood` is not
granted so the drop is never silent;
`crisis_flag` lets `safety_scan`/`trends` scan cheaply; `people` powers
relationship pattern-tracking and is therefore gated by `consent.relationships`
(`add-entry` drops it without that consent and says so in `dropped`); `offset` points
back into the prose. `forget --entry` / `--person` / `--mood` rewrite the file and every
offset together, and refuse outright if the file no longer matches the index.

## `state/continuity.yaml` — loaded first every turn
```yaml
rolling_summary: "最近在准备面试；散步能稳定情绪；…"
open_threads:
  - {thread: "周四的面试", opened: 2026-07-17, status: open}
recent_moods: [6, 4, 7]
updated: 2026-07-17
```

## `state/modules/*.yaml` — per-module cache
Each module **reads** `profile.yaml`+`continuity.yaml` but **writes only its own**
file (`destiny.yaml` = cached natal chart computed once; `career.yaml` = vectors;
`relationships.yaml` = tracked patterns). This ownership rule prevents modules
from clobbering each other.
