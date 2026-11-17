## Description:

OpenForge executes structured PRDs through staged phases with model routing, parallel sub-agents, validation gates, review-to-fix loops, and escalation in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use OpenForge to turn reviewed PRD markdown into phased implementation work, route phases across model tiers, run validation gates, and perform review-to-fix cycles inside an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PRD-supplied gate commands can run in the workspace with weak execution boundaries.

Mitigation: Review every Gate and Shell-Gate entry, prefer a dry run first, and run only trusted PRDs in a controlled workspace.

Risk: Spawned agents can change workspace files while executing implementation phases.

Mitigation: Use a disposable branch or sandbox for important work and review resulting diffs before keeping changes.

Risk: PRD content is passed to agents and could expose embedded secrets.

Mitigation: Do not put credentials, API keys, or secrets in PRD files; keep sensitive values in the environment or another managed secret store.

## Reference(s):

- [OpenForge Skill Source](artifact/SKILL.md)
- [OpenForge Changelog](artifact/CHANGELOG.md)
- [ClawHub Skill Page](https://clawhub.ai/corbin-breton/skills/openforge)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries and review reports, code and configuration file edits, and shell command execution results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .openforge/run-{timestamp}.md after successful runs when a working directory is specified.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
