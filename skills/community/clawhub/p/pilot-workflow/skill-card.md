## Description:

YAML-defined multi-step workflows with advanced orchestration capabilities, including conditional branching, loops, parallel execution, and event-driven triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and engineers use this skill to define and run reusable YAML workflows that coordinate multi-step tasks across Pilot Protocol agents. It is suited to workflows that need conditions, dependencies, loops, parallel execution, or event-driven orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow tasks, URLs, identifiers, or results may be sent to dynamically selected Pilot Protocol peers.

Mitigation: Review workflows before use, prefer explicit agent addresses or trusted allowlists, and avoid secrets or private data unless destination agents are verified.

Risk: Tag-based agent selection may route tasks to an unintended or untrusted peer.

Mitigation: Use explicit agent addresses for sensitive workflows and confirm peer trust before execution.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon, jq, yq, and Bash 4.0 or later.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
