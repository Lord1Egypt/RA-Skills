## Description: <br>
实时诊断持仓，结合腾讯行情和技术指标，计算买卖评分、状态、操作信号和盈亏情况。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayden-zhong](https://clawhub.ai/user/jayden-zhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors or agents maintaining a local holdings list use this skill to fetch current market data, score portfolio positions, and produce concise hold, warning, sell, pass, or fail diagnostics. Its outputs are portfolio analysis aids and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and executes holdings data and imports modules from a hard-coded external workspace path. <br>
Mitigation: Install and run it only in a private, trusted workspace where untrusted users or tools cannot edit the referenced holdings file or imported modules. <br>
Risk: Portfolio symbols and analysis inputs may be transmitted to Tencent market-data endpoints and analysis results may be saved locally. <br>
Mitigation: Use only holdings data appropriate for external market-data requests, and review local output files for sensitive portfolio details before sharing. <br>
Risk: The generated scores and sell or hold signals can be mistaken for investment advice. <br>
Mitigation: Treat outputs as diagnostic signals for review, not as authoritative financial recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayden-zhong/holdings-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jayden-zhong) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Console text and local JSON files with stock scores, signals, status labels, profit/loss metrics, and summary statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces portfolio diagnostics from local holdings data and external market-data responses.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
