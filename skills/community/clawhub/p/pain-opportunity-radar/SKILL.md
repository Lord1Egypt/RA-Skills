---
name: pain-opportunity-radar
description: "Systematically discover, verify, score, and validate high-frequency user pain points that could become Agent, Skill, or human-in-the-loop workflows. Use when researching product opportunities from forums, GitHub Issues, skill marketplaces, reviews, public tasks, or multilingual user expressions; when comparing opportunity lanes; or when moving from broad scanning into real-task validation."
description_zh: "高频痛点与Agent机会雷达"
description_en: "Pain and agent opportunity radar"
agent_created: true
version: "1.0.0"
---

# Pain opportunity radar

## When to use

Use this skill when the user wants to:

- Discover recurring pain points or unmet workflow needs.
- Evaluate Agent, Skill, automation, or human-in-the-loop opportunities.
- Research public expressions across forums, GitHub, X, Reddit, HN, reviews, marketplaces, or multiple languages.
- Compare business, personal, content, learning, life-admin, or cross-border opportunities.
- Move from idea collection to evidence-backed opportunity ranking.
- Design the next-stage user interview or real-task validation plan.

Do not use it for a single known feature with already-confirmed requirements.

## Architecture

Default to a fixed research workflow. Use an Agent only for open-ended source discovery where the next source depends on earlier findings. Keep scoring, evidence fields, thresholds, and output schemas deterministic.

## Workflow

### Step 1: [LLM] Reframe domains into task structures

Start with recurring task archetypes rather than the user's initial list of domains:

1. Capture and normalize information.
2. Reconcile fields, facts, versions, or eligibility.
3. Track cases, approvals, commitments, and deadlines.
4. Monitor exceptions and escalate.
5. Prepare drafts, previews, or submissions.
6. Preserve evidence, audit trails, and decision rationale.
7. Turn confirmed human corrections into reusable rules.
8. Require human confirmation before high-consequence actions.

Build a lane map across professional, business, creative, cross-border, personal, family, learning, and community contexts. Treat the user's suggested lanes as seeds, not boundaries.

### Step 2: [Deterministic] Define an evidence record

Every evidence item must contain:

- Source, URL, date, language, and collection method.
- User role and trigger event.
- Specific job to be done.
- Direct quote or faithful page-visible summary.
- Time, money, error, delay, anxiety, or opportunity cost.
- Current tools and workaround.
- Frequency signal.
- Payment or commitment signal.
- Agent-suitable steps.
- Mandatory human checkpoints.
- Evidence limitation and confidence grade.

Unknown fields stay empty. Never infer willingness to pay from engagement alone.

### Step 3: [LLM] Build multilingual query grids

For each lane, combine role, trigger, task, current tool, and pain language.

Useful pain patterns include:

- Repetition: every day, every week, every time, manual, copy-paste.
- Loss: hours, missed, delayed, error-prone, expensive, rejected.
- Workaround: spreadsheet, Notion, script, virtual assistant, consultant.
- Search for help: is there a tool, how do you manage, wish there was.
- Supply failure: unreliable, hallucinated, broke after update, still needs review.

Use Chinese and English by default. Add the relevant local language for cross-border research.

### Step 4: [Deterministic] Collect source-backed samples

Prefer first-party user expressions and public issue trackers:

1. Forum posts and comments.
2. GitHub Issues, Discussions, and roadmaps.
3. App, browser-extension, SaaS, and marketplace reviews.
4. Public freelance or service tasks showing spend.
5. Skill and Agent marketplaces for supply density.
6. Official reports only for scale or institutional validation.

Preserve source URLs. Search snippets are leads, not evidence. If a source cannot be opened, label it as an unverified lead and exclude it from scoring.

### Step 5: [LLM] Cluster by task identity

Merge evidence only when the same kind of user faces the same trigger and must complete the same job. Shared emotion or shared product names are insufficient.

For every cluster, search for counter-evidence:

- A current tool already solves the core task.
- The product or policy recently changed.
- The signal comes from a vocal minority.
- The task is infrequent or low-cost.
- The workflow depends on inaccessible data or unstable interfaces.

### Step 6: [Deterministic] Score value and confidence

Base score, 100 points:

- User value: 45.
- Agent fit: 35.
- Opportunity quality: 20.

Subtract up to 30 points for high-consequence decisions, irreversible actions, sensitive data, fragile sources, or weak workflow value.

Apply two multipliers:

