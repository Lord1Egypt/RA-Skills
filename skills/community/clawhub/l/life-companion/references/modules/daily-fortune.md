# Module: Daily fortune & check-in (每日运势)

The recurring companion hook — and a **rich, multi-system** daily reading, the way
market 运势 products are (西方星座 · 八字流日 · 生肖 · 五行), but with the skill's
line held: **every layer is computed from a real system (八字/生肖 traditional
rules, real astronomy) and labeled; interpretation is reflective, never a
prediction; and nothing is fabricated** — no invented "综合运 ⭐⭐⭐⭐", no made-up
lucky number. What makes it *yours* rather than a generic horoscope is that it's
woven with your journal + continuity. Pairs with `references/journaling.md`.

## Flow
1. **Safety + continuity first, always.** `companion.py brief` gives continuity +
   the last few entries in one call; add `trend --days 14` / `journal --since …` when
   you want the fuller picture. A heavy entry → care, not fortune (safety.md). If `brief`
   carries `_wellbeing_check` — two weeks of mostly low moods — don't open with a card at
   all: journaling.md, "When the low lasts".
2. **Compute the day from real systems** (never hand-compute):
   ```bash
   python3 "$D/scripts/bazi.py"  --date <birth.date> [--time <birth.time>] --gender <m|f> \
     --tz <birth.tz_at_birth> \
     [--lon <birth.lon> --true-solar-time] [--early-zishi] \
     [--time-window <birth.time_window_min>] \
     --on-date today --format json     # → computed.daily: 流年/流月/流日 十神+favor,
                                        #   zodiac_day (生肖 vs 日支), wuxing_tips
   python3 "$D/scripts/astro.py" --date <birth.date> [--time <birth.time>] \
     --tz <birth.tz_at_birth> \
     --on-date today --format json     # → 星座/双鱼…, 今日月亮星座, 逆行, 本命相位
   ```
   Pass the chart conventions exactly as destiny.md §2 does: `--lon … --true-solar-time`
   only if `conventions.true_solar_time`, `--early-zishi` only if `conventions.zishi_rule` is
   early, `--time-window` when `birth.time_accuracy` is `approx`. The day is then read
   against the chart the person was shown, not a second one. With a window, a
   `natal_relations` row or `zodiac_day` marked `uncertain` rests on a pillar the rough
   time can't settle: say so, or leave it out.
   Read `data/content/bazi-life-arc.md §1` for the 十神→dimension mappings that turn
   the 流日/流月 十神 into per-life-area reads. No birth data → skip charts, keep it
   journal + a general seasonal note; never fake a chart. `favor` is `平` for a
   near-balanced chart → read the 十神 theme, don't manufacture 宜/忌 or 五行 tips.

3. **Read yesterday before writing today.** This is the one module that runs *daily*,
   so its real failure mode isn't inaccuracy — it's **saying the same thing again**, at
   which point it becomes the cookie it was designed not to be. `companion.py brief`
   already returns the recent entries; the `> companion:` line in each one records what
   you actually said. Skim the last 2–3 before drafting, then:
   - don't reuse yesterday's 基调 wording, its 宜/忌 pair, or the same callback;
   - if the computed layers genuinely repeat (流日 十神 often does within a week), say
     so honestly — 「跟前天是同一路的日子」 — and change what you *do* with it (a
     different dimension, a shorter card, a question instead of advice);
   - if you nudged the same open thread yesterday, don't nudge it again today.

## Deliver — the daily card (rich but scannable; ~a screen, not an essay)

**Read `references/voice.md` before writing this.** The layer list below is what to
COVER, not a template to fill — the previous version of this section read as a form
because it was written as one, and the wording is what gives that away (emoji and
headers are fine).

Three things that matter more than the list:
- **Lead with whatever actually stands out today**, in a plain sentence. Not with a
  section header, and not with the background you already gave them.
- **Skip a layer that has nothing in it.** A dimension covered because the template had
  a slot for it is the most obvious filler there is. Saying 「生肖那层今天完全没动静」
  is better than manufacturing a line about it.
- **Vary the sentences.** At least one fragment per card. 「就这样。」

Open with a one-line disclaimer note once, then, in the person's `locale`/`tone`:

- **🌤 今日基调** — one line from the **流日** 十神 + `favor`, woven with the day's
  overall lean. (e.g. 流日 劫财[喜] = 借力/补给的一天.)
- **🔮 分层面** — 事业 / 财 / 感情 / 健康, each ONE short line: map the **流日 (+流月)**
  十神 onto that dimension via `bazi-life-arc.md §1`, and show the lean as **喜 ↑ /
  平 → / 忌 ↓** — clearly the *disclosed 扶抑 heuristic*, **NOT a cosmic score or a
  star rating**. (Gender-note 财/官/食伤 where relevant.)
