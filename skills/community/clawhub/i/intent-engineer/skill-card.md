## Description:

A meta-framework for designing, building, and orchestrating an ecosystem of strategically-aligned agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to design, register, and orchestrate related agent skills with shared intent, data contracts, workflow patterns, and audit templates. It is intended for building governable multi-skill ecosystems rather than completing a single narrow task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The orchestration script includes unsafe eval-based condition handling.

Mitigation: Do not run the orchestrator on untrusted workflow configurations; remove or replace eval-based condition handling before deployment.

Risk: The skill asks the agent to broadly govern behavior, expand scope, log decisions, and update skills recursively.

Mitigation: Require explicit user approval for scope expansion, logging, recursive framework updates, and changes to existing skills.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installing and deploy it only when a broad governance framework is specifically needed.

## Reference(s):

- [Agent Decision Framework](references/agent_decision_framework.md)
- [Data Contracts Guide](references/data_contracts_guide.md)
- [Support Ticket Data Contract](references/data_contracts_support_ticket.json)
- [Sentiment Response Data Contract](references/data_contracts_sentiment_response.json)
- [Deconstruct Intent Worksheet](references/deconstruct-intent-worksheet.md)
- [Ecosystem Governance](references/ecosystem_governance.md)
- [Integration Patterns](references/integration_patterns.md)
- [Recursive Skill Development](references/recursive_skill_development.md)
- [Shared Intent Framework](references/shared_intent.md)
- [Skill Registry](references/skill_registry.json)
- [Workflow Design Template](references/workflow-design-template.md)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with referenced JSON schemas, Python scripts, and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify skill files, workflow definitions, data contract schemas, registry entries, and audit logs when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
