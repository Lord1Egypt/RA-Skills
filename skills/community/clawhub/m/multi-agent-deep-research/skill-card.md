## Description:

Coordinate deep, source-verifiable research projects in OpenClaw using AgentSkills-compatible folders, local artifact tracking, and explicit evidence ledgers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzxx-bit](https://clawhub.ai/user/zzxx-bit)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, researchers, and research teams use this skill to run auditable deep-research workflows with local project state, source ledgers, claim ledgers, handoffs, and final reports that separate facts, interpretations, comparisons, and forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to create local project folders and files in the active workspace.

Mitigation: Review the proposed project root and file scaffold before execution, and keep generated research artifacts inside the intended workspace.

Risk: Research reports can become misleading if unsupported claims, stale facts, or incomparable metrics are promoted into final prose.

Mitigation: Use the source ledger, claim ledger, cutoff date, comparability notes, and QA gates before drafting or publishing conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zzxx-bit/skills/multi-agent-deep-research)
- [Project Layout](artifact/references/project-layout.md)
- [Delegation Patterns](artifact/references/delegation-patterns.md)
- [Evidence Standards](artifact/references/evidence-standards.md)
- [Starter Templates](artifact/references/templates.md)
- [OpenClaw Platform Notes](artifact/references/platform-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file paths, workflow steps, ledger templates, and handoff templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When followed by an agent, the skill creates local research project folders, ledgers, handoffs, and report drafts in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
