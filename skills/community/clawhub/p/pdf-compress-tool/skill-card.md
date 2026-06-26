## Description: <br>
Compress PDF files to a target size or by percentage, using a Ghostscript + pikepdf + QPDF multi-stage pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsonklose](https://clawhub.ai/user/johnsonklose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document workflows use this skill to reduce PDF file size for sharing, upload limits, or storage while choosing a target size, reduction percentage, output path, and quality level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the pikepdf Python package during normal use. <br>
Mitigation: Preinstall dependencies in a managed virtual environment before running the skill. <br>
Risk: The skill writes compressed PDFs and can process whole directories. <br>
Mitigation: Use explicit output paths and keep backups before compressing important files or batches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsonklose/pdf-compress-tool) <br>
- [Ghostscript downloads](https://ghostscript.com/releases/gsdnld.html) <br>
- [QPDF releases](https://github.com/qpdf/qpdf/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands] <br>
**Output Format:** [Compressed PDF files with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output PDFs for single-file or batch compression; compression results depend on installed PDF tools and selected quality settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
