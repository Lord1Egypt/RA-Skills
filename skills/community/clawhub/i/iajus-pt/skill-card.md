## Description:

Pesquisa de jurisprudência portuguesa via MCP IAJUS PT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaelob](https://clawhub.ai/user/rafaelob)

### License/Terms of Use:

MIT-0

## Use Case:

Legal researchers and practitioners use an authorized IAJUS PT connection to find Portuguese court decisions and precedents, review the returned source links, and report coverage limits. The skill does not provide legislation or Lex.

### Deployment Geography for Use:

Portugal

## Known Risks and Mitigations:

Risk: Service access may require a paid plan and OAuth authorization.

Mitigation: Review IAJUS plan terms and consent requirements before connecting; installation alone does not grant access.

Risk: Search terms may contain identifiers and are retained by the provider for 90 days.

Mitigation: Keep confidential client details and unnecessary personal information out of searches.

Risk: Returned case-law information may be incomplete or inaccurate.

Mitigation: Check decisions against their original sources and state coverage limits; distinguish empty or incomplete results from errors.

## Reference(s):

- [IAJUS PT MCP endpoint](https://pt.mcp.iajus.com.br/mcp)
- [OpenClaw MCP CLI and login documentation](https://github.com/openclaw/openclaw/blob/4e334e81e6946ff66ad06639c1d7dfde306a8b5d/docs/cli/mcp/registry.md)
- [OpenClaw MCP configuration documentation](https://github.com/openclaw/openclaw/blob/4e334e81e6946ff66ad06639c1d7dfde306a8b5d/docs/cli/mcp/json-output.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text with decision details and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the authorized service connection and its measured coverage; this skill does not provide legislation or Lex.]

## Skill Version(s):

2.0.21 (source: artifact/SKILL.md frontmatter; server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
