## Description:

Convert static images such as slides, posters, and infographics into editable PowerPoint files using OCR, text masking, inpainting, and python-pptx assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minutemighty](https://clawhub.ai/user/minutemighty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and knowledge workers use this skill through an agent to convert slide, poster, or infographic images into editable PowerPoint decks with OCR-created text boxes and reconstructed backgrounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large OCR and inpainting dependencies plus first-use model downloads can increase dependency and model supply-chain exposure.

Mitigation: Install in a sandbox or virtual environment, pin repository and dependency versions, and use --ocr-json with --skip-inpaint when model downloads should be avoided.

Risk: OCR grouping and inpainting can produce editable text or backgrounds that do not fully match dense charts, photo overlaps, large decorative fonts, or very large images.

Mitigation: Review generated PPTX files against the source image, warn users about likely artifacts, and adjust options such as --dilation or --skip-inpaint for difficult inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minutemighty/skills/image2pptx)
- [px-image2pptx source and docs](https://github.com/JadeLiu-tech/px-image2pptx)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [LAMA inpainting](https://github.com/advimman/lama)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files, Configuration]

**Output Format:** [Markdown guidance with shell and Python snippets; generated PowerPoint files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local PPTX outputs and optional intermediate files; OCR and inpainting models may download and cache locally on first use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
