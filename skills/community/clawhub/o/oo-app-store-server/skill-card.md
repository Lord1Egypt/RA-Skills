## Description:

App Store Server API (developer.apple.com). Use this skill for ANY App Store Server API request — reading, creating, updating, and deleting data. Whenever a task involves App Store Server API, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage App Store transactions, subscriptions, notifications, and retention messaging through their connected App Store Server API account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded code that was not verified and may introduce broader changes to agent skills.

Mitigation: Review and install a verified CLI release yourself, and disable automatic bundled-skill synchronization before use.

Risk: Actions can access connected Apple account and transaction data; some subscription changes are irreversible.

Mitigation: Review each action and its target, and carefully approve account changes, especially irreversible subscription extensions.

## Reference(s):

- [App Store Server API documentation](https://developer.apple.com/documentation/appstoreserverapi)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-app-store-server)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON request payloads and API responses, with Markdown instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read App Store data or change account state, depending on the selected action.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
