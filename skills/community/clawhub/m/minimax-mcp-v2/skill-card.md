## Description:

Perform real-time web searches and analyze images using MiniMax MCP with input prompts and flexible image sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillsp99](https://clawhub.ai/user/hillsp99)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to retrieve current web search results and generate image descriptions from local files or image URLs through MiniMax MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports command injection risk from invoking mcporter through shell=True with user-controlled inputs.

Mitigation: Review before installing and invoke mcporter with argument arrays before using untrusted queries, prompts, image paths, or URLs.

Risk: Search terms, image URLs, local image paths, screenshots, or file contents may be sent to an external MiniMax data flow.

Mitigation: Avoid submitting sensitive searches, local files, internal URLs, screenshots, or regulated data unless that external data flow is acceptable.

Risk: The security scan identifies an unpinned global mcporter dependency.

Mitigation: Prefer a pinned local mcporter dependency and review dependency provenance before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hillsp99/skills/minimax-mcp-v2)
- [Publisher profile](https://clawhub.ai/user/hillsp99)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON objects containing search results, links, summaries, dates, or image descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited to the first 10 organic results when structured MiniMax output is available.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
