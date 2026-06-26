## Description: <br>
Scores Chinese A-share short-term momentum candidates across theme strength, recent limit-up behavior, opening move, turnover, market sentiment, and board streaks to produce ranked stock-screening reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martinyan623](https://clawhub.ai/user/martinyan623) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate informational A-share short-term stock-screening reports and review ranked Top20 candidates after market close. The output is market analysis and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-screening outputs may be interpreted as investment advice or may be wrong because market data can be delayed, incomplete, or stale. <br>
Mitigation: Treat outputs as informational market analysis, verify against official market sources, and apply independent review before making trading decisions. <br>
Risk: The skill depends on AkShare and pandas and fetches public market data during execution. <br>
Mitigation: Install dependencies in an isolated environment and review package and data-source behavior before operational use. <br>
Risk: The artifact describes recurring after-close report generation and push behavior. <br>
Mitigation: Confirm or disable any separate scheduled push configuration before relying on recurring reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/martinyan623/niu-yao-stock-picker) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with ranked tables and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes reports/niu_yao_v1_YYYYMMDD.md when run in the expected workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
