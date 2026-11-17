## Description:

Intelligent model routing for sub-agent task delegation based on task complexity, cost, and capability requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicocabrerac](https://clawhub.ai/user/nicocabrerac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to classify agent tasks and select model tiers for sub-agent spawns, cron jobs, and routing policy checks so routine work can use cheaper models while complex or critical work uses stronger models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can persistently influence future agent model selection by patching AGENTS.md.

Mitigation: Review the proposed AGENTS.md changes before running install.sh and install only when persistent routing enforcement is intended.

Risk: Optional hourly automation can perform repeated live provider probes and rewrite model configuration.

Mitigation: Avoid enabling the hourly cron unless repeated probes and automated configuration updates are acceptable for the workspace.

Risk: Model discovery performs credentialed provider checks.

Mitigation: Validate provider base URLs and configuration before using discovery with real API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicocabrerac/skills/intelligent-router-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend model IDs, spawn payload snippets, audit results, provider health checks, and configuration updates.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 3.2.0, README reports 2.0.0, and _meta.json reports 3.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
