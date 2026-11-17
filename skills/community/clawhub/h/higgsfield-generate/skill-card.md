## Description:

Generate images and videos with Higgsfield AI models, including generic image/video generation and Marketing Studio workflows for branded ad images and videos with avatars and products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[higgsfield](https://clawhub.ai/user/higgsfield)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and developers use this skill to ask an agent to select Higgsfield models, prepare CLI commands, submit image or video generation jobs, and return the generated media URL with a brief summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send prompts, media files, product URLs, and related assets to Higgsfield.

Mitigation: Use only with content the user is comfortable sharing with Higgsfield, and avoid sensitive or restricted assets unless the user has explicitly approved that use.

Risk: The skill instructs the agent to install the Higgsfield CLI with an unverified remote installer script.

Mitigation: Do not run the remote installer automatically; install the CLI through a pinned, trusted, inspectable process before using the skill.

Risk: The skill requires Higgsfield account authentication before jobs can be submitted.

Mitigation: Have the user authenticate intentionally with `higgsfield auth login` and confirm completion before the agent continues.

## Reference(s):

- [Model Catalog](references/model-catalog.md)
- [Media Inputs](references/media-inputs.md)
- [Marketing Studio Modes](references/marketing-modes.md)
- [Marketing Studio Avatars](references/marketing-avatars.md)
- [Marketing Studio Products](references/marketing-products.md)
- [Prompt Engineering](references/prompt-engineering.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/higgsfield/skills/higgsfield-generate)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown text with inline shell commands and generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the Higgsfield CLI to submit generation jobs and return result URLs after waiting for completion.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
