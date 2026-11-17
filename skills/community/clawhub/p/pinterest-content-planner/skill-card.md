## Description:

Plans Pinterest pins by board and season with platform-length copy and tracked links for US sellers, shops, and lifestyle bloggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US Pinterest sellers, ecommerce shops, and lifestyle bloggers use the skill to plan pins by board and season, draft platform-length titles and descriptions, and prepare tracked destination links and seasonal timing.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The link-building script uses a placeholder destination and expects input columns that may not match the supplied template, which can produce missing or incorrect tracked links.

Mitigation: Set the real destination and reconcile the CSV headers with the script before running; check every generated link in a fresh output folder.

Risk: Pin content could reuse material without permission or omit disclosure for affiliate links.

Mitigation: Use only content the user has rights to and clearly disclose material connections, including affiliate links.

## Reference(s):

- [Pinterest pin limits and board planning](references/pinterest-pin-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/pinterest-content-planner)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Dated pin plans, pin titles and descriptions, tracked links, and seasonal guidance in Markdown or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pin titles are under 100 characters and descriptions under 800 characters; link reports include UTM-tagged destinations.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
