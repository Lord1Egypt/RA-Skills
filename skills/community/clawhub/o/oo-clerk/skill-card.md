## Description:

Operate Clerk through an OOMOL-connected account using the oo CLI for user lookup, creation, updates, access controls, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account administrators use the connected Clerk account to inspect user records and make approved changes, including creating, updating, locking, banning, and deleting users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code, and the hosted implementation was not verified.

Mitigation: Review setup, install a verified oo CLI release yourself, and review or disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: The Clerk connection gives OOMOL access to the account, and some actions change or delete user data.

Mitigation: Keep approval requirements for account changes and deletion, and review the action schema and payload before running writes.

## Reference(s):

- [Clerk Backend API documentation](https://clerk.com/docs/reference/backend-api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell command examples with JSON payloads and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The action schema and payload depend on the selected Clerk operation.]

## Skill Version(s):

1.0.7 (source: skill frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
