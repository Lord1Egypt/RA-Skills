## Description:

OpenClaw Skill quality audit based on CORE-EEAT framework adapted for AI agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[281862066-a11y](https://clawhub.ai/user/281862066-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate OpenClaw skills before installation, during development, or during maintenance. It produces structured quality and security audits, utility scores, security status labels, veto-item findings, and prioritized improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit recommendations and scanner command examples may be incorrect or inappropriate for a user's environment.

Mitigation: Review outputs before acting and run suggested scanners in a sandbox or reviewed local toolchain.

Risk: Illustrative npx-based scanner commands can install or execute third-party packages.

Mitigation: Prefer pinned versions or a reviewed local installation, and avoid running them with unnecessary secrets available.

## Reference(s):

- [OpenClaw Skill EEAT Benchmark](references/openclaw-skill-benchmark.md)
- [OpenClaw Skill Security Checklist](references/skill-security-checklist.md)
- [OpenClaw Security Guidelines](https://hello-claw.com/cn/adopt/chapter5/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown audit reports with scores, findings, recommendations, and illustrative command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security status labels, veto-item detection, prioritized action plans, and comparative scoring.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
