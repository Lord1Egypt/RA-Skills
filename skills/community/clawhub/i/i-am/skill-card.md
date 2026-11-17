## Description:

i-am analyzes OpenClaw conversation history to infer personality traits and prepare reviewed updates for USER.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[designer-awei](https://clawhub.ai/user/designer-awei)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can use this skill to review personality-trait summaries inferred from their conversation history and optionally update USER.md after confirming a preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad OpenClaw conversation history to infer personality traits.

Mitigation: Prefer manual mode, review the exact preview before confirming updates, and run it only when that profiling is intended.

Risk: The skill can store personality-profile data persistently in USER.md, ChangeLog.md, temp/USER.md, and temp/last_analysis.json.

Mitigation: Inspect those files after use and delete stored profile, preview, changelog, or timestamp data when it is no longer wanted.

Risk: Scheduled mode can create recurring profiling runs.

Mitigation: Avoid scheduled mode unless ongoing analysis is desired, and remove any i-am cron entries to stop recurring runs.

Risk: Preview files may be sent through the active chat channel.

Mitigation: Check channel sensitivity before sending or confirming profile updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/designer-awei/skills/i-am)
- [ClawHub publisher profile](https://clawhub.ai/user/designer-awei)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and preview file content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces USER.md preview content and can create persistent changelog, timestamp, and scheduled-task state.]

## Skill Version(s):

0.0.5 (source: server release metadata; artifact frontmatter says 4.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
