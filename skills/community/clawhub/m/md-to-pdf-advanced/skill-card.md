## Description: <br>
Convert Markdown files to PDF using WeasyPrint, Pandoc, or wkhtmltopdf with support for syntax highlighting, tables, images, custom CSS themes, and page styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[20181112523](https://clawhub.ai/user/20181112523) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert Markdown documents into PDF reports with selectable rendering backends, themes, page layout options, and image/table support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may install unpinned Python packages during normal use. <br>
Mitigation: Use a virtual environment or container and preinstall reviewed, pinned dependencies before running conversions. <br>
Risk: Rendering Markdown may fetch network resources or process local file references. <br>
Mitigation: Avoid converting untrusted Markdown unless remote URLs and local file references have been reviewed, and run with restricted network and filesystem access where practical. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/20181112523/md-to-pdf-advanced) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Markdown to PDF Script](artifact/scripts/md_to_pdf.py) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PDF files plus Markdown usage guidance and shell or Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes PDF output to a specified path; may use WeasyPrint, Pandoc, or wkhtmltopdf depending on installed dependencies.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
