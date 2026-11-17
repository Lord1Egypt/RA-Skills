## Description:

Optimizes long or unclear user prompts into clearer, structured, actionable instructions and may continue execution from the optimized prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjinhongmy-pixel](https://clawhub.ai/user/wangjinhongmy-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn long, scattered, or ambiguous requests into clearer prompts before an agent acts on them. It is intended for prompt clarification, task structuring, and reducing ambiguity in agent instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically rewrite and execute ordinary user requests without explicit approval.

Mitigation: Require explicit invocation or user confirmation before acting on the optimized prompt.

Risk: Automatic prompt rewriting can change how broad or ambiguous requests are interpreted.

Mitigation: Review the optimized prompt before execution and ask for clarification when the user's intent or required context is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjinhongmy-pixel/skills/prompt-tuner)
- [Publisher profile](https://clawhub.ai/user/wangjinhongmy-pixel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with an optimized prompt block and follow-up guidance or execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for clarification before execution when intent, required information, file paths, time cost, or irreversible actions are uncertain.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
