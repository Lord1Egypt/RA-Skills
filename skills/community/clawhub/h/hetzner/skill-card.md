## Description:

Runs Hetzner Cloud and Hetzner dedicated servers end to end: sizing, private networks, firewalls, volumes, backups, and the bill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to plan, provision, automate, troubleshoot, and document Hetzner Cloud, Robot dedicated server, DNS, storage, backup, Kubernetes, migration, and cost workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent guidance can affect real Hetzner infrastructure and costs through cloud operations.

Mitigation: Confirm the active project/context, location, quoted monthly EUR cost, and explicit user approval before write or destructive commands.

Risk: Secrets such as API tokens, rescue passwords, storage credentials, SSH private keys, or cloud-init values may be exposed if saved verbatim.

Mitigation: Store only secret pointers such as environment variables, keychain entries, password manager paths, or local key paths, and strip raw credentials from saved notes.

Risk: Destructive actions such as deletion, rebuild, disk-growing resize, detach, or cancellation may be irreversible or leave billable resources behind.

Mitigation: Snapshot and verify before destructive actions, list resources that would be orphaned, and review destructive steps carefully before execution.

Risk: Local inventories and account context can become stale, causing incorrect provisioning, teardown, or cost recommendations.

Mitigation: Read and update the configured local Clawic inventories and compare them with live project state before provisioning, teardown, or cost analysis.

## Reference(s):

- [ClawHub Hetzner Skill Page](https://clawhub.ai/ivangdavila/skills/hetzner)
- [Hetzner Skill Homepage](https://clawic.com/skills/hetzner)
- [Hetzner Skill Definition](artifact/SKILL.md)
- [Security Guidance](artifact/security.md)
- [Automation Guidance](artifact/automation.md)
- [Production Guidance](artifact/production.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and code examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the hcloud CLI for Hetzner Cloud command execution; durable notes are stored locally under configured Clawic paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
