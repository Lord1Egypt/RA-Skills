## Description: <br>
Converts Markdown files into formatted PDFs with Pandoc and Typst, including support for headings, tables, code blocks, links, emojis, and GitHub-style formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansschinkenwurst78-dev](https://clawhub.ai/user/hansschinkenwurst78-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to convert local Markdown notes, reports, or generated content into formatted PDF files next to the source Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion script creates hidden temporary Typst files in the input document folder and may overwrite or remove existing files with matching temporary names. <br>
Mitigation: Run the skill only in folders where hidden files named like .<document>.typ or .<document>_styled.typ are not important, or isolate the input Markdown in a working directory before conversion. <br>
Risk: The skill runs a local shell script against Markdown files and depends on locally installed Pandoc and Typst binaries. <br>
Mitigation: Use trusted Pandoc and Typst installations and run the script only on Markdown files from trusted sources. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/hansschinkenwurst78-dev/openclaw-md2pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Shell command output and a generated PDF file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Pandoc and Typst installations; writes the PDF next to the source Markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
