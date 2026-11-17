## Description:

Use Airtable through an OOMOL-connected account to read and manage bases, tables, fields, and records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Airtable workspaces use this skill to inspect data and perform approved changes through their OOMOL-connected Airtable account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes downloaded installer code without a separate approval step, and the remote installers and connector implementation were not verified.

Mitigation: Review and approve CLI installation separately before setup; check whether it installs additional skills, limit the connected Airtable account's access, and retain explicit approval for writes and deletions.

## Reference(s):

- [Airtable Web API documentation](https://airtable.com/developers/web/api/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Shell commands for the oo CLI and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that write or delete data require user confirmation as described in the skill.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
