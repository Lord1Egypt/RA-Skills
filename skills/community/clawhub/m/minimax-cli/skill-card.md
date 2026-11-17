## Description:

MiniMax CLI helps agents use the MiniMax AI platform from the terminal for text, image, video, speech, music, vision, and web search workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylerdotai](https://clawhub.ai/user/tylerdotai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, authenticate, and run mmx-cli commands for MiniMax multimodal generation, web search, quota checks, and direct API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill shows an unpinned global npm installation for mmx-cli.

Mitigation: Prefer a pinned, verified mmx-cli version or a local/project-scoped install, and avoid running npm with elevated privileges.

Risk: The skill shows an API key passed directly on the command line.

Mitigation: Use a safer authentication flow or environment-based secret handling when supported, avoid shared or logged terminal sessions, and check permissions on ~/.mmx/config.json.

Risk: MiniMax usage can affect quota or billing.

Mitigation: Check mmx quota before substantial use and monitor MiniMax quota or billing after running generation workflows.

## Reference(s):

- [MiniMax CLI Reference Notes](references/api-notes.md)
- [MiniMax Platform](https://platform.minimax.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run mmx-cli commands that return JSON responses or create local media files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
