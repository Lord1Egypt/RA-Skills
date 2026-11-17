## Description:

Search and retrieve questions and answers from any StackExchange site, including StackOverflow, ServerFault, SuperUser, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical agents use this skill to search StackExchange sites and retrieve question and answer content for implementation research, operations, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: StackExchange queries and selected site names are sent to the Pipeworx gateway.

Mitigation: Do not use the skill for confidential queries unless the user trusts that gateway and its handling of request data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-stackexchange)
- [Pipeworx StackExchange MCP gateway](https://gateway.pipeworx.io/stackexchange/mcp)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured text containing StackExchange question or answer content, links, tags, scores, and author metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Question and answer bodies may include HTML returned from StackExchange.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
