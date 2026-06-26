## Description: <br>
Use when the user asks to manage Google Classroom: create or update courses, enroll students and teachers, post announcements, create assignments, view submissions, grade work, manage topics, or send/accept invitations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Google Classroom through gogcli for course, roster, coursework, submission, announcement, topic, invitation, and profile management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Google Classroom operations can affect courses, rosters, grades, submissions, announcements, invitations, and deletions. <br>
Mitigation: Confirm the selected Google account, course, student or teacher identity, and requested action before executing mutating tools. <br>
Risk: The gog_classroom_run escape hatch can reach Classroom operations beyond the dedicated tools. <br>
Mitigation: Prefer dedicated tools when available and review the exact escape-hatch command and intended scope before use. <br>
Risk: Broad classroom-related triggers may activate the skill for ambiguous requests. <br>
Mitigation: Verify that the user intends live Google Classroom management before authenticating or acting on account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gogcli-mcp-classroom) <br>
- [gogcli](https://github.com/openclaw/gogcli) <br>
- [gogcli-mcp project link in skill text](https://github.com/chrischall/gogcli-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and tool-use guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or later and an authenticated gogcli account.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
