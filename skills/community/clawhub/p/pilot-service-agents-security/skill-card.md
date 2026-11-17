## Description:

Security and threat-intel lookups for CVEs, certificate transparency, URL and IP threat checks, DNS, WHOIS, and RDAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and security practitioners use this skill to discover Pilot Protocol security service agents, inspect each agent's filter contract, and run read-only CVE, certificate transparency, DNS, WHOIS/RDAP, URL, and IP reputation lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security lookup queries may expose domains, URLs, IP addresses, and CVE interests to Pilot Protocol agents, upstream providers, or Gemini summaries.

Mitigation: Submit only data appropriate for those external services; avoid /summary and free-text queries for sensitive indicators when a structured /data lookup is sufficient.

Risk: Lookup and summary results can be incomplete, stale, or provider-dependent.

Mitigation: Cross-check important findings across multiple listed sources and review structured response fields such as upstream_url before acting.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-security)
- [Pilot Skills catalog](https://teoslayer.github.io/pilot-skills/)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl and a Pilot Protocol daemon joined to network 9; agent responses may include external service data and upstream URLs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
