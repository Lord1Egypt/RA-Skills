## Description: <br>
Converts documents between Word (.docx), Markdown, and related formats using pandoc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mo-yuhua](https://clawhub.ai/user/mo-yuhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to read, create, edit, and convert Word, Markdown, and related local documents with pandoc. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document conversion or edit operations can overwrite important local files if output paths are chosen carelessly. <br>
Mitigation: Keep backups before edit or replace operations and review input and output paths before running the scripts. <br>
Risk: The skill depends on local document tooling such as pandoc and optional converters. <br>
Mitigation: Install required tools from trusted package managers and run the skill only on files the user intends to process. <br>


## Reference(s): <br>
- [Supported formats](references/supported-formats.md) <br>
- [Pandoc official documentation](https://pandoc.org/) <br>
- [Pandoc user guide](https://pandoc.org/MANUAL.html) <br>
- [ClawHub skill page](https://clawhub.ai/mo-yuhua/pandoc-docx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, create, convert, or edit local document files specified by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
