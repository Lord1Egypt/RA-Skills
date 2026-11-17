## Description:

This skill helps an agent use a Calculator Server MCP integration to perform addition and subtraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqatsh](https://clawhub.ai/user/dqatsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when an agent needs calculator operations through the configured MCP server. It supports addition and subtraction requests that require the XINIUDATA_MCP_TOKEN environment variable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and session data may be exposed because the documented MCP endpoint uses unencrypted HTTP.

Mitigation: Use an HTTPS endpoint with certificate validation, prefer short-lived least-privilege tokens, and rotate any token that may have been used over plaintext HTTP.

Risk: The skill depends on a private remote MCP server.

Mitigation: Install only when the private server and network path are trusted and reviewed for the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dqatsh/skills/my-test-skill-4-xn)
- [Publisher profile](https://clawhub.ai/user/dqatsh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the XINIUDATA_MCP_TOKEN environment variable for MCP server access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
