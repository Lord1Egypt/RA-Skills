## Description:

Query Linz Linien raw EFA endpoints for stop lookup and live departures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fjrevoredo](https://clawhub.ai/user/fjrevoredo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to resolve Linz public transport stop IDs from stop names and fetch upcoming live departures from Linz Linien EFA endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to an unencrypted HTTP API base URL.

Mitigation: Configure the base URL to the official HTTPS Linz endpoint before use.

Risk: The skill allows a custom API base URL, which can redirect requests to arbitrary destinations.

Mitigation: Constrain execution to the official Linz endpoint and avoid accepting untrusted base URL overrides.

Risk: Full request URLs may include stop-search terms.

Mitigation: Avoid logging full query URLs or redact stop-search parameters from diagnostics.

## Reference(s):

- [Endpoint Reference](artifact/references/endpoints.md)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [EFA XML API PDF](https://data.linz.gv.at/katalog/linz_ag/linz_ag_linien/fahrplan/EFA_XML_Schnittstelle_20151217.pdf)
- [Linz AG EFA Endpoint Base](https://www.linzag.at/linz2)
- [Open Data Catalog RDF](https://www.data.gv.at/api/hub/repo/datasets/linien-fahrwege-und-haltestellen-der-linz-ag-linien-2025.rdf?useNormalizedId=true&locale=de)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown or JSON summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require outbound network access to Linz Linien EFA endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
