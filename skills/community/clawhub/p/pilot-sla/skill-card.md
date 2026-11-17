## Description:

Service-level agreement enforcement with automatic penalty assessment for pilotctl workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to define SLA contracts, monitor pilotctl task completion times, calculate success rates, and identify automatic penalty conditions for critical agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SLA calculations may be unreliable if jq expressions interpolate unvalidated shell variables or if command failures are ignored.

Mitigation: Pass AGENT and TASK_ID through jq --arg, validate inputs, and handle pilotctl and jq failures before relying on the results.

Risk: Success-rate enforcement can produce incorrect values when no matching tasks exist.

Mitigation: Check that the task count is greater than zero before dividing and before using results for penalties or compliance decisions.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-sla)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command snippets and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, bc, and appropriate access to pilotctl task data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
