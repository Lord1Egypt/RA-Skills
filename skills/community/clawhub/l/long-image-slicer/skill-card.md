## Description: <br>
Long Image Slicer slices long screenshots into 9:16 image segments and can produce sliced images, ZIP archives, DOCX files, and A4 PDFs while trying to avoid cutting through text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunkai](https://clawhub.ai/user/yunkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a long screenshot, chat log image, image URL, or local image path and asks for slicing, PDF conversion, or printable document output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots and generated slices, ZIP archives, DOCX files, or PDFs may contain private user content saved on disk. <br>
Mitigation: Use only the needed input files, choose an appropriate output directory, and delete sensitive generated files when they are no longer needed. <br>
Risk: Optional image URL and local path handling can process untrusted images or unintended sensitive local files. <br>
Mitigation: Use trusted image URLs and explicit non-sensitive local paths supplied for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yunkai/long-image-slicer) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated image, ZIP, DOCX, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local images or trusted image URLs and writes generated artifacts to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
