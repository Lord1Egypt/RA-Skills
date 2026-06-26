## Description: <br>
猫眼电影个性化推荐系统——每周抓取中国大陆新上映/即将上映电影，基于用户观影偏好档案智能排序推荐，推送飞书周报 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[advnljs](https://clawhub.ai/user/advnljs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to collect current and upcoming mainland China movie listings from Maoyan, compare them with a local viewing-preference profile, and generate a personalized weekly recommendation report for Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local viewing-preference profile can contain sensitive personal preference details. <br>
Mitigation: Review profile.json before use and avoid storing preferences you would not want included or inferred in generated reports. <br>
Risk: Recommendation reports sent through Feishu may expose preference data if delivered to the wrong destination. <br>
Mitigation: Verify the Feishu destination before enabling scheduled delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/advnljs/movie-rec-personal-cn) <br>
- [Publisher profile](https://clawhub.ai/user/advnljs) <br>
- [Maoyan now-showing API endpoint](https://m.maoyan.com/ajax/movieOnInfoList) <br>
- [Maoyan coming-soon API endpoint](https://m.maoyan.com/ajax/comingList?ci=10&token=&limit=100) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendation report, JSON movie data, and profile or cron configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local profile.json preference file and live Maoyan API responses; reports may be delivered through Feishu when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
