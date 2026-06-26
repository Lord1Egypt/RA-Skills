## Description: <br>
Helps agents use bundled shell scripts and AppleScript to create Reminders, Notes, Calendar events, and iMessages on macOS when direct integrations are unavailable or unreliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qy-zhang](https://clawhub.ai/user/qy-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to perform common Apple app actions on macOS through AppleScript-backed shell scripts, especially when direct tool or plugin routes are unavailable or flaky. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real iMessages and create persistent Reminders, Notes, and Calendar data without a required final confirmation step. <br>
Mitigation: Manually confirm the recipient, message body, dates, calendar, and note account before running scripts, and verify important created items in the Apple app UI. <br>
Risk: macOS Automation and Full Disk Access permissions can give the agent broad control over Apple apps on the user's Mac. <br>
Mitigation: Grant only the Automation permissions needed for Reminders, Notes, Calendar, and Messages, and avoid Full Disk Access unless there is a specific need. <br>
Risk: Locale-dependent date parsing or missing Apple app accounts/calendars can cause failures or send items to fallback targets. <br>
Mitigation: Use YYYY-MM-DD HH:MM:SS date strings, confirm account and calendar names, and use the bundled troubleshooting checks when a script fails. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/qy-zhang/macos-applescript-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown responses with shell command usage and script result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include returned Apple app object IDs or a brief verification step when script output is empty.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
