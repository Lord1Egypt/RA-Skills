# API Reference

Base URL: `https://www.momaiagent.com/api/kb`

## Boundary Note

This reference covers the current public `KB` surfaces.

- The broader site source-of-truth is `articles + citations`.
- The smaller `kb_*` surfaces are only one part of the public answer layer.
- The public `insights` surface is another major public coverage layer, derived from evidence-qualified `articles + citations`.
- It does not search the full website `articles` or `/insight/*` corpus.
- If coverage feels narrower than the site, that is expected under the current public skill boundary.

Internal crawl note:

- the crawler now allows the same article title to be stored more than once when the website hostname is different
- same-website duplicate titles are still blocked
- stored `articles.slug` values may therefore carry a hostname suffix such as `-cdc-gov`, `-stanfordchildrens-org`, or `-canada-ca`

## Decision Order

Start here unless there is a clear reason not to:

1. `GET /api/kb/query?q=...`
2. inspect `quick_answer`, `meta.answer_layer`, `safety`, and top `matches`
3. open a more specific surface only if the question needs object-level detail

Prefer this routing:

- direct parenting question -> `query`
- authority-linked structured object -> `foods`, `rules`, `guides`, or `faqs`
- article-derived evidence coverage -> `insights`
- broader navigation path -> `topics`
- short common question -> `faqs`
- broad corpus sweep -> `feed`

Do not treat `feed` as a substitute for full-site article search. It is still limited to the current public KB layer.

## Endpoints

### `GET /api/kb/query?q=...`

Primary agent surface.

Useful params:

- `q=...` required natural-language question
- `locale=US|CA|Global`
- `limit=1-10`

Returns:

- `quick_answer`
- `safety`
- `meta.answer_layer`
- `llm_fallback`
- `matches.faqs`
- `matches.foods`
- `matches.guides`
- `matches.rules`
- `matches.topics`
- `matches.insights`
- `read_next`

Important `quick_answer` fields:

- `kind`
- `title`
- `answer`
- `why_this_applies`
- `evidence_strength.level`
- `evidence_strength.rationale`
- `age_scope`
- `locale_scope`
- `when_to_escalate`
- `confidence`
- `contraindications`
- `review.status`
- `review.reviewed_by`
- `review.last_reviewed_at`
- `review.freshness_days`
- `review.freshness_label`
- `evidence_signals.citation_count`
- `evidence_signals.evidence_level`
- `evidence_signals.primary_sources`

Important `llm_fallback` fields:

- `used`
- `non_authoritative`
- `reason`
- `question`
- `answer`
- `source_url`
- `citations`
- `primary_sources`
- `evidence_level`
- `trustworthiness_score`
- `freshness_days`
- `disclaimer`

Use when:

- the user asks a direct parenting question
- you need a concise answer plus ranked follow-up paths
- you want one endpoint for the first retrieval pass

Interpretation notes:

- Treat `quick_answer` as the first evidence-backed answer candidate, not final clinical truth.
- Prefer the structured `quick_answer` explanation fields over improvised paraphrase when they are present.
- Check `safety.escalate_now` and `safety.reasons` before writing a reassuring answer.
- Prefer `safety.urgency_level` and `safety.escalation_reason_codes` over ad hoc urgency wording.
- Check `meta.answer_layer`.
  - `kb` means a structured KB object won.
  - `insight-fallback` means an evidence-qualified article won.
  - `none` means there was no strong public match.
- Use top `matches` to confirm scope, age, locale, and evidence fit before answering with confidence.
- A good skill answer does not require a `kb` win every time. It requires the strongest public source-linked match from the current answer stack.
- If `llm_fallback` is present, it is supplementary only and should not be described as the authoritative public answer layer.

### `GET /api/kb`

Use for discovery. Returns:

- skill-facing surface names
- endpoint list
- supported query params
- example URLs
- the current public scope of the KB answer layer

### `GET /api/kb/feed?format=json`

Combined read-only knowledge feed.

Useful params:

- `type=rules,foods,guides`
- `locale=US|CA|Global`
- `limit=25`
- `format=json`

Use when:

- the user asks an open-ended guidance question
- you want the broadest public evidence surface first

### `GET /api/kb/foods`

Food-specific surface.

Useful params:

- `slug=...`
- `locale=US|CA|Global`
- `risk=none|low|medium|high`
- `method=...`
- `age=...`

Use when:

- the question is about a specific food
- the answer depends on serving form, age range, or risk

### `GET /api/kb/rules`

Structured rule surface.

Useful params:

- `slug=...`
- `locale=US|CA|Global`

Use when:

- the user needs a clear rule or prohibition
- the answer depends on a safety or compliance boundary

### `GET /api/kb/guides`

Structured guide surface.

Useful params:

- `slug=...`
- `locale=US|CA|Global`
- `type=framework|scenario|nutrition|allergen|pathway|other`

Use when:

- the user needs a longer guidance path
- the answer is more than a single FAQ or food record

### `GET /api/kb/topics`

Topic catalog.

Useful params:

- `slug=feeding-foundations`

Use when:

- the user needs a structured path rather than one answer
- you want to route the user toward broader reading

### `GET /api/kb/faqs`

FAQ surface for common questions.

Useful params:

- `slug=...`
- `category=...`
- `query=...`
- `limit=...`

Notes:

