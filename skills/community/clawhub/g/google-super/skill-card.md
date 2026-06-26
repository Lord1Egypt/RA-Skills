## Description: <br>
Unified Google services API integration with managed OAuth for Gmail, Google Calendar, Drive, Docs, Sheets, Slides, Meet, Tasks, Photos, Maps, Google Analytics, and Google Ads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a Google account through hosted OAuth and operate across Google services from an agent workflow, including email, calendars, files, documents, spreadsheets, meetings, tasks, maps, analytics, and ads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Google OAuth access can expose or change sensitive Google account data. <br>
Mitigation: Review the Google OAuth consent screen, grant only needed scopes, and revoke the ClawLink connection when it is no longer needed. <br>
Risk: Write, delete, Ads, and batch operations can create high-impact changes. <br>
Mitigation: Use these tools only with explicit intent and confirm destructive or advertising-related actions before execution. <br>


## Reference(s): <br>
- [Google Workspace APIs](https://developers.google.com/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Google Super Connection](https://claw-link.dev/dashboard?add=google-super) <br>
- [Google Super on ClawHub](https://clawhub.ai/hith3sh/google-super) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Google API read, write, delete, advertising, and analytics actions through ClawLink tools after OAuth connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
