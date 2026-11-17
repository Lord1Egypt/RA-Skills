# medication-information-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**17 endpoints across 1 platform group(s).**

## GoodRx (17)

### `goodrx_answer`

- **HTTP:** `GET /goodrx/answer`
- **What:** Get a GoodRx health question and answer. Returns one GoodRx health question with its short answer, supporting paragraphs, the source article, the drug it is about, more questions about that drug, related articles, and related medications. Use a slug from /goodrx/answers.
- **Params:** `slug` (string, **required**) — Question slug from /goodrx/answers

### `goodrx_answers`

- **HTTP:** `GET /goodrx/answers`
- **What:** List GoodRx health questions. Returns GoodRx's medication and health questions: the index's top questions and every question with its slug, grouped by drug where GoodRx's index groups it (questions GoodRx lists only in its sitemap carry just their slug). Use a slug with /goodrx/answer.
- **Params:** _none_

### `goodrx_brands`

- **HTTP:** `GET /goodrx/brands`
- **What:** List GoodRx featured brand-name drugs. Lists the brand-name drugs GoodRx features on its brand-name drugs page. Each entry has the drug name, `slug`, GoodRx URL, description, information URL and lowest price where shown. The `slug` feeds the drug prices endpoint. If GoodRx is unreachable, a retained copy up to about a day old is returned and flagged with an `X-Availability-Mode: stale` header.
- **Params:** _none_

### `goodrx_class`

- **HTTP:** `GET /goodrx/class`
- **What:** List drugs in a GoodRx drug class. Returns the drugs GoodRx lists for one drug class, with each drug's lowest displayed price and summary. Use a slug from /goodrx/classes.
- **Params:** `slug` (string, **required**) — Class slug from /goodrx/classes

### `goodrx_classes`

- **HTTP:** `GET /goodrx/classes`
- **What:** List GoodRx drug classes. Lists the drug classes in GoodRx's class directory, such as ACE Inhibitors, with each class name, GoodRx URL and the `slug` used to look up that class. If GoodRx is unreachable, a retained copy up to about a day old is returned and flagged with an `X-Availability-Mode: stale` header.
- **Params:** _none_

### `goodrx_comparison`

- **HTTP:** `GET /goodrx/comparison`
- **What:** Get a GoodRx drug comparison. Returns a GoodRx head-to-head drug comparison's key takeaways and the two drugs compared, with their price-page and information slugs. Use a slug from /goodrx/comparisons or /goodrx/drug-info alternatives.
- **Params:** `slug` (string, **required**) — Comparison slug

### `goodrx_comparisons`

- **HTTP:** `GET /goodrx/comparisons`
- **What:** List GoodRx drug comparisons. Lists GoodRx's head-to-head drug comparisons grouped by health topic, for example ADHD. Each comparison has a name, a `slug` for the comparison lookup and its GoodRx URL. If GoodRx is unreachable, a retained copy up to about a day old is returned and flagged with an `X-Availability-Mode: stale` header.
- **Params:** _none_

### `goodrx_condition`

- **HTTP:** `GET /goodrx/condition`
- **What:** Get a GoodRx health condition overview. Returns a health condition's GoodRx overview article as titled sections (definition, types, causes, symptoms, diagnosis, medications, treatments, prevention, references), with the condition's alternate name, authors, publish and modified dates, the medications-list URL, and related articles. Use a slug from /goodrx/conditions.
- **Params:** `slug` (string, **required**) — Condition slug from /goodrx/conditions

### `goodrx_condition_drugs`

- **HTTP:** `GET /goodrx/condition-drugs`
- **What:** List GoodRx medications for a condition. Returns the medications GoodRx lists for one health condition, with each drug's lowest displayed price and summary. Use a slug from /goodrx/conditions whose has_medications is true.
- **Params:** `slug` (string, **required**) — Condition slug from /goodrx/conditions

### `goodrx_conditions`

- **HTTP:** `GET /goodrx/conditions`
- **What:** List GoodRx health conditions. Lists the health conditions in GoodRx's conditions directory, with each condition's name, `slug` and GoodRx URL. `has_medications` tells you whether GoodRx publishes a medications list for that condition. If GoodRx is unreachable, a retained copy up to about a day old is returned and flagged with an `X-Availability-Mode: stale` header.
- **Params:** _none_

