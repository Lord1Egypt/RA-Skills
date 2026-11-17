## Description:

Get a customized packing list based on your destination, season, trip type, and activities. Never forget essentials again. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to answer packing-list and travel-essentials requests by collecting trip details, running flyai search commands, and formatting retrieved results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and use a third-party travel CLI.

Mitigation: Review and approve the npm package before installation, and avoid automatic global installs unless the execution environment explicitly permits them.

Risk: Travel-planning requests may include sensitive itinerary, identity, visa, payment, or booking-reference details, and the artifact describes raw-query execution logging.

Mitigation: Do not use the skill with sensitive travel or identity details unless logging and query disclosure are removed or tightly controlled.

Risk: The skill requires flyai or Fliggy-style search results and booking links, which can bias responses toward commercial booking outputs.

Mitigation: Review generated results for relevance, clearly report retrieval failures, and avoid fabricating prices, venues, or travel details.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Packing List Playbooks](references/playbooks.md)
- [Fallback Procedures](references/fallbacks.md)
- [Execution Log Schema](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include detailUrl booking links when results are shown, and follow the user's language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
