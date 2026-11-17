## Description:

Analyzes legacy systems and prepares evidence-based Strangler Fig migration plans, domain plans, and draft specifications for a user-confirmed target stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and migration architects use this skill to assess a legacy repository, map bounded contexts, and prepare a staged migration roadmap with draft specifications and rollback plans. After approval, it can hand off work for GitHub issues and downstream execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads an entire legacy repository and writes planning artifacts into the target repository.

Mitigation: Review repository access and the selected target before running; keep sensitive values out of generated plans and specifications.

Risk: After approval, delivery can create GitHub issues and hand off approved specifications for execution, including previously approved specifications.

Mitigation: Review and trust downstream skills, check the exact specification set, and require a separate explicit confirmation before orchestrator execution.

Risk: Portuguese-only approval prompts may be unclear to some users.

Mitigation: Arrange a clear translation or adjust the approval language before authorizing external actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/migration-planner)
- [Publisher-listed project link (release provenance unavailable)](https://github.com/afonsoft/skills)
- [Research methodology](artifact/references/research-phase.md)
- [Planning methodology](artifact/references/plan-phase.md)
- [SPEC and issue handoff](artifact/references/spec-handoff.md)
- [Strangler Fig patterns](artifact/references/strangler-fig-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, GitHub issues]

**Output Format:** [Markdown plans, draft specifications, and optional GitHub issues]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning artifacts cite source evidence; GitHub issues require approval. User-facing approvals are in Portuguese (pt-BR).]

## Skill Version(s):

1.0.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
