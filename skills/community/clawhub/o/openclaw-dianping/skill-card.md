## Description: <br>
查询大众点评餐厅信息，包括餐厅评分、人均消费、地址、菜系或区域推荐，以及附近美食推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newaiguy](https://clawhub.ai/user/newaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to guide an agent through browser-based Dianping restaurant lookup workflows, including searches by restaurant name, cuisine, city, and area. The skill helps collect restaurant cards with ratings, average spend, address, highlights, recommended dishes, and review summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require use of an authenticated Dianping browser session, including phone or SMS verification if the user is not logged in. <br>
Mitigation: Only enter a phone number or SMS verification code when you intentionally want the agent to use that Dianping account for the lookup. <br>
Risk: Restaurant search results can depend on city URL, city ID, account location, and dynamically loaded page content. <br>
Mitigation: Use the city-specific Dianping URL or explicit city search terms, then review extracted restaurant details against the visible page before relying on them. <br>


## Reference(s): <br>
- [OpenClaw大众点评 ClawHub release](https://clawhub.ai/newaiguy/openclaw-dianping) <br>
- [Dianping Hangzhou](https://www.dianping.com/hangzhou) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown or plain text restaurant lookup results and browser workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
