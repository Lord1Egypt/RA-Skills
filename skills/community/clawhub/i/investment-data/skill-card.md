## Description:

获取高质量 A 股投资数据，基于 investment_data 项目。支持日终价格、涨跌停数据、指数数据等。每日更新，多数据源交叉验证。触发词：股票数据、A股数据、金融数据、量化数据、历史行情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanleychanh](https://clawhub.ai/user/stanleychanh)

### License/Terms of Use:

Apache License 2.0

## Use Case:

Developers, data engineers, and quantitative research users can use this skill to download, query, and export A-share end-of-day prices, limit-up/limit-down data, index data, and related field definitions. Query output should be reviewed before investment analysis because the security evidence reports placeholder data behavior in core query paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Core query paths may return placeholder or generated data while presenting results as investment data.

Mitigation: Do not use query output for investment analysis until the data client is fixed to read verified real datasets and clearly label data provenance.

Risk: The downloader retrieves and extracts remote archives without archive integrity checks or safe extraction controls.

Mitigation: Avoid downloader and auto-update workflows until integrity verification and safe extraction are added; run downloads with least privilege in a controlled output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanleychanh/skills/investment-data)
- [Data fields reference](references/fields.md)
- [Usage examples](examples/usage_examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime scripts can print tabular text or export CSV, JSON, and Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, wget, tar, and Python packages including pandas, numpy, requests, pyyaml, and openpyxl; data workflows may require network access and local storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
