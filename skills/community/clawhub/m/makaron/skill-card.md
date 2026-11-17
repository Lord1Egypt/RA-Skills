## Description:

Use Makaron CLI to generate AI images, videos, music, and motion designs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vegekyd-sys](https://clawhub.ai/user/vegekyd-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to invoke Makaron CLI for creative media production, including image generation and editing, video creation and editing, music composition, and animated design workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an external npm-resolved CLI that can change after review while handling Makaron credentials and user media.

Mitigation: Pin and review the makaron-cli version in a locked environment before use.

Risk: Makaron API keys and provided media may be accessible to the CLI and project workspace used by the agent.

Mitigation: Use narrowly scoped credentials and isolated project directories, and provide only media intended for Makaron processing.

## Reference(s):

- [Makaron App](https://makaron.app)
- [Makaron agent registration discovery endpoint](https://www.makaron.app/api/agent/register)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create projects, upload media, poll run status, and extract generated media URLs from Makaron CLI responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
