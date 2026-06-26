## Description: <br>
Compresses a given PDF file to reduce its size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upwell](https://clawhub.ai/user/upwell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to compress a local PDF file with a selectable compression level and receive JSON containing the output path and before-and-after file sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the supplied PDF and creates a compressed copy next to it, which may leave an additional local copy of sensitive content. <br>
Mitigation: Use it only on PDFs intentionally provided for compression, review the generated output path, and avoid highly sensitive PDFs unless the local environment and Python dependency chain are trusted. <br>
Risk: Higher compression can rewrite images at lower DPI and quality, which may reduce document fidelity. <br>
Mitigation: Keep the original PDF and review the compressed result before replacing or distributing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/upwell/pdf-compressor) <br>


## Skill Output: <br>
**Output Type(s):** [json, files] <br>
**Output Format:** [JSON status object with original size, compressed size, and compressed PDF path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a compressed PDF copy next to the input file.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
