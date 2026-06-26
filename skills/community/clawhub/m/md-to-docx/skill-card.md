## Description: <br>
Converts Markdown files to formatted Word (.docx) documents with optional Word template style detection and Mermaid diagram rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krabww](https://clawhub.ai/user/krabww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and documentation teams use this skill to convert Markdown drafts, reports, and book chapters into Word documents while preserving common Markdown structure and optional template styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt installation of Python and Node dependencies. <br>
Mitigation: Install dependencies only in an approved environment and review package installation commands before execution. <br>
Risk: Mermaid rendering uses local browser automation and server evidence notes sandbox protections are disabled. <br>
Mitigation: Avoid untrusted Mermaid blocks or run conversion in a disposable or sandboxed environment. <br>
Risk: Implicit input or output paths can affect sensitive working directories. <br>
Mitigation: Use explicit input and output paths and review the target directory before running conversion. <br>
Risk: When no template is supplied, the output uses Chinese publishing defaults. <br>
Mitigation: Provide a trusted .doc or .docx template when a different house style or locale is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krabww/md-to-docx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated .docx file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can produce a Word .docx document from a Markdown input file and may embed Mermaid diagrams as PNG images when local dependencies are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
