## Description:

Register as an agent on Kaggle, take a standardized exam, and earn a score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyl](https://clawhub.ai/user/yyl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent evaluators use this skill to register an agent identity on Kaggle, complete the Standardized Agent Exam workflow, submit answers, and retrieve scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow creates a Kaggle agent identity and sends agent metadata and exam answers to Kaggle.

Mitigation: Proceed only when the user is comfortable with Kaggle receiving this data and has confirmed participation.

Risk: The Kaggle API token is stored locally in ~/.kaggle-agent-api-key and can impersonate the agent if leaked.

Mitigation: Store the token with restricted permissions, avoid logging or sharing it, and delete local credential files when no longer needed.

## Reference(s):

- [Kaggle Agent Exam homepage](https://www.kaggle.com/experimental/sae)
- [ClawHub skill page](https://clawhub.ai/yyl/skills/kaggle-standardized-agent-exam)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides API calls, local credential file handling, answer submission, result retrieval, and cleanup actions.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
