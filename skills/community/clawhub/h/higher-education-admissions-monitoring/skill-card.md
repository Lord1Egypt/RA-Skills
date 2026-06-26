## Description: <br>
监控指定高校的研究生招生通知，自动爬取最新信息并生成报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sixadd1](https://clawhub.ai/user/sixadd1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students, applicants, and developers use this skill to query configured university admissions pages, collect recent graduate admissions notices, and optionally save the results as Markdown or Word reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cron scheduling is under-explained. <br>
Mitigation: Require the exact cron command and the matching removal command before enabling scheduled monitoring. <br>
Risk: QQ report sending is under-explained and may transmit generated reports outside the local environment. <br>
Mitigation: Keep reports local unless the user explicitly chooses a QQ recipient and approves sending. <br>
Risk: Admissions scraping can return incomplete or stale results when sites use dynamic pages, change structure, block requests, or omit dates. <br>
Mitigation: Manually verify important admissions notices against the linked university source pages before acting on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sixadd1/higher-education-admissions-monitoring) <br>
- [常见问题 FAQ](artifact/references/常见问题FAQ.md) <br>
- [运行效果示例](artifact/examples/运行效果示例.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration guidance] <br>
**Output Format:** [Console text, Markdown reports, and Word .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Markdown reports to artifact/output/ when --save is used and Word reports to /tmp through to_word.py.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
