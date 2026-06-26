## Description: <br>
Microsoft Teams connector plugin for OpenClaw Gateway. Bridges Teams channels to OpenClaw AI sessions with per-channel system prompts, model configuration, and Azure Bot Framework authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homeofe](https://clawhub.ai/user/homeofe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to connect Microsoft Teams channels, group chats, and direct messages to OpenClaw AI sessions with per-channel prompts and model settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector handles Azure Bot Framework credentials, Graph/OpenClaw tokens, and Teams message or attachment content. <br>
Mitigation: Deploy with least-privilege Azure, Graph, GitHub, and OpenClaw credentials, and restrict the bot to channels where that access is appropriate. <br>
Risk: Teams file data and attachment details may be forwarded to the agent or logged, and chat history or temporary files may remain on the host. <br>
Mitigation: Disable sensitive content logging, define retention controls for history and temporary files, and avoid regulated or highly confidential channels until those controls are verified. <br>
Risk: Bundled Graph and GitHub modules include write-capable operations that may exceed the Teams connector's expected deployment scope. <br>
Mitigation: Remove or isolate unused Graph/GitHub modules and withhold write permissions unless they are explicitly required and reviewed. <br>


## Reference(s): <br>
- [OpenClaw Gateway](https://github.com/openclaw/openclaw) <br>
- [ClawHub release page](https://clawhub.ai/homeofe/openclaw-msteams-bot-elvatis) <br>
- [Publisher profile](https://clawhub.ai/user/homeofe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Teams messages carrying OpenClaw agent responses, with text, Markdown, code blocks, shell commands, and configuration snippets when produced by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include content derived from Teams messages and attachments forwarded to OpenClaw sessions.] <br>

## Skill Version(s): <br>
0.1.3 (source: evidence release, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
