## Description: <br>
Extracts and saves QR codes from each page of a PDF by converting pages to images and detecting QR regions with padding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mywebliu](https://clawhub.ai/user/mywebliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to batch extract QR code images from local PDF files, including customer-provided PDFs that contain generated QR codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies with --break-system-packages can modify the global Python environment. <br>
Mitigation: Use a Python virtual environment before installing the required packages. <br>
Risk: Full-page intermediate images may contain sensitive content from the source PDF. <br>
Mitigation: Choose a protected output directory and remove intermediate page images after confirming the extracted QR files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mywebliu/pdf-qr-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cropped QR images and full-page intermediate images to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
