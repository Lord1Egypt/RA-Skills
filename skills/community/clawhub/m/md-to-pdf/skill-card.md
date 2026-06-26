## Description: <br>
Converts Markdown files into styled PDF documents with an optional cover page, table of contents, Chinese text support, emoji support, code highlighting, and table formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanghaiyangming](https://clawhub.ai/user/shanghaiyangming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and agent operators can use this skill to turn Markdown reports or documents into polished PDF files with consistent print styling. It is most useful when a workflow needs a generated PDF artifact from Markdown source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown is rendered in a browser-based PDF workflow, so unsafe or sensitive Markdown can expose content during rendering. <br>
Mitigation: Use the skill only for Markdown you are comfortable rendering in a browser and review generated PDFs before sharing them. <br>
Risk: The Chrome debugging workflow is broad and can interact with an existing browser profile. <br>
Mitigation: Use an isolated Chrome profile for the debugging port when running the converter. <br>
Risk: Mermaid rendering may load a third-party script, and the documented QQ Bot flow can send generated PDFs externally. <br>
Mitigation: Use --no-mermaid for untrusted or sensitive documents unless Mermaid is vendored locally, and require explicit approval before copying or sending PDFs to QQ Bot media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shanghaiyangming/md-to-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PDF file with command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional cover pages, table of contents generation, custom CSS, and Mermaid rendering when enabled.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata; changelog: v4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
