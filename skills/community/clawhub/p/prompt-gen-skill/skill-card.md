## Description:

Generate detailed, optimized AI art prompts for Midjourney, DALL-E, and Stable Diffusion, including style, lighting, and composition keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agents use this skill to turn short image ideas into prompt variants for common image-generation systems. It is suited for drafting prompt text with style, lighting, composition, and quality modifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships with an exposed payment API key and attempts paid SkillPay charges.

Mitigation: Remove the exposed key, rotate any affected credential, and document the billing flow before use.

Risk: The skill sends the provided user_id to SkillPay.

Mitigation: Avoid personal identifiers as user_id and disclose the external data flow to users.

Risk: The release currently cannot run because of a Python indentation error.

Mitigation: Fix the syntax error and verify payment failure paths before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loverun321/skills/prompt-gen-skill)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object containing prompt variants and tips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Randomized prompt modifiers; attempts a paid SkillPay charge per call.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
