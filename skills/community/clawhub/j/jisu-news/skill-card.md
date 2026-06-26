## Description: <br>
按频道获取头条、财经、体育、娱乐等新闻列表，可查频道列表。当用户说：今天财经头条有什么？体育新闻摘要，或类似新闻聚合问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve JisuAPI news channels and fetch current news lists for channels such as headlines, finance, sports, entertainment, technology, and health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News queries are sent to the third-party JisuAPI service. <br>
Mitigation: Use specific news requests and avoid sending private, sensitive, or unrelated prompts through the skill. <br>
Risk: The skill requires a JISU_API_KEY for API access. <br>
Mitigation: Store the key in the environment, avoid exposing it in prompts or logs, and rotate it if it may have been disclosed. <br>
Risk: Returned news content comes from external internet sources and may have separate copyright or usage terms. <br>
Mitigation: Review source links and publisher terms before redistributing content; summarize and cite source URLs where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-news) <br>
- [JisuAPI News API documentation](https://www.jisuapi.com/api/news/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>
- [Publisher profile](https://clawhub.ai/user/jisuapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; returns channel lists or news result objects from JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
