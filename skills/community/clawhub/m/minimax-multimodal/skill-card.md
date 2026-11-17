## Description:

Use mmx to generate text, images, video, speech, and music via the MiniMax AI platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minimax-ai-dev](https://clawhub.ai/user/minimax-ai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the MiniMax CLI for multimodal generation, image understanding, web search, quota checks, and related API-resource workflows from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a global npm install for mmx-cli, and the release evidence notes that the package is unpinned.

Mitigation: Verify the npm package and version before installation, and install only in environments where that package is trusted.

Risk: The skill shows API-key usage patterns that can expose MiniMax credentials if copied directly into shell history or logs.

Mitigation: Prefer environment variables or secret-manager workflows, and avoid placing real API keys directly in commands.

Risk: The --yes flag can bypass confirmations before quota-consuming operations.

Mitigation: Use --dry-run or review command parameters before using --yes in automated workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and expected CLI output formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides mmx CLI calls that may return text, JSON, task IDs, file paths, media URLs, or generated media files depending on the command.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
