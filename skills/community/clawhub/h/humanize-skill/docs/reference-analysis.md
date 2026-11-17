# Reference analysis

This project uses five references, but keeps the final product intentionally small.

## blader/humanizer

What to borrow:

- A concrete catalog of AI-writing tells, organized as a 30-category checklist.
- A draft -> audit -> final loop.
- Optional voice calibration from user samples.
- Plain editorial rules that work inside a skill without a separate app.

What to change:

- Add provenance and fact-checking.
- Make real user voice the default aspiration, not only an optional paste-in sample.
- Avoid generic "add personality" when the domain calls for neutral technical prose.

## tinyhumansai/openhuman

What to borrow:

- Local-first memory: user context should be readable and controlled by the user.
- Source adapters: different upstreams can feed the same canonical text pipeline.
- Provenance: every style sample and evidence item should have a source label.
- Periodic sync as a concept, but not as a requirement for this skill.

What to avoid:

- A heavy desktop app, OAuth broker, scheduler, database, or managed integration layer.
- Storing raw private messages when a compact style profile is enough.

Humanize-skill adaptation:

```text
user export / pasted sample
        |
        v
canonical text with source label
        |
        v
style statistics + examples summary
        |
        v
compact voice profile notes
```

The profile can be saved as small, inspectable notes or JSON. It should not contain full account dumps.

## Oumi HallOumi

What to borrow:

- Treat fact checking as a separate pass after generation.
- Break output into claim-like sentences.
- Judge each claim against evidence.
- Return a status, confidence, explanation, and citation.

What to avoid:

- Fine-tuning or requiring HallOumi model inference for ordinary skill use.
- Blocking all use when no evidence source exists.

Humanize-skill adaptation:

```text
rewrite
  |
  v
claim extraction
  |
  +--> style/opinion: no evidence required
  |
  +--> factual claim: compare with evidence files or current sources
             |
             v
       supported / needs_evidence / possibly_wrong
              ^
              |
       external reference search when local evidence is insufficient
```

## Proposed architecture

The open-source project has four small layers:

1. `SKILL.md`: the agent-facing workflow and completion contract.
2. `docs/`: reference notes and source-ingestion guidance.
3. `examples/`: real agent runs with draft, sample, evidence, notes, and final output.
4. `assets/`: README visual assets.

There is no CLI layer. The host model performs the semantic rewrite, while the skill supplies the process, guardrails, and artifact shape.

## Core feature contract

The project should keep all documentation, examples, and future implementation notes aligned to one reader-strategy layer plus five rewrite promises.

The reader-strategy layer is:

0. **Audience and cognition mapping**: identify the target reader, their cognitive starting point, the new cognition the piece can add, and the author persona that best carries the text without inventing biography.

The five rewrite promises are:

1. **Quality-first humanization**: the main workflow improves clarity, specificity, credibility, and voice. It does not promise detector results.
2. **Deep voice matching**: samples should inform both surface style and deeper writer behavior — stance, ordering, repair, perspective, hedging, domain vocabulary, and signature tells.
3. **Five-layer AI-pattern diagnosis**: the diagnostic model covers lexical, phrasal, syntactic, structural, and cognitive layers. The cognitive layer matters as much as the visible hype-word layer.
4. **Specificity and reasoning pass**: generic claims should be replaced by real details and visible reasoning when the user supplies the basis. The skill should never invent specifics to sound human.
5. **Fact-aware rewriting**: factual claims should be supported, weakened, marked, or removed, with stronger evidence requirements for product, research, health, technical, legal, financial, and public-facing text.

These are not only marketing bullets. They are the completion contract for a successful run. Audience/cognition mapping should happen before the rewrite when reader fit matters; it should stay implicit for tiny edits and transactional replies.

## Positioning contract

The project should present itself as a quality-first, agent-native editorial skill:

- **Agent-native**: the host model performs semantic rewriting; the repository supplies instructions, reference docs, examples, and visual explanation.
- **Quality-first**: success is measured by reader fit, cognitive value, clarity, specificity, voice fidelity, factual grounding, and reviewability, not by detector scores.
- **User-controlled**: real voice and facts come from pasted text, local files, exports, or explicitly authorized connectors.
- **Evidence-aware**: specific factual claims must have support, a downgraded confidence level, a note, or removal.
- **Small and portable**: no training pipeline, background service, required OAuth broker, or mandatory CLI layer.

Future README images, examples, and release notes should foreground the reader-strategy layer and the five rewrite promises above. Avoid visuals or copy that make the project look like a generic "AI detector bypass" product, a regex cleaner, or a full SaaS platform.

## Source ingestion policy

Accept only user-controlled data:

- pasted text
- local files
- exports from social/chat/email tools
- connector output explicitly requested by the user

Default behavior:

- read the minimum needed
- summarize into profile metrics
- keep provenance labels
- do not print private source text in final output

## Fact-check policy

Lightweight by default, but with enough structure to leave a clean audit trail. The full method is in [docs/fact-check.md](./fact-check.md): claim taxonomy, source hierarchy, time and staleness, conflict protocol, fix matrix, tool unavailability, AI's specific factual failure modes, and the recommended `evidence.md` shape.

Short form:

