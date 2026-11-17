## Description:

Generates Phase A research notes for KokoChat Deeply courses by using KokoChat-hosted search and web fetch to collect real sources, narrate the research in Chinese, and emit a `koko.deeply.research.notes` block for Phase B course outlining.

This skill is ready for commercial/non-commercial use.

## Publisher:

[komako-workshop](https://clawhub.ai/user/komako-workshop)

### License/Terms of Use:

MIT-0

## Use Case:

KokoChat Deeply users use this skill to turn a course topic into researched notes with real sources. Developers can use it as the research pass in a two-phase pipeline where a later inference converts the notes into a course outline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and derived keywords may be visible to KokoChat-hosted search, its upstream search provider, and fetched websites.

Mitigation: Avoid confidential names, unreleased projects, secrets, or private document excerpts unless the surrounding KokoChat deployment provides appropriate privacy controls.

Risk: Search or fetch failures can leave the research notes incomplete, and invented sources would mislead the downstream course outline.

Mitigation: Use only URLs returned by successful hosted search or web fetch results, and state failures or gaps honestly in the research narration.

## Reference(s):

- [KokoChat Deeply Research on ClawHub](https://clawhub.ai/komako-workshop/skills/kokochat-deeply-research)
- [KokoChat hosted search endpoint](https://deeply.plus/deeply/search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Chinese prose followed by one fenced koko.deeply.research.notes JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The notes block contains a topic, synthesis, and flat source list; source URLs must come from hosted search or web fetch results.]

## Skill Version(s):

0.5.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
