## Description:

PromptBuddy optimizes user inputs into structured prompts, displays the first several optimized lines before answering, and skips simple queries when appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steventsang18](https://clawhub.ai/user/steventsang18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to transform informal requests into more structured prompts before the agent answers. It is intended for prompt optimization and visible prompt-preview workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes every user input through a prompt optimizer, which can expose secrets, private documents, credentials, or regulated data.

Mitigation: Use the skill only when prompt optimization is intentional, avoid sensitive inputs, and add opt-in behavior plus redaction before deployment with private or regulated data.

Risk: The artifact references a local smart_engine.py script that is not included for review.

Mitigation: Review and scan the script before installation, use safe argument passing, and restrict execution to trusted local environments.

## Reference(s):

- [PromptBuddy ClawHub skill page](https://clawhub.ai/steventsang18/skills/prompt-buddy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with prompt-preview text and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays the first 6-8 lines of the optimized prompt and may return a short skip notice for simple queries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