- This endpoint is DB-first.
- If the Supabase `kb_faqs` table is missing, it returns:
  - `"source": "static-fallback"`
  - `"table_status": "missing"`
- Mention that fallback explicitly if you use it in a final answer.

### `GET /api/kb/insights`

Evidence-qualified article surface derived from published `articles + citations`.

Useful params:

- `slug=...`
- `locale=US|CA|Global`
- `hub=feeding|sleep|mom-health|development|safety|recipes`
- `type=explainer|howto|research|faq|recipe|news`
- `query=...`
- `limit=...`

Use when:

- `query` shows `meta.answer_layer = insight-fallback`
- structured KB coverage is weak, but the public API has a strong evidence-qualified article
- you need `citation_count`, `primary_sources`, `evidence_level`, or article-linked read-next support

Important:

- `insights` is not a sidecar demo surface. It is one of the main public coverage layers when structured KB objects are sparse.
- Do not describe it as full-site search. It is still a filtered public evidence subset.

## Professional Answer Pattern

Use this response order whenever the API supports it:

1. `Direct answer`: the shortest defensible answer
2. `Why this applies`: what in the retrieved record makes it relevant
3. `Age / locale scope`: say who or what region it applies to
4. `Urgency`: one of `Emergency now`, `Same-day clinician`, `Routine clinician`, `Home guidance only`
5. `Read next`: one concrete page or path
6. `Evidence`: `source_label`, `source_url`, or joined `sources`

Avoid:

- diagnosis language
- emergency clearance
- personalized treatment decisions
- unsupported certainty beyond retrieved evidence
- claims that the whole website article library has been searched when only `/api/kb/*` was used

## Recommended Answer Stack

Interpret the current public system in this order:

1. `Authority KB first`
2. `Insight/article-derived second`
3. `Topic navigation third`
4. `No strong public source-linked match`

This is more accurate than treating every successful answer as a structured KB win.

## LLM fallback

- `/api/kb/query` may return a separate `llm_fallback` object when the authority-plus-insight-plus-topic stack does not produce a strong direct answer.
- Keep it separate from the source-linked answer.
- Label it clearly as non-authoritative exploratory guidance.

## Response notes

### Foods

Look for:

- `age_range`
- `feeding_methods`
- `serving_forms`
- `risk_level`
- `do_list`
- `dont_list`

### Topics

Look for:

- `focus`
- `summary`
- `url`
- `paths.search`
- `paths.trust`

### FAQs

Look for:

- `question`
- `answer`
- `source_layer`
- `source_type`
- `source_label`
- `source_url`
- `last_reviewed_at`
- `sources`

### Query

Look for:

- `quick_answer.kind`
- `quick_answer.title`
- `quick_answer.answer`
- `quick_answer.why_this_applies`
- `quick_answer.evidence_strength`
- `quick_answer.age_scope`
- `quick_answer.locale_scope`
- `quick_answer.when_to_escalate`
- `quick_answer.confidence`
- `quick_answer.contraindications`
- `quick_answer.evidence_signals`
- `quick_answer.review`
- `quick_answer.source_layer`
- `quick_answer.source_label`
- `quick_answer.source_url`
- `meta.answer_layer`
- `safety.urgency_level`
- `safety.escalation_reason_codes`
- `safety.reasons`
- `safety.message`
- `safety.escalate_now`
- `safety.reasons`
- `safety.message`
- `matches`
- `read_next`

### Insights

Look for:

- `citation_count`
- `evidence_level`
- `primary_sources`
- `citations`
- `last_reviewed_at`
- `source_layer`
- `read_more_url`

### Feed

Each record includes:

- `kind`
- `type`
- `title`
- `summary`
- `locale`
- `reviewed_by`
- `last_reviewed_at`
- `expires_at`
- `sources`

## Degraded Modes

- If `faqs.source` is `static-fallback`, say the answer came from the public site fallback layer rather than the Supabase FAQ table.
- If `query.meta.answer_layer` is `insight-fallback`, say the answer is coming from the evidence-qualified article layer.
- If `quick_answer.review.freshness_label` is `stale`, avoid sounding overly definitive and prefer a cautious framing.
- If `query.quick_answer` is null, do not fake a conclusion. Fall back to the best matching structured object or say the public API does not have a strong source-linked match.
- If `safety.escalate_now` is true, prioritize escalation language before any educational detail.

Coverage caveat:

- A weak or missing KB match does not prove the entire site has no related article.
- It only means the current public KB surface did not return a strong source-linked answer object.

## No-Strong-Match Pattern

Use this structure:

1. state that no strong public source-linked match was found for that phrasing
2. say what related evidence was found, if any
3. state what the API does not establish
4. give one concrete next path or clinician follow-up

If no strong match exists, say:

`I couldn’t find a strong source-linked match in the public Mom AI Agent knowledge API for that phrasing.`

If needed, you may add:

`That does not necessarily mean the broader website has no related article; it means the current public KB answer layer does not expose a strong match for this phrasing.`

## High-Risk Query Checklist

For questions involving infant symptoms or postpartum warning signs, explicitly check:

- age of infant
- locale
- urgency language in `safety`
- whether the answer is educational only
- whether a clinician or emergency referral should be stated first

Common examples:

- newborn fever
- breathing trouble
- seizures or unresponsiveness
- dehydration concerns
- allergic reactions
- heavy postpartum bleeding
- postpartum chest pain
- self-harm or suicidal thoughts
