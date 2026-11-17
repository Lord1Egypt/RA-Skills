## Description:

Hetzner Cloud CLI for managing servers, volumes, firewalls, networks, DNS, and snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to get concise Hetzner Cloud CLI setup guidance and command examples for managing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad SSH firewall rules can expose servers to the whole internet.

Mitigation: Restrict SSH source IP ranges, harden the server before exposure, and approve firewall commands only after reviewing the exact proposed command.

Risk: Cloud administration commands can create or modify billable or security-sensitive Hetzner resources.

Mitigation: Review each proposed hcloud command before approval, use the least-privileged API token possible, and create snapshots before modifications.

## Reference(s):

- [Hetzner Cloud CLI repository](https://github.com/hetznercloud/cli)
- [Hetzner Cloud Console](https://console.hetzner.cloud/)
- [ClawHub skill page](https://clawhub.ai/pasogott/skills/hetzner-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are guidance for user review and approval, not automatic execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
