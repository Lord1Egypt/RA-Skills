## Description:

Connect to Huodingdong ERP MCP through OOMOL to discover tools and read or manage ERP data using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

ERP users and operators use this skill to discover the available Huodingdong ERP tools and request data lookups or business operations through their OOMOL connection. It requires confirmation before write actions and explicit approval before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to run a remote installer that has not been verified.

Mitigation: Review setup behavior and install a verified oo CLI yourself. Limit permissions on the connected ERP account and retain approval for business changes.

## Reference(s):

- [Huodingdong ERP MCP](https://www.huodingdong.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API responses, JSON, Guidance]

**Output Format:** [JSON results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data and response shape depend on the selected ERP tool.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
