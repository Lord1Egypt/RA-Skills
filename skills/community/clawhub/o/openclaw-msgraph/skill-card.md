## Description: <br>
Read and manage Microsoft Outlook email and calendar data through Microsoft Graph, including inbox search, message moves, event listing, and event creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrskerrett](https://clawhub.ai/user/jrskerrett) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Microsoft account so it can check Outlook mail, organize messages, inspect calendar events, and create calendar entries with user authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read/write access to Outlook mail and calendars. <br>
Mitigation: Install only when those permissions are acceptable, and confirm move, create, or delete-style actions before execution. <br>
Risk: The auth command set can print a raw access token and stores OAuth tokens locally. <br>
Mitigation: Protect the local token file, avoid logging token output, and remove stored tokens when revoking access. <br>
Risk: LLM integration examples can expose mailbox or calendar contents to an external model provider. <br>
Mitigation: Send mailbox or calendar content to an external LLM only after explicit user approval for that data sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jrskerrett/openclaw-msgraph) <br>
- [Publisher profile](https://clawhub.ai/user/jrskerrett) <br>
- [Setup guide](references/SETUP.md) <br>
- [Microsoft Graph API reference](references/api.md) <br>
- [Skill guide](skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise human-facing summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger authenticated Microsoft Graph API calls that read or modify Outlook mail and calendar data.] <br>

## Skill Version(s): <br>
1.0.0 (source: pyproject.toml, CHANGELOG, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
