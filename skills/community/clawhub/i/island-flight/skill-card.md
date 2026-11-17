## Description:

Fly to islands, search island destination flights and beach flights with tropical route booking, with related travel booking and planning support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search island and beach-destination flights through the flyai CLI, compare recommended, low-cost, direct, or connecting routes, and return booking-linked Markdown results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned third-party travel CLI, including fallback guidance that may use sudo.

Mitigation: Install the CLI manually in a scoped environment, pin and review the package source and version, and do not allow sudo or global installs during automated execution.

Risk: Flight searches can include sensitive travel details, and the artifact describes persisting raw user queries in a local execution log.

Mitigation: Disable or redact local logging for sensitive itineraries and avoid retaining origin, destination, travel dates, or user queries unless the user explicitly accepts that handling.

Risk: The skill depends on live CLI output and booking detailUrl links for accurate schedules, prices, and route details.

Mitigation: Treat results as unavailable if the CLI fails or lacks booking links, and do not substitute model knowledge for prices, schedules, transfers, or ferry details.

## Reference(s):

- [island-flight ClawHub release](https://clawhub.ai/dingtom336-gif/skills/island-flight)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, inline booking links, and CLI bash commands for execution or recovery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI results and detailUrl booking links; may maintain an internal execution log when file writes are available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
