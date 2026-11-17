## Description:

Uses the MetaDig CLI to generate images, videos, speech, and music, and manage generation tasks and projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pythonthink](https://clawhub.ai/user/pythonthink)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent can request media generation through MetaDig, including images, video, speech, and music. Developers can also use it to check models and pricing, track jobs, download results, and organize work into projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running online installation scripts whose behavior has not been verified.

Mitigation: Require user approval before installation or upgrades, and prefer a fixed CLI release whose authenticity has been verified.

Risk: Reference media selected for generation is uploaded and receives public URLs.

Mitigation: Avoid confidential inputs and get the user's approval before uploading media.

Risk: Generation consumes account credits, and credentials can grant access to the account.

Mitigation: Confirm credit costs before paid generation and keep access tokens out of conversations.

## Reference(s):

- [MetaDig CLI documentation](https://waytometa.cn/docs/skills/agent-skill)
- [MetaDig CLI](https://waytometa.cn/cli)
- [CLI command guide](references/cli-command-guide.md)
- [Generation guide](references/generation-guide.md)
- [Common pitfalls](references/common-pitfalls.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Generated media files and URLs]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; generated media files or URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media uses the user's MetaDig account credits and may be added to a web canvas project.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
