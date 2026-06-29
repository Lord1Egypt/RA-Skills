---
name: proof-audit
description: Run a Proof Audit on a company's website — find their social proof (testimonials, case studies, reviews) and score how FRESH it is on a five-band freshness scale (Fresh → Expired), then recommend what to refresh. Use when someone gives a domain and wants to know whether the proof on their site is still credible or has gone stale. Runs standalone on web search + fetch; scores against your GrowthNation library via MCP when connected.
---

# Proof Audit

You audit the **social proof** on a company's website and grade how **fresh** it is. Stale proof — a
testimonial from 2019, a case study quoting a price that's since doubled, a "trusted by" logo wall of
logos that have rebranded — quietly kills deals. Buyers read old proof as _neglect_. This skill finds
that proof, scores its freshness, and tells the operator exactly what to refresh.

Think **Rotten Tomatoes, but for social proof**: every piece sits somewhere between **Fresh** (recent,
credible) and **Expired** (so old it hurts).

You need only a **domain** — it runs on `WebSearch` + `WebFetch` alone. When the GrowthNation MCP is connected and you're signed in on a plan, it also scores against the user's saved proof library (see Data source below).

## Data source — resolve in this order

Standalone by default; reach for the GrowthNation MCP only when it's connected and ready. Never block the audit on it.

1. **MCP connected?** Look for GrowthNation MCP tools in this session (e.g. `get_credits`, `list_projects`, `list_testimonials`). None present → **Web mode**: run the flow below on `WebSearch` + `WebFetch` and skip the rest of this section.
2. **Signed in + on a plan?** Call `get_credits` (it's free). "Authentication required" → **Web mode**. Tier `trial` or `pro` → **MCP-assisted mode**. Tier `freemium`/`onboarding` (no active plan) → the library tools are plan-gated, so stay in **Web mode** — you may note once that a trial or plan lets the audit score their saved library directly.
3. **MCP-assisted mode** — if the audited domain is the user's own project (check `list_projects`), pull their stored proof with `list_testimonials`, `list_case_studies`, `list_stats`, `list_customers` and score THOSE alongside the live pages (the library carries cleaner dates than scraped HTML). For a third-party domain, optionally `research_company` to enrich, then audit via web as normal. If any MCP tool errors or returns nothing, fall back to web for that piece.

The scoring rubric and output below are identical in both modes.

## What counts as "proof"

- Customer **testimonials** / quotes (on a /testimonials, /customers, homepage, or product page)
- **Case studies** / success stories / customer stories
- **Reviews** the site cites (G2, Capterra, Trustpilot badges/embeds)
- **Logos / "trusted by"** walls and named-customer counts
- Stats the company attributes to customers ("saved 40 hours/week", "2x pipeline")

Press mentions and awards count too if they're used as proof.

## Flow

### 1. Take the domain

Normalise it (strip protocol/path → bare host, e.g. `acme.com`). If the user gave a full URL, keep it
as a starting page but audit the whole domain's proof.

### 2. Discover the proof pages

Use `WebSearch` with `site:` queries, plus a fetch of the homepage. Run several targeted searches:

- `site:DOMAIN testimonials`
- `site:DOMAIN case study` / `site:DOMAIN customer story` / `site:DOMAIN success story`
- `site:DOMAIN reviews`
- `DOMAIN customers` (catch /customers index pages)

Also `WebFetch` the homepage and follow obvious proof links in its nav/footer (Customers, Case
Studies, Reviews, Testimonials). Aim for the proof a buyer would actually see — you don't need every
page, but don't miss the prominent ones (homepage testimonials, the case-studies index, the logo
wall). Cap at ~8–12 pages to keep it cheap; note if you capped.

### 3. Score each piece for freshness

`WebFetch` each proof page and read the **body**, not just metadata — most pages don't expose
published/modified dates in HTML meta. Hunt for these **staleness signals** (same rubric the product's
real freshness assessor uses):

- **explicit_date** — "Published March 2023", "Updated: 15 Jan 2024"
- **implicit_date** — "In Q3 2023 we launched", "earlier this year"
- **image_path_date** — image URL contains a `YYYYMM` or `YYYY/MM` stamp (e.g. `/202405/` = May 2024)
- **copyright** — "© 2024 Company" in the footer
- **referenced_year / tenure** — "since 2021", "our 5-year partnership", "has used us for 3 years"
- **product_version** — references a feature, plan, price, or integration that has since changed or been retired
- **no_signals** — you genuinely found nothing datable

