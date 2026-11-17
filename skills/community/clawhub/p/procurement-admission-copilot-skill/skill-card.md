## Description:

Shadow-mode copilot for B2B procurement admission that checks supplier material packages for completeness and consistency and tracks approval cases, while leaving admission decisions to a human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and human reviewers use the skill to check supplier qualification packages for missing or inconsistent information and to track approval case status, stalls, and gaps. It produces review materials for a human to assess; it does not make admission decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan could not resolve three local path-like references, so some referenced content may be unavailable or unreviewed.

Mitigation: Check the referenced files and confirm intended file access before installing.

Risk: The scan noted an undeclared tool scope and does not establish the skill's actual runtime permissions.

Mitigation: Review the permissions in the intended environment and grant only the access needed for the supplied materials and case files.

## Reference(s):

- [Procurement Admission Copilot on ClawHub](https://clawhub.ai/haiyangchenbj/skills/procurement-admission-copilot-skill)
- [Procurement Admission Qualification Checklist](artifact/references/qualification-checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Structured JSON readiness findings and Markdown supplier packages, readiness reports, or approval case dashboards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-only findings for a human procurement reviewer; no admission decision.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
