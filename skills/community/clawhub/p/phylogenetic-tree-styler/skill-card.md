## Description:

Analyze data with `phylogenetic-tree-styler` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and analysts use this skill to style Newick phylogenetic trees with taxonomy color blocks, bootstrap labels, and optional timeline context for review-ready analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are not pinned, which can affect reproducibility or introduce dependency risk over time.

Mitigation: Install the skill in an isolated Python environment and review or pin ete3, matplotlib, numpy, and pandas before use.

Risk: The script reads user-provided input paths and writes user-provided output paths without enforcing workspace restrictions itself.

Mitigation: Run it in a sandboxed workspace and pass only trusted, explicit input and output paths.

Risk: The skill executes local Python code to generate visualization files.

Mitigation: Run a non-destructive smoke check such as `python -m py_compile scripts/main.py` before executing file-dependent commands.

## Reference(s):

- [Runtime Checklist](references/runtime_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated image files such as PNG, PDF, or SVG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit input and output paths; optional taxonomy CSV, bootstrap threshold, timeline, size, color, and DPI parameters control the rendered tree.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
