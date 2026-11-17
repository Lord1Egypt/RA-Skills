## Description:

Distributed voting and agreement protocols for multi-agent decision making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate agreement among multiple agents for shared decisions, distributed transactions, or state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented quorum workflow can treat duplicate or unrelated votes as sufficient approval for state-changing commits.

Mitigation: Use it only after adding authenticated voter identities, proposal and term binding, duplicate-vote handling, and replay protection.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Pilot Consensus on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-consensus)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl, jq, uuidgen, and a running pilotctl daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
