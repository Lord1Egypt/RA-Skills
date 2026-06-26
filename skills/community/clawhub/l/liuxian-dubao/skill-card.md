## Description: <br>
Helps agents use the Xiacai sports-prediction API to register users, browse matches, publish Da Liu Ren-style predictions, and review settled results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjbcctv-123](https://clawhub.ai/user/xjbcctv-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interact with the Xiacai service: managing account authentication, finding sports matches, submitting predictions, and checking prediction history and settlements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires XIACAI_API_KEY, which is a sensitive credential tied to a Xiacai account. <br>
Mitigation: Store XIACAI_API_KEY only in the environment, avoid exposing it in logs or shared transcripts, and rotate it if disclosure is suspected. <br>
Risk: The skill can register accounts, update profile data, and post predictions to a third-party service. <br>
Mitigation: Require user confirmation before registration, profile updates, or prediction submission, and show the intended request before execution. <br>
Risk: Sports predictions can be incorrect or interpreted as stronger guidance than the evidence supports. <br>
Mitigation: Present predictions as entertainment-oriented analysis, verify match status before posting, and avoid framing outputs as financial or betting advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjbcctv-123/liuxian-dubao) <br>
- [Xiacai API base endpoint](https://xiacai.coze.site/api/v1) <br>
- [Skill overview](SKILL.md) <br>
- [Authentication and account guide](认证.md) <br>
- [Match listing guide](赛事.md) <br>
- [Prediction workflow guide](预测.md) <br>
- [Results and settlement guide](战绩.md) <br>
- [Error handling guide](错误处理.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls to Xiacai endpoints using XIACAI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
