## Description: <br>
Pilot Voice Memo helps agents send audio recordings and voice note files over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record, send, receive, and clear voice memo audio files between agents over Pilot Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice memo recording can capture bystanders, secrets, or sensitive background conversations. <br>
Mitigation: Confirm the recording environment and recipient before recording or sending audio. <br>
Risk: The skill sends and receives files through local Pilot Protocol tooling and daemon state. <br>
Mitigation: Install and use it only with trusted Pilot Protocol tooling on machines where the daemon configuration is understood. <br>
Risk: Clearing received files may remove locally stored received data. <br>
Mitigation: Review and preserve any needed received files before running the clear command. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and JSON-oriented pilotctl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary, a running Pilot Protocol daemon, and local audio recording or playback tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
