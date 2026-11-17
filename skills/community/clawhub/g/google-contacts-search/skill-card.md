## Description:

Atomic node skill to search google contacts. Loops internally until successful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to search a Composio-connected Google Contacts account and return matching contact records as structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose contact names, email addresses, phone numbers, or notes from a connected Google Contacts account to the agent or logs.

Mitigation: Install and run it only where the agent is permitted to access Google Contacts data through the configured Composio account, and avoid contexts where that data should not be visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-contacts-search)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and COMPOSIO_API_KEY; results may include sensitive Google Contacts data from the connected account.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
