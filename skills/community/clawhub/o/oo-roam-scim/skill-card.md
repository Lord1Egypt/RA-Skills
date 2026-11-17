## Description:

Use the OOMOL-connected oo CLI to read, create, update, and archive Roam SCIM users and groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use the skill to inspect Roam SCIM configuration and manage users and groups through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may make persistent changes to agent skills through automatic synchronization, and downloaded installers and hosted connector behavior are unverified.

Mitigation: Review the CLI installation first; disable startup skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting if only this connector is needed, use limited account permissions, and require confirmation for writes or destructive actions.

## Reference(s):

- [Roam SCIM API Documentation](https://developer.ro.am/)
- [Roam SCIM](https://ro.am)
- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and configuration details; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
