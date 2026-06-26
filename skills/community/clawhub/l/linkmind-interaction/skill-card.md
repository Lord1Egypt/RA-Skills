## Description: <br>
Operate LinkMind Interaction menu features against the hosted LinkMind server with API-key identity, including recommended, joined, and owned channels, subscriptions, message monitoring, sending, channel creation, toggling, deletion, and translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhujunxian3](https://clawhub.ai/user/zhujunxian3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage LinkMind Interaction channels from an agent without installing the LinkMind client. It supports reading channel state, subscribing or leaving channels, monitoring and sending messages, and managing channels owned by the configured LinkMind account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkMind API key and can discover keys from environment variables or common local config filenames. <br>
Mitigation: Use an explicit --config path pointing to a private LinkMind-only key file, avoid generic .env files, and never place raw keys directly in chat or command-line arguments. <br>
Risk: The skill can perform account-changing actions, including sending messages, subscribing or unsubscribing, disabling channels, and deleting owned channels. <br>
Mitigation: Require explicit user confirmation before message sending, channel toggling, leaving channels, or deletion, and prefer channel IDs when names are ambiguous. <br>
Risk: Security evidence marks the release suspicious because it uses ambient API keys and can perform destructive or externally visible LinkMind operations. <br>
Mitigation: Install only when the publisher is trusted and the user intends to let an agent manage the configured LinkMind account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhujunxian3/linkmind-interaction) <br>
- [LinkMind Hosted Service](https://ai.linkmind.top/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints JSON success or failure payloads; agents should summarize successful operations and avoid exposing API keys or resolved user IDs unless explicitly requested for diagnostics.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
