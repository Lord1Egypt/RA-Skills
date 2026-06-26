## Description: <br>
每日中午12点自动推送新闻午报到QQ和飞书，包含全球热点、科技动态、财经要闻 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a scheduled noon news digest that generates global, technology, and finance summaries and posts them to Feishu, with QQ delivery represented as a cron-integrated channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill posts generated digest content to a configured Feishu webhook and may expose information to that destination. <br>
Mitigation: Treat the Feishu webhook as a secret, install only when this delivery path is acceptable, and review posted content before relying on it. <br>
Risk: The security summary notes that QQ delivery and live news fetching are not fully implemented by the script. <br>
Mitigation: Do not assume QQ delivery or live news fetching works unless the script is updated and verified in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/news-noon-digest) <br>
- [World Monitor](https://www.worldmonitor.app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text news digest with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Feishu webhook environment variable for Feishu delivery; QQ delivery is described as cron-integrated rather than directly implemented by the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
