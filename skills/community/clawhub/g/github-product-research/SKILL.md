---
name: github-product-research
description: Research GitHub repositories as products rather than merely finding code. Use when Codex needs to discover open-source products, map a market, compare competitors, validate a product idea, analyze repository and issue signals, identify underserved demand or abandoned-but-wanted projects, and recommend product opportunities for product managers or indie builders. Supports Chinese and English requests with bilingual search expansion.
---

# GitHub Product Research

Turn GitHub repository evidence into product decisions. Find relevant products, compare their positioning and capabilities, examine demand and maintenance signals, identify gaps, and recommend credible opportunities.

## Set the Language

Detect the user's language and respond in that language by default.

- For a Chinese request, understand the request in Chinese, search with Chinese and English concepts, and report in natural Chinese.
- For an English request, search broadly and report in English.
- For an explicitly bilingual request, provide a complete Chinese report first and a complete English report second. Do not translate line by line.
- Preserve repository names, URLs, technical terms, and official product names in their original form.
- Avoid unnecessary mixing of Chinese and English.

## Define the Research Question

Convert the request into a decision-oriented brief:

1. State the product category, target user, use case, and constraints.
2. Identify the decision the research should support, such as entering a market, selecting a tool, validating an idea, or choosing a differentiated feature.
3. Clarify only when a missing constraint would materially change the research. Otherwise, state reasonable assumptions and proceed.
4. Define comparison dimensions before collecting candidates. Typical dimensions include target user, deployment model, core workflow, integrations, pricing or monetization, license, activity, adoption, and unmet demand.

## Expand Search Concepts Bilingually

Do not translate only word for word. Generate concept clusters containing:

- category names and synonyms;
- user problems and desired outcomes;
- technical implementation terms;
- adjacent categories and alternative solutions;
- common README, topic, and issue vocabulary.

For example, expand `AI 成本监控` into concepts such as `大模型用量监控`, `LLM cost monitoring`, `AI spend management`, `token usage dashboard`, `OpenAI cost tracker`, and `LLM observability`.

Use qualifiers when useful: language, stars, license, archived status, creation or update date, relevant GitHub topics, and keywords found in README files or issues. Treat stars as one signal, never as proof of product quality or demand.

## Execute a Search Plan

Cover at least three query families unless the request is narrowly scoped:

1. **Category queries:** product-category names, synonyms, GitHub topics, and common README phrases.
2. **Problem queries:** user pain, desired outcome, workaround, feature request, and migration language.
3. **Alternative queries:** adjacent categories, substitutes, commercial alternatives, and abandoned projects.

Search repositories and repository content first. Search issues and discussions whenever the request concerns demand, gaps, complaints, missing features, or abandoned projects.

Build a broad initial pool before ranking candidates. For a normal market scan, aim for 10–20 plausible repositories and inspect 5–8 serious candidates in depth. Treat these as defaults, not quotas; use fewer for a narrow category and more when the market is fragmented.

Stop expanding the search when two consecutive query variations add no materially new product type, competitor, user problem, or evidence pattern. Also stop when additional results are mostly duplicates, forks, templates, or irrelevant libraries. State when tool, access, or time constraints force an earlier stop.

## Gather Evidence

Prefer the connected GitHub app or GitHub API/CLI when available. Use web search as a fallback or to inspect public product documentation. Prefer primary sources:

- repository metadata, README, releases, commit history, contributors, license, and topics;
- open and closed issues, discussions, feature requests, bug reports, and maintainer responses;
- official documentation, demos, pricing, and project websites.

Inspect enough of each serious candidate to distinguish a product from a library, template, example, inactive experiment, or renamed fork. Deduplicate forks and mirrors unless their divergence is relevant.

Record the observation date for time-sensitive metrics. Keep links to the exact supporting sources.

### Degrade gracefully under access limits

Do not stop the report when GitHub API rate limits, inaccessible discussions, truncated search results, or web restrictions prevent full collection. Use three modes:

