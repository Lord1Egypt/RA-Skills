# Analysis playbooks

Best practices for complex analysis. Each playbook gives a mandatory procedure, its `kalo`
command mapping, and what not to do.
Commands are written in shorthand: `kalo` = `python3 <this-skill-dir>/scripts/kalo.py`.

Shared conventions:

- Always resolve categories with `kalo category search <keyword>` (for non-English markets, search the local-language keyword first). Prefer level-3 categories.
- Rank commands: `--page 5` max, `--limit 100` max per page.
- Detail commands take many ids at once (`kalo product detail <id1> <id2> ...`). **Never loop one id at a time** — it multiplies round trips and wall-clock for nothing.
- KaloData covers TikTok data only. No selling-point analysis, no review analysis, no fulfillment rates, no video scripts or captions. When asked for these, state the limitation — never fabricate.

---

## 1. Product diagnosis (product-diagnosis)

**Triggers**: "analyze this product", "why isn't it selling", "how do I grow this" — anything focused on a **single product** that needs same-price-band comparison. For category-level sourcing research use playbook 3.

**Mandatory four steps:**

1. **Pin down category id and price band** (always first)
   - `kalo product detail <product_id>` for unit price; resolve the category via `kalo category search <product keyword>` (pick level=3).
   - Set the band at ±25% of unit price (e.g. $89 → `--price 70-110`).
   - 📌 Without category id + price band you cannot pick valid benchmarks — cross-category or cross-price comparisons poison the conclusion.
2. **Collect industry data**
   - `kalo category detail <category_id>` for the category baseline (GMV, growth rate, channel mix). Always read the product's growth against the category's (e.g. "product -40.9% vs category -6.9% — falling much faster than the market").
   - `kalo product rank --category <category_id> --price <min-max>` for the same-category, same-band leaderboard (top 20-30).
   - `kalo product detail <id1> <id2> ...` in one call for the top 5-10 benchmarks. At least 5 samples.
   - 📌 A leaderboard alone is not collection — you need detail data on the benchmarks.
3. **Assess relative position**: the product vs same-band mean/median vs the top 3-5, expressed as a relative position ("X% above average", "in the top Y%").
4. **Report**: every metric carries its comparison basis.
   - ✅ "Unit price $89 vs $75 same-band average — priced 15% high, but sales growth still beats the mean, so the price can hold."
   - ❌ "$89 is high, cut the price." (no basis)

**Never**: pull rank without `--category` or `--price` to pick benchmarks; call anything "high/low/insufficient" from absolute values alone; start analyzing off the leaderboard only; declare "declining/growing" without the category baseline.

## 2. Creator diagnosis (creator-diagnosis)

**Triggers**: "analyze @creator", "what's this account's growth/selling strategy", "are they a good fit" — anything focused on a **single creator**. To find candidates use playbook 4.

**Precondition**: you need a creator id, an @handle, or a name + region. Ask once if you have none; if the user still doesn't provide one, give generic advice prefixed with "⚠️ No account data retrieved — the following is generic advice". Do not keep asking, and do not refuse to answer.

**Mandatory four steps:**

1. **Pin down category id and follower tier**: `kalo creator detail <id|@handle>` for follower count (handle matching is fuzzy — verify the returned `creator_handle`); resolve the category with `kalo category search <main product keyword>`. Use the matching tier (e.g. 500K followers → `--followers 300000-1000000`).
2. **Collect industry data**: `kalo creator rank --category <category_id> --followers <min-max>` for the same-category, same-tier leaderboard (top 20-30), then `kalo creator detail <id1> <id2> ...` for the top 5-10 benchmarks. At least 5 samples.
3. **Assess relative position**: GPM, video vs livestream revenue mix, views, engagement rate — each against the mean and the top performers.
4. **Report** with comparison basis.
   - ✅ "GPM $4.2 vs $2.8 tier average — monetizing 50% above average, but still 2x behind the top tier ($9+)."

Suggested output format:

| Metric | This creator | Category average | Top benchmark | Relative position |
|--------|--------------|------------------|---------------|-------------------|

**Never**: pull rank without `--category` or `--followers` to pick benchmarks; compare a 100K-follower account against a 1M one; conclude from absolute values alone.

## 3. Category sourcing / market research (product-discovery)

**Triggers**: "top N products/shops", "analyze category X", "sourcing plan / opportunities", "blue ocean / price bands" — **category-level** landscape research. Sourcing for a given brand or shop is still category-level research, not a diagnosis of that shop.

**Standard query chain:**

