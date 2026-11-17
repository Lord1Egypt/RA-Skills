## Description:

Halo guides agents through data-locked A-share fundamental analysis reports, using local data-fetching scripts and AI-authored analysis slots to reduce unsupported financial claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lululu811](https://clawhub.ai/user/lululu811)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to produce structured A-share stock analysis reports from fetched market, financial, news, and qualitative data. The skill is designed to keep source data locked in generated report skeletons while the agent fills only the analysis sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow expects local Python scripts and market/news data fetching, which can introduce risk if those scripts or data sources are not trusted.

Mitigation: Use the skill only in a trusted workspace, review referenced scripts before execution, and apply normal network and credential controls.

Risk: Generated investment-style reports may be read as financial advice.

Mitigation: Treat outputs as informational analysis, require human review, and preserve the report disclaimer and validity period.

Risk: Missing or failed data sources can lead to incomplete analysis.

Mitigation: Follow the skill's missing-data rules: label unavailable data, stop when core financial data is absent, and do not estimate or fabricate missing values.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/lululu811/halo-skill)
- [ClawHub skill page](https://clawhub.ai/lululu811/skills/halo-skill)
- [a-stock-data optional integration](https://github.com/simonlin1212/a-stock-data)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown reports with inline shell commands and structured analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report files from locally generated JSON data and instructs the agent to preserve locked data fields.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
