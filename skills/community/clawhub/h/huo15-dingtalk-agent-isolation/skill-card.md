## Description:

Creates isolated OpenClaw agent workspaces, agent directories, memory, and session history for DingTalk users, with manual binding and optional dynamic agent creation modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to configure per-user DingTalk agent isolation for known teams through manual bindings, or to prepare dynamic per-user agent creation for growing external or internal DingTalk deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic mode can persistently modify local OpenClaw configuration and connector source files.

Mitigation: Prefer manual bindings for known users; review dynamic-mode changes before installation, keep backups, and avoid elevated privileges.

Risk: Unvalidated DingTalk IDs or path templates can create unintended agent IDs, workspaces, or agent directories.

Mitigation: Add strict ID validation and constrain workspace and agent paths under approved OpenClaw directories before enabling dynamic mode.

Risk: Config writes in dynamic mode can become unsafe under concurrency or failure.

Mitigation: Use a locked and atomic config mutation API, set maxAgents, and test recovery from backups before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-dingtalk-agent-isolation)
- [Dynamic Agent Patch Reference](artifact/references/dynamic-agent-patch.ts)
- [Feishu Dynamic Agent Reference](artifact/references/feishu-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, TypeScript patch references, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include manual binding steps, generated OpenClaw configuration fragments, verification commands, and dynamic-mode patch guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
