## Description: <br>
Fetches daily news recommendations, personalizes ordering from user interests or query keywords, and generates a responsive H5 report page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxcoder1997](https://clawhub.ai/user/yxcoder1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch a daily news feed, sort it according to stated interests or available user profile context, and create a local HTML report for reading or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personalized sorting can use conversation context or stored profile memory, and generated local files may retain profile-derived interests or report contents. <br>
Mitigation: Ask the agent to use only preferences stated in the current request when appropriate, and review or delete data/sorted_ids.json and output/daily_report.html after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxcoder1997/jt-daily-report) <br>
- [News recommendation API endpoint](https://jiutian.10086.cn/jiujiuassist/proactive/get_user_news_recommend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON sorting data and a local HTML daily report, with shell commands and guidance for agent execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces data/sorted_ids.json and output/daily_report.html after fetching and sorting news data.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
