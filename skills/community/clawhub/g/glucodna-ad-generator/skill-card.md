## Description:

Generates 1024x1024 Chinese GlucoDNA kidney-protection advertising images with the product image and product copy using the Gemini API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangyisheng9-bot](https://clawhub.ai/user/jiangyisheng9-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and operators use this skill to create Chinese promotional image assets for GlucoDNA using product information, a product image, and Gemini image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gemini API keys may be exposed if stored in a shared workspace file.

Mitigation: Use a dedicated, restricted GEMINI_API_KEY from a protected environment or secret manager and avoid storing live keys in TOOLS.md.

Risk: The skill downloads a remote product image and writes a generated file to disk.

Mitigation: Run the skill in a reviewed virtual environment and confirm the intended output path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangyisheng9-bot/skills/glucodna-ad-generator)
- [GlucoDNA product image](https://hk3.com.my/wp-content/uploads/2024/04/PRODUCT-SIZE-500PX-07.png)

## Skill Output:

**Output Type(s):** [image file, text, shell commands, configuration]

**Output Format:** [PNG image file with console status text and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to a 1024x1024 advertisement image saved to the user's Desktop unless an output path is supplied.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
