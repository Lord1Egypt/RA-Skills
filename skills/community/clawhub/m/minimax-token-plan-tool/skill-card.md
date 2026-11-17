## Description:

A lightweight MiniMax Token Plan Tool skill that directly calls official MCP APIs using pure JavaScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yorch233](https://clawhub.ai/user/yorch233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the web with MiniMax Token Plan, analyze images with MiniMax VLM, and check Token Plan quota information from an OpenClaw-compatible JavaScript tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and image prompts are sent to MiniMax through the configured API host.

Mitigation: Avoid submitting sensitive queries or prompts unless the data is approved for MiniMax processing.

Risk: Local image files can be read and uploaded for MiniMax image understanding.

Mitigation: Use only non-sensitive images and avoid private, regulated, or confidential local file paths.

Risk: Remote image fetching has a reported SSRF weakness.

Mitigation: Avoid untrusted remote image URLs or run the skill in a network-isolated runtime until the weakness is fixed.

## Reference(s):

- [MiniMax Token Plan (China Mainland)](https://platform.minimaxi.com/subscribe/token-plan)
- [MiniMax Token Plan (Global)](https://platform.minimax.io/subscribe/token-plan)
- [MiniMax Coding Plan MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP/)
- [Minimax Multimodal Toolkit](https://clawhub.ai/minimax-ai-dev/minimax-multimodal)
- [ClawHub skill page](https://clawhub.ai/yorch233/skills/minimax-token-plan-tool)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON command output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a MiniMax Token Plan API key; web search sends queries to MiniMax, and image understanding sends local or remote image content to MiniMax.]

## Skill Version(s):

1.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
