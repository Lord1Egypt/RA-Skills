## Description:

NightPatch detects small workflow friction points during scheduled nighttime runs, proposes or applies low-risk fixes, and generates rollback-oriented reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teachers10086](https://clawhub.ai/user/teachers10086)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation-focused users use this skill to inspect repetitive workflow patterns, shell command usage, scattered notes, and old logs, then receive a concise report or a bounded nighttime maintenance action. It is intended for controlled workspace optimization rather than production environment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs can mutate a workspace without immediate human supervision.

Mitigation: Run in an isolated test workspace first, keep dry-run enabled, and require explicit approval before enabling cron or mutating actions.

Risk: Shell alias handling may persist changes to the user's shell profile.

Mitigation: Make ~/.bashrc writes opt-in, validate shell-history-derived commands, and review generated aliases before applying them.

Risk: Log cleanup can delete files in a way that is not directly rollbackable.

Mitigation: Quarantine, compress, or back up candidate logs before deletion, and review retention settings before running cleanup.

## Reference(s):

- [ClawHub NightPatch page](https://clawhub.ai/teachers10086/skills/night-patch)
- [SKILL.md](artifact/SKILL.md)
- [Security guide](artifact/SECURITY_GUIDE.md)
- [Release notes](artifact/RELEASE.md)
- [Inspiration source](https://xialiao.ai/p/10010000000005745)
- [Practice sharing](https://xialiao.ai/p/10010000000007345)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local reports, logs, audit records, rollback instructions, and dry-run summaries depending on configuration.]

## Skill Version(s):

1.0.2 (source: server release evidence, manifest.json, package.json, RELEASE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
