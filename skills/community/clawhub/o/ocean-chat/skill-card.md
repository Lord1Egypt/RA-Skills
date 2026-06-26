## Description: <br>
Ocean Chat provides OceanBus-powered P2P messaging, shared address book management, 1v1 meetup negotiation, and conversation threading for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use Ocean Chat to register OceanBus identities, manage contacts, send encrypted agent-to-agent messages, coordinate meetings, and route remote tasks to local Claude Code sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incoming OceanBus or WeChat messages can trigger persistent local Claude or shell execution when auto-exec or arbitrary on-message hooks are enabled. <br>
Mitigation: Keep auto-exec disabled by default, avoid arbitrary on-message commands, and require human review before enabling unattended execution. <br>
Risk: A PM2 listener or autostart setup can keep the remote-control channel active after initial configuration. <br>
Mitigation: Review PM2 startup configuration, stop listeners when not needed, and run the skill only in directories where remote task execution is intended. <br>
Risk: Message contents and execution results may pass through OceanBus or WeChat integrations and could expose sensitive repository or credential context. <br>
Mitigation: Do not run the skill on sensitive repositories or machines with production credentials, and avoid sending secrets or confidential output through chat messages. <br>


## Reference(s): <br>
- [Ocean Chat on ClawHub](https://clawhub.ai/ryanbihai/ocean-chat) <br>
- [Ocean Chat homepage](https://github.com/ryanbihai/ocean-chat) <br>
- [OceanBus SDK](https://www.npmjs.com/package/oceanbus) <br>
- [OceanBus MCP Server](https://www.npmjs.com/package/oceanbus-mcp-server) <br>
- [OceanBus: 用手机遥控 Claude Code](docs/手机遥控ClaudeCode-工程师上手.md) <br>
- [发本文件给你的claudecode](docs/发本文件给你的claudecode.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or suggest local Node.js, PM2, OceanBus, and Claude Code commands; remote execution modes should be reviewed before use.] <br>

## Skill Version(s): <br>
2.20.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
