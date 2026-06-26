## Description: <br>
Manage and optimize Jupyter notebooks by converting notebooks, extracting code cells, running notebooks headlessly, exporting to PDF/HTML, clearing outputs, and inspecting notebook metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Jupyter notebook workflows, including conversion, code extraction, headless execution, output cleanup, and metadata inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The run command executes notebook code with the user's privileges. <br>
Mitigation: Use the run command only with trusted notebooks, preferably in an isolated environment. <br>
Risk: The clean command overwrites notebook outputs by default when run in place. <br>
Mitigation: Back up notebooks or request a non-in-place cleaned copy before clearing outputs. <br>
Risk: The security scan notes insufficient warning or documentation around execution and overwrite behavior. <br>
Mitigation: Review command effects before execution and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/jupyter-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell commands and generated notebook, code, HTML, Markdown, PDF, reStructuredText, or LaTeX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the invoked notebook command and local nbconvert/Python environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
