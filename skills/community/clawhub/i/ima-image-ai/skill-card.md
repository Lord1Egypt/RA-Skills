## Description:

Generates and transforms images through the IMA Open API for text-to-image, image-to-image, style transfer, and reference-image continuity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to request AI-generated or transformed images for product photos, posters, thumbnails, logos, art, illustrations, and social graphics through IMA Studio services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed through troubleshooting or network behavior.

Mitigation: Use a scoped or test IMA_API_KEY first, keep it in the environment, avoid printing the full key, and rotate the key if it is exposed.

Risk: Prompts and selected local images are sent to IMA Studio services.

Mitigation: Do not submit sensitive prompts, confidential source images, or private user data unless the deployment has approved that data flow.

Risk: Custom endpoint configuration could redirect credentials or image data.

Mitigation: Use the documented IMA endpoints and avoid custom IMA_BASE_URL or IMA_IM_BASE_URL values unless they have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/allenfancy-gan/skills/ima-image-ai)
- [IMA Studio Homepage](https://www.imaclaw.ai)
- [References Map](references/README.md)
- [Security And Network](references/shared/security-and-network.md)
- [Catalog-Aware Dynamic Model Selection](references/shared/catalog-aware-selection.md)
- [Image Models](capabilities/image/references/models.md)
- [Parameter Tuning](capabilities/image/references/parameter-tuning.md)
- [Image Scenarios](capabilities/image/references/scenarios.md)
- [Troubleshooting](references/operations/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger API calls that return remote HTTPS image URLs; generated images are not downloaded by default.]

## Skill Version(s):

1.0.14 (source: server release metadata, created 2026-04-23; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
