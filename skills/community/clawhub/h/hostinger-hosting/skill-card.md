## Description:

Hostinger API integration via managed credentials for inspecting domains, DNS records, VPS instances, websites, subscriptions, and hosting account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill in OpenClaw to inspect and manage Hostinger domains, DNS, VPS instances, websites, subscriptions, and account information through a connected Hostinger account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party credential-broker plugin.

Mitigation: Review the ClawLink plugin publisher, version, and permissions before installation.

Risk: A connected Hostinger account can expose domains, DNS, VPS, website, subscription, billing, and account data to the integration.

Mitigation: Only connect Hostinger accounts whose resources and account data are acceptable to expose to this integration.

Risk: DNS, hosting, domain, and VPS write operations can have high-impact service effects.

Mitigation: Use preview or describe steps where available and confirm every write action before execution.

## Reference(s):

- [ClawHub Hostinger Skill](https://clawhub.ai/hith3sh/skills/hostinger-hosting)
- [Hostinger API Documentation](https://developers.hostinger.com/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hostinger-hosting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated Hostinger read and write operations through ClawLink; write operations require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
