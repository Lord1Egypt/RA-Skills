## Description:

Patent search and analytics via 9235 API (search, detail, claims, company portrait, Excel export).

This skill is ready for commercial/non-commercial use.

## Publisher:

[windinwing](https://clawhub.ai/user/windinwing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and IP research teams use this skill to query the 9235 patent service for patent records, claims, descriptions, legal events, citations, similar patents, company patent portraits, analytics, and spreadsheet exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent and IP search terms, patent identifiers, filters, analytics requests, and download paths are sent to the third-party 9235 API.

Mitigation: Use the skill only where sending those queries to 9235 is acceptable, and review the provider's terms and privacy policy before deployment.

Risk: The skill requires a 9235 API token for authentication.

Mitigation: Keep the token scoped and protected, provide it through environment or host-managed configuration, avoid committing real tokens, and rotate it if exposed.

Risk: The export path may attempt to install unpinned Python packages for spreadsheet support.

Mitigation: Preinstall required export dependencies from a trusted, pinned environment or restrict export features in controlled deployments.

Risk: Generated CSV/XLSX files may contain spreadsheet formulas or externally sourced content.

Mitigation: Treat exports as untrusted, review or neutralize formula-like values before sharing, and open files with spreadsheet protections enabled.

## Reference(s):

- [9235 Open Platform](https://www.9235.net/api/open)
- [9235 API Documentation](https://www.9235.net/api/interface.html)
- [9235 Search Help](https://www.9235.net/help/index.html)
- [ClawHub Skill Page](https://clawhub.ai/windinwing/skills/patent-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown/text responses with optional outbound CSV or XLSX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PATENT_API_TOKEN or host-managed OpenClaw API key; search terms, patent identifiers, pagination, filters, and download requests are sent to the 9235 API.]

## Skill Version(s):

1.0.10 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
