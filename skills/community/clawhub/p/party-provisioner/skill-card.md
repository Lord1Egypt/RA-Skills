## Description:

Calculate exact quantities of drinks, ice, food, glassware, and supplies for parties and events from headcount, duration, guest mix, and weather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and hosting planners use this skill to estimate party shopping quantities for drinks, ice, food, supplies, and optional budget checks from guest count, duration, guest mix, party style, and weather.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alcohol purchase estimates may be misread as encouragement to over-serve or as a substitute for local alcohol-law compliance.

Mitigation: Treat outputs as planning guidance only; follow local laws and responsible-hosting practices, including visible water, food, ending service before the event ends, and transportation planning.

Risk: Shopping quantities can be wrong when guest count, event duration, drinker mix, weather, or food style inputs are inaccurate.

Mitigation: Review the generated shopping list against actual attendees, dietary needs, venue constraints, and local product sizes before buying.

## Reference(s):

- [Party Provisioning Reference](references/provisioning-math.md)
- [ClawHub party-provisioner release page](https://clawhub.ai/voronindenis5/skills/party-provisioner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style text with inline shell commands and structured shopping-list quantities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are estimates rounded to purchasable units; users can refine quantities with event-specific inputs and local prices.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
