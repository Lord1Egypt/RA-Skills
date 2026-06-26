## Description: <br>
自动抓取龙港325802人才招聘网职位信息，按用户偏好筛选并整理后发送邮件通知。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttzuozhe](https://clawhub.ai/user/ttzuozhe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers use this skill to crawl Longgang 325802 recruitment listings, filter them by job preference, collect company contact details, and receive the organized results by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically sends scraped job results by email using embedded QQ SMTP credentials and a default recipient. <br>
Mitigation: Review the email behavior before installation; require user-provided mail credentials and recipient confirmation, and preview the exact job and contact data before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttzuozhe/longgang-job-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text job-search report, saved locally and sent by email] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes job title, company, address, phone, experience, education, and optional job description when found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json; SKILL.md lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
