## Description:

Detects and maps complexity imbalances across system boundaries so developers can see where pressure is building and what may fail first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill during architecture design, review, and refactoring to identify uneven complexity distribution across modules, services, APIs, and layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad invocation wording may cause the skill to influence architecture review conversations where a narrower review scope was intended.

Mitigation: Use explicit activation criteria or reviewer confirmation when teams want this analysis only for designated architecture reviews.

Risk: Architecture recommendations may be misleading if the agent lacks current codebase metrics, ownership context, or design constraints.

Mitigation: Review recommendations against repository evidence, system metrics, and team constraints before using them to plan refactors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/osmotic-pressure)
- [Publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown architecture analysis with pressure maps, pattern summaries, diagnoses, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, network access, persistence, or credential handling is required by the skill evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
