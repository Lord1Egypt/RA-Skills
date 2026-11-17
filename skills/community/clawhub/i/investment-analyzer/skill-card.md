## Description:

Investment analysis for properties and ETFs. BUY/PASS/INVESTIGATE verdicts backed by data. Scans Centris for listings, advises DCA allocation. Triggers: analyze property, ETF, scan Centris, 定投, DCA, 投资房, compare real estate vs ETF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clairproqc-star](https://clawhub.ai/user/clairproqc-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze rental properties, ETFs, real estate-versus-ETF allocation choices, property scans, and DCA allocations with metric tables and investment verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes plaintext personal financial, property, mortgage, ownership, and cloud document metadata.

Mitigation: Remove or replace personal data with placeholders before sharing or installing the skill, and restrict package access to intended users.

Risk: The package declares GEMINI_API_KEY even though the advertised workflows are local investment analysis scripts.

Mitigation: Verify whether the credential is needed and avoid granting unrelated API keys during installation or execution.

Risk: Python dependencies and live data sources can affect results or create execution risk.

Mitigation: Install dependencies from a trusted pinned environment and review network-dependent outputs before relying on them.

Risk: Investment, tax, mortgage, and property conclusions may be incomplete or misleading if treated as professional advice.

Mitigation: Use outputs as rough analysis only and confirm decisions with current source data and qualified financial, tax, or legal professionals.

## Reference(s):

- [Investment Decision Criteria](references/criteria.md)
- [Current Investment Portfolio](references/portfolio.md)
- [Personal Financial Profile](references/profile.md)
- [Centris](https://www.centris.ca)
- [ClawHub Skill Page](https://clawhub.ai/clairproqc-star/skills/investment-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with key metric tables, short summaries, and BUY / INVESTIGATE / PASS verdicts; helper scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts for property analysis, ETF analysis, allocation comparison, property scanning, and DCA allocation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
