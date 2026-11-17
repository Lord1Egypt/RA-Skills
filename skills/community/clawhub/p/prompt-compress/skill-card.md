## Description:

Prompt Compress helps agents analyze prompts, extract keywords, remove redundant wording, and produce shorter prompts that preserve the user's intended meaning while reducing token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackzh1982](https://clawhub.ai/user/jackzh1982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and agent users can use this skill to shorten long prompts, extract core requirements, structure task instructions, and estimate token savings before sending prompts to a model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggressive prompt compression can omit context, change nuance, or produce instructions that no longer fully match the original request.

Mitigation: Review compressed prompts before sending them onward, especially when using heavy or minimal compression levels.

Risk: Token counts are estimated with simplified Chinese, English, and other-character heuristics and may differ from a target model's tokenizer.

Mitigation: Treat token savings as approximate and verify with the deployment model's tokenizer for budget-sensitive workflows.

## Reference(s):

- [Token calculation reference](references/token-calculation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with compressed prompt content, token estimates, keyword analysis, and optional local Python command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compression levels include light, medium, heavy, and minimal; token counts are estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
