## Description: <br>
7-day weather forecast query powered by Alibaba Cloud IQS web search and page reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijian-github-20190615](https://clawhub.ai/user/lijian-github-20190615) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query 7-day weather forecasts for a city through Alibaba Cloud IQS search and page-reading APIs. It can return structured weather JSON for known sites or raw page text for agent interpretation when a site-specific parser is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Alibaba Cloud IQS API key. <br>
Mitigation: Store the key in a secret manager or restricted environment variable and avoid committing it to source control. <br>
Risk: Raw weather page text can be untrusted input and may be used to suggest parser changes. <br>
Mitigation: Treat raw page content as untrusted, review proposed parser changes manually, and scan the skill before deployment. <br>
Risk: Automatic parser edits after external page reads could introduce incorrect behavior. <br>
Mitigation: Keep the skill from making automatic code edits and require review before accepting parser updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijian-github-20190615/iqs-weather) <br>
- [Alibaba Cloud IQS Search Skill](https://skills.aliyun.com/skills/alibabacloud-iqs-search) <br>
- [Alibaba Cloud IQS API key documentation](https://help.aliyun.com/zh/document_detail/3025781.html) <br>
- [Alibaba Cloud IQS UnifiedSearch documentation](https://help.aliyun.com/zh/document_detail/2883041.html) <br>
- [Alibaba Cloud IQS ReadPageScrape documentation](https://help.aliyun.com/zh/document_detail/2983380.html) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON weather result data with command-line status and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIYUN_IQS_API_KEY and Node.js 18 or newer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
