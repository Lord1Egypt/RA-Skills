## Description:

Discovers premium 5-star hotels and luxury resorts using flyai CLI results, with support for related Fliggy travel services such as flights, train tickets, itinerary planning, visas, insurance, and car rental.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to retrieve real-time luxury hotel recommendations, compare options, and return booking-ready Markdown sourced from flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned globally installed third-party travel CLI.

Mitigation: Install and run it in an isolated environment, review the package and version before use, and avoid granting broader system access than needed.

Risk: User travel details are turned into shell commands for live lookup.

Mitigation: Validate destination, date, price, and keyword values before command execution and avoid including sensitive personal or payment information.

Risk: The runbook describes optional persistence of raw request logs.

Mitigation: Disable or remove the local execution log unless retention is explicitly required, and avoid storing sensitive travel details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/luxury-hotel)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with comparison tables, booking links, concise guidance, and inline shell commands when setup or retries are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI results; hotel recommendations must include booking links and a flyai-powered brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
