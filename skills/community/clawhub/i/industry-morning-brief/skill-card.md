## Description:

Generates sourced daily morning briefs for industry verticals by searching public web sources and synthesizing recent developments into a concise bulletin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and analysts use this skill to generate current, source-backed Markdown news briefs for industries such as new energy, EVs, solar, wind, hydrogen, semiconductors, and biotech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom industry queries may disclose sensitive topics to public search services.

Mitigation: Use only non-confidential industry terms and avoid private company plans, client names, or internal research topics in custom queries.

Risk: Fetched public headlines can be incomplete, stale, duplicated, or misleading.

Mitigation: Deduplicate sources, check publication dates, and keep final claims traceable to listed URLs before publishing the brief.

## Reference(s):

- [Sources by Industry](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/industry-morning-brief)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown brief with source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web fetching through curl; final brief should be deduplicated and grounded in listed source URLs.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
