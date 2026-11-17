## Description:

Offer-Rain helps an agent prepare and send resume application emails to recruiters through a user's configured 163 Mail SMTP account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-zhou-0302](https://clawhub.ai/user/eric-zhou-0302)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to turn job descriptions or recruiter instructions into email configuration files, verify recipient, subject, body, and attachment fields against the original posting, and send one or multiple resume emails after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store reusable email credentials in plaintext and copies them into local job-application configuration files.

Mitigation: Use a dedicated limited-scope mail app password, keep user.json and log files out of synced or shared directories, delete generated configs after sending, and rotate the authorization code if it was exposed.

## Reference(s):

- [Offer-Rain ClawHub skill page](https://clawhub.ai/eric-zhou-0302/skills/offer-rain)
- [163 Mail SMTP service](https://mail.163.com)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-application JSON configs under log/YYYY-MM-DD/ and sends email only after user confirmation.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
