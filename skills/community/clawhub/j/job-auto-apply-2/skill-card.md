## Description: <br>
Automates job search and application workflows across major job platforms, including match analysis, cover-letter generation, form filling, and application tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to search job boards, evaluate role fit, generate tailored application materials, and optionally submit applications from a configured applicant profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate real job applications while handling sensitive applicant profile, resume, and credential data. <br>
Mitigation: Keep dry-run and per-application confirmation enabled, store credentials securely, and review each application before submission. <br>
Risk: Applicant and job details may be shared with external AI services for compatibility analysis, resume tailoring, and cover-letter generation. <br>
Mitigation: Confirm data-sharing expectations before use and avoid sending unnecessary personal or confidential information. <br>
Risk: Automation against job platforms may conflict with platform limits or anti-bot controls. <br>
Mitigation: Prefer official APIs, respect platform terms and rate limits, and avoid CAPTCHA or proxy bypass workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/job-auto-apply-2) <br>
- [SkillBoss Job Auto Apply](https://skillboss.co/skills/job-auto-apply) <br>
- [LinkedIn Jobs API documentation](https://developer.linkedin.com/docs/v2/jobs) <br>
- [Indeed API documentation](https://opensource.indeedeng.io/api-documentation/) <br>
- [Wellfound documentation](https://docs.wellfound.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON application results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write application tracking JSON and sends applicant and job data to external services when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
