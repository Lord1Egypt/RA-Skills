## Description: <br>
Set up OpenViking context database for OpenClaw agents with filesystem-based memory management, tiered context loading, and persistent agent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engsathiago](https://clawhub.ai/user/engsathiago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure OpenViking as a context database for OpenClaw agents, including workspace setup, provider configuration, tiered memory settings, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can run a remote shell installer for the OpenViking CLI. <br>
Mitigation: Review the installer before execution and prefer a pinned or verified OpenViking release when possible. <br>
Risk: OpenViking configuration examples store provider API keys in a local config file. <br>
Mitigation: Restrict permissions on local configuration files and avoid storing raw API keys in plaintext when a secret manager or environment-based configuration is available. <br>
Risk: The health check can write a test entry into the configured memory store. <br>
Mitigation: Run health checks against a non-production workspace unless adding a test memory entry is acceptable. <br>


## Reference(s): <br>
- [OpenViking Examples](references/examples.md) <br>
- [OpenViking GitHub Repository](https://github.com/volcengine/OpenViking) <br>
- [OpenViking Documentation](https://github.com/volcengine/OpenViking/tree/main/docs) <br>
- [OpenViking OpenClaw Plugin](https://github.com/volcengine/OpenViking/tree/main/plugins/openclaw) <br>
- [OpenViking Examples](https://github.com/volcengine/OpenViking/tree/main/examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, JSON, YAML, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide local setup commands, configuration examples, and health-check guidance for OpenViking and OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
