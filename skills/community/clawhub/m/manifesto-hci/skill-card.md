## Description:

Manifesto HCI implements the Explicit State & Continuous Consensus pattern to maintain Git-backed project state, conversation logs, and intent synchronization for long-running agent work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leozhoski](https://clawhub.ai/user/leozhoski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and planners use this skill to keep durable goals, constraints, decisions, and active work state aligned across long-running projects. It is intended for projects where intent drift and loss of shared context are material risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist full conversation history and project state locally.

Mitigation: Use it only for projects where local Git-backed memory is desired, avoid sharing secrets while it is active, and review generated logs and commits.

Risk: Broad activation triggers and weak input scoping can record more context than expected.

Mitigation: Use a dedicated, non-sensitive project_id and avoid shared or untrusted conversations unless consent controls and path validation are added.

## Reference(s):

- [Manifesto HCI System Architecture and Protocol](references/specification.md)
- [Diff Sub-Agent System Prompt](references/diff_agent_prompt.md)
- [Manifesto Template](references/manifesto_template.md)
- [Light Mode Protocol](references/light_mode_protocol.md)
- [Light Mode Guide](references/light_mode_guide.md)
- [ClawHub skill page](https://clawhub.ai/leozhoski/skills/manifesto-hci)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON audit receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project state, append JSONL conversation logs, and create Git commits during use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
