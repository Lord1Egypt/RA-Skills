## Description:

1Password Events API (1password.com). Use this skill for ANY 1Password Events API request — searching and reading data. Whenever a task involves 1Password Events API, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to search 1Password Events API audit events, item usage, and sign-in attempts through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup executes downloaded CLI code that was not verified, and the CLI may make additional changes to agent skill files.

Mitigation: Review the setup steps, verify and install a specific CLI release, require approval for installation changes, and set OO_SKILLS_SYNC_DISABLED=1 before invocation if automatic skill-file writes are unwanted.

Risk: The connected service handles security-event data.

Mitigation: Confirm that OOMOL is permitted to handle this data before connecting the service.

## Reference(s):

- [1Password Events API reference](https://www.1password.dev/events-api/reference)
- [1Password](https://1password.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON event data with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only event queries; results depend on the connected account and action schema.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
