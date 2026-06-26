## Description: <br>
基于 V2.15 数学模型的双色球预测工具，包含均值回归、正态分布、大数定律、卡方检验等 7 种算法，提供红球 TOP10 和蓝球 TOP4 推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mumuli2021](https://clawhub.ai/user/mumuli2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and lottery-analysis users use this skill to run local 双色球 predictions from a SQLite history database, review red-ball and blue-ball recommendations, and verify prior predictions after results are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrelated publishing automation is included and could publish with a user's ClawHub account if run with credentials. <br>
Mitigation: Do not run auto_publish.sh or set CLAWHUB_TOKEN for this package unless deliberately publishing from your own account. <br>
Risk: The predictor reads from a local SQLite database path supplied through LOTTERY_DB_PATH. <br>
Mitigation: Point LOTTERY_DB_PATH only at a dedicated lottery-history database, not personal or unrelated SQLite files. <br>
Risk: Lottery predictions can be mistaken for reliable financial guidance. <br>
Mitigation: Treat generated predictions as entertainment and do not rely on them for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mumuli2021/lottery-predictor-v2-15) <br>
- [Publisher profile](https://clawhub.ai/user/mumuli2021) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, analysis, guidance] <br>
**Output Format:** [JSON or plain-text prediction reports with ranked number recommendations and verification results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SQLite lottery-history database through LOTTERY_DB_PATH; no network access is needed for prediction.] <br>

## Skill Version(s): <br>
2.15.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
