## Description:

Translate text in a public image with ImageTranslate.AI, preserve the selected layout style, and return a rendered PNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ImageTranslate.AI users use the skill to translate text in a public image, preserve a selected layout style, and receive the translated image as a rendered PNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translations may incur charges, including before an oversized rendered result is rejected.

Mitigation: Get authorization for the selected image, translation, and spending; review the action schema and avoid blind retries after errors.

Risk: First-time setup can run an external installer and modify bundled skills; the installer and hosted service were not audited.

Mitigation: Review the CLI installer and its bundled-skill changes before approving setup.

## Reference(s):

- [ImageTranslate.AI](https://imagetranslate.ai)
- [ImageTranslate.AI API documentation](https://imagetranslate.ai/docs/api)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Images, Files, API Calls]

**Output Format:** [Rendered PNG image with a JSON action response and execution metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The rendered image is returned through transit storage; the documented maximum is 50 MB.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
