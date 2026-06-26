## Description: <br>
Creates a presentation-ready copy of a NotebookLM-exported slide-deck PDF by masking the small visible NotebookLM footer badge at the bottom-right of each page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fudanjx](https://clawhub.ai/user/fudanjx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create a cleaned copy of a NotebookLM slide-deck PDF for sharing, presenting, or emailing while preserving the original file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The mask can cover content if used on an unsuitable PDF or with incorrect coordinates. <br>
Mitigation: Use the skill only for NotebookLM slide-deck PDFs with the expected footer badge, keep the original PDF, and spot-check the output before sharing. <br>
Risk: Optional metadata or annotation stripping can remove authorship, comments, links, review history, or other information recipients should see. <br>
Mitigation: Leave metadata and annotation stripping disabled unless removal is intentional and appropriate for the document. <br>
Risk: Using --force can overwrite an existing output file. <br>
Mitigation: Choose a distinct output path or review the existing output before rerunning with --force. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fudanjx/notebooklm-pdf-cleaner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fudanjx) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF file output with Markdown instructions and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a new *-clean.pdf by default; inspect mode emits text diagnostics instead of writing a file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
