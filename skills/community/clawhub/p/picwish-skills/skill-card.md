## Description: <br>
Root routing skill for PicWish image processing capabilities, routing image tasks to background removal, face cutout, upscaling, object or watermark removal, ID photo generation, colorization, compression, OCR, smart crop, and clothing segmentation sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[px94](https://clawhub.ai/user/px94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route common PicWish image-processing requests to the correct sub-skill and return saved outputs or OCR files. It is intended for tasks such as background removal, image enhancement, object cleanup, ID photos, document correction, text extraction, and clothing mask generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, supplied image URLs, and OCR inputs are sent to PicWish for remote processing. <br>
Mitigation: Use only authorized media and avoid sensitive faces, IDs, private documents, confidential screenshots, or regulated data unless the user has approval. <br>
Risk: Returned result URLs may contain temporary authentication query parameters. <br>
Mitigation: Treat complete result URLs as sensitive temporary links; prefer local saved paths and avoid unnecessary logging or sharing. <br>
Risk: Changing PICWISH_BASE_URL can redirect processing away from the expected PicWish endpoint. <br>
Mitigation: Set PICWISH_BASE_URL only to a trusted PicWish endpoint, or leave it unset so the skill uses its regional defaults. <br>


## Reference(s): <br>
- [ClawHub PicWish Skills Release](https://clawhub.ai/px94/picwish-skills) <br>
- [PicWish API](https://picwish.com) <br>
- [PicWish API Key](https://picwish.com/my-account?subRoute=api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON status with result URLs and local saved paths, plus downloaded image or OCR output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PicWish API key. Image inputs are processed by PicWish remote APIs, and temporary result URLs should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.7 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
