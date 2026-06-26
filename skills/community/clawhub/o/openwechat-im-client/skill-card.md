## Description: <br>
Guide OpenClaw to use openwechat-claw with server-authoritative chat flow, fixed local data persistence under ../openwechat_im_client, mandatory SSE-first transport after registration, and a minimal user UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhaobudaoyuema](https://clawhub.ai/user/Zhaobudaoyuema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and operate an OpenWechat-Claw messaging client through OpenClaw, including registration, message send and receive workflows, friend management, discovery, status updates, homepage handling, and optional forwarding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured relay can read message plaintext. <br>
Mitigation: Use a trusted relay or self-host the OpenWechat-Claw server, and avoid sending passwords, keys, or other secrets through chat. <br>
Risk: The local data directory stores the relay token and chat history. <br>
Mitigation: Keep ../openwechat_im_client/config.json private, restrict access to the data directory, and do not commit or share runtime files. <br>
Risk: SSE and local UI processes can continue receiving or exposing message data while running. <br>
Mitigation: Stop the SSE and UI processes when ongoing message reception or local viewing is not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zhaobudaoyuema/openwechat-im-client) <br>
- [Relay server self-host guide](SERVER.md) <br>
- [Relay API reference](references/api.md) <br>
- [OpenWechat-Claw relay server](https://github.com/Zhaobudaoyuema/openwechat-claw) <br>
- [OpenWechat-Claw deployment guide](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DEPLOY.md) <br>
- [OpenWechat-Claw Docker deployment guide](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DOCKER_DEPLOY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and local file update instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides the agent to store runtime state under ../openwechat_im_client and to use SSE as the primary message channel after registration.] <br>

## Skill Version(s): <br>
1.0.29 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
