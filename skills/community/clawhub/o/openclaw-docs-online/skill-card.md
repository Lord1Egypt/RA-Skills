## Description:

Guides an agent to access and query the official OpenClaw documentation at https://docs.openclaw.ai/ for accurate, sourced product information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uynewnas](https://clawhub.ai/user/uynewnas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to answer questions about OpenClaw features, configuration, troubleshooting, APIs, and deployment by consulting official documentation and returning source-linked Markdown guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready Gateway, Docker, API, or Nginx examples could expose an unauthenticated OpenClaw management API if reused in production as-is.

Mitigation: Review examples before operational use; require authentication, bind management APIs to loopback or a private network, use HTTPS, and restrict access with firewall or network controls.

Risk: Documentation answers may become stale or incomplete if the official OpenClaw documentation changes or does not cover the requested topic.

Mitigation: Consult the official documentation at answer time, include source links and applicable version details, and clearly state when documentation does not contain an answer.

## Reference(s):

- [OpenClaw official documentation](https://docs.openclaw.ai/)
- [OpenClaw getting started](https://docs.openclaw.ai/getting-started)
- [OpenClaw Gateway configuration](https://docs.openclaw.ai/configuration/gateway)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills)
- [OpenClaw API reference](https://docs.openclaw.ai/api)
- [OpenClaw troubleshooting](https://docs.openclaw.ai/troubleshooting)
- [ClawHub skill page](https://clawhub.ai/uynewnas/skills/openclaw-docs-online)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with source links and optional command or configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should cite official documentation, state version or freshness when available, and say when requested information is not found.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
