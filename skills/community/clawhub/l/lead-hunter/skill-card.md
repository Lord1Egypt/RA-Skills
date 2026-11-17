## Description:

Automated lead generation and enrichment for AI agents that helps find prospects, enrich them with contact and company data, score them, and prepare them for CRM or outreach workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galacticpuffin](https://clawhub.ai/user/galacticpuffin)

### License/Terms of Use:

MIT

## Use Case:

Sales, growth, and operations users can use this skill for authorized B2B prospect discovery, enrichment, scoring, and CRM handoff. Agents use it to assemble targeted lead lists, prioritize prospects, and prepare compliant outreach inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad scraping and enrichment workflows may collect personal or contact data without adequate authorization.

Mitigation: Use only authorized, compliant sources and approved enrichment providers; document permission and honor suppression lists before collecting or using lead data.

Risk: LinkedIn proxy or evasion-oriented workflows may violate platform rules or organizational policy.

Mitigation: Disable LinkedIn proxy or evasion guidance and rely on approved APIs, permitted exports, or other compliant discovery channels.

Risk: Guessed or historical personal-email harvesting and SMTP pings can create privacy, consent, and deliverability risk.

Mitigation: Do not use guessed or historical personal-email collection or SMTP ping validation; use approved verification providers and reject contacts that cannot be validated compliantly.

Risk: Automatic outreach and full lead-record webhooks may send sensitive contact data to unintended recipients.

Mitigation: Require documented outreach permission, keep human or policy approval in the outreach path, use vetted HTTPS webhook destinations, and send minimized fields rather than full lead records.

## Reference(s):

- [Lead Hunter on ClawHub](https://clawhub.ai/galacticpuffin/skills/lead-hunter)
- [ICP Configuration](artifact/config/icp.md)
- [Discovery Sources](artifact/discovery/sources.md)
- [Email Discovery and Verification](artifact/enrichment/email-discovery.md)
- [Output and Integrations](artifact/output/integrations.md)
- [Lead Scoring](artifact/scoring/lead-scoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with YAML configuration snippets, CLI examples, lead scoring guidance, and JSON/CSV export guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare CRM-ready lead records and webhook payload guidance; contact fields should be minimized and handled only through approved destinations.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
