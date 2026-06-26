## Description: <br>
Browser automation CLI with Nstbrowser integration for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NstbrowserIO](https://clawhub.ai/user/NstbrowserIO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to manage Nstbrowser profiles, browser sessions, proxy settings, snapshots, screenshots, and batch profile operations through the nstbrowser-ai-agent CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes high-impact profile, proxy, persistence, and anti-detection controls. <br>
Mitigation: Restrict use to authorized Nstbrowser automation and require human confirmation before delete, clear, reset, stop-all, screenshot, snapshot, debugger, or batch profile operations. <br>
Risk: Shell templates and examples may include unsafe operational patterns or credential handling risks. <br>
Mitigation: Review or rewrite shell templates before running them, avoid command-line passwords, and keep API keys in approved local configuration or environment storage. <br>
Risk: Browser automation can be misused to evade access controls or impersonate users. <br>
Mitigation: Use the skill only for explicit, authorized browser automation tasks and do not use anti-detection features to bypass site policies or access controls. <br>


## Reference(s): <br>
- [Nstbrowser AI Agent ClawHub release](https://clawhub.ai/NstbrowserIO/nstbrowser-ai-agent) <br>
- [Nstbrowser website](https://www.nstbrowser.io/) <br>
- [npm package](https://www.npmjs.com/package/nstbrowser-ai-agent) <br>
- [Source repository](https://github.com/Nstbrowser/nstbrowser-ai-agent) <br>
- [NST API Reference](references/nst-api-reference.md) <br>
- [Profile Management Guide](references/profile-management.md) <br>
- [Proxy Configuration Guide](references/proxy-configuration.md) <br>
- [Batch Operations Guide](references/batch-operations.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that operate on local Nstbrowser profiles, proxies, browser sessions, screenshots, snapshots, and batch profile changes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
