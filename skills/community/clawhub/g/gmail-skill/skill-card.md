## Description:

Automates Gmail inbox summaries, label management, spam and trash cleanup, message filing, and message deletion workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r39132](https://clawhub.ai/user/r39132)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect and manage a Gmail mailbox, including unread-message summaries, label organization, spam and trash cleanup, filing messages into labels, and confirmed deletion tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive Gmail actions, including label deletion, message trashing, and permanent deletion when full-scope authorization is present.

Mitigation: Confirm the target account, labels, dates, and exact command before running destructive actions; avoid full-scope permanent deletion unless it is specifically required.

Risk: The skill can run detached background jobs and deliver task output through WhatsApp, which may expose mailbox-derived information outside the local agent session.

Mitigation: Use background jobs only after confirming the WhatsApp recipient and task scope, and review local job logs and status before relying on the result.

Risk: The skill stores OAuth and job state locally, including a full-scope token file when permanent deletion is enabled.

Mitigation: Protect local token and job directories, remove unneeded full-scope tokens, and install the skill only in environments where local credential storage is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/r39132/skills/gmail-skill)
- [Gmail full access OAuth scope](https://mail.google.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some helper commands can emit TSV or JSON status output; background tasks can send progress and final results through WhatsApp.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
