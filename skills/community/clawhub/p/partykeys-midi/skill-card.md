## Description: <br>
Control PartyKeys MIDI keyboard via WebSocket - connect device, light up keys with 12 colors, listen to playing, play sequences, and follow mode for music teaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allen4z](https://clawhub.ai/user/allen4z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and music educators use this skill to connect an agent to a PartyKeys MIDI keyboard, control its lights and playback modes, listen for played notes, and support follow-along music teaching workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens an unauthenticated network WebSocket service for local hardware control. <br>
Mitigation: Use it only on a trusted LAN and avoid exposing port 18790 to the internet. <br>
Risk: Setup makes persistent OpenClaw configuration changes. <br>
Mitigation: Review or back up ~/.openclaw/mcp.json and ~/.openclaw/openclaw.json before setup, then remove the MCP entry and skill symlink when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allen4z/partykeys-midi) <br>
- [Publisher profile](https://clawhub.ai/user/allen4z) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with tool-call parameters and JSON text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 on macOS or Linux and uses a local WebSocket bridge on port 18790 for device control.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
