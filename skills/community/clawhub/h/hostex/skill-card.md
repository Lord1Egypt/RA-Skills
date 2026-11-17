## Description:

Hostex (hostex.io) OpenAPI v3.0 skill for querying and managing vacation rental properties, room types, reservations, availability, listing calendars, guest messaging, reviews, and webhooks via the Hostex API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ansonfreeman](https://clawhub.ai/user/ansonfreeman)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query Hostex property, reservation, availability, messaging, review, and webhook data, and to run guarded Hostex API write operations when explicitly authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hostex API access can expose sensitive reservation, guest, message, lock-code, pricing, and availability data.

Mitigation: Use a read-only, narrowly scoped Hostex PAT where possible, avoid printing or sharing returned data unnecessarily, and treat all API output as sensitive.

Risk: Changing HOSTEX_BASE_URL can send Hostex credentials to an unexpected API destination.

Mitigation: Leave HOSTEX_BASE_URL unset for normal use, and only override it with non-production tokens in controlled environments.

Risk: Write commands can change messages, listing prices, reservations, or property availability.

Mitigation: Keep writes disabled unless needed, review the generated change plan, require explicit user confirmation, and do not rely on --dry-run when --confirm is also present.

## Reference(s):

- [Hostex OpenAPI v3 Config](https://hostex.io/open_api/v3/config.json)
- [Hostex API Server](https://api.hostex.io/v3)
- [Local OpenAPI Reference](references/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/ansonfreeman/skills/hostex)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations are default; write operations require HOSTEX_ALLOW_WRITES=true and explicit confirmation.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
