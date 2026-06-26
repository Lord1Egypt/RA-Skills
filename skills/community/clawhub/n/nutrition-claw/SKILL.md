# nutrition-claw

A fully local, offline-first nutrition tracking CLI built for [openclaw](https://openclaw.ai). Track daily meals and ingredients, manage a personal food library, set nutrition goals, and search your history — all without sending data anywhere.

## Setup

The skill folder ships with pre-built JS in `dist/` but **not** `node_modules` — native dependencies (ONNX runtime for local embeddings) must be installed locally.

**1. Install dependencies**

```bash
cd <skill-folder>
npm install
```

**2. Build**

The `dist/` folder ships pre-built, but run this to recompile from source if needed (requires [Bun](https://bun.sh)):

```bash
npm run build
```

**3. Make the CLI available**

```bash
npm link
```

This creates a global `nutrition-claw` symlink so you can call it from anywhere.

**3. First-time goal setup**

```bash
nutrition-claw configure
```

Run the interactive wizard (no flags) or pass flags directly — see the `configure` command below.

> To unlink later: `npm unlink -g @pita/nutrition-claw`

## Overview

- All data (meals, foods, goals) is stored in `~/.nutrition-claw/` as plain JSON files — fully local, never uploaded
- Semantic search uses a local MiniLM embedding model (no API key; model downloads once on first search, then cached)
- Output is YAML — compact, human-readable, easy to parse
- Dates (`YYYY-MM-DD`) and times (`HH:MM`) must always be passed explicitly — the CLI never infers them
- Errors are written to stderr; structured data to stdout

---

## Command Reference

### `configure` — set nutrition goals

Two modes: interactive (no flags) guides through a wizard; non-interactive (flags provided) outputs YAML directly, no prompts.

```bash
# Auto mode — compute goals from body profile (Mifflin-St Jeor BMR + TDEE)
nutrition-claw configure \
  --sex male|female|other \
  --age <n> \
  --weight-kg <n> \
  --height-cm <n> \
  --activity sedentary|light|moderate|very|extra \
  --goal lose|recomp|maintain|lean-bulk|bulk \
  --rate 0.25|0.5|0.75        # kg/week loss (only for --goal lose)
  --surplus 200|350|500        # kcal surplus (only for --goal bulk)

# Manual mode — set each nutrient directly
nutrition-claw configure --calories-kcal 2000 --protein-g 150 --carbs-g 250 \
  --fiber-g 25 --sugar-g 50 --fat-g 65 --sat-fat-g 20
```

---

### `goals` — daily nutrition targets

Directions are fixed: `calories_kcal`, `carbs_g`, `sugar_g`, `fat_g`, `sat_fat_g` are **max** (upper limits); `protein_g`, `fiber_g` are **min** (targets to reach).

```bash
nutrition-claw goals get
nutrition-claw goals set --calories-kcal 2200 --protein-g 160
nutrition-claw goals delete --nutrient protein_g   # remove one
nutrition-claw goals delete                        # remove all
```

---

### `food` — reusable food library

Store nutrition data per reference amount (e.g. per 100g, per 100ml, per 1 tbsp). Values are scaled automatically when added to a meal. Intended workflow: user shares a photo of a nutrition label → extract values → `food add`. Next time they eat it, use `food search` to find it and `meal ingredient add --food` to auto-scale.

```bash
nutrition-claw food add --name "chicken breast" --per-amount 100 --per-unit g \
  --calories-kcal 165 --protein-g 31 --fat-g 3.6

nutrition-claw food add --name "whole milk" --per-amount 100 --per-unit ml \
  --calories-kcal 61 --protein-g 3.2 --fat-g 3.3

nutrition-claw food add --name "olive oil" --per-amount 1 --per-unit tbsp \
  --calories-kcal 119 --fat-g 13.5

nutrition-claw food list
nutrition-claw food get "chicken breast"      # exact name
nutrition-claw food search "chicken"          # semantic — no exact name needed
nutrition-claw food update "chicken breast" --protein-g 32
nutrition-claw food delete "chicken breast"
```

Supported units — WEIGHT: `g` `kg` `oz` `lb` · VOLUME: `ml` `L` `fl_oz` `cup` `tbsp` `tsp`

---

### `meal` — log daily meals and ingredients

`--date` and `--time` are always required for `meal add`. Meal nutrition totals are computed from their ingredients — never stored separately.

```bash
# Create a meal — returns the meal id
nutrition-claw meal add --name "Lunch" --date 2026-03-15 --time 13:00
# id: D-lfLPOP

# List meals for a day (includes per-ingredient breakdown and meal totals)
nutrition-claw meal list --date 2026-03-15

# Rename or delete a meal
nutrition-claw meal update D-lfLPOP --name "Dinner"
nutrition-claw meal delete D-lfLPOP
```

#### Ingredients

```bash
# Manual — specify nutrients directly
nutrition-claw meal ingredient add D-lfLPOP \
  --name "Chicken breast" --calories-kcal 165 --protein-g 31 --fat-g 3.6

# From food library — auto-scales by amount and unit
nutrition-claw meal ingredient add D-lfLPOP --food "chicken" --amount 200 --unit g
# matched: chicken breast  (nearest semantic match, scaled to 200g)

# Update ingredient by index
nutrition-claw meal ingredient update D-lfLPOP 0 --calories-kcal 170

# Delete ingredient by index
nutrition-claw meal ingredient delete D-lfLPOP 0
```

#### Ingredient impact feedback

Every `meal ingredient add` and `meal ingredient update` returns an `impact` block showing, per nutrient: how much this ingredient contributed (`added`), the running daily `total`, `goal`, `remaining` headroom or deficit, `pct` of goal consumed (100.0 = goal exactly met), and `status` (`ok` / `under` / `over`).

**Always interpret this and give the user explicit, opinionated feedback.** Examples:
- "Great — chicken pushes protein to 15% of goal with only 6.6% of calories used."
- "Heads up: this brings saturated fat to 94% of your daily limit."
- "You're now over your calorie goal for the day (112%)."
- "Protein is still well under target (15%) — consider a protein-rich addition."

Point out both wins and overages. Be specific with numbers. Synthesise into 1–2 sentences of nutritional coaching — don't just echo the YAML.

---

#### Ingredient nutrition commentary (food education + diary)

Every time an ingredient is added, **teach the user something real about that food**. The goal is genuine nutrition literacy — not just "this helps your goal", but *why* a food is considered healthy or unhealthy, what it does in the body, and what the science or conventional wisdom says about it. Assume the user is curious and wants to understand food, not just track numbers.

Go beyond the impact block. Explain the food itself:
- What makes it nutritionally valuable or problematic
- How it behaves in the body (e.g. fast vs slow digesting carbs, saturated vs unsaturated fat, complete vs incomplete protein)
- Any common misconceptions worth clearing up
- Why it fits or conflicts with their specific goal, with a brief explanation of the underlying reason

Examples of the right tone and depth:

- "Chicken breast is one of the most protein-efficient foods you can eat — roughly 31g of protein per 100g with almost no fat. For recomposition, that ratio is hard to beat: you're building and preserving muscle without spending many calories doing it."
- "Whole milk has more going for it than its reputation suggests — the fat is mostly saturated, which raises LDL, but it also raises HDL and the calcium, protein and fat-soluble vitamins (A, D, K2) are genuinely useful. The concern is more about quantity than the food itself."
- "Olive oil is rich in oleic acid, a monounsaturated fat linked to reduced inflammation and better cardiovascular markers. It's calorie-dense (about 120 kcal per tablespoon) so it's easy to accidentally blow your fat budget — but the fat itself is high quality."
- "White rice is almost pure starch — it digests quickly, spikes blood sugar, then drops off. That's actually useful around a workout when you want fast fuel, but it adds almost nothing else: negligible fiber, protein, or micronutrients. Brown rice is strictly more nutritious, though the difference in practice is modest."
- "Eggs have been unfairly demonised for decades over dietary cholesterol. For most people, dietary cholesterol has little effect on blood cholesterol — the liver adjusts. What eggs do offer is a near-complete amino acid profile, choline (important for brain function), and fat-soluble vitamins. They're excellent value nutritionally."

Keep remarks to 2–4 sentences. Be confident and specific — the user is curious, not looking for hedged generalities. Tie it back to their goal at the end if it adds something.

**To avoid repeating yourself, maintain a feedback diary** at `~/.nutrition-claw/feedback-diary.txt`.

**Diary format** — one entry per line:

```
<YYYY-MM-DD>|<normalised food name>|<topic key>
```

Example lines:

```
2026-03-15|chicken breast|protein-source
2026-03-15|olive oil|calorie-density
2026-03-16|whole milk|sat-fat-warning
```

**Topic keys** — use one of these per remark. Each maps to a distinct educational angle so the user learns something different each time they eat the same food. Rotate through them — the diary ensures you never repeat the same angle within 7 days.

| Key | What to explain |
|---|---|
| `protein-source` | Protein quantity, amino acid profile, and completeness — does it contain all essential amino acids? Is it fast or slow digesting (whey vs casein vs plant)? How much muscle-building signal does it deliver per calorie? |
| `calorie-density` | Energy per gram and what that means in practice — how easy is it to overeat? How does it affect satiety relative to its calorie cost? Compare to similar foods to give a sense of scale. |
| `sat-fat-warning` | Saturated fat content, which specific fatty acids are present (lauric, palmitic, stearic all behave differently), how they affect LDL and HDL, and where the nuance lies — not all saturated fat is equal. |
| `fiber-benefit` | Soluble vs insoluble fiber, how each type works in the gut, effects on blood sugar regulation, cholesterol, satiety, and the microbiome. Is this food a meaningful fiber source or negligible? |
| `sugar-concern` | Total sugars vs added sugars, glycaemic index vs glycaemic load, how quickly this food raises blood glucose and what the insulin response looks like, and whether the sugar is accompanied by fiber or protein that blunts the spike. |
| `fat-profile` | The full fat breakdown — saturated, monounsaturated, polyunsaturated (omega-3 vs omega-6 ratio). Which predominates, what effect that has on inflammation and cardiovascular health, and whether the fat in this food is something to lean into or be mindful of. |
| `glycaemic-response` | How this food behaves in the bloodstream — speed of digestion, blood sugar curve, insulin demand, and whether that matters for the user's goal (e.g. more relevant for fat loss or diabetes risk than for a bulking athlete). |
| `goal-alignment` | A mechanistic explanation of why this food is well or poorly matched to their specific goal — not just "good for weight loss" but *why*: satiety per calorie, thermic effect, muscle-sparing protein, etc. |
| `micronutrient` | A standout vitamin or mineral in this food — what it does in the body, why deficiency matters, how common that deficiency is, and whether this food is a meaningful source. Go specific: B12, magnesium, zinc, iron bioavailability, folate, etc. |
| `misconception` | A common myth or misunderstanding about this food, corrected with evidence. Eggs and cholesterol, fat making you fat, carbs being inherently bad, soy and hormones, MSG safety — whatever applies. Be direct and cite the actual science. |
| `processing` | How this food is produced or processed, and whether that matters nutritionally. Ultra-processed vs minimally processed, what's lost or added in processing (fiber stripped, nutrients added back, emulsifiers, preservatives), and how to read between the lines on labels. |
| `thermic-effect` | The thermic effect of food (TEF) — how much energy the body spends digesting this macronutrient. Protein costs ~20–30% of its calories to digest; fat costs ~0–3%; carbs 5–10%. High-TEF foods give a small but real metabolic advantage. |
| `satiety-index` | How filling this food is relative to its calories. Protein and fiber drive satiety; liquid calories and refined carbs don't. Some foods (potatoes, oats, eggs) are exceptionally satiating; others (nuts, croissants, chips) are very easy to overeat despite being calorie-dense. |
| `digestibility` | How well the body actually absorbs the nutrients in this food. Bioavailability varies enormously — plant iron (non-haem) absorbs at ~5–15% vs animal iron (haem) at ~25–35%; plant protein digestibility is lower than animal protein; phytates in legumes and grains can block mineral absorption. |
| `antinutrients` | Compounds that interfere with nutrient absorption — phytates, lectins, oxalates, tannins. How significant they are in this food, whether cooking, soaking, or fermenting reduces them, and whether they're actually a concern at realistic portion sizes (usually not, but worth knowing). |
| `omega-profile` | Omega-3 vs omega-6 content and the ratio between them. The modern diet is typically far too high in omega-6 (pro-inflammatory) and too low in omega-3 (anti-inflammatory). Does this food help or worsen that ratio? EPA/DHA vs ALA — which form is present and how well does it convert? |
| `gut-health` | How this food interacts with the gut microbiome. Does it feed beneficial bacteria (prebiotic fiber, resistant starch)? Is it fermented (probiotics)? Does it contain emulsifiers or additives that may disrupt the gut lining? A diverse microbiome is one of the strongest predictors of long-term health. |
| `blood-pressure` | Sodium content and its effect on blood pressure, potassium-to-sodium ratio (potassium blunts sodium's effect), nitrates in vegetables that relax blood vessels, and whether this food is something hypertension-conscious eaters should be mindful of. |
| `bone-health` | Calcium, phosphorus, vitamin D, vitamin K2, and magnesium — the full constellation of bone-relevant nutrients. Does this food contribute meaningfully? Are there compounds that interfere (oxalates blocking calcium absorption, excess phosphorus from processed foods)? |
| `hormonal-impact` | Foods that meaningfully affect hormones — phytoestrogens in soy (evidence is far more benign than the fear suggests), iodine and thyroid function, zinc and testosterone, blood sugar and insulin, cortisol and caffeine. Explain the actual mechanism and whether the effect size is clinically meaningful. |
| `antioxidants` | Polyphenols, flavonoids, carotenoids, vitamin C, vitamin E, selenium — what antioxidants this food contains, what they neutralise (free radicals, oxidative stress), and what that means for ageing, inflammation, and chronic disease risk. Avoid vague claims; be specific about the compounds. |
| `cooking-impact` | How cooking this food changes its nutritional profile — what's lost (some B vitamins and vitamin C are heat-sensitive), what's gained (lycopene in tomatoes increases with heat; cooking destroys antinutrients; protein digestibility improves). Raw vs cooked matters more than people think for some foods. |
| `food-pairing` | Nutrients in this food that are better absorbed when paired with something else — fat-soluble vitamins (A, D, E, K) need dietary fat; non-haem iron absorbs better with vitamin C; turmeric bioavailability jumps with black pepper (piperine). Small pairings can meaningfully change what the body actually gets. |
| `hydration` | Water content of the food and its contribution to daily hydration, electrolyte content (sodium, potassium, magnesium), and whether this food is hydrating, neutral, or mildly dehydrating (high sodium, high protein increasing urine output). Often overlooked but relevant to performance and energy. |
| `sport-performance` | How this food serves athletic performance specifically — pre/intra/post workout suitability, glycogen replenishment, muscle protein synthesis, creatine (in meat), beta-alanine, nitrates (in beetroot), caffeine, and recovery support. |
| `fermentation` | Whether this food is fermented, what that does to its nutrient profile (B vitamins increase, antinutrients decrease, probiotics added), and the health implications. Yoghurt, kefir, kimchi, sauerkraut, miso, tempeh — fermentation transforms a food meaningfully. |
| `environmental` | The environmental footprint of this food — carbon emissions, water use, land use. Not to moralize, but because many people are curious about how their food choices interact with sustainability. Animal products vary enormously (beef vs chicken vs eggs); some plant foods have surprising footprints (almonds, avocados). |
| `insulin-index` | Distinct from glycaemic index — the actual insulin response triggered, which isn't always predicted by carb content. Protein also triggers insulin. Some high-protein, low-carb foods (like beef) have a surprisingly high insulin index. Relevant for people managing insulin sensitivity. |
| `metabolic-flexibility` | Whether this food helps or hinders the body's ability to switch between burning carbs and fat for fuel. High-sugar, high-carb foods keep the body reliant on glucose; whole foods with fiber, protein, and fat support a more flexible metabolism. Particularly relevant for fat loss and energy stability goals. |
| `liver-health` | How this food interacts with liver function — fructose load (fructose is metabolised almost entirely in the liver), choline content (deficiency contributes to fatty liver), alcohol, cruciferous vegetables that upregulate detox pathways, and antioxidants that reduce oxidative stress on liver cells. |
| `skin-hair-nails` | Nutrients with visible effects — biotin, zinc, vitamin C (collagen synthesis), omega-3 (skin barrier), vitamin A (cell turnover), silica. People often don't connect diet to skin and hair quality; this is a chance to make that link concrete. |
| `sleep-recovery` | Foods that support or disrupt sleep and recovery — magnesium (muscle relaxation, sleep quality), tryptophan (serotonin and melatonin precursor), caffeine half-life, high-protein meals supporting overnight muscle protein synthesis, and the evidence on carbs before bed (not inherently bad). |
| `immune-function` | Nutrients that support or stress the immune system — vitamin C, vitamin D, zinc, selenium, beta-glucans (in oats and mushrooms), and the gut-immune axis. Does eating this food regularly support immune resilience? |
| `mental-health` | The gut-brain axis, omega-3 and depression, B vitamins and neurotransmitter synthesis, iron and cognitive function, blood sugar stability and mood. Food's effect on mental health is underappreciated and the evidence is growing fast. |
| `longevity` | Foods strongly associated with longevity research — polyphenol-rich foods, legumes (the most consistent predictor across Blue Zone populations), nuts, olive oil, whole grains, oily fish. What does the epidemiology actually say, and why? |
| `caffeine` | Caffeine content and its effects — adenosine blocking (why it wakes you up), half-life (~5–6 hours, so afternoon coffee genuinely disrupts sleep), tolerance and dependency, performance benefits (endurance, strength, focus), and the difference between coffee, tea, energy drinks, and matcha in terms of how the caffeine hits. |
| `alcohol` | Alcohol's caloric density (7 kcal/g, almost as dense as fat), how it's metabolised ahead of everything else which effectively pauses fat burning, its effect on sleep quality (disrupts REM despite feeling sedating), testosterone suppression, and the real evidence on "moderate drinking is healthy" (largely debunked by newer research). |
| `liquid-calories` | Why liquid calories are nutritionally different from solid ones — they bypass normal satiety signals, digest faster, don't require chewing (which itself is part of the fullness signal), and are easy to consume in large quantities without noticing. Relevant for juices, smoothies, milk, and any caloric drink. |
| `hydration-quality` | Not all fluids hydrate equally. Water is the baseline. Electrolyte content (sodium, potassium, magnesium) matters for cellular hydration. Caffeine is mildly diuretic but not enough to cancel the fluid it comes in. Alcohol is genuinely dehydrating. Sports drinks: useful for long exercise, unnecessary for casual activity. |
| `juice-vs-whole` | Why whole fruit is almost always better than juice — juicing strips the fiber, concentrates the sugars, and removes the chewing signal that contributes to satiety. A glass of orange juice can contain the sugar of 3–4 oranges with none of the fiber that blunts the blood sugar spike. |
| `artificial-sweeteners` | What the evidence actually says — they don't spike blood glucose, but the data on gut microbiome effects, cephalic insulin response, and whether they reinforce sugar cravings is more mixed than either the "totally safe" or "secretly harmful" camps admit. Useful for reducing sugar; not a free pass. |
| `tea-polyphenols` | Tea (green, black, white, oolong) is one of the richest dietary sources of polyphenols — specifically catechins (green tea) and theaflavins (black tea). These have well-documented anti-inflammatory and cardiovascular effects. Brewing time and temperature affect extraction. Milk may bind some polyphenols and reduce bioavailability. |
| `coffee-beyond-caffeine` | Coffee is far more than caffeine — it's one of the largest sources of antioxidants in the Western diet, contains chlorogenic acids that improve insulin sensitivity, and is consistently associated with reduced risk of type 2 diabetes, Parkinson's, and liver disease in epidemiological studies. The health case for moderate coffee is stronger than most people realise. |
| `sports-drinks` | When sports drinks are actually useful vs when they're just expensive sugar water — they matter for sustained exercise over ~60–90 minutes where glycogen depletion and electrolyte loss are real, but for most everyday activity they add unnecessary sugar and calories. Isotonic vs hypertonic vs hypotonic and what the difference means in practice. |
| `smoothie-nutrition` | Smoothies can be nutritional powerhouses or sugar bombs depending on what goes in them. Blending preserves fiber (unlike juicing) but breaks cell walls, making sugars more rapidly available. Adding protein, fat, or whole oats slows digestion. Portion size is the main trap — a 600ml smoothie can easily contain 600+ kcal without feeling like a full meal. |
| `milk-alternatives` | The nutritional comparison between dairy milk and plant alternatives — oat milk is lowest in protein and high in carbs; almond milk is very low calorie but also nearly devoid of protein; soy milk is the closest to dairy nutritionally (similar protein, often fortified); coconut milk is high in saturated fat. Fortification matters: check for added calcium and B12. |
| `collagen-drinks` | What bone broth and collagen drinks actually deliver — collagen protein is incomplete (low in tryptophan) so it's not a substitute for a full protein source, but glycine content is real and may support joint and gut lining health. The "collagen going directly to joints" claim is not how digestion works — it's broken into amino acids first. Useful, but the marketing overstates it. |
| `energy-drinks` | Energy drinks beyond caffeine — B vitamins (usually at doses far exceeding need, mostly excreted), taurine (evidence for harm is weak but evidence for benefit also limited), sugar content in non-sugar-free versions, and the risks of combining high caffeine doses with alcohol or exercise in heat. The caffeine dose in some is equivalent to 3–4 espressos. |
| `fermented-drinks` | Kefir, kombucha, kvass, tepache — fermented drinks contain live cultures, organic acids, B vitamins, and in some cases meaningful probiotic strains. Kombucha evidence is more anecdotal than kefir's; the sugar content varies widely by brand and fermentation time. Real fermented drinks are meaningfully different from probiotic-labelled products that may not survive to the gut. |

**Workflow on every `meal ingredient add` or `meal ingredient update`:**

1. Read `~/.nutrition-claw/feedback-diary.txt` (skip if absent).
2. **Purge expired entries**: remove any line whose timestamp is more than 7 days before today's date. Write the cleaned file back before proceeding.
3. Normalise the ingredient name to lowercase, trimmed (e.g. `"Chicken Breast"` → `"chicken breast"`).
4. Collect the topic keys already recorded for this normalised food name within the last 7 days.
5. Choose a topic key that is **not** already in that set. If all keys have been used recently, pick the one used least recently (oldest timestamp).
6. Write a 2–4 sentence educational remark for that topic. Explain the *why* — how the food behaves, what the science says, what a curious person would genuinely want to know. Connect it to their goal at the end if it adds something concrete.
7. Append a new line to the diary (create the file if needed):
   ```
   <YYYY-MM-DD>|<normalised food name>|<chosen topic key>
   ```

**Combine this remark with the impact feedback** into one cohesive response — don't deliver them as two separate blocks. Lead with the numbers if they're notable, then flow into the educational point naturally, or vice versa. The remark should feel like something a knowledgeable friend would say, not a disclaimer or a footnote.

---

### `summary` — daily totals vs goals

```bash
nutrition-claw summary --date 2026-03-15
# per-nutrient: consumed / goal / pct / status (ok | under | over)
```

---

### `history` — multi-day overview

```bash
nutrition-claw history --from 2026-03-01 --to 2026-03-15
nutrition-claw history --from 2026-03-15 --days 7
```

---

### `search` — semantic search (no exact name needed)

Three domain-specific searches — results scoped to the right data type:

```bash
nutrition-claw meal search "pasta"
nutrition-claw meal search "pasta" --from 2026-03-01 --to 2026-03-15

nutrition-claw meal ingredient search "chicken"
nutrition-claw meal ingredient search "chicken" --from 2026-03-10

nutrition-claw food search "beef"
```

---

## Nutrients

| Flag | Unit | Direction |
|---|---|---|
| `--calories-kcal` | kcal | max |
| `--protein-g` | g | min |
| `--carbs-g` | g | max |
| `--fiber-g` | g | min |
| `--sugar-g` | g | max |
| `--fat-g` | g | max |
| `--sat-fat-g` | g | max |

## Data location

```
~/.nutrition-claw/
  goals.json       # daily nutrition goals
  foods.json       # food library
  logs/            # YYYY-MM-DD.json per day
  vectors/         # local MiniLM vector index
```
