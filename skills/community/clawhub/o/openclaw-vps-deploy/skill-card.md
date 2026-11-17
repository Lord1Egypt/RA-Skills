## Description:

Deploys official or forked OpenClaw builds to a Hostinger VPS and configures SSH access, Node.js, OpenClaw installation, systemd, firewall rules, and auth token generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy a cloud-accessible OpenClaw gateway on a Hostinger VPS from either the official package or a custom fork. It also guides multi-agent VPS setups with separate ports, workspaces, systemd services, and optional tunnel exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment can run a persistent root service on a VPS.

Mitigation: Review and harden the service before use, prefer an unprivileged service account, and use a dedicated VPS for this workload.

Risk: The deployment handles SSH keys, API keys, and generated gateway tokens.

Mitigation: Use a dedicated deployment key, verify SSH host keys, avoid copying private keys to /tmp, protect generated tokens, and rotate any exposed API keys or tokens.

Risk: The gateway may be exposed over public HTTP.

Mitigation: Do not expose the raw gateway over public HTTP; place it behind TLS or a tunnel and keep direct ports closed where possible.

Risk: The deployment installs packages and can build a custom repository on the target server.

Mitigation: Pin trusted package and repository versions, review the selected package or repository before deployment, and validate the generated service and configuration before enabling them.

## Reference(s):

- [Known Gotchas - OpenClaw VPS Deployment](artifact/references/gotchas.md)
- [Multi-Agent VPS Deployment](artifact/references/multi-agent.md)
- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/openclaw-vps-deploy)
- [ClawHub publisher profile](https://clawhub.ai/user/maverick-software)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, Python, and systemd unit snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment commands, configuration files, service definitions, firewall guidance, and operational checks.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
