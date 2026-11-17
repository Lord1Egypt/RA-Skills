## Description:

知识卡片 helps an agent analyze a single concept in Chinese and produce an Obsidian-ready Markdown knowledge card using a five-dimension framework or a folk-concept framing method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to turn a single concept or term into a structured Chinese Obsidian knowledge card with frontmatter, wikilinks, plain-language explanation, practical application notes, and optional file output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad concept-analysis requests may route into this skill even when the user expected a shorter answer.

Mitigation: Use the skill for single-concept knowledge-card requests and confirm scope when the request includes multiple concepts or unclear intent.

Risk: The optional --file behavior can create a Markdown file in the current directory.

Mitigation: Use --file only when a local Obsidian-style Markdown file is intended.

Risk: Concept origin, academic lineage, or folk-concept framing may be uncertain for some topics.

Mitigation: Preserve uncertainty in the card and verify claims before using the output as authoritative research.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtoyun/skills/knowledgecards)
- [Publisher profile](https://clawhub.ai/user/xtoyun)
- [XTOCN homepage](https://www.xtocn.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Obsidian Markdown with YAML frontmatter, callouts, wikilinks, and optional Markdown file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports quick, standard, and deep depth modes; optional focus dimension; optional --file output; optional --no-wikilinks mode.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
