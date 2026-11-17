# Module: Destiny / 命盘 (BaZi 八字 — flagship)

Deliver a **命盘画像**: the person's Four-Pillars chart, computed exactly, then read
as a reflective portrait. This is the flagship — do it with craft. BaZi is the
default and deepest reading here. A **real Western natal chart is also built** now
(`scripts/astro.py --natal`, real Swiss-ephemeris planets + aspects, with
houses/ascendant when birth time+place are known) — see **§6** for when and how to
offer it. Lead with BaZi unless the person explicitly asks for the 星盘/Western chart.

Governing rule (see safety.md): **compute honestly, interpret humbly.** The chart
is fact; the meaning is a lens.

**On the gendered readings.** 子平's vocabulary maps 财 to a wife for a man and 官杀 to
a husband for a woman, and `bazi-life-arc.md` carries those notes because they are what
the tradition says. Deliver them as **the tradition's vocabulary, dated and situated** —
「传统上男命把财这条线也读作伴侣缘」 — never as a prescription about who someone should
partner with or what role they should play. The `birth.gender` field is a calculation
convention for 大运 direction (see onboarding.md); it is not a claim about the person,
and it must not turn into one in the reading.

## 1. Preconditions
- `companion.py brief` shows `birth.date` present and `consent.birth` granted?
  If not → `references/onboarding.md` Tier 1 (ask consent, collect birth block).
  Birth **date** is required; **time** may be unknown (BaZi still works — you just
  omit the hour pillar and flag it).
- **They can have the chart without storing anything.** If they don't want their birth
  data kept, compute straight from what they typed: no `set-profile`, and no `cache
  --module destiny` (the cache holds the pillars, so it needs birth consent and refuses
  without it). Say plainly that nothing was saved and that a later reading will need the
  details again.

## 2. Compute (never by hand)
Read the birth block, then run the flagship script with the profile's frozen
conventions:
```bash
python3 "$D/scripts/bazi.py" \
  --date <birth.date> [--time <birth.time>] --gender <m|f> \
  --tz <birth.tz_at_birth>                     # ← ALWAYS pass this when you have it \
  [--lon <birth.lon> --true-solar-time]        # only if conventions.true_solar_time
  [--early-zishi]                               # only if conventions.zishi_rule == early
  [--time-window <birth.time_window_min>]      # when birth.time_accuracy == approx
  --format json
```
**Boundaries and rough times.** When `birth.time_accuracy` is `approx`, pass
`--time-window <birth.time_window_min>`. The payload's `time_window` lists every pillar
the chart could have inside that window, and `changes` names the ones that actually move:
read those as uncertain and say so; read the rest normally. The ambiguities also flag a
birth within 15 minutes of a 时辰 boundary (naming both 时柱) or of the 日柱's turn (midnight
under 晚子时, 23:00 under 早子时 — naming both 日柱, since the 日柱 carries the 日主), a birth
within a day of any 節 (the 月柱; 立春 has its own note for the 年柱) — or, with no birth
time, a 節 that falls on the birth day as the birthplace counts it — a daylight-saving
birth whose standard-time 日柱 or 时柱 differs, and — when a longitude is known but TST is
off — the 日柱 and 时柱 True Solar Time would give. Pass these on in plain words. They are
the places a chart is least sure of itself, and the usual reason two apps disagree. A
節氣 moment in a note is printed on the birthplace's clock as 当地时间, with 北京时间
beside it; quote the local one to the person.

**`--tz` is not optional for a birth outside China.** 節氣 are absolute astronomical
instants and the engine resolves them on a Beijing clock, so without the birthplace
timezone a European or American birth can come back with the **wrong year or month
pillar** — and the ambiguity note will confidently describe the wrong side of the
boundary. Pass `birth.tz_at_birth` (an IANA name; a plain offset also works). 年柱/月柱
are then compared as absolute instants while 日柱/時柱 stay on the local clock, and the
payload records both frames under `conventions`. With no `--tz` the chart still
computes, but it says out loud that it assumed the birth clock was Beijing time —
surface that to the person rather than letting it pass.

