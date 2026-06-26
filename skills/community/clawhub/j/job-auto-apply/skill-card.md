## Description: <br>
Job Auto Apply helps an agent search job boards, score matches, generate cover letters, fill application forms, submit applications, and track results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Veeky-kumar](https://clawhub.ai/user/Veeky-kumar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to find matching roles across supported job platforms, prepare tailored application materials, and submit or stage applications with review controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle resumes, employment history, credentials, profile data, and job-platform submissions. <br>
Mitigation: Store credentials in a secure vault or environment variables, confirm where local profile, log, and result files are saved, and delete sensitive files when they are no longer needed. <br>
Risk: Automated submissions may apply to jobs before the user has reviewed the company, role, answers, or generated cover letter. <br>
Mitigation: Use dry-run mode first and require manual approval before every external application submission. <br>
Risk: The artifact includes anti-bot bypass guidance and job-board automation that may conflict with platform rules. <br>
Mitigation: Avoid captcha-solving or proxy-evasion workflows, prefer official APIs where available, and respect platform terms and rate limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Veeky-kumar/job-auto-apply) <br>
- [Platform Integration Reference](platform_integration.md) <br>
- [LinkedIn Jobs API Documentation](https://developer.linkedin.com/docs/v2/jobs) <br>
- [Indeed API Documentation](https://opensource.indeedeng.io/api-documentation/) <br>
- [Glassdoor Developer Documentation](https://www.glassdoor.com/developer/index.htm) <br>
- [Wellfound Documentation](https://docs.wellfound.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration, Python code, shell commands, and application-result JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save application tracking results to a local JSON file when the workflow runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
