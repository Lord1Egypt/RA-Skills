## Description: <br>
乐有家找房与小区查询：自然语言查11城二手房/租房、新房楼盘、学校及小区信息 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tandangfei](https://clawhub.ai/user/tandangfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search supported 乐有家 real-estate data for second-hand homes, rentals, new-home projects, schools, and communities, then summarize matching results for property-search conversations. <br>

### Deployment Geography for Use: <br>
China (coverage limited to 深圳, 中山, 东莞, 惠州, 广州, 佛山, 清远, 珠海, 江门, 长沙, and 南京). <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LYJ_API_KEY and sends property-search criteria to 乐有家 endpoints. <br>
Mitigation: Install only when the publisher and integration are trusted, scope prompts to the property search task, and do not include unrelated personal or confidential information. <br>
Risk: An API URL override could direct requests away from the intended 乐有家 service. <br>
Mitigation: Leave API URL overrides unset unless the destination is verified as the intended 乐有家 service. <br>
Risk: Search results may be incomplete, unavailable, or limited to the supported city list. <br>
Mitigation: Treat returned listings as lookup results, omit empty fields, and ask the user to adjust city, area, budget, or filters when no useful matches are returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tandangfei/lyj-house) <br>
- [Publisher profile](https://clawhub.ai/user/tandangfei) <br>
- [乐有家 homepage](https://www.leyoujia.com) <br>
- [乐有家 API key application site](https://shenzhen.leyoujia.com) <br>
- [House search endpoint](https://wap.leyoujia.com/wap/openclaw/ai/house/search) <br>
- [Community search endpoint](https://wap.leyoujia.com/wap/openclaw/ai/communitySearch) <br>
- [New home search endpoint](https://wap.leyoujia.com/wap/openclaw/ai/xfSearch) <br>
- [School search endpoint](https://wap.leyoujia.com/wap/openclaw/ai/schoolSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional inline curl commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LYJ_API_KEY and curl; returns concise property, community, school, or new-home summaries while suppressing raw API JSON.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
