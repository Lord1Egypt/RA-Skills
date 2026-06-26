## Description: <br>
Converts static images such as slides, posters, and infographics into editable PowerPoint files using OCR, text masking, inpainting, and PPTX assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MinuteMighty](https://clawhub.ai/user/MinuteMighty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content editors use this skill to turn static slide, poster, or infographic images into editable .pptx files with selectable text boxes over a reconstructed background. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Python ML dependencies and may download and cache OCR and inpainting models on first use. <br>
Mitigation: Install only in environments where those dependencies and local model caches are acceptable, or bypass downloads with precomputed OCR and skipped inpainting when appropriate. <br>
Risk: Using --work-dir can save intermediate OCR text and image masks derived from the input image. <br>
Mitigation: Avoid --work-dir for confidential images unless retaining those intermediate files locally is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MinuteMighty/image2pptx) <br>
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) <br>
- [LAMA inpainting](https://github.com/advimman/lama) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [PowerPoint .pptx file, optional JSON report and intermediate image files, and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save intermediate OCR text, masks, background images, and a report when --work-dir is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
