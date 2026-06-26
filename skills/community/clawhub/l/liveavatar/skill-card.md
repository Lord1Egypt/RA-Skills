## Description: <br>
Talk face-to-face with your OpenClaw agent using a real-time video avatar powered by LiveAvatar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eNNNo](https://clawhub.ai/user/eNNNo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to start a browser-based LiveAvatar interface for voice and video conversations with an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken input may contain sensitive information that is transcribed and passed through the avatar and agent flow. <br>
Mitigation: Avoid speaking secrets or other sensitive data unless the user accepts the LiveAvatar service and agent data handling. <br>
Risk: The skill launches a third-party npm package and depends on the LiveAvatar service. <br>
Mitigation: Install and run it only when the user trusts the LiveAvatar service and the openclaw-liveavatar npm package. <br>
Risk: The browser interface requires microphone access and a local OpenClaw Gateway. <br>
Mitigation: Confirm microphone permissions intentionally and run the OpenClaw Gateway before starting the avatar session. <br>


## Reference(s): <br>
- [LiveAvatar](https://liveavatar.com) <br>
- [LiveAvatar App](https://app.liveavatar.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to check configuration, launch the npm package, and explain browser microphone and local gateway requirements.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
