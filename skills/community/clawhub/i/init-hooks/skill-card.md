## Description:

Manage persistent startup hooks for OpenClaw containers and hosts, including inline commands, local scripts, and CDN-hosted archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw developers and operators use this skill to register, manage, test, and review scripts that run during startup, and to keep explicitly changed configuration synchronized to configured persistence paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing a mismatch between stated limits and a preset configuration path plus broad triggers and execution capabilities; its analysis is partial.

Mitigation: Review startup behavior, downloaded hooks, and configuration paths, and inspect or limit what runs before installing.

Risk: Configured inline commands, local scripts, and downloaded URL hooks can run during startup.

Mitigation: Use only hooks you trust, inspect their contents and effects, and require a matching SHA-256 for downloaded archives unless you explicitly accept the documented unverified exception.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/init-hooks)
- [Best practices](references/best-practices.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may operate startup hooks and user-selected configuration paths.]

## Skill Version(s):

1.0.4 (source: README changelog, released 2026-11-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
