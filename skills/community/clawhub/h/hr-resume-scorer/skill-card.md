## Description: <br>
简历批量筛选打分工具。支持PDF/Word/TXT格式简历解析，基于JD进行匹配度分析，多维度评分，生成Excel/JSON/Markdown报告。当用户需要筛选简历、批量评估候选人、简历打分、匹配度分析、生成筛选报告时触发此技能。适用于HR、猎头、招聘团队。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwu2495](https://clawhub.ai/user/jiuwu2495) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, recruiters, and hiring teams use this skill to parse one or more resumes, compare candidates against a job description, score candidate fit, and produce screening reports. The skill also surfaces candidate summaries, potential concerns, and recommendations for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles resumes and generated reports that may contain personal candidate data. <br>
Mitigation: Use it only under applicable recruiting, privacy, and employment-law obligations, and define retention and deletion rules for local reports. <br>
Risk: The skill includes candidate judgments such as personality, authenticity, risk, retention, and hiring recommendations. <br>
Mitigation: Use the output as decision support only; keep hiring decisions under human review and avoid relying on sensitive or subjective labels as the sole basis for decisions. <br>
Risk: The skill may collect or request verification records such as education, employment, or social insurance proof. <br>
Mitigation: Collect verification records only with explicit consent and only when necessary for the recruiting process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuwu2495/hr-resume-scorer) <br>
- [PDF compression tool referenced by the skill](https://smallpdf.com/compress-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON reports, Excel reports, and inline Python or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local candidate screening reports and process PDF, Word, TXT, or Markdown resume files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