### `goodrx_drug_guide`

- **HTTP:** `GET /goodrx/drug-guide`
- **What:** Get a GoodRx drug guide. Returns one dedicated GoodRx drug guide. side-effects: common and less common side effects with reported frequencies, serious and reported side effects, and the label source. dosage: coupon price per dosage and quantity for each dosage form, and typical dosing. interactions: interacting drugs grouped by severity (not_recommended, usually_not_recommended, increased_risk), with GoodRx slugs where linked. Includes reviewer, last-reviewed date, and related guides. Use pairs from /goodrx/drug-guides; a drug without that guide returns 404. Requests use US egress because GoodRx is US-only.
- **Params:** `slug` (string, **required**) — Drug slug from /goodrx/drug-guides; `topic` (string, **required**) — Guide topic

### `goodrx_drug_guides`

- **HTTP:** `GET /goodrx/drug-guides`
- **What:** List GoodRx drug guides. Returns GoodRx's dedicated drug guide pages (side effects, dosage, and interactions) as drug slug and topic pairs with last-modified dates, optionally filtered by topic and by the first character of the drug slug. Use the pairs with /goodrx/drug-guide.
- **Params:** `letter` (string, optional) — First character of the drug slug: a-z or 0-9; `topic` (string, optional) — Guide topic

### `goodrx_drug_info`

- **HTTP:** `GET /goodrx/drug-info`
- **What:** Get GoodRx drug information. Returns a drug's GoodRx information page as titled sections (uses, side effects, pros and cons, pharmacist tips, risks and warnings, dosage, interactions, contraindications, alternatives, pill images, references, and common questions), plus authors, publish and review dates, FAQs, and comparison links to alternatives. With audience=pets it returns the drug's cat and dog page (veterinary uses, side effects, and dosing) for drugs listed by /goodrx/pet-medications; other drugs return 404. Requests use US egress because GoodRx is US-only.
- **Params:** `audience` (string, optional) — people for the general page, pets for the cat and dog page; `slug` (string, **required**) — Drug slug from /goodrx/drugs (or /goodrx/pet-medications for audience=pets)

### `goodrx_health_article`

- **HTTP:** `GET /goodrx/health-article`
- **What:** Get a GoodRx Health article. Returns one GoodRx Health article: headline, description, authors, medical reviewers, published and modified dates, category tag, key takeaways, the body as headed sections of paragraphs and lists, FAQs, references, and related medications. Requests use US egress because GoodRx is US-only.
- **Params:** `path` (string, **required**) — Article path from /goodrx/health-articles (or a www.goodrx.com article URL)

### `goodrx_health_articles`

- **HTTP:** `GET /goodrx/health-articles`
- **What:** List GoodRx Health articles. Returns one page of GoodRx Health articles in a section, optionally one topic, most recently modified first: each article's path, section, topic, URL, and last-modified date, with total and total pages. Use a path with /goodrx/health-article.
- **Params:** `page` (integer, optional) — Page number, starting at 1; `page_size` (integer, optional) — Articles per page (1-200); `section` (string, **required**) — Article section; `topic` (string, optional) — Topic slug from /goodrx/health-topics

### `goodrx_health_topics`

- **HTTP:** `GET /goodrx/health-topics`
- **What:** List GoodRx Health article topics. Returns every GoodRx Health article topic as section and topic pairs with article counts and last-modified dates, optionally for one section. Sections: conditions, health-topic, well-being, pet-health, insurance, classes, drugs, healthcare-access, corporate, hcp (clinician resources), and drug (articles about one drug; the topic is the drug slug). Use the pairs with /goodrx/health-articles.
- **Params:** `section` (string, optional) — Article section

### `goodrx_pet_medications`

- **HTTP:** `GET /goodrx/pet-medications`
- **What:** List GoodRx pet medications. Lists the drugs that have a GoodRx information page for cats and dogs (21 on 2026-10-03). Each entry has the drug `slug` and the URL of its pet page; the `slug` can be passed to the drug information lookup with `audience=pets`. A retained copy up to about a day old is returned, flagged `X-Availability-Mode: stale`, if GoodRx is unreachable.
- **Params:** _none_
