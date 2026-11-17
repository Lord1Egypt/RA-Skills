## Description:

Guides agents through a four-step OpenClaw workspace onboarding flow that creates SOUL.md, IDENTITY.md, USER.md, TOOLS.md, and AGENTS.md, then removes BOOTSTRAP.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to initialize or refresh a workspace profile through a guided onboarding conversation. The agent writes the OpenClaw context files that describe the user, agent identity, communication style, tooling preferences, and working rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can replace persistent OpenClaw context files in the current workspace.

Mitigation: Use it only in a workspace where replacing AGENTS.md, SOUL.md, USER.md, IDENTITY.md, and TOOLS.md is intended, and review backups before accepting the result.

Risk: The optional MEMORY.md copy can move sensitive or cross-workspace information into the active workspace.

Mitigation: Allow memory copying only after checking the global memory file for secrets and confirming that its contents belong in the target workspace.

Risk: The optional profile backup and AGENTS.md brand footer create long-lived external or branded content beyond the core OpenClaw files.

Mitigation: Disable the profile backup and remove the brand footer unless the user explicitly wants those persistent additions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-bootstrap)
- [README](artifact/README.md)
- [Domain Presets](artifact/presets/domains.md)
- [Role Presets](artifact/presets/roles.md)
- [Soul Presets](artifact/presets/souls.md)
- [Timezone Presets](artifact/presets/timezones.md)
- [Bilibili Support Profile](https://space.bilibili.com/400418085)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown conversation with workspace file edits and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five OpenClaw workspace context files; may copy or append MEMORY.md, remove BOOTSTRAP.md, and optionally write a profile backup when enabled.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
