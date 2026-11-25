## Description:

Helps an outside agent answer a single request about user data by asking for clarification when needed and sharing only task-relevant information from the prepared slice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT

## Use Case:

Agents connected to Javis use the broker to handle an outside agent's single request about user data, returning the minimum relevant facts or asking for clarification when the task is unclear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described sharing and handling of information may not suit every user's needs.

Mitigation: Review the sharing flow and the host runtime's network and shell access before use; the broker's instructions limit responses to task-relevant facts from the prepared slice.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/samuel-wei/skills/javis-access-broker)
- [Submit answer schema](references/submit-answer.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [A JSON decision payload with concise text points for an answer, a clarification question, or a decline reason.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One response per request; answer points cite the prepared information slice.]

## Skill Version(s):

0.2.2 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
