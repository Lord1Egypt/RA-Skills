## Description: <br>
A meta-framework for designing, building, and orchestrating an ecosystem of strategically-aligned agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design, govern, register, and orchestrate related agent skills around shared intent, data contracts, decision logging, and ecosystem-level workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow conditions in the orchestrator can run arbitrary Python when evaluated. <br>
Mitigation: Do not run the orchestrator on untrusted workflow definitions; remove eval or replace it with a constrained condition parser before operational use. <br>
Risk: The framework can guide registry changes, self-modification, and high-impact multi-skill workflows. <br>
Mitigation: Require explicit user approval before registry updates, recursive skill changes, purchases, crypto-related activity, or other high-impact workflows. <br>
Risk: Audit and decision logs may capture secrets, personal data, or exact prompts. <br>
Mitigation: Redact sensitive values and avoid storing secrets, personal data, and exact prompts in logs. <br>


## Reference(s): <br>
- [Intent-Engineering Skill Page](https://clawhub.ai/danielfoojunwei/intent-engineer) <br>
- [Agent Decision Framework: How the Agent Operates](references/agent_decision_framework.md) <br>
- [Data Contracts Guide: Defining Machine-Readable Skill Interfaces](references/data_contracts_guide.md) <br>
- [Ecosystem Governance: Managing the Skill Ecosystem](references/ecosystem_governance.md) <br>
- [Integration Patterns: Composing Skills into Workflows](references/integration_patterns.md) <br>
- [Recursive Skill Development: How the Agent Improves Itself](references/recursive_skill_development.md) <br>
- [Shared Intent Framework: Organization-Wide Goals and Values](references/shared_intent.md) <br>
- [Skill Registry](references/skill_registry.json) <br>
- [Phase 1: Deconstruct Intent Worksheet](references/deconstruct-intent-worksheet.md) <br>
- [Phase 2: Workflow Design Template](references/workflow-design-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, Python snippets, templates, and shell commands when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow definitions, registry entries, data contracts, and audit or decision logs for skill ecosystems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
