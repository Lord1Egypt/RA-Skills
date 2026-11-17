## Description:

Self-hosted research tool combining Brave Search API + Browserless content fetching. Search the web with optional full-page content extraction and HTML parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[churchtg7](https://clawhub.ai/user/churchtg7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Power Search to run web searches, optionally fetch page content through Browserless, and return concise search results through a CLI or Telegram/OpenClaw command flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browserless setup and fetch behavior can create network exposure and private-network fetching risks.

Mitigation: Bind Browserless to 127.0.0.1, enable a token, add firewall or container limits, and block private, loopback, link-local, and metadata destinations before using --fetch or Telegram integration.

Risk: Search queries are sent to Brave and fetched snippets may be relayed through Telegram/OpenClaw infrastructure.

Mitigation: Avoid sensitive searches unless the deployment owner accepts those data flows.

Risk: Using an unpinned Browserless image can change runtime behavior across installs.

Mitigation: Pin the Browserless container image version during deployment.

## Reference(s):

- [Power Search ClawHub page](https://clawhub.ai/churchtg7/skills/power-search)
- [Publisher profile](https://clawhub.ai/user/churchtg7)
- [Power Search documentation](artifact/SKILL.md)
- [Security and transparency report](artifact/SECURITY.md)
- [Brave Search API](https://api.search.brave.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Plain text search results, JSON runner output, and Telegram-formatted Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include rank, title, URL, description, and optional fetched page preview text.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
