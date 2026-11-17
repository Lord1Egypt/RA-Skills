## Description:

Automatically archives daily OpenClaw chat transcripts into keyword-highlighted Markdown memory logs and can optionally update long-term memory summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanshijun607-png](https://clawhub.ai/user/yanshijun607-png)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to preserve important daily agent conversations, task context, configuration notes, and project highlights in local Markdown memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads saved chat transcripts and persists selected excerpts, which can include credentials or other sensitive workspace content.

Mitigation: Configure it narrowly, remove credential-related keywords, and periodically inspect or purge generated memory and log files.

Risk: Startup archiving can run automatically without a per-run confirmation step.

Mitigation: Disable startup archiving unless automatic capture is explicitly wanted, and prefer scheduled runs with reviewed scope.

Risk: Optional AI refinement can place sensitive summaries into long-term memory files.

Mitigation: Avoid AI refinement for sensitive workspaces or require review before MEMORY.md updates are retained.

Risk: Scheduled usage examples rely on unpinned npx execution.

Mitigation: Pin package versions and review scheduled commands before enabling recurring execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanshijun607-png/skills/memory-auto)
- [Configuration guide](artifact/CONFIGURATION.md)
- [Public README](artifact/PUBLIC-README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files with configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily memory logs, archive markers, runtime logs, and optional MEMORY.md updates in the user's workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package and changelog list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
