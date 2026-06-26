## Description: <br>
Gets daily and historical Hong Kong stock short selling data from HKEX and ETNet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KadinXu](https://clawhub.ai/user/KadinXu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve public Hong Kong short-selling data for selected stock codes, rankings, and local CSV history tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network requests to HKEX and ETNet reveal the stock codes and pages queried from the runtime environment. <br>
Mitigation: Use the skill only where outbound requests to those public market-data sites are acceptable, and review requested symbols before execution. <br>
Risk: Collection and history features may store fetched public market data as local CSV files. <br>
Mitigation: Run in a controlled Python virtual environment and choose or clean the local data directory according to retention needs. <br>
Risk: Market-data freshness and availability depend on HKEX and ETNet publishing schedules and page structure. <br>
Mitigation: Check returned dates and source availability before relying on results for analysis or workflow decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/KadinXu/hk-stock-short-selling) <br>
- [HKEX short selling statistics](https://www.hkex.com.hk/chi/stat/smstat/) <br>
- [ETNet](https://www.etnet.com.hk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime scripts may produce terminal tables, pandas DataFrames, and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public HKEX and ETNet market-data pages and may save fetched data under a local CSV data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
