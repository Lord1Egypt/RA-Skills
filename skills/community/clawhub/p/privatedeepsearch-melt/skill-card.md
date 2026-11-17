## Description:

Performs private, multi-round deep web searches excluding Google/Bing, synthesizes results with citations, and does not retain user data or logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romancircus](https://clawhub.ai/user/romancircus)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to run local SearXNG-backed web searches and multi-iteration research workflows that return source-linked findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External search engines and visited websites can receive query-derived requests and metadata.

Mitigation: Do not use the skill for sensitive searches unless that exposure is acceptable; use a VPN where appropriate.

Risk: The local SearXNG service may be reachable beyond localhost if exposed by container networking.

Mitigation: Bind SearXNG to 127.0.0.1 and enable rate limiting or firewall access to the port.

Risk: Unpinned Docker images or Python dependencies can change behavior across installs.

Mitigation: Pin the SearXNG Docker image and Python dependency versions before production use.

Risk: Documented curl templates can pass unsanitized query text to the local search endpoint.

Mitigation: URL-encode and sanitize query text before running shell examples or wrapping them in automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/romancircus/skills/privatedeepsearch-melt)
- [SearXNG](https://github.com/searxng/searxng)
- [Privacy Guide](docs/PRIVACY.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON search results, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research reports include query, date, source count, findings, and source links.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
