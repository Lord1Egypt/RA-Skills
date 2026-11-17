## Description:

Guides agents to perform adversarial review of non-trivial decisions before overconfident assumptions become costly mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to challenge architecture choices, non-trivial code changes, safety claims, deployments, migrations, and other high-risk or irreversible work before proceeding. It provides a bounded doubt cycle for extracting the artifact and contract, requesting adversarial review, reconciling findings, and deciding when to stop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewer subagents may increase cost or expose more context than necessary if used without scoping.

Mitigation: Limit reviewer input to the artifact and contract, and require explicit authorization for each cross-model review.

Risk: The workflow is primarily written in Chinese, which may cause misunderstandings for users who do not work in Chinese.

Mitigation: Translate the skill or add a language preference note before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-doubt-driven-development)
- [Publisher profile](https://clawhub.ai/user/qqyougitcom)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with checklists and adversarial review prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No direct code execution; may ask the agent to prepare scoped reviewer prompts.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
