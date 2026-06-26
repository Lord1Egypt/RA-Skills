## Description: <br>
Run a protein-ligand docking workflow for research questions about target binding, selectivity, and structural plausibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zackz2025](https://clawhub.ai/user/zackz2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, developers, and computational biology teams use this skill to assess whether a ligand may plausibly bind a protein target, compare homolog selectivity, and decide whether docking evidence is strong enough to continue. It guides sequence retrieval, structure search, AlphaFold quality checks, AutoDock Vina docking, and cautious interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scientific tools and external executables such as OpenBabel and AutoDock Vina can affect the reliability and safety of execution if paths or binaries are untrusted. <br>
Mitigation: Use trusted executable paths, run the workflow in a dedicated project directory, and install only when comfortable running local scientific analysis tools. <br>
Risk: Protein, ligand, and project data may be sensitive when sent to external services such as UniProt, RCSB, or Google Colab. <br>
Mitigation: Avoid sending confidential protein, ligand, or project data to external services unless that sharing is acceptable. <br>
Risk: Docking and AlphaFold-derived results can be misleading if model quality, interface confidence, or docking poses are weak. <br>
Mitigation: Review generated reports before relying on them, stop when confidence is poor, and separate computational plausibility from experimental validation. <br>


## Reference(s): <br>
- [Decision Guide](references/decision-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/zackz2025/protein-ligand-docking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell and Python commands plus JSON, structure, report, and figure files when the workflow reaches those stages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include FASTA files, selected PDB IDs or modeled structures, alignment summaries, model-quality JSON, docking-summary JSON, short written conclusions, Summary.md, Summary.docx, and figures.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
