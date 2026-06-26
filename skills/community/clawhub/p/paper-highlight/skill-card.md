## Description: <br>
Automatically highlight academic papers by 5 semantic categories - goal, motivation, method, results, contributions - to help you quickly skim a paper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yorch233](https://clawhub.ai/user/yorch233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, reviewers, and engineers use this skill to preflight an academic PDF, identify reusable paper content, and produce an annotated copy with stable semantic highlight colors and optional summary notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script reads user-selected PDFs and writes annotated copies, which may expose or alter sensitive paper content if outputs are shared carelessly. <br>
Mitigation: Use the skill only on PDFs you are comfortable processing locally, keep originals backed up, and review annotated PDFs and generated notes before sharing. <br>
Risk: The setup installs PyMuPDF into a local Python environment, so dependency changes could affect behavior over time. <br>
Mitigation: Use an isolated environment and consider pinning PyMuPDF during setup for repeatable runs. <br>
Risk: Automatic highlights and notes can be noisy or misleading for dense, long, or image-heavy papers. <br>
Mitigation: Use the preflight gate, choose conservative density settings when needed, and review the output before relying on the annotations. <br>


## Reference(s): <br>
- [Highlight Rules](references/highlight-rules.md) <br>
- [Paper Highlight on ClawHub](https://clawhub.ai/yorch233/paper-highlight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script writes an annotated PDF and can write a JSON report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-selected PDF and local Python environment with PyMuPDF; supports highlight density, opacity, optional categories, note mode, output path, dry-run, and JSON report controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
