## Description:

Operate AccuLynx through a connected OOMOL account to read information and create or update contacts, jobs, and appointments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected AccuLynx account can retrieve company settings and reference data, list calendar appointments, and create contacts or jobs or add and update initial appointments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute software whose installer and connector behavior are outside the verified artifact.

Mitigation: Review the installation source and use an inspected, pinned release before installing.

Risk: The connector mediates access to the user's connected AccuLynx account, and write actions change business data.

Mitigation: Preserve the required approval step and confirm the exact payload and effect before running a write action.

Risk: Agent skill synchronization may cause unwanted changes to the agent environment.

Mitigation: Review the OO CLI command reference for OO_SKILLS_SYNC_DISABLED and disable synchronization if it is unwanted.

## Reference(s):

- [AccuLynx API Documentation](https://apidocs.acculynx.com/docs/authentication)
- [OO CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [OO CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands with inline JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve account data; write actions require user confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
