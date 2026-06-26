## Description: <br>
Collects and analyzes OKX exchange tick data and historical K-line market data, with strategy-oriented collection recommendations and storage estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading engineers use this skill to plan and run OKX public market-data collection for backtesting, research, and local storage workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts OKX public market-data endpoints and writes local data files that can grow large for long ranges or many symbols. <br>
Mitigation: Review requested symbols, intervals, date ranges, and output paths before execution; monitor disk usage during collection. <br>
Risk: Related cloud-upload workflows are referenced but not implemented by this skill. <br>
Mitigation: Review any separate uploader or Tencent COS skill independently before providing cloud credentials. <br>


## Reference(s): <br>
- [OKX API Documentation](https://www.okx.com/docs-v5/en/) <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/okx-data-collector) <br>
- [OKX_DATA_ANALYSIS.md](OKX_DATA_ANALYSIS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, Python code, JSON data, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON and CSV market-data files whose size grows with symbol count, interval, and date range.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
