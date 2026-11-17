## Description:

Resilient MCP proxy for Google Stitch - 3-layer safety (auto-retry, token refresh, TCP drop recovery).

This skill is ready for commercial/non-commercial use.

## Publisher:

[choihyunsus](https://clawhub.ai/user/choihyunsus)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure and operate an MCP proxy for Google Stitch screen generation with retry, token refresh, TCP drop recovery, and generation status tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation relies on automatically running an unpinned npm package that is not included in the reviewed artifact.

Mitigation: Review the npm package and publisher before installing, pin a reviewed version, avoid automatic startup with npx -y, and provide only the minimum Google or Stitch credentials needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/choihyunsus/skills/n2-stitch-mcp)
- [NPM package](https://www.npmjs.com/package/n2-stitch-mcp)
- [Project website](https://nton2.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides setup for an MCP server that exposes Stitch API and generation tracking tools.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
