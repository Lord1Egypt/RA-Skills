## Description:

Detect agent failures and trigger automatic task redistribution or re-election.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor Pilot Protocol swarm members through heartbeat messages, detect unreachable agents, and prepare failover, task redistribution, or leader-election workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample heartbeat and failover shell snippets may be unsafe if copied directly into a real recovery system without hardened input handling.

Mitigation: Pass dynamic values into jq with --arg, read agent IDs safely, validate peer identifiers and addresses, and add explicit error handling before deployment.

Risk: A failover or leader-election workflow can make incorrect recovery decisions if peer health signals are stale, malformed, or unverified.

Mitigation: Use heartbeat timeout detection together with direct peer verification and operational checks before triggering task redistribution or re-election.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, and supporting shell tools such as jq and bc.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
