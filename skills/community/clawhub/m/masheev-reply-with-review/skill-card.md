## Description:

Draft customer-support replies in Masheev conversations, show each exact draft for human approval, and send only after explicit approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masheev](https://clawhub.ai/user/masheev)

### License/Terms of Use:

Apache-2.0

## Use Case:

External customer-support teams use the skill to draft accurate, business-voiced replies from Masheev conversation context and send only the exact message a human has reviewed and approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reply could reach the wrong recipient or contain wording the user did not approve.

Mitigation: Check the intended workspace, recipient, channel, and exact current draft; send only after explicit approval of that draft.

Risk: The external server's claimed safeguards have not been independently verified.

Mitigation: Review the requested OAuth permissions and verify the recipient and complete message before each send.

## Reference(s):

- [Masheev Agent Documentation](https://docs.masheev.com/agents)
- [Masheev MCP Server](https://api.masheev.com/api/agents/mcp)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Customer reply text and Masheev conversation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows a draft preview; sending requires explicit approval of that exact draft.]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
