## Description: <br>
Huo15 Crm Agent supports CRM sales work for finance and tax services by scoring leads, building customer briefs, generating sales pitches and follow-up plans, scanning industry timing hooks, searching Qichacha company data, retrieving company details, and identifying intent signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and CRM users use this skill to prioritize finance and tax service prospects, draft customer-facing outreach, plan follow-up activity, and prepare CRM action drafts for review. It can enrich prospect work with Qichacha company search and detail data when the user configures Qichacha credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Qichacha-backed tools send company search terms and detail identifiers to an external enrichment provider when credentials are configured. <br>
Mitigation: Configure Qichacha credentials only in approved environments and avoid sending confidential prospect data beyond the identifiers needed for enrichment. <br>
Risk: The skill can generate CRM and messaging nextActions that may create leads, schedule activities, post notes, or send outreach if another plugin executes them. <br>
Mitigation: Review every generated nextActions draft before allowing Odoo or messaging plugins to execute it. <br>
Risk: Documentation contains an outdated no-network claim while the security evidence confirms Qichacha features make external API calls. <br>
Mitigation: Treat the security evidence as authoritative and document external Qichacha calls during deployment review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-crm-agent) <br>
- [Publisher profile](https://clawhub.ai/user/zhaobod1) <br>
- [Qichacha OpenAPI](https://openapi.qcc.com/) <br>
- [Huo15 Huihuoyun Odoo package](https://www.npmjs.com/package/@huo15/huo15-huihuoyun-odoo) <br>
- [Prospect research notes](docs/v02-prospect-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured text or JSON-like tool results containing lead scores, briefs, pitch variants, follow-up plans, intent signals, and proposed nextActions for user review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Qichacha-backed company search and detail tools require user-supplied Qichacha credentials; CRM and messaging actions are emitted as drafts for confirmation rather than executed directly by this skill.] <br>

## Skill Version(s): <br>
0.2.1 (source: server evidence, frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
