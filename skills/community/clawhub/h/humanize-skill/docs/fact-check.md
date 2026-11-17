# Fact-check: a depth pass for claims

This document extends the short fact-check workflow in `SKILL.md`. The goal is the same: do not let the rewrite make unsupported facts sound more confident. The means are more specific: a sharper label system, a claim taxonomy, a source hierarchy, a conflict protocol, and a fix matrix that maps each claim state to a concrete textual move.

The fact-check pass is not a vibes check. It is also not a research project. The skill should be **lightweight, conservative, and honest about what it could and could not verify.**

## What this pass actually does

Five things, in order:

1. **Extract** the claim-like sentences from the draft.
2. **Classify** each claim by type (experience, number, prediction, attribution, comparison, causal, definitional, schedule, identity).
3. **Search** in the right places, in the right order: local evidence first, then primary sources, then reputable secondary, then the model's own memory only as a last resort.
4. **Label** each claim with a precise status (see below).
5. **Fix** the text using the fix matrix that maps label to textual move.

If step 3 cannot run (no web tools, sandboxed, off-domain), say so explicitly in the output. Do not pretend the claim is verified.

## The five states, not four

The base `SKILL.md` workflow uses four labels. They are a useful start, but they blur the most important distinction in fact work: *we did not find anything* vs *we found something, and it was weak*. Splitting them is the single highest-leverage change in this pass.

| Label | Meaning | What to write in the text |
| --- | --- | --- |
| `supported` | At least one source of appropriate tier backs the claim. Source recorded with title, URL, date, exact claim it supports. | Keep and cite when the surface is serious; keep without citation when the surface is informal. |
| `weak_support` | Found a source, but it is below the recommended tier for this claim type, or only partially supports the claim, or the match is keyword-overlap rather than substantive. | Hedge or soften, and add an inline source so the reader can judge. Do not present as established. |
| `unverified` | Searched, found nothing solid. Plausible but uncited. | Mark with hedging language ("by some accounts", "anecdotally", or simply state as personal observation) and add a `[needs verification]` note if the user wants a paper trail. |
| `contested` | Found sources that disagree, or found one source contradicting the claim. | Name the tension: "X says ..., Y argues ..." or "this is disputed; ...". Do not pick a side without justification. |
| `stale` | Was true, or widely believed, but newer evidence has moved on. Currency-sensitive. | Re-date the claim or remove it. Do not let a 2019 number stand in for a 2026 situation. |
| `wrong` | Source(s) directly contradict the claim with current evidence. | Remove or rewrite. Do not soften an error into a hedge — that is just a slower form of error. |
| `style_only` | Opinion, preference, forecast of the writer's own behavior, or rhetorical framing. | No change. The fact-check pass does not adjudicate taste. |

The base labels `supported`, `needs_evidence`, `possibly_wrong`, `style_only` are still in the main workflow. `needs_evidence` is a coarse bucket that covers `unverified` + `weak_support`. The depth split is for the final fix matrix; it is not a public API change.

## Claim taxonomy

Different kinds of claim demand different sources, different tolerances, and different fixes. The taxonomy below covers what the rewrite will actually encounter.

### 1. Experience and observation

- *"In 2024 we shipped a 3-region failover to 40,000 customers."*
- *"The team spent 6 weeks on this."*
- *"I have seen this pattern at three previous companies."*

These are the easiest class. They are also the easiest to get wrong in AI drafts, because the model will *invent* experiences to fit the topic. Source priority: **the user's own evidence or sample.** If the user did not supply the experience, do not supply it for them. Remove, soften, or re-cast as the user's *hypothesis* rather than *experience*.

### 2. Numbers and metrics

- *"60% of users churn in the first month."*
- *"Our p99 latency is 95ms."*
- *"The market is worth $4.2B."*

The hardest class. Three sub-issues:

- **Plausibility**: round numbers (60%, $4.2B) are the most common AI hallucination. Watch for them.
- **Source authority**: who measured this, on what sample, when, with what methodology.
- **Currency**: numbers age fast. A 2019 retention figure is rarely 2024's.

Source priority: the user's own data → primary publication (company metrics, government statistics, peer-reviewed paper) → reputable secondary (Reuters, FT, Nature news) → never just "studies show". For benchmark numbers, the standard practice is to cite the source and the date.

### 3. Predictions and forecasts

- *"AI writing tools will replace most marketing copy by 2028."*
- *"Latency will keep dropping as hardware improves."*

These are **not fact-checkable** in the usual sense. They are forecasts. The rewrite should make the speaker of the forecast explicit ("analysts at Gartner project..."), name the time horizon, and ideally name the conditions under which the forecast would be wrong. If the draft hides the speaker, the rewrite surfaces them.

