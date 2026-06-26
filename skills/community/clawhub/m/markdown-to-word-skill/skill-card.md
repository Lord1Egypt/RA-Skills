## Description: <br>
Provides documentation and Python scripts for converting Markdown files into Word documents, including batch conversion, images, tables, code blocks, formulas, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runmanfm-bit](https://clawhub.ai/user/runmanfm-bit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert one or more Markdown documents into Word .docx files and to apply optional document styling, templates, image handling, and conversion reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install script and conversion scripts execute local commands and install Python dependencies. <br>
Mitigation: Review scripts before use, install in a virtual environment, and run from a disposable or controlled workspace. <br>
Risk: Markdown with image support can embed referenced local images, including files addressed by absolute paths. <br>
Mitigation: Convert only trusted Markdown or disable image support; use narrow input, output, and image directories. <br>
Risk: The shipped scripts appear incomplete and may not run as documented. <br>
Mitigation: Run a small test conversion before relying on the skill for production documents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/runmanfm-bit/markdown-to-word-skill) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also produce JSON batch conversion reports when the batch script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-03-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
