## Description: <br>
Use when the user wants virtual try-on, dress a person in clothing from reference photos, garment fitting on a model still, or ecommerce fashion compositing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pruna-ai](https://clawhub.ai/user/pruna-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide virtual fashion try-on workflows, including uploading person and garment images, calling Pruna's p-image-try-on API, and checking generated outputs for identity and scene preservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected person, garment, and optional pose images to Pruna's external API for generation. <br>
Mitigation: Use only images the user has rights and consent to process, avoid sensitive or identifying photos when possible, and disclose the external processing step before use. <br>
Risk: The workflow requires a Pruna API key. <br>
Mitigation: Keep PRUNA_API_KEY out of chats, committed files, and generated artifacts; use environment variables or ignored local configuration. <br>
Risk: Virtual try-on outputs can change clothing while preserving identity and scene context, creating privacy and consent concerns for recognizable people. <br>
Mitigation: Confirm the user has permission to edit recognizable person images and review outputs before reuse or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pruna-ai/skills/p-image-try-on) <br>
- [Pruna p-image-try-on model docs](https://docs.api.pruna.ai/guides/models/p-image-try-on) <br>
- [Runware virtual try-on guide](https://runware.ai/docs/models/prunaai-p-image-try-on/guides/virtual-try-on) <br>
- [Replicate p-image-try-on page](https://replicate.com/prunaai/p-image-try-on) <br>
- [Pruna API shared reference](references/pruna-api.md) <br>
- [API credentials](references/api-credentials.md) <br>
- [p-image-try-on quality checklist](references/p-image-try-on-quality-checklist.md) <br>
- [Generation diversity](references/generation-diversity.md) <br>
- [Generation quality checklist hub](references/generation-quality-checklists.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides image upload, prediction polling, output download, seed selection, and visual quality review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
