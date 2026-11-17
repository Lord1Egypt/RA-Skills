## Description:

Routes user-selected photos from Meta Ray-Ban glasses or another camera through a configured messaging ingress to an approved specialist and destination with opt-in controls, allowlisted destinations, and confirmation before cross-session forwarding or persistent writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route intentionally submitted camera photos from a messaging ingress to configured specialist agents and destination databases while keeping forwarding and persistence visible and consent-bound.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes personal photos and extracted identifiers to configured destinations.

Mitigation: Use only private, allowlisted source and destination sessions; show the destination before forwarding or writing; keep automatic routing disabled unless scoped to a named route.

Risk: The sample specialist can post images and write database records based on a forgeable routing marker.

Mitigation: Before deployment, add a local approval or signed-envelope check so direct or replayed [Vision Router] messages cannot trigger posting images or creating database records.

Risk: Connected Discord, Notion, Airtable, or database credentials can create external side effects.

Mitigation: Grant credentials only the minimum write permissions needed and review destination behavior before installing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jonathanjing/skills/glass2claw)
- [ClawHub Homepage](https://clawhub.ai/jonathanjing/glass2claw)
- [README](artifact/README.md)
- [Vision Hub Sample Routing Logic](artifact/SAMPLE_AGENT.md)
- [Wine Specialist Sample Persona](artifact/SAMPLE_SOUL_WINE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with sample routing commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing protocol guidance and starter specialist-agent prompts; it does not provide executable code.]

## Skill Version(s):

2.3.4 (source: server release metadata, SKILL.md metadata, CHANGELOG, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
