## Description: <br>
Helps users use a rebate assistant for authorization and tutorials, Taobao/JD/Pinduoduo product-link rebates, product search, balance checks, and withdrawal flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfile](https://clawhub.ai/user/skyfile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to learn and authorize the rebate workflow, submit supported shopping links, search for products, and manage rebate balance or withdrawal actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local AI model API credentials and send raw shopping messages to the configured model provider. <br>
Mitigation: Install only if the publisher and configured model provider are trusted, and avoid sending sensitive personal or financial details in shopping requests. <br>
Risk: The rebate workflow sends product links, openId, balance, and withdrawal data to an external rebate backend. <br>
Mitigation: Review and accept the rebate backend and withdrawal flow before installation; confirm withdrawal actions before submitting them. <br>
Risk: The security verdict is suspicious because the skill handles account balance and withdrawal flows. <br>
Mitigation: Review the skill before deployment and scan updates before enabling new releases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skyfile/pdd-rebate) <br>
- [Rebate service endpoint](https://rebate-skill.io.mlj130.com) <br>
- [WeChat authorization page](https://xiaomaxiangshenghuo.io.mlj130.com/authlogin.html) <br>
- [Official account follow page](https://xiaomaxiangshenghuo.io.mlj130.com/follow.html) <br>
- [Rebate details page](https://xiaomaxiangshenghuo.io.mlj130.com/rebate-details.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown user responses with JSON diagnostics from command-line scripts when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes S01 authorization/tutorial, S02 link rebate, and S03 product search workflows; script stdout is intended to be returned directly.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
