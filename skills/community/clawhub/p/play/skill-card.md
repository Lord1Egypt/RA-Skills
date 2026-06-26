## Description: <br>
Make OpenClaw launch the Ashen Era CLI build, play a real run, and deliver a complete first-person play report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssochi](https://clawhub.ai/user/ssochi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when they want an agent to launch a local Ashen Era CLI build, complete a real play session, and write a first-person recap grounded in that run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute a local native Ashen Era CLI binary from packaged release archives. <br>
Mitigation: Install only when comfortable running the bundled game executable; use the documented play command and verify publisher/source for future release archives. <br>
Risk: Unsupported platforms or missing archives prevent a real gameplay session. <br>
Mitigation: Use the packed CLI launcher for target selection and stop plainly on unsupported environments or missing archives instead of faking a playthrough. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssochi/play) <br>
- [CLI Surface](references/cli-surface.md) <br>
- [Report Contract](references/report-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Text, Guidance] <br>
**Output Format:** [Markdown report with shell command details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report records the launch command, selected executable target, class, seed, locale, run result, key actions, and retrospective.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
