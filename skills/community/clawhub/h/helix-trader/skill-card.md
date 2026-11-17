## Description:

Helix Trader guides users through installing and safely operating a self-hosted crypto trading bot for local setup, diagnostics, testnet-first configuration, strategy selection, preview, status checks, and stopping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frederica123](https://clawhub.ai/user/frederica123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, and operate the Helix Trader bot on their own computer. It supports testnet-first setup, configuration preview, strategy selection, status checks, and safe stop workflows without requesting or echoing credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote setup code can change between installs.

Mitigation: Prefer a pinned Helix Trader release or audited commit, and inspect setup_backend.sh before running it.

Risk: Local admin access can be exposed by broad network binding, development reload mode, default credentials, or a weak JWT secret.

Mitigation: Bind the backend to 127.0.0.1, remove --reload for normal use, and change default admin credentials and JWT_SECRET before startup.

Risk: Exchange credentials can enable unintended trading impact if over-permissioned or used live before review.

Mitigation: Use testnet keys with minimum permissions and no withdrawal access; require explicit live-trading confirmation before any live operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/frederica123/skills/helix-trader)
- [Helix Trader Homepage](https://github.com/trade-upnow/helix-trader)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses testnet-first and preview-before-start workflows; does not request or echo secrets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
