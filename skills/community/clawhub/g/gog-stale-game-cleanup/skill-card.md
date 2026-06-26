## Description: <br>
Find installed GOG games not played in 30 or more days, email a report, and add Apple Reminders for cleanup review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal automation agents use this skill to identify installed GOG games that appear stale, receive an email report, and create reminders for uninstall review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can email local game details and install paths. <br>
Mitigation: Run with DRY_RUN=true first, verify EMAIL_TO and EMAIL_ACCOUNT, and only send reports to trusted recipients. <br>
Risk: The skill creates Apple Reminders by default when stale games are found. <br>
Mitigation: Use DRY_RUN=true to preview changes and confirm REMINDERS_LIST before allowing reminder creation. <br>
Risk: The security review flags unsafe environment-variable handling in the shell script. <br>
Mitigation: Review environment variable values before execution and consider patching the script to pass data into Python via arguments or environment reads instead of source interpolation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/gog-stale-game-cleanup) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and shell command examples for running the bundled cleanup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce console summaries, email reports, and Apple Reminders when executed with configured local tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
