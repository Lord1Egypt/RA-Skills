## Description: <br>
Multi-agent trading debate framework for collective market decision-making when a trading signal is detected or a position decision is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w491623834-oss](https://clawhub.ai/user/w491623834-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trading teams and agent operators use this skill to coordinate structured market-decision debates across regime detection, analyst reports, bull and bear arguments, judge verdicts, and execution or hold decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-order execution instructions could be used without sufficient approval or safety controls. <br>
Mitigation: Use the skill only for analysis or paper trading unless a separate live-order approval process requires human confirmation, explicit account and environment labels, allowed assets, maximum order size, and slippage limits. <br>
Risk: Simulated or insufficient-data trading outputs could be mistaken for production-ready signals. <br>
Mitigation: Fail closed when outputs are simulated or data is insufficient, and require review before any live execution workflow consumes the decision. <br>


## Reference(s): <br>
- [Feishu Trading Debate Formats](references/feishu_format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/w491623834-oss/multi-agent-trading-debate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown debate prompts and verdict templates, JSON log-entry examples, and command-line script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market regime, trading signal, confidence score, position size, risk level, stop loss, and next review time.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
