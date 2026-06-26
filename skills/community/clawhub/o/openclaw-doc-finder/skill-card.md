## Description: <br>
OpenClaw Doc Finder routes OpenClaw configuration, maintenance, troubleshooting, channel, skill, model, and deployment questions to relevant official documentation, URLs, commands, and configuration snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mslclaw](https://clawhub.ai/user/mslclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw setup, configuration, troubleshooting, channel integration, skill installation, model provider, CLI, gateway, remote access, and security questions with official documentation links and actionable snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch OpenClaw documentation remotely and use curl as a fallback. <br>
Mitigation: Review fetched content and generated commands before using them, and avoid remote-fetch fallbacks in restricted environments. <br>
Risk: The skill can run a bundled version-sync script that updates local reference and version files. <br>
Mitigation: Use the dry-run mode first and review file changes before allowing synchronization. <br>
Risk: Lookup questions and fetched pages may be retained locally. <br>
Mitigation: Do not include secrets, internal hostnames, or incident details in questions unless local retention is acceptable. <br>
Risk: Troubleshooting examples include token, API key, and .env handling. <br>
Mitigation: Redact secrets before sharing terminal output and keep environment files protected with restricted permissions. <br>


## Reference(s): <br>
- [OpenClaw Doc Finder release page](https://clawhub.ai/mslclaw/openclaw-doc-finder) <br>
- [OpenClaw document index](references/doc-index.md) <br>
- [OpenClaw diagnostic tree](references/diagnostic-tree.md) <br>
- [Gateway configuration guide](references/config-guide.md) <br>
- [Troubleshooting quick reference](references/troubleshoot.md) <br>
- [Prior document lookups](references/doc-lookups.md) <br>
- [Gateway configuration examples](https://docs.openclaw.ai/gateway/configuration-examples) <br>
- [Channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting) <br>
- [Secrets management](https://docs.openclaw.ai/gateway/secrets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown answers with official documentation URLs, fenced shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache fetched documentation and append lookup notes for future reuse.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and skill CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
