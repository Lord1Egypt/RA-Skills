## Description:

Positioning Mapper helps launch teams build a Dunford-style positioning canvas with competitive alternatives, verifiable unique attributes, value themes, a scored beachhead segment, and a one-sentence onlyness statement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, launch, and product teams use this skill before launch copy is written to identify real alternatives, isolate defensible value, select a beachhead segment, and hand off positioning to downstream messaging work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the manifest understates that the skill may use web connectors and persistent memory writes.

Mitigation: Review it as requiring network access and scoped write permissions before deployment.

Risk: Competitor research may send queries through the host's Firecrawl or Tavily connectors.

Mitigation: Avoid submitting confidential positioning inputs to connector-backed research unless the host environment and data policy allow it.

Risk: Approved positioning, claim, and launch-stage data may be stored in named memory locations.

Mitigation: Require user approval for durable writes and review claim or launch-stage proposals before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/positioning-mapper)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown positioning canvas with tables and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed memory updates only after user approval.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