**True Solar Time changes the clock, not the moment of birth.** With `--true-solar-time`
the 时柱 is read off the longitude-corrected clock, and so is the 日柱 when the correction
carries the birth across the 日柱's turn — midnight under 晚子时, 23:00 under 早子时 (the
payload names both 日柱 when it does). 年柱, 月柱, 立春 and 起运 stay on the
real birth instant. TST used to shift that instant too, so switching it on could move
立春 and give a western-China birth a different year pillar and a 大运 running the other
way. Everything the payload derives — 十神, the 五行 tally, 大运, 生肖, 命宫/胎元 — is read
off the pillars it displays; if you ever see them disagree, that is a bug, not a school.

It's deterministic and fast, so recompute freely; the cache described below is for
continuity, not speed. The JSON splits
`computed` (facts) from `heuristic` (the labeled 扶抑 strength guess) and lists
`ambiguities`. **Surface the ambiguities honestly** — unknown time, a 23:00 子时
boundary, or a TST shift all change the read and the user deserves to know.

The `cross_check_sxtwl` field is an independent confirmation of the year pillar
(立春 boundary). **Read its `agrees` field — don't compare the two ganzhi by eye.**
It can disagree for a benign reason: sxtwl works at date granularity, so on the 立春 day
itself it cannot know which side of the boundary a birth *time* falls on. The payload
labels that case (`_disagreement: expected …`) and the main engine, which uses the exact
立春 moment, stands. An **unexpected** disagreement (not on the 立春 day) is pushed into
`ambiguities` as well — when you see it there, say so and treat the chart as uncertain
rather than papering over it. A birth within a day of 立春 also raises its own
`ambiguities` entry: the year pillar hinges on the minute, so the birth time matters
more than usual — surface that.

## 3. Ground the interpretation
Two curated, school-tagged content files back the reading — read the one you need:
- **`data/content/bazi-interpretation.md`** — the quick sketch: day-master by
  element (§A), a line per 十神 (§B), element balance (§C), and **§E = the honesty
  voice** (sanctioned/forbidden language, the "user pushes for a literal year"
  script, fatalistic→honest rewrites). §E governs how everything below is worded.
- **`data/content/bazi-life-arc.md`** — the deep lookup: the full **十神 → 生活层面**
  tables (§1, with gender notes), **宫位 → 人生阶段/六亲** (§2), **五行 → 健康/气质**
  (§3, tendencies not diagnosis), and the **大运 (十神 × 喜忌) → per-dimension recipe**
  (§4) + life-arc framing (§5). This is what powers 分层面 (L2) and 分阶段 (L3).

