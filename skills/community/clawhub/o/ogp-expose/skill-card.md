## Description:

Expose OGP via a public HTTPS endpoint, usually a stable Cloudflare hostname or named tunnel, and help verify that gateway reachability and gatewayUrl configuration match the intended public endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dp-pcs](https://clawhub.ai/user/dp-pcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need to expose an OGP daemon to the internet for federation, peer discovery, or remote testing. It guides setup and verification for stable Cloudflare hostnames, temporary cloudflared or ngrok tunnels, reverse proxies, VPN-only access, and gatewayUrl alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose an OGP daemon through a public HTTPS tunnel.

Mitigation: Use it only when public exposure is intended, confirm OGP authentication, and prefer temporary tunnels for testing or named authenticated tunnels for production.

Risk: Persistent launchd or systemd tunnel configuration can keep public access available after initial setup.

Mitigation: Enable persistence only after review, document stop and removal steps, and verify the configured gatewayUrl and tunnel target before federation.

Risk: Privileged or global install commands can introduce supply-chain and host-configuration risk.

Mitigation: Pin and verify installed binaries where practical, avoid unnecessary sudo or global installs, and review commands before execution.

## Reference(s):

- [Ogp Expose ClawHub skill page](https://clawhub.ai/dp-pcs/skills/ogp-expose)
- [OGP documentation](https://github.com/dp-pcs/ogp)
- [Cloudflared downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [ngrok downloads](https://ngrok.com/download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline bash, JSON, XML, and systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for OGP, cloudflared, ngrok, curl verification, and local service configuration.]

## Skill Version(s):

0.6.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
