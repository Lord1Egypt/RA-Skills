## Description:

Uses the MiniMax Coding Plan API to perform web search and image understanding for information lookups and image analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirrorpromax](https://clawhub.ai/user/mirrorpromax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web through MiniMax Coding Plan MCP and analyze JPEG, PNG, or WebP images for descriptions, text extraction, and content understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a plaintext MiniMax API key.

Mitigation: Remove the embedded key, rotate it, and require users to provide credentials through their own environment.

Risk: The scripts run an unpinned external MCP package with the user's environment.

Mitigation: Pin and verify the dependency and pass only the minimal required environment variables to the subprocess.

Risk: Search prompts and image inputs may be sent to the MiniMax API.

Mitigation: Avoid sensitive prompts, private images, and secret-bearing environments unless the deployment has approved data-handling controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirrorpromax/skills/minimax-cp)
- [MiniMax API host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uvx, minimax-coding-plan-mcp, and a MiniMax API key; supports JPEG, PNG, and WebP image inputs.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
