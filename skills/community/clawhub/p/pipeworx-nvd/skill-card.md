## Description:

NVD MCP - wraps the NIST National Vulnerability Database API for free, no-auth CVE lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to let an agent search, retrieve, and review recent CVEs from the NIST National Vulnerability Database through the Pipeworx NVD MCP connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs a mutable npm-based MCP bridge under the user's account.

Mitigation: Review the install path before enabling it, preferably by pinning and reviewing the mcp-remote version or running the connector in a sandboxed MCP runtime.

## Reference(s):

- [Pipeworx NVD Pack](https://pipeworx.io/packs/nvd)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-nvd)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration]

**Output Format:** [Markdown or plain text responses with CVE data from MCP tools; setup configuration is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides search_cves, get_cve, and recent_cves tool access; free and no API key according to the skill evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
