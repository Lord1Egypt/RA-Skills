## Description:

Podcast Digest helps agents turn podcast audio, transcripts, titles, links, or pasted content into structured podcast notes, analytic summaries, Mermaid diagrams, web reports, slide decks, knowledge cards, and cross-episode research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackgoldenticked](https://clawhub.ai/user/blackgoldenticked)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze single podcast episodes or compare multiple episodes for learning, sharing, and research. It is oriented toward Chinese-language podcast digestion and produces structured notes, diagrams, visual reports, and study assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports or Web PPT decks can include untrusted podcast-derived text.

Mitigation: Treat generated HTML as untrusted and escape or sanitize podcast-derived fields before publishing on authenticated or shared websites.

Risk: Podcast summaries and cross-episode analyses may misstate speaker positions if source audio or transcripts are incomplete.

Mitigation: Prefer complete transcripts when available and review speaker attribution, quotes, and timestamps before sharing the output.

## Reference(s):

- [Podcast Digest skill page](https://clawhub.ai/blackgoldenticked/skills/podcast-digest)
- [Mermaid podcast visualization templates](references/mermaid-templates.md)
- [Multi-episode podcast research schema](references/multi-episode-schema.md)
- [Web report template specification](references/web-report-template.md.md)
- [Web PPT template specification](references/webppt-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese-language Markdown notes, Mermaid diagrams, and HTML web reports or slide decks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-episode deep analysis and multi-episode comparative research.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
