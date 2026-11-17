## Description:

Use an OOMOL-connected Quo (OpenPhone) account to read and manage contacts, messages, users, and phone numbers, and send text messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working in an OOMOL-connected Quo workspace can retrieve and manage contacts, review messages and account records, and send texts. The skill guides the agent to inspect each action's live schema and confirm state-changing actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may install software, and automatic synchronization can change other agent skills; these behaviors have not been verified.

Mitigation: Use a separately reviewed CLI installation, require approval before setup, and review or disable automatic skill synchronization using the CLI startup control.

Risk: The connected Quo account exposes messages and contacts through OOMOL-mediated access.

Mitigation: Connect only the intended Quo account and confirm that the account's messages and contacts are appropriate for this access.

## Reference(s):

- [Quo API documentation](https://www.quo.com/docs/)
- [Quo homepage](https://www.quo.com)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action results and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Quo data; create, update, delete, and send actions change account state and require user confirmation.]

## Skill Version(s):

1.0.6 (source: metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