- **🐯 生肖今日** — from `zodiac_day`: 属X · 今日与日支的关系 (`relations`: 六合/半合/三会/冲/
  害/破/刑/自刑, each with a one-line `reading`) → its `tone`. A real traditional relation,
  not vibes, from the same table as `natal_relations`, so it always matches that year row.
- **🪢 今天和你的四柱** — from `natal_relations`: the day's branch against each of the
  person's own pillars (年/月/日/时), by the same 六合/三合/三会/冲/害/破/刑 tables 合婚 uses,
  plus `same_pillar` when the day repeats one of their pillars exactly (伏吟). **Report only
  the rows marked `notable`**: 冲, 合 or 伏吟 on the 日支 (closest to the person in daily
  life) or the 月支 (work and rhythm). Some relation lands somewhere in the four pillars on
  almost every day (29.5 of 30, measured over 186 near-balanced charts), so listing them all
  says nothing; notable rows land on about 10 days a month. On a day with none, say plainly
  that nothing notable moves in 日支 or 月支 today, and don't reach for a 半合, 害 or 破 to
  fill the space. **For a near-balanced chart — every 喜/忌 is 平 and the 五行 tips are
  empty — a notable row is the day's real signal.** Read it as texture
  ("今天的地支冲你的日支，传统上读作贴身那一格被摇动"), never as an event. The other rows stay in
  the data for when the person asks.
- **♓ 星座今日** — from astro.py: X座 · **今日月亮在…座** · any **逆行**(水逆 etc.) ·
  notable **本命相位**. Frame the positions as astronomical fact, the meaning as a
  reflective lens ("水逆传统上提醒…沟通/复盘慢一点" — never "水逆导致你…").
- **🎨 五行小贴士** — `wuxing_tips`: the colours, directions and numbers that go with the
  person's 喜用五行 by the traditional correspondence, always with its `note`. Name them as
  that, not as luck: 「颜色 青/绿，方位 东，五行数 3、8（按你喜用五行的传统对应，图个彩头，不是保证）」.
  Never write the label 「幸运数字」: it reads as a promise, and the gate blocks it. If tips
  are empty (中和), say so; don't invent.
- **✅ 宜 / ⛔ 忌** — 2–3 agency-framed nudges synthesized from the above (a repair,
  a rest, a "别拍板大事" when 冲/刑). Never a lucky-number command, never fatalism.
  Write these as things a friend would say, not as almanac entries: 「收尾比开新战线
  划算」 lands; 「宜静养，忌远行」 is a 黄历 impression of one.
- **💬 结合你近况** — one earned callback to a recent journal entry/thread. This is
  the differentiator; without it, it's just a cookie.

When the systems **agree**, say so (it lands harder); when they **disagree** (e.g.
八字流日[喜] but 生肖刑害), **say that honestly** — "有借力也有磕碰,混着来" — don't
paper over it into a fake single verdict.

Say the mixed verdict once and plainly. Resist the 「不是好日子也不是坏日子，而是…」
shape — it's the most-flagged construction in `voice.md`, and 「混着来」 already said it.

## Guardrails
- Disclaimer once. Systems are real (八字/生肖 rules, real ephemeris); meanings are a
  reflective lens, not prediction (safety.md rule 1). The daily lens is exempt from
  §1 rule 6's "verify" duty — it's reflective, not a checkable external fact.
- **No fabrication:** no invented 综合运 score/stars, no lucky number that isn't the
  labeled 五行-derived 彩头, no "the stars will make you…". The per-dimension lean is
  the 扶抑 heuristic, labeled.
- Never fatalistic; agency language; keep it woven with the journal.
- Coverage now: **八字流日 · 生肖 · 西方星座(真实天文)· 五行**. A 紫微 chart now exists
  (`ziwei.py`), but a 紫微 **daily** layer needs 大限/流年宫位 progression that the engine
  deliberately does not compute — so it is still not in the daily card. If they ask, say
  that plainly: the natal 紫微盘 is available (destiny module), the daily layer isn't.
  Don't improvise one out of the natal chart.
- Close the loop: offer to log the day (`add-entry`, with your reflection), and offer
  a deeper drill-down on any layer. Keep it a daily touch — rich, but not exhausting;
  if they want the quick version, give just 基调 + 宜/忌.
- **Machine backstop:** `python3 "$D/scripts/selfcheck.py" --module daily --file draft.md` — exit 1 means a blocker; fix it before sending. Passing is not proof it's honest, only that it's free of the known bad shapes.
  (Invented 综合运 stars and lucky numbers are the two things it catches most often here.)
