## Description:

A scenario-driven investment advisory workflow for market interpretation, event analysis, portfolio diagnosis, asset allocation, and behavioral coaching using four expert perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-advice agents use this skill to route common investment advisory requests into structured market analysis, portfolio review, asset allocation, and behavior-coaching reports. It is intended to support advisory workflows and does not replace licensed investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive financial profile details, holdings, amounts, age, and risk preferences.

Mitigation: Minimize inputs, redact account identifiers, IDs, bank-card numbers, and credentials, and avoid retaining unnecessary precise portfolio details.

Risk: The documented purpose does not justify broad Bash/Exec and file read/write access.

Mitigation: Run the skill in a sandbox and restrict command execution and file permissions before use.

Risk: Personalized allocation or trading suggestions may be unsuitable without complete KYC information or professional review.

Mitigation: Require risk profile, time horizon, amount, and other KYC inputs before allocation guidance, keep disclaimers visible, and review recommendations with a qualified professional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/investment-advisory-workflow)
- [Four Experts Framework](artifact/references/four-experts.md)
- [Six-Stage Capability Library](artifact/references/six-stages.md)
- [Shared Skills Reference](artifact/references/shared-skills.md)
- [Report Template](artifact/templates/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, analysis, files]

**Output Format:** [Markdown reports with structured tables, data-source labels, confidence notes, action guidance, and optional PNG cards.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require external market-data tools or MCP services; reports should include disclaimers and data freshness or data-missing notes.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact clawhub.yaml; SKILL.md frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
