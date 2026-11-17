## Description:

Routes agent image-processing requests to 11 PicWish API-backed skills for background removal, face cutouts, upscaling, object and watermark removal, ID photos, colorization, compression, OCR, smart cropping, and clothing segmentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[px94](https://clawhub.ai/user/px94)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route image-processing requests to the appropriate PicWish sub-skill and run PicWish API tasks that return processed images, OCR outputs, masks, or saved local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected images and OCR inputs to PicWish servers, which can expose sensitive faces, IDs, documents, or proprietary images to third-party processing.

Mitigation: Use only images that the user is authorized to process, avoid sensitive content unless consent and third-party processing are acceptable, and review the skill before deployment.

Risk: Endpoint overrides can redirect requests away from the intended PicWish service.

Mitigation: Leave PICWISH_BASE_URL unset unless it is pinned to a trusted HTTPS PicWish endpoint.

Risk: Complete result URLs may contain access tokens and can remain useful during their validity window.

Mitigation: Do not share complete result URLs outside trusted channels; prefer saved local outputs when possible.

Risk: The security review flagged unsafe handling around shell execution.

Mitigation: Execute only the declared Node.js entry points in a least-privilege workspace and review any optional workspace helper before allowing it to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/px94/skills/picwish-skills)
- [PicWish API](https://picwish.com)
- [PicWish API Key](https://picwish.com/open-api)
- [README](artifact/README.md)
- [Security Model](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON execution inputs, saved file paths, and result URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PicWish API key; processed images, masks, and OCR outputs may be saved locally, and PicWish result URLs can be time-limited and token-bearing.]

## Skill Version(s):

1.0.7 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
