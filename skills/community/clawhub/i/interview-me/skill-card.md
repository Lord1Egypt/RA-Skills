## Description:

Extracts a user's underlying intent through one-question-at-a-time interviewing until the agent has high confidence about the request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to clarify ambiguous requests before implementation by interviewing the user one question at a time and summarizing the intended outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the stated interview purpose conflicts with broad automation, file/API, credential, and command-execution guidance.

Mitigation: Use the skill only in environments where file access and command execution are acceptable, and require explicit user confirmation before any file, API, credential, or shell-command activity.

Risk: The skill may produce automation-oriented guidance beyond intent clarification.

Mitigation: Constrain use to clarifying requirements and review any proposed actions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/interview-me)
- [SkillHub homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or structured JSON describing clarified user intent, status, and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask sequential clarifying questions before producing a final intent summary.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
