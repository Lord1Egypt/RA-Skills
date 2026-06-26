## Description: <br>
Schedule Manager helps macOS agents manage Apple Calendar events and Reminders tasks using osascript and reminders-cli, with GTD-style planning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
macOS users and agent operators use this skill to create, query, edit, and plan calendar events and reminders, including daily planning and weekly GTD review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar and Reminders operations can alter or delete real personal scheduling data. <br>
Mitigation: Require the agent to show the exact affected items, calendar or list, dates, and count before any delete, edit, complete, list deletion, or bulk operation, then ask for explicit confirmation. <br>
Risk: The skill requires macOS privacy permissions for Calendar and Reminders. <br>
Mitigation: Grant access only to trusted terminal or agent applications and revoke permissions when the skill is no longer needed. <br>


## Reference(s): <br>
- [GTD Methodology Guide](references/gtd-methodology.md) <br>
- [Apple Calendar osascript Reference](references/osascript-calendar.md) <br>
- [Apple Reminders osascript Reference](references/osascript-reminders.md) <br>
- [reminders-cli Guide](references/reminders-cli-guide.md) <br>
- [reminders-cli](https://github.com/keith/reminders-cli) <br>
- [Getting Things Done Forum](https://forum.gettingthingsdone.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and AppleScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute Calendar and Reminders actions after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
