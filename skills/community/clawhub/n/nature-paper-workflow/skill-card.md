## Description:

Routes academic paper workflow requests to installed sub-skills by identifying the discipline, workflow phase, and handoff needs across STEM and economics branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic writing assistants use this skill to classify paper-workflow requests, route them to specialized sub-skills, and keep phase handoffs clear for STEM and economics manuscripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Econ sub-skills are referenced from an unpinned third-party GitHub repository that can change after review.

Mitigation: Review and pin the Econ extension to a specific commit or release before installation, then verify the files before copying them into ~/.claude/skills.

Risk: Ambiguous academic requests may be routed to the wrong discipline branch, venue profile, or language workflow.

Mitigation: Confirm the branch, target venue, and language choice with the user when signals conflict or are unclear.

## Reference(s):

- [Skill page](https://clawhub.ai/edwardwason/skills/nature-paper-workflow)
- [discipline-routing.md](references/discipline-routing.md)
- [econ-workflow.md](references/econ-workflow.md)
- [workflow-map.md](references/workflow-map.md)
- [trigger-map.md](references/trigger-map.md)
- [skill-map.md](references/skill-map.md)
- [sub-skill-protocol.md](references/sub-skill-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with routing decisions, phase labels, handoff notes, and optional installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Router-only behavior; actual writing, analysis, file operations, and external tool use are delegated to installed sub-skills.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
