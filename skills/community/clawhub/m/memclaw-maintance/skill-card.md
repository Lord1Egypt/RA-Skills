## Description: <br>
MemClaw Maintenance Guide provides installation, configuration, verification, troubleshooting, and maintenance guidance for the MemClaw OpenClaw memory plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, verify, troubleshoot, and maintain the MemClaw persistent memory plugin. Daily memory operations are directed to the separate memclaw skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation of the external @memclaw/memclaw plugin and persistent memory behavior. <br>
Mitigation: Install only if the publisher and plugin are trusted, and review the plugin configuration before enabling it at session startup. <br>
Risk: MemClaw configuration uses LLM and embedding provider API keys. <br>
Mitigation: Use protected provider API keys, keep openclaw.json private, and avoid sharing configuration files publicly. <br>
Risk: Persistent memory can retain sensitive user or project information. <br>
Mitigation: Avoid storing secrets in memory and review memory retention practices before using the skill in sensitive environments. <br>
Risk: The skill recommends AGENTS.md changes and scheduled maintenance behavior that can affect future sessions globally. <br>
Mitigation: Review AGENTS.md changes and disable or adjust scheduled maintenance if global behavior is not desired. <br>


## Reference(s): <br>
- [MemClaw maintenance troubleshooting guide](references/troubleshooting.md) <br>
- [MemClaw maintenance tools reference](references/tools.md) <br>
- [memclaw daily-usage skill](https://clawhub.ai/sopaco/memclaw) <br>
- [MemClaw project repository](https://github.com/sopaco/cortex-mem) <br>
- [MemClaw plugin README](https://raw.githubusercontent.com/sopaco/cortex-mem/refs/heads/main/examples/%40memclaw/plugin/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation steps, OpenClaw configuration examples, maintenance tool examples, service checks, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.9.31 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
