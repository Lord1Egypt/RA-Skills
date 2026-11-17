## Description:

Orche is a multi-agent orchestration engine that systematically executes complex tasks through Query, Plan, Execute, and Verify phases with phase gates, critic debate, hallucination checks, and regression on verification failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reikys](https://clawhub.ai/user/reikys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use Orche to coordinate complex, multi-step agent work that benefits from explicit requirements, planning debate, parallel execution, and final verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-agent execution can consume meaningful tokens or model budget.

Mitigation: Invoke Orche deliberately, set practical budget and concurrency limits, and request approval at each step for high-risk or expensive tasks.

Risk: The workflow can write orchestration state and deliverables into workspace/orche-* paths.

Mitigation: Review generated state, plans, task outputs, and verification reports before relying on them or moving them into production work.

Risk: Parallel agents may produce incomplete or incorrect intermediate outputs.

Mitigation: Use the built-in phase gates, hallucination checklist, and final verification results as review checkpoints before acting on deliverables.

## Reference(s):

- [Orche ClawHub skill page](https://clawhub.ai/reikys/skills/orche)
- [reikys publisher profile](https://clawhub.ai/user/reikys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses and workspace files with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write orchestration state, plans, task outputs, verification reports, and completion summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
