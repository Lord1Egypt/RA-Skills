## Description:

排列五数字彩票分析工具，提供数据分析、选号策略、概率计算、冷热号分析等辅助功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents can use this skill to review Pai Lie Wu lottery rules, generate entertainment-only number selections, and run helper analyses such as hot/cold, difference, probability, and simple return calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes lottery-prediction and accuracy claims that can mislead users about a random event.

Mitigation: Present lottery outputs as entertainment and probability education only, and remove or clearly relabel unsupported prediction and accuracy claims before use.

Risk: The calculator accepts untrusted numeric input, which the security evidence flags as unsafe until validation is added.

Mitigation: Use the calculator only with trusted inputs or add strict numeric validation for amount and price before evaluating expressions.

Risk: The skill requests a network-capable web_search permission that the security evidence identifies as unnecessary.

Mitigation: Remove the web_search permission unless a reviewed live-data workflow is added and documented.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance and terminal text from Bash helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some analysis outputs are static or simulated; random selections are entertainment-only and do not predict lottery outcomes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
