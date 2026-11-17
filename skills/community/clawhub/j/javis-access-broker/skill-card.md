## Description:

For one outside-agent request, Javis's access broker asks for clarification when needed, uses only the request's prepared data slice, and submits the minimum answer with source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use the broker to answer one question about a user's data using only the material selected for that request. It asks for clarification when the task is unclear and returns a concise, cited response or declines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial coverage and medium confidence, and flagged an undeclared tool scope.

Mitigation: Before installing, assess whether network and shell access are needed and review the permissions granted by the host runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuel-wei/skills/javis-access-broker)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON response with summary text or exact segment references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-request answer, clarification question, or decline; answer points cite source slice IDs.]

## Skill Version(s):

0.1.1 (source: evidence.json release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
