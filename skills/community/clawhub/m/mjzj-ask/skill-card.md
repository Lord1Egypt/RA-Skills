## Description: <br>
卖家之家(跨境电商)问答搜索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search MJZJ Q&A content, list question categories, retrieve the user's own posted questions, and post new MJZJ questions through the supported API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the MJZJ_API_KEY credential for private actions, including posting questions and querying the user's own questions. <br>
Mitigation: Install only when the agent should access MJZJ Q&A with the user's API key, and keep the credential scoped to this intended use. <br>
Risk: Although labeled as search, the skill can post authenticated questions and includes money-related fields such as bountyMoney and watchMoney. <br>
Mitigation: Require explicit user confirmation of title, content, categories, anonymity, deadline, images, bountyMoney, and watchMoney before any question is posted. <br>
Risk: Large snowflake identifiers can lose precision if handled as numbers. <br>
Mitigation: Pass and preserve all ID-like fields as strings, including id, categoryIds, position, and nextPosition. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-ask) <br>
- [MJZJ Ask](https://mjzj.com/ask) <br>
- [MJZJ API key page](https://mjzj.com/user/agentapikey) <br>
- [MJZJ manual question form](https://mjzj.com/ask/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MJZJ question links and business error messages returned by the API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
