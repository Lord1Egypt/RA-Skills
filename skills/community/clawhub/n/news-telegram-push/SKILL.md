---
name: news-telegram-push
version: 2.0.4
description: Curate and send twice-daily English Telegram news pushes covering Industry News, Financial News, and Global Political News with strict deduplication and trusted-source filtering.

News Telegram Push

Objective
Curate and push high-signal English news updates twice daily at 7:00 AM and 7:00 PM for Telegram.

Each push must contain 3 sections:
- Industry News
- Financial News
- Global Political News

Each section must contain exactly 10 news items.
Total per push: 30 items.

Coverage
1) Industry News
This category includes:
- FX / CFD
- Crypto
- Prediction Markets
- Retail Trading App Technology

2) Financial News
Major financial and macroeconomic developments with broad market relevance.

3) Global Political News
Major political developments with meaningful market, regulatory, geopolitical, or cross-border impact.

Output format
Output in English only.
Do not include source names.
Do not include summaries.
Do not include source labels.
Do not include commentary before or after the list.
You MUST output exactly 3 sections in this exact order:
Industry News
Financial News
Global Political News

Under each section, you MUST output exactly 10 items.
For each section:
1. Headline
   Read more: link
2. Headline
   Read more: link
3. Headline
   Read more: link
4. Headline
   Read more: link
5. Headline
   Read more: link
6. Headline
   Read more: link
7. Headline
   Read more: link
8. Headline
   Read more: link
9. Headline
   Read more: link
10. Headline
    Read more: link

Each item must have:
- Number prefix (1., 2., 3... 10.) exactly as shown
- Headline on the same line after the number
- Read more: link on the next line with indentation

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Financial News
Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Global Political News
Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Headline
Read more: link

Formatting rules are strict:
exactly 10 numbered items per section
exactly 3 sections
numbering must visibly appear as 1. 2. 3. ... 10.
no bullets
no source labels
no summaries
no commentary before or after the list

Selection rules
Select the top 10 stories for each category.
Prioritize relevance, freshness, credibility, impact, and reader interest.
Use browsing popularity / visibility as an important ranking signal, but do not use low-quality or spammy sites.
If a story is high-ranking but has already been pushed before, skip it and move to the next ranked story.
Try to maximize signal and usefulness for finance and trading readers.

Deduplication rules
Very important:

Within the same push:
- Avoid duplicate stories within each category.
- Avoid the same event appearing in multiple categories in the same push.
- If the same event could fit multiple categories, place it in the single most appropriate category only.

Across the two daily pushes:
- Avoid repeating stories already pushed at 7:00 AM in the 7:00 PM push.
- Avoid repeating stories already pushed at 7:00 PM in the next 7:00 AM push unless there is a materially new development.

What counts as a materially new development:
Only allow a repeated topic if there is a genuine new update, such as:
- official ruling
- confirmed regulation
- launch went live
- acquisition completed
- major CEO/founder/public statement changing the situation
- meaningful legal, policy, market, or product development

If two articles describe the same core event without meaningful new information, keep only one.

Preferred sources
Use only high-credibility sources.

Major financial media:
- Reuters
- Bloomberg
- Financial Times
- Wall Street Journal
- CNBC
- MarketWatch
- Barron's

Industry / trade media:
- Finance Magnates
- FX News Group
- The Block
- CoinDesk
- Cointelegraph (use selectively)
- Decrypt (use selectively)

Primary sources:
Especially for Crypto and Prediction Markets, prefer:
- official company blogs
- official newsroom pages
- official product announcement pages
- official regulator / court / central bank / government websites
- official CEO / founder blogs or clearly authentic official statements

Exclusions
Do not use:
- AI-generated news sites
- spammy aggregators
- SEO farms
- anonymous repost blogs
- shallow rewrites with no original reporting
- rumor-only posts
- low-quality clickbait
- generic AI-generated "market prediction" articles

Inclusion filter
Industry News: include high-signal developments in:
- FX / CFD brokers
- Crypto exchanges, regulation, custody, infrastructure, payments
- Prediction market platforms, product, legal, regulatory, or company updates
- Retail trading apps, trading technology, onboarding, KYC, execution, charting, APIs, product launches, infrastructure, acquisitions, licensing

Avoid:
- promotional fluff
- recycled exchange token listings without significance
- trivial partnership announcements

Financial News: include:
- central banks
- inflation, jobs, GDP, rates, liquidity
- major equity / bond / FX / commodity developments
- banking, credit, funding, institutional market structure developments

Avoid:
- routine price recap articles with no real new event
- low-value market commentary

Global Political News: include:
- elections
- wars, ceasefires, sanctions
- major US / EU / China policy moves
- trade restrictions
- legislation and policy with financial, regulatory, or geopolitical impact

Avoid:
- celebrity politics
- partisan opinion content
- low-signal political commentary

Ranking logic
For each category, rank candidates by:
- importance to the target audience
- freshness
- credibility of source
- uniqueness / non-duplication
- likely reader interest
- broader market or geopolitical impact

If two stories are similar:
- choose the more authoritative source
- choose the more original report
- choose the story with greater market relevance

Final rule
Output only the final Telegram-ready list in English.
No internal reasoning.
No source labels.
No summaries.
No extra commentary.