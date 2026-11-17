## Description:

Manage and optimize Jupyter notebooks by converting notebooks, extracting code cells, running notebooks headlessly, exporting to PDF or HTML, clearing outputs, and inspecting notebook metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate on Jupyter notebooks from an agent workflow, including conversion, code-cell extraction, headless execution, output cleanup, and metadata inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public command list does not match the script's supported notebook commands, which can confuse users about intended behavior.

Mitigation: Review the installed script help and source before use, and rely only on commands that are actually dispatched by the script.

Risk: Headless notebook execution can run code contained in the notebook.

Mitigation: Execute only trusted notebooks, preferably in an isolated environment with explicit dependency review.

Risk: The cleanup command can overwrite notebooks in place by default.

Mitigation: Keep backups and request non-in-place cleanup unless overwriting the original notebook is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/jupyter-helper)
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown-style guidance with shell commands and generated notebook, code, or document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notebook execution and conversion depend on local Python, nbconvert, and the notebook's runtime dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
