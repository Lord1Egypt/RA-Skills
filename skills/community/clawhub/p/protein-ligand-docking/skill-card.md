## Description:

Run a protein-ligand docking workflow for research questions about target binding, selectivity, and structural plausibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zackz2025](https://clawhub.ai/user/zackz2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and scientific analysts use this skill to plan and interpret protein-ligand docking workflows for binding plausibility, homolog selectivity, and structure-quality decisions. It helps decide when to continue with sequence checks, structure search, AlphaFold/Colab modeling, AutoDock Vina docking, or a structured report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The docking helper can execute an AutoDock Vina binary path supplied by the user.

Mitigation: Use a trusted absolute path for AutoDock Vina and avoid attacker-controlled --vina_path values.

Risk: The report generator writes Markdown and DOCX files using a caller-provided output name.

Mitigation: Run reports in a dedicated least-privilege workspace and avoid output names that could overwrite unintended .md or .docx files.

Risk: Docking and AlphaFold-derived results can be scientifically misleading when structure confidence, interface confidence, or pose quality is poor.

Mitigation: Apply the documented pLDDT, PAE, grid-box, pose, and binding-score checks, and state that experimental assays remain the standard for validation.

## Reference(s):

- [Decision Guide](references/decision-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/zackz2025/skills/protein-ligand-docking)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, Markdown, DOCX, and docking output files when helper scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce FASTA files, selected structure IDs, alignment JSON, model-quality JSON, docking summary JSON, Summary.md, Summary.docx, and figure output depending on the workflow stage reached.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
