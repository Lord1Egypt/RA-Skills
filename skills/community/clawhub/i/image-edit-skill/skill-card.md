## Description: <br>
Expert Pillow (PIL) skill for image processing, manipulation, and analysis, including image editing, batch processing, watermarking, format conversion, and image information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangruihan](https://clawhub.ai/user/yangruihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and content operations teams use this skill to automate local 2D image editing, batch conversion, thumbnail generation, watermarking, and metadata inspection with Pillow-based scripts and reference guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local image files may contain sensitive EXIF or metadata that could be exposed in analysis output or preserved when files are shared. <br>
Mitigation: Review metadata before exporting or sharing outputs, and avoid preserving EXIF unless it is required for the workflow. <br>
Risk: Batch processing can alter many files or produce confusing results if inputs and outputs are mixed. <br>
Mitigation: Write batch results to a separate output directory, preserve original files, and test operations on one image before processing a full set. <br>
Risk: The dependency list is broad and unpinned for normal image-processing use. <br>
Mitigation: Pin current patched dependency versions and remove openpyxl if spreadsheet support is not required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yangruihan/image-edit-skill) <br>
- [Pillow image processing skill README](README.md) <br>
- [Pillow operations reference](references/common_operations.md) <br>
- [Image processing best practices](references/best_practices.md) <br>
- [Usage examples](EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python snippets; included scripts produce image files or text/JSON metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local image files with Pillow-based command-line scripts; image information output can include EXIF and other metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
