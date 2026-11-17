## Description:

Three-level multi-agent coordinator for OpenClaw that supports single-task delegation, swarm collaboration, and coordinator-mode task dispatch when work is complex enough for multiple agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate complex OpenClaw tasks by deciding when to delegate one subtask, launch a communicating swarm, or run a coordinator that decomposes work, assigns workers, monitors progress, and summarizes results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subagents may be directed to use independent tool allowlists and not inherit parent denial rules, creating a permission-boundary concern.

Mitigation: Install only where the platform enforces child-agent permissions and cannot bypass parent denial rules; avoid broad read, write, exec, or network scopes unless explicitly approved.

Risk: Coordinator and swarm modes can spawn multiple workers and exchange messages, increasing the chance that incorrect guidance or task state propagates across agents.

Mitigation: Use the documented two-stage review and independent verification steps before relying on coordinated worker outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-coordinator)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured coordination steps and inline command or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to spawn subagents, send inter-agent messages, maintain scratchpad files, and summarize worker progress.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
