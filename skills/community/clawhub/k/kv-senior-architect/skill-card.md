## Description:

Design system architecture, evaluate patterns, and produce architecture artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or review system architecture, choose architecture and technology patterns, generate diagrams, write ADRs, analyze dependencies, and assess scalability or domain boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project directories supplied by the user for diagram generation, dependency analysis, and architecture assessment.

Mitigation: Run the skill only on project directories intended for review and avoid including unrelated sensitive files in the analyzed path.

Risk: The local scripts support output or save paths that can replace existing files.

Mitigation: Choose explicit output paths in a scratch or generated-artifacts directory and review them before rerunning commands.

Risk: Generated Mermaid or PlantUML from untrusted repositories may be unsafe to render in privileged tooling.

Mitigation: Render diagrams from untrusted repositories in a restricted renderer without sensitive network or filesystem access.

## Reference(s):

- [Arquitecto Senior ClawHub Skill Page](https://clawhub.ai/felix-antonio-sl/skills/kv-senior-architect)
- [Architecture Patterns Reference](references/architecture_patterns.md)
- [System Design Workflows](references/system_design_workflows.md)
- [Technology Decision Guide](references/tech_decision_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with diagrams, ADRs, assessment reports, command examples, and optional JSON outputs from local analysis scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One primary architecture artifact per response; scripts can emit Mermaid, PlantUML, ASCII, JSON, or text reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
