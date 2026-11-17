## Description:

Timezone-aware NBA daily intelligence using bundled public ESPN/NBA fetchers plus official NBA injury-report PDFs, with compact day fast path, same-day stats, phase-specific game routes, stronger single-game live detail, independent official-report summaries, refresh-safe follow-ups, and direct tool-output delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhjsnsnsk](https://clawhub.ai/user/hhjsnsnsk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer NBA schedule, live-game, postgame, player-stat, injury-report, and official-report questions using public NBA and ESPN sources. It is intended for concise sports intelligence in English or Chinese while keeping relative dates grounded in the requestor's timezone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound data fetching may reach broader network destinations than the public documentation describes.

Mitigation: Run with outbound access restricted to known NBA and ESPN hosts, and block loopback, private, and link-local destinations.

Risk: Provider override environment variables could redirect public sports-data requests.

Mitigation: Avoid setting provider override environment variables in production; provide only the documented timezone configuration inputs.

Risk: Remote NBA pages and injury-report PDFs are parsed as external input.

Mitigation: Treat fetched sports content as untrusted, keep execution sandboxed, and review outputs before using them in sensitive decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhjsnsnsk/skills/nba-today-pulse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown sports reports and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are compact, timezone-aware, and routed by request type; no credentials are required.]

## Skill Version(s):

1.0.15 (source: server release metadata, README.md, SKILL.md, TOOLS.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
