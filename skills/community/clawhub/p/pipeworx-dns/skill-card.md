## Description:

DNS record lookups via Google DNS-over-HTTPS for A, AAAA, MX, NS, TXT, CNAME, and reverse DNS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect DNS records, verify DNS propagation, debug email delivery records, and perform reverse DNS lookups during domain and infrastructure troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNS lookup targets may include private hostnames, internal IPs, incident-response targets, or confidential customer domains and are sent to the Pipeworx gateway.

Mitigation: Use only for lookup targets you are comfortable sending to Pipeworx; avoid confidential customer domains, internal hostnames, and private IPs.

Risk: The setup uses an unpinned mcp-remote package, so installs may change without review.

Mitigation: Pin and review the mcp-remote package version or use a locally reviewed setup before enabling the MCP configuration.

## Reference(s):

- [Pipeworx DNS Pack](https://pipeworx.io/packs/dns)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with DNS lookup results, curl examples, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DNS queries are performed through a Pipeworx gateway; review lookup targets before use.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
