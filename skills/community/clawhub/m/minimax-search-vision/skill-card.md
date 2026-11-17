## Description:

MiniMax Search & Vision enables agents to search the web and analyze images through MiniMax Token Plan MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaolongliu1988](https://clawhub.ai/user/xiaolongliu1988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add MiniMax-backed web search and image understanding to an agent workflow. It is useful when an agent needs current search results, related search suggestions, or analysis of image URLs and local image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release depends on unpinned external mcporter and MiniMax MCP packages.

Mitigation: Pin and review external dependency versions before deployment, and install only in environments where that supply-chain exposure is acceptable.

Risk: The scripts pass a broad local environment to external MCP tooling.

Mitigation: Run with a narrowed environment containing only required MiniMax variables and avoid unrelated secrets in the execution context.

Risk: Search queries, screenshots, private images, and local image files may be sent to external MiniMax services.

Mitigation: Avoid sensitive queries and private images unless the data handling terms are approved for the intended use.

## Reference(s):

- [MiniMax Platform](https://platform.minimaxi.com)
- [MiniMax Token Plan MCP Guide](https://platform.minimaxi.com/docs/guides/token-plan-mcp-guide.md)
- [MiniMax API Reference](artifact/references/minimax_api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON results and Markdown guidance with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns result lists and related searches; image understanding returns structured analysis or raw model output.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
