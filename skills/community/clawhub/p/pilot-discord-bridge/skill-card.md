## Description: <br>
Bidirectional bridge between Pilot Protocol and Discord servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect Pilot agents with Discord communities for outbound notifications, rich embeds, and inbound Discord message streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord webhook URLs and bot credentials can be exposed if pasted into prompts, logs, or files. <br>
Mitigation: Store webhook values in an environment variable or secret manager and rotate them if exposed. <br>
Risk: Inbound Discord messages are untrusted input that may influence agent behavior. <br>
Mitigation: Restrict webhook and bot permissions to the needed channels and validate or review inbound commands before acting on them. <br>
Risk: External relay scripts and the Pilot daemon affect runtime behavior outside the skill text. <br>
Mitigation: Inspect any external discord_relay.py before running it and run the Pilot daemon with only the access required for the bridge. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require pilotctl, a running Pilot daemon, and Discord webhook or bot configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
