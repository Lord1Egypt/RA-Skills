## Description:

Generates brand-quality product photos and paid-social visuals through the Higgsfield CLI with mode-specific prompt enhancement and image URL delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[higgsfield](https://clawhub.ai/user/higgsfield)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, and marketing teams use this skill to turn product photos or product descriptions into studio, lifestyle, banner, carousel, ad, virtual try-on, conceptual, or restyled visual outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap step may execute an unverified live GitHub installer before other skill actions.

Mitigation: Prefer installing the Higgsfield CLI from a pinned or verified release and review what the installer changes before use.

Risk: Local product images passed with --image are uploaded to Higgsfield for generation.

Mitigation: Use only product images approved for upload to Higgsfield and avoid sensitive, private, or unreleased assets unless that processing is authorized.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/higgsfield/skills/higgsfield-product-photoshoot)
- [Higgsfield CLI installer](https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Markdown list of generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final responses are expected to contain only generated image URLs; local product images supplied with --image may be uploaded to Higgsfield for generation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
