## Description:

Guides an agent through setting up a local mail server with Stalwart Mail Server, Brevo outbound relay, a VPS inbound relay, Tailscale, DNS records, Postfix, and OpenDKIM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklili3](https://clawhub.ai/user/franklili3)

### License/Terms of Use:

MIT

## Use Case:

Developers, self-hosters, and operators use this skill to configure mail sending and receiving for a local server in home, NAT, or no-public-IP environments. It provides deployment commands, configuration examples, DNS guidance, user-management examples, webmail integration notes, and troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example credentials and placeholder secrets could be reused in a real deployment.

Mitigation: Replace all example passwords, SMTP keys, and placeholder credentials with unique, strong secrets before use.

Risk: Mail, relay, or management services could be exposed beyond the intended local or private network.

Mitigation: Bind management interfaces to loopback or intended Tailscale addresses only, restrict firewall rules, and avoid public exposure of the management API.

Risk: Broad relay trust settings could allow unintended peers to relay mail.

Mitigation: Narrow Postfix relay trust to exact approved peers instead of broad network ranges.

Risk: Disabled TLS peer verification could expose mail traffic or credentials.

Mitigation: Keep TLS certificate verification enabled and fix certificate trust issues directly.

Risk: Downloaded server binaries could be tampered with or mismatched for the environment.

Mitigation: Verify downloaded binaries and release checksums before execution.

## Reference(s):

- [Stalwart Mail Server](https://github.com/stalwartlabs/stalwart)
- [Brevo](https://www.brevo.com)
- [Tailscale](https://tailscale.com)
- [Postfix](http://www.postfix.org/)
- [OpenDKIM](http://www.opendkim.org/)
- [ClawHub skill page](https://clawhub.ai/franklili3/skills/local-mail-server)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with shell commands, TOML snippets, INI snippets, DNS records, tables, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include placeholders for domains, IP addresses, credentials, and service-specific account values.]

## Skill Version(s):

1.0.0 (source: evidence.release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
