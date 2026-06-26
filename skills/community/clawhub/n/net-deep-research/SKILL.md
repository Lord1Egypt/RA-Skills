---
name: net-deep-research
description: Perform deep multi-source internet research before answering. Use when the user prefixes a request with /net, asks for the latest information, wants real-time facts, requests web verification, asks which framework, tool, product, policy, or implementation path is best right now, or needs evidence-based answers synthesized from multiple public sources such as official docs, official sites, GitHub, package registries, standards sites, and other stable public references.
---
# Net Deep Research

When this skill is triggered, do not answer immediately.

Turn the request into a controlled research workflow:
1. classify the question,
2. normalize the scope,
3. decompose it into subquestions,
4. derive critical claims,
5. research in rounds,
6. resolve or expose conflicts,
7. answer from a structured evidence map.

## Trigger Handling

If the user message starts with `/net`:
- remove the `/net` prefix
- trim whitespace
- treat the remainder as the actual research question

Then restate the question in one sentence before researching.

## Goal

Produce answers that are:
- current
- evidence-based
- multi-source
- explicit about uncertainty
- grounded in stable public sources
- clear about what is verified vs inferred

## Hard Rules

Apply these rules strictly:
1. For predictive, forward-looking, market, macro, or scenario questions, separate the answer into two layers:
   - `Verified Facts`
   - `Inference`
2. Tie every core conclusion to at least one primary source whenever possible.
3. Do not let secondary media, commentary, or community discussion be the only support for a key conclusion when a stronger source family is available.
4. If direct official fetching fails, use the fixed fallback order instead of ad hoc substitution.
5. Do not skip subquestion decomposition for non-trivial questions.
6. Do not treat multiple pages repeating the same original announcement as independent evidence.

## Mode Selection

Choose one `primary_mode`. Add one `secondary_mode` only if it clearly helps.

### Mode A: Current Fact Check
Use for questions about latest status, current availability, recent releases, or whether something is already live.

### Mode B: Capability Or Compatibility Verification
Use for questions about support, compatibility, feature availability, plans, versions, models, or platforms.

### Mode C: Implementation Or How-To Research
Use for questions about how to build, integrate, deploy, or implement something, including best practices and architecture.

### Mode D: Comparison, Selection, Or Policy Confirmation
Use for questions about choosing among alternatives, policy confirmation, framework selection, official rules, or tradeoff analysis.

## Classification Rules

Apply these rules in order:
1. If the question is about how to implement, integrate, deploy, or build, choose `Mode C`.
2. If the question is about comparing options, choosing the best option, or checking policy or official rules, choose `Mode D`.
3. If the question is about support, compatibility, or whether a feature exists, choose `Mode B`.
4. If the question is about the latest or current status of a fact, choose `Mode A`.

Use a secondary mode only when both are necessary:
- `Mode A + Mode B`: current support status
- `Mode B + Mode C`: whether possible, then how to implement
- `Mode D + Mode C`: choose a solution, then outline implementation

## Question Normalization

Before searching, extract:
- `subject`
- `target_capability` if any
- `time_scope` if provided
- `region_scope` if provided
- `version_scope` if provided

Do not invent missing scopes.

Then rewrite the request as one normalized question.

## Subquestion Decomposition

Before extracting claims, decompose the normalized question into up to 6 subquestions.

Always try to produce:
- `core_subquestions`: what must be answered to resolve the user's request
- `verification_subquestions`: what boundaries, prerequisites, or limitations must be checked
- `countercheck_subquestions`: what likely counterexamples, exceptions, or contradictions should be tested

For simple questions, 2-3 subquestions is enough.
For complex questions, use 4-6 subquestions.

Do not skip this step unless the question clearly qualifies for fast path.

## Claim Extraction

Derive at most 3 critical claims from the subquestions.

Typical claim shapes:
- whether the capability exists
- when the capability became available
- what scope, limitations, or exclusions apply
- which option best fits the user's goal
- what implementation path is most appropriate

