## Description:

Automatic task memory and keep-alive loop for Obsidian-backed agents. Every task gets persistent notes. Arm the loop for long tasks, disarm when done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techieter](https://clawhub.ai/user/techieter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to persist task state in an Obsidian vault and optionally run scheduled keep-alive checks for long-running agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs always-enabled background jobs that may continue running after setup.

Mitigation: Inspect the five cron jobs after install, use /loop-stop when long-task monitoring is not needed, and remove or disable the jobs when background automation is no longer wanted.

Risk: Task details, private file paths, secrets, client data, or sensitive decisions may be persisted to an Obsidian vault.

Mitigation: Use a dedicated vault for agent task memory and review vault contents before using the skill with sensitive work.

Risk: Crafted vault paths may be mishandled by the installer.

Mitigation: Use a trusted, simple absolute vault path and review generated jobs and paths before relying on unattended runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/techieter/skills/memory-keep-alive-for-obsidian)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with command snippets and Obsidian note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates task memory notes, workflow state files, and scheduled job guidance for an Obsidian-backed OpenClaw setup.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
