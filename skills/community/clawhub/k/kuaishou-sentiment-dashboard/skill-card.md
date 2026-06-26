## Description: <br>
快手短视频运营增长助手适合内容创作者、运营、品牌方、电商在用户提供了快手内容链接时使用，帮助基于输入材料生成情绪、画像和讨论焦点、舆情与转化线索、优化建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, brand teams, and e-commerce teams use this skill to analyze Kuaishou video comments from a provided link. It returns sentiment, audience and discussion insights, public-opinion and conversion signals, and operational recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key for the AI Skills service. <br>
Mitigation: Store AISKILLS_API_KEY locally in the environment and do not paste it into chat or shared prompts. <br>
Risk: Kuaishou links and related metadata are sent to the configured API provider for analysis. <br>
Mitigation: Invoke the skill only for links and metadata that may be shared with that provider, and use explicit invocation for sensitive conversations. <br>
Risk: The skill returns operational sentiment and conversion guidance that may be incomplete or misleading if the source comments are unrepresentative. <br>
Mitigation: Review the generated insights against the original content, business context, and any available first-party analytics before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/kuaishou-sentiment-dashboard) <br>
- [AI Skills](https://ai-skills.ai) <br>
- [form-schema.json](references/form-schema.json) <br>
- [skill.json](references/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISKILLS_API_KEY and a Kuaishou video link or work ID; the runner polls until the comment-analysis task completes or times out.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
