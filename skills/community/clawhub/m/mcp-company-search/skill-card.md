## Description:

Searches corporate registries across multiple jurisdictions via the L402 API to find companies by name and jurisdiction for due diligence, compliance, and business research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this MCP server to search corporate registry records by company name and jurisdiction for KYC, due diligence, compliance research, and business partner verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions name different npm packages and use an unpinned npx install path.

Mitigation: Confirm the intended npm package owner and package name, pin a reviewed version, and reconcile the README and SKILL.md configuration before installation.

Risk: Company names and jurisdictions searched through the tool are sent to Nautdev's API and requests may involve L402 metered charges.

Mitigation: Confirm pricing and authorization before use, and avoid sending sensitive search terms unless the deployment has appropriate data-handling approval.

Risk: The MCP server performs outbound network requests from the agent runtime.

Mitigation: Run it with restricted filesystem, environment, and network access where practical, exposing only required configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-company-search)
- [Nautdev API base URL](https://api.nautdev.com)
- [Blue-Trianon-Ventures pricing reference](https://github.com/Blue-Trianon-Ventures)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls]

**Output Format:** [MCP tool responses containing JSON-formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on Nautdev API availability, configured base URL, and metered L402 access.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
