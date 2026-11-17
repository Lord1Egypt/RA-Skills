## Description:

Prepare an image for a destination with format, transparency, or file-size requirements. Choose a delivery format, test one export in the browser, and verify the downloaded file before batch conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnvxstudio](https://clawhub.ai/user/cnvxstudio)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing images for a website, upload form, or collaborator can use this skill to choose a suitable export format, test one image, and verify the delivered copy before processing a batch. It preserves the source and distinguishes proposed settings from checks that were actually completed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive images may be exposed to a website or external provider during processing.

Mitigation: Process only images the user authorized, review the website's privacy terms before sensitive uploads, and disclose that optional AI actions send the image and instructions to an external provider.

Risk: An export may not meet the destination's requirements or preserve image details or transparency.

Mitigation: Keep the original, test one sample, inspect the downloaded file's actual format, dimensions, size, transparency, and visual fidelity, and report destination acceptance as unverified unless it was tested.

## Reference(s):

- [Free Photo Editor](https://freephotoeditor.io/)
- [Source repository (server-resolved provenance)](https://github.com/cnvxstudio/image-export-preflight)
- [ClawHub skill release](https://clawhub.ai/cnvxstudio/skills/image-export-preflight)

## Skill Output:

**Output Type(s):** [Files, Guidance, Markdown]

**Output Format:** [An image delivery copy in the requested format, with a concise Markdown record of observed properties and unperformed checks; otherwise an export plan.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the source image; verifies format, dimensions, file size, transparency, and visual fidelity when processing tools are available.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
