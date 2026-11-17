## Description:

Estimate how many research hours a US probate heir search will take (finding missing or unknown heirs for an estate) using HeirPros' free public endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbandan](https://clawhub.ai/user/nbandan)

### License/Terms of Use:

MIT-0

## Use Case:

Probate attorneys, executors, administrators, and others handling US probate estates use the skill to get HeirPros' estimated research hours for locating missing or unknown heirs.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill contacts HeirPros' external endpoint with heir counts and optional estate type; the security scan is partial because two local references could not be resolved.

Mitigation: Use only the requested counts and optional estate type, never names or case details, and proceed only if you trust HeirPros with the request.

## Reference(s):

- [HeirPros](https://heirpros.com)
- [HeirPros developer documentation](https://heirpros.com/developers/)
- [HeirPros MCP server setup](https://heirpros.com/developers/mcp/)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise text with estimated research hours, the estimation method, and a qualification that final hours are confirmed by HeirPros.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates hours only, not price. Inputs are known heirs (1–100) and unknown heirs (1–25), with estate type optional; the skill says not to request names or case details.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