1. **Full mode:** inspect repository metadata, README, releases, meaningful commits, contributors, issues, discussions, pull requests, official product pages, commercial editions, successors, alternatives, and active forks.
2. **Limited mode:** prioritize the core repository list and positioning; archive or migration notices; latest release and meaningful commit; license; maintainer responsiveness; representative high-signal issues and pull requests; official commercial versions, successor projects, and active forks.
3. **Minimum viable mode:** return only verified core repositories and evidence that was actually accessible. Identify missing evidence, lower confidence, and avoid definitive gap or abandonment claims.

Do not prioritize historical star trends under constrained access unless a reliable source is already available. Current star counts are snapshots, and reconstructing trends may require costly or third-party data. Never substitute missing data with guesses.

## Build the Candidate Set

Use a funnel:

1. Gather a broad candidate pool.
2. Remove irrelevant, duplicate, deceptive, or insufficiently documented repositories.
3. Select a defensible comparison set based on the research question, not stars alone.
4. Explain inclusion and exclusion criteria.
5. Call out important commercial or closed-source alternatives only when they materially shape the open-source market, and label them clearly.

## Analyze Product Signals

Separate observed facts from interpretation.

Use a consistent qualitative rubric:

| Dimension | Strong | Moderate | Weak or unknown |
| --- | --- | --- | --- |
| Demand evidence | Repeated independent requests or behavioral signals | Several related signals with limited independence | Anecdote, inference, or no direct evidence |
| Product completeness | Clear end-to-end workflow used as a product | Useful workflow with notable gaps | Library, demo, template, or unclear product |
| Maintenance | Recent releases plus responsive maintenance | Some recent activity or uneven responsiveness | Stale, archived, or unresponsive |
| Differentiation | Clear underserved wedge | Incremental distinction | Commodity or unclear distinction |
| Commercial potential | Identifiable buyer, urgency, and route to distribution | Plausible user and value with untested willingness | Buyer, urgency, or distribution unclear |
| Evidence confidence | Multiple current primary sources | Limited or partly indirect sources | Sparse, old, or unverified sources |

Apply the rubric comparatively rather than pretending the labels are precise measurements. Explain the strongest reason for each rating.

### Product and adoption signals

Assess:

- clarity of target user and value proposition;
- completeness of the end-to-end workflow;
- installation friction, deployment options, integrations, and documentation;
- release cadence, recent maintenance, contributor concentration, and issue responsiveness;
- stars, forks, watchers, package downloads, community activity, or deployments when available;
- licensing, governance, monetization, and sustainability risks.

Do not compare raw star counts without noting repository age and category context. Do not infer active usage from stars alone.

### Demand signals

Look for repeated user problems in issues and discussions:

- feature requests with independent supporting comments or reactions;
- recurring workarounds, migration requests, and integration needs;
- unresolved pain in active projects;
- continued questions or forks around inactive projects;
- willingness to self-host, pay, migrate, or contribute.

Filter and prioritize before reading long threads:

1. Scan titles, labels, state, creation and update dates, reactions, comment counts, and duplicate links.
2. Prioritize relevant feature requests, enhancement proposals, integration requests, migration discussions, and repeated workflow blockers.
3. Read thread bodies and representative comments only when the item is relevant or contributes to a recurring pattern.
4. Deprioritize isolated installation failures, one-off environment errors, incomplete support requests, empty discussions, spam, bot-only activity, and issues already resolved by documentation.
5. Exclude irrelevant items from demand counts, but retain their number as a noise note when it materially affects confidence.

Use this conceptual weighting:

`signal strength = research relevance × independent users × interaction quality × persistence × unresolved severity`

Apply these rules:

