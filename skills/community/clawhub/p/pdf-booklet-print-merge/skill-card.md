## Description: <br>
Merge PDF files and create booklet-ready 2-up duplex output for saddle-stitch printing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninjahwdragon](https://clawhub.ai/user/ninjahwdragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, print-prep operators, and document owners use this skill to merge local PDF files and generate booklet-imposed PDFs for landscape duplex, short-edge flip, center-fold printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Existing output files can be overwritten when the selected output path already exists. <br>
Mitigation: Choose a deliberate output path and keep source PDFs separate from generated output files. <br>
Risk: The skill processes all PDFs in the input directory. <br>
Mitigation: Point --input-dir only at a folder containing PDFs intended for the merge and booklet layout. <br>
Risk: The runtime depends on the external pypdf package. <br>
Mitigation: Install pypdf from a trusted package source in a normal project folder or virtual environment. <br>


## Reference(s): <br>
- [Publish Checklist](references/publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated PDF file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a booklet-imposed PDF and, unless disabled, a sequential merged source PDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