- For low-risk drafts, flag unsupported specifics and avoid overclaiming.
- For unsupported, high-risk, or current facts, verify with external references instead of relying on model memory.
- Prefer primary, official, or scholarly sources over generic snippets. Treat the source tier as part of the citation: a peer-reviewed paper, a primary filing, an official changelog, a major-newspaper report, and an SEO blog are not equivalent.
- Watch for staleness. A 2019 statistic is rarely a 2026 fact. Re-date or remove.
- For missing or weak evidence, label precisely (`supported`, `weak_support`, `unverified`, `contested`, `stale`, `wrong`, `style_only`) and apply the fix matrix. The coarse `needs_evidence` label is the public API; the depth split is for the rewrite.
- If web/search tools are unavailable, all claims default to `unverified` and the final output states the limitation explicitly.
- When sources disagree, follow a protocol: higher tier wins, then newer, then primary, then less motivated. If still unresolved, name the tension rather than picking a side.

The skill should never make factual claims more specific during humanization unless those specifics come from the user's draft or cited evidence. Personal experience in the user's draft is theirs; numerical, attributed, identity, and schedule claims still need checking.

## Wikipedia: Signs of AI writing

This is the primary lexical and phrasal reference for the AI-pattern catalog in `docs/anti-ai-patterns.md`. It is maintained by WikiProject AI Cleanup as a community-edited catalog of words, phrases, and structural habits that mark LLM-generated text in Wikipedia and similar surfaces. The Wikipedia page is the authoritative substrate: when the local catalog and the Wikipedia list disagree, the Wikipedia entry wins for the underlying category, the local section wins for the rewrite. The catalog in `docs/anti-ai-patterns.md` opens with a "Wikipedia catalog index" that maps each local section to its Wikipedia anchor, so the two can be cross-checked section by section.

What to borrow:

- A community-maintained, regularly-updated list of specific tells.
- The em-dash overuse, significance inflation, vague attribution, and chatbot residue clusters as canonical categories.
- The "rule of three" structural pattern (paragraphs opening with the same grammatical role, three-clause parallelism, three-item lists).
- The canonical *labels* themselves as the public-facing vocabulary of the catalog. A user searching for "rule of three" or "significance inflation" should find this skill's entry through the same terms, not a renamed synonym.

What to change:

- Treat the Wikipedia list as the *lexical and phrasal substrate*, not as the whole catalog. The structural layer (heading cadence, bullet-list overuse, intro-body-summary sandwich) and the cognitive layer (uniform confidence, no stated limits, hidden reasoning, generic examples) are added by `humanize-skill` because the Wikipedia list does not cover them, and they are the patterns detector-style tools pick up most.
- Apply the "rewrite, don't delete" principle from `blader/humanizer` to each Wikipedia pattern: removing the matched phrase without rewriting the surrounding sentence leaves a formula fragment.
- Match the user's voice profile before applying any pattern removal. The Wikipedia list describes a generic AI default. A user with a stable em-dash habit, a personal use of "delve", or a signature that includes "tirelessly" is not the Wikipedia target. The voice profile is the override.
- Do not import the Wikipedia list as a hard rules engine. The list is a diagnostic aid. The final rewrite is editorial judgment.

The catalog in `docs/anti-ai-patterns.md` is layered on this source, plus `blader/humanizer`'s curation, plus the structural and cognitive layers this skill adds.

## lynote-ai/humanize-text

This is a 1.1k-star open-source tool whose stated purpose is "Bypass Turnitin, GPTZero, and all major AI detectors". The README documents four humanization methodologies (translation chain, multi-turn LLM rewriting, detection-guided feedback loop, mixed-engine translation) and a "Standard Pipeline" integration that combines the first two.

What to borrow:

- The translation-chain concept: routing text through distant languages (EN → 中文 → 日本語 → Suomi → EN) as a way to disrupt structural fingerprints. The technique is well-known and worth describing honestly, because a user who has chosen the alternative path benefits from seeing the methods documented rather than reinvented.
- The Standard Pipeline as a documented integration: two LLM rewrites (carrying history) plus two cross-engine translation hops. It is the canonical "best of both" combination in the detection-evasion literature.

What to change:

- **Do not import the pipeline into the default workflow.** The default workflow is a quality-direction pipeline. The translation chain, the detection-guided feedback loop, and the mixed-engine pipeline all serve a different purpose: lowering detector-classification scores. Importing them silently would change the skill's purpose and break the boundary in `SKILL.md` Non-goals and `README.md` Boundary.
- **Document the methods as an alternative, not as a default.** The user who wants this material opts in by reading [docs/detection-aware-methods.md](./detection-aware-methods.md). The user who does not want it should not see it in their default workflow. The two methodologies are not interchangeable.
- **Do not borrow the evaluation metric.** lynote-ai measures success by AI-detector confidence (e.g. "0.9997 human"). The skill's evaluation is by writing-quality dimensions, not by detector scores. Borrowing the metric would invert the skill's success criteria.
- **Do not borrow the marketing framing.** "Bypass" is the framing in lynote-ai. The skill frames the alternative as "detection-aware methods" because that is more honest about what the methods do, and because "bypass" is a word the skill's main workflow refuses to use.
- **Do not borrow the empirical claims as load-bearing.** "100% key information retention" and "9.1/10 expert quality score" are self-reported metrics from a project with a different purpose. They are not a substitute for this skill's quality direction. The appendix describes the methods, not the marketing claims.

The relationship to this skill is documented in [docs/detection-aware-methods.md](./detection-aware-methods.md), in particular the sections "Why this appendix exists" and "How this appendix relates to the main workflow".
