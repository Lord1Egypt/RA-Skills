## Description:

Fetch and organize Keruyun Open Platform API metadata, including endpoint paths, parameters, response examples, and module categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to look up Keruyun Open Platform endpoints and understand request parameters, response examples, authentication scope, QPS notes, and solution-oriented API groupings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API metadata includes high-impact business areas such as payments, transfers, employee management, coupons, CRM assets, and inventory.

Mitigation: Verify each endpoint against official Keruyun documentation and require explicit human approval before using any write, money-moving, or permission-changing operation.

Risk: Security evidence reports confirmed accuracy and packaging issues in the API reference data.

Mitigation: Treat outputs as lookup guidance, check paths and parameters before implementation, and prefer official Keruyun documentation for final integration decisions.

Risk: The bundled scraper imports an external scraper-template dependency.

Mitigation: Do not run artifact/scripts/scrape.py unless the local dependency and execution environment are trusted.

## Reference(s):

- [Keruyun Api Fetcher on ClawHub](https://clawhub.ai/woai36d/skills/keruyun-api-fetcher)
- [woai36d publisher profile](https://clawhub.ai/user/woai36d)
- [Keruyun Open Platform](https://open.keruyun.com/official/developer.html)
- [Keruyun website](https://www.keruyun.com)
- [Complete Keruyun API metadata](artifact/references/_all_apis_complete.json)
- [Organized Keruyun API modules](artifact/references/_modules_organized.json)
- [Solution API mapping](artifact/solutions/_solution_api_mapping.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be treated as API reference guidance; the skill does not itself authorize or execute Keruyun API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
