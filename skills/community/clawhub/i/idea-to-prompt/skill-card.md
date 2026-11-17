## Description:

Converts rambling or disorganized user thoughts into clear, structured, actionable prompts for coding, content, planning, or general tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackcorvu](https://clawhub.ai/user/blackcorvu)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to turn stream-of-consciousness ideas into actionable prompts. It helps classify the request, identify missing or conflicting details, ask targeted clarification questions when needed, and produce a prompt the user can review or execute.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad brainstorming-style phrases and may ask the agent to transform incomplete user ideas into a prompt.

Mitigation: Use the skill's clarification step when ambiguity could change the output direction, and have the user review the structured prompt before execution.

Risk: The skill instructions are mainly Chinese, which may affect reviewers or operators who cannot read Chinese.

Mitigation: Review the bilingual README summary and verify the Chinese instruction flow before deploying in environments where operator review is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blackcorvu/skills/idea-to-prompt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prompt templates with concise clarification questions when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask 1-3 targeted clarifying questions before producing the final structured prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
