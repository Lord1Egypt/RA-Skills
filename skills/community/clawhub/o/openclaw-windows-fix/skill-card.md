## Description:

Fixes the Windows scheduled task bug that kills OpenClaw processes during idle. One script, permanent fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to keep the OpenClaw Gateway scheduled task running through Windows idle periods by applying manual Task Scheduler settings or creating the documented batch command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented administrator batch command force-replaces a persistent scheduled task and may run it elevated.

Mitigation: Prefer the manual Task Scheduler edits or use a narrowly scoped script that backs up the existing task, verifies the OpenClaw task name, and changes only the idle and restart settings.

Risk: The task command path can become unsafe if the gateway command or working directory is untrusted or writable by the wrong users.

Mitigation: Confirm the gateway command path is trusted and protected before applying the task change, and avoid /rl HIGHEST unless it is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/openclaw-windows-fix)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with batch command snippets and manual Windows Task Scheduler steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows administrator review before changing a persistent scheduled task.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
