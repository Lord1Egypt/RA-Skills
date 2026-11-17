## Description:

Helps clean old OpenClaw session files, rebuild sessions.json, and reduce session metadata growth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccc-3po](https://clawhub.ai/user/ccc-3po)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect OpenClaw session storage, clean old session files, and rebuild sessions.json when session data has grown too large.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting old session files or rebuilding sessions.json can remove or alter local session history.

Mitigation: Back up the OpenClaw sessions directory, review the files selected for deletion and the rebuild plan, and require explicit confirmation before running cleanup commands.

Risk: The skill references a specific local OpenClaw sessions path.

Mitigation: Confirm the path points to the intended OpenClaw profile before executing any commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccc-3po/skills/openclaw-session-cleaner)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target local OpenClaw session files and should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
