## Description: <br>
AI Image Kit provides intelligent image processing and enhancement, including image enhancement, smart cropping, format conversion, and OCR text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to process local images, enhance quality, crop images for composition or thumbnails, and extract text from images with OCR. It is suited for workflows that need Python-based image manipulation and local file outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts read local image files and write to caller-provided output paths, which can overwrite existing files. <br>
Mitigation: Use a virtual environment, review dependencies before installation, and choose input and output paths deliberately. <br>
Risk: OCR output can be incomplete or inaccurate depending on image quality, language packs, and Tesseract configuration. <br>
Mitigation: Review extracted text before relying on it and confirm the required Tesseract languages are installed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/image-ai-kit) <br>
- [Project Homepage](https://github.com/openclaw/image-ai-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and generated image or OCR output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-provided local image paths and writes results to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
