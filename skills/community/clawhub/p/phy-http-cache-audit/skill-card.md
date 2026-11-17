## Description:

HTTP caching header analyzer that checks Cache-Control directives, ETag/Last-Modified freshness, Vary correctness, CDN cache status, and stale-while-revalidate opportunities for URLs or local development servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to audit HTTP cache headers, identify inefficient or risky cache behavior, and produce targeted configuration guidance for web assets and APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches live response headers from user-provided URLs with curl, which can expose private, local, or unauthorized endpoints to agent-initiated network requests.

Mitigation: Use only URLs you control or have permission to test, and avoid private admin endpoints, localhost services, and third-party systems unless that access is intended.

Risk: Generated cache guidance can change browser, CDN, or proxy behavior if applied without review.

Mitigation: Review proposed cache directives and configuration snippets against the resource type, data sensitivity, and deployment environment before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-http-cache-audit)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and server configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cache grades, issue summaries, remediation steps, and nginx, Apache, Cloudflare, Fastly, or Next.js configuration examples.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
