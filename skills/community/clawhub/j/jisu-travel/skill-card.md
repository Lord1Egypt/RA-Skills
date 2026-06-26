## Description: <br>
聚合航班列表、景点信息，火车段可走 train 能力。当用户说：查一下上海到东京的航班、杭州有什么景点推荐、顺带帮我看看火车票，或类似出行规划问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve travel-planning data for flights, scenic spots, and train routes or ticket availability. It is suited for agent workflows that need structured travel search results and provider links for Chinese-language travel planning requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel search details are sent to ly.com and JisuAPI during normal operation. <br>
Mitigation: Use only when sharing those itinerary details with the listed providers is acceptable. <br>
Risk: Train lookups require a JISU_API_KEY and may consume quota or incur billing. <br>
Mitigation: Use a dedicated API key where possible and monitor quota or billing in the JisuAPI account. <br>
Risk: Python dependencies are required to run the skill. <br>
Mitigation: Install requests and beautifulsoup4 in a virtual environment before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-travel) <br>
- [Publisher profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI train API](https://www.jisuapi.com/api/train/) <br>
- [LY.com travel provider](https://www.ly.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON printed to stdout, with markdown usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; train commands require JISU_API_KEY and send travel query details to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
