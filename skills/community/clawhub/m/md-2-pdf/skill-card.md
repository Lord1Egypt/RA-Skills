## Description: <br>
Convert markdown files to clean, formatted PDFs using reportlab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, writers, and agents use this skill to convert trusted Markdown documents into formatted PDF files from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown image links can embed local image files into the generated PDF. <br>
Mitigation: Use trusted Markdown, review image paths before conversion, and remove image references that should not be included. <br>
Risk: Careless output paths can place generated PDFs in unintended locations. <br>
Mitigation: Choose the output path deliberately with the --output option and review the target location before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araa47/md-2-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF file generated from Markdown, with optional terminal status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and Python 3.10 or newer; uses reportlab to render local Markdown content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