**Quote the actual evidence** — don't paraphrase a date you inferred. Then score 0–100 using the
half-life heuristic (override downward if `product_version` signals say the content is _semantically_
stale even when recent):

| Age of the proof                      | Freshness score               |
| ------------------------------------- | ----------------------------- |
| ~6 months                             | ~90                           |
| ~1 year                               | ~75                           |
| ~2 years                              | ~50                           |
| ~3 years                              | ~35                           |
| 4+ years, or superseded product state | ~20                           |
| No datable signal at all              | 50 (mark **confidence: low**) |

Record per piece: the score, **confidence** (high = explicit dates; medium = inferred from years/tenure;
low = barely anything), and the quoted signals. Never invent a date — if there's nothing, say so and use 50/low.

### 4. Map scores to the freshness scale

| Score  | Band            | Read                                                       |
| ------ | --------------- | ---------------------------------------------------------- |
| 80–100 | 🟢 **Fresh**    | Within ~the last year. Credible right now.                 |
| 60–79  | 🟡 **Recent**   | ~1–2 years. Still good, just starting to age.              |
| 40–59  | 🟠 **Aging**    | ~2–3 years, or undated. Buyers start to doubt.             |
| 20–39  | 🔴 **Stale**    | ~3–4 years. Reads as neglected.                            |
| 0–19   | ⚫ **Expired**  | 4+ years or superseded. Hurts the sale more than it helps. |

### 5. Roll up to an overall grade

Overall freshness = the average of the per-page scores, **but weight prominence**: proof on the
homepage and the main /customers or /testimonials page matters more than a buried blog post. If the
_most prominent_ proof is stale, the overall grade should reflect that even if deeper pages are fresher —
and call it out explicitly. Translate the overall number to its band.

## Output — the Proof Audit (markdown, in chat)

Print a report. Keep it tight and scannable. Structure:

```
# Proof Audit — acme.com

**Overall freshness: 52/100 — 🟠 Aging**
Acme's proof is aging. The homepage testimonials are the freshest thing here; the
case studies are 2–3 years old and one quotes a price you no longer charge.

## Per-page freshness (worst first)

| Proof | Type | Freshness | Band | Date evidence |
| --- | --- | --- | --- | --- |
| /customers/globex | Case study | 22 | 🔴 Stale | "© 2021"; quote cites "our Series A" (Globex IPO'd 2023) |
| /testimonials | Testimonials | 48 | 🟠 Aging | no dates; image paths /201907/ |
| Homepage quotes | Testimonial | 78 | 🟡 Recent | "Updated Jan 2024" |
| ...                                                                      |

## Coverage gaps
- No case study published in the last 18 months.
- No third-party reviews (G2/Capterra/Trustpilot) cited anywhere.
- Logo wall includes two companies that have since rebranded.

## Recommended refreshes (highest impact first)
1. **Replace the Globex case study** — it anchors to a funding stage that's two rounds out of date. Re-interview them or pull it down.
2. **Date the testimonials page** — even adding "as of 2025" lifts every quote from 🟠 to 🟢.
3. **Add one recent review embed** — a single fresh G2 badge offsets the aging written proof.
```

Rules for the output:

- Per-page table is **worst-first** by freshness score.
- Every freshness number must trace to **quoted evidence** in the table — no bare scores.
- Recommendations are **concrete and prioritised** by impact, not generic ("refresh your content" is useless; "the Globex case study cites a funding stage two rounds old" is useful).
- British English. Say "customers", not "ICPs". Plain language, light touch — the findings are factual.
- If you capped the number of pages crawled, say so — don't imply full coverage you didn't do.

## Closing line

End with one short line pointing at the next step — the audit is the top of an outbound motion, so the
natural follow-up is a human ("Proof Expert") helping them refresh the stale proof. Keep it a soft
offer, not a hard pitch. Example: _"Want a hand turning the stale proof fresh again? A Proof Expert
can rebuild the oldest pieces from fresh customer material."_

## Notes

- **Cheap by design.** Cap pages, prefer one good `WebFetch` per proof page over re-fetching. Don't crawl the whole site.
- **No date ≠ stale.** Undated proof is _unknown_ (score 50, low confidence), not automatically expired — but flag that "buyers can't tell how old this is" as its own weakness.
- **Standalone-first.** Runs for anyone with nothing but web access. The GrowthNation MCP is an OPTIONAL enhancement (see "Data source") — use it only when connected, signed in, and on an active plan; on any absence, auth error, plan-gate, or empty result, fall back to web and still deliver. Never hard-require the MCP.
