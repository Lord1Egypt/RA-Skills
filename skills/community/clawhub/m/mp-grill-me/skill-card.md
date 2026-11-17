## Description:

Mp Grill Me helps an agent pressure-test a plan or design by asking one focused question at a time, recommending answers, and inspecting the codebase when useful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and teams use this skill to examine plans or designs through persistent, step-by-step questioning. It is intended to surface unresolved decisions, dependencies, and recommended answers, including by inspecting the current codebase when that is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect the current codebase while reviewing a plan or design.

Mitigation: Use it only in workspaces where local code inspection by the agent is acceptable.

Risk: Persistent questioning and recommended answers may influence planning decisions even when context is incomplete.

Mitigation: Review recommendations before acting on them, especially for high-impact architecture, security, or product decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/mp-grill-me)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversational prompts with recommended answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks one question at a time and may include codebase findings when local inspection answers a review question.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
