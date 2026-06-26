## Description: <br>
AgentCall enables AI agents to join Google Meet, Zoom, and Microsoft Teams calls as a bot with voice, avatar, screenshare, real-time transcription, screenshots, and meeting chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnpatternai](https://clawhub.ai/user/johnpatternai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to let an AI agent attend and participate in live video meetings, including speaking, listening to transcripts, sharing visuals, sending chat, and recovering from meeting interruptions or crashes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting participants can influence the agent through live transcripts and chat while the agent may still have access to local tools, files, and commands. <br>
Mitigation: Use the skill only in trusted or properly scoped meetings and keep the agent framework's permission controls restrictive during calls. <br>
Risk: The skill can transcribe participants, take screenshots, send chat, and screenshare meeting content. <br>
Mitigation: Notify participants and follow the user's consent, privacy, and retention requirements before enabling these features. <br>
Risk: Webpage and screenshare modes can expose selected localhost pages through AgentCall tunnels. <br>
Mitigation: Serve only intended content on dedicated ports, avoid sensitive local services, and close spawned servers and tunnels when the call ends. <br>
Risk: The AgentCall API key may be stored in plaintext under ~/.agentcall. <br>
Mitigation: Protect the config file, avoid sharing it, and rotate the API key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/johnpatternai/join-meeting) <br>
- [AgentCall site](https://agentcall.dev) <br>
- [README](README.md) <br>
- [AgentCall API Reference](references/api.md) <br>
- [Collaborative Mode Guide](references/guides/collaborative-mode.md) <br>
- [Crash Recovery Guide](references/guides/crash-recovery.md) <br>
- [Interruption Handling Guide](references/guides/interruption-handling.md) <br>
- [UI Templates Guide](references/guides/ui-templates.md) <br>
- [Webpage AV Screenshare Guide](references/guides/webpage-av-screenshare.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, code examples, and meeting event commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live meeting actions such as TTS speech, chat messages, screenshots, screenshare commands, and localhost tunnel configuration.] <br>

## Skill Version(s): <br>
1.1.14 (source: server release metadata and plugin metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
