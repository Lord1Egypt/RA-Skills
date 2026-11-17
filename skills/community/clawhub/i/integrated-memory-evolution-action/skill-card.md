## Description:

Integrates a three-layer memory system, self-evolution workflow, and proactive action mode so agents can retain context, record lessons, and act from memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide agents through persistent memory checks, write-ahead logging, learning records, and proactive follow-up across tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent memory can capture and reuse user history beyond the current task.

Mitigation: Use only where persistent memory is intentional, users consent to storage, and retention practices are reviewed before installation.

Risk: Shared memory paths can expose sensitive context across agents or workspaces.

Mitigation: Restrict shared memory access to trusted agents and enforce workspace-appropriate access controls.

Risk: Scheduled or autonomous follow-up behavior can run without clear user approval.

Mitigation: Disable scheduled jobs by default or require explicit approval before enabling them.

Risk: Changes to agent-control files such as AGENTS.md or TOOLS.md can alter future agent behavior.

Mitigation: Require trusted human review before accepting changes to agent-control files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chungvic/skills/integrated-memory-evolution-action)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update persistent memory, learning, session-state, and agent-control files when enabled.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
