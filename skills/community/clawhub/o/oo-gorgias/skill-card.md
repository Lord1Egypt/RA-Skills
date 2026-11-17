## Description:

Gorgias (gorgias.com). Use this skill for ANY Gorgias request — searching and reading data. Whenever a task involves Gorgias, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support and operations teams can use this skill to retrieve Gorgias account, ticket, customer, tag, and user information through a connected Gorgias account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run a downloaded CLI installer, and the remote installers were unavailable for inspection.

Mitigation: Require explicit approval before running an installer; preferably install a reviewed, version-pinned CLI yourself.

Risk: Connecting Gorgias authorizes OOMOL to mediate access to private helpdesk data.

Mitigation: Connect only the intended Gorgias account and review what data the connected account makes available.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Gorgias API documentation](https://developers.gorgias.com/reference/introduction)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented Gorgias account and helpdesk data]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
