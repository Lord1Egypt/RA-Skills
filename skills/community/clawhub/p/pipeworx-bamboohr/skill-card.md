## Description:

Access and manage BambooHR employee data, including directory, individual profiles, time-off requests, and employee files through the Pipeworx BambooHR MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to BambooHR via an MCP server for employee directory lookup, profile retrieval, time-off request search, and employee file listing. Because these workflows involve sensitive employee data, organizations should confirm processor approval and access scope before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive employee data may pass through a third-party MCP gateway without documented authorization, privacy, or data-handling controls.

Mitigation: Verify who operates the Pipeworx gateway, confirm organizational approval for this processor, and review how BambooHR credentials and employee data are handled before installation.

Risk: Broad BambooHR access could expose employee files, time-off data, or profile details beyond the intended workflow.

Mitigation: Use narrowly scoped, revocable BambooHR access and avoid employee files or time-off workflows unless they are explicitly authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-bamboohr)
- [Pipeworx BambooHR MCP gateway](https://gateway.pipeworx.io/bamboohr/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return BambooHR employee directory, profile, time-off, and file metadata depending on the invoked tool and granted access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
