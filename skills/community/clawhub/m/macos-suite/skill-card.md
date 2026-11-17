## Description:

macOS Suite automates opening, reading, and creating content in local macOS apps including Mail, Calendar, Reminders, Notes, Maps, Freeform, Photos, Weather, Stocks, and Clock.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill on macOS to inspect local app state, open Apple app workflows, create confirmed local records, compose Freeform boards, and retrieve stock or weather outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access local Mail, Notes, Calendar, Reminders, Photos, Freeform, Weather, and Stocks data through macOS automation permissions.

Mitigation: Install only in trusted macOS workspaces and grant app automation, privacy, and accessibility permissions only when the requested workflow needs them.

Risk: Mail draft and send flows can include local file attachments.

Mitigation: Review recipient fields, message body, and attachment paths before using mail.draft or mail.send; use confirm=YES only after that review.

Risk: Caller-provided Shortcut names can run local Shortcuts during Reminders and Weather fallback flows.

Mitigation: Use only trusted Shortcut names and do not allow untrusted content to choose the shortcut= value or related command arguments.

Risk: Freeform commands modify the active local board through UI automation.

Mitigation: Prefer read-only or open-only commands until the target board and requested edits are clear, then require explicit confirm=YES for modifying actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/macos-suite)
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills)
- [ClawHub documentation](https://docs.openclaw.ai/tools/clawhub)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON command results with shell command examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with python3 and osascript; modifying actions require confirm=YES.]

## Skill Version(s):

0.2.3 (source: frontmatter, skill.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