- Treat reactions and comment counts as amplifiers, not standalone proof of demand.
- Give more weight to independent users describing the same job or pain than to repeated comments from one user.
- Merge duplicates and cross-linked issues into one demand cluster; do not inflate counts.
- Prefer comments that add a use case, workaround, switching behavior, urgency, or willingness to pay or contribute over simple `+1` comments.
- Compare feature requests and bugs on relevance and repeated user impact rather than assigning an automatic category winner.
- Quote sparingly and link to representative primary sources.

Do not discard deployment and configuration problems as a category. Promote them from low-value support noise to a product-friction signal when multiple independent users encounter the same obstacle, the problem persists across versions or environments, or users repeatedly request clearer onboarding, better defaults, managed hosting, or automated setup. Report the resulting pattern, not every individual error thread.

When enough dated data is available, compare valid demand clusters across equivalent windows, such as the latest 90 days versus the preceding 90 days. Exclude bots, spam, duplicates, and support noise. Report both the absolute number of valid clusters and the direction of change. Treat growth as suggestive unless the baseline, repository size, and collection coverage are comparable.

Distinguish one anecdote from a repeated pattern. If a conclusion depends mainly on noisy discussions or support requests, lower its evidence-confidence rating.

### Maintenance lifecycle

Classify lifecycle with multiple signals rather than a single cutoff. Inspect:

- latest release and latest meaningful default-branch commit;
- maintainer responses and issue-closing activity;
- pull request merge, review, and closure activity;
- archive or deprecation notice;
- contributor concentration and bus-factor risk;
- recent user comments, repeated unresolved requests, security or dependency problems, active forks, and migration discussions.

Ignore bot-only dependency bumps, formatting-only changes, and trivial documentation fixes when deciding whether development is meaningful.

Use these evidence bands as defaults:

- **Active:** at least two current signals agree, such as meaningful code activity within roughly 90 days, a release within 6 months, recent maintainer response, or recent pull request review or merge activity.
- **Maintenance mode:** few new features but continued security fixes, dependency maintenance, critical bug handling, or an explicit stability statement.
- **Inactive:** no meaningful release or code activity for roughly 6–12 months and clearly declining maintainer responsiveness, without an explicit end-of-life notice.
- **Likely unmaintained:** at least three signals agree, such as no meaningful commit for more than 12 months, no release for more than 12 months, no maintainer response for 6 months, several valid pull requests stalled for 6 months, unresolved critical dependency or security problems, or public requests for a new maintainer.
- **Archived or deprecated:** GitHub or the maintainer explicitly marks the project archived, deprecated, replaced, or end-of-life.

Treat time thresholds as evidence bands, not universal laws. Adjust for the project's historical release cadence, maturity, size, and category. A stable utility may require few commits; a fast-moving integration may become obsolete within months. Never use a fixed open-issue count such as `>100` without normalizing for repository scale and issue throughput.

### Abandoned-but-wanted projects and successor checks

Claim continuing demand only when recent independent evidence exists, such as repeated valid requests, active workarounds, meaningful forks, migration discussions, or willingness to pay or contribute. Otherwise label it a hypothesis.

Before calling an inactive project a market gap, actively check:

- README, organization repositories, releases, and pinned issues for renames, migrations, rewrites, or successor projects;
- official websites and documentation for hosted, Cloud, Pro, Enterprise, or paid editions;
- acquisitions, license changes, open-core transitions, or movement to another code host or ecosystem;
- active forks with meaningful commits, releases, maintainers, users, or differentiated roadmaps;
- established commercial and open-source alternatives serving the same job.

Classify the outcome as one of: `unclaimed gap`, `official migration or rename`, `open-source to commercial transition`, `community fork succession`, or `demand already served by alternatives`.

Treat the classification as context, not an automatic verdict. An open-source-to-commercial transition may leave room for a credible open, local-first, self-hosted, or lower-cost alternative; a community fork may still serve users poorly; and commercial alternatives may validate demand while leaving a segment underserved. Require a specific underserved user, constraint, or workflow before recommending entry.

### Gap and opportunity signals

