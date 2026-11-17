## Description:

Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".

This skill is ready for commercial/non-commercial use.

## Publisher:

[nox-admin](https://clawhub.ai/user/nox-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to stress-test plans, ideas, and designs through a structured adversarial interview. When repository context can answer a question, the skill directs the agent to inspect the codebase instead of asking the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: For repository-related plans, the skill may cause the agent to inspect project files while forming questions and recommendations.

Mitigation: Invoke the skill only in workspaces where codebase review is intended and appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown conversational responses with questions and recommended answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include codebase inspection findings when the user's workspace contains relevant evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
