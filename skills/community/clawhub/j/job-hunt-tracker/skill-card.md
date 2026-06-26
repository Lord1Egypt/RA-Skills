## Description: <br>
Job Hunt Tracker helps users locally track job applications, interviews, offers, follow-ups, job-search statistics, and related career-search notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkpareek0315](https://clawhub.ai/user/mkpareek0315) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a local job-search organizer for logging applications, scheduling interviews, tracking follow-ups, comparing offers, and reviewing job-hunt progress. It is intended for personal career tracking where the agent produces structured guidance and local file updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal job-search details, including companies, roles, salary ranges, offers, notes, and rejections, on the local machine. <br>
Mitigation: Review the contents of ~/.openclaw/job-hunt-tracker/ periodically and delete that folder when the data is no longer needed. <br>
Risk: The skill needs local read and write access to maintain the tracker files. <br>
Mitigation: Use it only when local job-search tracking is desired and keep the expected storage path limited to ~/.openclaw/job-hunt-tracker/. <br>


## Reference(s): <br>
- [Job Hunt Tracker on ClawHub](https://clawhub.ai/mkpareek0315/job-hunt-tracker) <br>
- [Publisher profile: mkpareek0315](https://clawhub.ai/user/mkpareek0315) <br>
- [Author social profile](https://x.com/Mkpareek19_) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style conversational responses with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local JSON files under ~/.openclaw/job-hunt-tracker/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
