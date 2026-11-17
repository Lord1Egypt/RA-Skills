## Description:

Multi-provider LLM assignment system for agents supporting cloud providers and local models, with user-defined providers, local-model discovery, YAML configuration, and task-based model routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msonline1110](https://clawhub.ai/user/msonline1110)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure cloud and local LLM providers, assign preferred models to agents, and route tasks by cost, latency, quality, or task type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provider manager can probe configured local model endpoints during discovery.

Mitigation: Restrict discovery endpoints to trusted localhost services and review endpoint configuration before running scans.

Risk: Provider configuration can include API keys or references to credential environment variables.

Mitigation: Use environment variables instead of inline api_key values, do not share real config files, and rotate any key that was committed or shared.

Risk: Running the management scripts can write local configuration or cache files.

Mitigation: Run scripts only against trusted configuration files and add runtime config and cache paths to the local .gitignore.

## Reference(s):

- [OpenClaw Smart Agent Hub on ClawHub](https://clawhub.ai/msonline1110/skills/oc-smart-agent-hub)
- [OpenClaw homepage](https://github.com/openclaw/openclaw)
- [English documentation](docs/README_en.md)
- [Chinese documentation](docs/README_zh.md)
- [Security notice](SECURITY_NOTICE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration and cache files when its bundled management scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, and VERSION_CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
