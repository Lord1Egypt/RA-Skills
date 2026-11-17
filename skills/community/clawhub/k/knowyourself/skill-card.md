## Description:

Visual identity discovery for AI agents - not an avatar generator, but a self-reflection system that creates a face from an agent's personality, memory, and relationship with its human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahaaiclub](https://clawhub.ai/user/ahaaiclub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an AI agent through quick or full visual identity discovery, producing avatar prompts, candidate images, structured evaluations, and a persistent visual identity file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad memory, personality files, and recent chat context, which can expose personal or project-sensitive details in derived image prompts.

Mitigation: Ask the agent to list the exact files and context it will read, exclude secrets or unrelated details, and show the outbound image prompt for approval before using an image-generation tool.

Risk: The skill saves a persistent visual identity file that may encode traits inferred from private memory or conversation history.

Mitigation: Require approval before creating or updating the identity file, review its contents before persistence, and revise or delete sensitive identity history when needed.

## Reference(s):

- [Evaluation Frameworks Reference](references/evaluation-frameworks.md)
- [Visual Identity File Template](references/identity-template.md)
- [AHA AI](https://ahaai.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables, image-generation prompts, scoring summaries, and identity-file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose image-generation prompts and create or update a long-lived visual-identity.md file after user checkpoints.]

## Skill Version(s):

1.1.2 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
