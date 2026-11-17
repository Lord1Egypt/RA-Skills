## Description:

Use MiniMax Coding Plan API for real-time web search and image understanding with the api.minimax.io endpoint and no external MCP server requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlin53882](https://clawhub.ai/user/jlin53882)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run MiniMax-backed web searches and image-understanding requests from a Node.js command-line tool using a configured MINIMAX_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, prompts, image URLs, and selected local image files may be sent to MiniMax using the user's API key.

Mitigation: Avoid sending sensitive, regulated, or confidential prompts or images unless that external transmission is acceptable for the intended use case.

Risk: Local image files are converted and submitted for image-understanding requests.

Mitigation: Review the selected file path before invoking image understanding and use only supported image types that are appropriate to share externally.

## Reference(s):

- [MiniMax Platform](https://platform.minimaxi.com)
- [ClawHub Skill Page](https://clawhub.ai/jlin53882/skills/minimax-coding-plan-tool-patched)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON objects containing web search results or image analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses can include titles, URLs, snippets, dates, and related searches; image responses include the prompt, image source, and returned analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
