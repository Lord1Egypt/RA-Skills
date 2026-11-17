## Description:

MiniMax image-understanding and web-search MCP skill for Docker-style environments, supporting image OCR, visual content understanding, and internet search through a local wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to configure and invoke MiniMax-backed image OCR, image content understanding, and web search through an MCP wrapper. It is aimed at Docker-style deployments such as environments adapted for 极空间.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A MiniMax API key could be exposed if pasted into chat or configured through an untrusted mechanism.

Mitigation: Configure the key outside chat using a trusted local secret mechanism, keep the credentials file private, and prefer a narrowly scoped, rotatable MiniMax key.

Risk: The wrapper executes external Node MCP tooling, and the security guidance flags executable path and dependency version handling for review.

Mitigation: Pin and review the MCP package version, fix the executable path before use, and avoid running the wrapper from untrusted project directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/minimax-mcp-docker)
- [Publisher profile](https://clawhub.ai/user/hongjiahao371-pixel)
- [MiniMax API platform](https://platform.minimaxi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call MiniMax MCP image-understanding or search commands; image-understanding operations can take 30-60 seconds and the wrapper uses a 120-second command timeout.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
