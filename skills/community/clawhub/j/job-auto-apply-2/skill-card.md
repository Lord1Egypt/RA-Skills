## Description:

Job Auto Apply helps agents search job boards, evaluate job matches, generate tailored cover letters, fill application forms, and track application status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job seekers use this skill to search for relevant roles, prepare application materials, and optionally submit applications with dry-run or confirmation controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive job-seeker information such as resumes, contact details, profile data, and application preferences.

Mitigation: Use dry-run mode until reviewed, avoid real resumes or profile data unless the user accepts external API transmission, and store credentials and profile files with restricted access.

Risk: Non-dry-run automation may submit applications or create records that are not reliable proof of successful filing.

Mitigation: Require explicit review before real application activity and verify submitted applications directly on the relevant job platform.

Risk: Automation, scraping, CAPTCHA handling, or proxy guidance may conflict with platform terms or expected user behavior.

Mitigation: Prefer official APIs, respect platform terms and rate limits, and avoid CAPTCHA or proxy workarounds.

Risk: Generated cover letters, screening answers, or match analyses may be inaccurate or misrepresent the applicant.

Mitigation: Require human review of generated application materials and only submit truthful, user-approved information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/job-auto-apply-2)
- [SkillBoss skill page](https://skillboss.co/skills/job-auto-apply)
- [Job Platform Integration Reference](artifact/platform_integration.md)
- [LinkedIn Jobs API documentation](https://developer.linkedin.com/docs/v2/jobs)
- [Indeed API documentation](https://opensource.indeedeng.io/api-documentation/)
- [Glassdoor developer documentation](https://www.glassdoor.com/developer/index.htm)
- [Wellfound documentation](https://docs.wellfound.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON profile and application result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; may send job descriptions and applicant profile details to named external AI APIs and job platforms.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
