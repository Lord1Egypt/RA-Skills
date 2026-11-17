## Description:

Gets daily and historical Hong Kong stock short selling data from HKEX and ETNet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadinxu](https://clawhub.ai/user/kadinxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market-data analysts use this skill to retrieve Hong Kong short-selling data for individual stocks, rankings, and local historical tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts HKEX and ETNet during data retrieval.

Mitigation: Review network access expectations before installation or execution.

Risk: History-saving functions and collection scripts can create or update local CSV files.

Mitigation: Run the skill in an approved workspace and monitor local market-data cache paths.

Risk: Documented examples may need import-path fixes.

Mitigation: Test the command-line and Python examples in the target agent environment before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadinxu/skills/hk-stock-short-selling)
- [HKEX short selling statistics](https://www.hkex.com.hk/chi/stat/smstat/)
- [ETNet](https://www.etnet.com.hk/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime helpers produce tabular pandas DataFrames and CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact HKEX and ETNet and may create or update local CSV market-data caches when history-saving functions or collection scripts are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
