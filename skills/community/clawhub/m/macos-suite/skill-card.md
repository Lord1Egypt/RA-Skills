## Description: <br>
macOS system app automation for opening, reading, and creating items in Mail, Calendar, Reminders, Notes, Maps, Freeform, Photos, Weather, Stocks, and Clock. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to operate local Apple apps through an agent, including reading app data, creating drafts or records, opening app views, and adding Freeform content after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request macOS Automation and privacy permissions that expose local Mail, Notes, Calendar, Reminders, Photos, and related app data. <br>
Mitigation: Install only when that local app access is acceptable, grant the narrow permissions required for the intended workflow, and review macOS permission prompts deliberately. <br>
Risk: Mutating actions can send mail or modify Calendar, Reminders, Notes, and Freeform content. <br>
Mitigation: Use the built-in confirm=YES requirement for mutating commands, prefer draft or read-only alternatives when possible, and have the agent present confirmation requests before execution. <br>
Risk: Stock quote and history commands contact third-party market-data services. <br>
Mitigation: Treat stock lookup inputs as outbound network requests and avoid submitting sensitive or confidential watchlists unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/macos-suite) <br>
- [Publisher profile](https://clawhub.ai/user/lilei0311) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw ClawHub documentation](https://docs.openclaw.ai/tools/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from command execution, with shell command examples and confirmation guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on macOS only and requires python3 and osascript.] <br>

## Skill Version(s): <br>
0.2.3 (source: frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
