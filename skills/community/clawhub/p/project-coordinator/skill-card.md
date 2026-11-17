## Description:

Project Coordinator spawns an isolated coordination session that owns project context, breaks work into tasks, and delegates parallel execution to subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaigegao1110](https://clawhub.ai/user/kaigegao1110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to coordinate multi-step workspace projects by collecting project scope, spawning a coordinator session, delegating work to subagents, monitoring progress, and compiling final results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad project automation authority through coordinator and subagent workflows that can inspect and modify workspace files and run shell commands.

Mitigation: Enable it only in workspaces where this level of automation is acceptable, and review coordinator outputs and file changes before relying on them.

Risk: The artifact documents a GitHub main-branch install path that is not backed by server-resolved import provenance for this release.

Mitigation: Prefer the ClawHub/OpenClaw registry install path; if using GitHub directly, verify the exact commit or checksum before enabling the skill.

## Reference(s):

- [Project Coordinator ClawHub listing](https://clawhub.ai/kaigegao1110/skills/project-coordinator)
- [Project Coordinator homepage](https://github.com/KaigeGao1110/Project-Coordinator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, task summaries, and implementation artifacts when project work requires them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate subagents that inspect or modify workspace files and run shell commands under the host platform's permissions.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
