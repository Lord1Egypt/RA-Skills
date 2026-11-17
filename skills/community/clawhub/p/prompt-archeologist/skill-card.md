## Description:

Reverse-engineers high-quality, reusable prompts from messy conversations, vague requests, or rough user descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goutham-nekkalapu](https://clawhub.ai/user/goutham-nekkalapu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn messy conversations, vague task descriptions, or rough workflow notes into reusable, portable prompts with brief notes about assumptions and customization points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may summarize sensitive conversation context into a reusable prompt shown in chat.

Mitigation: Avoid invoking it around sensitive context unless that context can safely be restated in the generated prompt.

Risk: Vague source material may cause the generated prompt to encode assumptions.

Mitigation: Review the excavation notes and customize placeholders, constraints, and assumptions before reusing the prompt.

## Reference(s):

- [Prompt Archeologist ClawHub listing](https://clawhub.ai/goutham-nekkalapu/skills/prompt-archeologist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a copy-ready prompt code block and brief excavation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include placeholders for reusable inputs and concise notes about source signals, assumptions, and customization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
