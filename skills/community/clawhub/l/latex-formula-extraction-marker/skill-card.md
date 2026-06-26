## Description: <br>
Convert PDF documents to Markdown using marker_single while preserving LaTeX formulas, equations, and document structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical document reviewers use this skill to convert selected PDFs, especially academic or technical papers with mathematical notation, into Markdown for downstream analysis or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs marker_single from the third-party marker-pdf package on local PDF inputs. <br>
Mitigation: Install and run it only in environments where that local conversion tool is acceptable, and use a sandbox for sensitive or untrusted documents. <br>
Risk: Using --keep-temp or cleanup=false leaves extracted Markdown and conversion artifacts on disk. <br>
Mitigation: Use the default cleanup behavior for sensitive files, or remove retained output directories after inspection. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/wu-uk/latex-formula-extraction-marker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown text returned by the Python API or printed by the command-line script, with usage guidance and example commands in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs marker_single locally with image extraction disabled; temporary conversion output is deleted by default unless the caller keeps it for inspection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
