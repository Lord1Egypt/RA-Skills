## Description:

Systematic deep research methodology for any domain using a 7-step workflow with credibility scoring, pattern recognition, adversarial analysis, iterative deepening, and cited report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustyorb](https://clawhub.ai/user/rustyorb)

### License/Terms of Use:

Personal research tool. Not for redistribution without K's authorization.

## Use Case:

External users, developers, and research-focused agents use this skill to structure deep investigations across domains, gather and score sources, preserve uncertainty and contradictions, and produce Obsidian-ready Markdown reports with YAML frontmatter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local-note and filesystem access could expose personal or workspace data during research.

Mitigation: Run the skill in a tightly sandboxed workspace and approve any filesystem locations explicitly before use.

Risk: Always-active activation and recurring automation can trigger research or state changes without enough user control.

Mitigation: Disable or narrow alwaysActive behavior and require confirmation before enabling cron, heartbeat, sub-agent, notification, MEMORY.md, or TASKS.md actions.

Risk: The bundled sourcing guidance references a hard-coded private SearXNG endpoint.

Mitigation: Configure search endpoints explicitly for the deployment environment and avoid using the hard-coded private address.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rustyorb/skills/k-deep-research)
- [Sourcing Strategies](references/sourcing-strategies.md)
- [Research Frameworks](references/research-frameworks.md)
- [Output Templates](references/output-templates.md)
- [OpenClaw Architecture](references/openclaw-architecture.md)
- [OpenClaw Skill Authoring](references/openclaw-skill-authoring.md)
- [Autonomy Patterns](references/autonomy-patterns.md)
- [Adversarial Analysis](references/adversarial-analysis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Obsidian-ready Markdown reports with YAML frontmatter, citations, credibility scores, synthesis, appendices, and investigation follow-ups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce long-form reports and may suggest filesystem, search, cron, heartbeat, memory, task registry, sub-agent, or notification actions when used in OpenClaw contexts.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and README state 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
