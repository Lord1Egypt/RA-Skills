## Description:

Clay (clay.com). Use this skill for ANY Clay request — reading, creating, updating, and deleting data. Whenever a task involves Clay, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Clay through an OOMOL-connected account can retrieve account, credit, search, table, workflow, and routine data, create searches, and run routines. The skill guides users to inspect action schemas and confirm changes before write or destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified code, and the CLI's documented startup synchronization can install additional skills.

Mitigation: Use a reviewed, version-pinned oo release and disable startup skill synchronization unless those additional installations are intended.

Risk: Configured routines may perform arbitrary downstream changes, including when run as a batch.

Mitigation: Inspect the routine definition and confirm the target and expected effects before running it; inspect item outcomes after completion.

Risk: The Clay connection and request data are handled by OOMOL.

Mitigation: Connect only an account intended for use through OOMOL and account for that data handling when choosing inputs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-clay)
- [oo CLI source and documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Clay](https://www.clay.com/)
- [Clay API documentation](https://developers.clay.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Clay connector results and JSON request payloads, with oo CLI commands and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read data, create searches, or run routines; routine outcomes are asynchronous and may require result inspection.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
