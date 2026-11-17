## Description:

Analyzes an author's articles to reconstruct thinking patterns and writing style, then generates a reusable style prompt and local writing persona sub-skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, brand teams, and style researchers use this skill to analyze permitted writing samples, create an author-style prompt, and generate a reusable local persona for drafting same-style content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch public-platform content through RedFox and uses a REDFOX_API_KEY.

Mitigation: Use it only with material you own, have permission to analyze, or can lawfully process; confirm the key source, scope, cost, and revocation path before collection.

Risk: The skill reads user-specified local files or folders and creates persistent local author-style skills.

Mitigation: Limit file paths to the intended corpus, review any generated sub-skill before enabling it, and remove or update generated local skills when they are no longer appropriate.

Risk: Author-style cloning can be misleading or inappropriate without consent and review.

Mitigation: Get permission or another lawful basis for style analysis, avoid deceptive impersonation, and review generated writing before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/multi-copywrite-alchemy)
- [Core Workflow](artifact/references/core_workflow.md)
- [Writing Persona Template](artifact/references/persona-template.md)
- [Writing Style and Thinking Framework](artifact/references/7-dimensions-framework.md)
- [Writing Formulas](artifact/references/writing-formulas.md)
- [RedFoxHub API key management](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown deliverable with generated prompt text and local persona skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a style prompt and a persistent local persona sub-skill; platform collection requires REDFOX_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
