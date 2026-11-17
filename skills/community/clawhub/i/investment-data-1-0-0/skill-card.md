## Description:

Provides A-share investment data workflows for downloading datasets, querying daily prices, limit-up and limit-down data, index data, and adjusted price data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chayjan](https://clawhub.ai/user/chayjan)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, data analysts, and quantitative finance users use this skill to install and operate scripts for A-share market data download, query, export, and scheduled update workflows. Users should verify returned market data before using it for investment or financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal query path can return synthetic or placeholder financial data while presenting an investment-data workflow.

Mitigation: Do not use returned data for financial decisions until the implementation reads verified datasets and clearly reports data provenance.

Risk: The updater downloads and extracts remote archives without the security safeguards called out by the scan guidance.

Mitigation: Run downloads only in a contained directory, disable scheduled updates, and add archive integrity checks and safe extraction before production use.

Risk: The update flow depends on external network downloads and local subprocess execution.

Mitigation: Review commands before execution and restrict runtime permissions to the minimum directories and binaries needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chayjan/skills/investment-data-1-0-0)
- [Data Fields Reference](references/fields.md)
- [Original investment_data Project](https://github.com/chenditc/investment_data)
- [DoltHub investment_data Repository](https://www.dolthub.com/repositories/chenditc/investment_data)
- [Original Chinese Documentation](https://github.com/chenditc/investment_data/blob/master/docs/README-ch.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; exported data may be CSV, JSON, or Excel.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local dataset archives, extracted data directories, and exported data files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
