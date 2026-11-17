## Description:

Orthogonal Agent Framework helps agents organize complex tasks across separate planning, execution, memory, and evaluation modules so each module can be combined, replaced, tested, or extended independently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixingxun](https://clawhub.ai/user/lixingxun)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to structure complex, multi-step work into planning, execution, memory, and evaluation artifacts. It is most useful when tasks need persistent context, iterative assessment, or independently replaceable agent modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may create task files in the workspace.

Mitigation: Choose the intended working directory before invoking the skill and review generated files before committing or sharing them.

Risk: The memory template can preserve sensitive task context if users record it there.

Mitigation: Avoid placing secrets, credentials, or private data in memory.md unless persistent storage is intentional.

## Reference(s):

- [Design Principles](references/design-principles.md)
- [ClawHub Release Page](https://clawhub.ai/lixingxun/skills/orthogonal-agent-framework)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown task plans, execution logs, memory notes, evaluation tables, and interface examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update plan.md, execution.md, memory.md, and evaluation.md in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
