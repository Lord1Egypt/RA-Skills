## Description: <br>
卖家之家(跨境电商)活动查询与发布 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators and agents use this skill to query MJZJ cross-border e-commerce activity listings and publish activities through MJZJ APIs when an MJZJ API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can upload files and publish business activities with the configured MJZJ API key. <br>
Mitigation: Require a final human confirmation that shows the exact activity title, organizer, city or address, times, images, registration fields, and destination account before upload or publication. <br>
Risk: The MJZJ API key could be exposed through chat, logs, URLs, or shared output. <br>
Mitigation: Keep MJZJ_API_KEY out of prompts and generated output, store it only in the skill configuration, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-activity) <br>
- [MJZJ activity page](https://mjzj.com/activity) <br>
- [MJZJ API key page](https://mjzj.com/user/agentapikey) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API endpoint guidance and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MJZJ_API_KEY for city lookup, image upload, and activity publishing; public activity query can run without a token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
