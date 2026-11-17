## Description:

AI-powered time tracking, client management, and project profitability for freelancers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and solo service providers use this skill to log time conversationally, manage client and project records, monitor project profitability, generate timesheets and billing reports, and prepare invoice data for approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores client contact details, billing rates, time entries, invoices, and exports on the machine running the agent.

Mitigation: Use a trusted host, restrict ~/.freelancer-toolkit permissions, enable disk encryption where appropriate, and include the data directory in a secure backup plan.

Risk: Generated CSV and JSON exports can contain sensitive billing and client data.

Mitigation: Review exports before sharing or opening them in spreadsheet applications, and remove stale exported files when they are no longer needed.

Risk: InvoiceGen Pro integration may pass client and billing data to another tool's processing pipeline.

Mitigation: Review invoice drafts before approval and check InvoiceGen Pro's security documentation before using the integration.

Risk: The optional setup flow can install jq through the system package manager with sudo.

Mitigation: Only approve the install after confirming it uses a trusted package manager, or install jq manually before running setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-freelancer-toolkit)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Security notes](artifact/SECURITY.md)
- [Dashboard manifest](artifact/dashboard-kit/manifest.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance, Markdown reports, CSV exports, JSON invoice payloads, and Bash command/script usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON data files and exports under ~/.freelancer-toolkit/.]

## Skill Version(s):

1.0.3 (source: server evidence release.version and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
