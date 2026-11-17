## Description:

Local-first privacy-first inference. Your OpenClaw agent thinks locally and asks the cloud intelligently. Saves 85%+ tokens, protects privacy, agent learns from cloud responses--cloud doesn't learn from you.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivaclaw](https://clawhub.ai/user/shivaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to route agent queries through local Ollama inference first, with optional cloud fallback for queries that need external model support. It is intended for cost-conscious and privacy-sensitive agent deployments that can review and configure the cloud boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud fallback may receive raw user queries or insufficiently stripped context despite the stated privacy guarantee.

Mitigation: Use local-only mode unless cloud providers are approved for the workload, and review audit logs before relying on the privacy boundary for sensitive or regulated data.

Risk: Docker services and local model endpoints can expose data or control surfaces if bound beyond the local host.

Mitigation: Bind Ollama and related services to localhost or a private network, restrict access with firewall rules, and avoid exposing model endpoints publicly.

Risk: Unpinned latest-tag container images and shared service credentials can make deployments harder to audit and reproduce.

Mitigation: Pin container image versions, use unique service credentials, and rotate any defaults before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shivaclaw/skills/project-nirvana-plugin)
- [GitHub repository](https://github.com/ShivaClaw/nirvana-plugin)
- [GitHub issues](https://github.com/ShivaClaw/nirvana-plugin/issues)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [Natural-language agent responses with JSON routing metadata, configuration examples, and audit records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes requests to local Ollama or optional cloud fallback; caches responses and records routing, privacy, and performance events.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
