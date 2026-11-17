## Description:

Helps agents build Python workflows for private fund portfolio analysis from XLS/XLSX valuation statements, covering market-neutral futures hedges, index-enhanced benchmark comparisons, holdings enrichment, and visual reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoerdata](https://clawhub.ai/user/xiaoerdata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial analysts use this skill to generate or refine Python analysis scripts that parse private fund valuation spreadsheets, enrich holdings with market, industry, and index data, and produce portfolio analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published guidance includes hardcoded MySQL connection defaults that could expose or unintentionally use database credentials.

Mitigation: Remove hardcoded database defaults, rotate any exposed credential, and provide secrets only through protected environment variables or a secrets manager.

Risk: Database-backed enrichment can access private or licensed financial data.

Mitigation: Use only authorized, least-privilege database access and verify that any generated script connects to approved data sources.

Risk: Generated CSV, JSON, and PNG reports may contain sensitive private-fund holdings and portfolio information.

Mitigation: Treat generated reports as sensitive financial files and store or share them only through access-controlled channels.

## Reference(s):

- [XLS Structure Reference](references/xls_structure.md)
- [Data Sources Reference](references/data_sources.md)
- [Analysis Script Prompt Generator](scripts/generate_analysis_script_prompt.py)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce CSV, JSON, and PNG analysis artifacts from private fund valuation data.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
