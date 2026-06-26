## Description: <br>
Query Ile-de-France Mobilites (IDFM) PRIM/Navitia for Paris and suburbs public transport, including place resolution, journey planning, and disruption or incident checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anthonymq](https://clawhub.ai/user/anthonymq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to resolve Ile-de-France transit places, plan routes, and check metro or RER disruptions through the IDFM PRIM/Navitia API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The IDFM PRIM API key can be exposed or sent to an untrusted endpoint if it is committed, printed, or used with an untrusted --base-url. <br>
Mitigation: Use a dedicated IDFM PRIM API key, keep it out of logs and source control, rotate it if exposed, and only use --base-url with trusted destinations. <br>


## Reference(s): <br>
- [IDFM PRIM / Navitia quick notes](references/idfm-prim.md) <br>
- [IDFM PRIM developer portal](https://prim.iledefrance-mobilites.fr/) <br>
- [IDFM PRIM Navitia API base](https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia) <br>
- [ClawHub skill page](https://clawhub.ai/anthonymq/idfm-journey-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, JSON, Configuration] <br>
**Output Format:** [Plain text route and disruption summaries, with optional raw JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IDFM_PRIM_API_KEY; --base-url can redirect requests to another endpoint.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
