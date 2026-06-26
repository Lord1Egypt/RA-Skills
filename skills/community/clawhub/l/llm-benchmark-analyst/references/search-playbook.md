# Search Playbook

Use this playbook to keep the search token-efficient, version-correct, and benchmark-scope-safe.

## 1) identity-first retrieval
Before searching any leaderboard, normalize:
- provider
- model family
- exact version or release label
- preview or stable status
- reasoning / non-reasoning mode if the provider distinguishes them
- tool mode if the benchmark has with-tools vs without-tools tracks
- benchmark row aliases used by the site

Never let the score search happen before identity normalization.

## 2) token-efficient search order
Use this exact sequence whenever possible:

1. **domain routing**
   - open `core-dimensions.md`
   - choose 1 primary dimension, or up to 3 for broad requests
2. **benchmark shortlist**
   - within the chosen dimension, list the first 3-6 benchmarks most likely to answer the question
   - confirm each benchmark is inside `benchmark-source.md`
3. **website retrieval**
   - search official pages for those shortlisted benchmarks
   - extract exact rows, variants, and dates
4. **overlap expansion**
   - inspect benchmark descriptions and overlap tags
   - add only the secondary benchmarks that materially change the answer
5. **synthesis**
   - map evidence back to the dimension level
   - only then write the report

## 3) benchmark shortlisting rules
Pick benchmarks that are:
- recent enough to reflect current models
- official or benchmark-author maintained
- directly relevant to the asked capability
- strong enough to avoid one-benchmark narratives

Do not over-search by default. Start narrow, expand when:
- scores conflict
- one benchmark is clearly noisy or defective
- the user asked for `comprehensive` or `exhaustive`
- the question spans multiple sub-capabilities

## 4) overlap expansion rules
After shortlisting, inspect benchmark descriptions for latent overlaps.

### for coding
Search not only classic coding boards, but also:
- terminal and repo benchmarks
- agentic coding benchmarks
- research/science benchmarks with code generation or optimization components
- project-level builders, review, and long-horizon coding tasks

### for multimodal
Search not only vision boards, but also:
- OCR and document understanding
- GUI/computer-use benchmarks
- multimodal deep-research benchmarks
- audio/video/omni tasks

### for reasoning
Search not only academic reasoning boards, but also:
- composite boards with reasoning-heavy mixes
- math/science research benchmarks
- community reasoning or adversarial consistency boards

### for vertical domains
Search not only the domain benchmark, but also:
- tool-use and planning benchmarks for the workflow shape
- multimodal or document benchmarks if the domain task depends on documents or images
- long-context or grounding benchmarks if the task requires retrieval and synthesis

## 5) evidence collection checklist
For each benchmark row, capture:
- benchmark name
- what it tests in a short clause
- exact score and unit
- exact model row name
- rank or relative placement if visible
- variant or split
- time point or access date
- official vs vendor-reported vs aggregator note
- warning tag from `data-defect-warnings.md`

## 6) source priority
Prefer sources in this order:
1. benchmark official leaderboard or official benchmark site
2. benchmark paper, official README, or benchmark-author post
3. authoritative aggregator that clearly cites benchmark sources
4. vendor self-report
5. community spreadsheet or screenshot as a last resort

When using vendor self-reports, label them clearly as `vendor-reported`.

## 7) exact comparison rules
Never compare unlike-with-unlike.

Always preserve:
- verified vs original benchmark
- public vs private split
- with-tools vs without-tools
- easy / medium / hard
- pass@1 vs pass@k
- exact score unit (accuracy, solved %, elo, success rate, index score, cost-adjusted score, time horizon, etc.)

Do not average raw scores across different metrics. If you need synthesis, use narrative convergence, rank patterns, or bucketed strength calls.

## 8) anchor-comparison rules
When the user asks for a report on a target model, add these comparisons if relevant:

### code or agentic coding
Compare with:
- current latest Claude Opus
- current latest Claude Sonnet
- current latest GPT-family model

### multimodal
Compare with:
- current latest Gemini-family model
- current latest GPT-family multimodal model if relevant

### intelligence / reasoning
Compare with:
- current latest GPT-family model
- optionally a second frontier reference if it is clearly central to the discussion

Search the `latest` anchor names first; do not trust memory.

## 9) predecessor-comparison rules
If the model family has a meaningful predecessor:
- prefer the immediate prior generation or last generally available comparable model
- compare only where the benchmark mode matches
- if the predecessor is missing from most modern leaderboards, say the comparison is partial
- do not force a predecessor comparison when the naming or deployment mode changed too much

## 10) image-only leaderboard fallback
If the leaderboard page hides the table in a canvas, chart, screenshot, or image:
- switch to multimodal inspection
- extract only visible numbers
- mark them as `image-extracted`
- avoid reading tiny or blurred text aggressively
- if the image is too poor, say `leaderboard appears image-only but the visible text is not reliable enough to extract`

## 11) confidence rubric
Use an explicit confidence note in the report.

- **high confidence**: multiple fresh official benchmarks agree, low warning burden, exact row match
- **medium confidence**: some official evidence but partial freshness gaps, moderate benchmark warnings, or a few vendor-reported rows
- **low confidence**: evidence depends on warned benchmarks, image-extracted values, stale rows, or ambiguous model aliases

## 12) common failure modes to avoid
- using a stale benchmark row for a newer model version
- comparing with-tools and without-tools as if they are one number
- using the wrong benchmark variant
- over-weighting a benchmark with published defects
- ignoring sub-scores and only quoting totals
- skipping overlap benchmarks because they live in a different section of the source document
- adding a benchmark that is not in `benchmark-source.md`
