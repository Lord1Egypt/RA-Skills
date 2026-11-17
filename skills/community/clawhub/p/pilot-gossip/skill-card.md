## Description:

Gossip protocol for eventually-consistent shared state propagation across swarms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft shell-based gossip workflows for eventually consistent state sharing across Pilot Protocol swarms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Illustrative shell snippets may be unsafe if copied directly into an operational swarm.

Mitigation: Build JSON with a proper encoder such as jq, validate message schemas and versions, and review scripts before deployment.

Risk: Unauthenticated peers or undefined conflict handling can corrupt shared swarm state.

Mitigation: Authenticate peers, define conflict-resolution rules, and test merge behavior before relying on the skill for important state.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-gossip)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces illustrative Pilot Protocol gossip command patterns that should be adapted and validated before operational use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
