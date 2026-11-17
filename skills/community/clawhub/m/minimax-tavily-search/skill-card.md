## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for Minimax AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenchao2046](https://clawhub.ai/user/wenchao2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily-backed web searches, retrieve concise source summaries, and extract clean text from URLs for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, requested URLs, and the Tavily API key are sent to Tavily's API.

Mitigation: Use this skill only when Tavily processing is acceptable, and provision a scoped API key through TAVILY_API_KEY.

Risk: URL extraction can send private, sensitive, or access-controlled URLs to a third-party service.

Mitigation: Do not run extraction on private or sensitive URLs unless that third-party processing has been reviewed and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenchao2046/skills/minimax-tavily-search)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted terminal text with answers, source links, extracted URL content, and failure notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search result count is capped at 20 by the script.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
