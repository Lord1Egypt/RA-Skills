## Description:

Processes external resources into stored knowledge with quality scoring and routing

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess external articles, papers, and documents, decide whether and where to store useful knowledge, and connect it to existing knowledge structures. It also guides quality review, discussion promotion, application routing, and curator-approved tidying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External knowledge may be published to GitHub Discussions by default or influence skill and agent updates without an approval gate.

Mitigation: Require explicit user approval before publishing ingested content or applying changes to skills and agent instructions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-memory-palace-knowledge-intake)
- [Memory Palace project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [KonMari method](https://konmari.com/about-the-konmari-method/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Structured Markdown knowledge entries, evaluation and routing recommendations, and optional GitHub GraphQL commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Knowledge storage and application suggestions; tidying changes require explicit curator approval.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
