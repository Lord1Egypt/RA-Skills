## Description:

Jobstead helps job seekers evaluate role fit, screen postings for scam signals, and produce tailored resume or cover-letter guidance grounded in their profile, tracker, lessons, and the job posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adibas03](https://clawhub.ai/user/adibas03)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to decide whether a specific role is worth pursuing, check scam or structural-fit concerns, and then shape honest application materials when the role clears the fit check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains job-search profile and application-tracker state that can contain sensitive applicant information.

Mitigation: Use it only when the user accepts that persistence, keep state limited to the skill's own reference files, and review or delete stored profile fields the user does not want retained.

Risk: The skill asks the agent to look for state in broad external memory locations, which can expose unrelated or stale personal context.

Mitigation: Disable automatic access to project memory, MCP memory, and native model memory unless the user explicitly wants those sources used for this job-search session.

Risk: Fit checks and scam assessments can influence job-search decisions and may be wrong when profile data, job postings, or policy details are stale.

Mitigation: Have the user confirm profile facts and verify time-sensitive requirements, sponsor registers, and suspicious posting details against authoritative sources before acting.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/adibas03/jobstead/tree/master/skills/jobstead)
- [ClawHub skill page](https://clawhub.ai/adibas03/skills/jobstead)
- [Jobstead playbook](https://raw.githubusercontent.com/adibas03/jobstead/refs/tags/v3.6/Jobstead.md)
- [Applicant Profile](references/profile.md)
- [Application Tracker](references/tracker.md)
- [Lessons](references/lessons.md)
- [Session Log](references/log.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain text guidance, including fit checks, scam assessments, tracker updates, resume tailoring, and cover-letter drafts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to persistent profile, tracker, lessons, and session-log files when the user confirms.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
