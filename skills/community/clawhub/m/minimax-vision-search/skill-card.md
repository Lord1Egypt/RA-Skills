## Description:

Analyze images and search the web using MiniMax MCP tools

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to analyze local, URL, or Telegram-saved images and run MiniMax-backed web searches from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unpinned external MCP tooling and includes curl-to-shell installer guidance.

Mitigation: Prefer a pinned and reviewed MCP package and avoid the curl-to-shell installer path.

Risk: Images, URLs, search queries, and the MiniMax API key are handled by MiniMax tooling.

Mitigation: Use a narrowly scoped MiniMax key, avoid submitting sensitive images, URLs, or search queries, and clean up private Telegram images stored under ~/.openclaw/media/inbound.

## Reference(s):

- [Minimax Vision Search on ClawHub](https://clawhub.ai/daowuu/skills/minimax-vision-search)
- [Project Homepage](https://github.com/daowuu/minimax-vision-search)
- [MiniMax MCP Guide](https://platform.minimaxi.com/docs/token-plan/mcp-guide)
- [MiniMax Token Plan](https://platform.minimaxi.com/subscribe/token-plan)
- [Chinese README](references/README_zh.md)
- [Setup Guide](references/setup.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts print JSON responses from MiniMax tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uvx and MINIMAX_API_KEY; MINIMAX_API_HOST is optional and defaults to https://api.minimaxi.com.]

## Skill Version(s):

1.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
