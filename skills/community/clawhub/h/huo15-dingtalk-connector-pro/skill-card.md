## Description: <br>
A DingTalk OpenClaw connector for AI Card streaming, session management, memory-system integration, media handling, document actions, and multi-agent routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to connect DingTalk bots to OpenClaw Gateway so agents can receive DingTalk messages, maintain conversation context, stream AI Card responses, route conversations to agents, and perform configured DingTalk media or document actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can transmit local files through DingTalk media handling. <br>
Mitigation: Disable or patch automatic local-path media upload unless the workflow explicitly requires it, and review media paths before deployment. <br>
Risk: Gateway methods can perform high-impact DingTalk send and document actions. <br>
Mitigation: Restrict who can call the plugin, review gateway method exposure, and configure DM and group allowlists before enabling the connector. <br>
Risk: DingTalk credentials grant access to external messaging and document APIs. <br>
Mitigation: Use least-privilege DingTalk credentials, store secrets through approved secret mechanisms, and rotate credentials if exposure is suspected. <br>
Risk: Helper install scripts may change OpenClaw configuration. <br>
Mitigation: Avoid helper install scripts unless you accept the configuration changes and have reviewed the script behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jobzhao15/huo15-dingtalk-connector-pro) <br>
- [Publisher profile](https://clawhub.ai/user/jobzhao15) <br>
- [npm package](https://www.npmjs.com/package/@huo15/dingtalk-connector-pro) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [DingTalk Open Platform](https://open-dev.dingtalk.com/) <br>
- [Agent routing guide](docs/AGENT_ROUTING.md) <br>
- [DingTalk DEAP Agent guide](docs/DEAP_AGENT_GUIDE.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, API calls] <br>
**Output Format:** [DingTalk messages, AI Cards, media uploads, document API actions, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured OpenClaw Gateway and least-privilege DingTalk credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
