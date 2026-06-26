## Description: <br>
Hermes Deployer guides developers through installing, configuring, deploying, and operating Hermes Agent on Linux servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy Hermes Agent as a long-running Linux server gateway, configure LLM providers and chat platform integrations, set up systemd operation, and troubleshoot runtime failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A long-running Hermes gateway can expose bot access or agent actions to unintended chat users. <br>
Mitigation: Restrict allowed users and channels before deployment, and avoid GATEWAY_ALLOW_ALL_USERS=true unless that exposure is intentional. <br>
Risk: LLM provider keys and bot tokens are stored in ~/.hermes/.env. <br>
Mitigation: Protect ~/.hermes/.env with restrictive filesystem permissions and rotate credentials if the server or bot channel is exposed. <br>
Risk: bypassPermissions can allow the deployed agent to act with broad local authority. <br>
Mitigation: Avoid bypassPermissions for production unless the operator has reviewed the command surface, server account permissions, monitoring, and rollback plan. <br>
Risk: Memory and auto-improvement features can persist or change behavior over time. <br>
Mitigation: Disable memory and auto-improvement until monitoring, audit, and rollback procedures are in place. <br>


## Reference(s): <br>
- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent) <br>
- [Weixin iLink platform](https://ilinkai.weixin.qq.com) <br>
- [Hermes Deployer ClawHub page](https://clawhub.ai/dengjiawei1226/hermes-deployer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, env, YAML, and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment, operations, upgrade, and troubleshooting guidance for Linux-hosted Hermes Agent gateways.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
