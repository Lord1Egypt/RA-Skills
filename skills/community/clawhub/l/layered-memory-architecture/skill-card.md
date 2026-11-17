## Description:

Helps agents design, explain, audit, and migrate toward layered long-term memory that separates hot canon, durable doctrine, project memory, episodic logs, and generated live summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uselesslibraries](https://clawhub.ai/user/uselesslibraries)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design, audit, explain, or improve token-efficient long-term memory systems. It is especially suited for reducing memory bloat, preserving project boundaries, and separating durable truth from logs or live derived summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration or audit advice could lead an agent to change persistent memory outside the intended scope.

Mitigation: Tell the agent exactly which memory files or stores are in scope and review proposed persistent changes before applying them.

Risk: Live status, logs, or generated summaries could be mistaken for durable canon during memory design.

Mitigation: Keep generated summaries marked as derived, route fresh or uncertain information to lower layers first, and promote only stable lessons after review.

## Reference(s):

- [Layered Memory Audit Checklist](references/audit-checklist.md)
- [Layer Classifier Pattern](references/classifier-pattern.md)
- [Layered Memory Architecture](references/doc-post.md)
- [Layered Memory Layout Template](references/layout-template.md)
- [Migration Pattern: Blob Memory to Layered Memory](references/migration-pattern.md)
- [Promotion Trigger Pattern](references/promotion-trigger-pattern.md)
- [Memory System Scorecard](references/scorecard.md)
- [Summary Generator Pattern](references/summary-generator-pattern.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown prose, checklists, rubrics, JSON classification snippets, and configuration-style layouts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only guidance skill with no hidden code or automatic persistence behavior found.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
