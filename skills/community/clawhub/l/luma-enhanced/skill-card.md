## Description:

Fetch upcoming events from Luma (lu.ma) for any city. Use when the user asks about tech events, startup meetups, networking events, conferences, or things happening in cities around the world. Returns events with details including venue, date, hosts, ticket status, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find upcoming Luma events for one or more city slugs, including event timing, venue, host, ticket status, and direct links. It is useful for answering questions about local tech events, startup meetups, networking events, conferences, and city activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts lu.ma and processes public event names, venues, host text, and links as external content.

Mitigation: Treat event details as untrusted until checked on Luma, and review links before relying on them.

Risk: Fetched public event metadata is retained locally for follow-up questions.

Mitigation: Clear ~/.openclaw/workspace/memory/luma-events.json when prior event lookups should not be retained.

Risk: Luma page structure, availability, or rate limits may affect results.

Mitigation: Limit request volume and treat empty or error results as fetch limitations rather than confirmation that no events exist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/firefrog-pepe/skills/luma-enhanced)
- [Luma city event pages](https://lu.ma)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files]

**Output Format:** [Human-readable text or JSON event data from a Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists fetched public event metadata to a local luma-events.json cache for follow-up questions.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
