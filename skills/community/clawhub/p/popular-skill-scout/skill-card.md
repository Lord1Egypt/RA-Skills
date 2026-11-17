## Description:

Find popular and practical skills across ClawHub and GitHub for concrete workflows, then return verified shortlists with usefulness, popularity, maintenance, and safety notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanziwen100](https://clawhub.ai/user/yuanziwen100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to discover practical agent skills for a specific workflow and compare candidates using current ClawHub and GitHub signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest ClawHub CLI fallback commands such as unpinned npx execution.

Mitigation: Ask the agent to avoid unpinned npx and to show exact commands before running any CLI fallback.

Risk: The skill may recommend trial-installing or running third-party skills.

Mitigation: Review the selected skill, required commands, and publisher details first, then test only in a disposable or tightly scoped environment.

Risk: Marketplace recommendations can be affected by stale popularity, unclear provenance, or suspicious flags.

Mitigation: Require live verification of ClawHub details, upstream source, maintenance, and safety notes before treating a candidate as a strong recommendation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanziwen100/skills/popular-skill-scout)
- [Sources And Queries](references/sources-and-queries.md)
- [Query Templates](references/query-templates.md)
- [Ranking Rubric](references/ranking-rubric.md)
- [Current Seeds](references/current-seeds.md)
- [ClawHub Skills Browse](https://clawhub.ai/skills?nonSuspicious=true)
- [OpenClaw Directory](https://www.openclawdirectory.dev/skills)
- [LobeHub Skills Marketplace](https://lobehub.com/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown shortlist with structured recommendation fields and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended, worth-inspecting, and skip sections with verification and safety notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
