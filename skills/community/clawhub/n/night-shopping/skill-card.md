## Description:

Find night markets, food streets, and local culinary hotspots. Discover street food, local specialties, and the best evening food experiences. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search FlyAI/Fliggy for night markets, food streets, and late-night food venues in a requested city, then present concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running the FlyAI CLI globally.

Mitigation: Use a version-pinned, user-approved CLI install in an isolated environment before allowing execution.

Risk: Travel searches are sent through the FlyAI/Fliggy provider and results include provider-selected booking links.

Mitigation: Tell users that live travel data and booking links come from provider output, and have them review destinations and URLs before booking.

Risk: The skill can persist raw user queries in a local execution log when filesystem writes are available.

Mitigation: Disable, redact, or regularly delete local logs that may contain sensitive travel queries.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output; does not expose raw JSON; includes provider-selected booking links when results are available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
