## Description:

Provides live OmniFocus access through native Omni Automation for reading and updating tasks, projects, inbox items, tags, due dates, flagged items, searches, and GTD reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberscribe](https://clawhub.ai/user/cyberscribe)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers with macOS OmniFocus use this skill to let an agent inspect live task data, summarize work, and perform approved task, project, folder, tag, date, note, and completion changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live access to the user's OmniFocus database and may require running local automation outside the normal sandbox.

Mitigation: Install only when that access is acceptable, grant macOS Automation permissions deliberately, and review results before acting on them.

Risk: Persistent write preferences can disable confirmations for destructive task changes.

Mitigation: Avoid `prefs set yolo`; prefer per-action confirmation before delete, move, rename, note replacement, or date changes.

## Reference(s):

- [Omnifocus4 ClawHub skill page](https://clawhub.ai/cyberscribe/skills/omnifocus4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; invoked commands return JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, OmniFocus 3 or 4, Python 3, and local automation access.]

## Skill Version(s):

1.0.3 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
