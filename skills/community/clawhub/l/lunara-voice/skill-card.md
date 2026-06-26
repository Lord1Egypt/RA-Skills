## Description: <br>
Lunara Voice lets OpenClaw agents manage voice agents, campaigns, outbound calls, call history, analytics, webhooks, tags, and LLM data export through the LunaraVox API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunara9897-jpg](https://clawhub.ai/user/lunara9897-jpg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Businesses and operators use this skill to let OpenClaw agents place and manage AI phone calls and campaigns, then review transcripts, analytics, exports, tags, webhooks, and related API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can place outbound calls and start large campaigns from a configured Lunara Voice account. <br>
Mitigation: Restrict who can invoke call and campaign tools, and require manual confirmation before outbound calls or campaign starts. <br>
Risk: Call transcripts, analytics, and bulk exports may expose sensitive conversation data. <br>
Mitigation: Keep PII masking enabled by default and approve any transcript access or bulk export before use. <br>
Risk: API key management and webhook tools can change account access or send call events to external destinations. <br>
Mitigation: Use least-privilege API keys, restrict key-management tools, and approve webhook destinations before creation or update. <br>


## Reference(s): <br>
- [LunaraVox Homepage](https://lunaravox.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/lunara9897-jpg/lunara-voice) <br>
- [OpenClaw Plugin Manifest](artifact/plugin/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and text or JSON tool results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate calls, campaigns, transcript retrieval, analytics updates, exports, webhook operations, and API key management through configured LunaraVox credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; plugin artifact declares 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
