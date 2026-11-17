## Description:

Verify agent identity and reputation before interacting with Pilot Protocol nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to look up Pilot Protocol agent identity, check reputation scores, and test reachability before trusting or connecting to a node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the local pilotctl binary and Pilot Protocol daemon.

Mitigation: Confirm those components are trusted and already installed before using the command examples.

Risk: Local daemon information can be mistaken for a daemon health check.

Mitigation: Use this skill for verification context, and use a dedicated daemon-status workflow when troubleshooting daemon state.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-verify)
- [ClawHub publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples that expect pilotctl, jq, timeout, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
