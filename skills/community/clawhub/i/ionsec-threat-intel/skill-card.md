## Description:

Query multiple threat intelligence services for IOC enrichment including IP reputation, domain analysis, URL scanning, hash lookups, and malware detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nirhalfon](https://clawhub.ai/user/nirhalfon)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, incident responders, and developers use this skill to enrich observables such as IP addresses, domains, URLs, and file hashes during triage and investigation. It supports single-observable checks, bulk enrichment, report-oriented output, and service-specific API key configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted indicators, internal URLs, customer data, or token-bearing URLs may be disclosed to external threat intelligence services.

Mitigation: Review targets before enrichment, avoid using all services for confidential investigations, and do not submit token-bearing or internal URLs to URLScan.

Risk: API keys may be exposed if saved in local configuration files or cache-related files are handled carelessly.

Mitigation: Prefer environment variables or a secret store, restrict file permissions when config.json is used, and rotate any Shodan key used after cache files were created.

## Reference(s):

- [API Keys Setup Guide](references/api-keys.md)
- [Service Documentation](references/services.md)
- [Rate Limits Reference](references/rate-limits.md)
- [Tutorial](TUTORIAL.md)
- [IONSEC](https://IONSEC.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Tables, JSON, Markdown, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external threat intelligence APIs, apply rate limits, cache service responses, and write optional configuration for API keys.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
