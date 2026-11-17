## Description:

Diagnoses and repairs proxy failures in mihomo, Clash.Meta, and Clash deployments across local, remote, container, router, NAS, and desktop environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkcodee](https://clawhub.ai/user/thinkcodee)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators and developers use this skill to diagnose proxy outages, identify likely network or configuration causes, and restore mihomo or Clash deployments across local and remote environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports credential exposure risk involving controller secrets and token-bearing subscription URLs.

Mitigation: Keep secrets and full subscription URLs private, restrict controller access to trusted networks, and avoid exposing the controller port publicly.

Risk: The security assessment flags unexpected network activity, local secret discovery, temporary-file behavior, and actions that may exceed their stated scope; three scripts were only partially analyzed.

Mitigation: Review scripts and destinations before use, run configuration changes in dry-run mode first, confirm the target system, retain a backup, and verify any changes before restarting services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thinkcodee/skills/mihomo-skill)
- [Publisher profile](https://clawhub.ai/user/thinkcodee)
- [Diagnosis playbook](references/diagnosis-playbook.md)
- [Mihomo configuration notes](references/mihomo-config-notes.md)
- [Platform access guide](references/platform-access.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic findings and configuration changes for review.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
