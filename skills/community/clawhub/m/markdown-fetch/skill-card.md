## Description:

Optimizes web fetching by using Cloudflare's Markdown for Agents, reducing token consumption by ~80%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtimeschange](https://clawhub.ai/user/howtimeschange)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to fetch web pages with an Accept header that prefers Markdown responses, reducing token use when a compatible server provides Markdown while falling back to HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-savings logs can print full fetched URLs, which may expose private links, tokens, internal hostnames, or sensitive paths.

Mitigation: Sanitize or omit URLs in logs by default, and enable full URL logging only for explicit debugging after confirming links contain no secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtimeschange/skills/markdown-fetch)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The fetch helper returns response metadata, detected content format, fetched content, optional token-savings data, and response headers.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
