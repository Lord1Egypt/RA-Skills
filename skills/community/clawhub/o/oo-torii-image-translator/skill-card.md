## Description:

Use the Torii Image Translator connector to extract text from public images, translate images, remove text or objects, and typeset translated text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to extract or translate text in public images, clean images, and typeset translated text through Torii Image Translator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs downloaded installation code and may automatically install and synchronize other agent skills.

Mitigation: Review the CLI installer and its skill-sync behavior separately, and approve them before setup.

Risk: Image processing may use Torii credits.

Mitigation: Choose the public images to process and agree on credit spending before processing.

## Reference(s):

- [Torii Image Translator](https://toriitranslate.com)
- [Torii API documentation](https://toriitranslate.com/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Image files, Guidance]

**Output Format:** [Structured JSON responses and downloadable PNG images, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent: structured OCR results or a processed PNG image.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