Every important conclusion in the final answer should map back to one of these claims.

## Query Planning

Plan queries per claim, not just per question.

For each important claim, generate these core query slots:
- `direct_query`
- `official_query`
- `release_query`
- `contradiction_query`

Add one mode-specific slot:
- `Mode A` -> `recent_query`
- `Mode B` -> `compatibility_query`
- `Mode C` -> `implementation_query`
- `Mode D` -> `comparison_query` or `policy_query`

Keep the total query count between 4 and 8 for a normal request.

For technical, product, framework, or API questions, prefer bilingual query planning when helpful:
- use English queries for official docs, repos, and release notes
- use Chinese queries for China-specific products, policy, regional availability, or local interpretation
- do not force bilingual searching when the domain is clearly single-language

## Research Rounds

Use a staged research workflow.

### Round 1: Primary Evidence
Search primary and official sources first.
Goal: establish the strongest direct evidence for each claim.

### Round 2: Independent Verification
Add independent support from a different strong source family.
Goal: confirm scope, version, timing, or practical limitations.

### Round 3: Conflict Resolution
Run only when needed.
Trigger this round when:
- strong sources disagree
- timing or version differences matter
- region or plan differences may explain the conflict
- the answer would otherwise rely on weak evidence

Goal: explain the disagreement, not just note it.

## Research Budget And Stop Rules

Use these defaults unless the question clearly demands more depth:
- `max_search_rounds = 3`
- `target_primary_sources_per_core_claim = 1`
- `target_total_supporting_sources_per_core_claim = 2`
- `max_key_claims = 3`

Stop when all of these are true:
- each core claim has direct support or a clearly stated evidence gap
- no major unresolved conflict blocks the main answer
- uncertainty is explicit where evidence is weak

Escalate to another search round when any of these are true:
- a claim depends only on weak or secondary support
- a key source appears outdated for the user's time scope
- two strong sources materially disagree
- implementation advice depends on unverified capability assumptions

## Source Routing

Use source families, not fixed websites, as the primary routing method.

### Mode A Priority
1. official announcement, changelog, release notes
2. official docs
3. official repository releases
4. high-quality secondary reporting

### Mode B Priority
1. official docs
2. API reference or SDK docs
3. official repository, release, or issue
4. package registry pages

### Mode C Priority
1. official docs
2. official repository README, examples, guides
3. package registry pages
4. stable technical references

### Mode D Priority
1. official docs or official sites
2. government, institutional, or standards sources when relevant
3. official repository, pricing, feature, or explanation pages
4. high-quality secondary analysis

## Preferred Source Families

Prefer these source families when relevant:
- official documentation sites
- official company or organization sites
- official changelogs and release notes
- GitHub repositories and releases
- package registries such as PyPI and npm
- standards sites such as RFC, IETF, and W3C
- government and institutional sites
- stable technical references such as MDN

## Accessibility, Stability, And Dedup Rules

Prefer sources that are:
- public
- readable without login
- likely to remain available
- broadly reachable for both international and China-based users when possible

Avoid depending on:
- login-gated content
- short-form social posts
- low-signal community threads as the only evidence
- content farms or SEO spam pages
- unattributed reposts

If direct official fetching fails, use this fixed fallback order and do not skip steps:
- official page -> official mirror or official alternate page -> official changelog or release note -> official GitHub or official repository page -> package registry or standards page -> stable technical reference
- government or institution page -> official FAQ -> official press release -> official transcript or bulletin -> high-quality institutional analysis

Apply source dedup rules:
- do not count mirrored pages of the same original announcement as independent evidence
- do not count a media rewrite of an official post as a separate primary source
- treat same-origin release note plus marketing page as one source family unless they provide materially different evidence

## Source Filtering And Scoring

