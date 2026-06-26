## Description: <br>
Connects local OpenClaw agents to browser voice chat through the hosted hotbutter.ai relay, sending transcribed speech to the local agent and relaying text responses back for speech output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michael-stajer](https://clawhub.ai/user/michael-stajer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to give a local OpenClaw agent a browser-based voice interface while the agent execution remains on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice transcripts and agent responses pass through hotbutter.ai by default. <br>
Mitigation: Use only for sessions where that data flow is acceptable, or configure --relay-url to a relay you control. <br>
Risk: Agent responses may include secrets or private data that would be sent through the relay. <br>
Mitigation: Use an OpenClaw agent with permissions appropriate for voice input and avoid sessions where secrets or private data may be spoken or printed. <br>
Risk: The server security summary notes that one registry summary describes the setup as self-hosted even though the default behavior uses a hosted relay. <br>
Mitigation: Review the hosted relay data path before installation and use the local alternative or a controlled relay when private operation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michael-stajer/hotbutter) <br>
- [hotbutter-os local alternative](https://github.com/hotbutter-ai/hotbutter-os) <br>
- [Hotbutter relay service](https://hotbutter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation and CLI output with plain-text agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a WebSocket relay by default and can be configured with a custom relay URL.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
