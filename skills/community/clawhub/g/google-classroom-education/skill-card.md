## Description: <br>
Manage Google Classroom courses, coursework, students, teachers, submissions, announcements, and grades through the Google Classroom API with ClawLink OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and manage Google Classroom courses, rosters, coursework, submissions, announcements, and grades from an OpenClaw chat. Write operations such as creating coursework, posting announcements, changing grades, or altering membership require explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers Google Classroom access through ClawLink OAuth and can use sensitive classroom data. <br>
Mitigation: Install only if the user trusts ClawLink to broker and store OAuth access, review requested permissions during connection, and use the correct school account. <br>
Risk: Coursework, announcements, grades, course membership, and deletion actions can change or remove classroom data. <br>
Mitigation: Require explicit confirmation before creating, deleting, grading, posting, or changing course membership, and preview write operations when available. <br>


## Reference(s): <br>
- [Google Classroom API Reference](https://developers.google.com/classroom/reference/rest) <br>
- [Google Classroom API Overview](https://developers.google.com/classroom/api/guides/overview) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [Google Classroom Skill Page](https://clawhub.ai/hith3sh/google-classroom-education) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Google Classroom account through ClawLink OAuth; write and destructive actions require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
