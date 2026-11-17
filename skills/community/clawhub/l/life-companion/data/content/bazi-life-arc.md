# BaZi life-arc & dimensions (十神 × 宫位 × 五行 × 大运/流年)

The deep-lookup layer for `modules/destiny.md`, sibling to `bazi-interpretation.md`.
Division of labor: `bazi-interpretation.md §A/§B/§C` = the quick sketch (day-master,
a one-line 十神 each, element balance); **this file = the full dimension tables +
the 大运/流年 reading recipe**; `bazi-interpretation.md §E` = the honesty voice,
sanctioned/forbidden language, and the "push for a literal year" script. Read §E
alongside this — every mapping here is spoken in §E's voice.

> **Framing contract.** Everything below is TRADITIONAL, REFLECTIVE association
> (子平/传统) — *倾向、季节、底色*, never a fabricated event, date, or certainty.
> The engine's numbers (四柱/十神/大运/喜忌) are reproducible; every mapping here is
> *interpretation*. Health mappings are temperament/lifestyle mirrors, **never
> diagnosis**. Where schools disagree, the split is labeled `[school: …]`.

> **Engine hooks (exact fields consumed).** Per pillar: `ten_god_gan` (透干十神),
> `ten_god_hidden` (藏干十神). Per 大运 decade (`luck_pillars.pillars[]`):
> `ganzhi`, `start_age`/`end_age`/`start_year`, `gan_element`, `zhi_main_element`,
> **`ten_god`** (大运干 vs 日主), **`favor`** (喜/忌/平), plus secondary
> **`zhi_ten_god`**/**`zhi_favor`** (大运支本气). Per 流年:
> `current_annual_pillar` + **`upcoming_annual_pillars[]`** (`civil_year`,
> `ganzhi`, `ten_god`, `favor`). Balance from `heuristic.strength` +
> `heuristic.favor_sets`; elements from `element_tally.with_hidden`; auxiliaries
> from `extras` (`mingong`/`shengong`/`taiyuan`). Sections 1 & 4 are the core
> lookups; 2, 3, 5 supply the overlay.

---

## 1. 十神 → 生活层面 (Ten Gods → Life Dimensions)

The Ten Gods are the *relationship* between the day master (日主) and every other
stem — the richest interpretive layer. Read each 十神 as a **register of energy**,
localize it by which pillar/宫位 it sits in (§2), and let the surrounding 大运
`favor` make it 喜 or 忌 (§4).

**Gender key (子平 convention, used throughout):**
- **男命:** 财 (正/偏) = 妻/女性缘 & money; 官杀 = 事业压力 & 子女 (古法; 部分流派用食伤).
- **女命:** 官杀 (正官/七杀) = 夫/男性缘; 食伤 = 子女 & self-expression.
- 印 = 母/长辈/庇护 (both); 比劫 = 兄弟姐妹/同辈/竞争者 (both).

### 比肩 — "Peer / Parallel Self" · 同我·同性
- **性格:** independent, self-reliant, principled, stubborn; strong sense of fairness; dislikes control.
- **事业:** partnerships among equals, teams, self-employment; competes head-on; weak at deference.
- **财:** 分财/破财 tendency — money shared, split, competed for; guarantor risk. When 身弱, instead *helps hold* wealth (帮身担财).
- **感情:** 男命 heavy 比劫 → 争妻/克妻倾向; both — strong friendships, hard to fully merge.
- **健康:** robust baseline; injury from overexertion; stress from stubbornness.
- **六亲/家庭:** 兄弟姐妹/朋友宫; peer bonds or rivalry.
- **学业:** self-taught, own-interest-driven; independent over group study.

### 劫财 — "Rob Wealth / Shadow Peer" · 同我·异性  *(stronger, more volatile 比肩)*
- **性格:** bold, enterprising, sociable but impulsive; risk-taking, magnetic; can be reckless.
- **事业:** entrepreneurship, sales, competitive/speculative fields.
- **财:** the classic **破财星** — dramatic gains AND losses; speculation pull. 男命: strongest 夺财/克妻 signal of all Ten Gods.
- **感情:** 男命 — sharpest spouse-competition marker; both — intense but unstable attractions.
- **健康:** high vitality but accident/overreach prone.
- **六亲:** siblings/peers who both help and drain.

### 食神 — "Eating God / Gentle Output" · 我生·同性  *(the gourmet/artist star)*
- **性格:** easygoing, warm, expressive, epicurean; creative, optimistic, tolerant.
- **事业/才华:** art, food, performance, teaching, R&D, writing, wellness; steady productive output.
- **财:** **食神生财** — the healthy money engine: earnings via talent & enjoyment; slow, sustainable.
- **感情:** affectionate, generous; **女命 食神 = 子女星** (gentle motherliness).
- **健康:** the "good appetite/longevity" star (食神有寿元之说); risk = overindulgence (food, comfort, weight).
- **学业:** talent that flows; performance, aesthetics, applied creativity.

### 伤官 — "Hurting Officer / Fierce Output" · 我生·异性  *(brilliant, unruly)*
- **性格:** clever, articulate, proud, rebellious, artistic; low tolerance for authority; witty and cutting.
- **事业/才华:** the **genius/star-quality** marker — performance, design, tech, litigation, entrepreneurship. Chafes in hierarchies.
- **财:** **伤官生财** — potent, fast wealth via talent/reputation; volatile, reputation-linked.
- **感情:** **女命 伤官见官 = classic caution** re: 夫星 (伤官 attacks 正官=husband) → traditionally read as friction/high standards, NOT a verdict `[school: 伤官配印 or 伤官生财 read as redeemed]`. 男命: charming, restless.
- **健康:** intense, "burns bright"; nervous/expressive overdrive; injury from overreach.
- **学业:** brilliant, unconventional, exam-strong when interested, allergic to rote.

### 正财 — "Proper Wealth" · 我克·异性  *(orderly, earned)*
- **性格:** practical, thrifty, reliable, realistic; values stability & fairness; hardworking.
- **事业/财:** **steady salaried/earned income**, budgeting, tangible assets; the "safe money" star.
- **感情:** **男命 正财 = 正妻/正缘** — the marriage/wife star: stable, committed; well-placed = harmonious prospect.
- **健康:** grounded, temperate; risk = overwork/tightness.
- **六亲:** 男命 妻星; both — 父星 in one school (财为父).
- **学业:** methodical, practical/applied/commercial subjects.

### 偏财 — "Windfall Wealth" · 我克·同性  *(fluid, expansive)*
- **性格:** generous, sociable, opportunistic, worldly; good with people & openings.
- **事业/财:** **business, deals, investment, side-income, windfalls**; wide money-reach, entrepreneurial.
- **感情:** **男命 偏财 = 情缘/异性缘** — romance, popularity `[school: 偏财重 → 风流 tendency, reflective only]`.
- **健康:** energetic, indulgent; overextension.
- **六亲:** **男命 父星** (偏财为父 = more common attribution than 正财).
- **学业:** broad, socially/commercially oriented learning.

### 正官 — "Proper Officer" · 克我·异性  *(order, status, responsibility)*
- **性格:** disciplined, principled, dutiful, respectable; law-abiding, self-controlled.
- **事业:** **the career/status/管理 star** — promotion, official position, reputation, working within systems; public/corporate ladders.
- **财:** wealth via position & steady advancement (财旺生官).
- **感情:** **女命 正官 = 正夫/正缘** — the husband star: stable, responsible; well-placed = orderly marriage.
- **健康:** disciplined but pressure-carrying; stress from responsibility & self-imposed standards.
- **六亲:** 女命 夫星; **子女星 in classical (官杀为子女)** `[school: many modern schools use 食伤=子女]`.
- **学业:** conscientious, exam/credential-oriented achiever.

### 七杀 (偏官) — "Seven Killings" · 克我·同性  *(raw power, pressure, drive)*
- **性格:** decisive, courageous, aggressive, charismatic; thrives under pressure; can be domineering.
- **事业:** **power, competition, crisis, command** — military/police, surgery, high-stakes leadership, athletics. Needs 制化 (食神制杀 / 杀印相生) to be constructive; unrestrained = self-destructive pressure.
- **财:** high-risk/high-reward, wealth through boldness.
- **感情:** **女命 七杀 = 偏夫/情缘/强势伴侣** — intense, magnetic, sometimes turbulent; 官杀混杂 cautions relational complexity `[reflective]`.
- **健康:** the sharpest **stress/injury/overdrive** register when 忌.
- **六亲:** 男命 子女星 (classical); rivals; demanding authority figures.
- **学业:** driven under pressure, competitive exams, nerve-demanding disciplines.

### 正印 — "Proper Seal / Nurture" · 生我·异性  *(support, learning, protection)*
- **性格:** kind, scholarly, receptive, patient; principled, traditional; nurtured & self-nurturing.
- **事业:** **the study/credential/庇护 star** — education, academia, licenses, knowledge work, care roles; advancement via qualifications & integrity.
- **财:** wealth via knowledge & credentials (steady, not speculative); 印 also *drains* 财 (贪财坏印 caution).
- **感情:** supportive, home-loving; strong maternal bond; 印重 can mean over-reliance/delayed independence.
- **健康:** the **support/庇护 & longevity** register — rest, recovery. 身弱喜印 = restorative.
- **六亲:** **母星/长辈/贵人** (primary mother star).
- **学业:** the strongest **学业** marker — scholarship, degrees, deep learning, memory.

### 偏印 (枭神) — "Indirect Seal / Owl" · 生我·同性  *(unconventional insight, detachment)*
- **性格:** intuitive, original, introspective, skeptical; sharp specialized mind; can be aloof, restless, self-doubting.
- **事业:** **specialist/技术/玄学/偏门 knowledge** — research, tech, medicine, arts, metaphysics, niche expertise.
- **财:** irregular, project-/expertise-based; 偏印夺食 caution (枭神夺食: undermines the 食神 engine → interrupted output, appetite dips).
- **感情:** somewhat detached, values space; unconventional bonds.
- **健康:** irregular rhythms — appetite/sleep/digestion sensitivity (枭夺食 mirror); introspective stress.
- **六亲:** secondary mother/step-parent; **女命 偏印重 traditionally cautioned re: 子女缘** `[reflective]`.
- **学业:** deep, self-directed, unconventional/specialized study; philosophy, metaphysics, R&D.

**Quick index (engine-facing):**

| 十神 | 关系 | 男命六亲 | 女命六亲 | 首要层面 |
|---|---|---|---|---|
| 比肩 | 同我同性 | 兄弟/朋友 | 姐妹/朋友 | 独立·竞争·分财 |
| 劫财 | 同我异性 | 兄弟(夺财) | 姐妹(夺财) | 冒险·破财 |
| 食神 | 我生同性 | (福) | 子女 | 才华·财源·享受 |
| 伤官 | 我生异性 | (才) | 子女·克夫星 | 才气·叛逆·生财 |
| 正财 | 我克异性 | **妻**·父 | 财·父 | 正财·稳定 |
| 偏财 | 我克同性 | **父**·情缘 | 财·父 | 商财·异性缘 |
| 正官 | 克我异性 | 子女(古)·事业 | **夫**·事业 | 事业·地位 |
| 七杀 | 克我同性 | 子女(古) | 偏夫·情缘 | 权力·压力 |
| 正印 | 生我异性 | **母**·长辈 | **母**·长辈 | 学业·庇护 |
| 偏印 | 生我同性 | 母(偏) | 母(偏)·克子星 | 偏学·技艺·孤 |

---

## 2. 宫位 (柱位) → 人生阶段与六亲

Each pillar is a **spatial-temporal palace** — a life period AND a class of
relationships. Overlay §1's 十神 onto the pillar it occupies to localize meaning.

| 柱 | 年龄段 | 六亲/关系 | 层面重点 | 别称 |
|---|---|---|---|---|
| **年柱** | 0–15岁·幼年·根 | 祖辈·父母·家世·大环境 | 家族根基、早年环境、祖业 | 根·祖上宫 |
| **月柱** | 16–30岁·青年·苗 | 父母·兄弟·师长 | 成长环境、事业根基、性格养成 (月令=格局/旺衰之源) | 苗·父母兄弟宫·提纲 |
| **日柱** | 31–45岁·中年·花 | **日干=自己 / 日支=配偶** | 自身·婚姻·核心性格 | 花·夫妻宫 |
| **时柱** | 46岁+·晚年·果 | 子女·下属·晚辈 | 子女缘、晚景、收成、退休 | 果·子女宫 |

**Refinements:**
- **日支 (夫妻宫)** = most-weighted marital indicator; read `ten_god_hidden` of the day pillar + its `favor`.
- **月令 (月支)** = the **格局 & 旺衰 pivot**; the engine's whole 扶抑 heuristic traces here. Extra weight.
- **命宫 (`extras.mingong`):** supplementary inner-disposition/underlying-theme overlay; some schools use it for career inclination `[school: strong in 三命/紫微-influenced, lighter in pure 子平]`.
- **身宫/胎元 (`extras.shengong`/`taiyuan`):** minor auxiliaries — later-life/physical tilt & pre-natal root. Faint background color only.
- **Pillar × 十神 rule of thumb:** a 十神's story concentrates at its pillar's age-band. 财 in 年月 = early/inherited wealth & (男)early romance; 官杀 in 时 = late career fruition + children theme; 印 in 月 = strong 学业/家教 backing.

---

## 3. 五行 → 健康/脏腑 + 气质

**Reflective tendencies only — lifestyle & temperament mirrors, NEVER diagnosis.**
Read `element_tally.with_hidden`: an element strongly **excessive OR absent (=0)**
flags where the tendency concentrates; balance is the ideal. Route real concerns to
a clinician.

| 五行 | 脏腑 (藏象) | 官窍/体 | 气质·情志 | 失衡倾向 (reflective) | 季/方/色 |
|---|---|---|---|---|---|
| **木** | 肝·胆 | 目·筋 | 仁·条达·成长·进取 | 郁→易怒/压抑;筋目、作息紧张 | 春·东·青绿 |
| **火** | 心·小肠 | 舌·脉 | 礼·热情·表达·外向 | 亢→焦躁/失眠;心神、循环、上火 | 夏·南·赤红 |
| **土** | 脾·胃 | 口·肌肉 | 信·稳重·包容·务实 | 滞→思虑过度;脾胃、湿重、体重 | 长夏·中·黄 |
| **金** | 肺·大肠 | 鼻·皮毛 | 义·决断·条理·刚毅 | 燥→悲/忧;呼吸道、皮肤、肠道 | 秋·西·白 |
| **水** | 肾·膀胱 | 耳·骨 | 智·灵动·内敛·机敏 | 寒→恐/怯;肾/泌尿、骨、耳、精力 | 冬·北·黑 |

**Reading recipe (engine-facing):**
1. From `with_hidden`, flag the **most excessive** and the **weakest/absent** element.
2. Express each as a *tendency/season* (temperament + 失衡 column), e.g. 火过旺 → "偏热情外放、节奏快，留意情绪与作息" — lifestyle framing, not a claim.
3. When a 大运/流年 element **balances** the chart (fills a gap / drains an excess) → a supportive "养" season for that 脏腑/情志; when it **aggravates** → a "注意调养" season. (This is the same signal as the `favor` tag — §4.)
4. Cross the deficient/excess element with its **十神 role** (e.g. 身弱 & 印弱 → "支持系统单薄" register). Always temperament + lifestyle, never a health claim.

---

## 4. 大运 decade-reading METHOD (十神 × favor → per-dimension recipe)

Per decade the engine hands you: `ganzhi`, `start_age`/`end_age`, `gan_element`,
`zhi_main_element`, **`ten_god`** (大运干 vs 日主), **`favor`** (喜/忌/平), and
secondary **`zhi_ten_god`**/**`zhi_favor`**. This is the master recipe.

