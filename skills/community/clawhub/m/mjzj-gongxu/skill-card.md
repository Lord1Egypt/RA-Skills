## Description: <br>
卖家之家(跨境电商)供需搜索与发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and cross-border ecommerce operators use this skill to search MJZJ supply-and-demand metadata, publish posts, and manage their own posts through MJZJ APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, refresh, and delete MJZJ account content when given a valid MJZJ_API_KEY. <br>
Mitigation: Use it only with an intended MJZJ account token and confirm the exact post before deletion or refresh. <br>
Risk: An expired, missing, or reset API key prevents authenticated account actions. <br>
Mitigation: Refresh the token from the MJZJ API key page and reconfigure MJZJ_API_KEY before retrying. <br>
Risk: Business rules such as quotas, refresh frequency, content review, and tag limits can block publishing or refreshing. <br>
Mitigation: Surface MJZJ business error messages to the user and use the manual publish page when automated publishing fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-gongxu) <br>
- [MJZJ supply and demand homepage](https://mjzj.com/gongxu) <br>
- [MJZJ API key page](https://mjzj.com/user/agentapikey) <br>
- [MJZJ manual publish page](https://mjzj.com/gongxu/publish) <br>
- [Get official tags API](https://data.mjzj.com/api/supplydemand/getOfficialTags) <br>
- [Get platforms API](https://data.mjzj.com/api/supplydemand/getPlatforms) <br>
- [Get regions API](https://data.mjzj.com/api/supplydemand/getRegions) <br>
- [Create supply-demand post API](https://data.mjzj.com/api/supplydemand/createinfo) <br>
- [Query my posts API](https://data.mjzj.com/api/supplydemand/querymyinfos?size=20&position=) <br>
- [Refresh post API](https://data.mjzj.com/api/supplydemand/refreshinfo) <br>
- [Delete post API](https://data.mjzj.com/api/supplydemand/deleteinfo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MJZJ_API_KEY for authenticated account actions; public metadata endpoints can be used without a token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
