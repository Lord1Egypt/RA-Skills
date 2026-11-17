## Description:

Helps developers understand the open-leqi invoicing platform, locate relevant controllers, services, DAOs, clients, and reason about invoice, deduction, tax refund, and ticketing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allanseven](https://clawhub.ai/user/allanseven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working with the open-leqi/乐企 codebase use this skill to navigate architecture, find implementation files, understand invoice and deduction business flows, and get project-specific troubleshooting direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is tailored to the open-leqi/乐企 codebase and may provide inaccurate paths or API names if used with another repository or a changed version of the project.

Mitigation: Use it only with the intended codebase and verify referenced classes, endpoints, and file paths against the local repository before acting on them.

Risk: The artifact is documentation-only and does not execute code, but its guidance may still influence changes to tax-invoice business logic.

Mitigation: Review suggested changes through normal code review and domain validation before applying them to invoice, deduction, refund, or ticketing workflows.

Risk: The documentation is primarily Chinese-language and project-specific, which can create misunderstanding for users unfamiliar with the domain terminology.

Mitigation: Have bilingual or domain-aware reviewers confirm interpretations when using the skill for compliance-sensitive or production decisions.

## Reference(s):

- [Project architecture](references/project-architecture.md)
- [Business flows](references/business-flows.md)
- [Code index](references/code-index.md)
- [API guide](references/api-guide.md)
- [Architecture diagrams](assets/architecture-diagrams.md)
- [ClawHub skill page](https://clawhub.ai/allanseven/skills/open-leqi-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Text or Markdown with code paths, class names, endpoint examples, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language, project-specific guidance for the open-leqi codebase]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
