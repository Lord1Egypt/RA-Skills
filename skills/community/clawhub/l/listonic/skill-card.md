## Description:

Access Listonic shopping lists: list lists/items, add/check/delete items, and manage lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremymahieu](https://clawhub.ai/user/jeremymahieu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and update Listonic shopping lists from a command-line workflow. It supports listing lists and items, adding items, toggling item completion, and creating, renaming, or deleting lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and refreshed tokens are stored in plaintext under ~/.openclaw/credentials/listonic without automatic permission hardening.

Mitigation: Prefer token mode, restrict the credential directory and config file permissions manually, and rotate or revoke Listonic tokens if they may have been exposed.

Risk: Delete commands can remove Listonic lists or items without built-in safeguards.

Mitigation: Require explicit user confirmation with the resolved list or item before running delete-list or delete-item commands.

Risk: The skill uses unofficial Listonic API endpoints that may change without notice.

Mitigation: Review behavior before deployment and re-test core list and item workflows after Listonic service changes.

## Reference(s):

- [ClawHub Listonic skill page](https://clawhub.ai/jeremymahieu/skills/listonic)
- [Publisher profile](https://clawhub.ai/user/jeremymahieu)
- [Listonic API endpoint used by the skill](https://api.listonic.com)
- [Listonic token endpoint used by the skill](https://api2022auth.ts.listonic.com/identity/connect/token)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Plain text CLI output with optional JSON responses and Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a local Listonic credential configuration file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
