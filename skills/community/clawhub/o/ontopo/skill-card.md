## Description:

Find restaurants, menus, booking links, and table availability across Israeli Ontopo venues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexpolonsky](https://clawhub.ai/user/alexpolonsky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Israeli restaurants, compare live availability, inspect menus, and obtain booking links for manual completion on Ontopo.

### Deployment Geography for Use:

Israel

## Known Risks and Mitigations:

Risk: Restaurant searches, booking criteria, and venue lookups are sent to Ontopo's external service.

Mitigation: Use user-approved search criteria and avoid adding sensitive personal details to queries.

Risk: Availability data may change or may not match final reservation availability.

Mitigation: Treat availability as advisory and confirm details on Ontopo before relying on a booking time.

Risk: The skill generates booking links but does not complete reservations.

Mitigation: Complete any reservation manually on Ontopo's website after reviewing the venue, party size, date, and time.

Risk: Installation resolves the current httpx package version.

Mitigation: Install in a controlled environment or pin dependencies according to local release policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexpolonsky/skills/ontopo)
- [Publisher profile](https://clawhub.ai/user/alexpolonsky)
- [Ontopo website](https://ontopo.com)
- [Ontopo API endpoint](https://ontopo.com/api)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Markdown, JSON, Guidance]

**Output Format:** [CLI output as human-readable text or JSON envelopes, with booking URLs for manual follow-up.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not place reservations; raw upstream payloads are available with --raw when --json is used.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
