## Description:

Read MaxPreps.com high school sports data — find a school, then get team schedules, scores, records, rosters, stat leaders, rankings, and athlete careers for any US high school.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up public sports information for a named US high school or team, including schedules, scores, rosters, rankings, and athlete careers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to MaxPreps page data or seasonal availability can make decoded results stale or empty.

Mitigation: For empty or unexpected results, check the current MaxPreps page and season history; use the skill's school and team lookup steps to resolve canonical paths.

## Reference(s):

- [MaxPreps](https://www.maxpreps.com)
- [MaxPreps MCP project (related tools)](https://github.com/chrischall/maxpreps-mcp)
- [Recipes](artifact/references/recipes.md)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/maxpreps-mcp)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON sports data and Markdown usage guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be piped to jq for filtering and summaries.]

## Skill Version(s):

1.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
