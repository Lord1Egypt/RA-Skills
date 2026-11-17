## Description:

Transforms vague task requests into clear, structured expert prompts for large language models such as Gemini, GPT, Claude, and Qwen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dk-style](https://clawhub.ai/user/dk-style)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and AI users use this skill to turn brief or incomplete requests into structured prompts with role, context, goals, constraints, workflow, output format, and initialization sections. It also explains key prompt design choices so users can refine the prompt for their model and task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Simplified Chinese output, which may surprise users expecting another language.

Mitigation: Specify the desired output language when asking the skill to generate a prompt.

Risk: The skill may fill missing request details with reasonable assumptions that do not match the user's intent.

Mitigation: Review the stated assumptions and generated prompt before using it in a production workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dk-style/skills/prompt-engineer-1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown response containing demand analysis, a structured prompt in a markdown code block, and a short design explanation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Simplified Chinese unless the user specifies another language.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
