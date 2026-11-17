## Description:

Compare health insurance plans, estimate total yearly costs, and choose coverage that fits medical usage, prescriptions, and financial risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to compare health insurance options, model low, expected, and high-use annual costs, and choose a coverage strategy that fits provider access, prescriptions, budget, and downside risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive insurance information may be retained locally if the user approves broad memory or artifact storage.

Mitigation: Ask for explicit approval before writing to local health-insurance memory, retain only durable decision context, and redact policy numbers, government IDs, payment details, and unnecessary personal information.

Risk: Plan recommendations may be unreliable if provider networks, formularies, deadlines, plan IDs, or enrollment confirmations are stale or unverified.

Mitigation: Confirm plan details against official insurer, employer, marketplace, or broker evidence before enrollment, preserve confirmation artifacts, and do not claim enrollment is complete without confirmation evidence.

## Reference(s):

- [Health Insurance ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/health-insurance)
- [Health Insurance Homepage](https://clawic.com/skills/health-insurance)
- [Setup Guide](artifact/setup.md)
- [Coverage Framework](artifact/coverage-framework.md)
- [Cost Model](artifact/cost-model.md)
- [Comparison Checklist](artifact/comparison-checklist.md)
- [Enrollment Playbook](artifact/enrollment-playbook.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional shell command blocks and structured comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; no external network requests; optional local memory requires explicit approval.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
