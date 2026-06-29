## Description: <br>
Fetches IT之家 daily, weekly, or monthly hot article rankings, formats them as a Markdown article list, and can support user-selected messaging-channel delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dustink66](https://clawhub.ai/user/dustink66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve IT之家 ranking articles on demand or prepare scheduled daily hot-news pushes to a selected messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches live IT之家 pages, so network failures or page-structure changes can produce empty or incomplete rankings. <br>
Mitigation: Check network access and update the parser when IT之家 changes the ranking page structure. <br>
Risk: Optional channel-send and cron examples can deliver formatted results to the wrong conversation or schedule if target settings are incorrect. <br>
Mitigation: Review the target channel, user, session, cron schedule, timezone, and message text before sending or creating a scheduled push. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dustink66/ithome-rank) <br>
- [IT之家](https://www.ithome.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article list with inline links, Python code, shell commands, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network access to IT之家 is required; optional messaging-channel and cron examples require user-selected channel and schedule settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
