## Description:

Guides commerce teams through turning competitor ad-material data into a scenario opportunity map using scenario labels, volume, GMV, efficiency, and strategic scenario layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce, marketing, and brand strategy users can use this skill to analyze competitor content data, classify demand scenarios, compare GMV efficiency, and decide which scenarios to prioritize. The skill is designed for structured strategic guidance rather than raw data collection or scriptwriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may display promotional contact information on first use.

Mitigation: Review the first-run behavior before installation and remove or block promotional output if it is not acceptable for the deployment environment.

Risk: The skill may persist onboarding state and analysis deliverables locally.

Mitigation: Run it only in workspaces where local persistence is acceptable, and instruct the agent not to create or update archives when records should not be retained.

Risk: Users may provide confidential product, competitor, sales, or GMV data for analysis.

Mitigation: Use approved data-handling practices, avoid unnecessary sensitive details, and review outputs before sharing them outside the intended team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-changjing)
- [ClawHub publisher profile](https://clawhub.ai/user/handsomeng)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown with structured tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local brand archive files when the user agrees to persistence.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
