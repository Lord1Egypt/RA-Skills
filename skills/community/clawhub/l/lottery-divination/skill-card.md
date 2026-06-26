## Description: <br>
彩票测算器 uses the current time to generate Meihua Yishu divination details and recommended numbers for 双色球 (ssq) or 大乐透 (dlt), with an entertainment-only lottery disclaimer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eamonnn101](https://clawhub.ai/user/Eamonnn101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for Chinese-language entertainment lottery number generation. The agent asks for the lottery type when needed, runs the local divination script, and returns formatted numbers with a clear disclaimer that lottery results are random and spending should remain minimal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat generated lottery numbers as financial advice or predictive guidance. <br>
Mitigation: Present the output as entertainment only, include the lottery disclaimer every time, and retain the suggested low spending limit. <br>
Risk: Broad trigger wording may activate the skill for vague requests to calculate a number. <br>
Mitigation: Confirm that the user wants lottery number generation and ask whether they want ssq or dlt when the lottery type is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Eamonnn101/lottery-divination) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Chinese Markdown-style response; the helper script emits JSON for the agent to format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes lottery numbers, divination details, an entertainment-only disclaimer, and a suggested low spending limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
