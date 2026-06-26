## Description: <br>
Jarvis deploys a local-first OpenClaw executive assistant persona and workspace for Dell Pro Max GB10 and NVIDIA DGX Spark systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gignaati](https://clawhub.ai/user/gignaati) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, executives, enterprise teams, and developers use this skill to configure an on-premise OpenClaw agent for operations, communications, research, memory, and system monitoring on GB10 or DGX Spark hardware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the setup understates network behavior. <br>
Mitigation: Bind services to localhost or VPN-only interfaces, keep dashboards off the public internet, and review firewall exposure before enabling remote access. <br>
Risk: Credential handling can expose business or personal accounts if integrations are configured broadly. <br>
Mitigation: Use dedicated low-privilege accounts for email, calendar, search, and messaging integrations, and avoid storing API keys in shell startup files such as ~/.bashrc. <br>
Risk: Always-on heartbeat and persistence can retain or act on sensitive workspace memory. <br>
Mitigation: Keep heartbeat disabled until tested, treat OpenClaw workspace memory as sensitive data, and prune or approve memory writes before using the skill with personal, client, or confidential business information. <br>
Risk: The security evidence calls for manual review of the skill's security claims before installation. <br>
Mitigation: Review the templates and scripts before deployment, customize them for the organization, and scan or audit the release before using it in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gignaati/jarvis-chief-of-ai-staff) <br>
- [Gignaati homepage](https://gignaati.com) <br>
- [NVIDIA DGX Spark OpenClaw Playbook](https://build.nvidia.com/spark/openclaw) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security) <br>
- [Qwen3.5 + OpenClaw on GB10 Guide](https://github.com/ZengboJamesWang/Qwen3.5-35B-A3B-openclaw-dgx-spark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw workspace templates and local deployment and security-hardening scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
