## Description:

Administer IT - monitor security and configure Workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and agents operating with approved Google Workspace administrative context use this persona to review pending IT requests, monitor suspicious login and audit activity, and configure Drive sharing policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this persona may operate with Google Workspace administrative permissions that can affect audit review, Drive sharing policy, or other organization settings.

Mitigation: Install it only for agents intended to operate in that administrative context and scope gws service account permissions appropriately.

Risk: Bulk Drive or security-policy changes can affect many users if executed without review.

Mitigation: Use dry-run mode and explicit review before bulk Drive or security-policy changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/persona-it-admin)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with Google Workspace CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use dry-run mode and explicit review before bulk Drive or security-policy changes.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
