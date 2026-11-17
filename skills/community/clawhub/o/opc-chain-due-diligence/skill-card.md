## Description:

OPC Chain Due Diligence helps agents produce a preliminary public-data risk scan of a target company across business background, intellectual property, technical strength, funding compliance, and overall diligence risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, corporate development teams, government or park recruitment teams, reviewers, advisors, and founders use this skill to generate a quick due-diligence report from public company and patent data. It is intended for early risk triage and should not be treated as legal, investment, compliance, or valuation advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target company identifiers and extra text entered by the user may be sent to third-party public-data APIs.

Mitigation: Enter only a clean company name or registration identifier and omit confidential deal, project, or investment context.

Risk: The report may be mistaken for legal, investment, compliance, or valuation advice.

Mitigation: Use the output only as preliminary public-data triage and route material decisions to qualified diligence, legal, finance, or compliance reviewers.

Risk: Documentation claims WIPO and OpenCorporates coverage that the inspected code does not implement.

Mitigation: Do not rely on the skill for WIPO or OpenCorporates coverage unless that behavior is separately verified in the deployed version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-chain-due-diligence)
- [Wikidata API endpoint](https://www.wikidata.org/w/api.php)
- [Wikidata entity data endpoint](https://www.wikidata.org/wiki/Special:EntityData/{qid}.json)
- [USPTO PatentsView API endpoint](https://api.patentsview.org/patents/query)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown report with a JSON summary payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes color-coded risk markers, source-limited findings, and preliminary recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
