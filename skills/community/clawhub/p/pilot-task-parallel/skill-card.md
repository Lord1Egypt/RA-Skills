## Description:

Fan-out tasks to multiple agents and merge results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to distribute independent work across multiple agents, wait for completion, and aggregate parallel task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example shell snippets can become unsafe when task IDs, peer addresses, or discovered agents are used without validation.

Mitigation: Pass task IDs to jq with --arg or --argjson, read peer addresses into arrays safely, and validate discovered agents before dispatching tasks.

Risk: Polling loops can wait indefinitely if submitted tasks never reach a terminal state.

Mitigation: Add polling timeouts and failure handling before using the examples in operational workflows.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-task-parallel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, Bash 4.0+, the pilot-protocol skill, and a running pilotctl daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
