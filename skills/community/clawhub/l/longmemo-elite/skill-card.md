## Description:

精英长记忆 (LongMemo Elite) guides agents to maintain durable cross-session memory with WAL-style state writes, hybrid retrieval, layered storage, budget controls, and memory hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure long-term memory workflows for cross-session projects, preference retention, multi-agent context sharing, and retrieval of prior decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable cross-session memory can retain sensitive, regulated, customer, or stale context longer than intended.

Mitigation: Enable the skill only for workspaces where durable memory is intentional, review what is written, and avoid using it for secrets, regulated data, private customer information, or contexts that must not resurface automatically.

Risk: Optional cloud memory services can move stored context outside the local workspace.

Mitigation: Review cloud service configuration before enabling synchronization and keep local-only storage when external persistence is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/longmemo-elite)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local memory files, vector stores, Git notes, and optional cloud memory records when followed.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
