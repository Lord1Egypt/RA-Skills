## Description:

Query Île-de-France Mobilités (IDFM) PRIM/Navitia for place resolution, journey planning, and disruptions/incident checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthonymq](https://clawhub.ai/user/anthonymq)

### License/Terms of Use:


## Use Case:

External users, transit-focused agents, and developers use this skill to resolve stops, plan journeys, and check disruptions for Île-de-France routes through IDFM PRIM/Navitia when an IDFM PRIM API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --base-url option can send the IDFM_PRIM_API_KEY to an arbitrary destination.

Mitigation: Use a limited-scope IDFM PRIM API key and do not pass --base-url unless the destination has been audited and trusted; prefer the official prim.iledefrance-mobilites.fr Navitia endpoint.

## Reference(s):

- [IDFM PRIM / Navitia quick notes](references/idfm-prim.md)
- [IDFM PRIM/Navitia endpoint](https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IDFM_PRIM_API_KEY; --json can return raw PRIM/Navitia responses.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
