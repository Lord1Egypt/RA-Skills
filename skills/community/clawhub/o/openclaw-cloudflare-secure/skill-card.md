## Description:

Securely expose an OpenClaw Gateway WebUI on a VPS via Cloudflare Zero Trust Access + Cloudflare Tunnel (cloudflared), including DNS cutover for custom hostnames and optional cleanup of Tailscale Serve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jskoiz](https://clawhub.ai/user/jskoiz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to expose an OpenClaw WebUI on a VPS behind Cloudflare Zero Trust Access and Cloudflare Tunnel while managing DNS records for a custom hostname.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and enable a persistent cloudflared system service with root privileges.

Mitigation: Review the service install command before execution, run it only on the intended VPS, and use the documented rollback command to disable the service when needed.

Risk: DNS cutover can delete or overwrite A, AAAA, and CNAME records for the target hostname.

Mitigation: Verify the zone and hostname arguments, keep a rollback record, and avoid production hostnames unless a rollback plan is ready.

Risk: Cloudflare tokens used by the helper scripts can modify DNS or install a tunnel if over-scoped or exposed.

Mitigation: Use narrowly scoped Cloudflare tokens, avoid storing secrets in logs or shell history, and rotate any token that may have been exposed.

Risk: The installer downloads the latest cloudflared package dynamically.

Mitigation: Prefer a pinned and verified cloudflared package in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jskoiz/skills/openclaw-cloudflare-secure)
- [Cloudflare API endpoint](https://api.cloudflare.com/client/v4)
- [cloudflared Linux AMD64 package](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline bash commands and bundled helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VPS shell access, Cloudflare DNS zone control, a Cloudflare API token, and a Cloudflare Tunnel token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
