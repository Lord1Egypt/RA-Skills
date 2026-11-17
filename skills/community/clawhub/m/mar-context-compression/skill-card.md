## Description:

Guides agents through context-compression strategies, structured summarization, and probe-based evaluation for long-running sessions and large codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design compression workflows that preserve session intent, file trails, decisions, current state, and next steps. They can also use its probe-based evaluation framework to test whether compressed context remains useful for continuing technical work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled evaluator can send conversation content, compacted context, probe responses, or other sensitive work material to an external HeyBoss/SkillBoss API.

Mitigation: Do not run the evaluator on private conversations, proprietary repositories, customer data, credentials, or regulated content unless approved; require explicit opt-in, redact sensitive inputs, or use a local-only evaluator.

## Reference(s):

- [Context Compression Evaluation Framework](references/evaluation-framework.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured-summary templates, evaluation rubrics, code examples, and optional JSON-style evaluator outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
