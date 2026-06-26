## Description: <br>
Work with Google Chat spaces, members, messages, attachments, and threaded conversations via the Google Chat API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect and manage Google Chat spaces, members, messages, attachments, reactions, threads, and related collaboration workflows through a connected Google account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawLink holds the Google OAuth connection and can access Google Chat data available to the connected account. <br>
Mitigation: Connect only an account whose Google Chat spaces should be exposed to this tool. <br>
Risk: Write or destructive actions can send messages, delete messages or spaces, change memberships, or otherwise alter Google Chat state. <br>
Mitigation: Review previews and confirm the intended target and effect before any send, deletion, membership change, or space management action. <br>
Risk: The skill can only act within the connected account's Google Chat permissions, so requests may fail when access is insufficient or a space requires bot authentication. <br>
Mitigation: Verify the connected account, space identifiers, and live tool catalog before acting on ambiguous or privileged requests. <br>


## Reference(s): <br>
- [Google Chat API Reference](https://developers.google.com/workspace/chat/api/reference/rest) <br>
- [Google Chat API Overview](https://developers.google.com/workspace/chat/api/guides/overview) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [Google Chat Skill Page](https://clawhub.ai/hith3sh/google-chat-messaging) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Google Chat tool names, ClawLink setup commands, preview guidance, and structured JSON parameters for tool calls.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
