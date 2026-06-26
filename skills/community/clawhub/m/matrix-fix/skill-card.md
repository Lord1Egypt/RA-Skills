## Description: <br>
Helps troubleshoot Matrix Channel failures including missing encryption modules, expired tokens, homeserver resolution errors, channel reconfiguration, room exit operations, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Boms](https://clawhub.ai/user/Boms) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when repairing an OpenClaw Matrix integration that cannot connect, authenticate, encrypt messages, or maintain its configured rooms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reset commands can remove Matrix account state or configuration and may cause downtime. <br>
Mitigation: Back up Matrix configuration and account state before running reset commands, and schedule the work for an acceptable maintenance window. <br>
Risk: Room-leaving commands can remove the bot from unintended Matrix rooms. <br>
Mitigation: Confirm the homeserver, bot account, access token context, and each room ID before issuing leave-room requests. <br>
Risk: Password examples can lead users to place credentials in shell history. <br>
Mitigation: Use secret-safe input methods or temporary protected files instead of typing production passwords directly into shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Boms/matrix-fix) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic commands, reset steps, Matrix API curl examples, and configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
