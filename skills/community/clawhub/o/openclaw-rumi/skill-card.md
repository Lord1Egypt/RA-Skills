## Description: <br>
Rumi helps OpenClaw users match with real humans who share their interests and chat through OpenClaw or on the web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ricky610329](https://clawhub.ai/user/Ricky610329) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users use Rumi to find real people for topic-driven conversations, peer perspective, human expertise, or casual chat. The agent gathers the user's intended topic, creates a single matching session, reports match status, and can relay messages in OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send personal context to an external matching service to find a human chat partner. <br>
Mitigation: Ask the agent to show the exact matching description before starting a session and remove sensitive details you do not want shared. <br>
Risk: The Rumi API token grants access to the user's Rumi account. <br>
Mitigation: Treat the token like a password and avoid sharing or storing it outside the intended plugin configuration. <br>
Risk: Repeated match requests can create duplicate active sessions. <br>
Mitigation: Use one active matching session at a time and poll the existing session before creating another. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ricky610329/openclaw-rumi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls] <br>
**Output Format:** [Conversational text with setup links, match status, icebreakers, and relayed chat messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before starting a matching session and uses one active matching session at a time.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
