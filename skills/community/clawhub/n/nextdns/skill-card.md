## Description:

Query and troubleshoot NextDNS via the NextDNS API for profile inspection, analytics, recent logs, blocked-domain diagnosis, DNS upstream health checks, and safe read-only preparation before configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naamah75](https://clawhub.ai/user/naamah75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect NextDNS profiles, analytics, and logs, diagnose blocked domains and DNS upstream behavior, and prepare safe read-only checks before any configuration change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NextDNS account data and DNS logs can reveal browsing and device activity.

Mitigation: Use protected environment variables for credentials, query logs only when needed, summarize minimally, and avoid sharing transcripts or terminal output containing helper results.

Risk: Command-line API keys or raw helper output can expose credentials or sensitive account data.

Mitigation: Prefer NEXTDNS_API_KEY from a protected environment over --api-key examples, and redact helper output before sharing.

Risk: Profile edits, list mutations, or log clearing can be destructive or privacy-impacting.

Mitigation: Keep diagnostics read-first, require explicit confirmation for any write or delete action, and back up the current profile before configuration changes.

Risk: The NextDNS API is marked beta, so response shapes may change.

Mitigation: Handle API responses defensively and consult the bundled API summary or upstream documentation when endpoint details matter.

## Reference(s):

- [NextDNS API summary](references/api-summary.md)
- [NextDNS API documentation](https://nextdns.github.io/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper responses include success status, HTTP status, requested URL without the API key, and decoded API response data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
