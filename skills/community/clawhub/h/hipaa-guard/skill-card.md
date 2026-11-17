## Description:

HIPAA Guard is a local pre-publication checker that scans healthcare product copy, privacy policies, and product descriptions for HIPAA-triggering or medical privacy risk terms and returns risk-ranked findings with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and compliance reviewers use this skill before publishing United States healthcare product content to flag wording about PHI handling, missing BAA coverage, unencrypted PHI, third-party PHI disclosure, breach notification gaps, or patient access restrictions. It is a lightweight screening aid and not a legal compliance determination.

### Deployment Geography for Use:

Global, with subject matter focused on United States HIPAA obligations.

## Known Risks and Mitigations:

Risk: The checker uses fixed terms and may miss HIPAA issues or produce false positives.

Mitigation: Use it as a pre-publication screening aid, then review flagged content with qualified compliance or legal counsel for material releases.

Risk: The tool output is not a legal compliance determination.

Mitigation: Do not treat clean results as proof of HIPAA compliance; supplement with a full compliance review or audit when handling PHI.

Risk: Most documentation and output are Chinese, which can affect review by English-only teams.

Mitigation: Have bilingual reviewers validate findings and remediation text before relying on the output in a production workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wwumit/skills/hipaa-guard)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text reports or structured JSON findings from a local command-line checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the highest risk level, finding count, matched terms, categories, source positions, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG released 2026-08-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
