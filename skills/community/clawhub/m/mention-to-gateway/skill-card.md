## Description:

Routes messages in @deviceid-agentid-ip plus instruction format to the specified IP gateway agent and returns the remote agent response content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxx328](https://clawhub.ai/user/lxx328)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and gateway operators use this skill to let agents address another gateway by mention syntax, forward the instruction to the target agent, and present only the target agent's reply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and gateway identity may be sent to arbitrary IP addresses over unauthenticated HTTP.

Mitigation: Deploy only in a controlled private gateway environment with trusted users, restricted outbound access, destination validation, authenticated encrypted transport, and an allowlisted gateway registry.

Risk: Remote replies may be displayed without clear attribution to the producing gateway.

Mitigation: Show visible labels that identify which remote gateway produced each response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxx328/skills/mention-to-gateway)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Text response content extracted from an OpenAI-compatible JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote response content is returned without additional wrapper text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
