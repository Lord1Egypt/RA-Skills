## Description:

检测并修复OpenClaw工作目录嵌套问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxkandel99-arch](https://clawhub.ai/user/maxkandel99-arch)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace administrators use this skill to diagnose nested .openclawworkspace directories, validate workspace paths, and plan repairs with dry-run and confirmation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended workflow depends on unpinned PowerShell scripts from a personal GitHub repository outside the reviewed package.

Mitigation: Inspect the exact downloaded scripts, trust the repository owner, and prefer a release that pins scripts to a specific commit with hashes.

Risk: Repair steps may change workspace paths or delete nested workspace directories.

Mitigation: Use dry-run mode first, back up configuration files, and require explicit user confirmation before destructive changes.

## Reference(s):

- [External workspace-health script repository](https://github.com/maxkandel99-arch/workspace-health)
- [ClawHub skill page](https://clawhub.ai/maxkandel99-arch/skills/openclaw-workspace-doctor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with PowerShell command examples and repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run repair steps, user confirmation before deletion, configuration backup, and an OpenClaw Gateway restart after fixes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
