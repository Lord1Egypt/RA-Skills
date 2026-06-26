## Description: <br>
Lead a team - run standups, coordinate tasks, and communicate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team leads use this persona to coordinate standups, prepare meetings and weekly digests, delegate email action items, and maintain shared team records through Google Workspace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persona can read email-derived data, calendar context, Drive or Sheets content, and team records that may contain employee or business-sensitive information. <br>
Mitigation: Use a least-privileged Google Workspace account, sanitize sensitive content by default, and require explicit confirmation before reading or reusing sensitive data. <br>
Risk: The persona can post standup summaries or other generated content to Chat and update shared Sheets, which may expose information to unintended audiences or create incorrect team records. <br>
Mitigation: Restrict allowed Chat spaces and Sheets, preview destinations and content before posting or writing, and verify dependent gws skills separately. <br>


## Reference(s): <br>
- [Persona Team Lead on ClawHub](https://clawhub.ai/googleworkspace-bot/persona-team-lead) <br>
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Google Workspace workflow and gws command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-calendar, gws-gmail, gws-chat, gws-drive, and gws-sheets utility skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata); skill metadata 0.22.5 (source: SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
