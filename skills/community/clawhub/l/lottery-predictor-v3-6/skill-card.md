## Description: <br>
基于 V3.6 智能评分系统的双色球预测工具，8 项维度评分 + 金手指波动，≥4 球命中率 46.1%（1000 期回测） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mumuli2021](https://clawhub.ai/user/mumuli2021) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to generate offline 双色球 lottery number recommendations, inspect historical prediction records, and verify predictions against later draw results. The skill requires a local lottery SQLite database and is intended for entertainment reference rather than guaranteed outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package mixes V3.6 and V2.15 identities and includes unrelated publishing automation, which could confuse users or cause the wrong skill version to be run or published. <br>
Mitigation: Review the package before installation, verify which prediction script the platform will execute, and remove or ignore the V2.15 publishing scripts and publish guides. <br>
Risk: The skill reads a local lottery database for offline prediction. <br>
Mitigation: Install only when comfortable granting access to the local lottery database path and set LOTTERY_DB_PATH to the intended SQLite database. <br>
Risk: Publishing guides mention token-based ClawHub workflows that could expose credentials if copied into a shell environment without care. <br>
Mitigation: Do not place ClawHub tokens into shell environments from the included docs unless the exposure risk is understood and the environment is trusted. <br>
Risk: Lottery predictions can be mistaken for reliable financial or gambling advice. <br>
Mitigation: Treat outputs as entertainment reference only; the artifact itself states that lottery outcomes are random and that historical patterns do not guarantee future results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mumuli2021/lottery-predictor-v3-6) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON-style prediction reports with ranked numbers, recommended combinations, backtest statistics, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, SQLite3, and LOTTERY_DB_PATH for the local lottery database.] <br>

## Skill Version(s): <br>
3.6.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
