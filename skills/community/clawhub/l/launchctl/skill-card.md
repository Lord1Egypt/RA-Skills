## Description: <br>
Schedules macOS applications to launch or quit through launchctl and launchd by translating natural language or cron-style schedules into user LaunchAgent plist files and management commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skkypy](https://clawhub.ai/user/skkypy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, power users, and operations staff use this skill to create, inspect, trigger, and remove user-level macOS LaunchAgent schedules for applications after previewing the generated plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write, load, unload, and remove user-level LaunchAgent plist files. <br>
Mitigation: Use --dry-run before write or remove operations and review the displayed plist paths and launchctl commands before confirming. <br>
Risk: Management commands can affect unrelated user LaunchAgents or processes when broad labels or prefixes are supplied. <br>
Mitigation: Operate only on labels or prefixes you recognize, preferably tasks created by this skill under com.user.launch. <br>
Risk: The --yes option skips interactive confirmation. <br>
Mitigation: Avoid --yes unless deliberate automation is required and the command arguments have already been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/skkypy/launchctl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plist configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run previews, launchctl commands, LaunchAgent plist content, status summaries, and removal guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
