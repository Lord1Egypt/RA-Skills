## Description:

Helps operators inspect, diagnose, back up, and change supported network devices, with optional NetBox lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators and developers use the skill to inspect device state, diagnose interface or BGP issues, and stage or apply configuration changes across supported Cisco, Arista, and Juniper devices. NetBox lookups are optional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may leave powerful network credentials in plaintext despite the encrypted-store design.

Mitigation: Start with read-only device accounts and NetBox tokens, resolve plaintext enable-password settings before granting privileged access, and provide the master password through an interactive prompt or secret manager rather than a shell profile.

Risk: Configuration changes can disrupt device access or service, and an audit record does not authorize a change.

Mitigation: Review and approve the exact configuration diff before applying it, use commit confirmation or the device revert timer where supported, and check the reported safety net before committing.

## Reference(s):

- [Project homepage](https://github.com/AIops-tools/Network-AIops)
- [ClawHub release page](https://clawhub.ai/zw008/skills/network-aiops)
- [Capabilities](references/capabilities.md)
- [Setup guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Files, Shell commands, Text]

**Output Format:** [Structured device data (JSON), diagnostic summaries, configuration diffs, and CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration backups and changes depend on the configured device and supported driver.]

## Skill Version(s):

0.15.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
