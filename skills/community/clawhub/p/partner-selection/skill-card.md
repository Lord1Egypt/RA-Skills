## Description:

Helps agents identify, evaluate, and recommend local e-invoicing compliance channel partners for a target country, including official registry checks, multi-round filtering, POC acceptance planning, and negotiation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangxf0927](https://clawhub.ai/user/tangxf0927)

### License/Terms of Use:

MIT-0

## Use Case:

External business, product, compliance, and partner teams use this skill when expanding an e-invoicing SaaS platform into a new country and need a traceable partner-selection report. It guides the agent through country confirmation, official registry review, candidate filtering, scoring, POC design, and go-to-market actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Official e-invoicing registries and regulatory requirements can change after the artifact's reference data is published.

Mitigation: Verify official registry pages and recent regulatory updates during each use, and keep clickable source URLs in the final report.

Risk: Partner recommendations may influence compliance, commercial, or go-to-market decisions.

Mitigation: Require human review by product, compliance, legal, and commercial owners before treating the report as an execution plan.

Risk: Some markets require written confirmation that multi-tenant proxy submission is legally acceptable before production use.

Mitigation: Obtain local legal confirmation before launch whenever proxy legality is pending or jurisdiction-specific.

Risk: The skill needs web access and creates a report file.

Mitigation: Run it with scoped web and filesystem permissions and review the generated report before sharing it externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangxf0927/skills/partner-selection)
- [Country regulatory reference](reference/country_regulatory_reference.md)
- [Partner scoring matrix](reference/partner_scoring_matrix.md)
- [POC acceptance scripts](reference/poc_acceptance_scripts.md)
- [OpenPeppol member directory for Malaysia](https://peppol.org/members/?country=Malaysia)
- [OpenPeppol Singapore and Malaysia authority page](https://peppol.org/peppolauthority/singapore-and-malaysia/)
- [IMDA nationwide e-invoicing framework](https://www.imda.gov.sg/how-we-can-help/nationwide-e-invoicing-framework)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Intermediate Simplified Chinese analysis and a final .docx report with tables, clickable URLs, scoring, POC scripts, and negotiation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a report file named partner_selection_[country]_[YYYYMMDD].docx when a compatible document-generation capability is available.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter and README report 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
