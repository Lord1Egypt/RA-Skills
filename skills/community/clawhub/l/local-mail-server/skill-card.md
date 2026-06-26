## Description: <br>
Guides an agent through setting up a self-hosted local mail server using Stalwart Mail Server, Brevo outbound relay, VPS inbound relay, Tailscale, DNS records, and related webmail configuration for environments without a public home IP address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklili3](https://clawhub.ai/user/franklili3) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and self-hosting administrators use this skill to configure a mail stack for home or NAT environments, including Stalwart, Postfix, OpenDKIM, Brevo relay, Tailscale connectivity, DNS authentication records, and webmail integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example passwords, SMTP keys, and placeholder credentials could be reused or exposed if copied directly. <br>
Mitigation: Replace all example credentials with strong, unique secrets and store operational credentials in an appropriate secret manager or protected configuration store. <br>
Risk: Disabling TLS peer verification or using invalid certificates can expose mail credentials and traffic. <br>
Mitigation: Use valid certificates or a trusted internal certificate authority, and keep TLS peer verification enabled for production deployments. <br>
Risk: Mail or administrative interfaces could be exposed beyond the intended local or VPN boundary. <br>
Mitigation: Restrict administrative interfaces to localhost or VPN access and verify firewall, DNS, and proxy settings before opening services. <br>
Risk: Following infrastructure changes without backups can make mail, DNS, VPS, or Nextcloud services difficult to recover. <br>
Mitigation: Back up VPS, DNS, Nextcloud, and mail-server configuration and data before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/franklili3/local-mail-server) <br>
- [Stalwart Mail Server](https://github.com/stalwartlabs/stalwart) <br>
- [Brevo](https://www.brevo.com) <br>
- [Tailscale](https://tailscale.com) <br>
- [Postfix](http://www.postfix.org/) <br>
- [OpenDKIM](http://www.opendkim.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, TOML, INI, DNS, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces setup guidance and example configuration snippets; users must replace placeholder domains, IP addresses, usernames, and secrets before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
