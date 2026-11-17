## Description:

音乐 is a CellCog-oriented AI music generation skill for creating original instrumental and vocal music from 5 seconds to 10 minutes for creative and automated workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and automation teams can use this skill to draft AI-assisted music generation requests for short clips or longer original instrumental and vocal works. The artifact states it is not suitable for processing copyrighted media content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks for broad shell execution and file access authority that is not well scoped to the documented music-generation workflow.

Mitigation: Review before installing; prefer or require a version that removes exec or documents exact allowed commands, inputs, outputs, and API endpoints.

Risk: The artifact includes API key setup guidance, which can expose credentials if users paste secrets into logs, prompts, or version-controlled files.

Mitigation: Use environment variables or a secret manager, avoid hardcoding keys, and review logs and generated files for accidental credential disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/music-gen-cellcog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include music prompt text, generation parameters, setup guidance, processing status, and metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
