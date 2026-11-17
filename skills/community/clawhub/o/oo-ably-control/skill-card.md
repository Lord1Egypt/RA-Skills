## Description:

Manage Ably Control apps, API keys, queues, and account or app statistics through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Ably account administrators use this skill to inspect account and app data, manage apps, API keys, and queues, and retrieve usage statistics through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a remote CLI installer whose behavior has not been inspected, and additional agent-skill installation behavior is unexplained.

Mitigation: Review the installer and choose and verify the CLI release before setup; consider setting OO_SKILLS_SYNC_DISABLED=1 before invocation.

Risk: The skill can create, update, delete, or revoke Ably resources and can retrieve account tokens or API key data.

Mitigation: Use narrowly scoped Ably credentials, protect returned key data, and confirm the exact payload and effect before write or destructive actions.

## Reference(s):

- [Ably Control API documentation](https://ably.com/docs/api/control-api)
- [Ably Control](https://ably.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read or change Ably resources; write and destructive actions require confirmation of the payload and effect.]

## Skill Version(s):

1.0.4 (source: evidence release version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
