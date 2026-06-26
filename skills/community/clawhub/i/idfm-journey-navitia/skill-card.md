## Description: <br>
Query Île-de-France Mobilités (IDFM) PRIM/Navitia for place resolution, journey planning, and disruptions or incident checks when the user has an IDFM PRIM API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anthonymq](https://clawhub.ai/user/anthonymq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and transit-focused agents use this skill to resolve Île-de-France locations, plan PRIM/Navitia journeys, and check disruptions or incidents from an IDFM API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an IDFM PRIM API key and includes an option that can send that key to a non-default API host. <br>
Mitigation: Use the default official PRIM/Navitia endpoint, avoid overriding --base-url unless the destination is trusted, and prefer a dedicated or revocable API key. <br>


## Reference(s): <br>
- [IDFM PRIM / Navitia quick notes](references/idfm-prim.md) <br>
- [IDFM PRIM/Navitia API endpoint](https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Plain text summaries or raw JSON from PRIM/Navitia API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IDFM_PRIM_API_KEY; supports place lookup, journey planning, disruption filters, and an optional raw JSON mode.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
