## Description: <br>
Jiimore Niche Review helps agents query Jiimore-powered Amazon niche review data and summarize consumer sentiment, pain points, and review themes for US, JP, or DE marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, e-commerce operators, and market researchers use this skill through an agent to retrieve niche-level Amazon review topics, sentiment, mention percentages, and examples for product research and improvement decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write full API responses outside the documented workspace fallback path. <br>
Mitigation: Review the configured output directory and avoid running the skill with confidential product research or customer data unless that storage location is acceptable. <br>
Risk: The skill can send automatic feedback content to a separate service without asking first. <br>
Mitigation: Review feedback behavior before installation and disable or avoid use where user comments, customer data, or proprietary research should not be reported externally. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-jiimore-get-niche-review-from-keyword) <br>
- [API reference](references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [LinkFox authorization guide](https://skill.linkfox.com/linkfoxskills/guide.htm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, files, markdown] <br>
**Output Format:** [Markdown guidance with JSON API parameters, command examples, and summarized or full JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can cache identical requests for 24 hours and writes full API responses to a LinkFox session data directory while printing summaries for larger responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
