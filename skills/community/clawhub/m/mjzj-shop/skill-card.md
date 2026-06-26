## Description: <br>
卖家之家(跨境电商)全球开店平台查询 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search cross-border e-commerce shop-opening platforms by platform name and retrieve the MJZJ platform list through the queryPlatform API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release metadata declares MJZJ_API_KEY as a sensitive credential requirement. <br>
Mitigation: Configure MJZJ_API_KEY only when needed and avoid exposing it in prompts, logs, or examples. <br>
Risk: Large snowflake-style identifiers can lose precision if treated as numbers. <br>
Mitigation: Preserve id, regionId, and similar identifiers as strings when passing through API results. <br>
Risk: The API may fail or return unavailable results. <br>
Mitigation: Tell the user to retry later and do not substitute web search for the documented MJZJ API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-shop) <br>
- [MJZJ global shop platform page](https://mjzj.com/gongxu) <br>
- [MJZJ queryPlatform API example](https://data.mjzj.com/api/global/queryPlatform?keywords=amazon) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API endpoint guidance and inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserve id and regionId values as strings to avoid precision loss.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
