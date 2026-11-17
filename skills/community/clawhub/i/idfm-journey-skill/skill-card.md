## Description:

Query Ile-de-France Mobilites (IDFM) PRIM/Navitia for Paris and suburban public transport place resolution, journey planning, and disruption or incident checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthonymq](https://clawhub.ai/user/anthonymq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve stops or stations, plan public transport routes, and check RER or metro disruptions in Ile-de-France using an IDFM PRIM API key.

### Deployment Geography for Use:

Global; service coverage is Ile-de-France, France.

## Known Risks and Mitigations:

Risk: The --base-url option can cause the IDFM PRIM API key to be sent to a server other than the official IDFM PRIM/Navitia endpoint.

Mitigation: Use only the official IDFM PRIM/Navitia endpoint, restrict who can invoke the skill, and prefer a version that removes or validates --base-url before sending the API key.

## Reference(s):

- [IDFM PRIM / Navitia quick notes](artifact/references/idfm-prim.md)
- [IDFM PRIM developer portal](https://prim.iledefrance-mobilites.fr/)
- [IDFM PRIM Navitia API base endpoint](https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia)
- [ClawHub skill release page](https://clawhub.ai/anthonymq/skills/idfm-journey-skill)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and optional JSON output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IDFM_PRIM_API_KEY for live API calls.]

## Skill Version(s):

0.1.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
