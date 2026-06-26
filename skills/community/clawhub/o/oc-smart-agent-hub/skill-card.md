## Description: <br>
Multi-provider LLM assignment system for agents supporting cloud providers, local models, user-defined providers, auto-discovery, zero-code configuration, and task-based model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msonline1110](https://clawhub.ai/user/msonline1110) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and route agent workloads across multiple cloud and local LLM providers. It helps assign models by agent role or task type while considering cost, latency, quality, and fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider configuration may expose API keys if users place credentials directly in config/models.yaml or share local configuration files. <br>
Mitigation: Use environment variables for API keys, keep config/models.yaml out of version control, and remove or replace credentials before sharing configuration. <br>
Risk: Local model discovery can contact local endpoints and reveal or depend on services running in the user's workspace or network environment. <br>
Mitigation: Review local_discovery endpoints and only run discovery commands in a controlled environment where local model services are expected. <br>
Risk: The skill includes Python scripts and third-party dependencies for provider management and routing. <br>
Mitigation: Review scripts before execution and install dependencies in a controlled environment, especially in sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/msonline1110/oc-smart-agent-hub) <br>
- [OpenClaw Homepage](https://github.com/openclaw/openclaw) <br>
- [English Documentation](docs/README_en.md) <br>
- [Chinese Documentation](docs/README_zh.md) <br>
- [Security Notice](SECURITY_NOTICE.md) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance, code] <br>
**Output Format:** [Markdown guidance with YAML configuration examples, Python command examples, and supporting script files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference provider API keys through environment variables and may scan configured local model endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
