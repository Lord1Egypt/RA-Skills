## Description:

Use NeetoDesk to read, create, and update tickets and comments through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents and operations teams use this skill to retrieve ticket and comment information, create tickets or comments, and update ticket fields in NeetoDesk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute downloaded CLI software without separate approval, and remote installer behavior remains unverified.

Mitigation: Review and approve the CLI installation separately; prefer a pinned release with independently verified integrity.

Risk: Ticket changes and replies can modify NeetoDesk data or send content on the user's behalf.

Mitigation: Connect only the intended NeetoDesk account and confirm the exact payload and effect before write actions.

## Reference(s):

- [NeetoDesk skill release](https://clawhub.ai/oomol/skills/oo-neetodesk)
- [NeetoDesk](https://www.neeto.com/neetodesk)
- [NeetoDesk API documentation](https://apidocs.neetodesk.com/getting-started/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and structured JSON responses, plus usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas to shape requests; write actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