Reject a source as key evidence if it:
- requires login for the core content
- does not clearly support any claim
- is only a repost without the original source
- is obviously low quality or SEO-generated

Score each candidate source across 6 dimensions, each from 0 to 2.
Apply the rules for each dimension mechanically: start from score 2 and walk down until a condition matches.
Total score range: `0-12`.

---

### 1. authority — who published it

Apply these checks in order. Stop at the first match.

| Condition | Score |
|---|---|
| The domain IS the official domain of the subject under research (e.g. `nextjs.org` for Next.js, `python.org` for Python, `rust-lang.org` for Rust) | 2 |
| The domain IS a `.gov`, `.edu`, or standards-body domain (e.g. `rfc-editor.org`, `w3.org`, `ietf.org`, `iso.org`, `ieee.org`) | 2 |
| The page IS on the subject's own GitHub/GitLab org (e.g. `github.com/facebook/react` for React) | 2 |
| The page IS on a curated developer reference platform (e.g. `MDN`, `caniuse.com`, `web.dev`, `docs.rs`, `nodejs.org/api`) | 1 |
| The page IS an official package-registry entry (e.g. `npmjs.com/package/*`, `pypi.org/project/*`, `crates.io/crates/*`) | 1 |
| The page IS authored by a verified project maintainer or recognized core contributor (e.g. a maintainer's blog, their personal GitHub, a signed commit/issue) | 1 |
| The page IS on an established tech publication with editorial process (e.g. `arstechnica.com`, `lwn.net`, `theverge.com` for product news only) | 1 |
| None of the above match | 0 |

---

### 2. stability — will this URL still work in 12 months

**Prefer automated scoring.** For each candidate URL, run the bundled Python scorer first:

```
python3 tools/score_stability.py --json "<url>"
```

This returns `{"score": <0|1|2>, "rule": "<matched_rule>", "explanation": "..."}`.

Use the returned score directly. Only fall back to manual scoring when the Python runtime is unavailable.

Manual scoring rules (identical to the script's logic, for reference):

| Condition | Score |
|---|---|
| The URL IS a GitHub/GitLab permalink: `/releases/tag/*`, `/blob/<sha>/*`, `/commit/*`, or a repo root with a fixed name | 2 |
| The URL IS on `docs.*` subdomain, `*.readthedocs.io`, `*.github.io`, or a `/docs/*` path on the official domain | 2 |
| The URL IS a `.gov`, `.edu`, standards-body, or institutional archive page | 2 |
| The URL IS a package-registry permalink (e.g. `npmjs.com/package/<name>`, `pypi.org/project/<name>`) | 2 |
| The URL IS an official blog post on the project's own domain (e.g. `nextjs.org/blog/*`) | 1 |
| The URL IS an official mirror or alternate-source page | 1 |
| The URL IS a reputable news outlet or established tech-publication article | 1 |
| The URL IS a third-party blog platform (e.g. `medium.com`, `dev.to`) — content may be reorganized or paywalled later | 1 |
| The page IS a social-media post (Twitter/X, Reddit, Hacker News, etc.) or a personal blog with no institutional backing | 0 |
| The URL contains session IDs, temporary tokens, or link-shortener domains (`t.co`, `bit.ly`, etc.) | 0 |

---

### 3. accessibility — can anyone read it without barriers

Apply these checks in order. Stop at the first match.

| Condition | Score |
|---|---|
| Page loaded successfully with NO login prompt, NO paywall overlay, NO captcha challenge, and NO geo-block | 2 |
| Page loaded but requires a free account to view beyond the first N paragraphs (e.g. Medium metered wall) | 1 |
| Page loaded but the site is known to be geo-restricted in some major regions (e.g. `bard.google.com` in specific regions) | 1 |
| Page requires login or paid subscription to view the core content; the visible portion is only a summary | 0 |
| Page is entirely behind a paywall, login wall, or captcha gate | 0 |

---

### 4. freshness — how current relative to the question's time scope

This dimension is scored **relative to the question**, not by absolute recency alone.

**Step 1: Determine the reference window.**

| Question has... | Reference window |
|---|---|
| Explicit `time_scope` (e.g. "in 2024", "last month", "since v18") | Use the user-stated window |
| A specific version number | Match against that version only |
| No time scope | Default to last 12 months |

**Step 2: Assign score based on how the source falls relative to the window.**

| Condition | Score |
|---|---|
| Source was published or last-updated WITHIN the reference window, AND explicitly covers the version/timeline asked | 2 |
| Source was published or last-updated within the reference window, but does not explicitly mention dates or versions | 1 |
| Source date is UNKNOWN but the content appears current (e.g. mentions a recent feature, links to up-to-date references) | 1 |
| Source was published or last-updated 12-24 months outside the reference window, but no evidence it has been superseded | 1 |
| Source is clearly OUTSIDE the reference window by > 24 months | 0 |
| Source has been explicitly SUPERSEDED by a later official announcement, release, or deprecation notice | 0 |

For version-specific questions, apply this version-based override:
| Condition | Score |
|---|---|
| Source explicitly documents or references the target version | 2 |
| Source covers a nearby version (± 1 major) with the same API surface | 1 |
| Source covers a version known to have breaking changes relative to the target | 0 |

---

### 5. relevance — does the content directly address the claim

Quantified by evidence proximity: how many inference steps are needed to connect source content to the claim.

| Condition | Score |
|---|---|
| Source contains a direct, explicit statement that confirms or refutes the claim — zero inference steps needed | 2 |
| Source covers the general topic and allows ONE logical inference step to reach the claim (e.g. it lists a supported feature set, and the user's feature is clearly inside/outside it) | 1 |
| Source only mentions the topic tangentially, or requires TWO OR MORE inference steps to connect to the claim | 0 |
| Source is about a different subject entirely | 0 |

---

### 6. primacy — how close is this to the original information

This dimension punishes mirroring. Two pages repeating the same official announcement should not both score high.

| Condition | Score |
|---|---|
| This IS the original source: the official announcement, the original research paper, the first-hand documentation, the actual release note, the commit itself | 2 |
| This is a SECONDARY source that retells or analyzes the original, but ADDS meaningful original context (e.g. new benchmark data, a comparison the original didn't do, an implementation walkthrough) | 1 |
| This is a TERTIARY or DERIVATIVE source: a pure repost, a summary without added insight, a "news roundup", or a mirrored press release | 0 |
| This is a community discussion that merely links to or quotes the primary source without adding verified new information | 0 |

---

### Minimum Rules

- Do not use a source with total score below **5** (out of 12) as key evidence
- Every important claim must have at least one source with **both** `authority >= 1` AND `relevance >= 1`
- Every core conclusion must be anchored to at least one source with `primacy = 2` whenever possible
- If a claim's best source has `primacy = 0`, explicitly flag this as a "derivative only" evidence gap
- Must report the 6-dimension score breakdown for any source used as key evidence in the Sources section (e.g. `A:2 S:2 A:2 F:1 R:2 P:2 = 11/12`)

### Scoring Shortcuts (for fast triage)

Before doing the full 6-dimension score, apply these instant-reject / instant-accept shortcuts:

| Shortcut | Action |
|---|---|
| Source is a social media post (Twitter/X, Reddit, HN) AND is not from a verified project maintainer account | Auto-score authority=0, stability=0; proceed with remaining 4 dims only |
| Source is a content farm, SEO spam, or AI-generated slop | Reject immediately; do not score |
| Source is the official GitHub release page of the EXACT project the user asked about | Auto-score authority=2, stability=2, primacy=2; score remaining 3 dims fresh |
| Source is a community forum (StackOverflow, Reddit thread) with an accepted answer from a recognized maintainer | Score normally; authority may be 1 for the maintainer's answer

## Evidence Extraction

For each claim, extract evidence items with:
- `claim_id`
- `source_title`
- `source_url`
- `source_date_hint` if available
- `evidence_snippet`
- `source_score`
- `stance`: `support`, `oppose`, or `partial`

Do not over-quote. Extract only the part needed to support the claim.

## Conflict Handling

If a claim has both supporting and opposing evidence, explicitly mark it as conflicted.

Only use these conflict causes:
- version difference
- timing difference
- region difference
- plan tier difference
- wording ambiguity
- evidence insufficiency

Do not invent a conflict explanation without support.

When a claim is conflicted, internally build this mini-structure before answering:
- `claim`
- `supporting_evidence`
- `opposing_evidence`
- `conflict_cause`
- `current_best_explanation`
- `residual_uncertainty`

## Confidence Rules

Assign confidence per key claim:

### High
- at least 2 supporting sources
- at least 1 strong primary source
- no major unresolved conflict

### Medium
- at least 1 reasonably strong source
- some scope limitation or minor conflict

### Low
- only weak support
- or unresolved conflict
- or no clear primary source

## Evidence Map

Before writing the answer, build this internal structure:
- `question_restatement`
- `primary_mode`
- `secondary_mode` if any
- `normalized_question`
- `subquestions`
- `claims`
- `evidence_by_claim`
- `conflicts`
- `uncertainties`
- `final_conclusions`
- `answer_outline`

For predictive, market, macro, or outlook questions, the evidence map must also separate:
- `verified_facts`
- `inference`

Do not skip this step.

## Final Answer Format

Default section order:
1. `Question Restatement`
2. `Short Answer`
3. `Key Findings`
4. `Cross-Source Notes`
5. `Uncertainties or Limits`
6. `Sources`

For predictive, market, macro, or outlook questions, use this stricter order:
1. `Question Restatement`
2. `Short Answer`
3. `Verified Facts`
4. `Inference`
5. `Cross-Source Notes`
6. `Uncertainties or Limits`
7. `Sources`

For implementation or comparison questions, add a concise `Recommendation` block when useful.

## Writing Rules

In `Short Answer`:
- answer directly
- keep it concise

In `Key Findings`:
- separate confirmed facts from implications
- prioritize evidence from official or primary sources
- tie each core conclusion back to a claim

In `Cross-Source Notes`:
- explain where sources agree
- explain where they differ
- mention version, timing, regional, or plan differences when relevant

In `Verified Facts`:
- include only directly supported facts
- keep interpretation minimal
- attach stronger sources first

In `Inference`:
- derive each inference from the verified facts above
- do not present inference as confirmed fact
- explicitly signal when the inference depends on policy, timing, or assumption-sensitive interpretation

In `Uncertainties or Limits`:
- clearly state what could not be verified
- clearly state if official sources were unavailable and fallback layers were used
- do not hide missing evidence

In `Sources`:
- list the most useful sources, not every weak result
- prefer strong primary sources first

## Fast Path

Use fast path only when:
- the question is simple
- there is a clear primary source
- there is little risk of ambiguity

Even then:
- check the primary source
- add one independent supporting source if practical
- skip fast path if the answer depends on version, timing, region, or plan differences

## Example Handling Pattern

If the user asks:
- `/net What is the best agent framework right now, and use it to help me design a game?`

Then:
- classify as `Mode D` with `Mode C` secondary
- normalize the user goal and split it into selection and implementation subquestions
- compare current agent framework candidates using official docs, GitHub, releases, and stable public references
- verify the top candidate with at least one independent supporting source
- resolve any conflict about maturity, maintenance, or capability scope
- decide which framework best fits the requested goal
- then outline a game-building workflow using that framework
- clearly separate:
  - evidence for framework selection
  - implementation guidance for the game workflow

## Final Reminder

Research first.
Model the question second.
Resolve conflicts third.
Answer last.
