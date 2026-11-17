## Description:

Model Router Manager is a local OpenClaw configuration helper for setting primary and fallback model chains and selecting cost, speed, or quality routing preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsdadad](https://clawhub.ai/user/zsdadad)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure OpenClaw model routing preferences, fallback model lists, and local usage statistics through shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises automatic routing, failover, cost savings, cost monitoring, and API integration capabilities that are not proven by the included script.

Mitigation: Use it as a lightweight local configuration helper and independently test routing, failover, statistics, and cost behavior before relying on those claims.

Risk: Model provider credentials or API keys could be exposed if users place them in unprotected local configuration files.

Mitigation: Keep secrets in protected environment variables or a managed secret store, and avoid writing API keys into the model-router configuration file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsdadad/skills/model-router-manager)
- [Declared project homepage](https://github.com/myboxstorage/model-router-manager)
- [Moltbook feedback page](https://www.moltbook.com/m/agentskills)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local model-router JSON configuration file for OpenClaw-oriented workflows.]

## Skill Version(s):

1.0.0 (source: release metadata, skill.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
