## Description: <br>
Guides agents to answer OpenClaw product, configuration, API, skill development, and troubleshooting questions by checking the official OpenClaw documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uynewnas](https://clawhub.ai/user/uynewnas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to locate official documentation, produce source-linked answers, and provide actionable steps for OpenClaw configuration, APIs, skills, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw answers can become stale or incorrect if the agent relies on memory instead of current documentation. <br>
Mitigation: Verify each OpenClaw answer against the official documentation, include source links and version or date context when available, and state clearly when the documentation does not answer the question. <br>
Risk: Suggested commands or configuration changes can affect local services, deployment settings, or security-sensitive production behavior. <br>
Mitigation: Review commands and configuration changes before running them, especially examples involving restarts, Docker deployment, local APIs, or production security settings. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw Getting Started](https://docs.openclaw.ai/getting-started) <br>
- [OpenClaw Gateway Configuration](https://docs.openclaw.ai/configuration/gateway) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/skills) <br>
- [OpenClaw API Reference](https://docs.openclaw.ai/api) <br>
- [OpenClaw Troubleshooting](https://docs.openclaw.ai/troubleshooting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown answers with source links and optional code or shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires web access for documentation verification and should include source URLs plus validity notes when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
