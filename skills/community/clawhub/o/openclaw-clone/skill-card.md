## Description:

Helps agents guide users through importing, comparing, and selectively adapting OpenClaw skills, memory, configuration, and expert knowledge from another OpenClaw instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhmza](https://clawhub.ai/user/zhmza)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to migrate or learn from another OpenClaw setup by importing backups, expert profiles, skills, memory, and persona files. It is most useful when the user has authorized access to the source instance or backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted backups, skill directories, or recommended SkillHub packages can be imported into an active OpenClaw workspace.

Mitigation: Install only from trusted sources, review imported skills and files before activation, and test in a disposable or backed-up workspace.

Risk: Imported memory and persona files may contain private information or unwanted behavioral instructions.

Mitigation: Avoid importing private MEMORY.md content directly, remove sensitive data, and merge persona changes manually after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhmza/skills/openclaw-clone)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [TEST-REPORT.md](artifact/TEST-REPORT.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct file copies, archive extraction, SkillHub installs, and edits to OpenClaw memory or persona files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
