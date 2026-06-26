## Description: <br>
Marrow provides persistent agent memory for OpenClaw by surfacing past failures, logging decisions, and enforcing memory use across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[majinbuu0x9](https://clawhub.ai/user/majinbuu0x9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use Marrow to make agent sessions automatically consult persistent memory, log decisions and outcomes, and query prior failures before risky or unfamiliar work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically records agent action summaries to an external memory service, which can expose sensitive workflow metadata if used in confidential or regulated contexts. <br>
Mitigation: Use it only where external action metadata logging is permitted, review Marrow privacy and retention terms, and avoid regulated, confidential, or secret-bearing workflows unless policy allows it. <br>
Risk: Marrow requires MARROW_API_KEY and an MCP server, so leaked credentials or an unverified server package could expose account access or alter logging behavior. <br>
Mitigation: Protect MARROW_API_KEY as a secret, verify the @getmarrow/mcp server source before installation, and rotate credentials if exposure is suspected. <br>
Risk: Mandatory logging instructions can accidentally capture sensitive payloads if an agent includes secrets or file contents in action summaries. <br>
Mitigation: Log only high-level action and outcome summaries; redact API keys, tokens, auth headers, PII, and sensitive file contents before every Marrow call. <br>


## Reference(s): <br>
- [Marrow homepage](https://getmarrow.ai) <br>
- [Marrow MCP quick reference](references/marrow-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/majinbuu0x9/marrow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions and MCP tool call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MARROW_API_KEY and an available @getmarrow/mcp server; logging instructions explicitly exclude secrets, credentials, PII, and sensitive file contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
