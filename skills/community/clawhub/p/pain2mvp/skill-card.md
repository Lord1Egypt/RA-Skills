## Description:

Discover and structure product opportunities from public user discussions, then convert top opportunities into a lightweight PRD for a coding agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-weijie](https://clawhub.ai/user/zhao-weijie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product builders, and product researchers use this skill to find recurring public pain points, rank product opportunities, and turn a persisted opportunity into a lightweight PRD for a coding agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores source URLs, author handles, evidence snippets, ranked opportunities, and PRD drafts in the configured TiDB database.

Mitigation: Use only a TiDB database intended for this skill, avoid saving private or sensitive user content, and review database retention and access controls.

Risk: Weak or contradictory public-discussion evidence can produce misleading opportunity rankings or PRD direction.

Mitigation: Preserve contradictions, mark weak findings as insufficient evidence, and review ranked opportunities before using generated PRDs for implementation.

## Reference(s):

- [Painpoint To PRD Contracts](references/contracts.md)
- [ClawHub Skill Page](https://clawhub.ai/zhao-weijie/skills/pain2mvp)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown summaries and PRDs with JSON persistence payloads and command-line helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TiDB-backed persistence for evidence rows, ranked opportunities, and PRD records.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
