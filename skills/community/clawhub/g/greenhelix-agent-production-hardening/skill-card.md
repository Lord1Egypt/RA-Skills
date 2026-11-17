## Description:

The Agent Production Hardening Guide provides a step-by-step playbook for taking AI agent systems from pilot to production with SLOs, circuit breakers, cost guardrails, EU AI Act compliance checklists, monitoring, SLA enforcement, code examples, and deployment patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this guide to assess and harden AI agent systems before production release. It helps teams define SLOs, monitor cost and latency, add resilience controls, plan deployment rollouts, and prepare operational and compliance review materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide contains live GreenHelix API examples and state-changing workflow examples that could affect an account if run with write-capable credentials.

Mitigation: Use sandbox or test-only least-privilege credentials, verify whether each endpoint is sandbox or production, and review account effects before running write-capable examples.

Risk: The skill requires GREENHELIX_API_KEY, and mishandled credentials could expose paid or privileged API access.

Mitigation: Provide credentials only through environment variables or a secrets manager, scope them to the minimum required permissions, and rotate them after testing.

Risk: Security evidence flags an unpinned package installation pattern in the guide.

Mitigation: Pin and isolate dependencies before installation, preferably in a temporary virtual environment or locked build workflow.

Risk: The guide includes operational and EU AI Act compliance guidance that may not match a reader's exact production or regulatory obligations.

Mitigation: Treat the material as implementation guidance and route production, legal, and regulated-workload decisions through internal engineering, security, and compliance review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-production-hardening)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with checklists, tables, Python examples, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human review before operational use; examples reference GREENHELIX_API_KEY and GreenHelix sandbox or API endpoints.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
