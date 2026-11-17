## Description:

Aircall (aircall.io). Use this skill for ANY Aircall request — searching and reading data. Whenever a task involves Aircall, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Aircall users and developers use the skill to retrieve and search calls, contacts, phone numbers, teams, and users through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run online CLI installers whose exact effects could not be inspected, without a clear approval step.

Mitigation: Review and install the CLI separately from a verified release before allowing the skill to run.

Risk: Automatic skill synchronization and the connected Aircall account can expose more access than intended through OOMOL.

Mitigation: Review automatic skill synchronization and connect only the Aircall account intended for use with OOMOL.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Aircall API documentation](https://developer.aircall.io/api-references/)
- [Aircall homepage](https://aircall.io)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [oo CLI commands with JSON request payloads and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available actions retrieve Aircall calls, contacts, numbers, teams, and users.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