### Step A — Establish the decade's 基调 (base tone)
1. **`ten_god`** → pick the dimension register from §1. That is *what the decade is about*.
2. **`favor`** → sets the *valence*: 喜 = 顺/借力/成; 忌 = 阻/耗/需谨慎; **平 = near-balanced chart, 扶抑 gives no hard steer → read the 十神 theme + which element gets amplified instead** (don't manufacture a valence).
3. **`zhi_ten_god`/`zhi_favor` + `zhi_main_element`** → grounds/modifies: 干支同气 (同十神组 → reinforces) or 干支相战 (opposing → internal tension).
4. State the tone as a *season*: "一段以 X 为主题的时期，整体偏 顺/守/中性".

### Step B — favor valence templates (apply to the chosen 十神's dimensions)

| 十神组 | 喜 (favorable) | 忌 (caution) |
|---|---|---|
| **比劫** | 得友助、合作有力、身弱得帮扛财扛事、自主增强 | 破财/分财、竞争耗损、合伙纠纷、(男)感情竞争 |
| **食伤** | 才华绽放、名声/创作/生财顺、(女)子女缘喜、身强得泄而畅 | 才华招损、口舌、(女·伤官)夫星受扰、冲动耗神 |
| **财** | 财路开、(男)感情/正缘至、务实收获、身强任财 | 财来财去/耗财、(身弱)财多身弱、(男)感情纷扰、贪财坏印 |
| **官杀** | 事业进阶、地位/责任提升、(女)姻缘/贵人、身强得官贵 | 压力/是非/健康透支、(身弱)受制、(女)感情波折 |
| **印** | 学业/贵人/庇护、休养生息、身弱得生而稳、名誉 | 依赖/停滞、印多晦财、(偏印)夺食·孤、拖延 |

*(平 valence: use the neutral middle of each cell — "此十神主题被点亮，方向中性，看你怎么用".)*

### Step C — Which dimensions "light up"
- 官杀运 → 事业/地位 (both), 感情 (女命 primary), 健康/压力 (secondary).
- 财运 → 财富 (both), 感情 (男命 primary).
- 印运 → 学业/名誉/庇护, 健康/休养, 母/长辈缘.
- 食伤运 → 才华/事业/财源, 子女 (女命), 表达/名声.
- 比劫运 → 同辈/合作/竞争, 财 (守或破), 自主/独立.

### Step D — Overlay & compose
- **Age band (§5 & §2):** same 十神 reads differently by stage — 官运@20s = 学业/初入职场; @40s = 事业进阶/管理; @55+ = 责任/健康/传承.
- **Interaction with 命局:** if the decade's 十神 is *already strong natally* → *amplifies* (可能过犹不及); if it fills a *natal absence* → *awakens* that dimension.
- **流年 within the decade:** apply the SAME A–C recipe to each `upcoming_annual_pillars[]` (`ten_god`+`favor`) as a shorter **"weather"** window inside the decade's "climate." 流年 `ten_god`==大运 & both 喜 = 应期高点; 冲/克 大运 or 忌 = 波动 window. Never assert a specific event/date — only "更可能是…的季节".

**Composition template (fill the slots):**
> 「{start_age}–{end_age}岁 · {ganzhi}（{ten_god}运，{favor}）：一段以 **{十神 register}** 为底色的时期，整体偏 **{顺/守/中性}**。最容易被点亮的是 **{dimensions}**；{gender note if 财/官/食伤}。可留意 **{喜: 借力方向 / 忌: 调节方向 / 平: 怎么安放}**。以上为倾向性的季节描述，非既定事件。」

---

## 5. Full life-arc framing + 大运 overlay

Four life stages = the **baseline arc**; the running 大运 = the **weather overlaid
on that climate**. Read stage first, then let the decade tilt it.

> Note: these four stages (0–18 / 18–35 / 35–55 / 55+) are a coarse life-arc
> framing and are intentionally *not* identical to §2's tighter 根苗花果 柱位 bands
> (年0–15 / 月16–30 / 日31–45 / 时46+). Two lenses on the same life — the 柱位 bands
> say which *pillar* governs an age; these say the life *theme*. Don't force them to
> line up to the year.

### 学业/成长 · 0–18岁 (Foundation) — 年柱 & 月柱主导
- **Themes:** 家世、父母/家教、性格塑形、学业根基。Stars: **印**, **食伤**, 月令 (天赋方向).
- **大运 overlay:** early decades — 印/食伤运 = 学业/才华 season; 官杀运早现 = 早熟/自律/压力; 财运早现 = 早接触现实/家计, (男)早发情窦。
- **Language:** aptitude/study-style/family-support tendencies — never grades or outcomes.

### 立业/感情 · 18–35岁 (Launch) — 月柱→日柱过渡
- **Themes:** 立足社会、事业起步、婚恋/正缘、独立成家。Stars: **官** (事业/女命夫), **财** (财/男命妻), **食伤生财**, 日支 activation.
- **大运 overlay:** 财官运 = 事业与姻缘的关键"应期季节"; 比劫运 = 创业/合伙/竞争、注意分财; 印运 = 深造/根基稳; 食伤运 = 才华变现/名声起步。
- **Language:** whether *more likely* a 立业/成家 active window — never assert 婚否.

### 事业/家庭 · 35–55岁 (Consolidation) — 日柱主导，兼看时柱
- **Themes:** 事业成熟、家庭责任、财富积累、子女养育。Stars: **官杀**, **财**, **食伤/时柱** (子女).
- **大运 overlay:** 官杀运 = 进阶/管理/也可能压力健康; 财运 = 财富高峰或耗财; 印运 = 名誉/休整/学习; 食伤运 = 才华再爆发/子女(女). 命局强弱决定"任得起 or 扛不动".
- **Language:** 强弱决定同一十神是"助力"还是"负荷".

### 收获/健康 · 55岁+ (Harvest) — 时柱主导
- **Themes:** 收成、退休转向、子女/晚辈、晚景养生。Stars: **时柱十神**, **印** (养·庇护·休), 五行平衡 → 养生 (§3).
- **大运 overlay:** 印/比劫运 = 休养、传承、同辈互助; 财官运晚现 = 老而弥坚/不宜过劳; 忌运 = "以守养为主". 健康全程用 §3 调养语言，绝不诊断。
- **Language:** 传承、健康作息、心境。

### Overlay algorithm (engine-facing)
1. Current age → baseline stage + governing 柱 (§2).
2. Active 大运 (`start_age ≤ age ≤ end_age`) → run §4 A–D for its `ten_god`+`favor`.
3. `upcoming_annual_pillars[]` → §4 short-window weather; flag 大运==流年 `ten_god` + 喜 as "高点季节", 冲克/忌 as "波动季节".
4. Compose: *stage climate* + *decade weather* + *year window*, each dimension in §1's register, gender-noted, health in §3's voice.
5. **Always close** with the framing contract: 倾向与季节，非既定事件；健康仅养生提示，非诊断；重大决策请结合现实与专业意见。

---

### Build notes / school flags
- **子女星:** classical uses **官杀=子女 (男命)** / **食伤=子女 (女命)**; many moderns use **食伤=子女 for both**. Default gendered classical + note.
- **父星:** **偏财=父** (preferred) vs 正财=父; 母 = 印 (agreed).
- **伤官见官 / 官杀混杂 / 枭神夺食 / 贪财坏印:** name as *classical cautions*, always "reflective, redeemable by 配印/生财/制化, not a verdict".
- **命宫/身宫/胎元:** supplementary; weight below the four柱.
- **favor source (critical):** the `favor` tag derives SOLELY from the disclosed 扶抑 heuristic (比劫+印=扶, 食伤+财+官杀=抑; near-balanced → 平). Carry that caveat into every valence statement — real 用神 needs 调候/病药/通关/格局, which this engine does not compute.