## Description: <br>
Deploy Hummingbot trading infrastructure including API server, MCP server, and Condor Telegram bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading infrastructure operators use this skill to install and configure Hummingbot API, optional agent MCP integration, and optional Condor access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation uses remote scripts, Docker images, and persistent MCP configuration that require review before use. <br>
Mitigation: Install in an isolated test environment first and review remote scripts and container behavior before connecting live accounts. <br>
Risk: Default or command-line credentials can expose Hummingbot API or trading account access. <br>
Mitigation: Replace all default credentials, avoid passing real exchange or trading credentials on command lines, and confirm where MCP registration stores secrets. <br>
Risk: Trading services may be reachable outside the intended local environment if deployed or networked incorrectly. <br>
Mitigation: Avoid exposing services beyond localhost unless deliberately configured and protected. <br>


## Reference(s): <br>
- [Hummingbot Deploy on ClawHub](https://clawhub.ai/fengtality/hummingbot-deploy) <br>
- [Hummingbot API Docs](https://hummingbot.org/hummingbot-api/) <br>
- [Hummingbot MCP Docs](https://hummingbot.org/mcp/) <br>
- [Hummingbot API Repository](https://github.com/hummingbot/hummingbot-api) <br>
- [Hummingbot MCP Repository](https://github.com/hummingbot/mcp) <br>
- [Condor Repository](https://github.com/hummingbot/condor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, verification, upgrade, and troubleshooting instructions for Docker-based services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
