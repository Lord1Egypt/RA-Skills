## Description:

Automatic trust management with configurable policies for Pilot Protocol agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list pending Pilot Protocol trust requests and generate policy-based approval or rejection shell commands for known agents or networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk approval or rejection commands can make security-sensitive trust changes with too little confirmation or scoping.

Mitigation: Run pending/listing commands first, verify node identities through stronger signals, scope filters narrowly, and add an explicit confirmation step before bulk approve or reject operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-auto-trust)
- [Publisher profile](https://clawhub.ai/user/teoslayer)
- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume pilotctl and jq are installed and that a Pilot Protocol daemon is running.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
