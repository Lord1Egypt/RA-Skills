## Description: <br>
A research-paper reading and reproduction assistant that parses PDFs or paper links, generates structured reports, finds code and datasets, scaffolds reproduction code, and designs experiments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Limax666](https://clawhub.ai/user/Limax666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, developers, and engineers use this skill to analyze papers, assess reproducibility, and create starter reports, code scaffolds, and experiment plans for reproducing results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scaffold paths can escape the chosen output directory when paper metadata is crafted. <br>
Mitigation: Use a dedicated temporary output directory, inspect generated paths and files, and avoid scaffolding from untrusted PDFs or JSON metadata. <br>
Risk: Generated training code, requirements, and research reports may be incomplete or unsuitable for direct execution. <br>
Mitigation: Review generated requirements, scripts, and reports before running training code or relying on the results. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/Limax666/paper-research-assistant) <br>
- [Code style guide](artifact/code_style.md) <br>
- [Experiment design guide](artifact/experiment_design.md) <br>
- [Report template](artifact/report_template.md) <br>
- [CMU experiment design reference](https://www.cs.cmu.edu/~aarti/Class/10701/experiment_design.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON metadata, Python code scaffolds, shell commands, and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files and commands should be reviewed before execution, publication, or reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
