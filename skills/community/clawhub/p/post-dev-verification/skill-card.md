## Description:

Post-development full-stack verification skill that guides agents through environment analysis, test design, real execution, metrics evaluation, and feedback-driven fixes after development work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill after implementation to design and run full-stack verification with real services where feasible, evaluate quality gates, and produce quality reports and reusable test scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct broad service, database, network, and credential-using test actions without strong built-in scope guards.

Mitigation: Install and run it only in disposable local, CI, or sandbox environments with test credentials.

Risk: Execution phases may start or stop services, run migrations or seeds, clean test artifacts, and send network requests.

Mitigation: Review the Phase 0 environment report before execution and confirm hosts, database names, cleanup commands, migration or seed commands, and any Authorization-bearing requests.

Risk: Production-like endpoints, shared databases, broad cleanup commands, or host-level service control could create unintended side effects.

Mitigation: Avoid those targets unless explicitly intended, and keep all side effects scoped to a test environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leonardo-lb/skills/post-dev-verification)
- [Test Taxonomy & Boundary Value Analysis Reference](references/test-taxonomy.md)
- [Post-Development Verification: Quality Metrics Reference](references/metrics.md)
- [Feedback Report Schema](references/feedback-schema.md)
- [Test Anti-Patterns: Detection & Fix Strategies](references/anti-patterns.md)
- [Real E2E Test Templates](references/real-e2e-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON feedback reports, test code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce environment reports, test plans, quality metrics, fix-loop feedback, and reusable test scripts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