1. **Resolve the category**: `kalo category search <keyword>`.
2. **Category health check** (required for sourcing/opportunity work — don't jump straight to `product rank` the moment you have an id): `kalo category detail <id1> <id2> ...` for the baseline — GMV, growth rate, active product count, channel mix (livestream/video/mall revenue split), revenue trend. Identify "large enough + growing fast" subcategories at the category layer first, then decide which ones to pull leaderboards for. `kalo category rank --sort revenue_growth_rate --level 2` (or 3) also works to pick high-growth subcategories directly.
3. **Leaderboard**: `kalo product rank --category <id> --sort revenue --limit 100`. Best-sellers by `revenue`, unit volume by `sales_volumn`, risers by `revenue_growth_rate`.
4. **Batch details**: all product ids in a single `kalo product detail <id1> <id2> ...`. Shop fields such as shop name are not in product data — an empty value there is not a bug; detail returns a shop id (foreign key), and shop info comes from the next step.
5. **Shop aggregation and details**: group by shop id, then `kalo shop detail <id1> ... <id30>` in one call for shop names, revenue splits and top products, and join back on shop id.
6. **Price-band sourcing**: call each band **separately** — `kalo product rank --price 50-70`, `--price 70-90`, … (rank sorts across all prices by default, so one query sliced by hand skews toward high tickets). Take at least the top 20-50 per band, then run the detail flow.

**Report requirements**: include a category-layer section (subcategory GMV / growth / channel mix from step 2) calling out which subcategories are large and which are growing, before drilling down to products. Product leaderboards with no category view means the top half of the analysis is missing. Back recommendations with data — never invent numbers.

**Never**: skip the category layer and rank a broad category by revenue (niche high-ticket items get mistaken for "opportunities"); look for shop names in product data; split 50 ids into 5 detail calls; answer a "price band analysis" without specifying bands.

## 4. Creator search / recommendation (creator-search)

**Triggers**: "find creators to work with", "recommend creators for X", "filter creators by follower count/category" — picking **candidates** from the creator pool. To diagnose a known creator use playbook 2.

**Mandatory three steps:**

1. **Resolve the category** (always first): `kalo category search <product keyword>`; for multi-category products, search several keywords and collect all ids. 📌 Never filter creators without a category, and never guess a category id from a product name.
2. **Filter**: `kalo creator rank --category <id> --followers <min-max> --revenue <min-max> --engagement HIGH --type INDEPENDENT`
   - **Default to `--type INDEPENDENT`** (filters out brand-owned accounts) unless the user explicitly wants those.
   - "High-quality video" → `--engagement HIGH`, or `--sort video_revenue` / `--sort content_views`.
   - Sorting: total revenue `revenue` (default), video revenue `video_revenue` (video partnerships), views `content_views` (content quality), growth `revenue_growth_rate` (upside).
   - Use `--page` when you need a deep candidate pool.
3. **Evaluate and compile**: pull follower count, GMV, video revenue, views and engagement rate; apply the user's secondary filters; deliver a shortlist with those metrics.

**Report requirements**: show the category search and the ids you settled on, state the filters used, and include key metrics in the shortlist. When asked for fields that don't exist (e.g. fulfillment rate), say plainly that KaloData doesn't provide them — never claim you can get them.

## 5. Viral video methodology (video-script)

**Triggers**: "video script", "how do I make one that takes off", "what do viral videos have in common", "shooting advice" — anything that needs viral data before advice. For a plain leaderboard lookup just use `kalo video rank`.

**Mandatory three steps:**

1. **Collect viral videos**: `kalo video rank --category <id> --region <market> --range last30Day` for the top 10-20, then `kalo video detail <id1> <id2> ...` for full metrics on at least 5 samples (views, likes, comments, shares, revenue, ad ROAS, trend). ⚠️ KaloData does not provide video scripts or captions — structural analysis is based on titles, duration, engagement and commercial metrics; for shot-by-shot breakdowns, ask the user for video links to watch themselves. 📌 No viral data = no shooting advice.
2. **Extract patterns and generate scripts**: analyze shared traits (opening hook, visual payoff, demo style, emotional beat, call to action), then produce 3 high-conversion script templates (table: timeline, shot, visual, copy/voiceover) — problem-solution, comparison test, and unboxing + use case. Attach 1-3 reference videos (from step 1) to each template.
3. **Full strategy**: production technique (shots/lighting/background/music), copy strategy (title formulas, 5-8 hashtags), publishing strategy (timing/cadence/A-B tests), and tracking benchmarks (completion rate >50%, like rate >5%, CTR >3%, conversion >2%).

**Never**: give shooting advice without viral data analysis; ignore the target market and category. Keep output under 3000 words.

## 6. Shot-by-shot script writing (script-creation)

**Triggers**: "write me a shooting script", "storyboard", "a script we can shoot as-is" — a scene-by-scene script for the operations and production team. **This playbook calls no API — it is pure writing**; pair it with playbook 5 when viral analysis is needed first.

**Settle before writing** (use the default or ask once if missing): duration (default 15-30s), target market (drives talent casting and dialogue language), product selling points and available asset images, reference viral videos, any extra user instructions. Priority: user instructions > reference videos > selling points.

**Writing requirements:**

- Field labels and descriptions in the language you're using with the user; **dialogue in the target market's local language**, written as native UGC speech, not translationese.
- Cast talent that fits the local market (ethnicity, age range, vibe, wardrobe).
- Describe the product only from angles the provided assets cover (front-only image → don't shoot the back or interior). Standard brand elements (hang tags, logos) can appear but must be anchored to the brand name.
- Borrow the hook rhythm and conversion beats of the reference videos; never copy dialogue or shots verbatim (platform duplicate detection).
- Budget dialogue for "duration - 2 seconds" to leave buffer; the timeline must total exactly the target duration with seamless scene transitions.
- Reference asset images as `@Image N`.

**Output format** (plain text — no JSON, no code fences):

```
Style & Color: one line on the overall aesthetic
Scene: one line on the environment
Subject: 1-3 sentences on talent + product (cite assets as @Image N)
Camera & Framing: one line on camera rhythm

Action Timeline:

[Scene 1: name]
Time: Xs-Ys | Shot: shot size | Location: place
VISUAL: what's on screen
AUDIO (speaker): "dialogue (local language)"
TALENT ACTION: what the talent does
...
```

Omit the AUDIO line for silent scenes. No captions or text overlays by default (add them only when the user asks). Keep total output under 750 characters.
