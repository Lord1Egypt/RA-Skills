## Description:

Full AI image creation workflow for intent classification, prompt enhancement, multi-direction generation via fal.ai, and error recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, enhance, generate, edit, and present AI-generated images through fal.ai-backed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be uploaded to fal.ai, including private, client, biometric, or otherwise sensitive images.

Mitigation: Review provider handling and user consent requirements before use, and avoid submitting sensitive images unless that transfer is approved.

Risk: Generated outputs may be saved locally and could persist in user-accessible folders.

Mitigation: Confirm the destination path before saving and apply local retention, access control, and cleanup practices appropriate for the content.

Risk: Safety-blocked prompts may be automatically rewritten for another attempt.

Mitigation: Require explicit user review and approval before retrying with a cleaned or rephrased prompt.

Risk: The workflow requires a fal.ai API key through FAL_API_KEY.

Mitigation: Store the key in an environment variable or secret manager and avoid embedding it in generated code, files, or chat output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-ai-image)
- [Canlah AI](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets, image URLs, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call fal.ai using FAL_API_KEY, upload reference images, generate up to four batch directions, and save generated images locally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
