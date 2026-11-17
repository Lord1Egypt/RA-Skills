## Description:

Generate production-ready image prompts for Midjourney and other image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to create, refine, critique, translate, and vary image-generation prompts for Midjourney and other image models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Midjourney and English prompt text when the request is underspecified.

Mitigation: Specify the target image model and prompt language when those choices matter.

Risk: Built-in examples and defaults may influence the generated aesthetic.

Mitigation: Provide brand constraints, prohibited content, and desired style direction for production prompts.

Risk: Midjourney model defaults and parameter compatibility can change over time.

Mitigation: Check official Midjourney documentation before relying on time-sensitive default-version or feature-compatibility claims.

## Reference(s):

- [Midjourney Prompt Guide](references/midjourney-prompt-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prompt text with optional numbered variants and short change notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Midjourney when no target model is specified; final prompt text defaults to English unless the user requests another language.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
