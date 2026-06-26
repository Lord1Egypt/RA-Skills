## Description: <br>
Converts PDF files into PNG or JPG images with configurable scale and page ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert local PDF documents into PNG or JPG image files, including selected pages and higher-resolution renders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local PDFs and writes output files, so sensitive PDFs or target paths may be exposed to the local runtime. <br>
Mitigation: Run it only on PDFs and output locations you are comfortable giving the tool access to. <br>
Risk: Existing output files can be overwritten during image generation. <br>
Mitigation: Use a dedicated output directory or review target filenames before execution. <br>
Risk: The skill depends on npm packages for PDF rendering and canvas output. <br>
Mitigation: Verify npm dependencies, including pdfjs-dist and canvas, come from trusted sources before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fly3094/pdf-to-images) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [PNG or JPG image files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports scale values from 0.5 to 5.0 and optional page ranges.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
