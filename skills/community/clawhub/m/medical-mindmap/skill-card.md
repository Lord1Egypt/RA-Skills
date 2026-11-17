## Description:

Supports local management of neurology and EEG-oriented medical knowledge as entities, relationships, facts, and structured summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[languang2026](https://clawhub.ai/user/languang2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, clinicians, students, and medical learners can use this skill to organize neurology and EEG study notes into a local knowledge graph and generate structured Markdown summaries. It is best treated as a note-taking and study aid, not as a clinical decision system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review found that the skill overstates EEG-analysis capabilities.

Mitigation: Present outputs as study notes or organizer-generated summaries, and require qualified medical review before using any content for health or clinical decisions.

Risk: The skill persists user-provided knowledge locally and may be used with sensitive health information.

Mitigation: Avoid storing patient-identifiable or sensitive health information unless local disk persistence is acceptable for the deployment environment.

Risk: Installation references include mutable or placeholder sources.

Mitigation: Install from a pinned, verified source and review the package contents before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/languang2026/skills/medical-mindmap)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, shell commands, and local JSON-backed knowledge records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may persist user-provided knowledge to local disk under a memory/mindmap directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
