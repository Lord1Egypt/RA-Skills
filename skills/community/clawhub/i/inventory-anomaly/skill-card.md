## Description:

Generates a modular inventory anomaly detection and demand forecasting system that reads Excel inventory and order data, applies ARIMA forecasting and standard-deviation anomaly checks, and produces TXT replenishment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawvincent](https://clawhub.ai/user/openclawvincent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to scaffold a local inventory analysis project for spare-parts or retail stock monitoring. It helps create code for Excel-based data management, anomaly detection, demand forecasting, test data generation, and replenishment reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated project reads and writes local inventory spreadsheets and reports, so live operational data could be overwritten or exposed through local files if run without workspace controls.

Mitigation: Install only in a project workspace, use copies of real inventory spreadsheets, and review local data/ and output/ paths before operational use.

Risk: The dependency ranges are broad for normal data-science packages, which can make production behavior vary across environments.

Mitigation: Pin reviewed versions of pandas, numpy, statsmodels, and openpyxl before operational deployment.

Risk: The generated templates expect Chinese-language worksheet names, field labels, and reports by default.

Mitigation: Confirm sheet names, report labels, and downstream consumers before using the generated system in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawvincent/skills/inventory-anomaly)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code templates and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated projects use local Excel input files under data/ and write TXT reports under output/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
