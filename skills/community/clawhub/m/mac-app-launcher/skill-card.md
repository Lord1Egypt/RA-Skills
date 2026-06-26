## Description: <br>
Searches installed macOS applications by keyword and opens selected apps with the macOS open command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlutwuwei](https://clawhub.ai/user/dlutwuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to find installed applications, review matches when there are multiple results, and launch the intended app from Spotlight or known application directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may launch a single matched macOS application automatically. <br>
Mitigation: For extra control, have the agent list matching application paths and wait for confirmation before opening anything. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlutwuwei/mac-app-launcher) <br>
- [Publisher profile](https://clawhub.ai/user/dlutwuwei) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and application path lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local macOS application search and launch commands when used by an agent with shell access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
