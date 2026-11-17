## Description:

基于 V2.15 数学模型的双色球预测工具，包含均值回归、正态分布、大数定律、卡方检验等 7 种算法，提供红球 TOP10 和蓝球 TOP4 推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mumuli2021](https://clawhub.ai/user/mumuli2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run local SQLite-based双色球 lottery analysis, generate ranked red and blue ball recommendations, and verify predictions after results are known. Outputs should be treated as entertainment and analysis support, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lottery recommendations may be mistaken for reliable financial or gambling advice.

Mitigation: Present predictions as entertainment only, preserve the skill disclaimer, and require users to make independent purchasing decisions.

Risk: The package includes ClawHub publishing automation that can publish from a user account when run with credentials.

Mitigation: Do not run auto_publish.sh or provide ClawHub tokens unless intentionally publishing; remove publishing files from installed runtime packages when possible.

Risk: The security summary flags weak database input handling around the lottery selector.

Mitigation: Use a dedicated, non-sensitive lottery SQLite database and allowlist supported lottery table names before broad deployment.

Risk: The skill depends on local SQLite data freshness and correctness.

Mitigation: Keep LOTTERY_DB_PATH pointed at a maintained lottery database and disclose the latest source issue used for any prediction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mumuli2021/skills/lottery-predictor-v2-15)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Test report](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON prediction records or human-readable text/Markdown with ranked lottery recommendations, combinations, analysis, and validation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, sqlite3, and LOTTERY_DB_PATH for local SQLite lottery data; package declares no network permission.]

## Skill Version(s):

2.15.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
