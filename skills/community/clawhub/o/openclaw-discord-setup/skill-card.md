## Description: <br>
Guides users through configuring a Discord bot as an OpenClaw messaging channel, including bot creation, server authorization, OpenClaw configuration, slash commands, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect OpenClaw to Discord for server-based messaging, slash commands, direct messages, and formatted responses. It is most useful when setting up a Discord bot channel and validating permissions, tokens, and gateway behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot tokens can be exposed if copied into public files or shared during setup help. <br>
Mitigation: Use a dedicated bot token, store it outside public files, avoid sharing credentials, and rotate the token if exposure is suspected. <br>
Risk: The bot may receive messages from unintended servers or direct-message contexts if access is too broad. <br>
Mitigation: Restrict allowedGuildIds to trusted servers and keep direct messages disabled unless consent, access controls, and data-handling expectations are clear. <br>


## Reference(s): <br>
- [Openclaw Discord Setup on ClawHub](https://clawhub.ai/yang1002378395-cmyk/openclaw-discord-setup) <br>
- [Discord Developer Portal Applications](https://discord.com/developers/applications) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, configuration examples, troubleshooting notes, and security recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, artifact footer) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
