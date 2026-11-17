## Description:

Monitors official Vietnam NSO monthly and quarterly socio-economic releases and compares same-period trends; used when users request official macro updates and year-over-year context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to retrieve official Vietnam NSO macroeconomic releases, compare current data with the same period in the prior year, and summarize sector implications for Vietnam equities with confidence and data-gap notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses web access to read official NSO pages and linked PDFs.

Mitigation: Confirm web access is acceptable before installation and require canonical NSO URLs over reposted summaries.

Risk: PDF or report extraction failures can leave indicator coverage incomplete.

Mitigation: Attempt both the summary page and report or PDF, list missing GDP/CPI/IIP/trade/retail/FDI/credit blocks, and downgrade confidence when data is incomplete.

Risk: Sector implications for Vietnam equities are interpretive and could be mistaken for financial advice.

Mitigation: Label NSO-derived statements as facts, label sector mappings as inferences, cite URLs for key claims, and avoid absolute buy or sell instructions.

## Reference(s):

- [Vietnam NSO Monthly Socio-Economic Reports](https://www.nso.gov.vn/bao-cao-tinh-hinh-kinh-te-xa-hoi-hang-thang)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with metadata, indicator tables, sector implications, confidence notes, data gaps, and cited URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes release date, extraction timestamp in ICT (UTC+7), completed and missing indicator blocks, and fact-versus-inference labeling.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
