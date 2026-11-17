## Description:

Design, implement, and operate a self-improving AI operating system for business with strategic planning, prioritization, knowledge management, operations, department agents, projects, auto-capture, communications, and metrics loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, founders, and agent builders use this skill to design a self-improving business operating system with strategy, department agents, memory, metrics, and learning loops. It provides implementation guidance, templates, and operating cadences for agentic business workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad business, customer, HR, and finance memory capture, which can expose sensitive information if storage and retrieval are not controlled.

Mitigation: Partition memory by department and data sensitivity, redact secrets and personal data before storage, and define retention and deletion rules before use.

Risk: Department agents may be used for public, outreach, deployment, invoice, or payment workflows without sufficiently explicit approval controls.

Mitigation: Run agents in draft-only mode by default, require human approval for public posts, outreach batches, deployments, invoices, and payments, and restrict connected accounts by department.

Risk: Auto-captured content can change long-term memory, SOPs, templates, or strategy based on incorrect or incomplete outputs.

Mitigation: Require review before captured content updates persistent memory, operating procedures, templates, or strategic documents.

## Reference(s):

- [CompoundOS ClawHub Skill Page](https://clawhub.ai/miknasbh-stack/skills/miknas-compoundos)
- [Strategic Layer Template](assets/strategy-template.md)
- [Department Agent Prompt Templates](assets/department-prompts.md)
- [Department Agents - ACRA Framework](references/department-agents.md)
- [Knowledge Management Setup](references/knowledge-setup.md)
- [Learning Loop & Auto-Capture](references/learning-loop.md)
- [Metrics & Monitoring - Operating Rhythm](references/metrics-cadence.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance, templates, and structured operating procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces business operating model plans, department agent prompts, metrics cadences, capture formats, and implementation checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
