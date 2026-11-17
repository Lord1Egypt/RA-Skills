## Description:

Use Go2.gg API for URL shortening, link analytics, QR code generation, webhooks, and link-in-bio pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rakesh1002](https://clawhub.ai/user/rakesh1002)

### License/Terms of Use:


## Use Case:

Developers, marketers, and site operators use this skill to ask an agent for Go2.gg API commands and examples that create short links, inspect analytics, generate QR codes, manage webhooks, and publish link-in-bio galleries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use a Go2.gg API key for link, QR, webhook, and gallery management.

Mitigation: Install it only when the agent is intended to use GO2GG_API_KEY, keep the key in the environment, and review proposed commands before execution.

Risk: Generated commands can delete links or QR codes, publish galleries, or configure webhooks that affect a live Go2.gg account.

Mitigation: Review destructive and publishing actions before running them, especially DELETE requests, gallery publication changes, and webhook configuration.

Risk: Sensitive URLs or secrets could be exposed through link destinations, metadata, gallery content, or webhook configuration.

Mitigation: Avoid placing sensitive URLs, credentials, or private data in link metadata, public gallery content, or webhook targets.

## Reference(s):

- [Go2.gg API documentation](https://go2.gg/docs/api/links)
- [Go2.gg API key dashboard](https://go2.gg/dashboard/api-keys)
- [ClawHub Go2.gg skill page](https://clawhub.ai/rakesh1002/skills/go2gg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with cURL commands, Python examples, and JSON request or response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external API calls that require GO2GG_API_KEY; unauthenticated QR generation examples are also documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
