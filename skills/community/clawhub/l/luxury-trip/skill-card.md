## Description:

Design premium luxury travel experiences — first class flights, 5-star resorts, private tours, Michelin dining, and VIP access to exclusive venues, with support for related travel booking and itinerary tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to plan premium trips with first-class or business-class flights, five-star hotels, top-rated points of interest, private tours, and booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global flyai CLI package.

Mitigation: Use a pinned CLI version in an isolated environment and require review before installation.

Risk: The runbook can persist raw travel queries, which may include names, dates, budgets, passport details, or other private information.

Mitigation: Disable local log persistence or redact sensitive travel details before writing execution logs.

Risk: Results depend on a third-party travel CLI, external booking links, and commercial branding.

Mitigation: Show only CLI-returned results with detailUrl booking links, disclose unavailable sections, and have users verify pricing and booking terms before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/luxury-trip)
- [Publisher Profile](https://clawhub.ai/user/dingtom336-gif)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown comparison tables and retry guidance with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should come from flyai CLI output, include detailUrl booking links, preserve the user's language, and avoid raw JSON in the final response.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
