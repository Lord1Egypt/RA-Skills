## Description: <br>
SillyTavern-compatible roleplay plugin with character cards, long memory, multimodal output (TTS/image), and Generative-Agents-style companion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garfeildma](https://clawhub.ai/user/garfeildma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this plugin to run SillyTavern-compatible roleplay sessions, import character cards, presets, and lorebooks, and add long memory plus multimodal companion features across supported chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted users could import roleplay assets from files or URLs that influence prompts, sessions, or stored lore. <br>
Mitigation: Restrict /rp import commands to trusted operators and review imported cards, presets, and lorebooks before use. <br>
Risk: Long-memory storage and proactive companion behavior can preserve personal conversation context and initiate follow-up messages. <br>
Mitigation: Enable these features only with user consent, document retention expectations, and provide operators a clear path to pause, end, or delete sessions. <br>
Risk: Third-party model, TTS, image, and embedding providers may receive prompts or generated roleplay context. <br>
Mitigation: Configure approved providers only, protect API credentials, and disclose provider use to users before enabling multimodal or external embedding features. <br>
Risk: Native SQLite vector extensions can introduce native-code risk if extension paths are not controlled. <br>
Mitigation: Use the built-in fallback or vetted SQLite extensions from trusted locations; do not allow untrusted operators to set extension paths. <br>
Risk: Persona synchronization can persistently change agent behavior beyond a single roleplay turn. <br>
Mitigation: Limit persona sync and restore commands to trusted operators and review the active persona state after synchronization. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/garfeildma/openclaw-tavern) <br>
- [Project homepage](https://github.com/garfeildma/openclaw-tavern) <br>
- [README](README.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Chat responses, slash-command output, configuration snippets, and media references for generated speech or images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist roleplay assets, session history, summaries, and memory vectors when SQLite storage is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, package.json, openclaw.plugin.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
