## Description:

Generate images from text prompts using the WellAPI gpt-image-2 model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolujava](https://clawhub.ai/user/laolujava)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language image prompts into local image files through the WellAPI gpt-image-2 endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation requests are sent to WellAPI, and the skill can store a WellAPI API key locally.

Mitigation: Use a protected WELLAPI_API_KEY environment variable when possible, review WellAPI handling expectations before use, and avoid placing sensitive information in prompts.

Risk: The onboarding flow points users to a referral registration URL and provides vendor-specific account-group remediation for errors.

Mitigation: Review the registration URL and verify any account-group changes directly in WellAPI before following the remediation guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laolujava/skills/gpt-image-2-generation)
- [WellAPI](https://wellapi.ai)
- [WellAPI image generations endpoint](https://wellapi.ai/v1/images/generations)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown status text with saved image file paths and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as jpeg, png, or webp files; API setup may store a local WellAPI key or use WELLAPI_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
