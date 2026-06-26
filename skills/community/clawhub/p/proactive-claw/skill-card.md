## Description: <br>
Proactive Claw is a proactive calendar assistant for OpenClaw that learns from user feedback and suggests prep time, buffers, follow-ups, and schedule improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googlarz](https://clawhub.ai/user/googlarz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to review upcoming calendar events, receive proactive scheduling suggestions, and apply approved prep, buffer, and follow-up actions. It is intended for users who want local-first productivity assistance while retaining confirmation control by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad calendar access can expose sensitive schedule data and OAuth tokens. <br>
Mitigation: Use a dedicated calendar account where possible, review requested Google or Nextcloud access before setup, and revoke Google OAuth access when the skill is no longer needed. <br>
Risk: Local productivity memory can retain meeting outcomes, policies, contacts, notification logs, and scoring data. <br>
Mitigation: Review and delete the local skill state directory when needed, use the export and health-check commands for inspection, and tune retention settings such as memory decay and action cleanup. <br>
Risk: Calendar action items may be written or deleted in paths where approval language is not fully enforced. <br>
Mitigation: Start with dry-run or simulation commands, keep autonomy at confirm or advisory, and verify the Actions calendar before enabling daemon, policy, relationship memory, or calendar editor features. <br>
Risk: Watched and ignored calendar filters may not be honored consistently by every scan path in this version. <br>
Mitigation: Manually verify which calendars are being scanned and avoid using the skill with calendars that should never be processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googlarz/proactive-claw) <br>
- [Security and Privacy Reference](SECURITY.md) <br>
- [Skill documentation](SKILL.md) <br>
- [Example configuration](config.example.json) <br>
- [Google Calendar API endpoint](https://www.googleapis.com/calendar/v3/) <br>
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create approved calendar action items and local state when configured by the user.] <br>

## Skill Version(s): <br>
1.2.41 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
