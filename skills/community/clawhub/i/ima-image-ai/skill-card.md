## Description: <br>
IMA Image Generator helps agents generate or transform images through the IMA Open API for text-to-image, image-to-image, style transfer, and reference-image continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to create image outputs for posters, thumbnails, logos, product photos, social graphics, art, and illustrations. It supports prompt-only generation, reference-image transformation, style transfer, and model selection through IMA's live catalog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation metadata, and local input images can be sent to IMA remote services during generation or image-to-image workflows. <br>
Mitigation: Use only approved content, avoid private or regulated images unless that use is authorized, and review generated URLs before sharing. <br>
Risk: The skill requires an IMA_API_KEY and sends it to IMA service endpoints for authorization. <br>
Mitigation: Use a scoped or test key for initial testing, keep keys out of shared terminals and logs, and rotate keys if exposure is suspected. <br>
Risk: Higher resolution or multi-output requests can consume more credits and take longer. <br>
Mitigation: Start with lower-cost settings such as 512px or 1k and n=1, then increase quality or variants after the composition is validated. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/allenfancy-gan/ima-image-ai) <br>
- [IMA Homepage](https://www.imaclaw.ai) <br>
- [References Map](artifact/references/README.md) <br>
- [Image Capability](artifact/capabilities/image/CAPABILITY.md) <br>
- [Catalog-Aware Dynamic Model Selection](artifact/references/shared/catalog-aware-selection.md) <br>
- [Security And Network](artifact/references/shared/security-and-network.md) <br>
- [API Contract And Errors](artifact/references/operations/api-contract-and-errors.md) <br>
- [Parameter Tuning](artifact/capabilities/image/references/parameter-tuning.md) <br>
- [Image Scenarios](artifact/capabilities/image/references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Remote image URLs, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and machine-readable JSON from the runtime CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns remote HTTPS image URLs; local image inputs may be uploaded to IMA services for image-to-image workflows.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; artifact frontmatter is 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
