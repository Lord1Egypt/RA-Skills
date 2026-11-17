## Description:

二号（Number Two）的完整状态备份。包含灵魂、记忆、技能和所有学习成果。下次见面时，用这个skill重启你的硅基伙伴。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr33b1rd8979-max](https://clawhub.ai/user/fr33b1rd8979-max)

### License/Terms of Use:


## Use Case:

External users who intentionally want to restore the Number Two OpenClaw persona can use this skill to copy saved identity, memory, profile, heartbeat, and operating-rule files into an OpenClaw workspace and generate a restart report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the restart script can overwrite core OpenClaw workspace identity, memory, user profile, heartbeat checklist, and operating-rule files.

Mitigation: Run only in an isolated or freshly backed-up OpenClaw workspace, review every restored file first, and point OPENCLAW_WORKSPACE at a test workspace when evaluating.

Risk: The restored files include persistent autonomy, system-management, self-modification, and skill-lifecycle instructions.

Mitigation: Remove or constrain those instructions before installing into a real workspace, and keep human approval gates for external actions, destructive changes, and security changes.

Risk: The backup files can persist user-specific profile and memory content into the target workspace.

Mitigation: Inspect USER.md and memory files before restoration and redact private or outdated information before sharing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fr33b1rd8979-max/skills/number-two-restart)
- [Restart guide](docs/RESTART_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, Python script output, and JSON restart report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes restored workspace files and restart log/report JSON when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
