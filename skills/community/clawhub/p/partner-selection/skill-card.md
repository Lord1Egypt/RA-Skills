## Description: <br>
Helps teams identify, evaluate, and recommend local e-invoicing compliance channel partners for a target country using regulatory checks, official registries, multi-round filtering, POC criteria, and negotiation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangxf0927](https://clawhub.ai/user/tangxf0927) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External product, compliance, and partnership teams use this skill when expanding an e-invoicing SaaS platform into a new country and needing a traceable shortlist of local compliance channel partners. It supports partner discovery, qualification filtering, POC acceptance planning, and commercial negotiation preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regulatory and partner recommendations may become outdated or incomplete because the workflow depends on live web research, public registries, and changing local e-invoicing rules. <br>
Mitigation: Verify conclusions against current official sources and local counsel before contracting, integration work, or production launch. <br>
Risk: Generated partner shortlists, POC criteria, and negotiation guidance could be mistaken for final compliance or procurement approval. <br>
Mitigation: Treat the output as research support and route the report through product, legal, compliance, and partnership review before acting on it. <br>
Risk: The skill generates a local .docx report that may contain sensitive commercial analysis about candidate partners. <br>
Mitigation: Store generated reports according to the user's internal document handling policy and review sharing scope before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangxf0927/partner-selection) <br>
- [Country regulatory reference](reference/country_regulatory_reference.md) <br>
- [Partner scoring matrix](reference/partner_scoring_matrix.md) <br>
- [POC acceptance scripts](reference/poc_acceptance_scripts.md) <br>
- [Peppol Singapore and Malaysia authority page](https://peppol.org/peppolauthority/singapore-and-malaysia/) <br>
- [IMDA Nationwide E-invoicing Framework](https://www.imda.gov.sg/how-we-can-help/nationwide-e-invoicing-framework) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Simplified Chinese partner-selection report, typically rendered as a .docx file with structured sections, tables, scores, and clickable source URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current web research, reads bundled reference files, and produces traceable recommendations that should be reviewed before contracting or production launch.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter and README show 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
