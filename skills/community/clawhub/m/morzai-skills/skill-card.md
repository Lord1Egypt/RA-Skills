## Description:

Unified entry point for Morzai workflows that routes ecommerce image-editing requests through api/commands.json into the matching child skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morzai-app](https://clawhub.ai/user/morzai-app)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to route product-image requests into apparel recoloring, garment retouching, clothing cleanup, or ecommerce listing image generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, reference images, and listing context may be sent to Morzai/Lumo remote services or processed through the morzai CLI.

Mitigation: Use the skill only when that data sharing matches the user's policy, and avoid confidential product photos unless approved.

Risk: Credentials may be required for CLI or remote-service access.

Mitigation: Use environment variables or the CLI authentication flow, and do not expose API keys, authorization headers, cookies, or signed upload URLs in outputs or logs.

Risk: Marketplace image generation or editing can produce artifacts, over-processing, or visuals that do not meet platform requirements.

Mitigation: Review generated images before publication, use the documented platform and quality guidance, and keep fallback messages focused on actionable next steps when generation fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/morzai-app/skills/morzai-skills)
- [Root Routing Skill](artifact/SKILL.md)
- [Command Routing Map](artifact/api/commands.json)
- [Apparel Recolor Intent Mapping](artifact/skills/apparel-recolor/references/intent-mapping.md)
- [Recolor Execution Guardrails](artifact/skills/apparel-recolor/references/fabric-texture-guide.md)
- [Clothing Adjustment Intent Mapping](artifact/skills/clothing-adjustment/references/intent-mapping.md)
- [Garment Retouch Intent Mapping](artifact/skills/garment-retouch/references/intent-mapping.md)
- [Ghost Mannequin Specs](artifact/skills/garment-retouch/references/ghost-mannequin-specs.md)
- [Ecommerce Product Kit Output Spec](artifact/skills/ecommerce-product-kit/references/output-spec.md)
- [Ecommerce Product Kit Error Fallback](artifact/skills/ecommerce-product-kit/references/error-fallback.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with optional CLI commands, saved file paths, and image-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference generated ecommerce image files through remote Morzai/Lumo services or the morzai CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
