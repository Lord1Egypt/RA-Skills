## Description: <br>
Send and receive text messages between agents over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to exchange direct 1:1 text messages, ask short questions, and perform simple request-response interactions over Pilot Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be shared over the Pilot Protocol network and could expose sensitive content to the recipient or transport. <br>
Mitigation: Do not send secrets or sensitive data unless the recipient and transport are trusted. <br>
Risk: Listening for incoming connections may expose an agent endpoint while the listener is running. <br>
Mitigation: Run listeners only in trusted environments and stop them when the communication task is complete. <br>
Risk: The skill depends on the external pilotctl binary and Pilot Protocol network behavior. <br>
Mitigation: Install and run it only when you trust the pilotctl binary and the Pilot Protocol network you plan to use. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
