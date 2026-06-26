## Description: <br>
Convert Markdown files to fully formatted Word DOCX documents with support for tables, images, code blocks, and GitHub Flavored Markdown features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoeCao](https://clawhub.ai/user/JoeCao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and document automation users use this skill to convert Markdown source files into editable Word DOCX documents while preserving common formatting, tables, images, code blocks, and GitHub Flavored Markdown features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown from untrusted sources can include remote image references that trigger outbound network requests during conversion. <br>
Mitigation: Review or remove remote image references before conversion, especially for documents from outside trusted sources. <br>
Risk: Markdown image paths can reference local files that may be embedded into the generated DOCX. <br>
Mitigation: Review local image paths before conversion and run the converter from a directory that limits access to intended assets. <br>
Risk: An implicit output filename can overwrite an existing DOCX when paths collide. <br>
Mitigation: Choose an explicit output filename and check the destination before running the conversion. <br>
Risk: The converter depends on npm packages installed from the JavaScript package ecosystem. <br>
Mitigation: Install only when the dependency set is acceptable for the target environment and follow local dependency review practices. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/JoeCao/joe-markdown-to-docx) <br>
- [Publisher profile](https://clawhub.ai/user/JoeCao) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX file output with terminal status messages and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converts one Markdown input file to one DOCX output file per command invocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
