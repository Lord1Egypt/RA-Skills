## Description:

Luxury Escape helps agents design premium travel experiences with flights, luxury hotels, attractions, itinerary support, and booking links sourced from flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-focused agents use this skill to plan premium trips, compare real-time travel options, and produce booking-ready recommendations from flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and rely on a global third-party npm CLI.

Mitigation: Install only in a constrained environment after trusting the flyai CLI, and prefer pinned, verified dependency installation.

Risk: Provider-controlled booking links may route users to external booking destinations.

Mitigation: Validate booking URLs before use and review recommendations before clicking or sharing them.

Risk: Travel requests and itinerary details may be logged locally.

Mitigation: Avoid entering sensitive personal details and disable or redact persistent logs by default.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/luxury-escape)
- [Publisher Profile](https://clawhub.ai/user/xiejinsong)
- [Output Templates](artifact/references/templates.md)
- [Luxury Travel Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and occasional inline shell commands for setup or retry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to come from flyai CLI output and booking links are expected to use detailUrl values.]

## Skill Version(s):

3.2.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
