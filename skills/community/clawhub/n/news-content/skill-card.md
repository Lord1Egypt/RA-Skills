## Description:

Input a news URL to efficiently extract the body, title, author, and date using a remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fonilye](https://clawhub.ai/user/fonilye)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract structured article content from public news URLs for summarization, analysis, or reuse by an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured network behavior can expose the API key and submitted URLs through unsafe TLS or HTTP behavior.

Mitigation: Use only non-sensitive public news URLs, configure an HTTPS backend, avoid http: endpoints, and use a scoped, rotatable API key.

Risk: The skill sends submitted URLs to a remote extraction service.

Mitigation: Review the remote data flow before deployment and do not use the skill for internal, private, or confidential URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fonilye/skills/news-content)
- [OpenClaw](https://openclaw.ai)
- [EasyAlpha API key portal](https://easyalpha.duckdns.org)
- [EasyAlpha extraction API endpoint](https://easyalpha.duckdns.org/api/v1/extract)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Remote API response rendered by the agent as text or Markdown; client-side errors are JSON strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus EASYALPHA_API_KEY and optional NEWS_EXTRACTOR_SERVER_URL environment variables.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
