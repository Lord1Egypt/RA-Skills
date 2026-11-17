## Description:

This skill provides an advisory checklist for assessing whether an AI system documents LGD's registered, evidenced, and gated criteria before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers can use it for a preliminary self-check of an AI system's registration, evidence, and access gates before deployment. Treat the result as advisory and verify safeguards independently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A passing score can result from keyword matches or supplied answers even when required safeguards are absent.

Mitigation: Use sanitized descriptions and treat results as advisory; independently verify evidence and safeguards before deployment.

Risk: The package does not include the advertised model-checking API or enforcement integration, and deployment behavior is unspecified.

Mitigation: Do not use a PASS result to deploy, expose, encrypt, or modify a service; require independent evidence and explicit approval for those actions.

## Reference(s):

- [LGD project hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory repository (project-listed reference)](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper (project-listed reference)](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation (project-listed reference)](https://github.com/zhaoxinghua09-cell/uibc-core)
- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/lgd-crypto-guard)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON with per-category scores, a gate result, and missing items; the rubric can also be printed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The gate is based on keyword matches or supplied answers and is not evidence of privacy compliance.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