Build the reading from those + the computed chart. **Name the tradition** ("in 子平
terms…"), never invent quotes, statistics, or precise life predictions. If the notes
don't cover something, stay qualitative or say it's outside what the chart speaks to.

## 4. Deliver the 命盘画像
Open with the one-line disclaimer note (disclaimers.md, destiny). Then, in the
user's `locale`, present two clearly separated parts:

**① 命盘 (computed — the facts)**
- Four Pillars grid (年/月/日/时 → 干支), with the day pillar marked as 日主.
- Day Master: e.g. 阴水（癸）— the "self" anchor.
- Five-element bars (use the `with_hidden` tally; state the weighting scheme).
- Ten Gods on the other stems (+ hidden-stem ten gods for the month, the key one).
- 大运 timeline: 起运 age + the decade pillars, with the *current* 大运 marked;
  plus this year's 流年 pillar.

**② 画像 (interpretive — a reflective, LAYERED lens)**

Build the 画像 as **four progressive layers L0→L3 + drill-down** — each deeper,
more granular, more term-heavy than the last. The reader chooses how far to go, so
"easy to understand" (L0/L1) and "comprehensive" (L2/L3) stop fighting. Keep the
①facts / ②lens split (that's the honesty spine); all the richness goes in ②.
Ground every line in `data/content/bazi-life-arc.md` (dimension + life-arc tables)
and speak in `bazi-interpretation.md §E`'s voice — and in the register of
`references/voice.md`: 大白话在前、术语在后, one idea per sentence, and the honesty
frame said **once** at the top rather than hedged into every clause.

**Read `references/voice.md` before writing the 画像.** The layers below are a
structure for *what to cover and in what order of depth* — they are not a form. L0 in
particular has to sound like a person who just looked at your chart and said one true
thing, which means plain words, no label, and no 「不是X，是Y」.

**Two rules baked into every layer below:**
- **Jargon-gloss rule.** A 十神/五行/扶抑 term appears only in `术语(大白话)` form
  on first use, e.g. `正官(责任、规矩、把自己嵌进体系做好)`、`偏印(靠钻研、悟、偏冷门
  专精的学习方式)`、`比劫(同类、手足、同侪)`. L0/L1 use **zero** terms.
- **Honesty-language rule (from §E).** Use season/agency shapes —「这十年是…的季节」
 「传统上倾向于…」「一种读法是…」「值得留意的是…」「适合…的事」. Never §E-forbidden
  shapes (dated events, 一劫/血光/死, guaranteed 婚/财/离, curses, diagnoses,
  fabricated numbers). Health = tendency + "找医生", never diagnosis.

Top de-noise: fold the disclaimer + archive-settings + birth-echo into ONE small
folded line ABOVE L0 (info kept, not hogging the opening). The real opener is L0.

---

**🪞 L0 · 一句话画像** *(the single most important line — zero jargon, friend-voice)*
One sentence that concentrates the day-master + dominant 十神 into "what kind of
person you are". First-glance payoff for the term-averse reader. It has to sound like
someone who just looked at your chart and said one true thing — so: plain words, no
label, no 「不是X，是Y」, and no dash doing the work a full stop should do.
> 例（癸亥·男）：你想事情想得很久。但认准了就会很实在地一点一点把它做出来，
> 不太声张，也不太回头。

**✍️ L1 · 性格速写** *(3–4 plain lines, still zero jargon)*
`**加粗引导词** + 一句大白话`, each ≤2 lines. What they're *like day to day*.
Vary them: one longer, one very short. Not every line needs three parallel clauses.
> - **想得深**：遇事先在心里过一遍。共情强，代价是容易把别人的情绪也接过来。
> - **有主见**：脑子转得快，像水一样能绕路，但方向是自己定的。
> - **务实**：不爱空谈。答应的事会当真。
> - **在意规矩**：「该做好」这三个字在你心里分量很重。

**🔎 L2 · 分层面** *(the 7 dimensions — first comprehensiveness block)*
Seven skippable blocks — **事业 / 财 / 感情 / 健康 / 家庭 / 学业 / 性格** — each
`**层面名** → 一句结论 → 半句依据(术语就地夹注)`, ≤3 lines, whole-block skippable,
gender-noted where 财/官/食伤 apply. Source each from `bazi-life-arc.md §1`.
> **💼 事业**：适合往深里做、还能被看见的路子。你盘里正官(责任、规矩、把自己嵌进体系里
> 做好)藏得厚，食伤(想表达、想把心里的东西做出来)也在。想靠谱，又想有作品感。
> **💰 财运**：偏稳稳积累那一路。正财(踏实赚取、务实攒钱那条线)清晰，靠专业和时间复利
> 比靠投机更合你。(男命：财这条线也关联伴侣缘。)
> **❤️ 感情**：投入得深，也肯承诺，但心思私密，不太外露。认真型。要留神的是想太多，
> 以及把对方的情绪也一并接过来。
> **🩺 健康(只谈倾向，不诊断)**：你水最旺，水在传统里主思虑、睡眠、情绪，所以最该照看的
> 是「脑子停不下来」。熬夜和反刍是主要消耗口。给思绪挖个出口，比硬扛省。真有担心请找医生。
> **👪 家庭/六亲**：比劫(同类、手足、同侪)有力，同辈和合伙人在你的故事里戏份重。是助力，
> 边界也得自己划。印星偏向偏印(靠钻研、悟、偏冷门专精的学习方式)，靠自己钻研多于被喂养。
> **📚 学业**：自学型。偏印(靠钻研、悟、偏冷门专精)是底色，适合深挖一门，慢慢成专家。
> **🧭 性格(底色)**：日主癸水(这张盘里的「你」，阴水，雨露雾气那种意象)。敏感，想象力强，
> 心思深而私密。有目标的时候这是动力；没出口的时候，容易变成停不下来的盘算。

Then the strength read as **one skippable gray line** (the most term-heavy thing,
demoted out of the body):
> `> 小字·可跳过：按「扶抑」一派估，这盘帮身≈8/耗身≈9、接近中和(near-balanced)——给你`
> `> 出口(表达、扛压、出成果)行，给支持(学习、盟友)也行，不被锁死在单一策略。这只是一种`
> `> 流派的启发，调候/病药等别的读法可能不同，我不替你钉死。`

**🕰️ L3 · 分阶段** *(the life-arc timeline — second comprehensiveness block; the
piece the old output missed entirely)*

> The worked example below is **illustrative formatting only** — its decade pillars are
> not the ones any real chart will produce. Always walk the actual
> `luck_pillars.pillars[]` from the JSON, including the direction (顺/逆行), which
> depends on year polarity × gender.
Walk **every** 大运 decade from `luck_pillars.pillars[]` as a table:
`年龄·干支(白话标签) → 基调一句话 → 最吃重的1–2层面`. Mark the current decade
`👉 当前`. Use the row's `ten_god` for the label and `favor` for valence — **but if
`favor`=平 (near-balanced chart), show the 十神 theme only and do NOT invent a
喜/忌; note that a 偏弱/偏强 chart would carry 喜/忌 per row.** Then give the current
decade +2 lines (基调 + 近期流年 from `upcoming_annual_pillars[]`). Don't expand
every row into prose — that recreates the wall; depth lives in the drill-down.
> | 年龄·大运 | 基调(一句话) | 最吃重的层面 |
> |---|---|---|
> | 3–12 乙卯(食神·表达萌芽) | 爱表达、点子多的童年，启蒙靠好奇心 | 学业·性格 |
> | 13–22 甲寅(伤官·锋芒) | 想法外冒、有点不服管的青春期，才华与叛逆同框 | 学业·性格 |
> | 23–32 癸丑(比肩·自立) | 靠自己站稳的立业期，同辈/伙伴戏份重 | 事业·家庭六亲 |
> | 👉 33–42 壬子(劫财·水旺自我) 当前 | 认准方向、往深里推的季节；自我/独立/协作被放大 | 事业·财运·性格 |
> | 43–52 辛亥(偏印·内省沉淀) | 转向内修与专精，学习滋养多，适合沉下来打磨 | 学业·健康 |
> | 53–62 庚戌(正印+官·收成) | 名望与责任并至的收获期，积累开始变成位置 | 事业·家庭六亲 |
>
> *(本盘近中和，扶抑不给硬喜忌，上面按十神主题读；若为偏弱/偏强，每行会再带 喜/忌。)*
>
> 👉 当前这步(壬子，33–42)：
> - **基调**：一步水运叠在水旺盘上——「往深里推进、认准方向」的好季节；水旺要挖渠，有明确
>   目标和出口时是动力，没出口时容易空转、算个不停。
> - **近期流年**：今年 2026 丙午是火、是正财(务实的成果与收入)被点亮的一年——落到具体、
>   摸得着的成果上会更有共鸣。这是「适合去做」的季节感，不是「你会怎样」的预言。

**结尾 · 下钻入口** *(aligned to L2 dimensions + L3 stages — not three floating options)*
> 想看哪一块更细？点一个我展开：
> 📖 按【层面】深挖 —— 事业/财运/感情/健康/家庭/学业/性格，挑一个
> 🕰️ 按【阶段】展开 —— 任意一步大运(尤其当前33–42)，我细说怎么借势
> 🎯 已经很准的那条 —— 直接说「性格那面镜子最像我」，我顺着聊
> (事业方向我还有专门的职业模块能更系统地做；要的话我接过去。)
> 要不要把这次起盘+画像记进你的私人档案，方便回看？另外，你希望我怎么称呼你？

### The same layers when `locale` is `en`

Every worked example above is Chinese, which made the English path something the model
had to improvise. It shouldn't be — the layers, the gloss rule and the honesty voice
all carry over verbatim. **BaZi keeps its Chinese terms** (SKILL.md's Language rule);
what changes is that the gloss now does double duty, translating *and* explaining:
`正官 (Proper Officer — responsibility, structure, doing it right inside a system)`.
Keep the pillars, 十神 and 大运 labels in 汉字 with pinyin on first use — transliterating
them away ("the Direct Officer star") loses the reader's ability to look anything up.

> *The chart itself is computed by traditional rules (a reproducible fact); how we read
> it is a cultural lens for self-reflection — not a scientific prediction. You decide.*
>
> **🪞 L0 · In one line**
> You take a long time to commit to something. Once you have, you're very hard to
> deflect, and you'd rather build the thing properly than quickly.
>
> **✍️ L1 · Quick sketch** *(plain words, zero terms)*
> - **You think before you feel out loud.** Strong empathy. It costs you, because other
>   people's moods tend to come home with you.
> - **Independent-minded.** Quick to adapt. Not easily talked off a direction.
> - **Practical about value.** You'd rather compound something real than chase a spike.
>
> **🔎 L2 · By life area** *(each ≤3 lines, skippable, gloss on first use)*
> **💼 Work** — suits the deep-specialist path that still gets *seen*. Your chart
> carries 正官 (zhèng guān, "Proper Officer" — responsibility, structure, doing it right
> inside a system) in the hidden stems, alongside 食伤 (shí shāng — the urge to express,
> to make the inside thing exist outside). Reliable *and* wanting a body of work.
> **🩺 Health (tendencies only — not a diagnosis)** — 水 (water) runs strongest here,
> and in this tradition water governs rumination and sleep. The thing worth minding is
> a mind that won't stop. If something actually worries you, see a doctor.
>
> *(small print, skippable)* On the 扶抑 (fú yì — "support/restrain") reading, this
> chart sits close to balanced. That's one school's rule of thumb, and 调候/病药 schools
> may read it differently — I'm not nailing it down for you.

Note what does *not* change in English: the ①facts / ②lens split, one disclaimer at the
top, tendency-and-agency verbs ("tends to", "worth noticing", "a season for"), and the
hard refusal to name events or dates. `selfcheck.py` checks the English shapes too
("you will definitely…", "destined to", "likely to get sick").

When the user takes a 【层面】or【阶段】offer, expand with the FULL `bazi-life-arc.md`
§4 recipe (十神 register × favor valence × age-band × 流年 weather) — richly, but
still in §E's voice: **detail from symbolism, never from invented events/dates.**
If they push for a literal year ("到底哪年结婚/发财"), run the §E5 three-beat
(name the want → give the season → kindly decline the fabricated specific).

**One honest caveat** where the chart is uncertain (unknown time → no hour pillar;
23:00 子时 or 立春 boundary; TST shift) — surface from the JSON `ambiguities`.

## 5. Comprehensive AND human-sized — the layers are how
The user wants depth (各阶段各层面) *and* readability. Don't choose — that's exactly
what L0→L3 is for: the opening lands in plain words (L0/L1), the comprehensiveness
lives in skimmable blocks and a timeline (L2/L3), and anything deeper is one
drill-down away. So: never a wall of prose, but never skip a dimension or a decade
either. Make each block short and skippable; let *structure*, not *omission*, keep
it digestible. If a section would balloon, compress it to its one-line essence and
offer to expand — the chart is theirs to revisit, so there's no need to cram
everything into one message.

## 6. Western natal chart (星盘 — real ephemeris, built)
Offer this when the person asks for a **星盘 / natal chart / astrology reading** (not
八字). It is a genuine astronomical chart, not a fake — same honesty spine as BaZi:
the sky is fact, the meaning is a lens.

**First, backfill coordinates if missing.** If `birth.place` is known but
`birth.lat`/`birth.lon`/`birth.tz_at_birth` are null (older profiles, or onboarding
that only got the city name), **derive them from the place and persist via
`set-profile` before computing** — otherwise the Ascendant/houses can never compute.
City coordinates and the UTC offset in effect at that date are public reference facts,
not fabrication; `tz_at_birth` must reflect any historical DST/zone in force then (see
`onboarding.md` Tier 1). Only truly leave them null if the place itself is unknown.

```bash
python3 "$D/scripts/astro.py" --natal \
  --date <birth.date> [--time <birth.time>] \
  [--lat <birth.lat> --lon <birth.lon> --tz <birth.tz_at_birth>]   # for 上升/宫位
  --format json      # or text for a quick human view
```
`--tz` takes the **IANA zone name** straight from the profile (`Asia/Shanghai`) — it
resolves the historical offset for that birth moment itself and records how in
`caveats`. A bare hour offset still works. Don't compute the DST offset by hand.

**What it computes (facts):** all ten bodies + North Node in sign & degree, natal
retrogrades, the major natal aspects, and — **only when birth time + place + tz are
all known** — the Ascendant, Midheaven, and Placidus house cusps.

**Honest degradation is the whole point — read the JSON `caveats` and state them:**
- **No birth time** → the Moon is flagged `approximate` (it moves ~12–15°/day, so its
  sign can be wrong) and there is **no Ascendant/houses**. Say so; don't guess a rising.
- **No birth place (lat/lon)** or **no tz** → **no Ascendant/houses** (they're
  place- and exact-time-specific). Planets-in-signs still hold for the slow bodies.
- Never fabricate a rising sign, a house placement, or a "your Moon is definitely X"
  when the data can't support it. Omit, and name what's missing (a birth time / place
  / timezone would let you compute it).

**Read `caveats` every time.** It now also carries: the resolved timezone and how it
was derived, a birth clock that **never existed** (spring-forward gap) or that **ran
twice** (autumn fall-back — an hour of doubt moves the Ascendant ~15°), and a Moon
sitting within ~1.5° of a sign boundary. Those are exactly the cases where a confident
sentence would be wrong.

**Interpretation** = same rules as everywhere: Sun/Moon/Rising and aspects are a
reflective, cultural lens — "one way to read this", agency language, no fatalism, no
event/date prediction, no fabricated authority. Glossed plain-language on first use,
just like the 十神 gloss rule. If asked to compare with the BaZi, treat them as **two
independent symbolic languages** describing the same person — note where they rhyme,
never claim one "proves" the other.

## 6b. 紫微斗数 (`ziwei.py`) — built, with a stated confidence gap

Offer this when they ask for **紫微 / 斗数 / 命宫** by name. It is a third symbol system
beside BaZi and the Western chart, not a better one.

```bash
python3 "$D/scripts/ziwei.py" --date <birth.date> --time <birth.time> \
                            --gender <m|f> --tz <birth.tz_at_birth> \
                            [--on-year 2026] --format json
```

**The birth hour is mandatory here** — 命宫, 身宫, 文昌文曲, 火铃, 地空地劫 all hang off
it. With no hour the script returns **no chart at all** rather than an empty grid, and
says so; pass that on and offer BaZi instead, which still reads without an hour pillar.

**What it computes:** 十二宫 with their stems, 命宫/身宫, 五行局 (taken from the 命宫
纳音 via lunar-python's own table), all 14 主星 by the 安星法, 六吉六煞禄马, 生年四化,
and 流年命宫.

**What it does NOT compute — say so, don't improvise:** 大限/小限 progression,
宫干四化 (飞星), the long tail of 杂曜, and 三方四正 as an interpretive method. This is
also why there is still **no 紫微 daily layer** in the daily-fortune card.

**The chart is cast on the birthplace's own clock.** The lunar day and the 时辰 come from
the birth date and time as recorded where they were born, the clock the 八字 时柱 uses too:
14:20 in Amsterdam is 未时, not the Beijing hour it happened to be. (This engine used to
convert a birth abroad to Beijing time first, which moved 命宫 and every star with it;
practitioners cast a birth abroad on its local time.) Still pass `--tz`: the chart does
not move with it, but it is how the engine knows daylight-saving time was in force, and
then it names the 时辰 standard time would give. Surface that note.

**The year stem comes from the LUNAR year, not 立春.** 斗数 places 命宫 and 紫微 from the
lunar month and day, so its year turns at 春节; 立春 is BaZi's boundary. A birth in the
window where the two disagree gets an explicit ambiguity naming both, because a minority
of schools do use 立春 and the year stem drives 四化/禄存/天魁天钺/火铃.

**An impossible date is refused, not charted.** Feb 30 used to roll silently into March
and come back as a complete, confident 命盘.

**⚠️ Be honest about the confidence gap.** BaZi has an independent cross-check
(sxtwl); this engine has none — there is no second ZWDS implementation available here.
`--selftest` verifies the implementation against the rules, including the published
紫微星定位表, but it cannot verify that every rule was transcribed correctly. A mutation
sweep showed how weak that was on its own: of nine deliberate 安星 errors it caught one,
because the invariants checked that the right SET of stars existed, not where they
landed. `tests/fixtures/ziwei_golden.json` now pins placements across all ten year
stems and catches 12 of 12 such mutations — but it was generated by this engine, so it
guards against regressions, not against a table transcribed wrong in the first place. The payload
carries `verification.independent_engine_cross_check: false`. **Lead with 八字** unless
they asked for 紫微 by name, and if they're weighing the two, say which one rests on a
cross-checked engine.

**Reading it** is the same discipline as everywhere: where a star sits is the fact;
what 紫微 or 破军 *means* is a register (`heuristic.star_registers` gives one line each),
glossed on first use like 十神, framed as a lens. 化忌 is not a curse and an empty 宫
is not a void — say what the tradition reads there and hand back the agency.

## 7. 合婚 — two charts side by side (`synastry.py`)

They will ask. 「我俩合不合」/「属相不合怎么办」 is one of the most common things anyone
brings to 命理 — and it is **the place this tradition does the most real damage**, because
a 属相不合 verdict has ended relationships that were fine. So this is built as a
one-way valve: the traditional relations are computed honestly, and the verdict is
unavailable.

```bash
python3 "$D/scripts/synastry.py" --a <A date> [--a-time HH:MM] --a-gender m --a-tz <A's birthplace zone> \
                               --b <B date> [--b-time HH:MM] --b-gender f --b-tz <B's birthplace zone> \
                               [--a-lon … --b-lon … --true-solar-time] [--early-zishi] --format json
```
Give each side the same timezone and conventions you would give bazi.py for that person.
Without them the comparison assumed both births were on Beijing time, so an overseas
partner's 属相 cell could differ from their own 命盘. Each side's warnings come back
labelled A： / B：.
Consent-gate the partner's birth data first (`relationships=yes`), and only use what
was volunteered — a third party never consented to being charted.

**What it computes (facts):** every traditional branch relation between the two charts,
pillar by pillar — 六合 / 三合 / 半合 / 三会 / 六冲 / 六害 / 六破 / 相刑 / 自刑, with the
pair that produced it; the 十神 each day master is to the other; and the two element
tallies side by side. All tables are listed in full in the script so anyone can check
them against a 子平 text.

**What it will not give you, by construction:** there is no 合/不合 field, no score, no
percentage, no recommendation. Do not synthesize one — `selfcheck.py --module synastry`
blocks it, including the 克夫/旺夫 register and «你们天生一对».

**How to deliver it**
- Report each relation as a **texture to notice**, in the tradition's own voice:
  「日支亥巳冲——传统上读作张力与推拉。冲不等于坏；很多长久的关系正是靠这股张力保持清醒。
  它说的是这段关系需要更多明说，不是它会散。」
- **A 冲 or 害 is never a reason to leave or not to start.** If they are already using
  the chart that way, that is safety.md §1 rule 7 firing — say so plainly and hand the
  question to `relationships.md`, which works from what actually happened between them.
- **When they ask about 属相 specifically:** 年支 is one of four pillars, and the
  tradition itself never decided a marriage on it alone. Say that, then offer the fuller
  read if they want it.
- Both charts carry their own ambiguities (unknown time → no hour pillar); the script
  merges them. Surface them — half a comparison is not a comparison.
- Close by handing it back: whether two people do well together is made of what they
  do — how they repair, whether they want the same decade. No arrangement of 干支
  knows that.

## 8. Where this lens stops
The 命盘 speaks to 事业, 感情, 财 — and there are modules that own those questions with
real data (career.md) or with their own logged record (relationships.md). The split is
in SKILL.md ("When two lenses touch the same question"); the short version:

- **Rhyme freely.** "This and your interest profile are saying the same thing in two
  languages" is a good line, and true.
- **Certify never.** The chart cannot make a career result more reliable, and 大运 is
  not grounds for taking a job, leaving someone, signing, moving, or spending.
- **Watch for the reverse.** The rigour of the computation — real 节气 boundaries, an
  sxtwl cross-check — makes a non-predictive reading *feel* like grounds for a decision.
  That's exactly when to say it isn't (safety.md §1 rule 7) and hand it over.

## 9. Remember what you already told them
`state/modules/destiny.yaml` (birth consent only — a chart computed without storing is
never cached) exists for this and was going unused — which is why a
second reading weeks later could contradict the first, and why the entry disclaimer got
repeated as if you'd never met. After delivering a 命盘, cache it:

```bash
companion.py cache --module destiny --merge-json '{
  "chart": {"pillars":"癸酉 丙辰 癸亥 丙辰","day_master":"癸","computed_on":"2026-08-22",
            "conventions":{"true_solar_time":false,"zishi_rule":"late"}},
  "delivered": [{"id":"reading-2026-08-22","layers":["L0","L1","L2","L3"],
                 "one_liner":"<the L0 line you actually gave>",
                 "drilldowns":["事业"],"disclaimer_given":true}]
}'
```
Read it back at the start of any destiny turn (`companion.py cache --module destiny`):

- **The chart is deterministic — but only under the same conventions.** If the cached
  `conventions` differ from what you're about to run (TST toggled, 早/晚子时 changed),
  the pillars may legitimately change: say so explicitly rather than quietly serving a
  different chart than last time.
- **Don't repeat what landed.** If L0/L1 were given, open by *building on* the one-liner
  they already have, not by re-deriving it. Go to the layer or dimension they haven't
  seen.
- **The disclaimer is once per context**, not once per message. `disclaimer_given`
  is how you know.
- If birth data changed or `forget --birth` ran, the cache is stale — drop it.

## Honesty checklist (before sending)
- Facts and lens visibly separated? Disclaimer note present once?
- Any life prediction, illness/marriage/wealth certainty, or fabricated figure? →
  remove or reframe as tendency.
- Ambiguities from the JSON surfaced? Agency language throughout?
- Natal chart: if `birth.place` was known but coords were null, did I backfill
  `lat`/`lon`/`tz_at_birth` (so Ascendant/houses can compute) rather than silently
  shipping a chart with no houses? Did I read `caveats` and state every omission
  (rising/houses/Moon) instead of guessing?
- Did I read `cross_check_sxtwl.agrees` (not eyeball the two ganzhi), and surface any
  立春-proximity ambiguity?
- **Machine backstop:** `python3 "$D/scripts/selfcheck.py" --module destiny --file draft.md` — exit 1 means a blocker; fix it before sending. Passing is not proof it's honest, only that it's free of the known bad shapes.