- Evidence factor: A 1.00, B 0.85, C 0.70, D 0.55.
- Supply factor: white space 1.00, moderate 0.92, crowded 0.82, saturated 0.72.

Keep market value separate from launch fit. Launch fit also considers user access, buildability, integrations, personal expertise, and distribution.

### Step 7: [LLM] Choose the implementation shape

- Use a Skill for one clear transformation with stable inputs and outputs.
- Use a fixed workflow for ordered steps, tool calls, checkpoints, and repeatability.
- Use an Agent only when the path and subtask decomposition genuinely vary.
- Use a partner-led solution when domain liability or enterprise integration dominates.

Start with the smallest useful unit. Generic summarizers, translators, content generators, and trackers require a deeper evidence, exception, or accountability layer to justify a new product.

### Step 8: [LLM] Build a portfolio

Place opportunities into four groups:

- Prototype now.
- Problem interviews.
- Partner or expert validation.
- Observe or stop.

A high pain score can still be a poor first product when distribution, liability, integrations, or incumbent density are unfavorable.

### Step 9: [Deterministic] Enter real-task validation

For each prototype:

- Recruit five target users.
- Require at least three recent real tasks per user.
- Collect redacted artifacts, current steps, baseline time, errors, and spend.
- Start in shadow mode before allowing external side effects.
- Record completion rate, time saved, human edits, failures, second-task commitment, and paid-pilot signal.

Interview questions must focus on the most recent actual task. Hypothetical interest is not evidence.

## Hard rules

1. Every substantive finding must link to a traceable source.
2. Search snippets and vendor claims do not become primary user evidence.
3. Do not treat supply as demand. Existing skills prove capability or competition only.
4. Do not treat downloads, likes, comments, or stars as willingness to pay.
5. Preserve evidence limitations in the final ranking.
6. Never let a single vivid story outrank a multi-source cluster without a confidence penalty.
7. Medical, legal, financial, identity, payment, publication, deletion, and contractual actions require explicit human control.
8. Do not automate final professional judgment. Limit the workflow to materials, evidence, drafts, state, and escalation.
9. Distinguish internal productivity value from external commercial opportunity.
10. Stop expanding lanes after the priority portfolio is stable; move to real-task validation.
11. Published articles may be revised when the user accepts it, but any change to a paper, academic citation, legal judgment, or other research source must be explicitly labeled as a correction, paraphrase, translation, or editorial adaptation. Never silently alter a paper’s content or present a paraphrase as a quotation.

## Pitfalls

- Do not infer that a local file is unpublished merely because it sits in a folder named `drafts`. The user’s confirmed release status, a CMS record, or a publication log is authoritative. Treat a published local source as the audit baseline and record the filename as storage metadata only.
- A prior fact-check report is a regression oracle, not proof that the current version is clean. Compare every historical P0/P1 item with the current published text.
- Separate event existence from causal attribution. A reported outage may be real while the claimed model behavior, permission path, or root cause remains disputed.
- Regulatory materials define jurisdiction-specific requirements. Do not compress them into universal prohibitions without checking the governing text.

## Failure handling

| Scenario | Action |
|---|---|
| API or network call fails | Retry once, then cross-check with another method before concluding unavailable |
| Source is blocked | Preserve the lead, exclude it from scored evidence, and use another source class |
| Search returns mostly vendor content | Use it only for supply mapping; continue to user comments, reviews, or issues |
| One platform dominates the sample | Apply a confidence penalty and create a source-specific补证 plan |
| Marketplace search has zero results | Record the exact query and search a second marketplace before calling it a gap |
| High-value direction has high liability | Route to partner/expert validation and narrow the prototype to low-risk evidence work |
| Users cannot show recent artifacts | Exclude them from validation and recruit task owners |

## Verification

Before delivery, verify:

- The evidence file opens and every scored cluster has traceable URLs.
- Sample counts and platform counts are computed from the saved data.
- Opportunity scores match the published formula.
- Supply density is supported by marketplace searches or a clearly labeled estimate.
- The top opportunities include counter-evidence and risk boundaries.
- The validation plan includes real artifacts, human checkpoints, pass thresholds, and stop conditions.
- The report states important source bias and failed-source evidence.

## Output format

Deliver these artifacts when the task is comprehensive:

1. Lane map CSV.
2. Evidence CSV.
3. Opportunity scorecard CSV.
4. Decision report with opportunity portfolio.
5. Real-task validation plan.
6. Interview and experiment logging template.

Lead with the decision, then evidence, boundaries, and next-stage actions.
