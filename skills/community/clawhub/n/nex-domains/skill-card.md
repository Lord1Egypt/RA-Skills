## Description:

Nex Domains helps agents manage a local domain portfolio, monitor DNS and SSL status, run WHOIS and health checks, sync Cloudflare zones, and export portfolio reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, DevOps teams, system administrators, domain managers, and web agencies use this skill to track domain inventories, check DNS and SSL health, monitor renewals, sync Cloudflare records, and create CSV or JSON portfolio exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can probe arbitrary domains with WHOIS, DNS, HTTP, and SSL checks.

Mitigation: Run checks only against domains the user is authorized to inspect, and avoid internal or confidential hostnames unless the deployment context explicitly allows it.

Risk: Cloudflare sync can use API credentials to import zone and DNS data.

Mitigation: Use a least-privilege Cloudflare API token, keep credentials in environment variables or a secret manager, and rotate tokens if exposed.

Risk: Portfolio exports and the local database may contain sensitive domain, client, cost, and DNS information.

Mitigation: Restrict permissions on the local data directory, protect exported CSV or JSON files, and share exports only with intended recipients.

Risk: Removing a domain deletes local portfolio records without a confirmation step.

Mitigation: Confirm the target domain with the user before running remove commands and keep backups for important portfolios.

## Reference(s):

- [Nex Domains on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-domains)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text terminal output, with optional CSV or JSON export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing responses should summarize CLI results and avoid exposing local database paths or credential values.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