### 4. Attributions and quotes

- *"Einstein said 'insanity is doing the same thing over and over...'"*
- *"According to a 2023 McKinsey report, ..."*

Attributions fail in two opposite ways:

- **Real attribution to wrong source**: Einstein did not say the insanity quote. Common one.
- **Fabricated attribution to look authoritative**: "studies show", "experts agree", "industry reports suggest".

For real attributions, verify with a primary source (the speaker's own writings, the original publication). For vague attributions, the rewrite either names a real source or removes the attribution. The middle ground "experts say" gets cut.

### 5. Causal claims

- *"Latency dropped because we moved to gRPC."*
- *"Customer churn fell after we raised prices."*

Causal claims are easy to overstate. Correlation is not causation, and the model's job in the rewrite is to soften "because" to "after" or "when" unless the cause is genuinely established. Look for:

- A mechanism that is on the page (not just temporal sequence).
- A counterfactual: would the outcome have happened anyway, in the absence of the supposed cause?
- An alternative cause the writer is not naming.

If the rewrite cannot defend the cause, write it as observed-after, not caused-by.

### 6. Comparisons and rankings

- *"We are the fastest in our category."*
- *"Twice as reliable as the next best alternative."*

Comparisons are usually *unsupported* unless the rewrite names:

- What the comparison is against (which competitor, which version).
- The metric and measurement.
- The date the comparison was made.

"We are the fastest" without those three pieces is marketing, not fact. The rewrite should either add the pieces (when the user has them) or remove the claim.

### 7. Identity and credentials

- *"John Smith is the CEO of Acme Corp."*
- *"Dr. Patel has 20 years of experience in pediatric oncology."*

Identity claims fail when the model confuses people with similar names. The fix is straightforward: if the surface is going to readers who will see the name (a press release, a profile, a citation), verify with a primary source. If the surface is internal and the name is incidental, the risk is lower, but still worth a quick search for the obvious "is this the same person who was indicted last year" check.

### 8. Schedule and currency

- *"The Q3 release ships on September 15."*
- *"GDPR fines up to 4% of global revenue."*

Schedules and laws are the highest-risk class because they are often the load-bearing claim of the document. Treat them as a separate pass: for every date, every named regulation, every price, every version number, verify with a current primary source. `stale` is the most common label here.

## Source hierarchy

Sources are not equal. The rewrite should know what it is citing.

### Tier 1 — primary

- The speaker's own writings, transcripts, or papers.
- Official company filings (10-K, S-1, IPO prospectus), earnings calls, official product pages, official changelogs.
- Government statistics agencies, central banks, courts, statutes, regulations.
- Peer-reviewed research papers.
- Standards bodies (W3C, IETF, ISO, RFC).
- Repository source code and official documentation.

### Tier 2 — reputable secondary

- Major newspapers of record (Reuters, AP, FT, NYT, WSJ, BBC).
- Established trade press (TechCrunch for tech, Politico for politics, etc., with awareness of bias).
- Industry analyst reports (Gartner, Forrester, IDC) — note the sponsor and methodology.
- Reference works (Britannica, Stanford Encyclopedia of Philosophy, OpenAlex / Crossref for academic lookup).
- Established encyclopedic sources (Wikipedia, only as a starting point — follow citations).

### Tier 3 — usable with caution

- Preprints (arXiv, SSRN): not peer-reviewed. Note as such.
- Conference talks and slides: useful for what was said, not for what is true.
- Vendor case studies and white papers: sponsored; treat as marketing.
- Well-maintained individual blogs: useful when the author is named and qualified on the topic.
- Stack Overflow / GitHub Issues / Reddit / Hacker News: useful for current practice, weak for facts.

### Tier 4 — avoid

- SEO content farms and listicles with no named author.
- Content that quotes a tier-3 source as if it were tier-1.
- AI-generated explainer articles with no provenance.
- Anything where the URL is the only evidence ("I read it somewhere").
- Anything more than 5 years old on a fast-moving topic, unless the claim is about history.

The hierarchy is a guideline, not a rule. A 2024 stack-overflow answer with a code snippet is more useful for "does this regex work" than a 2019 peer-reviewed paper on regex engines. Match the source to the question.

## Time and staleness

The hardest part of fact work is that the world moves. A fact-check pass that does not track time is a fact-check pass that will become wrong.

### Mark the date

Every fact-checked claim in the notes should record:

- The date the source was published or last updated.
- The date the fact-check was performed.

If a claim's source is older than 18 months and the topic is fast-moving (tech, AI, finance, regulation, prices, releases), flag for re-verification. Use exact dates, not relative ones ("last year" is not enough).

### Watch for "still believed" claims

Many AI drafts repeat claims that *used to be true* but are no longer accurate. The "studies show" pattern hides these. Specific tells:

- "According to recent research..." without a year.
- Numbers that have not changed in 3+ years on a moving topic.
- "Industry standard" claims that predate a major shift (e.g. the rise of LLMs, the end of a regulation, a major deprecation).

### Handle re-dating gracefully

When a stale claim is fixable, re-date it. "Studies in 2019 found..." is more honest than "studies have found...". When the new state is unknown, the rewrite should *not* re-assert the old state; it should say "as of [latest known date], ..." or remove the claim.

## Conflict handling

When sources disagree, do not pick a side based on the model's own intuition. Use this protocol:

1. **List** the disagreeing sources, with tier and date.
2. **Bias to higher tier**: peer-reviewed > trade press > blog. If a tier-1 source contradicts a tier-3 source, the tier-1 source wins.
3. **Bias to newer**: on fast-moving topics, prefer the more recent source unless the older one has methodological weight.
4. **Bias to primary**: if the disagreeing sources are different people talking about the same primary record, the primary record wins.
5. **Bias to less motivated**: a source with commercial interest in the claim is weaker than one without.

If after this the conflict is still unresolved, the rewrite presents both: "Source A says X, source B says Y, the disagreement is unresolved."

If the rewrite must pick a side, say so: "We follow source A because [reason]." The user then has the audit trail.

## The fix matrix

This is the part the base workflow glosses over. Each claim state maps to a concrete textual move.

| Claim state | Default move | Inline cue | Citation needed? |
| --- | --- | --- | --- |
| `supported` | Keep the claim, add a citation if the surface is formal. | None, or `[1]` | Yes if formal surface, no if informal |
| `weak_support` | Hedge in the text, add the source. | "by some accounts", "according to [...]", "early evidence suggests" | Yes, with the limitation visible |
| `unverified` | Mark as personal observation or hypothesis; remove if no role. | "I think", "in my read", "based on what I have seen" | Optional, only if a source can be added |
| `contested` | Name the tension. | "X argues ...; Y argues ...; we are not sure" | Both sources |
| `stale` | Re-date or remove. | "as of 2024", "through 2023" | Yes |
| `wrong` | Remove or rewrite. | None — do not hedge a known error | No (claim should not survive) |
| `style_only` | No change. | None | No |

The "inline cue" column is a starting list. Match the user's voice when adding hedges. A voice profile that does not hedge should not be made to hedge. In that case, the move is to *remove* the claim rather than to soften it badly.

### When to remove vs. soften

The default instinct is to soften. Often remove is the right call.

- **Remove when** the claim is load-bearing for the paragraph, the user's voice does not hedge, and the evidence is too weak to defend.
- **Soften when** the claim is supporting, not load-bearing, and a hedge preserves the user's argument.

A good test: if the claim is the *thesis* of the paragraph and the evidence is `unverified` or `wrong`, the rewrite needs a different thesis. Do not hedge a thesis into mush.

## The evidence file shape

A good `evidence.md` is structured, not narrative. Recommended shape:

```markdown
# Evidence for [topic]

## Sources

### [Source 1 — e.g. "Anthropic Claude 3.5 Sonnet model card"]
- URL: https://...
- Date: YYYY-MM-DD (publication or last-updated)
- Tier: 1 (primary) / 2 (reputable secondary) / 3 (caution)
- Claims it supports:
  - "[exact claim from the draft]"
  - "[exact claim from the draft]"
- Limitations: [what it does not cover, who funded it, sample size]

### [Source 2]
...

## Notes

- Source A and source B disagree on X. We follow A because [reason].
- Source C is older than 18 months; flag for re-verification.
- The user supplied this fact in their draft: "[exact fact]". Treat as the user's claim, not a verified fact.
```

When the user does not provide an evidence file, the agent builds this in memory and surfaces the structure in the notes when it is asked for. The structure is what the model reasons over; the prose is what the user reads.

## Tool unavailability

If web/search tools are unavailable, the fact-check pass changes shape but does not get skipped.

- All claims become `unverified` by default, with a per-claim note: "would normally verify via [source type] but search is unavailable."
- The final output must say so. Do not present unverified claims as `supported`.
- The fix matrix still applies: `unverified` claims get hedged or removed, not asserted.
- A short note in the rewrite output: "Fact-check pass performed against local evidence only. External verification was not available; any claim about [current/factual/risky topic] should be re-checked before publication."

This is the conservative default. It is better to say "I am not sure" than to silently downgrade the standard.

## Author-provided errors

Sometimes the user supplies the wrong information in good faith. A user might repeat a statistic they saw on a listicle, quote a politician's line that was later corrected, or claim a personal experience that did not happen as they remember it.

How to handle this:

- The fact-check pass is on the **text**, not the user. If the user's draft says "we doubled revenue in 2024", and the evidence does not support it, the rewrite should not assert it even though the user is the source of the claim.
- Phrase the correction gently. "I do not see a public source for this — do you have a doc I can cite?" is better than "you are wrong."
- For personal experiences, the bar is different. The user's own experience is theirs; the rewrite should not contradict it lightly. But for numerical, factual, or attributed claims, the rewrite should verify.
- For social or financial cost, do not strip the user's voice. The default move is to add a hedge, not a contradiction.

## AI's specific factual failure modes

The fact-check pass interacts with the AI-pattern pass. The catalog below overlaps with `docs/anti-ai-patterns.md` section 5, but the lens is *factual* rather than *stylistic*.

| Pattern | Why it happens | What to look for | Fix |
| --- | --- | --- | --- |
| **Invented statistic** | The model fills a gap with a plausible number. | Round percentages, large round numbers ($4B, 87%), no named source. | Remove or replace with the user's own data. |
| **Fuzzy attribution** | The model wants to look authoritative without naming a source. | "Studies show", "experts agree", "industry reports suggest", "researchers have found". | Replace with a named source, or cut. |
| **Anachronism** | The model does not track time well. | A 2018 statistic used as if it were 2025. A deprecated product called "current". | Re-date or remove. |
| **Confabulated authority** | The model names a real institution but with the wrong claim. | "According to a Stanford study..." with a study that does not exist. | Search the actual study; if not found, remove. |
| **Universal claim** | The model avoids picking a population. | "Most users", "every team", "research has consistently shown". | Add a population ("in our 2024 pilot, 38% of users...") or cut. |
| **Implied causation** | The model uses "because" without a mechanism. | "X improved because of Y" with no on-page mechanism. | Soften to "after" or "when". |
| **False confidence on a soft topic** | The model speaks with the same voice on hard facts and on speculation. | Predicting the future with the same grammar as a citation. | Add hedges to predictions; keep facts clean. |
| **Hallucinated quote** | The model produces text that *sounds* like a famous person. | Quotes that are not in the speaker's corpus; quotes on the wrong topic. | Verify with the speaker's own writings; remove if not found. |
| **Wrongly attributed identity** | The model confuses names. | Two people with similar names; a position held by a different person. | Verify with a primary biographical source. |

A single revision of the draft that catches all of these is rare. The fact-check pass is iterative: one pass to find the obvious ones, one to find the subtle ones, one final sweep to confirm.

## Citation form

The rewrite should not invent a citation style. Match the surface and the user's existing convention.

- **Markdown report or blog post**: numbered references at the end, inline `[1]` markers, or a `## Sources` section. Include title, URL, and date.
- **Newsletter / email**: short parenthetical — "per the 2024 Anthropic model card" — and a link.
- **Academic / formal**: full citation the first time, author-date or numbered after.
- **Internal docs**: link in the body. Format is less important than the audit trail.

Minimum viable citation in any surface: **title, URL, date**. Without date, the reader cannot judge staleness.

## What this pass is not

- It is not a research project. The skill is lightweight on purpose. A claim that would require a 30-minute literature review is `unverified` after one quick search, and that is the right label.
- It is not a guarantee. The skill cannot prevent every error. It can move the most common AI factual failure modes from "untracked" to "labeled and either fixed or flagged".
- It is not an excuse to drop claims. Some claims are worth keeping with a hedge. The fix matrix is the guide.
- It is not a substitute for an expert on the topic. If the user is writing about a domain the model does not know well, the fact-check pass surfaces the gaps; the user supplies the final say.
- It is not the same as the Oumi HallOumi system, which uses a fine-tuned model for the same task. This skill does the same job with editorial judgment, off-the-shelf search tools, and the user's own evidence. See `docs/reference-analysis.md` for what was borrowed and what was simplified.

## A note on the audit trail

Every fact-check pass leaves a trail. The trail is what makes the rewrite trustworthy.

- `notes.md` records the per-claim decision, with the source and the date.
- The final output notes when the pass was abbreviated (no external search, no local evidence file, etc.).
- The user can ask "where did this come from?" and the agent can answer per claim.

Without a trail, the fact-check pass is performance. With one, it is work.
