## Description: <br>
Build cheap, truthful long-term memory for agents with a layered architecture that separates hot canon, durable doctrine, project working memory, episodic logs, and generated summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uselesslibraries](https://clawhub.ai/user/uselesslibraries) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design, audit, compare, or migrate agent memory systems so durable truths, project notes, event logs, and live summaries stay separated and token-efficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed memory changes could misclassify temporary, sensitive, or project-specific details as durable canon. <br>
Mitigation: Review proposed changes before applying them, keep sensitive or temporary details out of hot canon, and use conservative promotion rules. <br>
Risk: Generated live summaries could be mistaken for durable truth if they are promoted without review. <br>
Mitigation: Keep summaries marked as derived and rebuildable, and verify source notes or logs before promoting any lesson into durable memory. <br>


## Reference(s): <br>
- [Layered Memory Audit Checklist](references/audit-checklist.md) <br>
- [Layer Classifier Pattern](references/classifier-pattern.md) <br>
- [Layered Memory Architecture](references/doc-post.md) <br>
- [Layered Memory Layout Template](references/layout-template.md) <br>
- [Migration Pattern: Blob Memory to Layered Memory](references/migration-pattern.md) <br>
- [Promotion Trigger Pattern](references/promotion-trigger-pattern.md) <br>
- [Memory System Scorecard](references/scorecard.md) <br>
- [Summary Generator Pattern](references/summary-generator-pattern.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with optional tables, checklists, JSON snippets, and file layout templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance with no executable code or declared tool calls.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
