## Description: <br>
Query Linz public transport stops for IDs and fetch live upcoming departures using Linz Linien EFA endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fjrevoredo](https://clawhub.ai/user/fjrevoredo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and transit-assistance agents use this skill to resolve Linz public transport stop IDs and retrieve upcoming departures for a selected stop. <br>

### Deployment Geography for Use: <br>
Global use; data coverage is Linz, Austria public transport. <br>

## Known Risks and Mitigations: <br>
Risk: The configured Linz EFA endpoint receives stop names or stop IDs sent by the agent. <br>
Mitigation: Use only a trusted base URL and avoid setting LINZ_TRANSPORT_API_BASE_URL or --base-url to an endpoint you do not trust. <br>
Risk: The default transit API base URL uses plain HTTP. <br>
Mitigation: Prefer an HTTPS base URL when it works for the endpoint. <br>
Risk: Live transit responses can be empty, ambiguous, or shape-variant. <br>
Mitigation: Confirm ambiguous stop matches, surface EFA message codes, and report when no upcoming departures are available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fjrevoredo/linz-public-transport) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>
- [Endpoint Reference](references/endpoints.md) <br>
- [Linz EFA XML API PDF](https://data.linz.gv.at/katalog/linz_ag/linz_ag_linien/fahrplan/EFA_XML_Schnittstelle_20151217.pdf) <br>
- [Linz AG EFA Endpoint](https://www.linzag.at/linz2) <br>
- [Linz Linien Open Data RDF](https://www.data.gv.at/api/hub/repo/datasets/linien-fahrwege-und-haltestellen-der-linz-ag-linien-2025.rdf?useNormalizedId=true&locale=de) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary with optional shell commands and JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stop IDs, departure times, line numbers, directions, platforms, and EFA diagnostics.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
