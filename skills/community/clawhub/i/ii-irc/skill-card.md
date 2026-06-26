## Description: <br>
Provides persistent IRC presence through ii with event-driven mention detection for monitoring IRC channels, sending messages, and integrating OpenClaw with IRC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[destructatron](https://clawhub.ai/user/destructatron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up an AI agent on IRC, watch channel mentions, read recent IRC context, and send replies through the ii file interface. It is intended for Linux environments where OpenClaw can receive events from a mention watcher. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watched-channel mentions can pass untrusted IRC text directly into OpenClaw events. <br>
Mitigation: Use private or moderated channels, add sender and channel allowlists, and require review before broad deployment. <br>
Risk: Frequent or hostile channel traffic can repeatedly wake the agent. <br>
Mitigation: Add rate limits for mention handling and disable the watcher service when the bot should be inactive. <br>
Risk: Channel logs under ~/irc grow indefinitely and may retain sensitive IRC content. <br>
Mitigation: Read logs with bounded tail commands, rotate or delete logs as needed, and keep the agent's filesystem permissions limited. <br>


## Reference(s): <br>
- [ii IRC client](https://tools.suckless.org/ii/) <br>
- [ii source repository](https://git.suckless.org/ii) <br>
- [ClawHub skill page](https://clawhub.ai/destructatron/ii-irc) <br>
- [Publisher profile](https://clawhub.ai/user/destructatron) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and service configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, operation, troubleshooting, and message-handling guidance for ii-based IRC integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
