## Description:

Vultr (vultr.com). Use this skill for ANY Vultr request — reading, creating, updating, and deleting data. Whenever a task involves Vultr, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect and manage Vultr instances, DNS domains, firewall groups, snapshots, and account details through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unverified remote installer and introduce broader local changes; the installer's exact effects could not be inspected.

Mitigation: Install and review a pinned CLI yourself, and block its automatic remote-install fallback.

Risk: Vultr write actions change infrastructure, and delete_instance permanently removes an instance.

Mitigation: Keep the skill's approval requirements for exact write payloads and confirm destructive targets before execution.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Vultr](https://www.vultr.com/)
- [Vultr API documentation](https://www.vultr.com/api/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text responses with JSON connector data, shell command examples, and JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema; write and destructive actions require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
