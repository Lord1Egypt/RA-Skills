## Description: <br>
Make outbound phone calls via ElevenLabs voice agent and Twilio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanjesse](https://clawhub.ai/user/humanjesse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to place outbound phone calls when a user asks to call, dial, or ring a phone number. It supports a custom first message and optional call context for the voice agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may place an outbound call to the wrong or unapproved recipient. <br>
Mitigation: Require the agent to restate the destination number and receive clear user consent immediately before every call. <br>
Risk: Outbound calls may create charges or expose ElevenLabs calling credentials. <br>
Mitigation: Install only for agents that need outbound calling and scope ELEVENLABS_API_KEY, ELEVENLABS_AGENT_ID, and ELEVENLABS_PHONE_NUMBER_ID to this use. <br>
Risk: Calls are limited to the supported E.164 phone number format used by the script. <br>
Mitigation: Normalize user-provided US phone numbers to +1XXXXXXXXXX and confirm the formatted number before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/humanjesse/outbound-call) <br>
- [Publisher profile](https://clawhub.ai/user/humanjesse) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response from the call script, with success metadata or error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY, ELEVENLABS_AGENT_ID, and ELEVENLABS_PHONE_NUMBER_ID.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