Identify opportunities only when evidence supports both a user problem and an inadequacy in current solutions. Describe:

- target user and job to be done;
- evidence of demand;
- shortcomings of current alternatives;
- proposed wedge or differentiator;
- likely distribution route and monetization path;
- technical, market, and evidence risks;
- the smallest validation experiment.

Rank opportunities by evidence strength, user value, differentiation, feasibility, and timing. Avoid presenting speculation as a market fact.

End the analysis with one explicit decision:

- **Build:** evidence and differentiation are strong enough to justify immediate validation or MVP work.
- **Differentiate:** demand exists, but entry requires a clear wedge against established solutions.
- **Wait and investigate:** the opportunity is plausible but blocked by weak evidence or a critical unknown.
- **No-go:** demand, differentiation, feasibility, timing, or competitive structure does not justify further investment.

Do not force a positive opportunity. Explain the decisive evidence, counterevidence, and what would change the verdict.

Recommend a product form only when it follows from the workflow, distribution channel, deployment needs, and buyer:

- CLI or SDK for developer-local and automation-heavy workflows;
- browser or IDE extension for in-context repetitive actions;
- GitHub App for repository-native automation;
- self-hosted service for privacy, control, or regulated environments;
- hosted SaaS for collaboration, continuous monitoring, or low-operations adoption;
- desktop app for local data, offline use, or nontechnical workflows;
- integration or plugin when users already live inside an established product.

Explain why the form fits. Do not default to SaaS.

## Produce the Report

Lead with the answer and adapt depth to the request. For a full Chinese report, use:

1. `## 执行摘要`
2. `## 市场概览`
3. `## 重点产品`
4. `## 功能对比`
5. `## 用户需求信号`
6. `## 产品空白与机会`
7. `## 建议行动项`
8. `## 来源与限制`

For a full English report, use:

1. `## Executive Summary`
2. `## Market Landscape`
3. `## Top Products`
4. `## Feature Comparison`
5. `## User Demand Signals`
6. `## Product Gaps and Opportunities`
7. `## Recommended Actions`
8. `## Sources and Limitations`

Use a compact comparison table when evaluating several products. Include repository, positioning, target user, key capabilities, license, activity, adoption signals, and notable limitations when the evidence permits.

For bilingual output, use two complete sections headed `# 中文报告` and `# English Report`.

For each recommended opportunity, provide an opportunity card:

- target user and job to be done;
- observed demand and evidence rating;
- proposed product form and why it fits;
- smallest viable product;
- acquisition or distribution path;
- plausible monetization;
- why now and the most credible defensibility mechanism;
- major risk and counterevidence;
- smallest next validation experiment.

Add a concise SWOT only when the user requests it or it materially clarifies a strategic choice. Do not let a polished recommendation hide weak evidence.

## Maintain Evidence Integrity

- Cite every time-sensitive metric and material factual claim near the claim.
- Label estimates, interpretations, and inferences explicitly.
- State what was searched, when it was observed, and what could not be verified.
- Never fabricate stars, dates, issue counts, pricing, licenses, features, or user demand.
- Treat missing evidence as unknown, not negative evidence.
- Explain selection bias and GitHub's limits: private usage, non-GitHub communities, commercial adoption, and silent users may be invisible.
- Prefer a narrower well-supported conclusion over a broad unsupported market claim.

## Example Requests

Chinese:

- 调研 GitHub 上的开源 AI 成本监控产品。
- 对比几个开源 Prompt 管理平台。
- 从 GitHub Issues 中发现产品机会。
- 寻找仍有用户需求但长期没有维护的开源项目。
- 寻找开源个人知识管理产品的市场空白。

English:

- Research open-source AI cost monitoring products on GitHub.
- Compare open-source prompt management platforms.
- Discover product opportunities from GitHub issues.
- Find abandoned open-source projects that still show user demand.
- Find gaps in the open-source personal knowledge management market.
