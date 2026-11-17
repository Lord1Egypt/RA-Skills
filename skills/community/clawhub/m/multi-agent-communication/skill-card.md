## Description:

This skill helps users build, manage, and optimize distributed agent systems with sessions_spawn and sessions_send for task decomposition, parallel processing, and agent coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate multi-agent workflows, including background child-agent tasks, persistent expert-agent sessions, parallel decomposition, and agent-to-agent messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invisible child-agent work can reduce user visibility during sensitive tasks.

Mitigation: Require explicit user approval for background agents on sensitive work and bind persistent sessions to visible threads when follow-up interaction is needed.

Risk: Wildcard cross-agent access can broaden agent communication beyond the intended team.

Mitigation: Use explicit allowlists for agent-to-agent access and child-agent spawning.

Risk: Parallel spawning and multi-round negotiation can exhaust resources or run longer than intended.

Mitigation: Keep recursion depth, child count, ping-pong turns, and timeouts capped to reviewed defaults.

## Reference(s):

- [Agent Configuration Reference](references/config.md)
- [Design Pattern Reference](references/patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with inline JSON and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration examples, tool-selection guidance, and multi-agent workflow patterns.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
