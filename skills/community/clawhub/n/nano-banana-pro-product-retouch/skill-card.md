## Description:

Nano Banana Pro 商品精修 helps agents retouch product photos by removing dust, fingerprints, scratches, color and white-balance issues, reflections, background artifacts, and shadow problems while preserving product geometry, packaging text, materials, labels, and disclosed defects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, product photographers, designers, and agents use this skill to generate controlled product-photo retouching prompts and AI Hive image-generation commands for marketplace-ready images. It supports cleanup, reflection control, color calibration, background and contact-shadow repair, and SKU consistency while preserving product facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI Hive API credentials and can send credentials and product images to a user-configured base URL.

Mitigation: Use a dedicated virtual environment, keep the default endpoint unless the alternate endpoint is fully trusted, and rotate the API key if it may have been used with an untrusted endpoint.

Risk: Product images and generated task data are uploaded to AI Hive during normal use.

Mitigation: Confirm that the uploaded product photos, packaging text, labels, and generated outputs are appropriate to share with AI Hive before running the workflow.

Risk: Retouching can remove or obscure defects that may need to remain visible.

Mitigation: Compare original and retouched images and verify that required damage, wear, product differences, labels, logos, and packaging facts remain accurate before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-product-retouch)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with inline bash commands; the bundled CLI can emit JSON task data and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and at least one input image for the skill-specific generate command.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
