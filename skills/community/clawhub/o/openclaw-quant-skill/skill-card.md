## Description: <br>
Professional quantitative trading system for cryptocurrency - backtesting, paper trading, live trading, and strategy optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and trading-system builders use this skill to produce commands, code examples, configuration guidance, and analysis workflows for crypto strategy backtesting, paper trading, performance review, and explicitly confirmed live trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package mixes a crypto live-trading skill with an unrelated video-generation skill. <br>
Mitigation: Review the packaged files before installation and treat the unrelated video-generation file as out of scope until the publisher removes or separates it. <br>
Risk: The skill asks users to install and run external code that was not reviewed in the server evidence. <br>
Mitigation: Review the external repository and dependencies before executing commands, and pin or inspect the code used for any trading workflow. <br>
Risk: Live-trading commands can place real orders when exchange credentials are provided. <br>
Mitigation: Use backtesting and paper or testnet mode first, disable withdrawals on exchange keys, set tight limits, and require explicit confirmation before any live-trading command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/openclaw-quant-skill) <br>
- [Openclaw Quant project repository](https://github.com/ZhenRobotics/openclaw-quant) <br>
- [Openclaw Quant issues](https://github.com/ZhenRobotics/openclaw-quant/issues) <br>
- [Openclaw Quant discussions](https://github.com/ZhenRobotics/openclaw-quant/discussions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python, YAML, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading risk warnings and confirmation prompts for live-trading workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
