## Description:

Uses AISA to call Perplexity Sonar models and produce cited deep-research answers for synthesis, comparison, and long-form research tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent users use this skill when they need a researched answer with citations rather than a raw list of links. It is suited to broad research questions, comparative analysis, and cited summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can perform broader search and extraction workflows than the Perplexity-only description discloses.

Mitigation: Review the available commands before use and restrict use to the workflows that match the intended research task.

Risk: Research queries and supplied URLs may be sent to AISA-backed services.

Mitigation: Do not use the skill with local credentials, private secrets, or sensitive information unless that disclosure is acceptable.

Risk: The skill requires an AISA API key.

Mitigation: Provide the key through the AISA_API_KEY environment variable and manage it according to the deployment environment's secret-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/perplexity-research-zh)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)
- [AISA service](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with cited research answers and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; research queries and supplied URLs may be sent to AISA-backed services.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
