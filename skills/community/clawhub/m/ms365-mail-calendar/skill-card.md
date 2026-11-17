## Description:

Microsoft 365 Email & Calendar CLI via Microsoft Graph API. Supports multiple accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droba07](https://clawhub.ai/user/droba07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to authenticate to Microsoft 365, inspect inbox and calendar data, send email, and create calendar events through Microsoft Graph from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email and create calendar events through Microsoft Graph, and the security evidence notes weak or misleading safeguards for these user-impacting actions.

Mitigation: Review commands before execution, use the least-privilege Microsoft app registration possible, and avoid granting access to accounts that should not be controlled by this CLI.

Risk: Authentication tokens are stored locally for each named account.

Mitigation: Protect the local credential directory, restrict filesystem access to the user running the skill, and remove stored account tokens when access is no longer needed.

Risk: Mail sending and calendar creation occur without an actual confirmation prompt in the current code.

Mitigation: Require human review of send and calendar-create command arguments before running the skill in workflows that affect real users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/droba07/skills/ms365-mail-calendar)
- [Microsoft Graph API v1.0](https://graph.microsoft.com/v1.0)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration]

**Output Format:** [Command-line text with Microsoft Graph email and calendar results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and MICROSOFT_CLIENT_ID; supports separate named Microsoft 365 accounts.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
